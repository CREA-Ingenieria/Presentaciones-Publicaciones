import subprocess

import imageio_ffmpeg
import pytest
from PIL import ImageChops, ImageStat

from crea_publicaciones import POST, ErrorCREA, Pieza, animar, mp4
from crea_publicaciones.base import WHITE


def _diferencia(a, b):
    return sum(ImageStat.Stat(ImageChops.difference(a.convert('RGB'), b.convert('RGB'))).mean)


def _pieza():
    p = Pieza(POST)
    p.patron()
    return p


@pytest.mark.parametrize('tipo, kw', [
    ('burbujas', {'caja': (100, 200, 900, 1100)}),
    ('torre', {'x': 540, 'y_base': 1100}),
    ('codigo', {'texto': 'repetir: probar', 'x': 72, 'y': 900, 'ancho': 780}),
])
def test_el_bucle_empalma(tipo, kw):
    p = animar(_pieza(), tipo, **kw)
    assert len(p.cuadros) == int((5.0 if tipo == 'burbujas' else 6.0) * 30)
    # El último cuadro está a un paso del primero: el bucle no da un salto.
    salto = _diferencia(p.cuadros[-1], p.cuadros[0])
    paso = max(_diferencia(p.cuadros[i], p.cuadros[i + 1]) for i in range(0, len(p.cuadros) - 1, 7))
    assert salto <= paso + 0.5


def test_parpadeo_solo_cambia_a_seneca():
    p = Pieza(POST)
    p.mascota(600, 700, alto=400)
    animar(p, 'parpadeo')
    x, y, w, h = p._mascota['caja']
    fija = p.im.convert('RGB')
    distintos = [c for c in p.cuadros if ImageChops.difference(c.convert('RGB'), fija).getbbox()]
    assert 0 < len(distintos) < len(p.cuadros)
    caja = ImageChops.difference(distintos[0].convert('RGB'), fija).getbbox()
    assert x <= caja[0] and caja[2] <= x + w and y <= caja[1] and caja[3] <= y + h


def test_parpadeo_sin_seneca():
    with pytest.raises(ErrorCREA, match='Séneca'):
        animar(Pieza(POST), 'parpadeo')


def test_una_sola_animacion_por_pieza():
    p = animar(_pieza(), 'burbujas')
    with pytest.raises(ErrorCREA, match='una sola'):
        animar(p, 'torre', x=540, y_base=1100)


def test_animacion_desconocida():
    with pytest.raises(ErrorCREA, match='no existe'):
        animar(_pieza(), 'confeti')


def test_torre_evita_el_color_del_fondo():
    from crea_publicaciones.animacion import torre_bloques
    p = Pieza(POST, fondo=WHITE)
    p.fondo('#D32985')
    animar(p, 'torre', x=540, y_base=1100, n=5, dur=1.0)
    assert p.animacion == 'torre'
    cuadros = torre_bloques(p.im, 540, 1100, n=1, colores=('#D32985', '#00AFC9'), evitar='#D32985', dur=0.1)
    assert cuadros[0].getpixel((540, 1100 - 31))[:3] == (0, 175, 201)


def test_mp4_con_audio_para_instagram(tmp_path):
    p = _pieza()
    salida = mp4([p.im.copy() for _ in range(10)], tmp_path / 'x.mp4', 30)
    info = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-hide_banner', '-i', str(salida)],
                          capture_output=True, text=True).stderr
    assert 'h264' in info and 'yuv420p' in info and 'Audio: aac' in info


def test_mp4_acepta_cuadros_perezosos(tmp_path):
    from crea_publicaciones.animacion import Cuadros
    p = _pieza()
    cuadros = Cuadros(lambda: (p.im.copy() for _ in range(10)), 10)
    assert len(cuadros) == 10
    assert mp4(cuadros, tmp_path / 'x.mp4', 30).stat().st_size > 0
    with pytest.raises(ErrorCREA, match='No hay cuadros'):
        mp4([], tmp_path / 'vacio.mp4')
