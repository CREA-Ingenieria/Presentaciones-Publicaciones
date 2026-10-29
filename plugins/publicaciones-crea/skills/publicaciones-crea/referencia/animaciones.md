# Animaciones sutiles

La skill no edita video ni reemplaza CapCut. Las animaciones que produce son sutiles, en bucle, y sirven para que una pieza respire.

## Instagram no acepta GIF

Toda animación sale como **MP4**, y eso tiene una consecuencia de fondo:

> Una publicación de video aparece como **reel**, no como foto del grid. Si la pieza debe verse estática en la cuadrícula del perfil, la animación va como **lámina de un carrusel** (que no sea la primera): el grid muestra la primera.

En historias no hay problema: el video es el formato natural. `entregar()` avisa si una publicación suelta va animada o si la primera lámina de un carrusel se mueve.

## Principios

- **Bucle corto:** de 3 a 6 segundos, a 30 fps. El último cuadro empalma con el primero; si la animación termina a medio camino, el bucle da un salto visible.
- **Un solo elemento se mueve.** Si se mueven dos, distrae. `animar()` no deja poner una segunda.
- **Movimiento lento y formas gruesas.** Instagram comprime fuerte: las líneas delgadas y el texto pequeño en movimiento se deshacen.
- **El color del fondo no puede repetirse en la animación.** Un bloque magenta sobre fondo magenta es invisible. La torre evita sola el color de fondo de la pieza.
- **`animar()` va al final del script de la pieza:** el MP4 parte de la pieza tal como está en ese momento.

## Las que hay

| Animación | Uso | Duración | Para qué sirve |
|---|---|---|---|
| Burbujas que suben | `animar(p, 'burbujas', caja=(x0, y0, x1, y1))` | 5 s | Agua, laboratorio, química |
| Torre que se balancea y se cae | `animar(p, 'torre', x=540, y_base=1100)` | 6 s | Estructuras, equilibrio, prueba y error |
| Código que se escribe | `lamina(..., codigo='…')` o `animar(p, 'codigo', texto=…, x=…, y=…, ancho=…)` | 6 s | Programación, lógica, método |
| Séneca que parpadea | `historia(..., animar=True)` o `animar(p, 'parpadeo')` | 5 s | Cualquiera: es el guiño de marca |
| Video del taller | `lamina(None, ..., video=…, desde=…, hasta=…)` | El tramo elegido | Mostrar lo que pasó; no es un bucle, es el video real dentro del marco CREA |

`dur=` cambia la duración. En `'codigo'`, el JPG muestra la línea completa y el MP4 la escribe, la deja un momento con el cursor y la borra.

## Pendientes

Por si hacen falta: el cohete de `recursos/ilustraciones/` cruzando en diagonal, un LED que pulsa y el patrón de doodles derivando despacio. Se agregan en `motor/crea_publicaciones/animacion.py`, con su test de que el bucle empalma.
