import pytest

from crea_publicaciones import caption, revisar_caption
from crea_publicaciones.caption import main

TAGS = ['#LaboratorioCREA', '#AguaLab', '#EducaciónSTEAM', '#STEM', '#uniandesciam']


def _bien(**kw):
    return caption('Así fue la visita del colegio a nuestro taller AguaLab 💧',
                   'Midieron pH y turbidez, y con esos datos diseñaron sus propios filtros.',
                   '¿Quieres traer a tu colegio? Escríbenos.', hashtags=kw.get('hashtags', TAGS))


def test_formula_sin_avisos():
    texto = _bien()
    assert texto.endswith('#LaboratorioCREA #AguaLab #EducaciónSTEAM #STEM #uniandesciam')
    assert '\n\n#LaboratorioCREA' in texto
    assert revisar_caption(texto) == ([], [])


def test_hashtags_sin_numeral_se_completan():
    assert '#AguaLab' in caption('Hola', hashtags=['LaboratorioCREA', 'AguaLab'])


@pytest.mark.parametrize('hashtags, aviso', [
    (['#AguaLab', '#EducaciónSTEAM', '#STEM', '#Ingeniería', '#uniandesciam'], 'falta #LaboratorioCREA'),
    (['#LaboratorioCREA', '#AguaLab'], '2 hashtags'),
    (TAGS + ['#ingenieria'], 'CamelCase'),
    (TAGS + ['#AguaLab'], 'repetidos'),
])
def test_reglas_de_hashtags(hashtags, aviso):
    _, avisos = revisar_caption(_bien(hashtags=hashtags))
    assert any(aviso in a for a in avisos), avisos


def test_emoji_en_medio_de_la_frase():
    _, avisos = revisar_caption(caption('Hoy 🚀 construimos cohetes.', hashtags=TAGS))
    assert any('emoji en medio' in a for a in avisos)


def test_vinetas_y_gancho_con_emoji_al_inicio():
    texto = caption('🔧✨ ¿Te interesa la robótica?', '📚 Introducción: electrónica\n🎨 Diseño: circuitos',
                    hashtags=TAGS)
    assert revisar_caption(texto) == ([], [])


@pytest.mark.parametrize('frase, aviso', [
    ('Vos podés armar tu robot.', 'voseo'),
    ('Construyen — y prueban — su filtro.', 'raya larga'),
    ('Vinieron {validar: número} estudiantes.', 'sin validar'),
    ('Vinieron [validar] estudiantes.', 'sin validar'),
    ('palabra ' * 50, 'párrafo largo'),
    ('Hoy #AguaLab fue genial.', 'hashtag dentro'),
])
def test_reglas_de_voz(frase, aviso):
    _, avisos = revisar_caption(caption(frase, hashtags=TAGS))
    assert any(aviso in a for a in avisos), avisos


@pytest.mark.parametrize('texto, aviso', [
    (caption('¡El futuro de la ingeniería está en sus manos!', hashtags=TAGS), 'frase gastada'),
    (caption('Una experiencia única e inolvidable.', hashtags=TAGS), 'frase gastada'),
    (caption('Armamos robots 🤖🤖🤖', 'Y los probamos 🔋💡', hashtags=TAGS), 'emojis'),
    (caption('Uno 🤖', 'Dos 💡', 'Tres 🔋', hashtags=TAGS), 'todos los párrafos'),
    (caption('¡Uno!', '¡Dos!', '¡Tres!', '¡Cuatro!', hashtags=TAGS), 'exclamaciones'),
])
def test_senales_de_texto_en_serie(texto, aviso):
    _, avisos = revisar_caption(texto)
    assert any(aviso in a for a in avisos), avisos


def test_vinetas_no_cuentan_como_emojis():
    texto = caption('🔧 ¿Te interesa la robótica?',
                    '📚 Introducción: uno\n🎨 Diseño: dos\n🔩 Ensamble: tres\n💡 Prueba: cuatro',
                    'Escríbenos 🤖', hashtags=TAGS)
    assert revisar_caption(texto) == ([], [])


def test_limite_de_instagram():
    errores, _ = revisar_caption(caption('a ' * 1200, hashtags=TAGS))
    assert errores


def test_cli(tmp_path, capsys):
    ruta = tmp_path / 'caption.txt'
    ruta.write_text(_bien(), encoding='utf-8')
    assert main([str(ruta)]) == 0
    assert 'sin avisos' in capsys.readouterr().out
