import os
import subprocess
import sys

import pytest

from conftest import SKILL


@pytest.mark.parametrize('nombre', ['build_cronica', 'build_historia', 'build_carrusel', 'build_convocatoria', 'build_estilos'])
def test_ejemplo_sin_avisos(nombre):
    entorno = {**os.environ, 'PYTHONPATH': str(SKILL / 'motor')}
    entorno.pop('PYTHONIOENCODING', None)
    r = subprocess.run([sys.executable, str(SKILL / 'ejemplos' / f'{nombre}.py')], capture_output=True,
                       text=True, encoding='utf-8', env=entorno)
    assert r.returncode == 0, r.stdout + r.stderr
    assert '✅ sin avisos' in r.stdout
