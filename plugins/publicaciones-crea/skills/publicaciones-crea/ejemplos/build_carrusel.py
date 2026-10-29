"""Carrusel de ejemplo: la lámina 2 escribe una línea de código en el MP4. Regenerar: <PYTHON> build_carrusel.py"""
from pathlib import Path

from crea_publicaciones import *  # noqa: F403

AQUI = Path(__file__).resolve().parent
FOTOS = AQUI / 'fotos'

# La lámina 1 es la que se ve en la cuadrícula del perfil: lleva el título
# principal, la foto más legible en miniatura y ninguna animación.
laminas = [
    lamina(FOTOS / 'foto-demo.jpg', chip='Taller', iconos=['truss', 'weight', 'recycle'],
           titulo='Dos vigas que no se balanceen',
           bajada='Material reciclado y una sola condición: que se sostengan solas.'),
    lamina(FOTOS / 'foto-demo2.jpg', chip='Reto', titulo='Y después, a probarlas',
           bajada='Una estructura no se sostiene por ser alta, sino por cómo reparte el peso.',
           codigo='repetir: preguntar → probar → mejorar'),
]

texto = caption(
    'Dos vigas, material reciclado y una sola condición: que se sostengan solas 🏗️',
    'En nuestro taller de estructuras cada equipo diseñó su propuesta, la probó y la volvió a armar. '
    'Hablamos de cargas, puntos de apoyo y centro de masa.',
    'Cada caída fue una pista para el siguiente intento.',
    hashtags=['#LaboratorioCREA', '#EducaciónSTEAM', '#Ingeniería', '#STEM', '#uniandesciam'],
)

raise SystemExit(entregar(AQUI / 'salida' / 'carrusel', laminas, texto).codigo)
