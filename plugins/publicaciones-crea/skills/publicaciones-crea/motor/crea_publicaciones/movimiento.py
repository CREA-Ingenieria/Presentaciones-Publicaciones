"""Estilo «movimiento»: láminas animadas con HyperFrames (HTML que se renderiza a video).

Cada lámina es un proyecto HyperFrames de 1080 × 1350 cuyos elementos llegan con las reglas de
movimiento de la skill hyperframes (references/motion.md): llegadas con colas largas
(expo/power4.out), el título palabra por palabra, los íconos con un resorte de amortiguación ~0,55
y los trazos dibujándose. La foto no se mueve (un acercamiento de cámara en un marco pequeño se ve
mal). Lo que aterriza se queda quieto, y la última imagen es la lámina terminada, así que sirve
también de portada estática.

El marco tiene su propio HTML (`proyecto`). Recortes y arcade se animan a partir de las capas que
arma el motor (`proyecto_capas`): la versión animada es exactamente el diseño estático.

Necesita Node (npx) y el Chrome que HyperFrames encuentra; el render sale sin audio y se le agrega
la pista en silencio que Instagram pide.
"""
import html
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageFilter

from .animacion import info_video
from .base import DARK, FUENTES, MARCA, MARGEN, WHITE, B, ErrorCREA, M, O, T, Y, contraste, cubrir, tinta
from .marco import BLOQUE, FOTO, colores_iconos, ruta_icono

HYPERFRAMES = 'hyperframes@0.8.212'
GSAP = 'gsap@3.14.2'
ANCHO, ALTO = 1080, 1350
DURACION_FOTO = 6.0


def _gsap(cache):
    """GSAP desde npm (el CDN puede estar bloqueado); se guarda una vez en `cache`."""
    destino = Path(cache) / 'gsap.min.js'
    if destino.is_file():
        return destino
    destino.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(['npm', 'pack', GSAP, '--silent', '--pack-destination', str(destino.parent)],
                       capture_output=True, text=True)
    tgz = destino.parent / f'{GSAP.replace("@", "-")}.tgz'
    if r.returncode != 0 or not tgz.is_file():
        raise ErrorCREA(f'No se pudo descargar GSAP de npm: {(r.stderr or r.stdout).strip()[-300:]}')
    subprocess.run(['tar', '-xzf', str(tgz), '-C', str(destino.parent), 'package/dist/gsap.min.js'], check=True)
    shutil.move(str(destino.parent / 'package' / 'dist' / 'gsap.min.js'), destino)
    shutil.rmtree(destino.parent / 'package', ignore_errors=True)
    tgz.unlink()
    return destino


def _palabras(texto, prefijo):
    return ' '.join(f'<span class="palabra {prefijo}">{html.escape(w)}</span>' for w in texto.split())


def proyecto(carpeta, *, titulo, bajada='', chip=None, acento=T, iconos=(), foto=None, video=None, desde=0,
             hasta=None, foco=0.5, ajuste='cubrir', cache=None):
    """Escribe el proyecto HyperFrames de una lámina en `carpeta` y devuelve su duración en segundos."""
    carpeta = Path(carpeta)
    assets = carpeta / 'assets'
    (assets / 'fonts').mkdir(parents=True, exist_ok=True)
    shutil.copy(_gsap(cache or carpeta.parent / '.cache'), assets / 'gsap.min.js')
    for peso in ('Regular', 'Bold', 'ExtraBold', 'SemiBold'):
        shutil.copy(FUENTES / f'Montserrat-{peso}.ttf', assets / 'fonts')
    shutil.copy(MARCA / 'crea_logo.png', assets / 'logo.png')
    # La trama de doodles, ya teñida del acento (una máscara CSS no siempre se aplica en el render).
    from .base import Pieza, POST
    from .marco import trama
    lienzo = Pieza(POST, fondo=(0, 0, 0, 0))
    trama(lienzo, acento)
    lienzo.im.save(assets / 'trama.png')
    colores = colores_iconos(acento, len(iconos))
    for clave, color in zip(iconos, colores):
        shutil.copy(ruta_icono(clave, 'd' if color == Y else 'w'), assets / f'icono-{clave}.png')

    x0, y0, x1, y1 = FOTO
    fw, fh = x1 - x0, y1 - y0
    if video:
        _, _, dur_video = info_video(video)
        hasta = min(hasta or dur_video, dur_video)
        duracion = round(hasta - desde, 2)
        shutil.copy(video, assets / 'video.mp4')
        # Debajo del video: su primer cuadro desenfocado (para el ajuste "contener") y el cuadro final.
        from .animacion import leer_video
        primero = next(leer_video(video, desde, hasta))
        cubrir(primero, fw, fh).filter(ImageFilter.GaussianBlur(28)).convert('RGB').save(assets / 'fondo-video.jpg')
        medio = ('<video id="video" class="clip" data-start="0" data-duration="{d}" data-track-index="2" '
                 'data-media-start="{s}" muted playsinline src="assets/video.mp4"></video>').format(d=duracion, s=desde)
        ajuste_css = 'contain' if ajuste == 'contener' else 'cover'
    else:
        duracion = DURACION_FOTO
        img = Image.open(foto).convert('RGB')
        # Sin acercamiento de cámara: en un marco pequeño se ve mal. La foto va quieta, a su tamaño.
        cubrir(img, fw, fh, 0, foco, ajuste).convert('RGB').save(assets / 'foto.jpg', quality=92)
        medio = ''
        ajuste_css = 'cover'

    iconos_html = ''
    radio = 60
    for i, (clave, color) in enumerate(zip(iconos, colores)):
        cx = x1 - 40 - radio - i * (120 + 16)
        iconos_html += (f'<div class="icono" id="icono-{i}" style="left:{cx - radio - 7}px;top:{y1 - radio - 7}px;'
                        f'background:{color}"><img src="assets/icono-{clave}.png"></div>')
    chip_html = f'<div id="chip">{html.escape(chip.upper())}</div>' if chip else ''
    foto_html = ('<div id="foto-caja" data-layout-allow-overflow><div id="foto-mueve"><img id="foto" src="assets/foto.jpg"></div></div>'
                 if not video else '<div id="foto-caja" data-layout-allow-overflow><img id="fondo-video" src="assets/fondo-video.jpg"></div>')
    seg = M if acento != M else T
    css = f"""
      @font-face {{ font-family: 'CREA'; src: url('assets/fonts/Montserrat-Regular.ttf'); font-weight: 400; }}
      @font-face {{ font-family: 'CREA'; src: url('assets/fonts/Montserrat-SemiBold.ttf'); font-weight: 600; }}
      @font-face {{ font-family: 'CREA'; src: url('assets/fonts/Montserrat-Bold.ttf'); font-weight: 700; }}
      @font-face {{ font-family: 'CREA'; src: url('assets/fonts/Montserrat-ExtraBold.ttf'); font-weight: 800; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {ANCHO}px; height: {ALTO}px; overflow: hidden; background: {WHITE}; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: 'CREA', sans-serif; }}
      .capa {{ position: absolute; inset: 0; }}
      #trama {{ position: absolute; inset: 0; background: url('assets/trama.png') no-repeat top left / 100% 100%; }}
      #bloque {{ position: absolute; left: {BLOQUE[0]}px; top: {BLOQUE[1]}px; width: {BLOQUE[2] - BLOQUE[0]}px;
                height: {BLOQUE[3] - BLOQUE[1]}px; border-radius: 64px; background: {acento}; }}
      #foto-caja {{ position: absolute; left: {x0}px; top: {y0}px; width: {fw}px; height: {fh}px;
                   border-radius: 64px; overflow: hidden; background: {DARK}; }}
      #foto-mueve {{ position: absolute; left: 0; top: 0; width: {fw}px; height: {fh}px; }}
      #foto, #fondo-video {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
      #video {{ position: absolute; left: {x0}px; top: {y0}px; width: {fw}px; height: {fh}px;
               border-radius: 64px; object-fit: {ajuste_css}; z-index: 2; }}
      #telon {{ position: absolute; left: {x0 - 2}px; top: {y0 - 2}px; width: {fw + 4}px; height: {fh + 4}px;
               border-radius: 66px; background: {WHITE}; transform-origin: 50% 0%; }}
      #punto {{ position: absolute; left: {BLOQUE[2] - 60}px; top: {BLOQUE[1] + 8}px; width: 52px; height: 52px;
               border-radius: 50%; background: {Y}; }}
      #chip {{ position: absolute; left: {x0 + 40}px; top: 148px; padding: 16px 28px; border-radius: 40px;
              background: {acento}; color: {WHITE}; font-weight: 600; font-size: 30px; letter-spacing: 0.02em; }}
      .icono {{ position: absolute; width: 134px; height: 134px; border-radius: 50%; border: 7px solid {WHITE};
               display: flex; align-items: center; justify-content: center; }}
      .icono img {{ width: 70px; height: 70px; }}
      #titulo {{ position: absolute; left: {MARGEN}px; top: 820px; width: {ANCHO - 2 * MARGEN}px; color: {acento};
                font-weight: 700; font-size: 96px; line-height: 1.08; letter-spacing: -0.01em; }}
      #bajada {{ position: absolute; left: {MARGEN}px; width: {ANCHO - 2 * MARGEN - 168}px; color: #3C3C4A;
                font-weight: 400; font-size: 36px; line-height: 1.32; }}
      .palabra {{ display: inline-block; }}
      #logo {{ position: absolute; left: {ANCHO - MARGEN - 120}px; top: 1158px; width: 120px; }}
      svg {{ position: absolute; inset: 0; overflow: visible; }}
    """
    trazos = f"""
      <svg width="{ANCHO}" height="{ALTO}" viewBox="0 0 {ANCHO} {ALTO}">
        <circle id="anillo-1" cx="0" cy="{ALTO}" r="150" fill="none" stroke="{acento}" stroke-width="16"/>
        <circle id="anillo-2" cx="0" cy="{ALTO}" r="112" fill="none" stroke="{seg}" stroke-width="16"/>
        <circle id="anillo-3" cx="0" cy="{ALTO}" r="74" fill="none" stroke="{Y}" stroke-width="16"/>
        <path id="ele" d="M {MARGEN - 20} 430 L {MARGEN - 20} {y1 + 20} L {MARGEN + 340} {y1 + 20}"
              fill="none" stroke="{DARK}" stroke-width="5" stroke-linejoin="round"/>
        <path id="circuito" d="M 236 {ALTO - 44} L {ANCHO} {ALTO - 44}" fill="none" stroke="{DARK}" stroke-width="5"/>
        <circle id="nodo-1" cx="560" cy="{ALTO - 44}" r="13" fill="{T}"/>
        <circle id="nodo-2" cx="604" cy="{ALTO - 44}" r="8" fill="{T}"/>
      </svg>"""
    escena = f"""
    <div id="fondo" class="clip capa" data-start="0" data-duration="{duracion}" data-track-index="1">
      <div id="trama"></div>
      {trazos}
      <div id="bloque"></div>
      {foto_html}
      <div id="titulo">{_palabras(titulo, 'p-titulo')}</div>
      {f'<div id="bajada">{_palabras(bajada, "p-bajada")}</div>' if bajada else ''}
      <img id="logo" src="assets/logo.png">
    </div>
    {medio}
    <div id="encima" class="clip capa" data-start="0" data-duration="{duracion}" data-track-index="3"
         style="z-index: 3" data-layout-allow-overlap>
      <div id="telon"></div>
      <div id="punto"></div>
      {chip_html}
      {iconos_html}
    </div>"""
    guion = f"""
      const tl = gsap.timeline({{ paused: true }});
      const D = {duracion};
      // Los trazos se dibujan: anillos y líneas con stroke-dasharray.
      document.querySelectorAll('#ele, #circuito, #anillo-1, #anillo-2, #anillo-3').forEach((el) => {{
        const largo = el.getTotalLength();
        el.style.strokeDasharray = largo;
        el.style.strokeDashoffset = largo;
      }});
      tl.fromTo('#bloque', {{ x: 140, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.8, ease: 'expo.out' }}, 0.1);
      tl.fromTo('#telon', {{ scaleY: 1 }}, {{ scaleY: 0, duration: 0.7, ease: 'power3.inOut' }}, 0.3);
      tl.to(['#anillo-1', '#anillo-2', '#anillo-3'], {{ strokeDashoffset: 0, duration: 0.9, ease: 'power2.inOut',
            stagger: 0.12 }}, 0.4);
      tl.to('#ele', {{ strokeDashoffset: 0, duration: 0.7, ease: 'power2.inOut' }}, 0.6);
      tl.fromTo('#punto', {{ scale: 0 }}, {{ scale: 1, duration: 0.45, ease: 'back.out(2.2)' }}, 0.8);
      {"tl.fromTo('#chip', { x: -40, opacity: 0, filter: 'blur(6px)' }, { x: 0, opacity: 1, filter: 'blur(0px)', duration: 0.4, ease: 'power4.out' }, 0.9);" if chip else ''}
      tl.fromTo('.icono', {{ scale: 0, rotation: -25 }}, {{ scale: 1, rotation: 0, duration: 0.8,
            ease: 'elastic.out(1, 0.55)', stagger: 0.09 }}, 1.0);
      tl.fromTo('.p-titulo', {{ opacity: 0, filter: 'blur(6px)' }}, {{ opacity: 1, filter: 'blur(0px)',
            duration: 0.16, ease: 'power2.out', stagger: 0.07 }}, 1.15);
      tl.fromTo('.p-bajada', {{ opacity: 0, color: '#B8C0CC' }}, {{ opacity: 1, color: '#3C3C4A', duration: 0.12,
            stagger: 0.04 }}, 1.6);
      tl.to('#circuito', {{ strokeDashoffset: 0, duration: 0.8, ease: 'power2.inOut' }}, 1.4);
      tl.fromTo(['#nodo-1', '#nodo-2'], {{ scale: 0, transformOrigin: '50% 50%' }}, {{ scale: 1, duration: 0.35,
            ease: 'back.out(2)', stagger: 0.08 }}, 2.0);
      tl.fromTo('#logo', {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: 'expo.out' }}, 1.9);
      // La bajada se ubica bajo el título según cuántas líneas tomó.
      const t = document.getElementById('titulo');
      const b = document.getElementById('bajada');
      if (b) b.style.top = (t.offsetTop + t.offsetHeight + 24) + 'px';
      window.__timelines['main'] = tl;
    """
    pagina = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={ANCHO}, height={ALTO}" />
    <script src="assets/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duracion}"
         data-width="{ANCHO}" data-height="{ALTO}">
      {escena}
    </div>
    <script>{guion}</script>
  </body>
</html>
"""
    (carpeta / 'index.html').write_text(pagina, encoding='utf-8')
    (carpeta / 'hyperframes.json').write_text(json.dumps({'paths': {'assets': 'assets'}}), encoding='utf-8')
    return duracion


def render(carpeta, salida):
    """Renderiza el proyecto y le agrega la pista de audio en silencio. Devuelve la ruta del MP4."""
    import imageio_ffmpeg
    carpeta, salida = Path(carpeta).resolve(), Path(salida).resolve()
    crudo = carpeta / 'render.mp4'
    r = subprocess.run(['npx', '-y', HYPERFRAMES, 'render', '--output', str(crudo)], cwd=carpeta,
                       capture_output=True, text=True)
    if r.returncode != 0 or not crudo.is_file():
        raise ErrorCREA(f'HyperFrames no pudo renderizar {carpeta.name}: {(r.stdout + r.stderr).strip()[-800:]}')
    salida.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', str(crudo),
                        '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
                        '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest',
                        '-movflags', '+faststart', str(salida)], capture_output=True, text=True)
    if r.returncode != 0:
        raise ErrorCREA(f'ffmpeg no pudo agregar el audio a {salida.name}: {r.stderr.strip()[-300:]}')
    return salida


def portada(mp4, salida):
    """La última imagen del video: la lámina terminada, para la portada estática del carrusel."""
    import imageio_ffmpeg
    r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-sseof', '-0.1', '-i',
                        str(mp4), '-frames:v', '1', '-q:v', '2', str(salida)], capture_output=True, text=True)
    if r.returncode != 0:
        raise ErrorCREA(f'No se pudo sacar la portada de {Path(mp4).name}: {r.stderr.strip()[-300:]}')
    return Path(salida)


# Cómo entra cada pieza, por estilo. Las claves son los roles de las capas (ver recortes.py y arcade.py).
ANIMACION = {
    'recortes': """
      tl.fromTo('#foto-grupo', { scale: 1.12, rotation: 4, opacity: 0, transformOrigin: '540px 432px' },
                { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: 'expo.out' }, 0.15);
      tl.fromTo('#sombra-foto', { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.5);
      tl.fromTo('.cinta', { scaleX: 0, transformOrigin: '0% 50%' }, { scaleX: 1, duration: 0.25, ease: 'power2.out',
                stagger: 0.12 }, 0.65);
      tl.fromTo('.sello', { scale: 2.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.12, ease: 'power4.in' }, 0.95);
      tl.to('.sello', { scale: 1.1, duration: 0.05, ease: 'power2.out' }, 1.07);
      tl.to('.sello', { scale: 1, duration: 0.35, ease: 'elastic.out(1, 0.4)' }, 1.12);
      tl.fromTo('.icono', { scale: 0, rotation: -30 }, { scale: 1, rotation: 0, duration: 0.8,
                ease: 'elastic.out(1, 0.55)', stagger: 0.1 }, 1.1);
      tl.fromTo('.trazo', { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0% 0 0)', duration: 0.6,
                ease: 'power2.inOut', stagger: 0.15 }, 1.3);
      tl.fromTo('.palabra', { y: -70, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: 'back.out(2.2)',
                stagger: 0.07 }, 1.25);
      tl.fromTo('.nota', { x: -60, rotation: -3, opacity: 0 }, { x: 0, rotation: 0, opacity: 1, duration: 0.4,
                ease: 'expo.out' }, 1.6);
      tl.fromTo('.palabra-bajada', { opacity: 0 }, { opacity: 1, duration: 0.1, stagger: 0.035 }, 1.8);
      tl.fromTo('.sticker', { scale: 0, rotation: -20 }, { scale: 1, rotation: 0, duration: 0.6,
                ease: 'back.out(1.8)' }, 2.0);
      tl.fromTo('.logo', { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: 'back.out(2)' }, 2.2);
    """,
    # Arcade va en pasos, como un juego: nada se desliza suave.
    'arcade': """
      tl.fromTo('.ventana', { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: 'steps(5)' }, 0.1);
      tl.fromTo('#telon', { scaleY: 1, transformOrigin: '50% 100%' }, { scaleY: 0, duration: 0.6, ease: 'steps(12)' },
                0.45);
      tl.fromTo('.hud', { y: -60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: 'steps(4)' }, 0.25);
      tl.fromTo('.corazon', { scale: 0 }, { scale: 1, duration: 0.12, ease: 'steps(2)', stagger: 0.08 }, 0.6);
      tl.fromTo('.item', { y: -24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.2, ease: 'steps(3)', stagger: 0.1 },
                0.9);
      tl.fromTo('.palabra', { y: -16, opacity: 0 }, { y: 0, opacity: 1, duration: 0.12, ease: 'steps(2)',
                stagger: 0.14 }, 1.15);
      tl.fromTo('.dialogo', { scaleX: 0, transformOrigin: '0% 50%' }, { scaleX: 1, duration: 0.3, ease: 'steps(6)' },
                1.8);
      tl.fromTo('.logo', { opacity: 0 }, { opacity: 1, duration: 0.4, ease: 'steps(4)' }, 2.0);
    """,
}
VELOCIDAD_ESCRITURA = 38      # letras por segundo, como el diálogo de la versión estática


def proyecto_capas(carpeta, pieza, estilo, video=None, desde=0, hasta=None, ajuste='cubrir', cache=None):
    """Escribe el proyecto HyperFrames de una lámina de recortes o arcade a partir de `pieza.capas`.

    Cada capa es una imagen en su posición; su rol decide cómo entra. Devuelve la duración.
    """
    if estilo not in ANIMACION:
        raise ErrorCREA(f'No hay animación por capas para el estilo "{estilo}"')
    if not pieza.capas:
        raise ErrorCREA('La pieza no tiene capas: se arma con lamina(..., estilo="recortes" o "arcade")')
    carpeta = Path(carpeta)
    assets = carpeta / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copy(_gsap(cache or carpeta.parent / '.cache'), assets / 'gsap.min.js')
    if video:
        _, _, dur_video = info_video(video)
        hasta = min(hasta or dur_video, dur_video)
        duracion = round(hasta - desde, 2)
        shutil.copy(video, assets / 'video.mp4')
    else:
        duracion = DURACION_FOTO

    def img(c, extra=''):
        nombre = f'{c.nombre}.png'
        c.img.save(assets / nombre)
        return (f'<img id="{c.nombre}" class="{c.rol}" src="assets/{nombre}" '
                f'style="position:absolute;left:{c.x}px;top:{c.y}px;width:{c.img.width}px;'
                f'height:{c.img.height}px{extra}">')

    fondo = [c for c in pieza.capas if not c.encima and c.rol != 'foto']
    fotos = [c for c in pieza.capas if c.rol == 'foto']
    encima = [c for c in pieza.capas if c.encima]
    medio = ''
    if video:
        if estilo == 'recortes':
            from .recortes import CENTRO_FOTO, FOTO as TAM, GIRO
            w, h = TAM
            # El video va girado como la copia (Pillow gira al revés que CSS).
            medio = (f'<video id="video" class="clip" data-start="0" data-duration="{duracion}" data-track-index="2" '
                     f'data-media-start="{desde}" muted playsinline src="assets/video.mp4" '
                     f'style="position:absolute;left:{CENTRO_FOTO[0] - w // 2}px;top:{CENTRO_FOTO[1] - h // 2}px;'
                     f'width:{w}px;height:{h}px;object-fit:{"contain" if ajuste == "contener" else "cover"};'
                     f'transform:rotate({-GIRO}deg)"></video>')
        else:
            from .arcade import ESC, VENTANA
            x0, y0, x1, y1 = (v * ESC for v in VENTANA)
            medio = (f'<video id="video" class="clip" data-start="0" data-duration="{duracion}" data-track-index="2" '
                     f'data-media-start="{desde}" muted playsinline src="assets/video.mp4" '
                     f'style="position:absolute;left:{x0}px;top:{y0}px;width:{x1 - x0}px;height:{y1 - y0}px;'
                     f'object-fit:{"contain" if ajuste == "contener" else "cover"}"></video>')
    grupo = ''.join(img(c) for c in fotos) + medio
    telon = ''
    if estilo == 'arcade':
        from .arcade import ESC, NOCHE, VENTANA
        x0, y0, x1, y1 = (v * ESC for v in VENTANA)
        telon = (f'<div id="telon" style="position:absolute;left:{x0}px;top:{y0}px;width:{x1 - x0}px;'
                 f'height:{y1 - y0}px;background:{NOCHE[1]}"></div>')

    # La escritura del diálogo (arcade): línea por línea, letra por letra, y luego el cursor parpadea.
    escritura = ''
    t = 2.1
    lineas = [c for c in encima if c.rol == 'escritura']
    for c in lineas:
        letras = getattr(c, 'letras', 20)
        dur = round(letras / VELOCIDAD_ESCRITURA, 2)
        escritura += (f"tl.fromTo('#{c.nombre}', {{ clipPath: 'inset(0 100% 0 0)' }}, {{ clipPath: 'inset(0 0% 0 0)', "
                      f"duration: {dur}, ease: 'steps({letras})' }}, {t:.2f});\n")
        t += dur + 0.05
    if any(c.rol == 'cursor' for c in encima):
        escritura += "tl.set('#cursor', { opacity: 0 }, 0);\n"
        k, visible = t, True
        while k < duracion - 0.05:
            escritura += f"tl.set('#cursor', {{ opacity: {1 if visible else 0} }}, {k:.2f});\n"
            visible = not visible
            k += 0.4

    pagina = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={ANCHO}, height={ALTO}" />
    <script src="assets/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {ANCHO}px; height: {ALTO}px; overflow: hidden; background: {WHITE}; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      .capa {{ position: absolute; inset: 0; }}
      img {{ display: block; image-rendering: {"pixelated" if estilo == "arcade" else "auto"}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{duracion}"
         data-width="{ANCHO}" data-height="{ALTO}">
      <div id="capa-fondo" class="clip capa" data-start="0" data-duration="{duracion}" data-track-index="1"
           data-layout-allow-overlap>
        {''.join(img(c) for c in fondo)}
      </div>
      <div id="foto-grupo" class="capa" style="z-index:2">{grupo}</div>
      <div id="capa-encima" class="clip capa" data-start="0" data-duration="{duracion}" data-track-index="3"
           style="z-index:3" data-layout-allow-overlap>
        {telon}
        {''.join(img(c) for c in encima)}
      </div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {ANIMACION[estilo]}
      {escritura}
      window.__timelines['main'] = tl;
    </script>
  </body>
</html>
"""
    (carpeta / 'index.html').write_text(pagina, encoding='utf-8')
    (carpeta / 'hyperframes.json').write_text(json.dumps({'paths': {'assets': 'assets'}}), encoding='utf-8')
    return duracion


def carrusel(carpeta, laminas, acento=T, estilo='marco', cache=None):
    """Renderiza cada lámina (dicts con los argumentos de `lamina`) a `carpeta/carrusel-N.mp4`.

    'marco' usa su propio HTML; 'recortes' y 'arcade' se animan desde las capas del motor.
    La última imagen de cada video es la lámina terminada: sale también como JPG.
    """
    from .piezas import lamina
    carpeta = Path(carpeta)
    proyectos = carpeta / 'proyectos'
    archivos = []
    for i, datos in enumerate(laminas, 1):
        p = proyectos / f'carrusel-{i}'
        if p.exists():
            shutil.rmtree(p)
        cache_i = cache or proyectos / '.cache'
        if estilo == 'marco':
            proyecto(p, acento=acento, cache=cache_i,
                     **{k: v for k, v in datos.items() if k not in ('sticker', 'nivel')})
        else:
            datos = dict(datos)
            if estilo != 'recortes':
                datos.pop('sticker', None)
            if estilo != 'arcade':
                datos.pop('nivel', None)
            pieza = lamina(datos.pop('foto', None), acento=acento, estilo=estilo, **datos)
            proyecto_capas(p, pieza, estilo, video=datos.get('video'), desde=datos.get('desde', 0),
                           hasta=datos.get('hasta'), ajuste=datos.get('ajuste', 'cubrir'), cache=cache_i)
        mp4 = render(p, carpeta / f'carrusel-{i}.mp4')
        archivos.append(mp4)
        archivos.append(portada(mp4, carpeta / f'carrusel-{i}.jpg'))
        (p / 'render.mp4').unlink(missing_ok=True)
        print(f'-> {mp4}')
    return archivos


# --------------------------------------------------------------------------- reel vertical

REEL_ANCHO, REEL_ALTO = 1080, 1920
ESCENA = 3.0          # cinco escenas de 3 s: gancho, revelación, conceptos, momento, cierre


def _foto_reel(origen, destino, w, h, foco=0.5):
    cubrir(Image.open(origen).convert('RGB'), w, h, 0, foco).convert('RGB').save(destino, quality=92)


def reel(carpeta, *, gancho, revelacion, conceptos, momento, cierre, contacto=None, acento=T, cache=None):
    """Escribe un reel vertical de 15 s con la estructura de /brag: gancho → revelación → momentos → cierre.

    - gancho: video (vertical idealmente), titulo, chip, desde.
    - revelacion: foto, titulo, bajada, foco.
    - conceptos: antes ('Hablamos de'), palabras (3 a 5, una gira como tragamonedas), iconos.
    - momento: video, titulo, desde.
    - cierre: foto, titulo, bajada, foco.
    - contacto (opcional): titulo, destacar (una palabra del título en amarillo) y lineas: tuplas
      (ícono, texto), con '@' para una cuenta. Es la última escena, de 4,5 s, sobre el color del acento,
      con tarjetas, anillos, la línea de la pared y Séneca saludando: un reel se ve fuera del perfil y
      tiene que decir dónde escribir.
    Texto solo en la banda segura de un reel (168 a 1330 px); debajo, solo decoración.
    Devuelve la duración.
    """
    carpeta = Path(carpeta)
    assets = carpeta / 'assets'
    (assets / 'fonts').mkdir(parents=True, exist_ok=True)
    shutil.copy(_gsap(cache or carpeta.parent / '.cache'), assets / 'gsap.min.js')
    for peso in ('Regular', 'SemiBold', 'Bold', 'ExtraBold'):
        shutil.copy(FUENTES / f'Montserrat-{peso}.ttf', assets / 'fonts')
    shutil.copy(MARCA / 'crea_logo.png', assets / 'logo.png')
    from .base import Pieza, STORY
    from .marco import trama
    lienzo = Pieza(STORY, fondo=(0, 0, 0, 0))
    trama(lienzo, acento)
    lienzo.im.save(assets / 'trama.png')
    from .animacion import leer_video
    shutil.copy(gancho['video'], assets / 'gancho.mp4')
    shutil.copy(momento['video'], assets / 'momento.mp4')
    primero = next(leer_video(momento['video'], momento.get('desde', 0)))
    cubrir(primero, REEL_ANCHO, REEL_ALTO).filter(ImageFilter.GaussianBlur(40)).convert('RGB').save(
        assets / 'momento-fondo.jpg', quality=85)
    caja_foto = (1080 - 2 * 96, 760)
    _foto_reel(revelacion['foto'], assets / 'revelacion.jpg', *caja_foto, revelacion.get('foco', 0.5))
    _foto_reel(cierre['foto'], assets / 'cierre.jpg', *caja_foto, cierre.get('foco', 0.5))
    iconos = conceptos.get('iconos', ())
    colores = colores_iconos(acento, len(iconos))
    for clave, color in zip(iconos, colores):
        shutil.copy(ruta_icono(clave, 'd' if color == Y else 'w'), assets / f'icono-{clave}.png')
    shutil.copy(ruta_icono('bulb', 'd'), assets / 'icono-transicion.png')

    t1, t2, t3, t4, t5 = ESCENA, 2 * ESCENA, 3 * ESCENA, 4 * ESCENA, 5 * ESCENA
    DURACION_CONTACTO = 4.5
    total = t5 + (DURACION_CONTACTO if contacto else 0)
    e = html.escape
    palabras = conceptos['palabras']
    rodillo = ''.join(f'<div class="rueda-p">{e(p)}</div>' for p in palabras)
    iconos_html = ''.join(f'<div class="ic" style="background:{c}"><img src="assets/icono-{k}.png"></div>'
                          for k, c in zip(iconos, colores))
    seg = M if acento != M else T
    # El reel pone letra sobre el acento a pantalla completa: con turquesa o naranja, la letra va oscura y la
    # palabra destacada, amarilla sobre una etiqueta oscura (el amarillo sobre esos acentos no se lee).
    sobre = tinta(acento)
    titulo_claro = acento if contraste(acento, WHITE) >= 3 else DARK
    destacado = (f'color: {Y};' if contraste(Y, acento) >= 3 else
                 f'color: {Y}; background: {DARK}; padding: 0 0.14em; border-radius: 0.12em;')
    css = f"""
      @font-face {{ font-family: 'CREA'; src: url('assets/fonts/Montserrat-Regular.ttf'); font-weight: 400; }}
      @font-face {{ font-family: 'CREA'; src: url('assets/fonts/Montserrat-SemiBold.ttf'); font-weight: 600; }}
      @font-face {{ font-family: 'CREA'; src: url('assets/fonts/Montserrat-Bold.ttf'); font-weight: 700; }}
      @font-face {{ font-family: 'CREA'; src: url('assets/fonts/Montserrat-ExtraBold.ttf'); font-weight: 800; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {REEL_ANCHO}px; height: {REEL_ALTO}px; overflow: hidden; background: {WHITE}; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: 'CREA', sans-serif; }}
      .escena {{ position: absolute; inset: 0; overflow: hidden; }}
      .vid {{ position: absolute; left: 0; top: 0; width: {REEL_ANCHO}px; height: {REEL_ALTO}px; object-fit: cover; }}
      .titulo {{ position: absolute; left: 96px; width: 820px; font-weight: 800; line-height: 1.04;
                letter-spacing: -0.01em; }}
      .palabra {{ display: inline-block; }}
      .bajada {{ position: absolute; left: 96px; width: 800px; font-size: 38px; line-height: 1.32; font-weight: 400; }}
      .chip {{ position: absolute; left: 96px; top: 220px; padding: 16px 28px; border-radius: 40px; font-weight: 600;
              font-size: 32px; letter-spacing: 0.03em; color: {sobre}; background: {acento}; }}
      .tarjeta {{ position: absolute; left: 96px; top: 250px; width: {caja_foto[0]}px; height: {caja_foto[1]}px;
                 border-radius: 64px; overflow: hidden; }}
      .tarjeta .mueve {{ position: absolute; left: 0; top: 0; width: {caja_foto[0]}px; height: {caja_foto[1]}px; }}
      .tarjeta img {{ width: 100%; height: 100%; display: block; }}
      .bloque {{ position: absolute; left: 120px; top: 226px; width: {caja_foto[0]}px; height: {caja_foto[1]}px;
                border-radius: 64px; background: {acento}; }}
      .punto {{ position: absolute; left: {96 + caja_foto[0] - 34}px; top: 214px; width: 56px; height: 56px;
               border-radius: 50%; background: {Y}; }}
      .trama {{ position: absolute; inset: 0; background: url('assets/trama.png') no-repeat top left / 100% 100%; }}
      #velo-gancho {{ position: absolute; inset: 0;
                     background: linear-gradient(180deg, rgba(30,42,58,0.55) 0%, rgba(30,42,58,0) 20%,
                     rgba(30,42,58,0) 34%, rgba(30,42,58,0.78) 47%, rgba(30,42,58,0.88) 80%); }}
      #rueda {{ position: absolute; left: 96px; top: 860px; height: 130px; width: 900px; overflow: hidden; }}
      #rueda-tira {{ position: absolute; left: 0; top: 0; }}
      .rueda-p {{ height: 130px; font-size: 112px; font-weight: 800; color: {DARK}; line-height: 130px; }}
      #iconos {{ position: absolute; left: 96px; top: 1110px; display: flex; gap: 22px; }}
      .ic {{ width: 132px; height: 132px; border-radius: 50%; border: 8px solid {WHITE}; display: flex;
            align-items: center; justify-content: center; }}
      .ic img {{ width: 70px; height: 70px; }}
      #momento-fondo {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #momento-velo {{ position: absolute; inset: 0; background: rgba(30,42,58,0.72); }}
      #momento-vid {{ position: absolute; left: 0; top: 420px; width: {REEL_ANCHO}px; height: 608px;
                     object-fit: cover; }}
      #logo-cierre {{ position: absolute; left: {REEL_ANCHO // 2 - 75}px; top: 1500px; width: 150px; }}
      .transicion {{ position: absolute; pointer-events: none; }}
      #barrido {{ left: 0; top: 0; width: {REEL_ANCHO}px; height: {REEL_ALTO}px; background: {acento};
                 transform-origin: 50% 100%; }}
      #bombillo {{ left: {REEL_ANCHO // 2 - 90}px; top: {REEL_ALTO // 2 - 90}px; width: 180px; height: 180px;
                  border-radius: 50%; background: {Y}; display: flex; align-items: center; justify-content: center; }}
      #bombillo img {{ width: 100px; height: 100px; }}
      #iris {{ left: 0; top: 0; width: {REEL_ANCHO}px; height: {REEL_ALTO}px; background: {WHITE}; }}
      #barrido-2 {{ left: 0; top: 0; width: {REEL_ANCHO}px; height: {REEL_ALTO}px; background: {acento}; }}
      #trama-contacto {{ position: absolute; inset: 0; background: url('assets/trama-contacto.png') no-repeat top left / 100% 100%; }}
      .destacado {{ {destacado} }}
      .tarjeta-c {{ position: absolute; left: 96px; width: 820px; min-height: 108px; border-radius: 54px;
                   background: {WHITE}; display: flex; align-items: center; gap: 26px; padding: 14px 40px 14px 16px;
                   box-shadow: 10px 12px 0 rgba(30,42,58,0.28); }}
      .tarjeta-c .circulo {{ flex: none; width: 80px; height: 80px; border-radius: 50%; display: flex;
                            align-items: center; justify-content: center; }}
      .tarjeta-c .circulo img {{ width: 46px; height: 46px; }}
      .tarjeta-c .arroba {{ color: {WHITE}; font-size: 50px; font-weight: 800; line-height: 1; margin-top: -6px; }}
      .tarjeta-c .texto {{ color: {DARK}; font-size: 36px; font-weight: 700; line-height: 1.2; }}
      #seneca, #seneca-guino {{ position: absolute; left: 748px; top: 1262px; height: 600px; }}
      #logo-contacto {{ position: absolute; left: 96px; top: 1196px; width: 120px; }}
      #firma {{ position: absolute; left: 240px; top: 1206px; color: {sobre}; }}
      #firma b {{ display: block; font-size: 32px; font-weight: 800; }}
      #firma span {{ display: block; font-size: 28px; font-weight: 400; opacity: 0.9; margin-top: 6px; }}
      svg {{ position: absolute; inset: 0; overflow: visible; }}
    """
    anillos = f"""
      <svg width="{REEL_ANCHO}" height="{REEL_ALTO}" viewBox="0 0 {REEL_ANCHO} {REEL_ALTO}">
        <circle class="anillo" cx="0" cy="{REEL_ALTO}" r="190" fill="none" stroke="{acento}" stroke-width="18"/>
        <circle class="anillo" cx="0" cy="{REEL_ALTO}" r="146" fill="none" stroke="{seg}" stroke-width="18"/>
        <circle class="anillo" cx="0" cy="{REEL_ALTO}" r="102" fill="none" stroke="{Y}" stroke-width="18"/>
        <path d="M 300 {REEL_ALTO - 70} L {REEL_ANCHO} {REEL_ALTO - 70}" stroke="{DARK}" stroke-width="6"/>
        <circle cx="640" cy="{REEL_ALTO - 70}" r="15" fill="{T}"/><circle cx="690" cy="{REEL_ALTO - 70}" r="9" fill="{T}"/>
      </svg>"""

    escena_contacto = ''
    if contacto:
        from .base import MASCOTA
        shutil.copy(MARCA / 'crea_logo.png', assets / 'logo-contacto.png')
        shutil.copy(MASCOTA / 'seneca_saludo.png', assets / 'seneca.png')
        shutil.copy(MASCOTA / 'seneca_guino.png', assets / 'seneca-guino.png')
        blanca = Pieza(STORY, fondo=(0, 0, 0, 0))
        trama(blanca, WHITE, opacidad=0.09)
        blanca.im.save(assets / 'trama-contacto.png')
        colores_c = (M, T, O, Y, B)
        tarjetas = ''
        for i, linea in enumerate(contacto['lineas']):
            icono, texto = linea if isinstance(linea, (tuple, list)) else (None, linea)
            color = colores_c[i % len(colores_c)]
            if icono == '@':
                dentro = '<span class="arroba">@</span>'
            elif icono:
                shutil.copy(ruta_icono(icono, 'd' if color == Y else 'w'), assets / f'contacto-{icono}.png')
                dentro = f'<img src="assets/contacto-{icono}.png">'
            else:
                dentro = ''
            tarjetas += (f'<div class="tarjeta-c" style="top: {640 + 136 * i}px"><div class="circulo" '
                         f'style="background: {color}">{dentro}</div><div class="texto">{html.escape(texto)}</div></div>')
        destacar = (contacto.get('destacar') or '').lower()
        titulo_c = ' '.join(
            f'<span class="palabra p-contacto{" destacado" if destacar and w.strip("¡!¿?,.").lower() == destacar else ""}">'
            f'{html.escape(w)}</span>' for w in contacto['titulo'].split())
        aros = f"""<svg width="{REEL_ANCHO}" height="{REEL_ALTO}" viewBox="0 0 {REEL_ANCHO} {REEL_ALTO}">
        <circle class="aro-c" cx="{REEL_ANCHO}" cy="0" r="190" fill="none" stroke="{M}" stroke-width="18"/>
        <circle class="aro-c" cx="{REEL_ANCHO}" cy="0" r="146" fill="none" stroke="{Y}" stroke-width="18"/>
        <circle class="aro-c" cx="{REEL_ANCHO}" cy="0" r="102" fill="none" stroke="{T}" stroke-width="18"/>
        <circle class="aro-c" cx="0" cy="{REEL_ALTO}" r="220" fill="none" stroke="{Y}" stroke-width="18"/>
        <circle class="aro-c" cx="0" cy="{REEL_ALTO}" r="176" fill="none" stroke="{M}" stroke-width="18"/>
        <circle class="aro-c" cx="0" cy="{REEL_ALTO}" r="132" fill="none" stroke="{T}" stroke-width="18"/>
        <path id="circuito-c" d="M 96 1420 L 660 1420" stroke="{WHITE}" stroke-width="6" fill="none"/>
        <circle class="nodo-c" cx="420" cy="1420" r="15" fill="{Y}"/>
        <circle class="nodo-c" cx="464" cy="1420" r="9" fill="{Y}"/>
      </svg>"""
        escena_contacto = f'''<div id="s-contacto" class="clip escena" data-start="{t5}" data-duration="{DURACION_CONTACTO}"
         data-track-index="10" style="z-index:10; background: {acento}" data-layout-allow-overlap>
      <div id="trama-contacto"></div>
      {aros}
      <div class="titulo" style="top: 250px; font-size: 80px; color: {sobre}">{titulo_c}</div>
      {tarjetas}
      <img id="seneca" src="assets/seneca.png">
      <img id="seneca-guino" src="assets/seneca-guino.png" style="opacity: 0">
      <img id="logo-contacto" src="assets/logo-contacto.png">
      <div id="firma"><b>Laboratorio CREA</b><span>Universidad de los Andes</span></div>
    </div>'''

    def pal(texto, clase):
        return ' '.join(f'<span class="palabra {clase}">{e(w)}</span>' for w in texto.split())
    cuerpo = f"""
    <video id="gancho-vid" class="clip vid" data-start="0" data-duration="{t1}" data-track-index="1"
           data-media-start="{gancho.get('desde', 0)}" muted playsinline src="assets/gancho.mp4" style="z-index:1"></video>
    <div id="s-gancho" class="clip escena" data-start="0" data-duration="{t1}" data-track-index="2" style="z-index:2"
         data-layout-allow-overlap>
      <div id="velo-gancho"></div>
      <div class="chip" id="chip-gancho">{e(gancho.get('chip', '').upper())}</div>
      <div class="titulo" style="top: 960px; font-size: 112px; color: {WHITE}">{pal(gancho['titulo'], 'p-gancho')}</div>
    </div>
    <div id="s-revela" class="clip escena" data-start="{t1}" data-duration="{ESCENA}" data-track-index="3"
         style="z-index:3; background: {WHITE}">
      <div class="trama"></div>
      <div class="bloque" id="bloque-revela"></div>
      <div class="tarjeta"><div class="mueve" id="mueve-revela"><img src="assets/revelacion.jpg"></div></div>
      <div class="punto"></div>
      <div class="titulo" id="titulo-revela" style="top: 1060px; font-size: 80px; color: {titulo_claro}">
        {pal(revelacion['titulo'], 'p-revela')}</div>
      <div class="bajada" id="bajada-revela" style="top: 1250px; color: #3C3C4A">{e(revelacion.get('bajada', ''))}</div>
      {anillos}
    </div>
    <div id="s-conceptos" class="clip escena" data-start="{t2}" data-duration="{ESCENA}" data-track-index="4"
         style="z-index:4; background: {Y}">
      <div class="titulo" style="top: 760px; font-size: 56px; font-weight: 600; color: {DARK}">
        {e(conceptos.get('antes', 'Hablamos de'))}</div>
      <div id="rueda"><div id="rueda-tira">{rodillo}</div></div>
      <div id="iconos">{iconos_html}</div>
    </div>
    <div id="s-momento" class="clip escena" data-start="{t3}" data-duration="{ESCENA}" data-track-index="5"
         style="z-index:5; background: {DARK}">
      <img id="momento-fondo" src="assets/momento-fondo.jpg">
      <div id="momento-velo"></div>
    </div>
    <video id="momento-vid" class="clip" data-start="{t3}" data-duration="{ESCENA}" data-track-index="6"
           data-media-start="{momento.get('desde', 0)}" muted playsinline src="assets/momento.mp4"
           style="z-index:6"></video>
    <div id="s-momento-texto" class="clip escena" data-start="{t3}" data-duration="{ESCENA}" data-track-index="7"
         style="z-index:7">
      <div class="chip" style="top: 300px">{e(gancho.get('chip', '').upper())}</div>
      <div class="titulo" style="top: 1090px; font-size: 92px; color: {WHITE}">{pal(momento['titulo'], 'p-momento')}</div>
    </div>
    <div id="s-cierre" class="clip escena" data-start="{t4}" data-duration="{ESCENA}" data-track-index="8"
         style="z-index:8; background: {WHITE}">
      <div class="trama"></div>
      <div class="bloque"></div>
      <div class="tarjeta"><div class="mueve" id="mueve-cierre"><img src="assets/cierre.jpg"></div></div>
      <div class="punto"></div>
      <div class="titulo" style="top: 1060px; font-size: 88px; color: {titulo_claro}">{pal(cierre['titulo'], 'p-cierre')}</div>
      <div class="bajada" id="bajada-cierre" style="top: 1260px; color: #3C3C4A">{e(cierre.get('bajada', ''))}</div>
      <img id="logo-cierre" src="assets/logo.png">
      {anillos}
    </div>
    {escena_contacto}
    <div id="transiciones" class="clip escena" data-start="0" data-duration="{total}" data-track-index="9"
         style="z-index:9" data-layout-allow-overlap data-layout-allow-occlusion>
      <div id="barrido" class="transicion"></div>
      <div id="bombillo" class="transicion"><img src="assets/icono-transicion.png"></div>
      <div id="iris" class="transicion"></div>
      {'<div id="barrido-2" class="transicion"></div>' if contacto else ''}
    </div>"""
    n = len(palabras)
    contacto_js = ''
    if contacto:
        # Transición 5, inundación de color: el acento sube y se queda como fondo del contacto.
        contacto_js = f"""
      tl.fromTo('#barrido-2', {{ scaleY: 0, transformOrigin: '50% 100%' }}, {{ scaleY: 1, duration: 0.4,
                ease: 'power2.inOut' }}, {t5 - 0.4});
      tl.to('#barrido-2', {{ opacity: 0, duration: 0.01 }}, {t5 + 0.05});
      document.querySelectorAll('.aro-c, #circuito-c').forEach((el) => {{
        const largo = el.getTotalLength();
        el.style.strokeDasharray = largo;
        el.style.strokeDashoffset = largo;
      }});
      tl.fromTo('#trama-contacto', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {t5});
      tl.to('.aro-c', {{ strokeDashoffset: 0, duration: 0.8, ease: 'power2.inOut', stagger: 0.08 }}, {t5 + 0.05});
      tl.fromTo('.p-contacto', {{ opacity: 0, filter: 'blur(6px)' }}, {{ opacity: 1, filter: 'blur(0px)', duration: 0.15,
                stagger: 0.06 }}, {t5 + 0.15});
      tl.fromTo('.destacado', {{ scale: 1.35 }}, {{ scale: 1, duration: 0.5, ease: 'back.out(3)' }}, {t5 + 0.5});
      tl.fromTo('.tarjeta-c', {{ x: -70, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: 'expo.out',
                stagger: 0.13 }}, {t5 + 0.7});
      tl.fromTo('.tarjeta-c .circulo', {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: 0, duration: 0.8,
                ease: 'elastic.out(1, 0.55)', stagger: 0.13 }}, {t5 + 0.8});
      tl.fromTo(['#seneca', '#seneca-guino'], {{ y: 720 }}, {{ y: 0, duration: 0.7, ease: 'back.out(1.6)' }}, {t5 + 1.1});
      tl.to('#circuito-c', {{ strokeDashoffset: 0, duration: 0.6, ease: 'power2.inOut' }}, {t5 + 1.3});
      tl.fromTo('.nodo-c', {{ scale: 0, transformOrigin: '50% 50%' }}, {{ scale: 1, duration: 0.35, ease: 'back.out(2)',
                stagger: 0.08 }}, {t5 + 1.8});
      tl.fromTo('#logo-contacto', {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.5,
                ease: 'back.out(2)' }}, {t5 + 1.5});
      tl.fromTo('#firma', {{ x: -20, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: 'expo.out' }}, {t5 + 1.65});
      // Séneca guiña dos veces mientras saluda.
      tl.set('#seneca-guino', {{ opacity: 1 }}, {t5 + 2.5});
      tl.set('#seneca-guino', {{ opacity: 0 }}, {t5 + 2.7});
      tl.set('#seneca-guino', {{ opacity: 1 }}, {t5 + 3.6});
      tl.set('#seneca-guino', {{ opacity: 0 }}, {t5 + 3.8});"""
    guion = f"""
      const tl = gsap.timeline({{ paused: true }});
      // Gancho: la imagen ya está en el cuadro 0; el título llega palabra por palabra.
      tl.fromTo('#chip-gancho', {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: 'power4.out' }}, 0.1);
      tl.fromTo('.p-gancho', {{ opacity: 0, filter: 'blur(8px)' }}, {{ opacity: 1, filter: 'blur(0px)', duration: 0.16,
                ease: 'power2.out', stagger: 0.08 }}, 0.25);
      // Transición 1, inundación de color: el bloque del acento sube y barre hacia la revelación.
      tl.fromTo('#barrido', {{ scaleY: 0, transformOrigin: '50% 100%' }}, {{ scaleY: 1, duration: 0.35,
                ease: 'power2.in' }}, {t1 - 0.35});
      tl.to('#barrido', {{ scaleY: 0, transformOrigin: '50% 0%', duration: 0.45, ease: 'power2.out' }}, {t1});
      // Revelación.
      tl.fromTo('#bloque-revela', {{ x: 120, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.7, ease: 'expo.out' }}, {t1 + 0.15});
      tl.fromTo('.p-revela', {{ opacity: 0, filter: 'blur(6px)' }}, {{ opacity: 1, filter: 'blur(0px)', duration: 0.15,
                stagger: 0.07 }}, {t1 + 0.45});
      tl.fromTo('#bajada-revela', {{ opacity: 0, filter: 'blur(8px)' }}, {{ opacity: 1, filter: 'blur(0px)',
                duration: 0.2 }}, {t1 + 0.55});
      tl.fromTo('#s-revela .anillo', {{ scale: 0, transformOrigin: '0% 100%' }}, {{ scale: 1, duration: 0.7,
                ease: 'expo.out', stagger: 0.08 }}, {t1 + 0.3});
      // Transición 2, zoom a través del bombillo: crece hasta ser el fondo amarillo de los conceptos.
      tl.fromTo('#bombillo', {{ scale: 0, opacity: 1 }}, {{ scale: 1, duration: 0.3, ease: 'back.out(2)' }}, {t2 - 0.6});
      tl.to('#bombillo', {{ scale: 14, duration: 0.35, ease: 'power3.in' }}, {t2 - 0.3});
      tl.to('#bombillo', {{ opacity: 0, duration: 0.01 }}, {t2 + 0.05});
      // Conceptos: una palabra gira como tragamonedas.
      tl.fromTo('#rueda-tira', {{ y: 0 }}, {{ y: 0, duration: 0.01 }}, {t2});
      {''.join(f"tl.to('#rueda-tira', {{ y: {-130 * k}, duration: 0.12, ease: 'power2.inOut' }}, {t2 + 0.25 + k * 0.62:.2f});" for k in range(1, n))}
      tl.fromTo('#iconos .ic', {{ scale: 0, rotation: -25 }}, {{ scale: 1, rotation: 0, duration: 0.8,
                ease: 'elastic.out(1, 0.55)', stagger: 0.1 }}, {t2 + 0.2});
      // Transición 3, barrido rápido: la escena amarilla se va hacia arriba con desenfoque.
      tl.to('#s-conceptos > *', {{ y: -500, filter: 'blur(14px)', opacity: 0, duration: 0.25, ease: 'power3.in' }},
            {t3 - 0.25});
      // Momento.
      tl.fromTo('.p-momento', {{ opacity: 0, filter: 'blur(6px)' }}, {{ opacity: 1, filter: 'blur(0px)', duration: 0.15,
                stagger: 0.07 }}, {t3 + 0.3});
      // Transición 4, iris desde el punto amarillo hacia el cierre.
      tl.fromTo('#iris', {{ clipPath: 'circle(0px at {96 + caja_foto[0] - 6}px 242px)' }},
                {{ clipPath: 'circle(2300px at {96 + caja_foto[0] - 6}px 242px)', duration: 0.45, ease: 'power2.in' }},
                {t4 - 0.45});
      tl.to('#iris', {{ opacity: 0, duration: 0.3, ease: 'power2.out' }}, {t4});
      // Cierre: queda quieto al menos dos segundos.
      tl.fromTo('.p-cierre', {{ opacity: 0, filter: 'blur(6px)' }}, {{ opacity: 1, filter: 'blur(0px)', duration: 0.15,
                stagger: 0.08 }}, {t4 + 0.3});
      tl.fromTo('#bajada-cierre', {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {t4 + 0.6});
      tl.fromTo('#logo-cierre', {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: 'expo.out' }}, {t4 + 0.7});
      {contacto_js}
      window.__timelines['main'] = tl;
    """
    pagina = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={REEL_ANCHO}, height={REEL_ALTO}" />
    <script src="assets/gsap.min.js"></script>
    <style>{css}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}"
         data-width="{REEL_ANCHO}" data-height="{REEL_ALTO}">
      {cuerpo}
    </div>
    <script>{guion}</script>
  </body>
</html>
"""
    (carpeta / 'index.html').write_text(pagina, encoding='utf-8')
    (carpeta / 'hyperframes.json').write_text(json.dumps({'paths': {'assets': 'assets'}}), encoding='utf-8')
    return total
