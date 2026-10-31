"""El marco CREA de las piezas 4:5 con foto (crónica y lámina de carrusel).

Toma sus formas de la marca y no las inventa: el bloque de color corrido con el punto amarillo
y la línea en L salen del logo; los anillos concéntricos, del cuadro magenta del logo; la línea
con puntos turquesa, de la pared del laboratorio. Los íconos en círculos de color dicen de qué
se trató la actividad.

Lo decorativo vive fuera de las zonas de texto. Solo se anotan para la revisión los íconos,
que sí pueden chocar con el texto si alguien mueve la retícula.
"""
import difflib

from PIL import Image

from .base import DARK, MARGEN, MARCA, RECURSOS, WHITE, B, ErrorCREA, M, O, Pieza, T, Y

ICONOS_PNG = RECURSOS / 'iconos' / 'png'
ANCHO, ALTO = 1080, 1350
RADIO = 64
FOTO = (MARGEN, 96, ANCHO - MARGEN - 24, 744)     # la foto, un poco corrida para que asome el bloque
BLOQUE = (MARGEN + 24, MARGEN, ANCHO - MARGEN, 720)
DIAMETRO_ICONO = 120
MAX_ICONOS = 3
ROTACION = (M, O, Y, T, B)


def claves_iconos():
    return sorted({p.stem.rsplit('_', 1)[0] for p in ICONOS_PNG.glob('*.png')})


def ruta_icono(clave, color='w'):
    ruta = ICONOS_PNG / f'{clave}_{color}.png'
    if not ruta.is_file():
        parecidos = difflib.get_close_matches(clave, claves_iconos(), n=3)
        pista = f' ¿Quisiste decir {", ".join(parecidos)}?' if parecidos else ''
        raise ErrorCREA(f'No existe el ícono "{clave}".{pista} La lista está en referencia/piezas.md')
    return ruta


def colores_iconos(acento, n):
    """Colores de los círculos: los de la marca que no son el acento, para que la pieza tenga ritmo."""
    otros = [c for c in ROTACION if c != acento]
    return [otros[i % len(otros)] for i in range(n)]


def zona_iconos(n):
    """(x izquierda, y inferior) de lo que ocupan n íconos, con su borde blanco."""
    if not n:
        return (ANCHO, 0)
    radio = DIAMETRO_ICONO // 2
    x_ultimo = FOTO[2] - 40 - radio - (n - 1) * (DIAMETRO_ICONO + 16)
    return (x_ultimo - radio - 7, FOTO[3] + radio + 7)


def trama(p, color, opacidad=0.08):
    """Los doodles de la plantilla, en el color de acento y muy suaves, sobre el fondo blanco."""
    patron = Image.open(MARCA / 'patron_doodles.png').convert('RGBA')
    esc = p.w / patron.width
    patron = patron.resize((p.w, int(patron.height * esc)), Image.LANCZOS)
    alfa = Image.new('L', p.im.size, 0)
    for y in range(0, p.h, patron.height):
        alfa.paste(patron.getchannel('A'), (0, y))
    pico = alfa.getextrema()[1] or 255
    capa = Image.new('RGBA', p.im.size, color)
    capa.putalpha(alfa.point(lambda v: int(v * 255 / pico * opacidad)))
    p.im.alpha_composite(capa)


def debajo(p, acento):
    """Lo que va detrás de la foto: trama, anillos, bloque corrido, línea en L y línea de circuito."""
    trama(p, acento)
    d = p.d
    # Anillos del logo, saliendo de la esquina inferior izquierda (fuera del cuadrado del perfil).
    segundo = M if acento != M else T
    for r, color in ((150, acento), (112, segundo), (74, Y)):
        d.ellipse([-r, ALTO - r, r, ALTO + r], outline=color, width=16)
    # El bloque de color corrido arriba a la derecha, como el marco turquesa del logo.
    d.rounded_rectangle(BLOQUE, RADIO, fill=acento)
    # La línea en L del logo, abajo a la izquierda de la foto.
    d.line([(MARGEN - 20, 430), (MARGEN - 20, FOTO[3] + 20), (MARGEN + 340, FOTO[3] + 20)], fill=DARK, width=5,
           joint='curve')
    # La línea de la pared del laboratorio: trazo oscuro con dos puntos turquesa.
    y = ALTO - 44
    d.line([(236, y), (ANCHO, y)], fill=DARK, width=5)
    for x, r in ((560, 13), (604, 8)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=T)


def encima(p, acento, chip=None, iconos=()):
    """Lo que va sobre la foto: punto amarillo, chip e íconos. Devuelve la capa (para los videos)."""
    if len(iconos) > MAX_ICONOS:
        raise ErrorCREA(f'Van hasta {MAX_ICONOS} íconos: más se vuelve ruido')
    capa = Pieza(p.formato, fondo=(0, 0, 0, 0))
    d = capa.d
    # El punto amarillo en la esquina del bloque, como en el logo.
    cx, cy, r = BLOQUE[2] - 34, BLOQUE[1] + 34, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=Y)
    if chip:
        capa.chip(chip, FOTO[0] + 40, 148, bg=acento, fg=WHITE, mayus=True)
    # Íconos en círculos de color montados sobre el borde inferior de la foto, de derecha a izquierda.
    radio = DIAMETRO_ICONO // 2
    for i, (clave, color) in enumerate(zip(iconos, colores_iconos(acento, len(iconos)))):
        x = FOTO[2] - 40 - radio - i * (DIAMETRO_ICONO + 16)
        y = FOTO[3]
        caja = (x - radio, y - radio, x + radio, y + radio)
        d.ellipse([caja[0] - 7, caja[1] - 7, caja[2] + 7, caja[3] + 7], fill=WHITE)
        d.ellipse(caja, fill=color)
        glifo = Image.open(ruta_icono(clave, 'd' if color == Y else 'w')).convert('RGBA')
        lado = int(DIAMETRO_ICONO * 0.58)
        glifo = glifo.resize((lado, lado), Image.LANCZOS)
        capa.im.alpha_composite(glifo, (x - lado // 2, y - lado // 2))
        capa._anotar(caja, f'icono:{clave}')
    p.im.alpha_composite(capa.im)
    p.cajas += capa.cajas
    p.notas += capa.notas
    return capa.im
