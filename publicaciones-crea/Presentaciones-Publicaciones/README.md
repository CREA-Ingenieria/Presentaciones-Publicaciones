# Presentaciones y publicaciones CREA

Skills de Claude Code del Laboratorio CREA, Universidad de los Andes.

## publicaciones-crea

Publicaciones de Instagram con el estilo CREA a partir de las fotos de un taller: **crónica de taller** (4:5), **historia** (9:16), **carrusel** y **convocatoria**. Entrega la pieza en JPG, un MP4 en bucle si lleva animación, y el caption listo para copiar.

Es la hermana de `material-crea` (presentaciones y documentos, en [`CREA-Ingenieria/skills-crea`](https://github.com/CREA-Ingenieria/skills-crea)): comparte paleta, tipografía, Séneca y lenguaje, pero no necesita PowerPoint.

### Antes de instalar

- **Claude Code** (terminal o app de escritorio).
- **Python 3.10 o más.** Si no lo tienes, la skill te dice cómo instalarlo la primera vez que la uses.
- No hace falta PowerPoint, ni instalar fuentes, ni ffmpeg: todo viene dentro del motor.

### Instalar

En Claude Code:

```
/plugin marketplace add CREA-Ingenieria/Presentaciones-Publicaciones
/plugin install publicaciones-crea@crea-publicaciones
```

Luego pásale a Claude las fotos del taller y lo que pasó, por ejemplo: "hazme una publicación de CREA con estas fotos del taller AguaLab con el Liceo". La skill te hace las preguntas que le faltan, te muestra la pieza y el caption en texto para que los apruebes, y recién entonces genera los archivos.

La frase que conviene decirle:

> **"Antes de generar nada, hazme las preguntas y muéstrame el caption."**

### Actualizar

```
/plugin marketplace update crea-publicaciones
/plugin update publicaciones-crea@crea-publicaciones
```

Después reinicia Claude Code.

### Probar sin instalar

```
claude --plugin-dir ./plugins/publicaciones-crea
```

### Llevarla a `skills-crea`

El plugin sigue la misma estructura que `material-crea`, así que puede vivir en el mismo marketplace:

1. Copia `plugins/publicaciones-crea/` a `skills-crea/plugins/`.
2. Agrega la entrada al `plugins` de `skills-crea/.claude-plugin/marketplace.json` (la misma de `.claude-plugin/marketplace.json` de este repo).
3. Agrega `publicaciones-crea` al CI de `skills-crea` (el `working-directory` de `.github/workflows/tests.yml` de este repo) y la entrada al `CHANGELOG.md`.

Desde ahí se instala con `/plugin install publicaciones-crea@crea`.

### Problemas frecuentes

| Síntoma | Qué hacer |
|---|---|
| "Python … es muy viejo" o no encuentra Python | Instala Python 3.12 (la skill te da el comando) y reinicia Claude Code |
| No abre las fotos del iPhone (HEIC) | En Windows y Mac se abren solas; si no, pide las fotos en JPG |
| `marketplace add` falla con 404 o pide clave | Tu git no está autenticado con una cuenta de la org: `gh auth login` |

## Proponer mejoras

Mira [CONTRIBUTING.md](CONTRIBUTING.md).
