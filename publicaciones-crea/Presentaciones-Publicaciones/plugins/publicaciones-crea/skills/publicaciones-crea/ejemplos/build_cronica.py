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
)

texto = caption(
    '¡Las estudiantes del Liceo Femenino de Cundinamarca se convirtieron en Ingenieras Ambientales '
    'por un día! 👩‍🔬💧',
    'Recibimos al Liceo en nuestro taller AguaLab, donde trabajaron con muestras reales del Eje Ambiental.',
    'Midieron parámetros fisicoquímicos como pH, turbidez y conductividad, y con lo que encontraron '
    'diseñaron y probaron sus propios filtros de agua. 🧪🔬',
    '¡El futuro de nuestro planeta está en excelentes manos! 🌎✨',
    hashtags=['#LaboratorioCREA', '#AguaLab', '#EducaciónSTEAM', '#MujeresEnSTEAM', '#uniandesciam'],
)

raise SystemExit(entregar(AQUI / 'salida' / 'cronica', pieza, texto).codigo)
