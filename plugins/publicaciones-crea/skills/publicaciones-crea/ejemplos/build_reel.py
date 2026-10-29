"""Galería: un reel vertical con la estructura aprobada y el contacto del laboratorio al final.

    <PYTHON> build_reel.py [--render]

Escribe el proyecto HyperFrames en salida/reel/proyecto; con --render (necesita Node: ANIMADO=si en el
paso 0) lo renderiza a salida/reel/reel.mp4. En un encargo real, gancho y momento son videos del taller;
aquí, como no hay video de demostración, se arma uno con un barrido de luz sobre la foto (la foto no se
mueve). Ver referencia/galeria.md.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from crea_publicaciones import O, contacto_reel, mp4, movimiento

AQUI = Path(__file__).resolve().parent
FOTOS = AQUI / 'fotos'
SALIDA = AQUI / 'salida' / 'reel'


def video_demo(foto, salida, segundos=5, fps=30):
    """Un clip vertical de la foto quieta con una franja de luz que la cruza: el lugar de un video real."""
    base = Image.open(foto).convert('RGB').resize((720, 1280))
    n = int(segundos * fps)

    def cuadro(i):
        luz = Image.new('L', base.size, 0)
        x = -400 + (base.width + 800) * i / n
        ImageDraw.Draw(luz).polygon([(x, 0), (x + 180, 0), (x - 220, base.height), (x - 400, base.height)], fill=90)
        return Image.composite(Image.new('RGB', base.size, (255, 244, 214)), base,
                               luz.filter(ImageFilter.GaussianBlur(60)))
    return mp4((cuadro(i) for i in range(n)), salida, fps)


if __name__ == '__main__':
    SALIDA.mkdir(parents=True, exist_ok=True)
    video = video_demo(FOTOS / 'foto-demo2.jpg', SALIDA / 'video-demo.mp4')
    movimiento.reel(
        SALIDA / 'proyecto', acento=O, cache=AQUI / 'salida' / '.cache',
        gancho=dict(video=video, titulo='¿Cuánto peso aguanta?', chip='Taller de estructuras'),
        revelacion=dict(foto=FOTOS / 'foto-demo.jpg', titulo='Un puente de palitos',
                        bajada='Cada equipo cargó su cercha.'),      # corta: la escena dura 3 s
        conceptos=dict(antes='Hablamos de', palabras=['compresión', 'tensión', 'triángulos', 'cargas'],
                       iconos=['truss', 'weight', 'target']),
        momento=dict(video=video, titulo='Triángulos, no cuadrados', desde=1.0),
        cierre=dict(foto=FOTOS / 'foto-demo.jpg', titulo='¡Gracias por venir!',
                    bajada='Nos vemos en el próximo reto de estructuras.', foco=0.7),
        contacto=contacto_reel(),     # siempre: un reel se ve fuera del perfil
    )
    if '--render' in sys.argv:
        final = movimiento.render(SALIDA / 'proyecto', SALIDA / 'reel.mp4')
        movimiento.portada(final, SALIDA / 'reel-final.jpg')
        print('->', final)
    else:
        print('->', SALIDA / 'proyecto', '(con --render sale el MP4)')
