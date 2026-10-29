"""Historia de ejemplo, con Séneca parpadeando en el MP4. Regenerar: <PYTHON> build_historia.py"""
from pathlib import Path

from crea_publicaciones import *  # noqa: F403

AQUI = Path(__file__).resolve().parent

pieza = historia(
    foto=AQUI / 'fotos' / 'foto-demo.jpg',
    categoria='Taller',
    titulo='Ingenieras por un día',
    aliado='Liceo Femenino de Cundinamarca',
    acento=T,
    animar=True,
)

# Las historias no llevan caption: el texto vive en la pieza.
raise SystemExit(entregar(AQUI / 'salida' / 'historia', pieza).codigo)
