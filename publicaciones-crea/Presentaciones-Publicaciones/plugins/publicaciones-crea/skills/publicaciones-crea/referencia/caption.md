# El caption

El público de la cuenta **son los colegios**, no los estudiantes de Uniandes. Lo dice la propia biografía: *"¡Trae a tu colegio y transforma la creatividad en realidad!"*. El registro es el de docentes y aliados de `voz-crea.md`, con la calidez de quien cuenta algo que acaba de pasar.

## La fórmula

Cinco bloques, en este orden, cada uno un párrafo de `caption(...)`:

1. **Gancho:** una línea con la transformación lograda, más dos emojis.
   *"¡Las estudiantes del Liceo Femenino de Cundinamarca se convirtieron en Ingenieras Ambientales por un día! 👩‍🔬💧"*
   En convocatorias, pregunta retórica: *"🔧✨ ¿Te interesa la robótica y la electrónica?"*
2. **Contexto:** qué taller, con quién. **El taller se nombra siempre con su nombre propio:** "nuestro taller AguaLab", "el taller Mothbot".
3. **Detalle técnico:** los conceptos reales, sin diluir: *"parámetros fisicoquímicos"*, *"resistencias, transistores y LEDs"*, *"HTML, CSS y JavaScript"*. Este bloque es el que distingue a CREA: trata al lector como capaz. Sale de lo que respondió la persona en el paso 1, o del vault.
4. **Cierre con proyección:** *"¡El futuro de nuestro planeta está en excelentes manos! 🌎✨"*
5. **Hashtags**, en bloque aparte (el argumento `hashtags`).

### Convocatoria

Gancho con pregunta, contexto, la lista de lo que se aprende y el cierre con cómo inscribirse. La lista sigue un patrón fijo, **emoji + sustantivo + dos puntos**, en un solo párrafo:

```
📚 Introducción: conceptos básicos de electrónica y física
🎨 Diseño: circuitos, resistencias, transistores y LEDs
🔩 Ensamble: estructuras impresas en 3D
```

Y siempre la frase **"No necesitas experiencia previa."**, salvo que el taller sí la pida.

### Proyecto institucional

Se **acredita a las personas** (`Proyecto liderado por @…`, `Diseño y animación @…`) y se cierra con `Laboratorio CREA · Universidad de los Andes`.

## Reglas de voz

- **Primera persona del plural, pero el héroe es el visitante.** CREA dice "Recibimos", "Nos encanta ver". El logro es de los estudiantes; el laboratorio nunca se felicita a sí mismo.
- **Exclamaciones** al abrir y cerrar. Es el tono de la cuenta.
- **Emojis en pares, al final del párrafo.** Nunca en medio de una frase. Al principio solo en el gancho de una convocatoria y en las viñetas.
- **Frases cortas.** Si un párrafo pasa de tres líneas en el celular (unos 300 caracteres), sobra algo.
- **Tuteo en español colombiano.** Nunca voseo.
- **Sin rayas largas (—):** comas, dos puntos o punto seguido.
- **Nada de datos inventados.** Cantidades, edades, duraciones y nombres propios solo si vienen confirmados. Si faltan, se omiten o se marcan `{validar:…}` hasta que alguien de CREA los confirme.

## Hashtags

La cuenta migró de minúsculas sueltas (`#ingenieria #steam`) a CamelCase de marca. **Se usa el formato nuevo.**

- **Fijos:** `#LaboratorioCREA` + el nombre del taller (`#AguaLab`, `#Mothbot`).
- **Habituales:** `#EducaciónSTEAM` `#uniandesciam` `#MujeresEnSTEAM` `#STEM` `#Ingeniería`.
- **Entre cinco y siete**, en un bloque al final, separado por una línea en blanco. `#uniandesciam` es la única excepción en minúsculas.

## Lo que revisa el motor

`revisar_caption()` (y `entregar()`, que la llama) marca como **error** un caption de más de 2200 caracteres (el límite de Instagram) o vacío, y como **aviso**:

- hashtags que no están solos en el bloque final, o que aparecen dentro del texto;
- falta `#LaboratorioCREA`; menos de 5 o más de 7 hashtags; repetidos; en minúsculas;
- emojis en medio de una frase;
- párrafos de más de 300 caracteres;
- voseo, rayas largas y datos `{validar:…}` o `[validar]`.

Lo que el motor no puede revisar, lo revisas tú: que el taller tenga su nombre propio, que el detalle técnico sea real y que el héroe sea el visitante.
