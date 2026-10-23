"""El caption: armarlo con la fórmula CREA y revisarlo contra las reglas de voz.

    <PYTHON> -m crea_publicaciones.caption caption.txt     revisa un caption escrito a mano
"""
import re
import sys
from pathlib import Path

LIMITE_INSTAGRAM = 2200      # caracteres que Instagram acepta en un caption
HASHTAGS_MIN, HASHTAGS_MAX = 5, 7
PARRAFO_LARGO = 300          # caracteres: más de unas tres líneas en el celular
FIJO = '#LaboratorioCREA'
# Hashtags que la cuenta usa en minúscula a propósito; el resto va en CamelCase.
MINUSCULA_PERMITIDA = {'#uniandesciam'}

_EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿⌀-⏿]')
_RELLENO = re.compile('[\\s️‍\U0001F3FB-\U0001F3FF]')
_VOSEO = re.compile(r'\b(tenés|podés|querés|sabés|hacés|venís|decís|sos|vení|mirá|andá|probá|armá)\b', re.I)
_HASHTAG = re.compile(r'#\w+')


def caption(*parrafos, hashtags):
    """Une los párrafos con una línea en blanco y cierra con el bloque de hashtags."""
    tags = [h if h.startswith('#') else f'#{h}' for h in hashtags]
    cuerpo = '\n\n'.join(p.strip() for p in parrafos if p and p.strip())
    return f'{cuerpo}\n\n{" ".join(tags)}'


def _emojis_en_medio(linea):
    # Los emojis van al principio (viñeta o gancho) o al final de la línea, nunca en medio.
    s = linea.strip()
    i = 0
    while i < len(s) and (_EMOJI.match(s[i]) or _RELLENO.match(s[i])):
        i += 1
    j = len(s)
    while j > i and (_EMOJI.match(s[j - 1]) or _RELLENO.match(s[j - 1])):
        j -= 1
    return bool(_EMOJI.search(s[i:j]))


def revisar_caption(texto):
    """Devuelve (errores, avisos). Un error impide publicar; un aviso hay que mirarlo."""
    errores, avisos = [], []
    if len(texto) > LIMITE_INSTAGRAM:
        errores.append(f'el caption tiene {len(texto)} caracteres; Instagram acepta {LIMITE_INSTAGRAM}')
    bloques = [b for b in re.split(r'\n\s*\n', texto.strip()) if b.strip()]
    if not bloques:
        return ['el caption está vacío'], []
    ultimo = bloques[-1]
    tags = _HASHTAG.findall(ultimo)
    if not tags or _HASHTAG.sub('', ultimo).strip():
        avisos.append('los hashtags van solos en un bloque al final, separados por una línea en blanco')
    for b in bloques[:-1]:
        if _HASHTAG.search(b):
            avisos.append(f'hashtag dentro del texto: "{b[:40]}"; van todos en el bloque final')
    if tags:
        if FIJO not in tags:
            avisos.append(f'falta {FIJO}, que va siempre')
        if not HASHTAGS_MIN <= len(tags) <= HASHTAGS_MAX:
            avisos.append(f'{len(tags)} hashtags; van entre {HASHTAGS_MIN} y {HASHTAGS_MAX}')
        repetidos = {t for t in tags if tags.count(t) > 1}
        if repetidos:
            avisos.append(f'hashtags repetidos: {" ".join(sorted(repetidos))}')
        for t in tags:
            if t == t.lower() and t not in MINUSCULA_PERMITIDA and len(t) > 4:
                avisos.append(f'{t} va en CamelCase (por ejemplo #{t[1:].capitalize()})')
    for b in bloques[:-1] if tags else bloques:
        if len(b) > PARRAFO_LARGO:
            avisos.append(f'párrafo largo ({len(b)} caracteres): "{b[:40]}…". Si pasa de tres líneas, sobra algo')
        for linea in b.splitlines():
            if _emojis_en_medio(linea):
                avisos.append(f'emoji en medio de la frase: "{linea.strip()[:50]}". Van al final del párrafo')
    if _VOSEO.search(texto):
        avisos.append(f'voseo ("{_VOSEO.search(texto).group(0)}"): CREA tutea en español colombiano')
    if '—' in texto:
        avisos.append('raya larga (—): usa comas, dos puntos o punto seguido')
    for marca in re.findall(r'\{validar[^}]*\}|\[validar[^\]]*\]', texto):
        avisos.append(f'dato sin validar: {marca}')
    return errores, avisos


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print('Uso: python -m crea_publicaciones.caption <caption.txt>')
        return 2
    errores, avisos = revisar_caption(Path(argv[0]).read_text(encoding='utf-8'))
    for e in errores:
        print(f'❌ {e}')
    for a in avisos:
        print(f'⚠️ {a}')
    if not errores and not avisos:
        print('✅ caption sin avisos')
    return 2 if errores else 1 if avisos else 0


if __name__ == '__main__':
    sys.exit(main())
