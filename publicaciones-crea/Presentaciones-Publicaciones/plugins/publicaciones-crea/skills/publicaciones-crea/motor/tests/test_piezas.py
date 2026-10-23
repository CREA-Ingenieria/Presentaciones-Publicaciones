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
