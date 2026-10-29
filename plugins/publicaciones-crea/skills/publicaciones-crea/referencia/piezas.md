# Piezas y funciones

Los scripts hacen `from crea_publicaciones import *`. Cada función de pieza devuelve una `Pieza`; `entregar()` la guarda y la revisa. Las rutas de fotos pueden ser `Path` o texto; las HEIC del celular se convierten solas cuando el equipo puede (ver el paso 0).

Colores: `T`, `M`, `O`, `B` como acento; `Y`, `DARK`, `BODY`, `SOFT`, `WHITE` para lo demás. Ver `estandar.md`.

## Las cuatro piezas

### Crónica de taller (4:5)

`cronica(foto, titulo, bajada='', categoria='Taller', aliado=None, acento='#00AFC9', iconos=(), foco=0.5, nombre='cronica')`

Foto en el marco CREA con el chip de `categoria` encima y los `iconos` de la actividad, chip gris con el `aliado`, título en el acento y bajada. La pieza más frecuente. Para un proyecto institucional: `categoria='Proyecto'`.

- `iconos`: de cero a tres claves de la lista de abajo. Si el nombre del aliado es largo y llega hasta los íconos, el chip baja a la fila siguiente y le queda menos espacio a la bajada: usa menos íconos o acorta.

- `titulo`: dos líneas de 96 px como máximo (unos 30 caracteres en total).
- `bajada`: hasta tres líneas, menos si el título ocupa dos y hay aliado: la bajada no puede salirse del cuadrado del perfil. Si no cabe, el informe dice que se encogió: acórtala.

### Historia (9:16)

`historia(foto, titulo, categoria='Taller', aliado=None, acento='#00AFC9', mascota=True, animar=False, nombre='historia')`

Fondo de patrón en el acento, foto, chips blancos, título blanco y Séneca abajo a la derecha. Con `animar=True`, el MP4 hace parpadear a Séneca (5 s en bucle). Las historias no llevan caption.

### Lámina de carrusel (4:5)

`lamina(foto, titulo, bajada='', chip=None, acento='#00AFC9', iconos=(), codigo=None, video=None, desde=0, hasta=None, foco=0.5, ajuste='cubrir', estilo='marco', sticker=None, nivel=None, nombre=None)`

Como la crónica, en el mismo marco CREA y con sus `iconos`, sin aliado.

`estilo` cambia el diseño de la lámina (los datos son los mismos):

- `'marco'` (por defecto): el marco CREA de la crónica.
- `'recortes'`: collage impreso; papel crema, semitono, la foto pegada con cinta, sello de goma con el `chip`, íconos como stickers y, con `sticker='creabot'` o `'seneca'`, un sticker grande junto al título.
- `'arcade'`: pantalla del taller «CREA tu propio videojuego»; barra con `nivel` (el número de lámina), corazones e inventario con los íconos, título pixelado y la bajada en una caja de diálogo con CREABOT, que en los videos se escribe sola.

La línea de `codigo` animada solo va en `'marco'`. Las láminas animadas con HyperFrames y el reel vertical están en `crea_publicaciones.movimiento` (en desarrollo: necesitan Node y Chrome). Se pasan varias en una lista a `entregar()`, que las nombra `carrusel-1`, `carrusel-2`… en ese orden.

- **La lámina 1** es la que se ve en la cuadrícula del perfil: lleva el título principal, la foto más legible en miniatura y **ninguna animación**.
- `codigo`: una línea tipo terminal que el MP4 escribe letra por letra (6 s en bucle); el JPG la muestra completa. Esa lámina se sube como video en su posición del carrusel. Úsala en programación, lógica o para el método ("repetir: preguntar → probar → mejorar").
- `video`: un video del taller corre dentro del recuadro de la foto, con el chip encima; `foto` puede ser `None` y el JPG muestra el primer cuadro. `desde` y `hasta` (segundos) recortan el tramo: úsalos para quitar el arranque o el final en que la cámara baja. El MP4 sale **sin el audio original** (ruido del salón y voces de estudiantes). Mira cuadros de todo el video antes de elegir el tramo.
- `foco`: qué franja vertical queda cuando la foto o el video se recorta (0 arriba, 0,5 al centro, 1 abajo). Ajústalo para que entren las caras o el letrero.
- `ajuste='contener'`: muestra la foto o el video **entero** al centro, con los costados rellenos de su propia versión desenfocada y oscura. Es para lo vertical (un video de celular) que, recortado al recuadro horizontal, perdería a la gente.

### Convocatoria (4:5)

`convocatoria(titulo, puntos, contacto, pregunta=None, nota='No necesitas experiencia previa.', acento='#0051C6', mascota=True, nombre='convocatoria')`

Sin foto: fondo de patrón, pregunta en un chip, título, de 1 a 4 `puntos` con viñetas amarillas, la `nota` y el `contacto` en un chip amarillo. Séneca abajo a la derecha. La nota por defecto va siempre, salvo que el taller sí pida experiencia.

Las viñetas son cuadros de color, no emojis: Montserrat no trae emojis y saldrían como cajas vacías. Los emojis van en el caption.

## El marco CREA y los íconos

La crónica y la lámina de carrusel van en el marco CREA (`motor/crea_publicaciones/marco.py`), hecho con las formas de la marca:

- detrás de la foto, el **bloque del color de acento corrido** arriba a la derecha, con el **punto amarillo** en la esquina, y la **línea oscura en L** abajo a la izquierda, como en el logo;
- los **anillos concéntricos** del logo, saliendo de la esquina inferior izquierda;
- la **línea con puntos turquesa** de la pared del laboratorio, en la franja de abajo;
- una **trama de doodles** muy suave en el color de acento;
- y, montados sobre el borde inferior de la foto, **hasta tres íconos** en círculos de colores CREA (los que no son el acento), que dicen de qué se trató la actividad.

Todo lo decorativo queda fuera de las zonas de texto y del cuadrado del perfil, salvo el bloque y los íconos, que acompañan a la foto. En una lámina con video, el chip, el punto y los íconos van encima de cada cuadro.

**Elegir los íconos.** Que nombren la actividad, no que la adornen: lo que se construyó, el concepto central y la herramienta. Por ejemplo:

| Actividad | Íconos |
|---|---|
| Robótica (Mothbot) | `robot`, `bulb`, `cogs` |
| Agua (AguaLab) | `flask`, `eye`, `recycle` |
| Cohetes | `rocket`, `launch`, `distance` |
| Estructuras, torres, puentes | `truss`, `bridge`, `weight` |
| Programación | `code`, `laptop`, `blocks` |
| Fabricación digital | `print3d`, `layers`, `tools` |
| Agradecimiento o equipo | `users`, `school` |

Los que hay: `adult` `arch` `atom` `badge` `ban` `base` `bell` `blocks` `bottle` `bridge` `bridgew` `bulb` `check` `clock` `code` `cogs` `compass` `cork` `cube` `cycle` `distance` `drafting` `eye` `flask` `gear` `glue` `goggles` `hand` `hands` `laptop` `launch` `layers` `napkin` `palette` `paper` `pasta` `pencil` `pencil2` `pin` `play` `ppt` `print3d` `recycle` `robot` `rocket` `ruler` `school` `scissors` `shapes` `soda` `speed` `suspension` `tablet` `tape` `target` `teoria` `tools` `tree` `triangle` `trophy` `truss` `users` `vinegar` `vr` `wait` `walk` `wash` `weight`.

## Animación

`animar(pieza, tipo, dur=None, fps=30, **kw)`

Agrega una animación en bucle a cualquier pieza. **Va al final**, después de todo lo demás: lo que se dibuje después no sale en el MP4. Una sola por pieza. Ver `animaciones.md`.

| `tipo` | Argumentos | Para qué |
|---|---|---|
| `'burbujas'` | `caja=(x0, y0, x1, y1)`, `n`, `colores` | Agua, laboratorio, química |
| `'torre'` | `x`, `y_base`, `n`, `ancho`, `alto` | Estructuras, equilibrio, prueba y error |
| `'codigo'` | `texto`, `x`, `y`, `ancho`, `tam` | Programación, lógica, método |
| `'parpadeo'` | (ninguno; la pieza tiene que llevar a Séneca) | Cualquiera: es el guiño de marca |

## Caption

`caption(*parrafos, hashtags)`

Une los párrafos con una línea en blanco y cierra con el bloque de hashtags. La fórmula de los párrafos está en `caption.md`. Un párrafo puede tener varias líneas (`'📚 Introducción: …\n🎨 Diseño: …'`).

`revisar_caption(texto)`

Devuelve `(errores, avisos)` con las reglas de `caption.md`. `entregar()` la corre sola. Para revisar un caption suelto: `<PYTHON> -m crea_publicaciones.caption caption.txt`.

## Entrega

`entregar(carpeta, piezas, caption=None, final=False)`

Recibe una pieza o una lista. Guarda en `carpeta`:

- `<nombre>.jpg` por pieza (calidad 95, sin submuestreo de color) y `<nombre>.mp4` si está animada (H.264, yuv420p, `+faststart`, con pista de audio en silencio: sin ella Instagram rechaza el archivo en algunas rutas de subida).
- `caption.txt`.
- `revision/<nombre>-perfil.jpg`: cómo se ve en la cuadrícula del perfil. `revision/<nombre>-zonas.jpg`: la historia con las franjas de la interfaz en rojo.

Imprime el informe y devuelve un resultado con `codigo` (0 listo, 1 con avisos, 2 con errores), `archivos`, `avisos` y `errores`. Termina el script con `raise SystemExit(entregar(...).codigo)`.

Avisa de: texto fuera de la zona segura o de la cuadrícula del perfil; elementos que se superponen o tapan el logo; títulos encogidos o recortados; fotos que se verán borrosas; la primera lámina animada; una publicación animada suelta (sube como **reel**, no como foto del grid); un carrusel de una lámina; publicaciones sin caption; datos `{validar:…}`; y todo lo de `revisar_caption`. Con `final=True`, los `{validar:…}` pasan a ser errores.

## Para algo que las plantillas no cubren

`Pieza(formato=POST, fondo=WHITE, tipo='pieza', nombre=None, acento=T)` es el lienzo, con estos métodos. Úsalo solo cuando ninguna de las cuatro piezas sirva, y sigue las medidas de `estandar.md`.

| Método | Qué hace |
|---|---|
| `.patron(color)` | Fondo de color con los doodles de la plantilla |
| `.fondo(color)` | Fondo de color plano |
| `.foto(ruta, caja, radio)` | Foto que cubre la caja, con esquinas redondeadas |
| `.velo(caja, desde='abajo')` | Degradado oscuro para que el texto se lea sobre la foto |
| `.texto(t, x, y, ancho, tam, peso, color, max_lineas=…)` | Texto con ajuste de línea; devuelve la `y` final |
| `.chip(t, x, y, bg, fg)` | Etiqueta redondeada; devuelve `(x, y, ancho, alto)` |
| `.codigo(texto, x, y, ancho)` | Tarjeta tipo terminal |
| `.img(ruta, x, y, alto=… o ancho=…)` | Una imagen con transparencia |
| `.mascota(x, y, alto, pose)` | Séneca, pose `'saludo'` o `'guino'` |
| `.logo(ancho=150)` | Logo CREA en la esquina que corresponde al formato |
| `.segura()` / `.cuadro_perfil()` | Las zonas, para posicionar a mano |

Pesos de fuente: `'r'` Regular, `'m'` Medium, `'sb'` SemiBold, `'b'` Bold, `'eb'` ExtraBold. Tamaños: `TITULO` (96), `SUB` (48), `CUERPO` (36), `ETIQ` (30). Margen: `MARGEN` (72).
