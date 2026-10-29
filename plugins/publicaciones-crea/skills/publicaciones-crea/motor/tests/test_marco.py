import pytest

from crea_publicaciones import B, M, POST, T, ErrorCREA, Pieza, cronica, lamina
from crea_publicaciones.marco import FOTO, claves_iconos, colores_iconos, encima, ruta_icono, zona_iconos


def test_iconos_en_los_siete_colores():
    claves = claves_iconos()
    assert len(claves) == 68
    for clave in ('robot', 'bulb', 'cogs'):
        for c in 'wd':
            assert ruta_icono(clave, c).is_file()


def test_icono_mal_escrito_sugiere():
    with pytest.raises(ErrorCREA, match='robot'):
        ruta_icono('robto')


def test_colores_de_los_iconos_no_repiten_el_acento():
    for acento in (T, M, B):
        assert acento not in colores_iconos(acento, 3)
    assert len(set(colores_iconos(B, 3))) == 3


def test_maximo_tres_iconos():
    with pytest.raises(ErrorCREA, match='hasta 3'):
        encima(Pieza(POST), T, iconos=['robot', 'bulb', 'cogs', 'gear'])


def test_lamina_con_iconos_sin_avisos(foto):
    p = lamina(foto, 'Robots que siguen la luz', 'Una bajada corta.', chip='Taller', acento=B,
               iconos=['robot', 'bulb', 'cogs'])
    assert p.revisar() == []
    assert sum(1 for etq, _ in p.cajas if etq.startswith('icono')) == 3
    # El círculo del primer ícono (a la derecha) es del primer color que no es el acento.
    assert p.im.getpixel((FOTO[2] - 40 - 60, FOTO[3] + 50))[:3] == (0xD3, 0x29, 0x85)


def test_marco_pinta_los_colores_de_marca(foto):
    p = lamina(foto, 'Título', acento=B)
    # El bloque corrido asoma arriba de la foto, y el punto amarillo está en su esquina.
    assert p.im.getpixel((540, 84))[:3] == (0x00, 0x51, 0xC6)
    assert p.im.getpixel((1008 - 34, 72 + 34))[:3] == (0xEB, 0xE2, 0x12)


def test_aliado_largo_baja_si_choca_con_los_iconos(foto):
    corto = cronica(foto, 'Título', aliado='Colegio', iconos=['robot', 'bulb', 'cogs'])
    largo = cronica(foto, 'Título', aliado='Institución Educativa Distrital de Nombre Largo',
                    iconos=['robot', 'bulb', 'cogs'])
    y = lambda p: next(c[1] for etq, c in p.cajas if etq.startswith('chip:Inst') or etq.startswith('chip:Cole'))
    assert y(corto) == 792 and y(largo) > 792
    assert not any('se superponen' in a for a in largo.revisar())
