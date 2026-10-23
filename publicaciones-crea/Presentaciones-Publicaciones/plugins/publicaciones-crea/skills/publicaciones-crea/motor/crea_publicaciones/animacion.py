"""Animaciones sutiles en bucle y su exportación a MP4 (Instagram no acepta GIF).

Cada animación devuelve una lista de cuadros cuyo último empalma con el primero.
Los scripts no las llaman directo: usan `animar(pieza, tipo, ...)` al final de la pieza.
"""
import math
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from .base import ETIQ, MASCOTA, O, T, WHITE, Y, B, M, ErrorCREA, dibujar_codigo

TIPOS = ('burbujas', 'torre', 'codigo', 'parpadeo')


def burbujas(base, caja=None, n=16, colores=(WHITE, T, Y), dur=5.0, fps=30, semilla=7):
    # Cada burbuja recorre la caja completa una vez por ciclo, así el último cuadro
    # empalma con el primero. Radios gruesos a propósito: la compresión de
    # Instagram se come los detalles finos.
    rnd = random.Random(semilla)
    caja = caja or (0, 0, base.width, base.height)
    x0, y0, x1, y1 = caja
    alto = y1 - y0
    bb = [{'x': rnd.randint(x0 + 20, x1 - 20), 'r': rnd.randint(8, 22),
           'fase': rnd.random(), 'col': rnd.choice(colores),
           'a': rnd.randint(70, 150), 'vaiven': rnd.uniform(10, 30)} for _ in range(n)]
    total = int(dur * fps)
    cuadros = []
    for i in range(total):
        t = i / total
        capa = Image.new('RGBA', base.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(capa)
        for b in bb:
            p = (b['fase'] + t) % 1.0
            y = y1 - p * alto
            x = b['x'] + b['vaiven'] * math.sin(p * 2 * math.pi + b['fase'] * 6)
            # Se desvanece al nacer y al morir para que el ciclo no dé un salto.
            a = int(b['a'] * min(1.0, p / 0.15, (1 - p) / 0.15))
            if a <= 0:
                continue
            r = b['r']
            d.ellipse([x - r, y - r, x + r, y + r], fill=b['col'] + f'{a:02x}')
            d.ellipse([x - r, y - r, x + r, y + r], outline=WHITE + f'{min(255, a + 60):02x}', width=3)
        f = base.copy()
        f.alpha_composite(capa)
        cuadros.append(f)
    return cuadros


def _bloque(ancho, alto, color, alpha):
    pad = 10
    im = Image.new('RGBA', (ancho + 2 * pad, alto + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([pad, pad, pad + ancho, pad + alto], 12,
                        fill=color + f'{alpha:02x}', outline=WHITE + f'{alpha:02x}', width=3)
    return im


def torre_bloques(base, x, y_base, n=5, ancho=130, alto=62, colores=None,
                  evitar=None, dur=6.0, fps=30, semilla=3):
    # Una torre que se balancea cada vez más, se cae y vuelve a estar en pie. El
    # ciclo cierra porque el último tramo desvanece los bloques caídos mientras
    # reaparece la torre en reposo: el cuadro final es el inicial.
    rnd = random.Random(semilla)
    colores = colores or (Y, O, T, M, B)
    # Un bloque del color del fondo sería invisible.
    colores = [c for c in colores if c.lower() != (evitar or '').lower()] or list(colores)
    cols = [colores[i % len(colores)] for i in range(n)]
    total = int(dur * fps)
    t_caida, t_reposo = 0.55, 0.80      # fracciones del ciclo
    g, lado = 900.0, rnd.choice((-1, 1))
    cuadros = []
    for k in range(total):
        t = k / total
        capa = Image.new('RGBA', base.size, (0, 0, 0, 0))
        for i in range(n):
            cx, cy = float(x), float(y_base - (i + 0.5) * alto)
            ang, alpha = 0.0, 255
            if t < t_caida:                       # balanceo que crece
                p = t / t_caida
                lean = (p ** 1.8) * math.sin(2 * math.pi * 1.9 * p) * lado
                cx += lean * ((i + 1) / n) ** 1.6 * 52
                ang = -lean * (i + 1) / n * 11
            else:
                # Congela la inclinación del momento del derrumbe y cae.
                dt = (t - t_caida) * dur
                lean = math.sin(2 * math.pi * 1.9) * lado or lado
                cx += lean * ((i + 1) / n) ** 1.6 * 52
                cx += lado * (0.5 + 0.5 * i) * 170 * dt
                cy += (-110 + 35 * i) * dt + 0.5 * g * dt * dt
                ang = -lean * (i + 1) / n * 11 + lado * (70 + 35 * i) * dt
                # Se desvanecen justo antes de que reaparezca la torre.
                desv = t_reposo - 0.12
                alpha = 0 if t > t_reposo else (
                    255 if t < desv else int(255 * (1 - (t - desv) / 0.12)))
            if alpha:
                b = _bloque(ancho, alto, cols[i], alpha).rotate(ang, Image.BICUBIC, expand=True)
                capa.alpha_composite(b, (int(cx - b.width / 2), int(cy - b.height / 2)))
        if t > t_reposo:                          # la torre vuelve a aparecer
            f = (t - t_reposo) / (1 - t_reposo)
            a = int(255 * min(1.0, f * 1.25))
            for i in range(n):
                b = _bloque(ancho, alto, cols[i], a)
                capa.alpha_composite(b, (int(x - b.width / 2),
                                         int(y_base - (i + 0.5) * alto - b.height / 2)))
        f = base.copy()
        f.alpha_composite(capa)
        cuadros.append(f)
    return cuadros


def codigo_frames(base, texto, x, y, ancho, tam=ETIQ, dur=6.0, fps=30, **kw):
    # Ciclo: se escribe, se queda un momento con el cursor parpadeando, se borra.
    total = int(dur * fps)
    cuadros = []
    for k in range(total):
        t = k / total
        if t < 0.55:
            prop = t / 0.55
        elif t < 0.86:
            prop = 1.0
        else:
            prop = max(0.0, 1 - (t - 0.86) / 0.14)
        im = base.copy()
        parpadeo = not (0.55 <= t < 0.86 and int((t - 0.55) * dur * 2) % 2)
        dibujar_codigo(im, texto, x, y, ancho, tam, prop, cursor=parpadeo, **kw)
        cuadros.append(im)
    return cuadros


def parpadeo_frames(pieza, dur=5.0, fps=30):
    # Las dos poses de Séneca solo se diferencian en los ojos: el parpadeo es
    # cambiar de pose dos veces por ciclo. Se repinta solo su caja, partiendo de
    # lo que había debajo, así el resto de la pieza queda intacto.
    if not pieza._mascota:
        raise ErrorCREA('Para el parpadeo, la pieza tiene que llevar a Séneca (pieza.mascota(...))')
    x, y, ancho, alto = pieza._mascota['caja']
    caja = (int(x), int(y), int(x) + ancho, int(y) + alto)
    guino = Image.open(MASCOTA / 'seneca_guino.png').convert('RGBA').resize((ancho, alto), Image.LANCZOS)
    region = pieza._mascota['antes'].crop(caja)
    region.alpha_composite(guino)
    total = int(dur * fps)
    ojos_cerrados = {int(total * f) + i for f in (0.39, 0.82) for i in range(6)}
    cuadros = []
    for i in range(total):
        f = pieza.im.copy()
        if i in ojos_cerrados:
            f.paste(region, caja[:2])
        cuadros.append(f)
    return cuadros


def animar(pieza, tipo, dur=None, fps=30, **kw):
    """Agrega una animación en bucle a la pieza. Va al final: lo que se dibuje después no sale en el MP4.

    - 'burbujas': caja=(x0, y0, x1, y1), n, colores
    - 'torre': x, y_base, n, ancho, alto (evita sola el color del fondo)
    - 'codigo': texto, x, y, ancho, tam (dibuja la tarjeta completa en el JPG y la escribe en el MP4)
    - 'parpadeo': Séneca guiña dos veces (la pieza tiene que llevarla)
    """
    if tipo not in TIPOS:
        raise ErrorCREA(f'La animación "{tipo}" no existe. Usa una de: {", ".join(TIPOS)}')
    if pieza.cuadros is not None:
        raise ErrorCREA('Una pieza lleva una sola animación: si se mueven dos cosas, distrae')
    base = pieza.im.copy()
    if tipo == 'burbujas':
        pieza.cuadros = burbujas(base, dur=dur or 5.0, fps=fps, **kw)
    elif tipo == 'torre':
        kw.setdefault('evitar', pieza.color_fondo)
        pieza.cuadros = torre_bloques(base, dur=dur or 6.0, fps=fps, **kw)
    elif tipo == 'codigo':
        texto, x, y, ancho = kw.pop('texto'), kw.pop('x'), kw.pop('y'), kw.pop('ancho')
        tam = kw.pop('tam', ETIQ)
        kw.setdefault('acento', Y)
        pieza.codigo(texto, x, y, ancho, tam, cursor=False, **kw)
        pieza.cuadros = codigo_frames(base, texto, x, y, ancho, tam, dur=dur or 6.0, fps=fps, **kw)
    else:
        pieza.cuadros = parpadeo_frames(pieza, dur=dur or 5.0, fps=fps)
    pieza.fps, pieza.animacion = fps, tipo
    return pieza


def mp4(cuadros, salida, fps=30):
    """Lista de cuadros → MP4 listo para Instagram: H.264, yuv420p, +faststart y audio en silencio."""
    import imageio_ffmpeg
    w, h = cuadros[0].size
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.Popen(
        [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
         '-s', f'{w}x{h}', '-r', str(fps), '-i', '-',
         # Pista de audio en silencio: sin ella Instagram rechaza el archivo en
         # algunas rutas de subida.
         '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
         '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-crf', '18',
         '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', str(salida)],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    try:
        for c in cuadros:
            p.stdin.write(c.convert('RGB').tobytes())
        p.stdin.close()
    except BrokenPipeError:
        pass
    error = p.stderr.read().decode('utf-8', 'replace')
    if p.wait() != 0:
        raise ErrorCREA(f'ffmpeg no pudo exportar {salida.name}: {error.strip()[-400:]}')
    return salida
