# Revisión visual

El informe de `entregar` revisa lo que se puede medir: textos que se encogen, contraste, el cuadrado del perfil, las franjas de la interfaz. Lo demás se revisa **mirando**. Antes de mostrar cualquier pieza, abre cada JPG, lo que hay en `revision/` y, si hay video, cuadros sacados del MP4. Recorre esta lista. Si algo falla, se corrige el script y se regenera.

## La foto

- [ ] **Ninguna cara, letrero ni logo de la foto queda debajo de un chip, un ícono, el sello o la nota.** Si pasa, mueve la foto (`foco`), quita el chip o usa menos íconos. Un letrero de CREA o del aliado tapado es el error más visible.
- [ ] **Nadie queda cortado por la frente o por el mentón.** `foco` (0 arriba, 1 abajo) decide qué parte de una foto vertical se queda. En recortes, una foto vertical va con `ajuste='contener'`.
- [ ] **La foto que abre el carrusel se lee en miniatura:** una acción clara (manos en el montaje, un robot andando, alguien explicando), no un grupo de espaldas.
- [ ] **Las fotos de WhatsApp vienen comprimidas.** Si se ve el ruido o los bloques, úsala en un marco más pequeño o elige otra. Pide el original si es la foto principal.
- [ ] Las caras de menores solo con autorización confirmada (`SKILL.md`, reglas).

## El texto

- [ ] El titular se lee de un vistazo: 2 a 6 palabras, una idea. Si el informe dice que se encogió o que no cabe, **se acorta**.
- [ ] Una sola palabra destacada por titular, y es la que carga el sentido.
- [ ] La bajada dice qué se hizo, con los conceptos reales del taller (`crea.md`), no adjetivos.
- [ ] Nada de amarillo como color de letra, ni cursiva.
- [ ] Ningún `{validar:…}` en la versión que se entrega.

## El perfil y las franjas de Instagram

- [ ] En `revision/`, la vista del perfil (el 4:5 recortado a cuadrado: de y = 135 a 1215) muestra el titular entero en la primera lámina. Lo que se sale es decoración (el logo, la barra de arcade).
- [ ] En historias: nada importante en los 250 px de arriba, los 320 de abajo ni los 180 de la derecha (en rojo en `revision/`).
- [ ] En el reel: el texto vive entre 168 y 1330 px de alto. Debajo, solo decoración.

## El movimiento

- [ ] **La foto no se mueve:** ni acercamiento ni paneo (ver las decisiones).
- [ ] El último cuadro de cada lámina animada es la lámina estática. Compara `carrusel-N.jpg` con el JPG del estilo estático.
- [ ] Lo que aterriza se queda quieto: no hay títulos que respiran ni íconos que flotan.
- [ ] Ninguna escena entra igual que la anterior, y cada transición tiene una causa en pantalla.
- [ ] Sobre video, el texto tiene contraste (velo o caja oscura): mira un cuadro en el momento más claro del video, no solo el primero.
- [ ] Cada línea alcanza a leerse (0,5 s + 0,3 s por palabra) y la última se queda al menos 2 s.
- [ ] `npx hyperframes check --json` sin errores, y los avisos de contraste, `line_unread` y `text_below_floor` resueltos (`movimiento.md`).

## El carrusel completo

- [ ] Un estilo y un acento para todas las láminas.
- [ ] La primera lámina es un JPG. Los videos van de la segunda en adelante.
- [ ] El orden cuenta algo: qué se hizo → cómo se hizo → quién estuvo → gracias.
- [ ] Un reel siempre termina con la escena de contacto.

## Decisiones de CREA

Lo que CREA aprobó o rechazó en encargos reales. Pesan más que el gusto de quien arma la pieza. Cuando CREA decide algo nuevo, se agrega aquí con la fecha y el encargo.

| Fecha | Encargo | Decisión |
|---|---|---|
| 2026-10-23 | Mothbot · Garcés Navas IED | La lámina de agradecimiento va **sin chip**: tapaba el letrero CREA de la foto. Un chip nunca va sobre un letrero, una cara o un logo |
| 2026-10-28 | Mothbot · Garcés Navas IED | **Nada de acercamiento ni paneo sobre las fotos**, en ningún estilo: «se ve muy mal cuando el marco es pequeño». Se anima el diseño, no la foto |
| 2026-10-28 | Mothbot · Garcés Navas IED | El caption **no puede sonar a IA**: nada de frases hechas, emojis al final de cada párrafo ni cadenas de «¡». Se escribe como alguien que estuvo ahí (`caption.md`) |
| 2026-10-28 | Mothbot · Garcés Navas IED | Más elementos de la marca y de la actividad en la pieza: formas del logo, íconos de lo que se construyó, colores insignia |
| 2026-10-28 | Mothbot · Garcés Navas IED | **Cada estilo tiene versión estática y animada**, y la animada termina en el diseño estático |
| 2026-10-29 | Mothbot · Garcés Navas IED (reel) | **El reel termina con el contacto del laboratorio** |
| 2026-10-29 | Mothbot · Garcés Navas IED (reel) | La escena de contacto **lleva el mismo diseño que el resto**: una versión de texto plano sobre color se rechazó por «muy simple». Lleva titular con palabra destacada, tarjetas con íconos, anillos, la línea de la pared, la firma y Séneca |
| — | Regla de Instagram | La primera lámina de un carrusel va estática: si es un video, el perfil muestra el post como reel |
