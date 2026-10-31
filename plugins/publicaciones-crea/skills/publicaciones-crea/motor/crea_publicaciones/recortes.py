"""Estilo «recortes»: la lámina como un collage impreso sobre papel.

Gramática tomada del estilo halftone-dossier y del papercut de lemo-opuscar y de la estética de
gbro-collage-broll: papel crema con grano, semitono en las tintas de la marca, la foto como una
copia impresa pegada con cinta, sellos de goma, stickers recortados con borde blanco y un titular
con la sombra corrida de una impresión mal registrada. Los motivos son los de la pared del
laboratorio: la línea con puntos y el rayo dibujado a mano.
"""
import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from .base import (BODY, CUERPO, DARK, ILUSTRACIONES, MARGEN, MASCOTA, TITULO, WHITE, B, ErrorCREA, M, Pieza, T, Y, cubrir,
                   font, palabras, recortar_capa)
from .marco import colores_iconos, ruta_icono

ANCHO, ALTO = 1080, 1350
PAPEL = '#F7F1E6'
FOTO = (840, 600)                 # la foto dentro de la copia impresa
BORDE = 20                        # el margen blanco de la copia
CENTRO_FOTO = (540, 432)
GIRO = -2.5
STICKERS = {'creabot': ILUSTRACIONES / 'creabot.png', 'seneca': MASCOTA / 'seneca_baile.png'}


def sticker_personaje(nombre):
    """'creabot' o 'seneca' (los dibujos originales), o una pose: 'creabot:salta', 'seneca:baile-espejo'."""
    if nombre in STICKERS:
        return Image.open(STICKERS[nombre]).convert('RGBA')
    quien, _, pose = nombre.partition(':')
    from . import personajes
    if quien == 'creabot' and pose:
        return personajes.creabot(pose, alto=600)
    if quien == 'seneca' and pose:
        return personajes.seneca(pose, alto=600)
    raise ErrorCREA(f'El sticker "{nombre}" no existe. Usa "creabot", "seneca", "creabot:<pose>" o "seneca:<pose>" '
                    f'(poses en referencia/personajes.md)')


ANCHO_TEXTO = 700                 # deja la columna derecha al sticker


def _ruido(w, h, escala, amplitud, semilla):
    """Ruido de valor reproducible: un mosaico pequeño ampliado. Devuelve una imagen L centrada en 128."""
    rnd = random.Random(semilla)
    chico = Image.new('L', (max(1, w // escala), max(1, h // escala)))
    chico.putdata([128 + rnd.randint(-amplitud, amplitud) for _ in range(chico.width * chico.height)])
    return chico.resize((w, h), Image.BICUBIC if escala > 8 else Image.NEAREST)


def papel(p):
    """Papel crema con manchas suaves y grano fino."""
    p.fondo(PAPEL)
    rgb = p.im.convert('RGB')
    for escala, amplitud, semilla, fuerza in ((40, 40, 11, 0.5), (3, 40, 12, 0.35)):
        gris = _ruido(p.w, p.h, escala, amplitud, semilla)
        rgb = Image.blend(rgb, ImageChops.soft_light(rgb, Image.merge('RGB', (gris, gris, gris))), fuerza)
    p.im.paste(rgb.convert('RGBA'))


def semitono(p, centro, alcance, color, paso=24, angulo=15, k=0.72):
    """Puntos de semitono cuya talla sigue la distancia a `centro`, impresos en multiplicar."""
    capa = Image.new('RGB', p.im.size, 'white')
    d = ImageDraw.Draw(capa)
    a = math.radians(angulo)
    ca, sa = math.cos(a), math.sin(a)
    n = int(max(p.w, p.h) * 1.5 / paso)
    for i in range(-n, n):
        for j in range(-n, n):
            x = centro[0] + (i * ca - j * sa) * paso
            y = centro[1] + (i * sa + j * ca) * paso
            if not (-paso < x < p.w + paso and -paso < y < p.h + paso):
                continue
            densidad = 1 - math.hypot(x - centro[0], y - centro[1]) / alcance
            if densidad <= 0.05:
                continue
            r = densidad * paso * k / 2 * 1.4
            d.ellipse([x - r, y - r, x + r, y + r], fill=color)
    mezcla = ImageChops.multiply(p.im.convert('RGB'), capa)
    p.im.paste(mezcla.convert('RGBA'))


def _copia(img, foco, ajuste):
    """La foto como copia impresa: margen blanco, girada."""
    w, h = FOTO
    copia = Image.new('RGBA', (w + 2 * BORDE, h + 2 * BORDE), WHITE)
    copia.alpha_composite(cubrir(img, w, h, 0, foco, ajuste), (BORDE, BORDE))
    return copia.rotate(GIRO, Image.BICUBIC, expand=True)


def _sombra(alfa, desvio=(10, 14), blur=12, fuerza=0.38):
    s = Image.new('RGBA', (alfa.width + 80, alfa.height + 80), (0, 0, 0, 0))
    a = Image.new('L', s.size, 0)
    a.paste(alfa.point(lambda v: int(v * fuerza)), (40 + desvio[0], 40 + desvio[1]))
    s.putalpha(a.filter(ImageFilter.GaussianBlur(blur)))
    tinta = Image.new('RGBA', s.size, DARK)
    tinta.putalpha(s.getchannel('A'))
    return tinta


def _pegar(dest, pieza, centro, con_sombra=True):
    x, y = centro[0] - pieza.width // 2, centro[1] - pieza.height // 2
    if con_sombra:
        dest.alpha_composite(_sombra(pieza.getchannel('A')), (x - 40, y - 40))
    dest.alpha_composite(pieza, (x, y))
    return (x, y, x + pieza.width, y + pieza.height)


def colocador(foco, ajuste):
    def colocar(dest, img, sombra=True):
        return _pegar(dest, _copia(img, foco, ajuste), CENTRO_FOTO, con_sombra=sombra)
    return colocar


def cinta(ancho=190, alto=52, angulo=0, semilla=0):
    """Un trozo de cinta de enmascarar, translúcido y con los bordes mordidos."""
    rnd = random.Random(semilla)
    c = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(c)
    puntos = [(0, 0)] + [(x, rnd.randint(0, 5)) for x in range(12, ancho, 12)] + [(ancho, 0)]
    puntos += [(ancho - rnd.randint(0, 6), alto)] + [(x, alto - rnd.randint(0, 5)) for x in range(ancho - 12, 0, -12)]
    puntos += [(rnd.randint(0, 6), alto)]
    d.polygon(puntos, fill=(235, 226, 18, 170))
    return c.rotate(angulo, Image.BICUBIC, expand=True)


def sello(texto, color, angulo=-8, semilla=3):
    """Sello de goma: doble borde redondeado, letra pesada y tinta irregular."""
    f = font(54, 'eb')
    bb = f.getbbox(texto)
    w, h = bb[2] - bb[0] + 64, bb[3] - bb[1] + 44
    s = Image.new('RGBA', (w + 16, h + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    d.rounded_rectangle([4, 4, w + 11, h + 11], 18, outline=color, width=9)
    d.rounded_rectangle([17, 17, w - 2, h - 2], 10, outline=color, width=4)
    d.text((8 + (w - (bb[2] - bb[0])) // 2 - bb[0], 8 + (h - (bb[3] - bb[1])) // 2 - bb[1]), texto, font=f, fill=color)
    # Tinta irregular: se comen pequeñas zonas, como en un sello real.
    mordida = _ruido(s.width, s.height, 4, 60, semilla).point(lambda v: 0 if v < 80 else 255)
    a = Image.composite(s.getchannel('A'), Image.new('L', s.size, 0), mordida)
    s.putalpha(a.point(lambda v: int(v * 0.95)))
    return s.rotate(angulo, Image.BICUBIC, expand=True)


def sticker_circular(clave, color, diametro=128, angulo=0):
    """Un ícono como sticker troquelado: círculo de color con borde blanco."""
    borde = 12
    s = Image.new('RGBA', (diametro + 2 * borde, diametro + 2 * borde), (0, 0, 0, 0))
    d = ImageDraw.Draw(s)
    d.ellipse([0, 0, s.width - 1, s.height - 1], fill=WHITE)
    d.ellipse([borde, borde, borde + diametro, borde + diametro], fill=color)
    glifo = Image.open(ruta_icono(clave, 'd' if color == Y else 'w')).convert('RGBA')
    lado = int(diametro * 0.58)
    glifo = glifo.resize((lado, lado), Image.LANCZOS)
    s.alpha_composite(glifo, ((s.width - lado) // 2, (s.height - lado) // 2))
    return s.rotate(angulo, Image.BICUBIC, expand=True)


def rayo(d, x, y, escala=1.0, color=DARK):
    """El rayo dibujado a mano de la pared del laboratorio."""
    pts = [(0, 0), (34, 58), (16, 62), (44, 118), (-4, 50), (16, 46), (-10, 4)]
    d.line([(x + px * escala, y + py * escala) for px, py in pts] + [(x, y)], fill=color, width=6, joint='curve')


def _lienzo():
    return Image.new('RGBA', (ANCHO, ALTO), (0, 0, 0, 0))


def armar(p, foto, *, titulo, bajada, chip, acento, iconos, foco, ajuste, sticker=None):
    """Arma la lámina pieza por pieza (cada una queda en `p.capas` para animarla).

    Devuelve (capa de encima, colocador de la foto, base sin la capa de encima).
    """
    capas = []

    def poner(lienzo, nombre, rol, encima=False):
        c = recortar_capa(lienzo, nombre, rol, encima)
        if c:
            capas.append(c)

    papel(p)
    semitono(p, (ANCHO + 60, -40), 560, acento)
    semitono(p, (-80, ALTO + 60), 470, M if acento != M else T, angulo=45)
    poner(p.im.copy(), 'fondo', 'fondo')
    lz = _lienzo()
    rayo(ImageDraw.Draw(lz), 40, 1150, 0.9)
    poner(lz, 'rayo', 'trazo')
    # La línea con puntos de la pared, al pie.
    lz = _lienzo()
    d = ImageDraw.Draw(lz)
    y = ALTO - 44
    d.line([(236, y), (ANCHO, y)], fill=DARK, width=5)
    for x, r in ((560, 13), (604, 8)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=T)
    poner(lz, 'circuito', 'trazo')

    # La foto como copia impresa, con su sombra aparte (en la animación la copia cae y la sombra aparece).
    copia = _copia(foto, foco, ajuste)
    cx, cy = CENTRO_FOTO[0] - copia.width // 2, CENTRO_FOTO[1] - copia.height // 2
    caja = (cx, cy, cx + copia.width, cy + copia.height)
    lz = _lienzo()
    lz.alpha_composite(_sombra(copia.getchannel('A')), (cx - 40, cy - 40))
    poner(lz, 'sombra-foto', 'sombra')
    lz = _lienzo()
    lz.alpha_composite(copia, (cx, cy))
    poner(lz, 'foto', 'foto')
    p._anotar((MARGEN, caja[1] + 10, ANCHO - MARGEN, caja[3] - 10), 'foto')

    # Titular con la sombra corrida de una impresión mal registrada, una capa por palabra.
    y_titulo = 836
    prueba = Pieza(p.formato, fondo=(0, 0, 0, 0))
    fin = prueba.texto(titulo, MARGEN, y_titulo, ancho=ANCHO_TEXTO, tam=TITULO - 4, peso='eb', color=DARK,
                       inter=1.04, max_lineas=2)
    p.notas += prueba.notas
    p.cajas += prueba.cajas
    for k, (img, x, y) in enumerate(palabras(titulo, MARGEN, y_titulo, ANCHO_TEXTO, prueba.ultimo_tam, 'eb', 1.04,
                                             DARK, sombra=acento)):
        lz = _lienzo()
        lz.alpha_composite(img, (x, y))
        poner(lz, f'titulo-{k}', 'palabra')
    if bajada:
        # La bajada va en una nota de papel blanco pegada sobre el collage.
        lineas = max(1, min(3, int((1215 - fin - 40) // int(CUERPO * 1.32))))
        prueba = Pieza(p.formato, fondo=(0, 0, 0, 0))
        fin_bajada = prueba.texto(bajada, MARGEN, fin + 32, ancho=ANCHO_TEXTO - 40, tam=CUERPO - 2, peso='r',
                                  color=BODY, inter=1.32, max_lineas=lineas)
        p.notas += prueba.notas
        p.cajas += prueba.cajas
        hoja = Image.new('RGBA', (ANCHO_TEXTO - 8, fin_bajada - fin - 8), WHITE)
        lz = _lienzo()
        _pegar(lz, hoja, (MARGEN - 16 + hoja.width // 2, fin + 20 + hoja.height // 2))
        poner(lz, 'nota', 'nota')
        for k, (img, x, y) in enumerate(palabras(bajada, MARGEN, fin + 32, ANCHO_TEXTO - 40, prueba.ultimo_tam, 'r',
                                                 1.32, BODY)):
            lz = _lienzo()
            lz.alpha_composite(img, (x, y))
            poner(lz, f'bajada-{k}', 'palabra-bajada')
    if sticker:
        st = sticker_personaje(sticker)
        alto = 300
        st = st.resize((round(st.width * alto / st.height), alto), Image.LANCZOS)
        st = st.rotate(6, Image.BICUBIC, expand=True)
        lz = _lienzo()
        caja_st = _pegar(lz, st, (ANCHO - MARGEN - st.width // 2, 990))
        poner(lz, 'sticker', 'sticker')
        p._anotar(caja_st, f'sticker:{sticker}')
    # El logo, como un sticker más.
    lx, ly, lado = ANCHO - MARGEN - 120, 1158, 120
    blanco = Image.new('RGBA', (lado + 20, lado + 20), (0, 0, 0, 0))
    ImageDraw.Draw(blanco).rounded_rectangle([0, 0, lado + 19, lado + 19], 14, fill=WHITE)
    logo = Pieza(p.formato, fondo=(0, 0, 0, 0))
    _pegar(logo.im, blanco, (lx + lado // 2, ly + lado // 2))
    logo.logo(x=lx, y=ly, ancho=lado)
    p.cajas += logo.cajas
    poner(logo.im, 'logo', 'logo')

    # Lo que va encima de la foto (y de un video): cintas, sello e íconos.
    lz = _lienzo()
    lz.alpha_composite(cinta(angulo=38, semilla=1), (caja[0] - 40, caja[1] - 34))
    poner(lz, 'cinta-1', 'cinta', encima=True)
    lz = _lienzo()
    lz.alpha_composite(cinta(angulo=-35, semilla=2), (caja[2] - 170, caja[1] - 40))
    poner(lz, 'cinta-2', 'cinta', encima=True)
    if chip:
        s = sello(chip.upper(), M if acento != M else B)
        sx, sy = min(caja[2] - s.width + 30, ANCHO - MARGEN - s.width), max(caja[1] + 40, 150)
        lz = _lienzo()
        lz.alpha_composite(s, (sx, sy))
        poner(lz, 'sello', 'sello', encima=True)
        p._anotar((sx, sy, sx + s.width, sy + s.height), f'chip:{chip}')
    # Íconos como stickers sobre el borde inferior derecho de la copia, un poco desordenados.
    for i, (clave, color) in enumerate(zip(iconos, colores_iconos(acento, len(iconos)))):
        st = sticker_circular(clave, color, angulo=(-9, 7, -4)[i % 3])
        ix = caja[2] - 110 - i * 150
        iy = caja[3] - 62 + (0, 14, -6)[i % 3]
        lz = _lienzo()
        _pegar(lz, st, (ix, iy))
        poner(lz, f'icono-{i}', 'icono', encima=True)
        p._anotar((ix - 64, iy - 64, ix + 64, iy + 64), f'icono:{clave}')

    # La lámina estática es la suma de las capas, en orden.
    for c in capas[1:]:
        if not c.encima:
            p.im.alpha_composite(c.img, (c.x, c.y))
    base = p.im.copy()
    encima = _lienzo()
    for c in capas:
        if c.encima:
            encima.alpha_composite(c.img, (c.x, c.y))
    p.im.alpha_composite(encima)
    p.capas = capas
    return encima, colocador(foco, ajuste), base
