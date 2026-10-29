"""El set precargado de CREA: talleres, contacto, hashtags y aliados, con su estado de validación.

La fuente es `recursos/crea.json`; `referencia/crea.md` lo explica. Un dato 'por validar' no se publica
sin preguntar: las funciones que arman piezas lo dejan fuera salvo que se pida lo contrario.
"""
import json
from functools import lru_cache

from .base import RECURSOS, B, ErrorCREA, M, O, T

ACENTOS = {'T': T, 'M': M, 'O': O, 'B': B}


@lru_cache(maxsize=1)
def crea():
    return json.loads((RECURSOS / 'crea.json').read_text(encoding='utf-8'))


def taller(nombre):
    """Los datos de un taller por su nombre propio (sin importar mayúsculas)."""
    for t in crea()['talleres']:
        if t['nombre'].lower() == nombre.lower():
            return dict(t, acento=ACENTOS.get(t['acento']) if t['acento'] else None)
    nombres = ', '.join(t['nombre'] for t in crea()['talleres'])
    raise ErrorCREA(f'El taller "{nombre}" no está en el set de CREA ({nombres}). Pregunta su nombre propio '
                    'exacto y, si es nuevo, agrégalo a recursos/crea.json')


def contacto_reel(destacar='colegio', incluir_por_validar=False):
    """La escena de contacto del reel con los datos del set: la biografía como titular y cada contacto
    con su ícono. Sin `incluir_por_validar`, lo no confirmado se queda fuera."""
    datos = crea()
    lineas = [(c['icono'], c['valor']) for c in datos['contacto']
              if c['estado'] == 'confirmado' or incluir_por_validar]
    return {'titulo': datos['biografia']['valor'], 'destacar': destacar, 'lineas': lineas}


def por_validar():
    """Todo lo que el set tiene sin confirmar, para preguntarlo en una sola tanda."""
    datos = crea()
    salida = [f"contacto: {c['valor']} ({c['fuente']})" for c in datos['contacto'] if c['estado'] != 'confirmado']
    salida += [f"taller: {t['nombre']} ({t['fuente']})" for t in datos['talleres'] if t['estado'] != 'confirmado']
    salida += [f"aliado: {a['nombre']} ({a['nota']})" for a in datos['aliados'] if a['estado'] != 'confirmado']
    return salida
