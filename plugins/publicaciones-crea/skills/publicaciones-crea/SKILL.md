---
name: publicaciones-crea
description: Crea publicaciones de Instagram del Laboratorio CREA (crónica de taller, historia, carrusel, convocatoria y reel) a partir de las fotos y videos de un taller, con la identidad visual y el lenguaje de CREA. Cada carrusel sale en uno de tres estilos (marco, recortes, arcade), en versión estática (JPG) y animada (MP4), más el caption listo para copiar. Úsala cuando pidan una publicación, post, historia, carrusel, reel, variantes o caption de Instagram "de CREA", o pasen fotos o videos de un taller de CREA para redes. No la uses para presentaciones ni documentos (eso es material-crea).
---

# Publicaciones CREA

Convierte las fotos y videos de un taller en una publicación de Instagram completa: la pieza visual y el caption, **generados con código** sobre la misma retícula, la misma paleta y el mismo lenguaje del laboratorio, para que la cuenta se vea como una cuenta y no dependa de quién la arme.

Tú (Claude) haces el trabajo de criterio: mirar el material, elegir la foto, escribir el titular y el caption, proponer el estilo y revisar el resultado. El motor hace el trabajo exacto: retícula, colores, tipografía, íconos, animación, recortes de Instagram. Lo que la skill ya sabe de CREA (talleres, contacto, hashtags, aliados) está en `referencia/crea.md`; lo que CREA aprobó y rechazó, en `referencia/revision-visual.md`. **Úsalo en vez de preguntarlo o inventarlo.**

La skill no publica y no inventa datos. Entrega los archivos; subirlos es de CREA.

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
- **Código 1 (advertencias):** cuéntale qué falta y sigue. Lo habitual: este equipo no abre fotos HEIC del iPhone (pídelas en JPG) o no tiene Node.
- **`ANIMADO=no`**: no hay Node, así que **solo se pueden hacer versiones estáticas** (JPG y los MP4 del motor). Dilo en el paso 2, antes de proponer algo animado o un reel. Con `ANIMADO=si`, las versiones animadas usan HyperFrames (`referencia/movimiento.md`).
- **`PYTHON=<ruta>`**: es el único intérprete con el que se corren los `build_*.py`. En el resto de esta skill, `<PYTHON>` significa esa ruta.
- **`MODO=vault`** o **`MODO=autonomo`**: decide de dónde salen el nombre del taller, los conceptos y la voz (paso 1).

## Mapa de decisiones

Antes de proponer nada, decide estas cuatro cosas. Si la persona no lo dijo, propón la opción por defecto.

| Pregunta | Opciones | Por defecto | Dónde está |
|---|---|---|---|
| **¿Qué pieza?** | Publicación suelta (crónica) · carrusel · historia · convocatoria · reel | Carrusel de 3 a 5 láminas si hay más de dos fotos buenas; crónica si hay una | `referencia/estandar.md`, `referencia/piezas.md` |
| **¿Qué estilo?** | `marco` (sobrio, la cara diaria) · `recortes` (collage hecho a mano) · `arcade` (programación, robótica, público joven) | `marco`, con una variante en otro estilo si el taller lo pide | `referencia/estilos.md` |
| **¿Estática o animada?** | Estática (JPG) · animada (MP4 con HyperFrames) · las dos | Las dos cuando hay Node: la estática va siempre, la animada se ofrece | `referencia/movimiento.md` |
| **¿Reel?** | Sí, cuando hay video del taller y se quiere alcance fuera del perfil | Ofrécelo si llegan videos | `referencia/movimiento.md` (el reel) |

Reglas del mapa:

- Un carrusel va **entero en un estilo y un acento**. La primera lámina es un JPG; los videos van de la segunda en adelante.
- Si piden «variantes» u «otros estilos», entrega los tres, cada uno con versión estática y animada (`referencia/estilos.md`).
- Un reel **siempre termina con el contacto** del laboratorio (`contacto_reel()` del set de CREA).
- **La foto nunca se mueve**: ni acercamiento ni paneo, en ningún estilo ni en el reel. Se anima el diseño.

## El flujo: 5 pasos, sin saltarse ninguno

1. **Mirar el material y preguntar.** Abre cada imagen antes de preguntar nada: qué se ve, cuál se lee mejor en miniatura, si hay caras de estudiantes, si hay letreros o logos que no se pueden tapar, si es de WhatsApp (comprimida). De los videos, saca cuadros de todo el largo (con el ffmpeg de `imageio_ffmpeg`) para ver qué muestran y dónde hay que cortar. Busca el taller y el aliado en el set de CREA (`referencia/crea.md`; desde código, `taller()`, `contacto_reel()` y `por_validar()`): lo **confirmado** no se pregunta. Luego haz **todas las preguntas en una sola tanda, con una opción por defecto propuesta** (no una por mensaje):
   - **Qué se publica:** las cuatro decisiones del mapa (pieza, estilo, estática o animada, reel), con tu propuesta.
   - **Qué tipo es:** crónica de taller, convocatoria o proyecto institucional (ver `referencia/estandar.md`).
   - **Crónica:** qué taller (nombre propio exacto), qué colegio o aliado, qué hicieron concretamente (conceptos y actividades reales), dónde fue (para la ubicación del post), a quién se etiqueta y **si hay autorización de uso de imagen** para las caras.
   - **Convocatoria:** qué taller se abre y para quién, qué aprenderán (2 o 3 puntos), cómo se inscriben, y fecha solo si está confirmada.
   - **Proyecto institucional:** qué es y qué resuelve, quién lo lideró y quién participó (con sus cuentas si se etiquetan), qué aliados.
   - **Lo que el set tiene por validar** y vas a usar (un correo, un nombre de taller, la cuenta de un aliado): pregúntalo en esta misma tanda («¿sigue siendo este el correo?»). `por_validar()` lo lista.

   En **`MODO=vault`**, antes de preguntar lee `identity/voice-and-tone.md` y la nota de la experiencia (`experiences/<exp>/<exp>.md`): de ahí salen el nombre propio del taller y los conceptos; pregunta solo lo que falte. En **`MODO=autonomo`**, la voz sale de `referencia/voz-crea.md` y `referencia/caption.md`.
2. **Proponer la pieza y el caption en texto y esperar la aprobación.** El estilo y por qué; qué foto o video va en cada lámina y en qué orden; título (con su palabra destacada), bajada, chip, acento, **íconos de la actividad** (`referencia/piezas.md` y los sugeridos por taller en `referencia/crea.md`); qué se anima; y el **caption completo**, escrito como alguien de CREA que estuvo ahí (`referencia/caption.md`: nada de frases hechas ni emojis en serie). Di explícitamente **qué se dedujo y qué se inventó**. Todo dato sin confirmar va como `{validar:…}`. Revisa el caption antes de mostrarlo: guárdalo en un `.txt` y corre `<PYTHON> -m crea_publicaciones.caption <archivo>.txt`. **No generes nada sin aprobación.**
3. **Generar.** Escribe `build_<pieza>.py` con las funciones de `referencia/piezas.md` (y de `referencia/movimiento.md` para lo animado y el reel) y córrelo con `<PYTHON> build_<pieza>.py`. La versión estática termina con `entregar(...)`, que guarda las piezas, exporta los MP4, escribe `caption.txt` y revisa todo. Parte de los ejemplos aprobados de `ejemplos/` (`referencia/galeria.md`), no de cero.
4. **Revisar y regenerar.** Mira **todas** las piezas generadas y lo que hay en `revision/`, y recorre la lista de `referencia/revision-visual.md` (caras y letreros tapados, cortes, contraste sobre video, perfil, franjas de Instagram, tiempos de lectura, último cuadro de lo animado). Lee los avisos del informe y los de `npx hyperframes check`. Corrige el **script** y regenera; nunca edites la imagen a mano. Una pieza que se entrega no lleva avisos.
5. **Entregar.** Corre la versión final con `entregar(..., final=True)`: si quedan datos `{validar:…}`, sale con error. Entrega la lista de archivos, la ubicación y las etiquetas del post, y el **caption en un bloque aparte, listo para copiar y pegar**. Di en qué posición del carrusel va cada MP4 y, si hay estilos o versiones, un zip por estilo. Si alguien de CREA confirmó un dato del set, actualiza `crea.json` (`referencia/crea.md`, «Mantener el set»); si CREA aprobó o rechazó algo nuevo, agrégalo a las decisiones de `referencia/revision-visual.md`.

## Qué leer según la pieza

| Pieza o momento | Lee |
|---|---|
| Cualquiera | `referencia/estandar.md` (formatos, retícula, paleta, Séneca), `referencia/piezas.md` (las funciones) y `referencia/crea.md` (el set de CREA) |
| Elegir o cambiar el estilo | `referencia/estilos.md` |
| Versión animada o reel | `referencia/movimiento.md` |
| Animación en bucle del motor (burbujas, código, parpadeo) | `referencia/animaciones.md` |
| Antes de mostrar o entregar | `referencia/revision-visual.md` |
| Partir de algo aprobado | `referencia/galeria.md` y `ejemplos/` |
| Poner a Séneca o a CREABOT | `referencia/personajes.md` (las poses y cuándo usar cada una) |
| El caption | `referencia/caption.md`; en `MODO=autonomo`, también `referencia/voz-crea.md` |
| Algo falló | `referencia/errores-conocidos.md` |

## Dónde queda cada pieza

En `./<AAAA-MM-DD-tema>/`, dentro de la carpeta donde se abrió Claude Code. Lleva `build_<pieza>.py`, los `.jpg` y `.mp4`, `caption.txt`, `revision/` y un `README.md` corto que cuenta de dónde salió el contenido, **qué falta validar** y cómo se regenera (`<PYTHON> build_<pieza>.py`, con la ruta completa de `<PYTHON>`). Con estilos: `estilos/<estilo>/estatico` y `estilos/<estilo>/animado` (con `proyectos/`, editables con `npx hyperframes preview`). El reel, en `reel/`.

**Las fotos de estudiantes no viajan.** Se quedan en la carpeta de quien hizo el encargo: no se suben a ningún repositorio ni se meten en material que se comparte. En `MODO=vault`, pregunta antes de guardar la carpeta dentro del vault.

## Esqueleto de un script

```python
"""Carrusel del taller Mothbot con el colegio. Regenerar: <PYTHON> build_carrusel_mothbot.py"""
from pathlib import Path

from crea_publicaciones import *  # noqa: F403

AQUI = Path(__file__).resolve().parent
MOTH = taller('Mothbot')            # acento, íconos y hashtags del set de CREA
ESTILO = 'marco'                    # o 'recortes' / 'arcade' (referencia/estilos.md)

laminas = [
    lamina(AQUI / 'fotos' / 'equipo.jpg', 'Un robot que sigue la luz',
           'Armaron un Mothbot con LEDs, resistencias y un sensor de luz.',
           chip='Colegio …', acento=MOTH['acento'], iconos=MOTH['iconos'], estilo=ESTILO),
    lamina(None, 'Voltaje, corriente y resistencia', '…', acento=MOTH['acento'],
           video=AQUI / 'video.mp4', hasta=10, estilo=ESTILO),
]
texto = caption('…', '…', hashtags=['#LaboratorioCREA', *MOTH['hashtags'], '#EducaciónSTEAM'])
raise SystemExit(entregar(AQUI, laminas, texto).codigo)
```

Una publicación suelta es `entregar(AQUI, cronica(...), texto)`; una historia, `entregar(AQUI, historia(...))` (las historias no llevan caption). La versión animada de un carrusel es `carrusel(AQUI / 'animado', [dict(...), ...], estilo=ESTILO)` y el reel, `reel(...)` con `contacto=contacto_reel()` (`referencia/movimiento.md`).

## Reglas que no se negocian

- **No inventar datos.** Cantidades, edades, duraciones, fechas y nombres propios salen de lo que dijo alguien de CREA, del set de CREA (lo confirmado) o del vault; si no, se omiten o van con `{validar:…}`. Un dato «por validar» del set no se publica sin preguntar. Una publicación con un dato inventado es peor que una sin ese dato.
- **Autorización de imagen.** Antes de publicar una foto con menores, alguien de CREA confirma que hay autorización de uso de imagen. Si no la hay, se elige otro encuadre (manos, materiales, el montaje). Esto no lo decide la skill.
- **El taller se nombra siempre con su nombre propio** ("nuestro taller AguaLab"), en la pieza y en el caption.
- **Un título que no cabe es un título largo:** si el informe dice que se encogió o se recortó, **se acorta el texto**; no se achica la letra.
- **Un color de acento por pieza**, de la paleta. Nunca amarillo como color de letra ni como acento. Sin cursiva.
- **Nada tapa una cara, un letrero o un logo de la foto.** Si un chip o un ícono cae encima, se mueve la foto o se quita el chip.
- **La foto no se mueve** en las versiones animadas ni en el reel (decisión de CREA, 2026-10-28).
- **La primera lámina de un carrusel va estática.** Las animaciones en bucle del motor: una por pieza.
- **Las decisiones de CREA** (`referencia/revision-visual.md`) pesan más que el gusto propio.
- **Regenerar, no parchar.**
- Al entregar, di qué se **dedujo o inventó** para que alguien de CREA lo valide.
