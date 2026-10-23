"""Revisa y prepara el entorno de publicaciones-crea. Usa solo la librería estándar.

    python revisar.py --datos <carpeta de datos del plugin> [--completa] [--dir <carpeta de trabajo>]

Imprime una línea por revisión y termina con PYTHON=<ruta> (si el motor quedó listo) y
MODO=vault|autonomo. Sale con 0 (listo), 1 (advertencias) o 2 (bloqueado).
"""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import venv
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
MOTOR = SKILL / 'motor'
PAQUETE = 'crea_publicaciones'
DISTRIBUCION = 'crea-publicaciones'
PLUGIN_JSON = SKILL.parents[1] / '.claude-plugin' / 'plugin.json'
OK, AVISO, ERROR = 'ok', 'aviso', 'error'
ICONO = {OK: '✅', AVISO: '⚠️', ERROR: '❌'}


class Revision:
    def __init__(self, nombre, estado, detalle=''):
        self.nombre, self.estado, self.detalle = nombre, estado, detalle

    def linea(self):
        return f'{ICONO[self.estado]} {self.nombre}' + (f': {self.detalle}' if self.detalle else '')


def version_plugin(plugin_json=PLUGIN_JSON):
    return json.loads(Path(plugin_json).read_text(encoding='utf-8'))['version']


def python_suficiente(info=sys.version_info):
    return tuple(info[:2]) >= (3, 10)


def instrucciones_python(sistema=None):
    if (sistema or platform.system()) == 'Windows':
        return ('Instala Python 3.12: en una terminal corre `winget install Python.Python.3.12`, o descárgalo '
                'de https://www.python.org/downloads/ y marca "Add python.exe to PATH". Luego reinicia Claude Code.')
    return ('Instala Python 3.12 con el instalador de https://www.python.org/downloads/macos/ y reinicia '
            'Claude Code. El python3 que trae Xcode suele ser 3.9 y no sirve.')


def detectar_modo(inicio):
    inicio = Path(inicio).resolve()
    for carpeta in (inicio, *inicio.parents):
        if (carpeta / 'identity' / 'voice-and-tone.md').is_file():
            return 'vault'
    return 'autonomo'


def python_venv(datos, sistema=None):
    sistema = sistema or platform.system()
    partes = ('Scripts', 'python.exe') if sistema == 'Windows' else ('bin', 'python')
    return Path(datos).joinpath('venv', *partes)


def _corre(py):
    try:
        return subprocess.run([str(py), '-c', 'pass'], capture_output=True).returncode == 0
    except OSError:
        return False


def _crear_venv(datos):
    venv.EnvBuilder(with_pip=True, clear=True).create(str(Path(datos) / 'venv'))


def asegurar_venv(datos):
    py = python_venv(datos)
    if py.is_file() and _corre(py):
        return Revision('Entorno virtual', OK, str(py.parents[1]))
    _crear_venv(datos)
    return Revision('Entorno virtual', OK, f'creado en {Path(datos) / "venv"}')


def version_instalada(py):
    codigo = f"import importlib.metadata as m; print(m.version('{DISTRIBUCION}'))"
    try:
        r = subprocess.run([str(py), '-c', codigo], capture_output=True, text=True)
    except OSError:
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def huella_motor(motor=MOTOR):
    """Ruta, tamaño y fecha de cada archivo del paquete: cambia si cambia el código aunque no suba la versión."""
    h = hashlib.sha256()
    base = Path(motor) / PAQUETE
    for f in sorted(base.rglob('*')):
        if f.is_file() and '__pycache__' not in f.parts:
            st = f.stat()
            h.update(f'{f.relative_to(base).as_posix()}|{st.st_size}|{st.st_mtime_ns}\n'.encode('utf-8'))
    return h.hexdigest()


def asegurar_paquete(py, version, motor=MOTOR, forzar=False):
    antes = version_instalada(py)
    if antes == version and not forzar:
        return Revision('Motor', OK, f'versión {version}')
    opciones = ['--force-reinstall', '--no-deps'] if antes == version else ['--upgrade']
    r = subprocess.run([str(py), '-m', 'pip', 'install', '--disable-pip-version-check', '-q',
                        *opciones, str(motor)], capture_output=True, text=True)
    if r.returncode != 0:
        return Revision('Motor', ERROR, 'pip no pudo instalar el motor:\n' + (r.stderr or r.stdout)[-2000:])
    ahora = version_instalada(py)
    if ahora != version:
        return Revision('Motor', ERROR, f'quedó instalada la versión {ahora}, se esperaba {version}')
    if antes == version:
        return Revision('Motor', OK, f'reinstalado {version} (el código cambió)')
    return Revision('Motor', OK, f'instalado {version}' + (f' (antes {antes})' if antes else ''))


def soporte_heic(sistema=None, py=None):
    """Las fotos del iPhone llegan en HEIC; cada sistema las abre de una forma distinta."""
    sistema = sistema or platform.system()
    if sistema == 'Windows':
        if shutil.which('powershell'):
            return Revision('Fotos HEIC', OK, 'con el decodificador de Windows')
        return Revision('Fotos HEIC', AVISO, 'no se encontró PowerShell: pide las fotos en JPG')
    if sistema == 'Darwin' and shutil.which('sips'):
        return Revision('Fotos HEIC', OK, 'con sips de macOS')
    if py and subprocess.run([str(py), '-c', 'import pillow_heif'], capture_output=True).returncode == 0:
        return Revision('Fotos HEIC', OK, 'con pillow-heif')
    return Revision('Fotos HEIC', AVISO, 'no se pueden abrir en este equipo: pide las fotos en JPG '
                    'o instala pillow-heif en el entorno')


_PRUEBA = '''
import sys, tempfile
from pathlib import Path
from PIL import Image
from crea_publicaciones import Pieza, POST, T, animar, mp4
d = Path(tempfile.mkdtemp(prefix='crea-pub-prueba-'))
p = Pieza(POST)
p.patron(T)
p.texto('Prueba', 72, 400, peso='b', tam=96)
p.logo()
p.guardar(d / 'prueba.jpg')
cuadros = [p.im.copy() for _ in range(15)]
mp4(cuadros, d / 'prueba.mp4', 30)
ok = (d / 'prueba.jpg').stat().st_size > 0 and (d / 'prueba.mp4').stat().st_size > 0
print('ok' if ok else 'archivos vacíos')
sys.exit(0 if ok else 1)
'''


def prueba_render(py, timeout=120):
    try:
        r = subprocess.run([str(py), '-c', _PRUEBA], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return Revision('Render de prueba', AVISO, f'no terminó en {timeout} s. Corre de nuevo con --completa')
    if r.returncode == 0:
        return Revision('Render de prueba', OK, 'JPG y MP4')
    return Revision('Render de prueba', AVISO, (r.stdout + r.stderr).strip()[-1500:] +
                    '\nCuando lo corrijas, corre de nuevo con --completa')


def _leer_estado(datos):
    try:
        return json.loads((Path(datos) / 'estado.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def _guardar_estado(datos, estado):
    (Path(datos) / 'estado.json').write_text(json.dumps(estado), encoding='utf-8')


def _revisar(datos, completa):
    datos.mkdir(parents=True, exist_ok=True)
    version = version_plugin()
    revisiones = [Revision('Python', OK, platform.python_version()), asegurar_venv(datos)]
    py = python_venv(datos)
    estado = _leer_estado(datos)
    huella = huella_motor()
    paquete = asegurar_paquete(py, version, forzar=estado.get('huella') != huella)
    if paquete.estado == OK:
        estado['huella'] = huella
    revisiones.append(paquete)

    if paquete.estado == OK:
        if completa or estado.get('version') != version:
            render = prueba_render(py)
            revisiones.append(render)
            estado.update(version=version, render_ok=render.estado == OK)
        elif estado.get('render_ok') is False:
            revisiones.append(Revision('Render de prueba', AVISO, 'la última prueba falló; cuando lo corrijas, '
                                       'corre de nuevo con --completa'))
        revisiones.append(soporte_heic(py=py))
    _guardar_estado(datos, estado)
    return revisiones, py, paquete


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser(description='Revisa y prepara el entorno de publicaciones-crea.')
    ap.add_argument('--datos', required=True, help='carpeta de datos del plugin (${CLAUDE_PLUGIN_DATA})')
    ap.add_argument('--completa', action='store_true', help='repite el render de prueba')
    ap.add_argument('--dir', default=os.getcwd(), help='carpeta de trabajo, para detectar el modo')
    args = ap.parse_args(argv)
    modo = detectar_modo(args.dir)

    if not python_suficiente():
        print(Revision('Python', ERROR, f'{platform.python_version()} es muy viejo; se necesita 3.10 o más').linea())
        print(instrucciones_python())
        print(f'MODO={modo}')
        return 2

    try:
        revisiones, py, paquete = _revisar(Path(args.datos), args.completa)
    except Exception as e:  # noqa: BLE001 - cualquier sorpresa bloquea, nunca se sigue sin PYTHON=
        print(Revision('Revisión del entorno', ERROR, f'falló de forma inesperada: {type(e).__name__}: {e}').linea())
        print('Muéstrale este mensaje a quien mantiene la skill.')
        print(f'MODO={modo}')
        return 2

    for r in revisiones:
        print(r.linea())
    codigo = 2 if any(r.estado == ERROR for r in revisiones) else 1 if any(r.estado == AVISO for r in revisiones) else 0
    if paquete.estado == OK:
        print(f'PYTHON={py}')
    print(f'MODO={modo}')
    return codigo


if __name__ == '__main__':
    sys.exit(main())
