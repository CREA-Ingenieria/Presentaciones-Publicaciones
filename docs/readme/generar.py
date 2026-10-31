"""Genera las imágenes y animaciones del README con el motor y las fotos de demostración.

    <PYTHON> docs/readme/generar.py [--sin-animado]

Corre los ejemplos de la skill (con --animado y --render, que necesitan Node) y arma con lo que sale
el banner, las piezas, los estilos, el flujo, los recursos, la revisión y los GIF. Sin fotos de
estudiantes: todo sale de ejemplos/fotos.
"""
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFilter

from crea_publicaciones import B, DARK, M, O, T, WHITE, Y, animar, convocatoria, mp4
from crea_publicaciones.base import BODY, ILUSTRACIONES, MARCA, MASCOTA, SOFT, font
from crea_publicaciones.marco import claves_iconos, ruta_icono, trama

AQUI = Path(__file__).resolve().parent
SKILL = AQUI.parents[1] / 'plugins' / 'publicaciones-crea' / 'skills' / 'publicaciones-crea'
EJEMPLOS = SKILL / 'ejemplos'
SALIDA = EJEMPLOS / 'salida'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
ESTILOS = ('marco', 'recortes', 'arcade')
ROTACION = (T, M, O, Y, B)


def correr(script, *args):
    r = subprocess.run([sys.executable, str(EJEMPLOS / script), *args], capture_output=True, text=True,
                       encoding='utf-8')
    if r.returncode != 0:
        raise SystemExit(f'{script} falló:\n{r.stdout}\n{r.stderr}')


def texto(d, xy, t, tam, peso='sb', color=DARK, ancla='la'):
    d.text(xy, t, font=font(tam, peso), fill=color, anchor=ancla)


def ajustar(im, alto):
    return im.resize((round(im.width * alto / im.height), alto), Image.LANCZOS)


def sombra(lienzo, im, x, y, radio=18, desvio=(10, 14), opacidad=70):
    s = Image.new('RGBA', (im.width + 80, im.height + 80), (0, 0, 0, 0))
    s.paste((30, 42, 58, opacidad), (40, 40, 40 + im.width, 40 + im.height))
    s = s.filter(ImageFilter.GaussianBlur(radio))
    lienzo.alpha_composite(s, (x - 40 + desvio[0], y - 40 + desvio[1]))
    lienzo.alpha_composite(im.convert('RGBA'), (x, y))


def anillos(d, cx, cy, radios=(150, 116, 82), colores=(T, M, Y), grosor=16):
    for r, c in zip(radios, colores):
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=c, width=grosor)


def pared(d, x0, x1, y):
    """La línea con puntos turquesa de la pared del laboratorio."""
    d.line((x0, y, x1, y), fill=DARK, width=5)
    centro = x0 + (x1 - x0) * 0.62
    for dx, r in ((0, 13), (40, 8)):
        d.ellipse((centro + dx - r, y - r, centro + dx + r, y + r), fill=T)


def circulo_icono(lienzo, clave, cx, cy, color, r=46, borde=6):
    d = ImageDraw.Draw(lienzo)
    d.ellipse((cx - r - borde, cy - r - borde, cx + r + borde, cy + r + borde), fill=WHITE)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    ic = Image.open(ruta_icono(clave, 'd' if color == Y else 'w')).convert('RGBA')
    ic = ic.resize((int(r * 1.15), int(r * 1.15)), Image.LANCZOS)
    lienzo.alpha_composite(ic, (cx - ic.width // 2, cy - ic.height // 2))


def fondo(w, h, acento=T, opacidad=0.07):
    """Blanco con la trama de doodles de la marca, de cualquier tamaño."""
    p = SimpleNamespace(w=w, h=h, im=Image.new('RGBA', (w, h), WHITE))
    trama(p, acento, opacidad=opacidad)
    return p.im


def banner():
    lienzo = fondo(1600, 640)
    d = ImageDraw.Draw(lienzo)
    anillos(d, 0, 640, radios=(130, 98, 66), colores=(T, M, Y), grosor=16)
    logo = ajustar(Image.open(MARCA / 'crea_logo.png').convert('RGBA'), 90)
    lienzo.alpha_composite(logo, (96, 64))
    texto(d, (96, 190), 'Publicaciones', 88, 'eb')
    texto(d, (96, 286), 'CREA', 88, 'eb', T)
    texto(d, (96, 412), 'Instagram del Laboratorio CREA,', 32, 'r', BODY)
    texto(d, (96, 454), 'hecho con Claude Code.', 32, 'r', BODY)
    pared(d, 200, 700, 540)
    portadas = [Image.open(SALIDA / 'estilos' / e / 'estatico' / 'carrusel-1.jpg').convert('RGBA') for e in ESTILOS]
    for i, (im, giro) in enumerate(zip(portadas, (6, 0, -6))):
        im = ajustar(im, 430).rotate(giro, expand=True, resample=Image.BICUBIC)
        sombra(lienzo, im, 760 + i * 228, 92 - (14 if giro == 0 else 0))
    d = ImageDraw.Draw(lienzo)
    d.ellipse((700, 64, 744, 108), fill=Y)
    lienzo.convert('RGB').save(AQUI / 'banner.jpg', quality=86, optimize=True)


def piezas():
    alto = 560
    items = [('Crónica', 'cronica/cronica.jpg', '4:5'), ('Carrusel', 'carrusel/carrusel-1.jpg', '4:5 · hasta 10'),
             ('Historia', 'historia/historia.jpg', '9:16'), ('Convocatoria', 'convocatoria/convocatoria.jpg', '4:5')]
    ims = [ajustar(Image.open(SALIDA / ruta).convert('RGBA'), alto) for _, ruta, _ in items]
    sep = 48
    w = sum(i.width for i in ims) + sep * (len(ims) + 1)
    lienzo = Image.new('RGBA', (w, alto + 170), WHITE)
    d = ImageDraw.Draw(lienzo)
    x = sep
    for (nombre, _, formato), im in zip(items, ims):
        sombra(lienzo, im, x, 40, radio=14, desvio=(6, 10), opacidad=50)
        texto(d, (x, alto + 70), nombre, 34, 'b')
        texto(d, (x, alto + 116), formato, 26, 'r', BODY)
        x += im.width + sep
    lienzo.convert('RGB').save(AQUI / 'piezas.jpg', quality=86, optimize=True)


def flujo():
    pasos = [('tools', 'Entorno', 'Python, motor\ny Node'), ('eye', 'Mirar', 'Fotos, videos\ny preguntas'),
             ('pencil', 'Proponer', 'Pieza y caption\nen texto'), ('cogs', 'Generar', 'build_*.py\ncon el motor'),
             ('check', 'Revisar', 'Perfil, zonas\ny avisos'), ('launch', 'Entregar', 'JPG, MP4\ny caption')]
    w, h = 1600, 520
    lienzo = fondo(w, h, opacidad=0.05)
    d = ImageDraw.Draw(lienzo)
    paso_x = (w - 200) / (len(pasos) - 1)
    y = 200
    d.line((100, y, w - 100, y), fill=DARK, width=6)
    for i, (icono, nombre, detalle) in enumerate(pasos):
        cx = int(100 + i * paso_x)
        circulo_icono(lienzo, icono, cx, y, ROTACION[i % 5], r=64, borde=10)
        d = ImageDraw.Draw(lienzo)
        d.ellipse((cx + 34, y - 92, cx + 82, y - 44), fill=DARK)
        texto(d, (cx + 58, y - 68), str(i), 28, 'b', WHITE, 'mm')
        texto(d, (cx, y + 120), nombre, 36, 'b', DARK, 'mm')
        for j, linea in enumerate(detalle.split('\n')):
            texto(d, (cx, y + 172 + j * 36), linea, 26, 'r', BODY, 'mm')
    d.rounded_rectangle((470, 30, 1130, 92), radius=31, fill=Y)
    texto(d, (800, 61), 'Nada se genera sin aprobación (paso 2)', 28, 'sb', DARK, 'mm')
    lienzo.convert('RGB').save(AQUI / 'flujo.png', optimize=True)


def iconos():
    claves = claves_iconos()
    cols, celda_w, celda_h = 12, 128, 150
    filas = -(-len(claves) // cols)
    lienzo = Image.new('RGBA', (cols * celda_w + 40, filas * celda_h + 40), WHITE)
    for i, clave in enumerate(claves):
        cx, cy = 20 + (i % cols) * celda_w + celda_w // 2, 20 + (i // cols) * celda_h + 56
        circulo_icono(lienzo, clave, cx, cy, ROTACION[i % 5], r=40, borde=0)
        texto(ImageDraw.Draw(lienzo), (cx, cy + 66), clave, 20, 'm', BODY, 'mm')
    lienzo.convert('RGB').save(AQUI / 'iconos.png', optimize=True)


def marca():
    w, h = 1600, 640
    lienzo = Image.new('RGBA', (w, h), WHITE)
    d = ImageDraw.Draw(lienzo)
    texto(d, (60, 50), 'Paleta', 34, 'b')
    colores = [('Turquesa', T, 'T'), ('Magenta', M, 'M'), ('Naranja', O, 'O'), ('Azul', B, 'B'),
               ('Amarillo', Y, 'Y'), ('Oscuro', DARK, 'DARK'), ('Gris', SOFT, 'SOFT')]
    for i, (nombre, c, clave) in enumerate(colores):
        x = 60 + i * 104
        d.rounded_rectangle((x, 110, x + 88, 198), radius=20, fill=c, outline='#D5DAE1' if c == SOFT else None)
        texto(d, (x + 44, 222), clave, 22, 'b', DARK, 'mm')
        texto(d, (x + 44, 250), c, 17, 'r', BODY, 'mm')
    texto(d, (60, 320), 'Montserrat, dentro del motor', 34, 'b')
    for i, (peso, nombre) in enumerate((('r', 'Regular'), ('sb', 'SemiBold'), ('b', 'Bold'), ('eb', 'ExtraBold'))):
        texto(d, (60, 380 + i * 58), f'{nombre}: Taller AguaLab', 38, peso)
    texto(d, (900, 50), 'Personajes', 34, 'b')
    x = 900
    for ruta in (MASCOTA / 'seneca_saludo.png', MASCOTA / 'seneca_baile.png', ILUSTRACIONES / 'creabot.png'):
        im = ajustar(Image.open(ruta).convert('RGBA'), 300)
        lienzo.alpha_composite(im, (x, 130))
        x += im.width + 40
    texto(d, (900, 470), 'Séneca (saluda, guiña y baila) y CREABOT', 26, 'r', BODY)
    logo = ajustar(Image.open(MARCA / 'crea_logo.png').convert('RGBA'), 90)
    lienzo.alpha_composite(logo, (900, 520))
    lienzo.convert('RGB').save(AQUI / 'marca.png', optimize=True)


def revision():
    perfil = Image.open(SALIDA / 'carrusel' / 'revision' / 'carrusel-1-perfil.jpg').convert('RGBA')
    zonas = Image.open(SALIDA / 'historia' / 'revision' / 'historia-zonas.jpg').convert('RGBA')
    lamina = Image.open(SALIDA / 'carrusel' / 'carrusel-1.jpg').convert('RGBA')
    alto = 520
    ims = [ajustar(lamina, alto), ajustar(perfil, ajustar(perfil, alto).height * 360 // alto), ajustar(zonas, alto)]
    ims[1] = perfil.resize((360, 360))
    etiquetas = ['La lámina (4:5)', 'Cómo queda en el perfil', 'Lo que tapa Instagram']
    w = sum(i.width for i in ims) + 60 * 4
    lienzo = Image.new('RGBA', (w, alto + 140), WHITE)
    d = ImageDraw.Draw(lienzo)
    x = 60
    for im, et in zip(ims, etiquetas):
        sombra(lienzo, im, x, 30 + (alto - im.height) // 2, radio=12, desvio=(5, 8), opacidad=45)
        texto(d, (x, alto + 76), et, 28, 'sb')
        x += im.width + 60
    lienzo.convert('RGB').save(AQUI / 'revision.jpg', quality=86, optimize=True)


def gif(origen, destino, ancho, fps=15, colores=128):
    filtro = (f'fps={fps},scale={ancho}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors={colores}'
              f':stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle')
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-i', str(origen), '-vf', filtro, str(destino)], check=True)


def bucles():
    """Las cuatro animaciones en bucle del motor, una al lado de la otra."""
    from crea_publicaciones.animacion import leer_video
    base = dict(contacto='crea.uniandes.edu.co', mascota=False)
    burbujas = animar(convocatoria('Laboratorio de agua', ['Muestras reales', 'Filtros'], acento=T, nombre='b',
                                   **base), 'burbujas', caja=(560, 160, 1020, 760))
    torre = animar(convocatoria('Prueba y error', ['Cargas', 'Equilibrio'], acento=M, nombre='t', **base), 'torre',
                   x=800, y_base=760)
    videos = [mp4(burbujas.cuadros, SALIDA / 'bucle-burbujas.mp4', 30), mp4(torre.cuadros, SALIDA / 'bucle-torre.mp4', 30),
              SALIDA / 'carrusel' / 'carrusel-2.mp4', SALIDA / 'historia' / 'historia.mp4']
    pistas = [[ajustar(c, 420) for c in leer_video(v)] for v in videos]
    n = max(len(p) for p in pistas)
    w = sum(p[0].width for p in pistas) + 24 * 5
    cuadros = []
    for i in range(n):
        lienzo = Image.new('RGB', (w, 468), WHITE)
        x = 24
        for p in pistas:
            lienzo.paste(p[i % len(p)], (x, 24))
            x += p[0].width + 24
        cuadros.append(lienzo)
    gif(mp4(cuadros, SALIDA / 'bucles.mp4', 30), AQUI / 'bucles.gif', 900, fps=12)


def animados():
    for estilo in ESTILOS:
        gif(SALIDA / 'estilos' / estilo / 'animado' / 'carrusel-1.mp4', AQUI / f'animado-{estilo}.gif', 340)
    gif(SALIDA / 'reel' / 'reel.mp4', AQUI / 'reel.gif', 270, fps=12)


if __name__ == '__main__':
    animado = '--sin-animado' not in sys.argv
    for script in ('build_cronica.py', 'build_historia.py', 'build_carrusel.py', 'build_convocatoria.py'):
        correr(script)
    correr('build_estilos.py', *(['--animado'] if animado else []))
    if animado:
        correr('build_reel.py', '--render')
    banner()
    piezas()
    flujo()
    iconos()
    marca()
    revision()
    bucles()
    if animado:
        animados()
    for f in sorted(AQUI.glob('*.*')):
        if f.suffix != '.py':
            print(f'{f.name}: {f.stat().st_size // 1024} KB')
