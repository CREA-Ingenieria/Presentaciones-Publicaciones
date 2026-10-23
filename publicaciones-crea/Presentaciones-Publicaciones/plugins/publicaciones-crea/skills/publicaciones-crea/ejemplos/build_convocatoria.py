"""Convocatoria de ejemplo. Regenerar: <PYTHON> build_convocatoria.py"""
from pathlib import Path

from crea_publicaciones import *  # noqa: F403

AQUI = Path(__file__).resolve().parent

pieza = convocatoria(
    pregunta='¿Te interesa la robótica y la electrónica?',
    titulo='Construye tu propio robot',
    puntos=['Conceptos básicos de electrónica y física',
            'Diseño de circuitos y componentes',
            'Ensamble sobre estructuras impresas en 3D'],
    contacto='crea@uniandes.edu.co',
    acento=B,          # robótica -> azul
)

texto = caption(
    '🔧✨ ¿Te interesa la robótica y la electrónica?',
    'Abrimos inscripciones para nuestro taller Mothbot, donde construirás tu propio robot.',
    '📚 Introducción: conceptos básicos de electrónica y física\n'
    '🎨 Diseño: circuitos, resistencias, transistores y LEDs\n'
    '🔩 Ensamble: estructuras impresas en 3D',
    'No necesitas experiencia previa. ¡Escríbenos a crea@uniandes.edu.co y reserva tu cupo! 🤖💡',
    hashtags=['#LaboratorioCREA', '#Mothbot', '#EducaciónSTEAM', '#STEM', '#Ingeniería'],
)

raise SystemExit(entregar(AQUI / 'salida' / 'convocatoria', pieza, texto).codigo)
