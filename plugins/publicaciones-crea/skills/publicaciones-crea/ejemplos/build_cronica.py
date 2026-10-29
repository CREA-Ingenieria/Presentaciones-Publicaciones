"""Crónica de taller de ejemplo. Regenerar: <PYTHON> build_cronica.py"""
from pathlib import Path

from crea_publicaciones import *  # noqa: F403

AQUI = Path(__file__).resolve().parent

pieza = cronica(
    foto=AQUI / 'fotos' / 'foto-demo.jpg',
    categoria='Taller',
    titulo='Ingenieras por un día',
    bajada='Analizaron muestras del Eje Ambiental y construyeron sus propios filtros.',
    aliado='Liceo Femenino de Cundinamarca',
    acento=T,
    iconos=['flask', 'recycle'],
)

texto = caption(
    'Así fue la visita del Liceo Femenino de Cundinamarca a nuestro taller AguaLab 💧',
    'Trabajaron con muestras reales del Eje Ambiental: midieron pH, turbidez y conductividad, y con esos '
    'datos diseñaron y probaron sus propios filtros de agua.',
    '¿Quieres traer a tu colegio? Escríbenos por mensaje directo.',
    hashtags=['#LaboratorioCREA', '#AguaLab', '#EducaciónSTEAM', '#MujeresEnSTEAM', '#uniandesciam'],
)

raise SystemExit(entregar(AQUI / 'salida' / 'cronica', pieza, texto).codigo)
