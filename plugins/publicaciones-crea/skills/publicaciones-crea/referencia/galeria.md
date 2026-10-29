# Galería de ejemplos aprobados

Parte de aquí, no de cero. Cada ejemplo usa las fotos de demostración de `ejemplos/fotos/` (estructuras, sin personas) y sigue el mismo patrón que se aprobó en el encargo Mothbot · Colegio Garcés Navas IED (octubre de 2026). Ese encargo no está en el repositorio porque tiene fotos de estudiantes; lo que se aprendió de él está en las decisiones de `revision-visual.md`.

Para verlos, corre el script con `<PYTHON>` y abre lo que queda en `ejemplos/salida/`. Las imágenes de `ejemplos/galeria/` son la referencia de cómo tiene que verse.

## Los tres estilos: `ejemplos/build_estilos.py`

Un carrusel de 3 láminas (qué se hizo → el concepto → gracias) con acento naranja, en los tres estilos. `datos(estilo)` muestra cómo se adapta la misma lista de láminas a cada estilo: el sticker solo en recortes, el `nivel` solo en arcade. Con `--animado` hace también las versiones animadas.

| Estilo | Referencia |
|---|---|
| marco | `ejemplos/galeria/marco.jpg` |
| recortes | `ejemplos/galeria/recortes.jpg` |
| arcade | `ejemplos/galeria/arcade.jpg` |

**Por qué funciona:**

- **Los titulares son cortos y concretos:** «Un puente de palitos», «Triángulos, no cuadrados». Dicen la cosa, no la adornan. Ninguno se encoge.
- **Los íconos nombran la actividad:** cercha y pesa para estructuras; personas y colegio en la lámina de gracias. No hay íconos de relleno.
- **La bajada dice qué hicieron** («Cada equipo diseñó una cercha y la cargó hasta que cedió») y lleva un concepto real («El triángulo no se deforma»).
- **Un acento para todo el carrusel**; los íconos toman los otros colores de la marca.
- **Los stickers marcan el principio y el final** en recortes (CREABOT abre, Séneca despide). Las láminas del medio no llevan.
- **La foto vertical** va con `ajuste='contener'` en la copia horizontal del collage, para no cortar la estructura.
- **El caption** pasa el revisor sin avisos: arranca con una escena concreta, nombra los conceptos y cierra con un dato del taller («El que más aguantó no fue el más alto»), no con una frase motivacional. El revisor marcó «llenos de» en un primer borrador, y se cambió.

## El reel: `ejemplos/build_reel.py`

Gancho → revelación → conceptos → momento → cierre → contacto, en 19,5 s, con acento naranja. Referencia: `ejemplos/galeria/reel.jpg` (un cuadro por escena).

**Por qué funciona:**

- **El gancho es una pregunta** que el resto del reel contesta.
- **La bajada de la revelación tiene 5 palabras:** la escena dura 3 s y una línea necesita 0,5 s más 0,3 s por palabra. Con 11 palabras, `hyperframes check` avisó `line_unread`.
- **Los conceptos son los del taller**, no palabras bonitas: compresión, tensión, triángulos, cargas.
- **El contacto sale del set** (`contacto_reel()`): la biografía como titular, «colegio» destacado, y solo los datos confirmados.
- **Con un acento claro (turquesa o naranja), la letra sobre el acento va oscura** y la palabra destacada va en amarillo sobre una etiqueta oscura. El motor lo decide solo con `tinta()`; con azul o magenta, la letra va blanca.
- En un encargo real, el gancho y el momento son videos del taller. Aquí, a falta de video de demostración, `video_demo()` hace un clip con una franja de luz sobre la foto quieta.

## Las piezas sueltas

| Script | Qué muestra |
|---|---|
| `ejemplos/build_cronica.py` | Publicación suelta en marco, con aliado |
| `ejemplos/build_carrusel.py` | Carrusel con la lámina 2 animada en bucle (código que se escribe) |
| `ejemplos/build_historia.py` | Historia con Séneca |
| `ejemplos/build_convocatoria.py` | Convocatoria con puntos e inscripción |

## Agregar un ejemplo

Cuando CREA aprueba un encargo con algo nuevo (un tipo de pieza, una forma de usar un estilo), rehazlo aquí con las fotos de demostración, agrega su imagen a `ejemplos/galeria/` y escribe el «por qué funciona». Las fotos de estudiantes no entran al repositorio.
