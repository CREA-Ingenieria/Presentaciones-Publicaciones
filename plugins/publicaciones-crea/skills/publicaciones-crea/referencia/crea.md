# El set de CREA

Lo que la skill ya sabe del laboratorio, para no preguntarlo en cada encargo ni inventarlo. La fuente es `motor/crea_publicaciones/recursos/crea.json`; este archivo lo explica. **Cada dato tiene un estado:**

- **confirmado:** se usa sin preguntar.
- **por validar:** no se publica sin preguntar. En el paso 1, inclúyelo en la tanda de preguntas («¿sigue siendo este el correo?»). Si no hay respuesta, se omite o va como `{validar:…}`.

Desde un script, `from crea_publicaciones import *` trae `taller()`, `contacto_reel()` y `por_validar()`; el JSON entero sale con `from crea_publicaciones.datos import crea`.

## El laboratorio

**Laboratorio CREA** · Facultad de Ingeniería · Universidad de los Andes · Bogotá.

**Biografía de la cuenta** (confirmado): *«¡Trae a tu colegio y transforma la creatividad en realidad!»*. Es el titular natural de un cierre o de un llamado a la acción.

## Contacto

| Ícono | Dato | Estado | De dónde sale |
|---|---|---|---|
| `@` | @crea_uniandes | confirmado | instagram.com/crea_uniandes |
| `laptop` | crea.uniandes.edu.co | confirmado | sitio del laboratorio |
| `paper` | crea@uniandes.edu.co | **por validar** | solo aparece en el ejemplo de convocatoria del Kit CREA |
| `pin` | Centro de Bienvenida, Universidad de los Andes | confirmado | crea.uniandes.edu.co |

`contacto_reel()` arma la escena de contacto del reel con estos datos (sin los que están por validar, salvo `incluir_por_validar=True`).

## Talleres

El nombre propio va siempre igual, en la pieza y en el caption («nuestro taller Mothbot»). El acento es una convención para que el feed tenga ritmo, no una regla heredada.

| Taller | Acento | Íconos sugeridos | Qué se hace | Estado |
|---|---|---|---|---|
| AguaLab | Turquesa (`T`) | `flask`, `eye`, `recycle` | Muestras reales de agua: parámetros fisicoquímicos y diseño de filtros | confirmado |
| Mothbot | Azul (`B`) | `robot`, `bulb`, `cogs` | Un robot pequeño seguidor de luz con componentes sencillos; electrónica básica (voltaje, corriente, resistencias, LEDs). Se acompaña de un brazo robótico de demostración | confirmado |
| Ciencia de Cohetes | Naranja (`O`) | `rocket`, `launch`, `distance` | (falta: preguntarlo) | confirmado el nombre |
| Diseñadores del Futuro | Magenta (`M`) | `drafting`, `palette`, `shapes` | (falta: preguntarlo) | confirmado el nombre |
| CREA tu propio videojuego | Turquesa (`T`) | `code`, `laptop`, `play` | Un juego tipo «collector» en HTML, CSS y JavaScript | **por validar**: en la tabla del Kit aparece «Programación web»; confirmar si es el mismo |
| Explorando nuevos planetas | (sin definir) | `rocket`, `atom`, `target` | Para 13 a 17 años | **por validar** |
| Sé lo que quieras ser | (sin definir) | `users`, `bulb`, `tools` | Para 9 a 12 años | **por validar** |

Un taller que no está aquí se pregunta (nombre exacto, qué se hace) y se agrega al JSON con una PR.

## Hashtags

- **Fijos:** `#LaboratorioCREA` + el del taller cuando lo tiene (`#AguaLab`, `#Mothbot`).
- **Habituales:** `#EducaciónSTEAM` `#uniandesciam` `#MujeresEnSTEAM` `#STEM` `#Ingeniería`.

## Aliados

| Aliado | Cuenta | Estado | Nota |
|---|---|---|---|
| Bancolombia | @bancolombia | confirmado | Organizó el encuentro del taller Mothbot con el Colegio Garcés Navas IED en su sede del Centro Internacional (Ak. 7 #32-28), octubre de 2026 |
| SLB | (sin cuenta) | **por validar** | Aliado institucional: sus logos vienen en la plantilla de CREA. Confirmar la cuenta antes de etiquetar |

## Personajes

- **Séneca**, la mascota (la cabra): `saludo`, `guino` (el par de parpadeo) y `baile` (sticker con borde blanco).
- **CREABOT**, el robot de CREA, del taller «CREA tu propio videojuego»: sticker y retrato de la caja de diálogo del estilo arcade.

## Mantener el set

Cuando alguien de CREA confirma un dato en un encargo, cámbialo a `confirmado` en `crea.json`, con la fuente y la fecha, en la misma PR que el resto del trabajo. Cuando un dato cambia (un correo nuevo, un taller que se renombra), se cambia aquí y en ningún otro lugar.
