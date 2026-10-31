import pytest
from PIL import Image, ImageChops, ImageStat

from crea_publicaciones import ErrorCREA, creabot, entregar, lamina, seneca
from crea_publicaciones.base import POST, STORY, Pieza
from crea_publicaciones.personajes import PARCHE, POSES_CREABOT, POSES_SENECA
from conftest import SKILL


@pytest.mark.parametrize('pose', POSES_CREABOT)
def test_creabot_cada_pose(pose):
    im = creabot(pose, alto=240)
    assert im.mode == 'RGBA' and im.height == 240
    assert im.getpixel((0, 0))[3] == 0 or im.getpixel((im.width - 1, im.height - 1))[3] == 0


@pytest.mark.parametrize('pantalla', ['icono:robot', '</>', 'carga'])
def test_creabot_pantalla(pantalla):
    assert creabot('frente', alto=200, pantalla=pantalla).height == 200


def test_creabot_pose_que_no_existe():
    with pytest.raises(ErrorCREA, match='salta'):
        creabot('vuela')


@pytest.mark.parametrize('pose', POSES_SENECA)
def test_seneca_cada_pose(pose):
    im = seneca(pose, alto=300)
    assert im.mode == 'RGBA' and im.height == 300


def test_seneca_sin_buzo_amarillo():
    with pytest.raises(ErrorCREA, match='amarillo'):
        seneca('saludo', buzo='Y')


def _parche(im, base, espejo=False):
    x0, y0, x1, y1 = PARCHE[base]
    w, h = im.size
    caja = (round((1 - x1) * w), round(y0 * h), round((1 - x0) * w), round(y1 * h)) if espejo else \
        (round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h))
    return im.crop(caja).convert('RGB')


def test_el_espejo_no_voltea_el_logo():
    original, espejo = seneca('saludo', alto=800), seneca('saludo-espejo', alto=800)
    assert original.size == espejo.size
    dif = ImageStat.Stat(ImageChops.difference(_parche(original, 'saludo'), _parche(espejo, 'saludo', True)))
    volteado = ImageStat.Stat(ImageChops.difference(
        _parche(original, 'saludo'), _parche(espejo, 'saludo', True).transpose(Image.FLIP_LEFT_RIGHT)))
    assert sum(dif.mean) < sum(volteado.mean) / 3


def test_el_buzo_cambia_y_la_cara_no():
    t, o = seneca('saludo', alto=600, buzo='T'), seneca('saludo', alto=600, buzo='O')
    w, h = t.size
    buzo, cara = (round(w * 0.2), round(h * 0.62)), (round(w * 0.43), round(h * 0.2))
    assert t.getpixel(buzo)[:3] != o.getpixel(buzo)[:3]
    assert t.getpixel(cara) == o.getpixel(cara)


def test_sticker_de_recortes_con_pose(foto):
    p = lamina(foto, 'Un robot que salta', 'Bajada corta.', estilo='recortes', sticker='creabot:celebra')
    assert any(c.nombre == 'sticker' for c in p.capas)
    with pytest.raises(ErrorCREA, match='sticker'):
        lamina(foto, 'Título', estilo='recortes', sticker='dragon')


def test_mascota_en_otra_pose_y_buzo(tmp_path):
    p = Pieza(STORY)
    caja = p.mascota(600, 1200, alto=400, pose='asoma', buzo='M')
    assert caja[3] == 400 and p._mascota is None
    p2 = Pieza(POST)
    p2.img(creabot('salta', alto=300), 700, 900)
    r = entregar(tmp_path, p2)
    assert not r.errores and r.archivos


def test_personajes_md_nombra_cada_pose():
    doc = (SKILL / 'referencia' / 'personajes.md').read_text(encoding='utf-8')
    for pose in (*POSES_CREABOT, *POSES_SENECA):
        assert f'`{pose}`' in doc, pose
