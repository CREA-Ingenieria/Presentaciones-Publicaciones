---
name: publicaciones-crea
description: Crea publicaciones de Instagram del Laboratorio CREA (crónica de taller, historia, carrusel, convocatoria) a partir de las fotos de un taller, con la identidad visual y el lenguaje de CREA. Entrega la pieza en JPG (y MP4 en bucle si lleva animación) más el caption listo para copiar. Úsala cuando pidan una publicación, post, historia, carrusel o caption de Instagram "de CREA", o pasen fotos de un taller de CREA para redes. No la uses para presentaciones ni documentos (eso es material-crea).
---

# Publicaciones CREA

Convierte las fotos de un taller en una publicación de Instagram completa: la pieza visual y el caption, **generados con código** sobre la misma retícula, la misma paleta y el mismo lenguaje del laboratorio, para que la cuenta se vea como una cuenta y no dependa de quién la arme.

La skill no publica, no edita video y no inventa datos. Entrega los archivos; subirlos es de CREA.

## Paso 0: revisar el entorno (siempre, antes de todo)

Prueba `py -3 --version`, `python3 --version` y `python --version`, y usa el primero que corra y sea 3.10 o más. Si ninguno sirve, **para** y dile a la persona cómo instalar Python:

- **Windows:** `winget install Python.Python.3.12` en una terminal, o el instalador de https://www.python.org/downloads/ marcando "Add python.exe to PATH".
- **Mac:** el instalador de https://www.python.org/downloads/macos/ (el `python3` que trae Xcode suele ser 3.9 y no sirve).

Después tiene que reiniciar Claude Code. Con un Python que sirva, corre la revisión:

```
python "${CLAUDE_PLUGIN_ROOT}/skills/publicaciones-crea/entorno/revisar.py" --datos "${CLAUDE_PLUGIN_DATA}"
```

- Instala o actualiza sola lo que falte: entorno virtual y motor (Pillow e imageio-ffmpeg, que trae su propio ffmpeg). Montserrat viene dentro del motor: no hay que instalar fuentes. La primera vez y después de cada actualización genera un JPG y un MP4 de prueba.
- **Código 2 (bloqueado):** muéstrale a la persona el mensaje tal cual y no sigas.
- **Código 1 (advertencias):** cuéntale qué falta y sigue. Lo habitual es que este equipo no abra fotos HEIC del iPhone: pídelas en JPG.
- **`PYTHON=<ruta>`**: es el único intérprete con el que se corren los `build_*.py`. En el resto de esta skill, `<PYTHON>` significa esa ruta.
- **`MODO=vault`** o **`MODO=autonomo`**: decide de dónde salen el nombre del taller, los conceptos y la voz (paso 1).

## El flujo: 5 pasos, sin saltarse ninguno

1. **Mirar las fotos y preguntar.** Abre cada imagen antes de preguntar nada: qué se ve, cuál se lee mejor en miniatura, si hay caras de estudiantes. Luego haz **todas las preguntas en una sola tanda, con una opción por defecto propuesta** (no una por mensaje):
   - **Qué se publica:** publicación del feed, historia o carrusel (cuántas láminas y en qué orden).
   - **Qué tipo es:** crónica de taller, convocatoria o proyecto institucional (ver `referencia/estandar.md`).
   - **Crónica:** qué taller (nombre propio exacto), qué colegio o aliado, qué hicieron concretamente (conceptos y actividades reales) y **si hay autorización de uso de imagen** para las caras.
   - **Convocatoria:** qué taller se abre y para quién, qué aprenderán (2 o 3 puntos), cómo se inscriben, y fecha solo si está confirmada.
   - **Proyecto institucional:** qué es y qué resuelve, quién lo lideró y quién participó (con sus cuentas si se etiquetan), qué aliados.
   - **Cierre:** color de acento (por defecto, el del taller) y si lleva animación sutil (cuál).

   En **`MODO=vault`**, antes de preguntar lee `identity/voice-and-tone.md` y la nota de la experiencia (`experiences/<exp>/<exp>.md`): de ahí salen el nombre propio del taller y los conceptos; pregunta solo lo que falte. En **`MODO=autonomo`**, la voz sale de `referencia/voz-crea.md` y `referencia/caption.md`.
2. **Proponer la pieza y el caption en texto y esperar la aprobación.** Qué foto va en cada pieza o lámina, título, bajada, chips, acento, animación, y el **caption completo**. Di explícitamente **qué se dedujo y qué se inventó**. Todo dato sin confirmar va como `{validar:…}`. Si quieres, revisa el caption antes de mostrarlo: guárdalo en un `.txt` y corre `<PYTHON> -m crea_publicaciones.caption <archivo>.txt`. **No generes nada sin aprobación.**
3. **Generar.** Escribe `build_<pieza>.py` con las funciones de `referencia/piezas.md` y córrelo con `<PYTHON> build_<pieza>.py`. Termina con `entregar(...)`, que guarda las piezas, exporta los MP4, escribe `caption.txt` y revisa todo.
4. **Revisar y regenerar.** Mira **todas** las piezas generadas y lo que hay en `revision/`: cómo queda cada publicación en la cuadrícula del perfil y, en las historias, qué tapa la interfaz de Instagram (en rojo). Lee los avisos del informe. Corrige el **script** y regenera; nunca edites la imagen a mano. Una pieza que se entrega no lleva avisos.
5. **Entregar.** Corre la versión final con `entregar(..., final=True)`: si quedan datos `{validar:…}`, sale con error. Entrega la lista de archivos y el **caption en un bloque aparte, listo para copiar y pegar**. Si hay MP4, di en qué posición del carrusel va.

## Qué leer según la pieza

| Pieza | Lee |
|---|---|
| Cualquiera | `referencia/estandar.md` (formatos, retícula, paleta, Séneca) y `referencia/piezas.md` (las funciones) |
| El caption | `referencia/caption.md`; en `MODO=autonomo`, también `referencia/voz-crea.md` |
| Lleva animación | `referencia/animaciones.md` |
| Algo falló | `referencia/errores-conocidos.md` |

## Dónde queda cada pieza

En `./<AAAA-MM-DD-tema>/`, dentro de la carpeta donde se abrió Claude Code. Lleva `build_<pieza>.py`, los `.jpg` y `.mp4`, `caption.txt`, `revision/` y un `README.md` corto que cuenta de dónde salió el contenido, **qué falta validar** y cómo se regenera (`<PYTHON> build_<pieza>.py`, con la ruta completa de `<PYTHON>`).

**Las fotos de estudiantes no viajan.** Se quedan en la carpeta de quien hizo el encargo: no se suben a ningún repositorio ni se meten en material que se comparte. En `MODO=vault`, pregunta antes de guardar la carpeta dentro del vault.

## Esqueleto de un script

```python
"""Crónica del taller AguaLab con el Liceo. Regenerar: <PYTHON> build_cronica_agualab.py"""
from pathlib import Path

from crea_publicaciones import *  # noqa: F403

AQUI = Path(__file__).resolve().parent

pieza = cronica(AQUI / 'fotos' / 'IMG_0412.jpg', 'Ingenieras por un día',
                'Analizaron muestras del Eje Ambiental y construyeron sus propios filtros.',
                aliado='Liceo Femenino de Cundinamarca', acento=T)
texto = caption('¡…! 👩‍🔬💧', 'Recibimos al … en nuestro taller AguaLab…', '…', '¡…! 🌎✨',
                hashtags=['#LaboratorioCREA', '#AguaLab', '#EducaciónSTEAM', '#MujeresEnSTEAM', '#uniandesciam'])
raise SystemExit(entregar(AQUI, pieza, texto).codigo)
```

Para un carrusel, `entregar(AQUI, [lamina(...), lamina(...)], texto)`. Para una historia, `entregar(AQUI, historia(...))`: las historias no llevan caption.

## Reglas que no se negocian

- **No inventar datos.** Cantidades, edades, duraciones, fechas y nombres propios salen de lo que dijo alguien de CREA o del vault; si no, se omiten o van con `{validar:…}`. Una publicación con un dato inventado es peor que una sin ese dato.
- **Autorización de imagen.** Antes de publicar una foto con menores, alguien de CREA confirma que hay autorización de uso de imagen. Si no la hay, se elige otro encuadre (manos, materiales, el montaje). Esto no lo decide la skill.
- **El taller se nombra siempre con su nombre propio** ("nuestro taller AguaLab"), en la pieza y en el caption.
- **Un título que no cabe es un título largo:** si el informe dice que se encogió o se recortó, **se acorta el texto**; no se achica la letra.
- **Un color de acento por pieza**, de la paleta. Nunca amarillo como color de letra ni como acento. Sin cursiva.
- **Una sola animación por pieza**, en bucle, y la primera lámina de un carrusel va estática.
- **Regenerar, no parchar.**
- Al entregar, di qué se **dedujo o inventó** para que alguien de CREA lo valide.
