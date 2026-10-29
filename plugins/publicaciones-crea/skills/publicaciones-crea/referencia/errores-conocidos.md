# Errores conocidos

| Problema | Causa | Solución |
|---|---|---|
| "No se puede abrir … HEIC" | Pillow no lee HEIC; cada sistema lo resuelve distinto | Windows usa su decodificador y Mac usa `sips`, sin instalar nada. En otro sistema, pide la foto en JPG o instala `pillow-heif` en el entorno |
| "texto encogido de … a … px" o "texto recortado" | El texto es más largo que su espacio | Acórtalo. No se reduce la letra |
| "se pierde en la cuadrícula del perfil" | Texto fuera del cuadrado central del 4:5 (`y` entre 135 y 1215) | Acorta el título o la bajada; en piezas a mano, súbelo |
| "fuera de zona segura" en una historia | Texto en las franjas que tapa la interfaz | Mira `revision/<pieza>-zonas.jpg` y muévelo |
| "se superponen" | Dos elementos chocan, o algo tapa el logo | Acorta el texto que empuja al otro; en piezas a mano, revisa las coordenadas |
| "… es de baja resolución y se verá borroso" | La foto o el video se amplía más de 1,5 veces | Pide el original (no el que pasó por WhatsApp). Si no lo hay, se acepta el aviso y se le cuenta a quien encargó la pieza |
| Instagram rechaza el MP4 | El archivo no tenía pista de audio | `mp4()` ya agrega una en silencio; si se exporta por otra vía, agrégala |
| La publicación animada aparece como reel | Un video suelto en el feed es un reel | La animación va en una lámina de carrusel que no sea la primera |
| Un bloque de la torre invisible | Era del mismo color que el fondo | La torre evita sola el color de fondo; si pasas `colores`, no incluyas el del fondo |
| El MP4 no tiene algo que sí está en el JPG | Se dibujó después de `animar()` | `animar()` va al final del script |
| Viñetas o emojis que salen como cajas vacías en la imagen | Montserrat no trae glifos de emoji | Los emojis van en el caption; en la imagen, viñetas de color |
| El patrón de doodles no se ve | El PNG viene como marca de agua, con alfa máximo de 26/255 | `Pieza.patron()` normaliza al pico antes de aplicar la opacidad; no lo cambies |
| Acentos que no se dibujan | El subconjunto `latin-ext` de Montserrat no trae `á é í ó ú ñ` | El motor usa la familia completa que trae adentro; no la reemplaces por otra |
| "El amarillo no se usa como acento" | El título quedaría en amarillo sobre blanco, o blanco sobre amarillo | Usa `T`, `M`, `O` o `B`; el amarillo es para chips y viñetas con texto oscuro |
| La pieza sale distinta en otro equipo | (Ya no pasa) El kit usaba la Montserrat del sistema si existía | El motor usa siempre la suya |
