# Los personajes: Séneca y CREABOT

Las dos mascotas insignia del laboratorio. Las hojas con todas las poses están en `ejemplos/galeria/personajes-creabot.jpg` y `ejemplos/galeria/personajes-seneca.jpg`: míralas antes de elegir.

Desde un script: `creabot(pose, alto=600, pantalla=None)` y `seneca(pose, alto=600, buzo='T')` devuelven la imagen (con fondo transparente) y `p.img(imagen, x, y)` la pega en la pieza. En el estilo recortes, `lamina(..., sticker='creabot:salta')` o `sticker='seneca:baile-espejo'`. Sobre una pieza sin la Séneca de siempre (`historia(..., mascota=False)`), `p.mascota(x, y, alto, pose=..., buzo=...)`.

## CREABOT

El robot del taller «CREA tu propio videojuego». Está redibujado en vector con las medidas y colores del original, así que sale nítido a cualquier tamaño y cada pose mueve sus partes. **No tiene brazos**, como el original: no se los agregues.

| Pose | Qué expresa | Para qué |
|---|---|---|
| `frente` | El original | Cualquier pieza |
| `feliz` | Ojos cerrados de alegría | Logros, cierre, agradecimiento |
| `guino` | Complicidad | Un dato curioso, una pista |
| `mira-izquierda`, `mira-derecha` | Mira hacia un lado | Ponlo junto al titular **mirando hacia el texto** |
| `sorpresa` | Ojos abiertos y alerta | Un resultado inesperado, «¿sabías que…?» |
| `pensando` | Mira arriba con un «?» | Preguntas, retos, convocatorias |
| `salta` | Salto con sombra | Inicio de taller, energía |
| `camina` | Va en camino | «Vamos para…», visitas, giras |
| `celebra` | Salto con confeti de la marca | Premios, cierres, aniversarios |
| `pantalla` | El pecho es una pantalla | Con `pantalla='icono:<clave>'` muestra un ícono de la lista (por defecto, el bombillo), o un texto corto: `'¡Hola!'`, `'</>'` |
| `cargando` | Barra de carga en el pecho | «Muy pronto», convocatorias que se abren |
| `corazones` | Ojos de corazón | Gracias, aliados, comunidad |
| `dormido` | Ojos cerrados y «z» | Vacaciones, pausas, «volvemos el…» |

## Séneca

La cabra, mascota de la cuenta. Es una ilustración hecha a mano: **no se redibuja en posturas nuevas** (eso es trabajo de ilustración; si CREA tiene los archivos originales o encarga más poses, se agregan a `recursos/mascota/`). Las variantes salen de los tres dibujos originales:

| Pose | Qué es | Para qué |
|---|---|---|
| `saludo` | El original, saludando | Historias, convocatorias, cierres |
| `guino` | El original, guiñando | El parpadeo animado; complicidad |
| `baile` | Bailando, con chaqueta | Celebraciones; el sticker de recortes |
| `saludo-espejo`, `guino-espejo`, `baile-espejo` | Las mismas, mirando al otro lado (el logo del buzo se mantiene legible) | Para que mire hacia el texto o hacia el centro |
| `asoma`, `asoma-espejo` | De la cintura para arriba, saludando | Asomándose desde el borde inferior de una foto o una lámina |
| `cabeza` | La cara en un círculo del color del buzo, con borde blanco | Avatares, firmas, viñetas, destacados del perfil |

**`buzo=`** pinta el buzo del color del taller: `'T'` (el original), `'M'`, `'O'` o `'B'`. Con magenta, el parche CREA lleva un borde blanco para no perderse. El baile lleva chaqueta y se queda turquesa.

## Reglas

- **Una mascota por pieza.** Si salen las dos, es la lámina de cierre o una pieza sobre el laboratorio.
- **CREABOT** para programación, robótica, videojuegos y el estilo arcade. **Séneca** para todo lo demás y para la voz de la cuenta.
- **La mascota mira hacia el contenido** (el titular, la foto), nunca hacia afuera de la pieza: usa `mira-*` o `-espejo`.
- **La pose dice algo**: `celebra` en un cierre de taller común es exagerado; `pensando` en un agradecimiento no tiene sentido.
- Nada de amarillo como color de buzo (no es acento) ni accesorios inventados sobre Séneca.
- **El buzo no va del color del fondo:** sobre una historia naranja, Séneca va en turquesa o azul, no en naranja.
- **`asoma` toca el borde:** se pega al borde inferior de la pieza o de la foto (`y = alto de la pieza - alto`), nunca flotando.
- Las mascotas son marco de la pieza: pueden salir del cuadrado del perfil, pero **no tapan caras, letreros ni logos de la foto**.
