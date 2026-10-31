"""Las mascotas de CREA en más poses: CREABOT redibujado en vector y variantes de Séneca.

CREABOT es geométrico, así que se redibuja por partes (pies, piernas, cuerpo, cabeza, ojos) con las
medidas y colores del dibujo original (`ilustraciones/creabot.png`) y cada pose mueve esas partes:
salta, camina, mira, piensa, celebra, y su pecho puede ser una pantalla. Sin brazos, como el original.

Séneca es una ilustración a mano: no se redibuja en otras posturas (eso es trabajo de ilustración).
Sus variantes salen de los dibujos originales: espejo, busto para asomarse, cabeza en círculo y el buzo
en el color del taller.
"""
import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from .base import MASCOTA, WHITE, B, ErrorCREA, M, O, T, Y, font
from .marco import ruta_icono

# Medidas del dibujo original (265 × 346 px). Todo se dibuja en esas unidades, escalado.
TINTA = '#11142E'
NARANJA_ALTO, NARANJA, NARANJA_BAJO = (255, 160, 40), (251, 140, 8), (226, 78, 4)
BISEL = (255, 241, 222)
IRIS, IRIS_BORDE = (248, 251, 252), (205, 225, 252)
CABEZA = (26, 10, 243, 127)
CUERPO = (13, 126, 253, 232)
CADERA = (41, 222, 226, 246)
PIERNAS = ((41, 238, 85, 300), (180, 238, 226, 300))
PIES = ((23, 296, 107, 335), (160, 296, 244, 335))
OJOS = ((89, 66), (179, 66))
R_OJO, R_IRIS, R_PUPILA = 39, 30, 18
PERNOS_CABEZA = ((47, 36), (222, 36), (47, 101), (222, 101))
PERNOS_CUERPO = ((36, 152), (231, 152), (36, 206), (231, 206))
LIENZO = (420, 470)          # margen para saltos, giros y globos
ORIGEN = (78, 92)            # dónde cae la esquina (0, 0) del dibujo original en el lienzo

POSES_CREABOT = ('frente', 'feliz', 'guino', 'mira-izquierda', 'mira-derecha', 'sorpresa', 'pensando', 'salta',
                 'camina', 'celebra', 'pantalla', 'cargando', 'corazones', 'dormido')


def _gradiente(w, h, arriba, abajo):
    g = Image.new('RGB', (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        g.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(arriba, abajo)))
    return g.resize((w, h))


class _Lapiz:
    """Dibuja en unidades del dibujo original sobre una capa escalada."""

    def __init__(self, esc):
        self.esc = esc
        self.im = Image.new('RGBA', (round(LIENZO[0] * esc), round(LIENZO[1] * esc)), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def p(self, x, y):
        return ((x + ORIGEN[0]) * self.esc, (y + ORIGEN[1]) * self.esc)

    def caja(self, c):
        return (*self.p(c[0], c[1]), *self.p(c[2], c[3]))

    def bloque(self, c, radio, borde=8, arriba=NARANJA_ALTO, abajo=NARANJA_BAJO, bisel=True):
        """Una caja de CREABOT: contorno oscuro, relleno naranja en degradado y el bisel claro arriba a la izquierda."""
        x0, y0, x1, y1 = self.caja(c)
        e = self.esc
        self.d.rounded_rectangle((x0, y0, x1, y1), radius=radio * e, fill=TINTA)
        ix0, iy0, ix1, iy1 = x0 + borde * e, y0 + borde * e, x1 - borde * e, y1 - borde * e
        mascara = Image.new('L', self.im.size, 0)
        ImageDraw.Draw(mascara).rounded_rectangle((ix0, iy0, ix1, iy1), radius=(radio - borde / 2) * e, fill=255)
        grad = _gradiente(round(ix1 - ix0) + 1, round(iy1 - iy0) + 1, arriba, abajo)
        capa = Image.new('RGBA', self.im.size, (0, 0, 0, 0))
        capa.paste(grad, (round(ix0), round(iy0)))
        self.im.paste(capa, (0, 0), ImageChops.multiply(mascara, capa.getchannel('A')))
        if bisel:
            b = 6 * e
            self.d.rounded_rectangle((ix0, iy0, ix1 - 14 * e, iy0 + b), radius=b / 2, fill=BISEL)
            self.d.rounded_rectangle((ix0, iy0, ix0 + b, iy1 - 14 * e), radius=b / 2, fill=BISEL)

    def circulo(self, cx, cy, r, fill=None, outline=None, width=0):
        x, y = self.p(cx, cy)
        r *= self.esc
        self.d.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=outline, width=round(width * self.esc))

    def linea(self, puntos, ancho, color=TINTA, curva=True):
        pts = [self.p(x, y) for x, y in puntos]
        self.d.line(pts, fill=color, width=round(ancho * self.esc), joint='curve' if curva else None)
        for x, y in (pts[0], pts[-1]):
            r = ancho * self.esc / 2
            self.d.ellipse((x - r, y - r, x + r, y + r), fill=color)

    def arco(self, cx, cy, r, inicio, fin, ancho, color=TINTA):
        pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
               for a in range(inicio, fin + 1, 4)]
        self.linea(pts, ancho, color)


def _ojo(l, cx, cy, tipo, mira=(0, 0)):
    l.circulo(cx, cy, R_OJO, fill=TINTA)
    if tipo in ('feliz', 'cerrado', 'guino'):
        l.circulo(cx, cy, R_OJO - 9, fill=NARANJA)
        if tipo == 'feliz':
            l.arco(cx, cy + 10, 17, 200, 340, 9)
        else:
            l.arco(cx, cy - 4, 17, 20, 160, 9)
        return
    if tipo == 'corazon':
        l.circulo(cx, cy, R_OJO - 9, fill=IRIS)
        x, y = l.p(cx, cy + 2)
        r = 9 * l.esc
        l.d.ellipse((x - 2 * r, y - 1.6 * r, x, y + 0.4 * r), fill=M)
        l.d.ellipse((x, y - 1.6 * r, x + 2 * r, y + 0.4 * r), fill=M)
        l.d.polygon(((x - 1.95 * r, y - 0.35 * r), (x + 1.95 * r, y - 0.35 * r), (x, y + 2 * r)), fill=M)
        return
    l.circulo(cx, cy, R_OJO - 9, fill=IRIS_BORDE)
    l.circulo(cx, cy, R_IRIS - 3, fill=IRIS)
    r = R_PUPILA * (0.62 if tipo == 'sorpresa' else 1)
    px, py = cx + mira[0] * 10, cy + mira[1] * 10
    l.circulo(px, py, r, fill=TINTA)
    l.circulo(px - r * 0.38, py - r * 0.38, r * 0.3, fill=WHITE)


def _cabeza(l, ojos=('normal', 'normal'), mira=(0, 0)):
    l.bloque(CABEZA, 16)
    for x, y in PERNOS_CABEZA:
        l.circulo(x, y, 4.5, fill=TINTA)
    for (cx, cy), tipo in zip(OJOS, ojos):
        _ojo(l, cx, cy, tipo, mira)


def _pantalla(l, contenido, esc):
    """El pecho como pantalla: caja oscura con un ícono, un texto corto o una barra de carga."""
    x0, y0, x1, y1 = 46, 148, 220, 210
    l.d.rounded_rectangle(l.caja((x0, y0, x1, y1)), radius=10 * esc, fill=TINTA)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if contenido == 'carga':
        l.d.rounded_rectangle(l.caja((x0 + 16, cy - 9, x1 - 16, cy + 9)), radius=9 * esc, outline=T,
                              width=round(3 * esc))
        l.d.rounded_rectangle(l.caja((x0 + 21, cy - 4, x0 + 21 + (x1 - x0 - 42) * 0.62, cy + 4)), radius=4 * esc,
                              fill=Y)
    elif contenido.startswith('icono:'):
        ic = Image.open(ruta_icono(contenido.split(':', 1)[1], 'w')).convert('RGBA')
        lado = round(46 * esc)
        ic = ic.resize((lado, lado), Image.LANCZOS)
        amarillo = Image.new('RGBA', ic.size, Y)
        amarillo.putalpha(ic.getchannel('A'))
        x, y = l.p(cx, cy)
        l.im.alpha_composite(amarillo, (round(x - lado / 2), round(y - lado / 2)))
    else:
        f = font(round(30 * esc), 'eb')
        x, y = l.p(cx, cy)
        l.d.text((x, y), contenido, font=f, fill=Y, anchor='mm')


def _cuerpo(l, pantalla=None):
    l.d.rounded_rectangle(l.caja(CADERA), radius=8 * l.esc, fill=TINTA)
    l.bloque(CUERPO, 18)
    for x, y in PERNOS_CUERPO:
        l.circulo(x, y, 4.5, fill=TINTA)
    if pantalla:
        _pantalla(l, pantalla, l.esc)


def _pierna(l, i, dx=0, dy=0, alto=0):
    """Una pierna con su pie. `alto` acorta la pierna (sube el pie) para el salto."""
    x0, y0, x1, y1 = PIERNAS[i]
    l.d.rectangle(l.caja((x0 + dx, y0, x1 + dx, y1 - alto + dy)), fill=TINTA)
    fx0, fy0, fx1, fy1 = PIES[i]
    l.d.rounded_rectangle(l.caja((fx0 + dx, fy0 - alto + dy, fx1 + dx, fy1 - alto + dy)), radius=10 * l.esc,
                          fill=TINTA)


def _girar(capa, grados, pivote, esc):
    if not grados:
        return capa
    cx, cy = ((pivote[0] + ORIGEN[0]) * esc, (pivote[1] + ORIGEN[1]) * esc)
    return capa.rotate(grados, resample=Image.BICUBIC, center=(cx, cy))


def _mover(capa, dx, dy, esc):
    if not dx and not dy:
        return capa
    salida = Image.new('RGBA', capa.size, (0, 0, 0, 0))
    salida.alpha_composite(capa, (round(dx * esc), round(dy * esc)))
    return salida


def _borde_blanco(im, grosor):
    """El borde de sticker blanco del dibujo original, alrededor de toda la silueta."""
    # Se engrosa la silueta a un cuarto del tamaño (mucho más rápido) y se vuelve a escalar.
    peq = im.getchannel('A').resize((im.width // 4, im.height // 4), Image.BILINEAR)
    r = max(1, grosor // 4)
    alfa = peq.filter(ImageFilter.GaussianBlur(r * 0.75)).point(lambda v: 255 if v > 6 else 0)
    alfa = alfa.resize(im.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(1.5))
    fondo = Image.new('RGBA', im.size, (255, 255, 255, 0))
    fondo.putalpha(alfa)
    fondo.alpha_composite(im)
    return fondo


def _extras(l, pose, rng):
    e = l.esc
    if pose == 'pensando':
        l.circulo(258, -38, 30, fill=WHITE, outline=TINTA, width=6)
        l.circulo(236, 2, 9, fill=WHITE, outline=TINTA, width=5)
        l.circulo(225, 20, 5, fill=WHITE, outline=TINTA, width=4)
        x, y = l.p(258, -38)
        l.d.text((x, y), '?', font=font(round(40 * e), 'eb'), fill=M, anchor='mm')
    elif pose == 'sorpresa':
        for i, (dx, ang) in enumerate(((-30, -18), (0, 0), (30, 18))):
            x, y = 134 + dx * 2.2, -30
            fin = (x + math.sin(math.radians(ang)) * 26, y - math.cos(math.radians(ang)) * 26)
            l.linea([(x, y), fin], 8, O)
    elif pose == 'dormido':
        for i, (dx, dy, t) in enumerate(((225, -10, 26), (255, -40, 34), (290, -78, 42))):
            x, y = l.p(dx, dy)
            l.d.text((x, y), 'z', font=font(round(t * e), 'eb'), fill=B, anchor='mm')
    elif pose in ('salta', 'celebra'):
        l.d.ellipse(l.caja((40, 368, 228, 384)), fill=(17, 20, 46, 60))
        for x in (70, 134, 198):
            l.linea([(x, 326), (x, 350)], 6, (17, 20, 46, 140))
    elif pose == 'camina':
        for y, largo in ((150, 46), (182, 62), (214, 40)):
            l.linea([(-58, y), (-58 + largo, y)], 7, (17, 20, 46, 150))
    if pose == 'celebra':
        colores = (T, M, O, Y, B)
        for i in range(26):
            x, y = rng.uniform(-60, 330), rng.uniform(-80, 120)
            if 10 < x < 260 and y > 0:
                continue
            c = colores[i % 5]
            if i % 2:
                l.circulo(x, y, rng.uniform(5, 8), fill=c)
            else:
                w, ang = rng.uniform(8, 13), rng.uniform(0, 180)
                pts = [(x + math.cos(math.radians(ang + k * 90)) * w * (1 if k % 2 == 0 else 0.45),
                        y + math.sin(math.radians(ang + k * 90)) * w * (1 if k % 2 == 0 else 0.45)) for k in range(4)]
                l.d.polygon([l.p(px, py) for px, py in pts], fill=c)


def creabot(pose='frente', alto=600, pantalla=None):
    """CREABOT en una pose, como imagen RGBA recortada con su borde blanco de sticker.

    `pantalla` convierte el pecho en pantalla: 'icono:<clave>' (un ícono de la lista), un texto corto
    ('¡Hola!', '</>') o 'carga'. Las poses 'pantalla' y 'cargando' la traen puesta.
    """
    if pose not in POSES_CREABOT:
        raise ErrorCREA(f'CREABOT no tiene la pose "{pose}". Usa una de: {", ".join(POSES_CREABOT)}')
    esc = 4
    rng = random.Random(7)
    ojos, mira = ('normal', 'normal'), (0, 0)
    cabeza_giro = cuerpo_giro = 0
    cabeza_dy = salto = 0
    piernas = [dict(), dict()]
    if pose == 'feliz':
        ojos, cabeza_giro = ('feliz', 'feliz'), 5
    elif pose == 'guino':
        ojos, cabeza_giro = ('normal', 'guino'), -4
    elif pose == 'mira-izquierda':
        mira, cabeza_giro, cuerpo_giro = (-1, 0), 5, 2
    elif pose == 'mira-derecha':
        mira, cabeza_giro, cuerpo_giro = (1, 0), -5, -2
    elif pose == 'sorpresa':
        ojos, cabeza_dy = ('sorpresa', 'sorpresa'), -12
    elif pose == 'pensando':
        mira, cabeza_giro = (0.7, -0.7), -7
    elif pose in ('salta', 'celebra'):
        ojos, salto = ('feliz', 'feliz'), -40
        piernas = [dict(alto=26, dx=6), dict(alto=26, dx=-6)]
        cabeza_giro = 4 if pose == 'salta' else -4
    elif pose == 'camina':
        cuerpo_giro, cabeza_giro, mira = -4, -2, (1, 0)
        piernas = [dict(alto=14, dx=-10), dict(dx=8)]
    elif pose == 'pantalla':
        pantalla = pantalla or 'icono:bulb'
        mira = (0, 0.8)
    elif pose == 'cargando':
        pantalla, ojos = 'carga', ('cerrado', 'cerrado')
    elif pose == 'corazones':
        ojos, cabeza_giro = ('corazon', 'corazon'), 4
    elif pose == 'dormido':
        ojos, cabeza_giro, cabeza_dy = ('cerrado', 'cerrado'), 6, 4

    lp = _Lapiz(esc)
    for i in (0, 1):
        _pierna(lp, i, **piernas[i])
    lc = _Lapiz(esc)
    _cuerpo(lc, pantalla)
    lh = _Lapiz(esc)
    _cabeza(lh, ojos, mira)
    cuerpo = _girar(lc.im, cuerpo_giro, (134, 236), esc)
    cabeza = _girar(lh.im, cabeza_giro + cuerpo_giro, (134, 127), esc)
    if cuerpo_giro:
        # La cabeza sigue al cuerpo: su base se corre con el giro del torso.
        cabeza = _mover(cabeza, -math.sin(math.radians(cuerpo_giro)) * 110, 0, esc)
    cabeza = _mover(cabeza, 0, cabeza_dy, esc)
    figura = Image.new('RGBA', lp.im.size, (0, 0, 0, 0))
    for capa in (lp.im, cuerpo, cabeza):
        figura.alpha_composite(capa)
    figura = _mover(figura, 0, salto, esc)
    figura = _borde_blanco(figura, round(7 * esc))
    le = _Lapiz(esc)
    _extras(le, pose, rng)
    le.im.alpha_composite(figura)
    salida = le.im
    salida = salida.crop(salida.getchannel('A').getbbox())
    return salida.resize((round(salida.width * alto / salida.height), alto), Image.LANCZOS)


# --- Séneca ---------------------------------------------------------------------------------------

POSES_SENECA = ('saludo', 'guino', 'baile', 'saludo-espejo', 'guino-espejo', 'baile-espejo', 'asoma', 'asoma-espejo',
                'cabeza')
BUZO = {'T': None, 'M': M, 'O': O, 'B': B}
# Dónde está el parche CREA en cada dibujo, en fracciones del ancho y el alto: se vuelve a voltear en el
# espejo para que el logo no quede al revés.
PARCHE = {'saludo': (425 / 1252, 1528 / 2473, 678 / 1252, 1784 / 2473),
          'guino': (425 / 1252, 1528 / 2473, 678 / 1252, 1784 / 2473),
          'baile': (234 / 363, 254 / 497, 266 / 363, 284 / 497)}


def _caja_parche(base, w, h):
    x0, y0, x1, y1 = PARCHE['saludo' if base in ('asoma', 'cabeza') else base]
    return round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)


def _recolorear_buzo(im, color):
    """Pasa el buzo turquesa al color del taller sin tocar el resto (ojos, logo, cuerpo)."""
    hsv = im.convert('RGB').convert('HSV')
    h, s, v = hsv.split()
    destino = Image.new('RGB', (1, 1), color).convert('HSV').getpixel((0, 0))
    # El turquesa del buzo está entre los tonos ~120 y ~145 (de 255), con saturación media o alta.
    hd, sd, vd = h.load(), s.load(), v.load()
    m = Image.new('L', im.size, 0)
    md = m.load()
    nh, ns, nv = h.copy(), s.copy(), v.copy()
    nhd, nsd, nvd = nh.load(), ns.load(), nv.load()
    vt = 205       # brillo de referencia del turquesa del buzo
    for y in range(im.height):
        for x in range(im.width):
            if 118 <= hd[x, y] <= 150 and sd[x, y] > 90 and vd[x, y] > 60:
                md[x, y] = 255
                nhd[x, y] = destino[0]
                nsd[x, y] = min(255, round(sd[x, y] * destino[1] / 230))
                nvd[x, y] = max(0, min(255, round(vd[x, y] * destino[2] / vt)))
    nuevo = Image.merge('HSV', (nh, ns, nv)).convert('RGB').convert('RGBA')
    nuevo.putalpha(im.getchannel('A'))
    salida = im.copy()
    salida.paste(nuevo, (0, 0), m.filter(ImageFilter.GaussianBlur(0.6)))
    return salida


def seneca(pose='saludo', alto=600, buzo='T'):
    """Séneca en una pose o variante, como imagen RGBA. `buzo` ('T', 'M', 'O', 'B') pinta el buzo del
    color del taller (las poses de saludo, guiño y asoma; el baile lleva chaqueta y se deja turquesa)."""
    if pose not in POSES_SENECA:
        raise ErrorCREA(f'Séneca no tiene la pose "{pose}". Usa una de: {", ".join(POSES_SENECA)}')
    if buzo not in BUZO:
        raise ErrorCREA('El buzo de Séneca va en T, M, O o B (el amarillo no es acento)')
    base = pose.split('-')[0]
    archivo = {'saludo': 'seneca_saludo.png', 'guino': 'seneca_guino.png', 'baile': 'seneca_baile.png',
               'asoma': 'seneca_saludo.png', 'cabeza': 'seneca_saludo.png'}[base]
    im = Image.open(MASCOTA / archivo).convert('RGBA')
    escala = alto * (1.0 if base not in ('asoma', 'cabeza') else 2.1) / im.height
    trabajo = im.resize((round(im.width * min(1, escala * 1.4)), round(im.height * min(1, escala * 1.4))),
                        Image.LANCZOS)
    w, h = trabajo.size
    if BUZO[buzo] and base != 'baile':
        trabajo = _recolorear_buzo(trabajo, BUZO[buzo])
        if buzo == 'M':
            # El parche CREA también es magenta: un borde blanco lo separa del buzo.
            x0, y0, x1, y1 = _caja_parche(base, w, h)
            ImageDraw.Draw(trabajo).rectangle((x0, y0, x1, y1), outline=WHITE, width=max(2, round(w * 0.012)))
    if pose.endswith('-espejo'):
        x0, y0, x1, y1 = _caja_parche(base, w, h)
        trabajo = trabajo.transpose(Image.FLIP_LEFT_RIGHT)
        caja = (w - x1, y0, w - x0, y1)
        trabajo.paste(trabajo.crop(caja).transpose(Image.FLIP_LEFT_RIGHT), caja)
    if base == 'asoma':
        trabajo = trabajo.crop((0, 0, w, round(h * 0.6)))
    elif base == 'cabeza':
        lado = round(w * 0.98)
        cx, cy = round(w * 0.43), round(h * 0.255)
        cara = trabajo.crop((cx - lado // 2, cy - lado // 2, cx + lado // 2, cy + lado // 2))
        circulo = Image.new('RGBA', cara.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(circulo)
        d.ellipse((0, 0, lado - 1, lado - 1), fill={'T': T, 'M': M, 'O': O, 'B': B}[buzo])
        mascara = Image.new('L', cara.size, 0)
        ImageDraw.Draw(mascara).ellipse((0, 0, lado - 1, lado - 1), fill=255)
        circulo.alpha_composite(cara)
        circulo.putalpha(ImageChops.multiply(circulo.getchannel('A'), mascara))
        borde = Image.new('RGBA', (lado + 24, lado + 24), (0, 0, 0, 0))
        ImageDraw.Draw(borde).ellipse((0, 0, lado + 23, lado + 23), fill=WHITE)
        borde.alpha_composite(circulo, (12, 12))
        trabajo = borde
    trabajo = trabajo.crop(trabajo.getchannel('A').getbbox())
    return trabajo.resize((round(trabajo.width * alto / trabajo.height), alto), Image.LANCZOS)

