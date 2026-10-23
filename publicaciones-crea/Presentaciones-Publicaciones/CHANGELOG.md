# Cambios

Formato: [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Versiones: [semver](https://semver.org/lang/es/).

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
