"""Entrega: guarda las piezas, exporta los MP4, escribe el caption y revisa todo junto.

`revision/` lleva lo que hay que mirar antes de entregar: cómo queda cada pieza en la
cuadrícula del perfil y, en las historias, qué tapa la interfaz de Instagram.
"""
import sys
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw

from .animacion import mp4
from .base import POST, STORY, UI_ABAJO, UI_ARRIBA, UI_DERECHA, ErrorCREA, Pieza
from .caption import revisar_caption

MAX_LAMINAS = 20       # lo que Instagram acepta en un carrusel


@dataclass
class Resultado:
    codigo: int                        # 0 listo, 1 con avisos, 2 con errores
    archivos: list = field(default_factory=list)
    avisos: list = field(default_factory=list)
    errores: list = field(default_factory=list)


def _nombrar(piezas):
    laminas = [p for p in piezas if p.tipo == 'lamina']
    for i, p in enumerate(laminas, 1):
        p.nombre = p.nombre or f'carrusel-{i}'
        # Solo la primera lámina se ve en la cuadrícula del perfil.
        p.en_perfil = i == 1
    for i, p in enumerate(piezas, 1):
        p.nombre = p.nombre or f'{p.tipo}-{i}'
    nombres = [p.nombre for p in piezas]
    repetidos = {n for n in nombres if nombres.count(n) > 1}
    if repetidos:
        raise ErrorCREA(f'Dos piezas con el mismo nombre: {", ".join(sorted(repetidos))}. Usa nombre=...')


def _reglas_de_conjunto(piezas):
    errores, avisos = [], []
    laminas = [p for p in piezas if p.tipo == 'lamina']
    if len(laminas) > MAX_LAMINAS:
        errores.append(f'el carrusel tiene {len(laminas)} láminas; Instagram acepta {MAX_LAMINAS}')
    if len(laminas) == 1:
        avisos.append('un carrusel de una sola lámina: usa cronica() para una publicación suelta')
    if laminas and laminas[0].cuadros is not None:
        avisos.append(f'{laminas[0].nombre}: la primera lámina va estática; si se anima, el grid la '
                      'convierte en reel. Pon la animación en otra lámina')
    feed = [p for p in piezas if p.formato == POST and p.tipo != 'lamina']
    for p in feed:
        if p.cuadros is not None:
            avisos.append(f'{p.nombre}: una publicación animada sube como reel, no como foto del grid. '
                          'Si debe verse estática en el perfil, va como lámina de un carrusel')
    return errores, avisos


def _vista_perfil(p, ruta):
    p.im.crop(p.cuadro_perfil()).convert('RGB').resize((360, 360), Image.LANCZOS).save(ruta, quality=90)


def _vista_zonas(p, ruta):
    # Las franjas que tapa la interfaz, en rojo translúcido.
    capa = Image.new('RGBA', p.im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    rojo = (220, 38, 38, 110)
    d.rectangle([0, 0, p.w, UI_ARRIBA], fill=rojo)
    d.rectangle([0, p.h - UI_ABAJO, p.w, p.h], fill=rojo)
    d.rectangle([p.w - UI_DERECHA, UI_ARRIBA, p.w, p.h - UI_ABAJO], fill=rojo)
    im = p.im.copy()
    im.alpha_composite(capa)
    im.convert('RGB').resize((540, 960), Image.LANCZOS).save(ruta, quality=90)


def entregar(carpeta, piezas, caption=None, final=False):
    """Guarda JPG (y MP4 si hay animación), caption.txt y revision/; imprime el informe.

    Con `final=True`, cualquier dato `{validar:…}` que quede es un error y no un aviso.
    """
    carpeta = Path(carpeta)
    piezas = [piezas] if isinstance(piezas, Pieza) else list(piezas)
    if not piezas:
        raise ErrorCREA('No hay piezas que entregar')
    _nombrar(piezas)
    revision = carpeta / 'revision'
    revision.mkdir(parents=True, exist_ok=True)
    for viejo in revision.glob('*.jpg'):      # que no quede la vista de una versión anterior
        viejo.unlink()
    errores, avisos = _reglas_de_conjunto(piezas)
    archivos = []

    for p in piezas:
        archivos.append(p.guardar(carpeta / f'{p.nombre}.jpg'))
        if p.cuadros is not None:
            archivos.append(mp4(p.cuadros, carpeta / f'{p.nombre}.mp4', p.fps))
        if p.en_perfil:
            _vista_perfil(p, revision / f'{p.nombre}-perfil.jpg')
        if p.formato == STORY:
            _vista_zonas(p, revision / f'{p.nombre}-zonas.jpg')
        avisos += [f'{p.nombre}: {a}' for a in p.revisar()]

    if caption is None:
        # Las historias no llevan caption; todo lo que va al feed, sí.
        if any(p.formato != STORY for p in piezas):
            avisos.append('sin caption: la publicación se entrega con su caption, listo para copiar')
    else:
        ruta = carpeta / 'caption.txt'
        ruta.write_text(caption.strip() + '\n', encoding='utf-8')
        archivos.append(ruta)
        e, a = revisar_caption(caption)
        errores += [f'caption: {x}' for x in e]
        avisos += [f'caption: {x}' for x in a]

    if final:
        sin_validar = [a for a in avisos if 'sin validar' in a]
        errores += sin_validar
        avisos = [a for a in avisos if a not in sin_validar]

    codigo = 2 if errores else 1 if avisos else 0
    r = Resultado(codigo, archivos, avisos, errores)
    _informe(r, carpeta)
    return r


def _informe(r, carpeta):
    # La consola de Windows no siempre es UTF-8 y el informe lleva ✅ y ⚠️.
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    for a in r.archivos:
        print(f'-> {a}')
    print(f'-> {carpeta / "revision"} (mírala antes de entregar)')
    for e in r.errores:
        print(f'❌ {e}')
    for a in r.avisos:
        print(f'⚠️ {a}')
    if r.codigo == 0:
        print('✅ sin avisos')
