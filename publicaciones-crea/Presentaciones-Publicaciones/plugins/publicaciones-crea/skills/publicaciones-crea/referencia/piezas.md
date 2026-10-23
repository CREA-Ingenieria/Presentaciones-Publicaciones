# Piezas y funciones

Los scripts hacen `from crea_publicaciones import *`. Cada función de pieza devuelve una `Pieza`; `entregar()` la guarda y la revisa. Las rutas de fotos pueden ser `Path` o texto; las HEIC del celular se convierten solas cuando el equipo puede (ver el paso 0).

Colores: `T`, `M`, `O`, `B` como acento; `Y`, `DARK`, `BODY`, `SOFT`, `WHITE` para lo demás. Ver `estandar.md`.

## Las cuatro piezas

### Crónica de taller (4:5)

`cronica(foto, titulo, bajada='', categoria='Taller', aliado=None, acento='#00AFC9', nombre='cronica')`

Foto arriba con el chip de `categoria` encima, chip gris con el `aliado`, título en el acento y bajada. La pieza más frecuente. Para un proyecto institucional: `categoria='Proyecto'`.

- `titulo`: dos líneas de 96 px como máximo (unos 30 caracteres en total).
- `bajada`: hasta tres líneas, menos si el título ocupa dos y hay aliado: la bajada no puede salirse del cuadrado del perfil. Si no cabe, el informe dice que se encogió: acórtala.

### Historia (9:16)

`historia(foto, titulo, categoria='Taller', aliado=None, acento='#00AFC9', mascota=True, animar=False, nombre='historia')`

Fondo de patrón en el acento, foto, chips blancos, título blanco y Séneca abajo a la derecha. Con `animar=True`, el MP4 hace parpadear a Séneca (5 s en bucle). Las historias no llevan caption.

### Lámina de carrusel (4:5)

`lamina(foto, titulo, bajada='', chip=None, acento='#00AFC9', codigo=None, nombre=None)`

Como la crónica, sin aliado. Se pasan varias en una lista a `entregar()`, que las nombra `carrusel-1`, `carrusel-2`… en ese orden.

- **La lámina 1** es la que se ve en la cuadrícula del perfil: lleva el título principal, la foto más legible en miniatura y **ninguna animación**.
- `codigo`: una línea tipo terminal que el MP4 escribe letra por letra (6 s en bucle); el JPG la muestra completa. Esa lámina se sube como video en su posición del carrusel. Úsala en programación, lógica o para el método ("repetir: preguntar → probar → mejorar").

### Convocatoria (4:5)

`convocatoria(titulo, puntos, contacto, pregunta=None, nota='No necesitas experiencia previa.', acento='#0051C6', mascota=True, nombre='convocatoria')`

Sin foto: fondo de patrón, pregunta en un chip, título, de 1 a 4 `puntos` con viñetas amarillas, la `nota` y el `contacto` en un chip amarillo. Séneca abajo a la derecha. La nota por defecto va siempre, salvo que el taller sí pida experiencia.

Las viñetas son cuadros de color, no emojis: Montserrat no trae emojis y saldrían como cajas vacías. Los emojis van en el caption.

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
