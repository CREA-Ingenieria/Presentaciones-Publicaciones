import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

ENTORNO = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('revisar', ENTORNO / 'revisar.py')
revisar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(revisar)


def test_python_suficiente():
    assert not revisar.python_suficiente((3, 9, 18))
    assert revisar.python_suficiente((3, 10, 0))
    assert revisar.python_suficiente((3, 12, 1))


def test_modo_vault_desde_subcarpeta(tmp_path):
    (tmp_path / 'identity').mkdir()
    (tmp_path / 'identity' / 'voice-and-tone.md').write_text('x', encoding='utf-8')
    sub = tmp_path / 'experiences' / 'agualab ñ'
    sub.mkdir(parents=True)
    assert revisar.detectar_modo(sub) == 'vault'


def test_modo_autonomo(tmp_path):
    assert revisar.detectar_modo(tmp_path) == 'autonomo'


def test_python_venv_por_sistema(tmp_path):
    assert revisar.python_venv(tmp_path, 'Windows') == tmp_path / 'venv' / 'Scripts' / 'python.exe'
    assert revisar.python_venv(tmp_path, 'Darwin') == tmp_path / 'venv' / 'bin' / 'python'


def test_venv_roto_se_recrea(tmp_path, monkeypatch):
    py = revisar.python_venv(tmp_path)
    py.parent.mkdir(parents=True)
    py.write_text('no soy un python', encoding='utf-8')
    creado = []
    monkeypatch.setattr(revisar, '_crear_venv', lambda datos: creado.append(datos))
    r = revisar.asegurar_venv(tmp_path)
    assert creado == [tmp_path]
    assert r.estado == revisar.OK and 'creado' in r.detalle


def test_paquete_al_dia_no_reinstala(monkeypatch):
    monkeypatch.setattr(revisar, 'version_instalada', lambda py: '1.0.0')
    monkeypatch.setattr(subprocess, 'run', lambda *a, **k: pytest.fail('no debía llamar a pip'))
    assert revisar.asegurar_paquete(Path('py'), '1.0.0').estado == revisar.OK


def test_paquete_viejo_se_reinstala(monkeypatch):
    versiones = iter(['0.9.0', '1.0.0'])
    monkeypatch.setattr(revisar, 'version_instalada', lambda py: next(versiones))
    llamadas = []
    monkeypatch.setattr(subprocess, 'run',
                        lambda args, **k: llamadas.append(args) or subprocess.CompletedProcess(args, 0, '', ''))
    r = revisar.asegurar_paquete(Path('py'), '1.0.0')
    assert r.estado == revisar.OK and '0.9.0' in r.detalle
    assert 'install' in llamadas[0]


def test_pip_falla(monkeypatch):
    monkeypatch.setattr(revisar, 'version_instalada', lambda py: None)
    monkeypatch.setattr(subprocess, 'run',
                        lambda args, **k: subprocess.CompletedProcess(args, 1, '', 'sin internet'))
    r = revisar.asegurar_paquete(Path('py'), '1.0.0')
    assert r.estado == revisar.ERROR and 'sin internet' in r.detalle


def test_motor_cambiado_sin_subir_version_se_reinstala(monkeypatch, tmp_path):
    motor = tmp_path / 'motor'
    (motor / revisar.PAQUETE).mkdir(parents=True)
    (motor / revisar.PAQUETE / 'base.py').write_text('a = 1', encoding='utf-8')
    h1 = revisar.huella_motor(motor)
    (motor / revisar.PAQUETE / 'base.py').write_text('a = 22', encoding='utf-8')
    assert revisar.huella_motor(motor) != h1
    monkeypatch.setattr(revisar, 'version_instalada', lambda py: '1.0.0')
    llamadas = []
    monkeypatch.setattr(subprocess, 'run',
                        lambda args, **k: llamadas.append(args) or subprocess.CompletedProcess(args, 0, '', ''))
    r = revisar.asegurar_paquete(Path('py'), '1.0.0', motor=motor, forzar=True)
    assert r.estado == revisar.OK and '--force-reinstall' in llamadas[0]


@pytest.mark.parametrize('sistema, hay, estado', [
    ('Windows', {'powershell'}, revisar.OK),
    ('Windows', set(), revisar.AVISO),
    ('Darwin', {'sips'}, revisar.OK),
])
def test_soporte_heic(monkeypatch, sistema, hay, estado):
    monkeypatch.setattr(revisar.shutil, 'which', lambda nombre: nombre if nombre in hay else None)
    assert revisar.soporte_heic(sistema).estado == estado


def test_heic_en_linux_depende_de_pillow_heif(monkeypatch):
    monkeypatch.setattr(subprocess, 'run', lambda args, **k: subprocess.CompletedProcess(args, 1, '', ''))
    assert revisar.soporte_heic('Linux', py='py').estado == revisar.AVISO
    monkeypatch.setattr(subprocess, 'run', lambda args, **k: subprocess.CompletedProcess(args, 0, '', ''))
    assert revisar.soporte_heic('Linux', py='py').estado == revisar.OK


@pytest.mark.parametrize('hay, version, estado', [
    ({'node', 'npx'}, 'v22.11.0\n', revisar.OK),
    ({'node', 'npx'}, 'v16.20.2\n', revisar.AVISO),
    ({'node'}, 'v22.11.0\n', revisar.AVISO),
    (set(), '', revisar.AVISO),
])
def test_soporte_animado(monkeypatch, hay, version, estado):
    monkeypatch.setattr(revisar.shutil, 'which', lambda nombre: nombre if nombre in hay else None)
    monkeypatch.setattr(subprocess, 'run', lambda args, **k: subprocess.CompletedProcess(args, 0, version, ''))
    r = revisar.soporte_animado()
    assert r.estado == estado
    if estado == revisar.AVISO:
        assert 'solo versiones estáticas' in r.detalle


def test_main_dice_si_hay_animado(monkeypatch, tmp_path, capsys):
    _entorno_falso(monkeypatch, [])
    monkeypatch.setattr(revisar, 'soporte_animado',
                        lambda: revisar.Revision('Versiones animadas', revisar.AVISO, 'sin Node'))
    assert revisar.main(['--datos', str(tmp_path), '--dir', str(tmp_path)]) == 1
    salida = capsys.readouterr().out.strip().splitlines()
    assert salida[-3] == 'ANIMADO=no' and salida[-2].startswith('PYTHON=')


def test_main_python_viejo(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(revisar, 'python_suficiente', lambda info=None: False)
    assert revisar.main(['--datos', str(tmp_path)]) == 2
    assert 'python.org' in capsys.readouterr().out


def _entorno_falso(monkeypatch, renders, render_ok=True):
    monkeypatch.setattr(revisar, 'asegurar_venv', lambda d: revisar.Revision('Entorno virtual', revisar.OK))
    monkeypatch.setattr(revisar, 'asegurar_paquete', lambda py, v, **k: revisar.Revision('Motor', revisar.OK))
    monkeypatch.setattr(revisar, 'soporte_heic', lambda **k: revisar.Revision('Fotos HEIC', revisar.OK))
    monkeypatch.setattr(revisar, 'soporte_animado', lambda: revisar.Revision('Versiones animadas', revisar.OK))

    def falso_render(py):
        renders.append(py)
        return revisar.Revision('Render de prueba', revisar.OK if render_ok else revisar.AVISO, 'x')
    monkeypatch.setattr(revisar, 'prueba_render', falso_render)


def test_render_solo_tras_cambio_de_version(monkeypatch, tmp_path, capsys):
    renders = []
    _entorno_falso(monkeypatch, renders)
    args = ['--datos', str(tmp_path), '--dir', str(tmp_path)]
    assert revisar.main(args) == 0
    assert revisar.main(args) == 0
    assert len(renders) == 1
    salida = capsys.readouterr().out.strip().splitlines()
    assert salida[-2].startswith('PYTHON=') and salida[-1] == 'MODO=autonomo'
    estado = json.loads((tmp_path / 'estado.json').read_text(encoding='utf-8'))
    estado['version'] = '0.0.1'
    (tmp_path / 'estado.json').write_text(json.dumps(estado), encoding='utf-8')
    revisar.main(args)
    assert len(renders) == 2
    revisar.main(args + ['--completa'])
    assert len(renders) == 3


def test_render_fallido_no_se_repite_solo(monkeypatch, tmp_path):
    renders = []
    _entorno_falso(monkeypatch, renders, render_ok=False)
    args = ['--datos', str(tmp_path), '--dir', str(tmp_path)]
    assert revisar.main(args) == 1
    assert revisar.main(args) == 1
    assert len(renders) == 1
    revisar.main(args + ['--completa'])
    assert len(renders) == 2


def test_render_con_timeout(monkeypatch):
    def cuelga(args, **k):
        assert k.get('timeout'), 'el render de prueba necesita timeout'
        raise subprocess.TimeoutExpired(args, k['timeout'])
    monkeypatch.setattr(subprocess, 'run', cuelga)
    assert revisar.prueba_render('py').estado == revisar.AVISO


def test_excepcion_inesperada_bloquea(monkeypatch, tmp_path, capsys):
    def explota(datos):
        raise RuntimeError('venv bloqueado')
    monkeypatch.setattr(revisar, 'asegurar_venv', explota)
    assert revisar.main(['--datos', str(tmp_path), '--dir', str(tmp_path)]) == 2
    salida = capsys.readouterr().out
    assert 'venv bloqueado' in salida and 'PYTHON=' not in salida
    assert salida.strip().splitlines()[-1] == 'MODO=autonomo'
