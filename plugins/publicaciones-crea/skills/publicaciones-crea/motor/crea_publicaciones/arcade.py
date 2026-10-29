"""Estilo «arcade»: la lámina como una pantalla del taller «CREA tu propio videojuego».

Gramática tomada del estilo pixel-rpg de lemo-opuscar: todo lo que no es la foto vive en un lienzo
de 270 × 338 píxeles que se amplía ×4 sin suavizar; los degradados son tramado ordenado (Bayer),
nunca mezclas; la bajada es una caja de diálogo con retrato que, en un video, se escribe al ritmo
de la lectura. La foto real va entera, sin pixelar, dentro de una ventana de bordes en escalera.
Nada se toma de juegos comerciales: corazones, estrellas, cerros y letras salen del código; el
retrato es CREABOT, el robot de CREA.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFilter

from .base import (DARK, ILUSTRACIONES, MARGEN, WHITE, B, ErrorCREA, M, O, Pieza, T, Y, cubrir, envolver, font,
                   recortar_capa)
from .marco import ruta_icono

ESC = 4
ANCHO, ALTO = 1080, 1350
LW, LH = ANCHO // ESC, (ALTO + ESC - 1) // ESC
NOCHE = ('#0E1430', '#152044', '#1B2C5E', '#21397A')    # del cielo alto al horizonte
TINTA, PLATA = '#0B0F1E', '#B8C4D6'
VENTANA = (18, 40, 252, 176)       # la foto, en píxeles del lienzo chico (full: 72, 160, 1008, 704)
BAYER = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))
CORAZON = ('.XX.XX.', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...')
VELOCIDAD = 38                     # letras por segundo al escribir el diálogo


def _rgb(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def cielo(chico):
    """Degradado nocturno por tramado de Bayer, estrellas y dos capas de cerros."""
    d = ImageDraw.Draw(chico)
    tramos = len(NOCHE) - 1
    for y in range(LH):
        pos = y / LH * tramos
        i, f = int(pos), pos - int(pos)
        a, b = NOCHE[min(i, tramos)], NOCHE[min(i + 1, tramos)]
        for x in range(LW):
            d.point((x, y), fill=b if f * 16 > BAYER[y % 4][x % 4] else a)
    rnd = random.Random(5)
    for _ in range(70):
        x, y = rnd.randrange(LW), rnd.randrange(int(LH * 0.6))
        d.point((x, y), fill=rnd.choice((WHITE, WHITE, Y, '#9FD8E6')))
    for _ in range(6):
        x, y = rnd.randrange(8, LW - 8), rnd.randrange(8, int(LH * 0.5))
        d.line([(x - 2, y), (x + 2, y)], fill=WHITE)
        d.line([(x, y - 2), (x, y + 2)], fill=WHITE)
    for color, base, amp, fase in (('#16306E', LH - 42, 10, 0.0), ('#0F214F', LH - 26, 7, 1.7)):
        for x in range(LW):
            h = base - int(amp * (0.6 * math.sin(x / 23 + fase) + 0.4 * math.sin(x / 9 + fase * 2)))
            d.line([(x, h), (x, LH)], fill=color)


def caja_pixel(d, caja, relleno=None):
    """Borde de tres capas (tinta, blanco, plata) por fuera de `caja`, como las ventanas de los juegos."""
    x0, y0, x1, y1 = caja
    for k, color in ((3, TINTA), (2, WHITE), (1, PLATA)):
        d.rectangle([x0 - k, y0 - k, x1 + k - 1, y1 + k - 1], outline=color)
    if relleno:
        d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=relleno)


def corazon(d, x, y, color):
    for j, fila in enumerate(CORAZON):
        for i, c in enumerate(fila):
            if c == 'X':
                d.point((x + i, y + j), fill=color)


def texto_pixel(texto, tam, ancho, peso='eb', colores=(WHITE,), contorno=TINTA, max_lineas=2):
    """Texto a píxel: Montserrat a tamaño chico, umbral duro, degradado por filas y contorno de 8 vecinos.

    Devuelve (imagen RGBA del lienzo chico, tamaño final, recortado). Baja de tamaño hasta caber.
    """
    original = tam
    while True:
        f = font(tam, peso)
        lineas = envolver(texto, f, ancho)
        if len(lineas) <= max_lineas or tam <= 7:
            break
        tam -= 1
    recortado = len(lineas) > max_lineas
    lineas = lineas[:max_lineas]
    alto_l = int(tam * 1.18)
    mask = Image.new('L', (ancho + 4, alto_l * len(lineas) + 6), 0)
    md = ImageDraw.Draw(mask)
    for i, ln in enumerate(lineas):
        md.text((2, 2 + i * alto_l), ln, font=f, fill=255)
    mask = mask.point(lambda v: 255 if v > 110 else 0)
    alto = mask.height
    relleno = Image.new('RGBA', mask.size, (0, 0, 0, 0))
    rd = ImageDraw.Draw(relleno)
    for y in range(alto):
        color = colores[min(len(colores) - 1, (y % alto_l) * len(colores) // alto_l)]
        rd.line([(0, y), (mask.width, y)], fill=color)
    out = Image.new('RGBA', mask.size, (0, 0, 0, 0))
    if contorno:
        borde = mask.filter(ImageFilter.MaxFilter(3))
        out.paste(Image.new('RGBA', mask.size, contorno), (0, 0), borde)
    out.paste(relleno, (0, 0), mask)
    return out, tam, recortado or tam < original * 0.85


def _ampliar(im):
    return im.resize((im.width * ESC, im.height * ESC), Image.NEAREST)


def item(clave, color, lado=14):
    """Un ícono como objeto del inventario: casilla con borde y el ícono pixelado."""
    s = Image.new('RGBA', (lado + 2, lado + 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    d.rectangle([0, 0, lado + 1, lado + 1], fill=TINTA)
    d.rectangle([1, 1, lado, lado], fill=color)
    g = Image.open(ruta_icono(clave, 'd' if color == Y else 'w')).convert('RGBA').resize((lado - 4, lado - 4),
                                                                                          Image.LANCZOS)
    g.putalpha(g.getchannel('A').point(lambda v: 255 if v > 120 else 0))
    s.alpha_composite(g, (3, 3))
    return s


def retrato(lado=28):
    bot = Image.open(ILUSTRACIONES / 'creabot.png').convert('RGBA')
    bot = bot.resize((round(bot.width * lado / bot.height), lado), Image.LANCZOS)
    bot.putalpha(bot.getchannel('A').point(lambda v: 255 if v > 128 else 0))
    return bot


def colocador(foco, ajuste):
    x0, y0, x1, y1 = (v * ESC for v in VENTANA)

    def colocar(dest, img, sombra=True):
        dest.alpha_composite(cubrir(img, x1 - x0, y1 - y0, 0, foco, ajuste), (x0, y0))
        return (x0, y0, x1, y1)
    return colocar


def _chico():
    return Image.new('RGBA', (LW, LH), (0, 0, 0, 0))


def armar(p, foto, *, titulo, bajada, chip, acento, iconos, foco, ajuste, nivel=None):
    """Arma la lámina pieza por pieza (cada una queda en `p.capas` para animarla).

    Devuelve (capa de encima por cuadro, colocador de la foto, base sin el diálogo).
    """
    capas = []

    def poner(chico, nombre, rol, encima=False, grande=None):
        c = recortar_capa(grande if grande is not None else _ampliar(chico).crop((0, 0, ANCHO, ALTO)), nombre, rol,
                          encima)
        if c:
            capas.append(c)

    fondo = Image.new('RGBA', (LW, LH), NOCHE[0])
    cielo(fondo)
    poner(fondo, 'fondo', 'fondo')

    # La ventana de la foto, con esquinas de corchete.
    ch = _chico()
    d = ImageDraw.Draw(ch)
    caja_pixel(d, VENTANA)
    for (x, y, dx, dy) in ((VENTANA[0] - 6, VENTANA[1] - 6, 1, 1), (VENTANA[2] + 5, VENTANA[1] - 6, -1, 1),
                           (VENTANA[0] - 6, VENTANA[3] + 5, 1, -1), (VENTANA[2] + 5, VENTANA[3] + 5, -1, -1)):
        d.line([(x, y), (x + 4 * dx, y)], fill=Y)
        d.line([(x, y), (x, y + 4 * dy)], fill=Y)
    poner(ch, 'ventana', 'ventana')
    colocar = colocador(foco, ajuste)
    grande = Image.new('RGBA', (ANCHO, ALTO), (0, 0, 0, 0))
    colocar(grande, foto)
    poner(None, 'foto', 'foto', grande=grande)
    p._anotar(tuple(v * ESC for v in VENTANA), 'foto')

    # Barra de arriba: nivel o etiqueta, vidas e inventario.
    etiqueta = f'NIVEL {nivel}' if nivel else (chip or 'CREA').upper()
    hud, _, _ = texto_pixel(etiqueta, 11, 120, colores=(Y, O), max_lineas=1)
    ch = _chico()
    ch.alpha_composite(hud, (MARGEN // ESC, 18))
    poner(ch, 'hud', 'hud')
    # La barra de arriba es marco, como el logo: puede quedar fuera de la cuadrícula del perfil.
    p._anotar((MARGEN, 18 * ESC, MARGEN + hud.width * ESC, (18 + hud.height) * ESC), f'hud:{etiqueta}')
    for i in range(5):
        ch = _chico()
        corazon(ImageDraw.Draw(ch), 104 + i * 9, 21, M)
        poner(ch, f'corazon-{i}', 'corazon')
    for i, clave in enumerate(iconos):
        ch = _chico()
        ch.alpha_composite(item(clave, (T, O, M, Y, B)[i % 5]), (LW - MARGEN // ESC - 16 - i * 19, 17))
        poner(ch, f'item-{i}', 'item')

    # Título en letras de píxel, con degradado amarillo-naranja por filas, una capa por palabra.
    ancho_tit = VENTANA[2] - VENTANA[0] - 4
    tit, tam, ajustado = texto_pixel(titulo.upper(), 20, ancho_tit, colores=(Y, Y, O))
    y_tit = VENTANA[3] + 14
    if ajustado:
        p.notas.append(f'título encogido o recortado para caber: "{titulo[:40]}". Acórtalo')
    f = font(tam, 'eb')
    alto_l = int(tam * 1.18)
    k = 0
    for n, linea in enumerate(envolver(titulo.upper(), f, ancho_tit)[:2]):
        inicio = 0
        for w in linea.split(' '):
            img, _, _ = texto_pixel(w, tam, 400, colores=(Y, Y, O), max_lineas=1)
            ch = _chico()
            ch.alpha_composite(img, (VENTANA[0] + int(f.getlength(linea[:inicio])), y_tit + n * alto_l))
            poner(ch, f'titulo-{k}', 'palabra')
            inicio += len(w) + 1
            k += 1
    tx0, ty0, tx1, ty1 = tit.getbbox()
    p._anotar(((VENTANA[0] + tx0) * ESC, (y_tit + ty0) * ESC, (VENTANA[0] + tx1) * ESC, (y_tit + ty1) * ESC),
              f'texto:{titulo[:28]}')

    # La caja de diálogo con el retrato. Termina antes del logo, que tiene su esquina abajo a la derecha.
    texto_x = VENTANA[0] + 36
    fin_dialogo = (ANCHO - MARGEN - 120 - 24) // ESC
    ancho_texto = fin_dialogo - texto_x - 6
    lineas_dlg = envolver(bajada, font(10, 'b'), ancho_texto) if bajada else []
    y_dlg = y_tit + tit.height + 8
    dialogo = (VENTANA[0], y_dlg, fin_dialogo, y_dlg + max(36, 12 * min(3, len(lineas_dlg)) + 12))
    if bajada:
        ch = _chico()
        caja_pixel(ImageDraw.Draw(ch), dialogo, relleno='#13204D')
        ch.alpha_composite(retrato(), (dialogo[0] + 4, dialogo[1] + 6))
        poner(ch, 'dialogo', 'dialogo')
        if len(lineas_dlg) > 3:
            p.notas.append(f'la bajada no cabe en la caja de diálogo (3 líneas): "{bajada[:40]}". Acórtala')
        p._anotar((texto_x * ESC, (dialogo[1] + 5) * ESC, (dialogo[2] - 4) * ESC, (dialogo[3] - 2) * ESC),
                  f'texto:{bajada[:28]}')
    logo = Pieza(p.formato, fondo=(0, 0, 0, 0))
    logo.logo(ancho=120, y=1158)
    p.cajas += logo.cajas
    poner(None, 'logo', 'logo', grande=logo.im)

    fps = 30

    def escrito(n, cursor):
        capa = _chico()
        if bajada:
            txt, _, _ = texto_pixel(bajada[:n] or ' ', 10, ancho_texto, peso='b', colores=(WHITE,), contorno=None,
                                    max_lineas=3)
            capa.alpha_composite(txt, (texto_x, dialogo[1] + 5))
            if cursor and n >= len(bajada):
                cx, cy = dialogo[2] - 8, dialogo[3] - 6
                ImageDraw.Draw(capa).polygon([(cx - 2, cy - 2), (cx + 2, cy - 2), (cx, cy + 1)], fill=Y)
        return capa

    if bajada:
        # Una capa por línea del diálogo: en la animación se escriben una tras otra.
        alto_dlg = int(10 * 1.18)
        for n, linea in enumerate(envolver(bajada, font(10, 'b'), ancho_texto)[:3]):
            txt, _, _ = texto_pixel(linea, 10, ancho_texto + 40, peso='b', colores=(WHITE,), contorno=None,
                                    max_lineas=1)
            ch = _chico()
            ch.alpha_composite(txt, (texto_x, dialogo[1] + 5 + n * alto_dlg))
            antes = len(capas)
            poner(ch, f'dialogo-linea-{n}', 'escritura', encima=True)
            if len(capas) > antes:
                capas[-1].letras = len(linea)
        ch = _chico()
        cx, cy = dialogo[2] - 8, dialogo[3] - 6
        ImageDraw.Draw(ch).polygon([(cx - 2, cy - 2), (cx + 2, cy - 2), (cx, cy + 1)], fill=Y)
        poner(ch, 'cursor', 'cursor', encima=True)

    def encima(i=None):
        """La caja de diálogo escrita hasta el cuadro `i` (None: completa, para la imagen fija)."""
        n = len(bajada or '') if i is None else int(i / fps * VELOCIDAD)
        return _ampliar(escrito(n, i is None or (i // 12) % 2 == 0)).crop((0, 0, ANCHO, ALTO))

    # La lámina estática es la suma de las capas, en orden.
    p.im.paste(capas[0].img, (0, 0))
    for c in capas[1:]:
        if not c.encima:
            p.im.alpha_composite(c.img, (c.x, c.y))
    base = p.im.copy()
    p.im.alpha_composite(encima())
    p.capas = capas
    return encima, colocar, base


def comprobar_nivel(nivel):
    if nivel is not None and not (isinstance(nivel, int) and 0 < nivel < 100):
        raise ErrorCREA('El nivel es el número de la lámina: un entero de 1 a 99')
