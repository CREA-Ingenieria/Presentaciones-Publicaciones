# Los estilos

Las láminas de carrusel (`lamina(..., estilo=...)`) tienen tres estilos. Los datos son los mismos en los tres; cambia el diseño. Cada estilo tiene **versión estática** (JPG y MP4 con el motor) y **versión animada** (HyperFrames, ver `movimiento.md`). La crónica suelta usa el marco; la historia y la convocatoria tienen su propio diseño (`piezas.md`).

## Cómo elegir

| Si la publicación… | Estilo | Por qué |
|---|---|---|
| Es la crónica de siempre, para el feed, con aliado o institución | **marco** | El más sobrio y el más reconocible: la cara diaria de la cuenta |
| Cuenta un taller lleno de material, manos y piezas; quiere sentirse hecha a mano | **recortes** | El collage vuelve la foto un objeto pegado en la bitácora del taller |
| Es de programación, videojuegos, robótica, o para un público joven | **arcade** | Habla el idioma del taller «CREA tu propio videojuego»; es el más juguetón |
| No es claro | Propón **marco** por defecto y ofrece una variante en otro estilo | Que CREA elija viéndolos |

Un carrusel va **entero en un estilo**. No se mezclan estilos entre láminas.

Cuando la persona pide «variantes» o «otros estilos», entrega los tres (estático y animado), cada uno en su carpeta (`estilos/<estilo>/estatico` y `.../animado`) con un zip por estilo y un video corrido de las láminas animadas para compararlas.

## Marco

**Qué lo define:** las formas del logo CREA. El bloque del acento corrido detrás de la foto, el punto amarillo en su esquina, la línea en L, los anillos concéntricos, la línea con puntos turquesa de la pared del laboratorio, la trama de doodles muy suave y hasta tres íconos de la actividad en círculos de color sobre el borde de la foto.

**Cuida:**
- Los íconos nombran la actividad (lo que se construyó, el concepto, la herramienta), no la adornan. Ver `crea.md` por taller.
- El chip va sobre la foto, arriba a la izquierda: si cae sobre un letrero, una cara o un logo de la foto, **se quita** (decisión de CREA, 2026-10-23: la lámina de agradecimiento va sin chip porque tapaba el letrero CREA).
- Si el nombre del aliado choca con los íconos, el chip baja solo y le queda menos espacio a la bajada: usa menos íconos o acorta.

## Recortes

**Qué lo define:** un collage impreso. Papel crema con grano; semitono en las tintas de la marca (el acento arriba a la derecha, magenta abajo a la izquierda); la foto como copia impresa con margen blanco, girada 2,5° y pegada con dos cintas; el `chip` como **sello de goma**; los íconos como **stickers** troquelados; el titular con la **sombra corrida** de una impresión mal registrada; la bajada en una nota de papel; el rayo dibujado y la línea de la pared.

**Parámetro propio:** `sticker='creabot'` o `'seneca'` pone un sticker grande junto al título; también acepta una pose (`'creabot:salta'`, `'seneca:baile-espejo'`, ver `personajes.md`). Úsalo en la primera lámina (CREABOT en robótica o programación) y en la de cierre o agradecimiento (Séneca). No en todas: si todas lo llevan, deja de decir algo.

**Cuida:**
- El sello no puede salirse del margen ni del cuadrado del perfil (el motor lo vigila).
- Una foto vertical en la copia horizontal pierde a la gente: `ajuste='contener'`.

## Arcade

**Qué lo define:** una pantalla del taller «CREA tu propio videojuego». Todo lo que no es la foto vive en un lienzo de 270 × 338 píxeles ampliado ×4 sin suavizar; los degradados son tramado (Bayer), nunca mezclas; cielo nocturno con estrellas y cerros; barra de arriba con **NIVEL n**, corazones e inventario (los íconos como objetos); la foto entera, sin pixelar, en una ventana de bordes en escalera; el título en letras de píxel con degradado amarillo-naranja; la bajada en una **caja de diálogo** con el retrato de CREABOT.

**Parámetro propio:** `nivel=` es el número de la lámina (1, 2, 3…). Sin él, la barra muestra el `chip`.

**Cuida:**
- Nada de personajes, fondos, corazones ni sonidos de juegos comerciales: todo sale del código o de CREA (CREABOT).
- La caja de diálogo admite tres líneas: si el informe dice que no cabe, acorta la bajada.
- La barra de arriba es marco (como el logo): puede quedar fuera de la cuadrícula del perfil.

## Lo común a los tres

- **La foto no se mueve.** Ni en la versión animada: lo que se anima es el diseño (decisión de CREA, 2026-10-28: un acercamiento sobre una foto en un marco pequeño se ve mal).
- Un acento por carrusel, el del taller (`crea.md`).
- La primera lámina va estática en el carrusel (JPG): si es un video, Instagram muestra el post como reel en el perfil.
- La versión animada termina exactamente en el diseño estático: el último cuadro es la lámina.
