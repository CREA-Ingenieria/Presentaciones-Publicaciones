"""Galería: el mismo carrusel en los tres estilos, cada uno estático y animado.

    <PYTHON> build_estilos.py [marco] [recortes] [arcade] [--animado]

Sin estilos, hace los tres. La versión estática sale en salida/estilos/<estilo>/estatico; con --animado
(necesita Node: ANIMADO=si en el paso 0), también la animada en salida/estilos/<estilo>/animado.
Es el patrón aprobado para un encargo con variantes: ver referencia/galeria.md.
"""
import sys
from pathlib import Path

from crea_publicaciones import O, caption, entregar, lamina, movimiento

AQUI = Path(__file__).resolve().parent
FOTOS = AQUI / 'fotos'
ESTILOS = ('marco', 'recortes', 'arcade')

# Los datos son los mismos en los tres estilos; un estilo, un acento para todo el carrusel.
LAMINAS = [
    dict(foto=FOTOS / 'foto-demo.jpg', chip='Taller', iconos=['truss', 'weight', 'recycle'],
         titulo='Un puente de palitos', bajada='Cada equipo diseñó una cercha y la cargó hasta que cedió.',
         sticker='creabot'),
    dict(foto=FOTOS / 'foto-demo2.jpg', chip='Reto', iconos=['truss', 'target'], foco=0.55, ajuste='contener',
         titulo='Triángulos, no cuadrados', bajada='El triángulo no se deforma: por eso sostiene más peso.'),
    dict(foto=FOTOS / 'foto-demo.jpg', chip='Gracias', iconos=['users', 'school'], foco=0.7,
         titulo='¡Gracias por venir!', bajada='Nos vemos en el próximo reto de estructuras.', sticker='seneca'),
]

TEXTO = caption(
    'Palitos de madera, pegante y una pregunta: ¿cuánto peso aguanta un puente que cabe en una mesa?',
    'En nuestro taller de estructuras cada equipo diseñó su cercha, la cargó y vio por dónde cedía. '
    'Hablamos de compresión, tensión y de por qué casi todos los puentes se arman con triángulos.',
    'El que más aguantó no fue el más alto.',
    hashtags=['#LaboratorioCREA', '#EducaciónSTEAM', '#Ingeniería', '#STEM', '#uniandesciam'],
)


def datos(estilo):
    """Lo propio de cada estilo: el sticker solo en recortes; en arcade, el número de nivel."""
    salida = []
    for i, d in enumerate(LAMINAS, 1):
        d = dict(d)
        if estilo != 'recortes':
            d.pop('sticker', None)
            d.pop('ajuste', None)       # 'contener' es para la copia horizontal del collage
        if estilo == 'arcade':
            d['nivel'] = i
        salida.append(d)
    return salida


def estatico(estilo):
    laminas = [lamina(d.pop('foto'), acento=O, estilo=estilo, **d) for d in datos(estilo)]
    return entregar(AQUI / 'salida' / 'estilos' / estilo / 'estatico', laminas, TEXTO).codigo


def animado(estilo):
    salida = AQUI / 'salida' / 'estilos' / estilo / 'animado'
    movimiento.carrusel(salida, datos(estilo), acento=O, estilo=estilo, cache=AQUI / 'salida' / '.cache')
    return 0


if __name__ == '__main__':
    args = sys.argv[1:]
    estilos = [a for a in args if a in ESTILOS] or list(ESTILOS)
    codigo = 0
    for estilo in estilos:
        codigo = max(codigo, estatico(estilo))
        if '--animado' in args:
            codigo = max(codigo, animado(estilo))
    raise SystemExit(codigo)
