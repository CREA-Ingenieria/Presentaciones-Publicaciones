# Cambios

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versiones: [semver](https://semver.org/lang/es/).

## [1.3.0] - 2026-10-29

### Agregado
- Tres estilos para las láminas (`lamina(..., estilo=...)`): `marco`, `recortes` (collage impreso con sello, cintas y stickers; `sticker='creabot'|'seneca'`) y `arcade` (pantalla pixelada con `nivel`, inventario y caja de diálogo con CREABOT). Cada estilo dibuja sus piezas como capas (`Pieza.capas`).
- Versiones animadas con HyperFrames (`crea_publicaciones.movimiento`): `carrusel()`, `proyecto()`, `proyecto_capas()`, `render()` y `portada()`. La versión animada termina en el diseño estático; GSAP y Montserrat van dentro de cada proyecto.
- `reel()`: reel vertical gancho → revelación → conceptos → momento → cierre, con una escena final de contacto (tarjetas con íconos, anillos, la línea de la pared, la firma y Séneca).
- El set de CREA (`recursos/crea.json`, `datos.py`): talleres con acento, íconos y hashtags, contacto, biografía, aliados y personajes, cada dato con estado (`confirmado` o `por validar`) y fuente. `taller()`, `contacto_reel()` y `por_validar()`.
- `contraste()` y `tinta()`: el color de letra que se lee sobre un fondo.
- `entorno/revisar.py` revisa Node e imprime `ANIMADO=si|no`: sin Node, solo versiones estáticas.
- Referencias nuevas: `crea.md` (el set), `estilos.md` (cómo elegir), `movimiento.md` (animado y reel), `revision-visual.md` (lista de revisión y decisiones de CREA con fecha) y `galeria.md`.
- Ejemplos aprobados con fotos de demostración: `build_estilos.py` (los tres estilos, estático y animado) y `build_reel.py`, con sus imágenes de referencia en `ejemplos/galeria/`.
- Más poses de las mascotas (`personajes.py`, `referencia/personajes.md`): CREABOT redibujado en vector con 14 poses (feliz, guiño, mira, sorpresa, pensando, salta, camina, celebra, pantalla con ícono o texto, cargando, corazones, dormido) y variantes de Séneca (espejo con el logo legible, asoma, cabeza en círculo y el buzo en el color del taller). `sticker='creabot:<pose>'`, `p.mascota(pose=, buzo=)` y `p.img()` con una imagen ya hecha.
- README visual: banner, piezas, los tres estilos (estático y animado en GIF), el reel, las animaciones en bucle, el flujo de trabajo, la revisión automática, la paleta, los personajes y los 68 íconos. Las imágenes salen del motor con `docs/readme/generar.py`.

### Cambiado
- `SKILL.md` reescrita con un mapa de decisiones (qué pieza, qué estilo, estática o animada, reel) y el flujo apoyado en el set de CREA y en la revisión visual.
- La foto no se mueve en ninguna animación: se quitó el acercamiento (decisión de CREA, 2026-10-28).
- En el reel, con acentos claros (turquesa, naranja), la letra sobre el acento va oscura y la palabra destacada va en amarillo sobre una etiqueta oscura; los títulos sobre blanco van en oscuro si el acento no alcanza 3:1.
- `from crea_publicaciones import *` trae también `taller`, `contacto_reel` y `por_validar`.

## [1.2.0] - 2026-10-28

### Agregado
- Marco CREA para la crónica y la lámina de carrusel (`marco.py`): bloque de color corrido con el punto amarillo y línea en L (del logo), anillos concéntricos, línea con puntos turquesa (de la pared del laboratorio) y trama suave de doodles en el color de acento.
- `iconos=`: hasta tres íconos de la actividad en círculos de colores CREA, montados sobre la foto (también sobre los videos). Trae los 68 íconos de `material-crea` en PNG.
- `revisar_caption()` avisa de lo que suena a texto hecho en serie: frases gastadas, más de cuatro emojis, todos los párrafos terminados en emoji, más de tres exclamaciones.

### Cambiado
- `referencia/caption.md` reescrita: el caption cuenta lo que pasó como alguien que estuvo ahí; la fórmula fija y el "cierre con proyección" se quitaron.
- En la crónica, si el chip del aliado llega hasta los íconos, baja a la fila siguiente.
- Captions de los ejemplos reescritos con la voz nueva.

## [1.1.0] - 2026-10-23

### Agregado
- `lamina(video=…)`: un video del taller corre dentro del recuadro de la foto, con el chip encima, recortado con `desde` y `hasta`, y sin su audio original.
- `foco`, para elegir la franja vertical que queda al recortar una foto o un video.
- `ajuste='contener'`, para mostrar entera una foto o un video vertical sobre su propia versión desenfocada.
- Los cuadros de un video se generan al exportarlo, sin cargarlo entero en memoria.

### Cambiado
- El aviso de baja resolución también vale para los videos.

## [1.0.0] - 2026-10-23

### Agregado
- Primera versión de `publicaciones-crea`, a partir de la parte de publicaciones del Kit CREA (`post_lib.py`, los cuatro `build_*.py` y la guía de publicaciones).
- Motor instalable (`crea-publicaciones`) con sus recursos adentro: Montserrat en cinco pesos, logo, patrón, Séneca y logos de aliados.
- Las cuatro piezas como funciones: `cronica()`, `historia()`, `lamina()` y `convocatoria()`.
- `animar()` con burbujas, torre, código y parpadeo de Séneca; exporta MP4 listo para Instagram.
- `caption()` y `revisar_caption()`: la fórmula y las reglas de voz y hashtags de la cuenta.
- `entregar()`: guarda JPG, MP4 y `caption.txt`, genera `revision/` (vista del perfil y zonas de la historia) y revisa todo junto; con `final=True`, los `{validar:…}` son error.
- Revisión del entorno (`entorno/revisar.py`): entorno virtual, motor, render de prueba y soporte de fotos HEIC.

### Cambiado respecto al kit
- El motor usa siempre su propia Montserrat, no la del sistema: la pieza sale igual en cualquier equipo.
- Las fotos HEIC también se abren en Mac (con `sips`), no solo en Windows.
- Un título o una bajada que se encoge más de un 15 % o se recorta genera un aviso, en vez de achicarse en silencio.
- La bajada calcula cuántas líneas caben antes del borde del cuadrado del perfil.
- Avisos nuevos: primera lámina animada, publicación animada que subiría como reel, fotos que se verán borrosas y datos sin validar.
