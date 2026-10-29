import pytest

from crea_publicaciones import ErrorCREA, caption, cronica, entregar, historia, lamina

TAGS = ['#LaboratorioCREA', '#AguaLab', '#EducaciónSTEAM', '#STEM', '#uniandesciam']
CAPTION = caption('¡Un gran día en el laboratorio! 🔬✨', hashtags=TAGS)


def test_entrega_completa(tmp_path, foto):
    r = entregar(tmp_path, cronica(foto, 'Ingenieras por un día'), CAPTION)
    assert r.codigo == 0, r.avisos + r.errores
    assert (tmp_path / 'cronica.jpg').is_file()
    assert (tmp_path / 'caption.txt').read_text(encoding='utf-8').startswith('¡Un gran día')
    assert (tmp_path / 'revision' / 'cronica-perfil.jpg').is_file()


def test_carrusel_se_nombra_y_solo_la_primera_va_al_perfil(tmp_path, foto):
    laminas = [lamina(foto, 'Uno'), lamina(foto, 'Dos', codigo='probar')]
    r = entregar(tmp_path, laminas, CAPTION)
    assert r.codigo == 0, r.avisos
    nombres = sorted(a.name for a in r.archivos)
    assert nombres == ['caption.txt', 'carrusel-1.jpg', 'carrusel-2.jpg', 'carrusel-2.mp4']
    assert [p.name for p in (tmp_path / 'revision').iterdir()] == ['carrusel-1-perfil.jpg']


def test_primera_lamina_animada_avisa(tmp_path, foto):
    r = entregar(tmp_path, [lamina(foto, 'Uno', codigo='probar'), lamina(foto, 'Dos')], CAPTION)
    assert any('primera lámina' in a for a in r.avisos)


def test_publicacion_animada_sube_como_reel(tmp_path, foto):
    from crea_publicaciones import animar
    p = animar(cronica(foto, 'Título'), 'burbujas', dur=1.0)
    r = entregar(tmp_path, p, CAPTION)
    assert any('reel' in a for a in r.avisos)


def test_historia_sin_caption_y_con_zonas(tmp_path, foto):
    r = entregar(tmp_path, historia(foto, 'Ingenieras por un día'))
    assert r.codigo == 0, r.avisos
    assert (tmp_path / 'revision' / 'historia-zonas.jpg').is_file()


def test_publicacion_sin_caption_avisa(tmp_path, foto):
    r = entregar(tmp_path, cronica(foto, 'Título'))
    assert any('sin caption' in a for a in r.avisos)


def test_final_convierte_lo_no_validado_en_error(tmp_path, foto):
    texto = caption('Vinieron {validar: número} estudiantes. 🔬✨', hashtags=TAGS)
    assert entregar(tmp_path, cronica(foto, 'Título'), texto).codigo == 1
    r = entregar(tmp_path, cronica(foto, 'Título'), texto, final=True)
    assert r.codigo == 2 and any('sin validar' in e for e in r.errores)


def test_nombres_repetidos(tmp_path, foto):
    with pytest.raises(ErrorCREA, match='mismo nombre'):
        entregar(tmp_path, [cronica(foto, 'A'), cronica(foto, 'B')], CAPTION)


def test_la_revision_vieja_no_se_queda(tmp_path, foto):
    (tmp_path / 'revision').mkdir()
    (tmp_path / 'revision' / 'vieja-perfil.jpg').write_bytes(b'x')
    entregar(tmp_path, cronica(foto, 'Título'), CAPTION)
    assert not (tmp_path / 'revision' / 'vieja-perfil.jpg').exists()


def test_carrusel_con_video(tmp_path, foto):
    from PIL import Image

    from crea_publicaciones import mp4
    video = mp4([Image.new('RGB', (1280, 720), (0, 120, 200)) for _ in range(15)], tmp_path / 'v.mp4', 30)
    r = entregar(tmp_path / 'salida', [lamina(foto, 'Uno'), lamina(None, 'Dos', video=video)], CAPTION)
    assert r.codigo == 0, r.avisos
    assert (tmp_path / 'salida' / 'carrusel-2.mp4').is_file()
