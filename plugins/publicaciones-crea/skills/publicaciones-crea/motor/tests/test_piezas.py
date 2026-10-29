import pytest

from crea_publicaciones import B, M, O, POST, STORY, T, Y, ErrorCREA, convocatoria, cronica, historia, lamina


def test_cronica(foto):
    p = cronica(foto, 'Ingenieras por un día', 'Analizaron muestras y construyeron filtros.',
                aliado='Colegio de prueba')
    assert p.formato == POST and p.tipo == 'cronica'
    assert p.revisar() == []


def test_cronica_sin_aliado_ni_bajada(foto):
    assert cronica(foto, 'Ingenieras por un día').revisar() == []


@pytest.mark.parametrize('acento', [T, M, O, B, '00afc9'])
def test_acentos_de_la_paleta(foto, acento):
    cronica(foto, 'Título', acento=acento)


def test_amarillo_y_colores_ajenos_no_son_acento(foto):
    with pytest.raises(ErrorCREA, match='amarillo'):
        cronica(foto, 'Título', acento=Y)
    with pytest.raises(ErrorCREA, match='paleta'):
        cronica(foto, 'Título', acento='#00FF00')


def test_bajada_larga_no_se_sale_del_perfil(foto):
    p = cronica(foto, 'Un título que ocupa dos líneas', 'palabra ' * 40, aliado='Colegio')
    avisos = p.revisar()
    assert not any('cuadrícula' in a for a in avisos)
    assert any('Acórtalo' in a or 'recortado' in a for a in avisos)


def test_historia(foto):
    p = historia(foto, 'Ingenieras por un día', aliado='Colegio')
    assert p.formato == STORY and p.cuadros is None
    assert p.revisar() == []


def test_historia_animada_necesita_a_seneca(foto):
    assert historia(foto, 'Título', animar=True).animacion == 'parpadeo'
    with pytest.raises(ErrorCREA):
        historia(foto, 'Título', mascota=False, animar=True)


def test_lamina_con_codigo_se_anima(foto):
    p = lamina(foto, 'Y después, a probarlas', 'Bajada corta.', chip='Reto', codigo='repetir: probar')
    assert p.animacion == 'codigo' and len(p.cuadros) == 180
    assert p.revisar() == []


def test_convocatoria():
    p = convocatoria('Construye tu propio robot', ['Uno', 'Dos', 'Tres'], 'crea@uniandes.edu.co',
                     pregunta='¿Te interesa la robótica?')
    assert p.revisar() == []


def test_convocatoria_cuenta_los_puntos():
    with pytest.raises(ErrorCREA):
        convocatoria('Título', [], 'correo')
    with pytest.raises(ErrorCREA):
        convocatoria('Título', ['a'] * 5, 'correo')


@pytest.fixture
def video(tmp_path):
    """Un video vertical de 2 s a 30 fps, con un cuadro distinto cada segundo."""
    from PIL import Image

    from crea_publicaciones import mp4
    cuadros = [Image.new('RGB', (360, 640), (200, 30, 30) if i < 30 else (30, 30, 200)) for i in range(60)]
    return mp4(cuadros, tmp_path / 'video.mp4', 30)


def test_lamina_con_video(video):
    p = lamina(None, 'Manos a la obra', chip='Mothbot', video=video)
    assert p.animacion == 'video' and len(p.cuadros) == 60
    cuadros = list(p.cuadros)
    assert len(cuadros) == 60
    rojo, azul = cuadros[5].getpixel((540, 600)), cuadros[45].getpixel((540, 600))
    assert rojo[0] > 150 and azul[2] > 150
    # El chip se ve encima del video en cada cuadro, igual que en el JPG.
    assert cuadros[45].getpixel((140, 170)) == p.im.getpixel((140, 170))


def test_lamina_con_video_recortado(video):
    p = lamina(None, 'Título', video=video, desde=0.5, hasta=1.5)
    assert len(p.cuadros) == 30 and len(list(p.cuadros)) == 30


def test_video_vertical_contenido_no_se_amplia(video):
    cubierto = lamina(None, 'Título', video=video)
    contenido = lamina(None, 'Título', video=video, ajuste='contener')
    assert any('baja resolución' in a for a in cubierto.revisar())
    assert contenido.revisar() == []
    # Contenido: el video va al centro y los costados son su versión desenfocada y oscura.
    centro, costado = contenido.im.getpixel((540, 400)), contenido.im.getpixel((150, 400))
    assert centro[0] > 150 and costado[0] < centro[0]


def test_lamina_video_errores(video, foto):
    with pytest.raises(ErrorCREA, match='una sola'):
        lamina(None, 'Título', video=video, codigo='probar')
    with pytest.raises(ErrorCREA, match='foto o un video'):
        lamina(None, 'Título')
    with pytest.raises(ErrorCREA, match='tramo'):
        lamina(foto, 'Título', video=video, desde=5)
    with pytest.raises(ErrorCREA, match='ajuste'):
        lamina(foto, 'Título', ajuste='estirar')


def test_foco_elige_la_franja():
    from PIL import Image

    from crea_publicaciones.base import cubrir
    im = Image.new('RGB', (400, 1200), (255, 0, 0))
    im.paste((0, 0, 255), (0, 600, 400, 1200))
    assert cubrir(im, 400, 300, foco=0).getpixel((200, 150))[:3] == (255, 0, 0)
    assert cubrir(im, 400, 300, foco=1).getpixel((200, 150))[:3] == (0, 0, 255)


def test_iconos_van_sobre_el_video(video):
    p = lamina(None, 'Título', video=video, iconos=['robot'])
    primero = next(iter(p.cuadros))
    from crea_publicaciones.marco import FOTO
    centro = (FOTO[2] - 40 - 60 - 30, FOTO[3])
    assert primero.getpixel(centro) == p.im.getpixel(centro)
