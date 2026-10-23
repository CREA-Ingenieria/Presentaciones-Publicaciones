"""Primitivas del motor: lienzo, colores, fuentes, texto, fotos y revisión de zonas.

Todas las medidas van en píxeles sobre el lienzo de Instagram (1080 de ancho). Las piezas
de piezas.py se construyen sobre `Pieza`; los scripts casi nunca dibujan a mano.
"""
import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RECURSOS = Path(__file__).resolve().parent / 'recursos'
FUENTES = RECURSOS / 'fuentes'
MARCA = RECURSOS / 'marca'
MASCOTA = RECURSOS / 'mascota'
LOGOS = RECURSOS / 'logos'
ILUSTRACIONES = RECURSOS / 'ilustraciones'

T, M, O, B, Y = '#00AFC9', '#D32985', '#E9A222', '#0051C6', '#EBE212'
DARK, BODY, WHITE, SOFT = '#1E2A3A', '#3C3C4A', '#FFFFFF', '#EEF1F5'
PALETA = {T, M, O, B, Y, DARK, BODY, WHITE, SOFT}

# Lienzos. POST es el principal; CUAD es lo que el perfil deja ver de POST.
POST, CUAD, STORY = (1080, 1350), (1080, 1080), (1080, 1920)

# Las presentaciones trabajan en 960x540 pt con margen de 66 pt (6,9 % del ancho).
# Sobre 1080 px eso da 74 px; redondeado a la rejilla de 12 queda 72.
REJ, MARGEN = 12, 72

# Escala derivada de la de presentaciones conservando la proporción 2,8:1
# entre título y cuerpo (36:13 pt allá, 96:36 px acá).
TITULO, SUB, CUERPO, ETIQ, NUM = 96, 48, 36, 30, 288

# Franjas que tapa la interfaz de Instagram en historias y reels.
UI_ARRIBA, UI_ABAJO, UI_DERECHA = 250, 320, 180

# Si el autoajuste baja un título por debajo de esta fracción, el texto es largo.
AJUSTE_TOLERADO = 0.85

PESOS = {'r': 'Regular', 'm': 'Medium', 'sb': 'SemiBold', 'b': 'Bold', 'eb': 'ExtraBold'}
_FUENTES = {}


class ErrorCREA(Exception):
    """Error de uso del motor, con un mensaje pensado para quien escribe el script de la pieza."""


def font(tam, peso='sb'):
    # Siempre la Montserrat del paquete, nunca la del sistema: así el texto mide lo
    # mismo en cualquier equipo y la pieza sale idéntica al regenerarla.
    if peso not in PESOS:
        raise ErrorCREA(f'Peso "{peso}" no existe. Usa uno de: {", ".join(PESOS)}')
    k = (tam, peso)
    if k not in _FUENTES:
        _FUENTES[k] = ImageFont.truetype(str(FUENTES / f'Montserrat-{PESOS[peso]}.ttf'), tam)
    return _FUENTES[k]


def _heic_a_jpg(ruta, destino, sistema=None):
    sistema = sistema or platform.system()
    if sistema == 'Windows':
        # Pillow no lee HEIC; el decodificador WIC de Windows sí trae el códec completo.
        ps = (f'Add-Type -AssemblyName PresentationCore; '
              f'$s=[IO.File]::OpenRead("{ruta}"); '
              f'$d=[Windows.Media.Imaging.BitmapDecoder]::Create($s,"None","OnLoad"); '
              f'$e=New-Object Windows.Media.Imaging.JpegBitmapEncoder; $e.QualityLevel=98; '
              f'$e.Frames.Add($d.Frames[0]); $o=[IO.File]::Create("{destino}"); '
              f'$e.Save($o); $o.Close(); $s.Close()')
        r = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True)
    elif sistema == 'Darwin' and shutil.which('sips'):
        r = subprocess.run(['sips', '-s', 'format', 'jpeg', str(ruta), '--out', str(destino)],
                           capture_output=True, text=True)
    else:
        try:
            import pillow_heif
        except ImportError:
            raise ErrorCREA(f'No se puede abrir {Path(ruta).name}: en este sistema las fotos HEIC necesitan '
                            '`pip install pillow-heif`, o pide la foto en JPG') from None
        pillow_heif.register_heif_opener()
        Image.open(ruta).convert('RGB').save(destino, quality=98)
        return
    if not Path(destino).is_file():
        raise ErrorCREA(f'No se pudo convertir {Path(ruta).name}: {(r.stderr or r.stdout).strip()[:200]}')


def abrir(ruta):
    """Abre una imagen. Las fotos HEIC del celular se convierten primero a JPG."""
    ruta = Path(ruta).resolve()
    if not ruta.is_file():
        raise ErrorCREA(f'No existe la imagen {ruta}')
    if ruta.suffix.lower() not in ('.heic', '.heif'):
        return Image.open(ruta)
    destino = Path(tempfile.gettempdir()) / f'crea-{ruta.stem}-{ruta.stat().st_size}.jpg'
    if not destino.is_file():
        _heic_a_jpg(ruta, destino)
    return Image.open(destino)


def envolver(t, f, ancho):
    lineas = []
    for parrafo in t.split('\n'):
        if not parrafo:
            lineas.append('')
            continue
        act = ''
        for pal in parrafo.split(' '):
            prueba = f'{act} {pal}'.strip()
            if f.getbbox(prueba)[2] <= ancho or not act:
                act = prueba
            else:
                lineas.append(act)
                act = pal
        lineas.append(act)
    return lineas


def dibujar_codigo(im, texto, x, y, ancho, tam=ETIQ, prop=1.0, cursor=True,
                   fondo=DARK, color=WHITE, acento=Y, pad=28):
    """Tarjeta tipo terminal. `prop` es la fracción del texto ya escrita. Devuelve su caja."""
    f = font(tam, 'm')
    lineas = envolver(texto, f, ancho - 2 * pad)
    alto_l = int(tam * 1.45)
    alto = 2 * pad + alto_l * len(lineas)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x, y, x + ancho, y + alto], 20, fill=fondo)
    n = int(round(len(texto) * max(0.0, min(1.0, prop))))
    escrito, usados = [], 0
    for ln in lineas:
        escrito.append(ln[:max(0, n - usados)])
        usados += len(ln) + 1
    for i, ln in enumerate(escrito):
        ly = y + pad + i * alto_l
        if ln:
            d.text((x + pad, ly), ln, font=f, fill=color)
        if cursor and (not ln or len(ln) < len(lineas[i])) and (i == 0 or escrito[i - 1]):
            cx = x + pad + (f.getbbox(ln)[2] if ln else 0)
            d.rectangle([cx + 4, ly + 4, cx + 4 + int(tam * 0.55), ly + tam], fill=acento)
            break
    return (x, y, x + ancho, y + alto)


class Pieza:
    """Un lienzo de Instagram que anota dónde pone cada cosa para poder revisarlo después."""

    def __init__(self, formato=POST, fondo=WHITE, tipo='pieza', nombre=None, acento=T):
        if formato not in (POST, CUAD, STORY):
            raise ErrorCREA('El formato tiene que ser POST (4:5), CUAD (1:1) o STORY (9:16)')
        self.w, self.h = formato
        self.formato = formato
        self.tipo, self.nombre, self.acento = tipo, nombre, acento
        self.color_fondo = fondo
        self.im = Image.new('RGBA', formato, fondo)
        self.d = ImageDraw.Draw(self.im)
        self.cajas = []
        self.notas = []          # avisos que nacen al dibujar (autoajuste, recortes)
        self.cuadros = None      # si la pieza se anima: lista de imágenes del bucle
        self.fps = 30
        self.animacion = None
        self.en_perfil = formato == POST
        self._mascota = None

    # --- zonas -----------------------------------------------------------
    def segura(self):
        if self.formato == STORY:
            return (MARGEN, UI_ARRIBA, self.w - UI_DERECHA, self.h - UI_ABAJO)
        return (MARGEN, MARGEN, self.w - MARGEN, self.h - MARGEN)

    def cuadro_perfil(self):
        """Lo que sobrevive de la pieza en la cuadrícula del perfil."""
        if self.h <= self.w:
            return (0, 0, self.w, self.h)
        dy = (self.h - self.w) // 2
        return (0, dy, self.w, dy + self.w)

    def _anotar(self, caja, etiqueta):
        self.cajas.append((etiqueta, tuple(int(v) for v in caja)))

    def _vigilar_validar(self, t):
        if '{validar' in t or '[validar' in t:
            self.notas.append(f'dato sin validar en la imagen: "{t[:40]}"')

    # --- fondo -----------------------------------------------------------
    def fondo(self, color):
        self.color_fondo = color
        self.d.rectangle([0, 0, self.w, self.h], fill=color)

    def patron(self, color=T, opacidad=0.35, escala=1.0):
        """Fondo de color con la franja de doodles de la plantilla."""
        # El PNG ya viene como marca de agua (alfa máximo 26/255), así que se
        # normaliza al pico: 'opacidad' es la del trazo más fuerte.
        self.fondo(color)
        p = Image.open(MARCA / 'patron_doodles.png').convert('RGBA')
        esc = (self.w / p.width) * escala
        p = p.resize((int(p.width * esc), int(p.height * esc)), Image.LANCZOS)
        capa = Image.new('RGBA', self.im.size, (0, 0, 0, 0))
        for y in range(0, self.h, p.height):
            capa.alpha_composite(p, (0, y))
        a = capa.getchannel('A')
        pico = a.getextrema()[1] or 255
        capa.putalpha(a.point(lambda v: min(255, int(v * 255 / pico * opacidad))))
        self.im.alpha_composite(capa)

    def foto(self, ruta, caja=None, radio=0):
        """Foto que cubre la caja, centrada y sin estirar, con esquinas redondeadas."""
        caja = caja or (0, 0, self.w, self.h)
        x0, y0, x1, y1 = caja
        cw, ch = x1 - x0, y1 - y0
        im = abrir(ruta).convert('RGBA')
        esc = max(cw / im.width, ch / im.height)
        if esc > 1.5:
            self.notas.append(f'la foto {Path(ruta).name} es pequeña ({im.width}x{im.height}) y se verá borrosa')
        im = im.resize((max(1, round(im.width * esc)), max(1, round(im.height * esc))), Image.LANCZOS)
        im = im.crop(((im.width - cw) // 2, (im.height - ch) // 2,
                      (im.width - cw) // 2 + cw, (im.height - ch) // 2 + ch))
        if radio:
            mask = Image.new('L', (cw, ch), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, cw - 1, ch - 1], radio, fill=255)
            im.putalpha(mask)
        self.im.alpha_composite(im, (x0, y0))
        self._anotar(caja, 'foto')

    def velo(self, caja=None, color=DARK, alpha=210, desde='abajo'):
        """Degradado del oscuro de marca para que el texto blanco se lea sobre la foto."""
        caja = caja or (0, 0, self.w, self.h)
        x0, y0, x1, y1 = caja
        cw, ch = x1 - x0, y1 - y0
        g = Image.new('L', (1, ch))
        for i in range(ch):
            t = i / max(1, ch - 1)
            v = t if desde == 'abajo' else 1 - t
            g.putpixel((0, i), int(alpha * (v ** 1.6)))
        capa = Image.new('RGBA', (cw, ch), color)
        capa.putalpha(g.resize((cw, ch)))
        self.im.alpha_composite(capa, (x0, y0))

    # --- contenido -------------------------------------------------------
    def texto(self, t, x, y, ancho=None, tam=CUERPO, peso='sb', color=DARK,
              align='l', inter=1.25, mayus=False, max_lineas=None, minimo=None):
        """Texto con ajuste de línea. Con `max_lineas` baja de tamaño hasta caber. Devuelve la y final."""
        ancho = ancho or (self.w - 2 * MARGEN)
        self._vigilar_validar(t)
        if mayus:
            t = t.upper()
        original = tam
        if max_lineas:
            minimo = minimo or int(tam * 0.6)
            while tam > minimo and len(envolver(t, font(tam, peso), ancho)) > max_lineas:
                tam -= 2
            lineas = envolver(t, font(tam, peso), ancho)
            if len(lineas) > max_lineas:
                lineas = lineas[:max_lineas]
                lineas[-1] = lineas[-1].rstrip()[:-1] + '…'
                self.notas.append(f'texto recortado, no cabe en {max_lineas} líneas: "{t[:40]}". Acórtalo')
                t = '\n'.join(lineas)
            elif tam < original * AJUSTE_TOLERADO:
                self.notas.append(f'texto encogido de {original} a {tam} px para caber: "{t[:40]}". Acórtalo')
        f = font(tam, peso)
        lineas = envolver(t, f, ancho)
        alto = int(tam * inter)
        ancho_max = 0
        for i, ln in enumerate(lineas):
            lw = f.getbbox(ln)[2] if ln else 0
            ancho_max = max(ancho_max, lw)
            lx = x if align == 'l' else (x + (ancho - lw) // 2 if align == 'c' else x + ancho - lw)
            self.d.text((lx, y + i * alto), ln, font=f, fill=color)
        fin = y + len(lineas) * alto
        self._anotar((x, y, x + ancho_max, fin), f'texto:{t[:28]}')
        return fin

    def chip(self, t, x, y, bg=T, fg=WHITE, tam=ETIQ, peso='sb', pad=(28, 16), radio=None, mayus=False):
        """Etiqueta redondeada. Devuelve (x, y, ancho, alto)."""
        self._vigilar_validar(t)
        if mayus:
            t = t.upper()
        f = font(tam, peso)
        bb = f.getbbox(t)
        cw, ch = bb[2] - bb[0] + 2 * pad[0], int(tam * 1.32) + 2 * pad[1]
        radio = ch // 2 if radio is None else radio
        self.d.rounded_rectangle([x, y, x + cw, y + ch], radio, fill=bg)
        self.d.text((x + pad[0] - bb[0], y + (ch - (bb[3] - bb[1])) // 2 - bb[1]), t, font=f, fill=fg)
        self._anotar((x, y, x + cw, y + ch), f'chip:{t[:24]}')
        return (x, y, cw, ch)

    def codigo(self, texto, x, y, ancho, tam=ETIQ, **kw):
        """Tarjeta tipo terminal con una línea de código."""
        caja = dibujar_codigo(self.im, texto, x, y, ancho, tam, **kw)
        self._anotar(caja, f'codigo:{texto[:24]}')
        return caja

    def img(self, ruta, x, y, alto=None, ancho=None):
        im = abrir(ruta).convert('RGBA')
        if alto:
            ancho = round(im.width * alto / im.height)
        elif ancho:
            alto = round(im.height * ancho / im.width)
        else:
            ancho, alto = im.size
        im = im.resize((ancho, alto), Image.LANCZOS)
        self.im.alpha_composite(im, (int(x), int(y)))
        self._anotar((x, y, x + ancho, y + alto), Path(ruta).name)
        return (x, y, ancho, alto)

    def mascota(self, x, y, alto=520, pose='saludo'):
        """Séneca. Guarda lo que había debajo para poder hacerla parpadear."""
        if pose not in ('saludo', 'guino'):
            raise ErrorCREA('Séneca solo tiene dos poses: "saludo" y "guino"')
        antes = self.im.copy()
        caja = self.img(MASCOTA / f'seneca_{pose}.png', x, y, alto=alto)
        self._mascota = {'caja': caja, 'antes': antes}
        return caja

    @staticmethod
    def ancho_mascota(alto):
        with Image.open(MASCOTA / 'seneca_saludo.png') as m:
            return round(m.width * alto / m.height)

    def logo(self, x=None, y=None, ancho=150):
        """Logo CREA. Abajo a la derecha; en historia, abajo a la izquierda (a la derecha van los botones)."""
        x0, y0, x1, y1 = self.segura()
        if x is None:
            x = x0 if self.formato == STORY else x1 - ancho
        if y is None:
            y = y1 - ancho
        return self.img(MARCA / 'crea_logo.png', x, y, ancho=ancho)

    # --- revisión --------------------------------------------------------
    def revisar(self):
        """Avisos de calidad: zonas, cuadrícula del perfil, superposiciones y marcas sin validar."""
        av = list(self.notas)
        sx0, sy0, sx1, sy1 = self.segura()
        mx0, my0, mx1, my1 = MARGEN, MARGEN, self.w - MARGEN, self.h - MARGEN
        _, gy0, _, gy1 = self.cuadro_perfil()
        for etq, (x0, y0, x1, y1) in self.cajas:
            # El texto respeta la zona que la interfaz deja libre; lo decorativo
            # (fotos, mascota) solo tiene que respetar el margen.
            es_texto = etq.startswith(('texto', 'chip'))
            zx0, zy0, zx1, zy1 = (sx0, sy0, sx1, sy1) if es_texto else (mx0, my0, mx1, my1)
            if x0 < zx0 - 1 or y0 < zy0 - 1 or x1 > zx1 + 1 or y1 > zy1 + 1:
                av.append(f'fuera de zona segura: {etq}')
            elif es_texto and self.en_perfil and (y0 < gy0 or y1 > gy1):
                av.append(f'se pierde en la cuadrícula del perfil: {etq}')
        for i, (ea, a) in enumerate(self.cajas):
            for eb, b in self.cajas[i + 1:]:
                if ea == 'foto' or eb == 'foto':
                    continue
                # Choques con texto y lo que tape el logo: "nada encima de los logos".
                vigilar = (ea.startswith(('texto', 'chip', 'codigo')) or eb.startswith(('texto', 'chip', 'codigo'))
                           or 'crea_logo' in ea or 'crea_logo' in eb)
                if vigilar and a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                    av.append(f'se superponen: {ea} / {eb}')
        return av

    def guardar(self, ruta):
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        self.im.convert('RGB').save(ruta, quality=95, subsampling=0)
        return ruta
