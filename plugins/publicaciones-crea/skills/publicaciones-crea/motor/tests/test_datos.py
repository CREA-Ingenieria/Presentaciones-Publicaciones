import pytest

from crea_publicaciones import B, ErrorCREA, contacto_reel, por_validar, taller
from crea_publicaciones.datos import crea
from crea_publicaciones.marco import claves_iconos
from conftest import SKILL


def test_taller_por_nombre_sin_importar_mayusculas():
    t = taller('mothbot')
    assert t['nombre'] == 'Mothbot' and t['acento'] == B and '#Mothbot' in t['hashtags']


def test_taller_desconocido_pide_preguntar():
    with pytest.raises(ErrorCREA, match='Pregunta'):
        taller('Robótica submarina')


def test_iconos_del_set_existen():
    claves = set(claves_iconos())
    for t in crea()['talleres']:
        assert set(t['iconos']) <= claves, t['nombre']
    for c in crea()['contacto']:
        assert c['icono'] == '@' or c['icono'] in claves, c['valor']


def test_todo_dato_tiene_estado_y_fuente():
    datos = crea()
    for d in (datos['biografia'], *datos['contacto'], *datos['talleres'], *datos['aliados']):
        assert d['estado'] in ('confirmado', 'por validar')
    for d in (*datos['contacto'], *datos['talleres']):
        assert d['fuente']


def test_contacto_reel_deja_fuera_lo_por_validar():
    c = contacto_reel()
    valores = [v for _, v in c['lineas']]
    assert '@crea_uniandes' in valores and 'crea@uniandes.edu.co' not in valores
    assert c['titulo'].startswith('¡Trae a tu colegio') and c['destacar'] == 'colegio'
    assert 'crea@uniandes.edu.co' in [v for _, v in contacto_reel(incluir_por_validar=True)['lineas']]


def test_por_validar_lista_lo_pendiente():
    pendiente = ' '.join(por_validar())
    assert 'crea@uniandes.edu.co' in pendiente and 'SLB' in pendiente
    assert 'Mothbot' not in pendiente


def test_crea_md_explica_todo_el_set():
    doc = (SKILL / 'referencia' / 'crea.md').read_text(encoding='utf-8')
    datos = crea()
    for valor in ([t['nombre'] for t in datos['talleres']] + [c['valor'] for c in datos['contacto']]
                  + [a['nombre'] for a in datos['aliados']] + datos['hashtags']['habituales']
                  + [datos['biografia']['valor']]):
        assert valor in doc, valor
