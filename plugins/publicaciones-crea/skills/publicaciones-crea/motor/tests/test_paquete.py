import json
import re
from pathlib import Path

import crea_publicaciones
from conftest import SKILL

PLUGIN_JSON = SKILL.parents[1] / '.claude-plugin' / 'plugin.json'
PYPROJECT = SKILL / 'motor' / 'pyproject.toml'
R = SKILL / 'motor' / 'crea_publicaciones' / 'recursos'


def test_recursos_viven_dentro_del_paquete():
    from crea_publicaciones import base
    assert base.RECURSOS == Path(base.__file__).resolve().parent / 'recursos'
    assert not (SKILL / 'recursos').exists()
    for f in ('fuentes/Montserrat-Regular.ttf', 'fuentes/Montserrat-Medium.ttf', 'fuentes/Montserrat-SemiBold.ttf',
              'fuentes/Montserrat-Bold.ttf', 'fuentes/Montserrat-ExtraBold.ttf', 'fuentes/OFL.txt',
              'marca/crea_logo.png', 'marca/patron_doodles.png', 'mascota/seneca_saludo.png',
              'mascota/seneca_guino.png'):
        assert (R / f).is_file(), f


def test_versiones_coinciden():
    v_plugin = json.loads(PLUGIN_JSON.read_text(encoding='utf-8'))['version']
    v_py = re.search(r'^version = "([^"]+)"', PYPROJECT.read_text(encoding='utf-8'), re.M).group(1)
    assert v_plugin == v_py == crea_publicaciones.__version__


def test_changelog_tiene_la_version():
    v = json.loads(PLUGIN_JSON.read_text(encoding='utf-8'))['version']
    changelog = (SKILL.parents[3] / 'CHANGELOG.md').read_text(encoding='utf-8')
    assert f'## [{v}]' in changelog


def test_ejemplos_sin_personas():
    # Las fotos de estudiantes no viajan dentro del plugin: solo las de objetos del taller.
    fotos = sorted(p.name for p in (SKILL / 'ejemplos' / 'fotos').iterdir())
    assert fotos == ['foto-demo.jpg', 'foto-demo2.jpg']
