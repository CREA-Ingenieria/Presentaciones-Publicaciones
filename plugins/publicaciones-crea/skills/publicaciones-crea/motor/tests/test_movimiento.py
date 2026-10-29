import os
import re
import shutil

import pytest
from PIL import Image, ImageChops

from crea_publicaciones import B, O, T, contacto_reel, lamina, movimiento
from crea_publicaciones.base import DARK, WHITE, contraste, tinta
from conftest import FOTOS

EXTRA = {'recortes': {'sticker': 'creabot'}, 'arcade': {'nivel': 1}}


@pytest.fixture
def cache(tmp_path):
    """GSAP falso en la caché: los proyectos se escriben sin red ni npm."""
    c = tmp_path / 'cache'
    c.mkdir()
    (c / 'gsap.min.js').write_text('/* gsap */', encoding='utf-8')
    return c


def _lamina(estilo):
    return lamina(FOTOS / 'foto-demo.jpg', 'Un puente de palitos', 'Cada equipo cargó su cercha.', chip='Taller',
                  iconos=['truss', 'weight'], acento=O, estilo=estilo, **EXTRA[estilo])


@pytest.mark.parametrize('estilo', ['recortes', 'arcade'])
def test_las_capas_componen_la_lamina_estatica(estilo):
    p = _lamina(estilo)
    lienzo = Image.new('RGBA', p.im.size, (0, 0, 0, 0))
    for c in sorted(p.capas, key=lambda c: c.encima):
        lienzo.alpha_composite(c.img.convert('RGBA'), (c.x, c.y))
    dif = ImageChops.difference(lienzo.convert('RGB'), p.im.convert('RGB'))
    assert max(b[1] for b in dif.getextrema()) <= 2


@pytest.mark.parametrize('estilo', ['recortes', 'arcade'])
def test_proyecto_capas(tmp_path, cache, estilo):
    p = _lamina(estilo)
    duracion = movimiento.proyecto_capas(tmp_path / 'p', p, estilo, cache=cache)
    html = (tmp_path / 'p' / 'index.html').read_text(encoding='utf-8')
    assert duracion > 0 and "window.__timelines['main']" in html
    ids = re.findall(r'id="([^"]+)"', html)
    assert len(ids) == len(set(ids)), 'ids repetidos'
    for c in p.capas:
        assert (tmp_path / 'p' / 'assets' / f'{c.nombre}.png').is_file()


def test_proyecto_capas_sin_capas(tmp_path, cache, foto):
    with pytest.raises(Exception, match='capas'):
        movimiento.proyecto_capas(tmp_path / 'p', lamina(foto, 'Título'), 'recortes', cache=cache)


def _reel(carpeta, cache, video, acento=B, contacto=None):
    foto = FOTOS / 'foto-demo.jpg'
    return movimiento.reel(
        carpeta, acento=acento, cache=cache, contacto=contacto,
        gancho=dict(video=video, titulo='¿Cuánto peso aguanta?', chip='Taller'),
        revelacion=dict(foto=foto, titulo='Un puente', bajada='Cada equipo cargó su cercha.'),
        conceptos=dict(antes='Hablamos de', palabras=['tensión', 'cargas'], iconos=['truss', 'weight']),
        momento=dict(video=video, titulo='Triángulos'),
        cierre=dict(foto=foto, titulo='¡Gracias!', bajada='Nos vemos pronto.'))


@pytest.fixture
def video(tmp_path):
    from crea_publicaciones import mp4
    return mp4([Image.new('RGB', (360, 640), (200, 30, 30)) for _ in range(60)], tmp_path / 'video.mp4', 30)


def test_reel_termina_con_el_contacto(tmp_path, cache, video):
    con = _reel(tmp_path / 'con', cache, video, contacto=contacto_reel())
    sin = _reel(tmp_path / 'sin', cache, video)
    assert con == pytest.approx(sin + 4.5)
    html = (tmp_path / 'con' / 'index.html').read_text(encoding='utf-8')
    assert 's-contacto' in html and '@crea_uniandes' in html
    assert 'crea@uniandes.edu.co' not in html, 'un dato por validar no se publica'
    ids = re.findall(r'id="([^"]+)"', html)
    assert len(ids) == len(set(ids)), 'ids repetidos'


def test_reel_no_mueve_las_fotos(tmp_path, cache, video):
    _reel(tmp_path / 'r', cache, video, contacto=contacto_reel())
    html = (tmp_path / 'r' / 'index.html').read_text(encoding='utf-8')
    guion = html[html.index('gsap.timeline'):]
    for foto in ('#mueve-revela', '#mueve-cierre', '#foto-mueve'):
        assert foto not in guion, f'{foto} se anima: la foto no se mueve (decisión de CREA, 2026-10-28)'


@pytest.mark.parametrize('acento, letra', [(B, WHITE), (T, DARK), (O, DARK)])
def test_reel_letra_legible_sobre_el_acento(tmp_path, cache, video, acento, letra):
    _reel(tmp_path / 'r', cache, video, acento=acento, contacto=contacto_reel())
    html = (tmp_path / 'r' / 'index.html').read_text(encoding='utf-8')
    assert f'#firma {{ position: absolute; left: 240px; top: 1206px; color: {letra}; }}' in html


def test_tinta_y_contraste():
    assert contraste(WHITE, WHITE) == pytest.approx(1)
    assert contraste('#000000', WHITE) == pytest.approx(21)
    assert tinta(B) == WHITE and tinta(T) == DARK and tinta(O) == DARK
    for acento in (T, O, B):
        assert contraste(tinta(acento), acento) >= 3


@pytest.mark.skipif(not (os.environ.get('CREA_RENDER') and shutil.which('npx')),
                    reason='render real con HyperFrames: CREA_RENDER=1 y Node')
def test_render_real_de_una_lamina(tmp_path):
    laminas = [dict(foto=FOTOS / 'foto-demo.jpg', titulo='Un puente de palitos', iconos=['truss'])]
    movimiento.carrusel(tmp_path, laminas, estilo='recortes', acento=O)
    assert (tmp_path / 'carrusel-1.mp4').stat().st_size > 0 and (tmp_path / 'carrusel-1.jpg').is_file()
