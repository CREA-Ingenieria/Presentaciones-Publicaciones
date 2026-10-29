# El caption

El público de la cuenta **son los colegios**: docentes, coordinadores y familias, además de los aliados. Lo dice la biografía: *"¡Trae a tu colegio y transforma la creatividad en realidad!"*. El registro es el de docentes y aliados de `voz-crea.md`.

Lo más importante: **el caption tiene que sonar a alguien de CREA que estuvo en el taller**, no a una plantilla. Un texto que cumple todas las reglas y aun así suena hecho en serie no sirve.

## Cómo suena

- **Cuenta lo que pasó, con los hechos que dio la persona.** Qué hicieron, con qué, qué probaron, qué salió. Un detalle concreto vale más que tres adjetivos.
- **Primera persona del plural, como quien estuvo ahí:** "armamos", "recibimos", "probamos", "hablamos de". El logro es de los estudiantes; CREA no se felicita a sí mismo.
- **Oraciones de largo distinto.** Una corta, otra más larga. Párrafos de una a tres oraciones.
- **Los conceptos técnicos, dichos sin adorno:** "hablamos de voltaje, corriente y resistencias", no "exploraron los fascinantes conceptos de…".
- **El taller con su nombre propio:** "el taller Mothbot", "AguaLab".
- **Agradecer directo:** "Gracias a @bancolombia por organizar el encuentro". Sin "por abrirnos las puertas".
- **Cerrar con algo útil o con nada.** Una invitación ("¿Quieres traer a tu colegio? Escríbenos"), una pregunta al lector o un dato. No con una moraleja.
- **Una o dos exclamaciones en todo el texto.** De uno a cuatro emojis, donde aportan algo (🤖 en un taller de robots). No un par al final de cada párrafo.
- **Tuteo en español colombiano.** Nunca voseo. Sin rayas largas (—).
- **Nada de datos inventados.** Cantidades, edades, duraciones y nombres propios solo si vienen confirmados. Si faltan, se omiten o se marcan `{validar:…}`.

## Lo que delata un texto hecho en serie

| Suena hecho en serie | Mejor |
|---|---|
| "¡El futuro de la ingeniería está en sus manos! 🚀✨" | Nada, o una invitación: "¿Quieres traer a tu colegio? Escríbenos." |
| "Una experiencia única e inolvidable llena de aprendizaje" | Lo que hicieron: "Armamos un robot que sigue la luz." |
| "No solo aprendieron electrónica, sino también trabajo en equipo" | "Por turnos, todos probaron el brazo robótico." |
| "¡Gracias por abrirnos las puertas! 🙌🏦" | "Gracias a @bancolombia por organizar el encuentro." |
| Cada párrafo termina en dos emojis | Uno o dos emojis en todo el texto, donde sumen |
| Cuatro párrafos del mismo largo, con la misma forma | Párrafos de largo distinto; el que no aporta, se quita |
| "Exploraron los conceptos de voltaje, corriente, resistencia y LEDs, y cómo…" | "Hablamos de voltaje, corriente y resistencias: lo básico para entender un circuito." |

`revisar_caption()` avisa de las frases gastadas más comunes (`FRASES_GASTADAS` en `motor/crea_publicaciones/caption.py`), de más de cuatro emojis, de los párrafos que terminan todos en emoji y de más de tres exclamaciones. Un caption sin avisos todavía puede sonar a plantilla: léelo en voz alta.

## Estructura (una guía, no un molde)

1. **Qué pasó y con quién**, en una o dos líneas.
2. **Qué hicieron**, con los conceptos reales del taller. Sale de lo que respondió la persona en el paso 1, o del vault.
3. **Gracias o créditos**, si hay aliado o equipo que nombrar.
4. **Cierre**, solo si suma: una invitación o una pregunta.
5. **Hashtags**, en bloque aparte (el argumento `hashtags`).

No todos los captions llevan los cinco. Uno de tres líneas está bien si dice lo necesario.

### Convocatoria

Abre con la pregunta (*"¿Te interesa la robótica y la electrónica?"*), dice qué taller se abre y para quién, lista lo que se aprende y cierra con cómo inscribirse. La lista sigue el patrón de la cuenta, **emoji + sustantivo + dos puntos**:

```
📚 Introducción: conceptos básicos de electrónica y física
🎨 Diseño: circuitos, resistencias, transistores y LEDs
🔩 Ensamble: estructuras impresas en 3D
```

Y la frase **"No necesitas experiencia previa."**, salvo que el taller sí la pida. Las viñetas no cuentan para el límite de emojis.

### Proyecto institucional

Se **acredita a las personas** (`Proyecto liderado por @…`, `Diseño y animación @…`) y se cierra con `Laboratorio CREA · Universidad de los Andes`.

## Hashtags

La cuenta migró de minúsculas sueltas (`#ingenieria #steam`) a CamelCase de marca. **Se usa el formato nuevo.**

- **Fijos:** `#LaboratorioCREA` + el nombre del taller (`#AguaLab`, `#Mothbot`).
- **Habituales:** `#EducaciónSTEAM` `#uniandesciam` `#MujeresEnSTEAM` `#STEM` `#Ingeniería`.
- **Entre cinco y siete**, en un bloque al final, separado por una línea en blanco. `#uniandesciam` es la única excepción en minúsculas.

## Captions reales de la cuenta

Esta guía se calibra con captions reales de [@crea_uniandes](https://www.instagram.com/crea_uniandes/) y con los textos de [crea.uniandes.edu.co](https://crea.uniandes.edu.co/). Los fragmentos que hay hoy salen del análisis de la cuenta de septiembre de 2026:

- *"¡Las estudiantes del Liceo Femenino de Cundinamarca se convirtieron en Ingenieras Ambientales por un día! 👩‍🔬💧"*
- *"🔧✨ ¿Te interesa la robótica y la electrónica?"*
- Las viñetas `📚 Introducción:` / `🎨 Diseño:` / `🔩 Ensamble:` y *"No necesitas experiencia previa."*
- *"Recibimos…"*, *"Nos encanta ver…"*

**Pendiente:** pegar aquí de tres a cinco captions reales completos de la cuenta y dos o tres textos del sitio, y ajustar esta guía a cómo escribe de verdad el equipo.

## Lo que revisa el motor

`revisar_caption()` (y `entregar()`, que la llama) marca como **error** un caption de más de 2200 caracteres (el límite de Instagram) o vacío, y como **aviso**:

- hashtags que no están solos en el bloque final, o que aparecen dentro del texto;
- falta `#LaboratorioCREA`; menos de 5 o más de 7 hashtags; repetidos; en minúsculas;
- emojis en medio de una frase; más de cuatro emojis; todos los párrafos terminados en emoji;
- frases gastadas y más de tres exclamaciones;
- párrafos de más de 300 caracteres;
- voseo, rayas largas y datos `{validar:…}` o `[validar]`.
