import inspect
import re

import crea_publicaciones
from conftest import SKILL

PUBLICOS = ['cronica', 'historia', 'lamina', 'convocatoria', 'animar', 'caption', 'revisar_caption', 'entregar']


def test_piezas_md_documenta_las_firmas():
    doc = (SKILL / 'referencia' / 'piezas.md').read_text(encoding='utf-8')
    for nombre in PUBLICOS:
        firma = f'{nombre}{inspect.signature(getattr(crea_publicaciones, nombre))}'
        assert firma in doc, f'falta o está desactualizada: {firma}'


def test_skill_md_enlaza_referencias():
    skill = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    assert skill.startswith('---\nname: publicaciones-crea\n')
    for f in (SKILL / 'referencia').glob('*.md'):
        assert f'referencia/{f.name}' in skill, f.name


def test_skill_md_paso_cero_y_modos():
    skill = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    for texto in ('${CLAUDE_PLUGIN_ROOT}/skills/publicaciones-crea/entorno/revisar.py', '${CLAUDE_PLUGIN_DATA}',
                  'PYTHON=', 'MODO=vault', 'MODO=autonomo', 'winget install Python.Python.3.12',
                  'sea 3.10 o más', 'final=True', '-m crea_publicaciones.caption'):
        assert texto in skill, texto


def test_scripts_no_buscan_el_motor_a_mano():
    textos = {f.name: f.read_text(encoding='utf-8') for f in (SKILL / 'ejemplos').glob('*.py')}
    textos['SKILL.md'] = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    for nombre, texto in textos.items():
        assert "/ 'motor'" not in texto and 'sys.path' not in texto, nombre


def test_piezas_md_lista_los_iconos():
    from crea_publicaciones.marco import claves_iconos
    doc = (SKILL / 'referencia' / 'piezas.md').read_text(encoding='utf-8')
    for clave in claves_iconos():
        assert f'`{clave}`' in doc, clave


def test_movimiento_md_documenta_las_firmas():
    from crea_publicaciones import movimiento
    doc = (SKILL / 'referencia' / 'movimiento.md').read_text(encoding='utf-8')
    for nombre in ('carrusel', 'proyecto', 'proyecto_capas', 'reel'):
        firma = f'{nombre}{inspect.signature(getattr(movimiento, nombre))}'
        assert firma in doc, f'falta o está desactualizada: {firma}'


def test_estilos_md_cubre_cada_estilo():
    from crea_publicaciones.piezas import ESTILOS
    doc = (SKILL / 'referencia' / 'estilos.md').read_text(encoding='utf-8')
    skill = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    for estilo in ESTILOS:
        assert f'## {estilo.capitalize()}' in doc and f'`{estilo}`' in skill, estilo


def test_skill_md_cuenta_las_decisiones_y_el_paso_cero_animado():
    skill = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    for texto in ('ANIMADO=no', 'Mapa de decisiones', 'contacto_reel()', 'por_validar()', 'La foto no se mueve'):
        assert texto in skill, texto


def test_galeria_enlaza_ejemplos_que_existen():
    doc = (SKILL / 'referencia' / 'galeria.md').read_text(encoding='utf-8')
    for ruta in re.findall(r'`(ejemplos/[^`]+)`', doc):
        assert (SKILL / ruta).exists(), ruta
