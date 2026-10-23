from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[2]
FOTOS = SKILL / 'ejemplos' / 'fotos'


@pytest.fixture
def foto(tmp_path):
    """Una foto de 1600 x 1200 px para las pruebas."""
    from PIL import Image
    ruta = tmp_path / 'foto.png'
    Image.new('RGB', (1600, 1200), (120, 90, 60)).save(ruta)
    return ruta
