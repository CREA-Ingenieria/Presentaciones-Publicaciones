# Cómo proponer mejoras

Nadie hace push directo a `main`: todo entra por PR.

## Flujo

1. `git clone https://github.com/CREA-Ingenieria/Presentaciones-Publicaciones` y `git checkout -b <tu-nombre>/<tema>`.
2. Prepara tu entorno de desarrollo una vez: `cd plugins/publicaciones-crea/skills/publicaciones-crea && python -m pip install -e "motor[test]"`.
3. Haz el cambio. Si es del motor, agrega o ajusta su test en `motor/tests/`.
4. `python -m pytest -q` tiene que pasar en tu equipo, y los cuatro ejemplos (`ejemplos/build_*.py`) tienen que salir sin avisos.
5. Sube la versión en `plugins/publicaciones-crea/.claude-plugin/plugin.json`, `motor/pyproject.toml` y `__version__` en `motor/crea_publicaciones/__init__.py`, y agrega la entrada al `CHANGELOG.md`:
   - **Parche** (1.0.0 → 1.0.1): corrección sin cambios visibles en el estilo.
   - **Menor** (1.0.x → 1.1.0): pieza, animación o variante nueva.
   - **Mayor** (1.x → 2.0.0): algo que obliga a reescribir scripts `build_*.py` existentes.
6. Abre la PR. El CI corre los tests en Windows, Mac y Linux.

## Probar tu rama como plugin antes de la PR

```
claude --plugin-dir ./plugins/publicaciones-crea
```

La revisión del entorno reinstala el motor en su venv cada vez que cambia el código de `motor/crea_publicaciones/`, aunque no hayas subido la versión.

## Fotos

Las fotos de ejemplo (`ejemplos/fotos/`) son de objetos del taller, sin personas, a propósito. **No agregues fotos de estudiantes al repo**: un test lo vigila.

## Voz y tono

`referencia/voz-crea.md` es la misma de `material-crea`, que a su vez destila `identity/voice-and-tone.md` del vault de CREA. Si la voz cambia, actualiza las dos skills. Lo propio de Instagram vive en `referencia/caption.md`.
