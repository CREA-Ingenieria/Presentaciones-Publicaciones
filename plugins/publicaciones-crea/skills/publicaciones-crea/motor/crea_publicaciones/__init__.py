"""Motor de la skill publicaciones-crea. Los scripts de cada pieza hacen `from crea_publicaciones import *`."""
__version__ = '1.3.0'
from .animacion import animar, mp4  # noqa: F401
from .base import (BODY, CUAD, CUERPO, DARK, ETIQ, MARGEN, POST, SOFT, STORY, SUB, TITULO, WHITE, B,  # noqa: F401
                   ErrorCREA, M, O, Pieza, T, Y)
from .caption import caption, revisar_caption  # noqa: F401
from .datos import contacto_reel, por_validar, taller  # noqa: F401
from .entrega import entregar  # noqa: F401
from .piezas import convocatoria, cronica, historia, lamina  # noqa: F401
