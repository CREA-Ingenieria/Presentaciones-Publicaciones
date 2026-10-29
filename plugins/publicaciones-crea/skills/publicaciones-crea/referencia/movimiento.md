# Movimiento: láminas animadas y reel (HyperFrames)

Las versiones animadas se escriben como HTML y se renderizan a video con **HyperFrames** (`npx hyperframes`). Lo hace `crea_publicaciones.movimiento`; no escribas el HTML a mano. Las animaciones en bucle del motor (burbujas, torre, código, parpadeo) son otra cosa: `animaciones.md`.

## Antes de empezar

- **Node.js** (probado con la 22) y acceso a **npm**: la primera vez, `npx` descarga HyperFrames y el motor descarga GSAP con `npm pack`. El paso 0 revisa que Node esté; si no, solo se pueden hacer versiones estáticas.
- **Chrome o Chromium**: HyperFrames lo encuentra solo.
- **Montserrat va dentro de cada proyecto** y **GSAP se sirve desde el proyecto**, no desde un CDN: en redes cerradas el CDN falla y el render se bloquea.
- Un render de una lámina de 6 s tarda unos 30 s; uno de 13 s, un minuto. Avisa antes de lanzar muchos.

## Funciones

`carrusel(carpeta, laminas, acento='#00AFC9', estilo='marco', cache=None)`

Renderiza cada lámina (diccionarios con los argumentos de `lamina`) a `carpeta/carrusel-N.mp4`, saca su último cuadro como `carrusel-N.jpg` y deja los proyectos editables en `carpeta/proyectos/`. Es la forma normal de hacer la versión animada de un estilo.

`proyecto(carpeta, *, titulo, bajada='', chip=None, acento='#00AFC9', iconos=(), foto=None, video=None, desde=0, hasta=None, foco=0.5, ajuste='cubrir', cache=None)`

El proyecto HyperFrames de una lámina en estilo marco (tiene su propio HTML).

`proyecto_capas(carpeta, pieza, estilo, video=None, desde=0, hasta=None, ajuste='cubrir', cache=None)`

El proyecto de una lámina de recortes o arcade a partir de `pieza.capas`: cada pieza del diseño es una imagen en su posición y su **rol** decide cómo entra. Por eso la versión animada es exactamente el diseño estático.

`reel(carpeta, *, gancho, revelacion, conceptos, momento, cierre, contacto=None, acento='#00AFC9', cache=None)`

El reel vertical (ver abajo).

`render(carpeta, salida)` renderiza un proyecto y le agrega la pista de audio en silencio que Instagram pide. `portada(mp4, salida)` saca el último cuadro.

## Cómo entra cada estilo

| Estilo | Entrada |
|---|---|
| marco | El bloque se desliza desde la derecha; la foto se revela con un telón; los anillos y la línea en L se dibujan; el punto amarillo rebota; el chip entra desde un desenfoque; los íconos con resorte; el título palabra por palabra; el circuito se dibuja; el logo sube |
| recortes | La copia cae girada y se pega; aparece su sombra; las cintas se estiran; el sello golpea (de 2,6× a 1× en 0,12 s, con rebote); los íconos saltan; el rayo y la línea se trazan; las palabras del título caen una por una; la nota entra deslizándose; el sticker salta; el logo cierra |
| arcade | Todo en **pasos** (`steps()`), nada suave: la ventana aparece en escalones, la foto «enciende» de arriba abajo, la barra baja, los corazones y los objetos salen uno a uno, las palabras del título aparecen de a una, la caja de diálogo se abre y su texto se escribe línea por línea, letra por letra, con el cursor parpadeando al final |

## El reel

Vertical (1080 × 1920), escenas de 3 s con la estructura de `/brag`: **gancho → revelación → conceptos → momento → cierre**, y una escena final de **contacto** de 4,5 s. Un reel se ve fuera del perfil: **siempre lleva el contacto** (`contacto=contacto_reel()` del set de CREA).

| Escena | Qué lleva | Transición que la cierra |
|---|---|---|
| Gancho | El video más vivo, a pantalla completa desde el cuadro 0, y el título | El color del acento sube y barre |
| Revelación | La foto principal en el marco, con quién fue y dónde | El ícono del bombillo crece hasta llenar el cuadro |
| Conceptos | Fondo amarillo: «Hablamos de…» y una palabra que gira como tragamonedas (los conceptos reales del taller) | Barrido rápido hacia arriba |
| Momento | Un tramo del otro video, con su título | Iris desde el punto amarillo |
| Cierre | La foto del equipo o del aliado y el agradecimiento | El color del acento sube |
| Contacto | Titular de la biografía con una palabra en amarillo, tarjetas de contacto con íconos, anillos, la línea de la pared, la firma del laboratorio y Séneca saludando | — |

Texto solo en la **banda segura** del reel (de 168 a 1330 px de alto); debajo, solo decoración. Nada de texto bajo la columna de botones de la derecha.

- **Bajadas cortas:** cada escena dura 3 s, así que una bajada no pasa de unas 6 palabras («Cada equipo cargó su cercha»). Con 11, `hyperframes check` avisa `line_unread`.
- **Letra sobre el acento:** con azul o magenta va blanca; con turquesa o naranja (no llegan a 3:1 con blanco) el motor la pone oscura y la palabra destacada va en amarillo sobre una etiqueta oscura. Lo decide `tinta()`; no lo cambies a mano.

## Reglas de movimiento

De la skill hyperframes (`references/motion.md`) y de lo que CREA aprobó y rechazó:

- **Llegar despacio, irse limpio:** llegadas con cola larga (`expo.out`, `power4.out`), salidas un 40 % más cortas.
- **Lo que aterriza se queda quieto.** Nada de títulos que respiran, flotan o siguen creciendo.
- **La foto no se mueve.** Ni acercamiento ni paneo sobre fotos (decisión de CREA, 2026-10-28). Los videos sí corren.
- **Cada transición tiene una causa en pantalla** (un color que sube, un ícono que crece, un punto que se abre). Tres a cinco tipos por reel; ninguna escena entra igual que la anterior.
- **Una palabra destacada** por titular, en el color que carga el sentido.
- **La última línea se queda al menos 2 s.** Una línea se lee en 0,5 s más 0,3 s por palabra.
- **El cierre y el contacto llevan el mismo cuidado que el resto** (decisión de CREA, 2026-10-29: una escena final de texto plano sobre color se rechazó por «muy simple»).

## Revisar antes de entregar

1. `npx hyperframes check --json` dentro de cada proyecto: **ningún error**. Los avisos que importan: contraste (texto a menos de 3:1), `line_unread` (una línea que no alcanza a leerse), `text_below_floor` (letra de menos de 28 px). `film_silent` se acepta: la música se elige al subir el reel a Instagram. `nested_structure_needs_subcomposition` también.
2. Saca cuadros del MP4 (con el ffmpeg de `imageio_ffmpeg`) al inicio, a mitad de cada entrada y al final, y míralos. El último cuadro de cada lámina tiene que ser igual a su versión estática.
3. Entrega, además de las láminas, un video corrido con todas para verlas de una vez, y los proyectos (`proyectos/`) por si alguien quiere editarlos (`npx hyperframes preview`).
