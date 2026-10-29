import pytest

from crea_publicaciones import CUAD, POST, STORY, ErrorCREA, Pieza
from crea_publicaciones.base import MARGEN, PESOS, abrir, font


def test_fuentes_del_paquete_en_los_cinco_pesos():
    for peso in PESOS:
        assert font(36, peso).getname()[0] == 'Montserrat'
    with pytest.raises(ErrorCREA):
        font(36, 'italica')


def test_formato_desconocido():
    with pytest.raises(ErrorCREA):
        Pieza((1000, 1000))


def test_zonas_seguras():
    assert Pieza(POST).segura() == (72, 72, 1008, 1278)
    assert Pieza(STORY).segura() == (72, 250, 900, 1600)
    assert Pieza(POST).cuadro_perfil() == (0, 135, 1080, 1215)
    assert Pieza(CUAD).cuadro_perfil() == (0, 0, 1080, 1080)


def test_texto_dentro_no_avisa():
    p = Pieza(POST)
    p.texto('Hola', MARGEN, 600)
    assert p.revisar() == []


def test_texto_fuera_de_la_cuadricula_del_perfil():
    p = Pieza(POST)
    p.texto('Abajo', MARGEN, 1230)
    assert any('cuadrícula del perfil' in a for a in p.revisar())


def test_texto_en_la_franja_de_la_historia():
    p = Pieza(STORY)
    p.texto('Arriba', MARGEN, 100)
    assert any('fuera de zona segura' in a for a in p.revisar())


def test_superposicion_y_logo():
    p = Pieza(POST)
    p.texto('Uno', MARGEN, 600)
    p.texto('Dos', MARGEN, 610)
    p.logo()
    p.chip('Encima del logo', 840, 1150)
    avisos = p.revisar()
    assert any('se superponen: texto:Uno / texto:Dos' in a for a in avisos)
    assert any('crea_logo' in a for a in avisos)


def test_titulo_largo_avisa_en_vez_de_encogerse_en_silencio():
    p = Pieza(POST)
    p.texto('Un título demasiado largo para caber en dos líneas sin achicarse', MARGEN, 600,
            tam=96, peso='b', max_lineas=2)
    assert any('Acórtalo' in a for a in p.revisar())


def test_titulo_imposible_se_recorta_y_avisa():
    p = Pieza(POST)
    p.texto('palabra ' * 60, MARGEN, 400, tam=96, max_lineas=2)
    assert any('recortado' in a for a in p.revisar())


def test_dato_sin_validar_en_la_imagen():
    p = Pieza(POST)
    p.texto('Vinieron {validar: número} estudiantes', MARGEN, 600)
    assert any('sin validar' in a for a in p.revisar())


def test_logo_cambia_de_esquina_en_historia():
    x_post = Pieza(POST).logo()[0]
    x_story = Pieza(STORY).logo()[0]
    assert x_post > 800 and x_story == MARGEN


def test_foto_cubre_la_caja_sin_estirar(foto):
    p = Pieza(POST)
    p.foto(foto, (72, 72, 1008, 744), radio=64)
    assert p.im.getpixel((540, 400))[:3] == (120, 90, 60)
    assert p.im.getpixel((73, 73))[:3] == (255, 255, 255)     # esquina redondeada


def test_foto_pequena_avisa(tmp_path):
    from PIL import Image
    ruta = tmp_path / 'chica.jpg'
    Image.new('RGB', (200, 150)).save(ruta)
    p = Pieza(POST)
    p.foto(ruta, (72, 72, 1008, 744))
    assert any('baja resolución' in a for a in p.revisar())


def test_abrir_imagen_que_no_existe(tmp_path):
    with pytest.raises(ErrorCREA, match='No existe'):
        abrir(tmp_path / 'nada.jpg')


def test_mascota_solo_dos_poses():
    with pytest.raises(ErrorCREA):
        Pieza(POST).mascota(600, 600, pose='futbol')
