# Estándar CREA en Instagram

Todo lo que aquí se dice sobre color, tipografía y márgenes **deriva** del estándar de las presentaciones de CREA (`material-crea`). No se inventa nada nuevo. Se escribió a partir del análisis de la cuenta **@crea_uniandes** (feed, reels y destacados, septiembre de 2026).

## Los tres tipos de contenido

Identificar cuál es lo primero que hay que resolver: cada uno se escribe distinto.

| Tipo | Cuándo | Protagonista | Pieza |
|---|---|---|---|
| **Crónica de taller** | Ya pasó un taller y hay fotos | Los estudiantes que vinieron | `cronica()`, o un carrusel de `lamina()` |
| **Convocatoria** | Se abren inscripciones a un taller | Quien lee: se le habla de tú | `convocatoria()` |
| **Proyecto institucional** | Un logro, un desarrollo, una alianza | El proyecto y su equipo | `cronica()` con `categoria='Proyecto'` |

La crónica es, de lejos, la más frecuente. Una **historia** (`historia()`) sirve para cualquiera de los tres: avisos, reposteos, recordatorios.

## Formatos

| Formato | Medida | Constante | Cuándo |
|---|---|---|---|
| **Publicación** | 1080 × 1350 (4:5) | `POST` | El principal. Ocupa más pantalla en el feed |
| **Cuadrado** | 1080 × 1080 (1:1) | `CUAD` | Cuando la foto solo funciona cuadrada (solo con `Pieza`, no hay plantilla) |
| **Historia** | 1080 × 1920 (9:16) | `STORY` | Avisos, reposteos, recordatorios |

**El 4:5 se recorta a cuadrado en la cuadrícula del perfil.** Pierde 135 px arriba y 135 abajo. Por eso el título, la bajada y los chips viven entre `y=135` y `y=1215`; solo el logo puede quedar por fuera. El motor lo verifica y `revision/<pieza>-perfil.jpg` muestra cómo queda. En un carrusel solo cuenta la primera lámina.

## Retícula y márgenes

Las presentaciones trabajan en 960 × 540 pt con margen de 66 pt: el **6,9 % del ancho**. Sobre 1080 px eso da 74 px, que en una rejilla de 12 queda en **72 px**.

| | Presentación | Publicación |
|---|---|---|
| Margen lateral | 66 pt | **72 px** |
| Margen inferior | ≥ 30 pt | **≥ 72 px** |
| Rejilla | — | **12 px** |

**Las franjas que tapa la interfaz de Instagram** (historias y reels): 250 px arriba (foto de perfil, nombre), 320 abajo (caja de respuesta) y 180 a la derecha (botones). Ahí **no va texto**; una foto o Séneca sí pueden entrar. `revision/<pieza>-zonas.jpg` las pinta en rojo.

**La zona del logo cambia de esquina.** En la publicación va abajo a la derecha. En la historia eso queda bajo los botones de Instagram, así que va abajo a la izquierda. `Pieza.logo()` lo resuelve solo.

## Paleta

Los colores de la plantilla de CREA. **No se inventan colores nuevos**, y en particular no se usan los verdes y naranjas que aparecieron en algunas piezas sueltas de la cuenta.

| Color | Hex | Constante | Uso |
|---|---|---|---|
| Turquesa | `00AFC9` | `T` | Color dominante, acento por defecto |
| Magenta | `D32985` | `M` | Segundo acento |
| Naranja | `E9A222` | `O` | Tercer acento |
| Azul | `0051C6` | `B` | Cuarto acento (tecnología, robótica) |
| Amarillo | `EBE212` | `Y` | Etiquetas y viñetas; **siempre con texto oscuro**, nunca como acento |
| Texto oscuro | `1E2A3A` | `DARK` | Títulos sobre fondo claro |
| Texto cuerpo | `3C3C4A` | `BODY` | Párrafos |
| Gris suave | `EEF1F5` | `SOFT` | Fondo de chips informativos |
| Blanco | `FFFFFF` | `WHITE` | Fondo de pieza y de chips sobre color |

**Un color de acento por pieza.** A diferencia de una diapositiva, donde los colores rotan entre tarjetas, aquí toda la publicación se compromete con uno. Reparto por taller, para que el feed tenga ritmo:

| Taller | Acento |
|---|---|
| AguaLab | Turquesa (`T`) |
| Mothbot / robótica | Azul (`B`) |
| Ciencia de Cohetes | Naranja (`O`) |
| Diseñadores del Futuro | Magenta (`M`) |
| Programación web | Turquesa (`T`) |

Es una convención, no una regla heredada: si CREA prefiere otra, se cambia aquí.

## Tipografía

Todo en **Montserrat**, sin cursivas. El motor usa siempre la Montserrat que trae adentro (cinco pesos), no la del sistema: así la pieza mide y se ve igual en cualquier equipo.

La escala conserva la proporción título:cuerpo de las diapositivas, **2,8 : 1** (36 : 13 pt allá, 96 : 36 px acá).

| Elemento | Tamaño | Peso | Color |
|---|---|---|---|
| Título de publicación | 96 px | Bold | Acento, o blanco sobre color |
| Título de historia | 84 px | Bold | Blanco |
| Subtítulo | 48 px | SemiBold | Acento o cuerpo |
| Bajada / cuerpo | 36 px | Regular | Texto cuerpo |
| Chip | 30 px | SemiBold | Blanco sobre acento, oscuro sobre gris |
| Número de sección | 288 px | ExtraBold | Acento |

**Los títulos caben en dos líneas sin encogerse.** El motor baja el tamaño si hace falta para que quepan, pero avisa si baja más de un 15 % o si tuvo que recortar: eso significa que el texto es largo y hay que acortarlo. Como guía, caben unos 16 caracteres por línea en el título de una publicación y unos 15 en el de una historia: un título de dos líneas tiene, como mucho, unos 30 caracteres.

## Imágenes

- **Rectángulo redondeado**, radio 64 px sobre 936 de ancho: el 0,07 de las presentaciones.
- La foto **cubre** su caja y se centra. Nunca se estira. Si es tan pequeña que tendría que ampliarse más de 1,5 veces, el motor avisa: se verá borrosa. Lo que pasa por WhatsApp suele llegar así: pide el original.
- Si recortar pierde lo importante (una foto o un video vertical en el recuadro horizontal), se elige la franja con `foco` o se muestra entera con `ajuste='contener'`.
- **Videos del taller:** van en una lámina de carrusel (`lamina(video=…)`), recortados a lo que se entiende y **sin su audio**.
- Si el texto va encima de la foto, lleva **velo** (`Pieza.velo()`): un degradado del oscuro de marca. Las plantillas no ponen texto sobre la foto salvo el chip de categoría.
- Foto real del taller primero, siempre.
- **Caras de menores:** solo con autorización de uso de imagen confirmada por CREA. Si no la hay, otro encuadre: manos, materiales, el montaje.

## El marco CREA

Las publicaciones con foto (crónica y carrusel) no van sobre blanco plano: van en un marco hecho con las formas de la marca, para que se reconozcan en el feed antes de leerlas. Sus piezas salen del logo (el bloque de color corrido, el punto amarillo, la línea en L, los anillos concéntricos) y de la pared del laboratorio (la línea con puntos turquesa). Los íconos de la actividad van en círculos de los colores que no son el acento, así la pieza tiene los cinco colores sin perder su color principal. El detalle está en `piezas.md`.

## Séneca

La cabra es el único elemento de marca que la cuenta ya usa de forma sistemática: los destacados del perfil son Séneca en poses distintas sobre cuadrados de color plano.

Hay dos poses en alta resolución, extraídas de la plantilla de presentaciones: `saludo` (ojos abiertos) y `guino`. Se diferencian **solo en los ojos**, así que son un par de parpadeo listo para animar.

- **Sí** en historias, convocatorias y piezas de fondo plano, abajo a la derecha, alto 380 a 520 px.
- **No** encima de una foto de taller: compite con las personas de la foto.
- **No** junto al logo grande si ya se ve el logo del buzo: es redundante.

Las otras poses (fútbol, leyendo, recostada) solo existen a 150 × 150 px en las portadas de destacados. Para usarlas hay que pedir el arte original a quien las hizo.
