import os
import subprocess
import sys
from pathlib import Path

import pytest

REVISAR = Path(__file__).resolve().parents[1] / 'revisar.py'

pytestmark = [
    pytest.mark.instalacion,
    pytest.mark.skipif(os.environ.get('CREA_PRUEBA_INSTALACION') != '1',
                       reason='define CREA_PRUEBA_INSTALACION=1 para correrla'),
]


def test_revisar_instala_y_el_motor_funciona_fuera_del_repo(tmp_path):
    datos = tmp_path / 'datos con espacio ñ'
    trabajo = tmp_path / 'trabajo'
    trabajo.mkdir()
    r = subprocess.run([sys.executable, str(REVISAR), '--datos', str(datos), '--dir', str(trabajo)],
                       capture_output=True, text=True, encoding='utf-8', cwd=trabajo)
    assert r.returncode in (0, 1), r.stdout + r.stderr
    assert 'Render de prueba: JPG y MP4' in r.stdout, r.stdout
    lineas = r.stdout.strip().splitlines()
    assert lineas[-1] == 'MODO=autonomo'
    py = lineas[-2].removeprefix('PYTHON=')
    codigo = ("from crea_publicaciones import *\n"
              "p = convocatoria('Construye tu robot', ['Uno'], 'crea@uniandes.edu.co')\n"
              "r = entregar('salida', p, caption('Hola 🤖', hashtags=['#LaboratorioCREA']))\n"
              "from crea_publicaciones import base; assert 'site-packages' in str(base.RECURSOS)")
    r2 = subprocess.run([py, '-c', codigo], capture_output=True, text=True, cwd=trabajo)
    assert r2.returncode == 0, r2.stderr
    assert (trabajo / 'salida' / 'convocatoria.jpg').is_file()
    r3 = subprocess.run([sys.executable, str(REVISAR), '--datos', str(datos), '--dir', str(trabajo)],
                        capture_output=True, text=True, encoding='utf-8', cwd=trabajo)
    assert 'Motor: versión' in r3.stdout
