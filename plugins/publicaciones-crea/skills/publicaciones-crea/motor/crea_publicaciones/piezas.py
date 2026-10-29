"""Las cuatro piezas de CREA para Instagram: crónica, historia, lámina de carrusel y convocatoria.

Cada función devuelve una `Pieza` lista para `entregar()`. La retícula de cada una está
fijada aquí, en múltiplos de 12, para que todas las piezas de la cuenta se vean iguales.
"""
from pathlib import Path

from PIL import Image

from . import marco, recortes
from .animacion import animar as _animar
from .animacion import leer_video, video_con, video_en_caja
from .base import (BODY, CUERPO, DARK, ETIQ, MARGEN, POST, SOFT, STORY, TITULO, UI_ARRIBA, WHITE, B, ErrorCREA, M,
                   O, Pieza, T, Y, _escala, abrir)

ANCHO = 1080
FOTO_POST = marco.FOTO  # crónica y lámina: la foto va dentro del marco CREA
RADIO = 64              # 0,07 del ancho de la foto, como en las diapositivas
Y_CHIP_FOTO = 148       # el chip sobre la foto queda dentro del cuadrado del perfil (y >= 135)
Y_LOGO_POST = 1158
ANCHO_BAJADA = ANCHO - 2 * MARGEN - 168     # se aparta del logo
FIN_PERFIL = 1215       # el texto del 4:5 termina antes de que el perfil lo recorte
INTER_BAJADA = 1.32


def _lineas_bajada(y, tope=3):
    # Cuántas líneas de bajada caben entre el título y el borde del cuadrado del perfil.
    return max(1, min(tope, int((FIN_PERFIL - y) // (CUERPO * INTER_BAJADA))))


def _acento(acento):
    # Amarillo no sirve de acento: el título o el fondo quedarían con letra ilegible.
    acento = '#' + str(acento).lstrip('#').upper()
    if acento == Y:
        raise ErrorCREA('El amarillo no se usa como acento (no se lee como letra ni bajo letra blanca). '
                        'Usa T, M, O o B')
    if acento not in (T, M, O, B):
        raise ErrorCREA(f'Acento {acento} fuera de la paleta. Usa T (turquesa), M (magenta), O (naranja) o B (azul)')
    return acento


def cronica(foto, titulo, bajada='', categoria='Taller', aliado=None, acento=T, iconos=(), foco=0.5,
            nombre='cronica'):
    """Crónica de taller (4:5) en el marco CREA: foto real, chip de categoría, íconos de la actividad,
    aliado, título y bajada."""
    acento = _acento(acento)
    p = Pieza(POST, WHITE, tipo='cronica', nombre=nombre, acento=acento)
    marco.debajo(p, acento)
    p.foto(foto, FOTO_POST, radio=RADIO, foco=foco)
    marco.encima(p, acento, chip=categoria, iconos=iconos)
    y_titulo = 792
    if aliado:
        # Si el nombre del aliado es largo y llega hasta los íconos, el chip baja a la fila siguiente.
        x_iconos, y_iconos = marco.zona_iconos(len(iconos))
        _, _, ancho_chip, _ = Pieza(POST).chip(aliado, MARGEN, 0, tam=ETIQ - 4, peso='m')
        y_chip = 792 if MARGEN + ancho_chip < x_iconos - 12 else y_iconos + 12
        p.chip(aliado, MARGEN, y_chip, bg=SOFT, fg=DARK, tam=ETIQ - 4, peso='m')
        y_titulo = y_chip + 96
    y = p.texto(titulo, MARGEN, y_titulo, tam=TITULO, peso='b', color=acento, inter=1.08, max_lineas=2)
    if bajada:
        p.texto(bajada, MARGEN, y + 24, ancho=ANCHO_BAJADA, tam=CUERPO, peso='r', color=BODY,
                inter=INTER_BAJADA, max_lineas=_lineas_bajada(y + 24))
    p.logo(ancho=120, y=Y_LOGO_POST)
    return p


def historia(foto, titulo, categoria='Taller', aliado=None, acento=T, mascota=True, animar=False,
             nombre='historia'):
    """Historia (9:16) sobre el patrón de color. Con `animar=True`, Séneca parpadea en el MP4."""
    acento = _acento(acento)
    if animar and not mascota:
        raise ErrorCREA('La animación de la historia es Séneca parpadeando: necesita mascota=True')
    p = Pieza(STORY, tipo='historia', nombre=nombre, acento=acento)
    p.patron(acento)
    # La interfaz tapa 250 px arriba, 320 abajo y 180 a la derecha: ahí no va texto.
    p.foto(foto, (MARGEN, 340, ANCHO - MARGEN, 1100), radio=RADIO)
    p.chip(categoria, MARGEN, UI_ARRIBA, bg=WHITE, fg=acento, mayus=True)
    y_titulo = 1148
    if aliado:
        p.chip(aliado, MARGEN, 1148, bg=WHITE, fg=acento, tam=ETIQ - 4, peso='m')
        y_titulo = 1230
    ancho_texto = 720 if mascota else p.segura()[2] - MARGEN     # se detiene antes de Séneca
    p.texto(titulo, MARGEN, y_titulo, ancho=ancho_texto, tam=TITULO - 12, peso='b', color=WHITE,
            inter=1.1, max_lineas=2)
    p.logo(ancho=150)
    if mascota:
        alto = 380
        p.mascota(ANCHO - MARGEN - Pieza.ancho_mascota(alto), p.segura()[3] - alto, alto=alto)
    if animar:
        _animar(p, 'parpadeo')
    return p


ESTILOS = ('marco', 'recortes', 'arcade')


def lamina(foto, titulo, bajada='', chip=None, acento=T, iconos=(), codigo=None, video=None, desde=0,
           hasta=None, foco=0.5, ajuste='cubrir', estilo='marco', sticker=None, nivel=None, nombre=None):
    """Lámina de carrusel (4:5) en uno de los estilos CREA: 'marco', 'recortes' o 'arcade'.

    `sticker` ('creabot' o 'seneca') solo en 'recortes'; `nivel` (el número de lámina) solo en 'arcade'.

    `iconos`: hasta tres claves de ícono que dicen de qué se trató la actividad. Con `codigo`, la
    línea se escribe letra por letra en el MP4. Con `video`, el video corre en el recuadro de la
    foto (entre `desde` y `hasta`, en segundos) y el JPG muestra su primer cuadro; en ese caso
    `foto` puede ser None. `foco` elige la franja vertical que queda al recortar;
    `ajuste='contener'` muestra la foto o el video entero (para lo vertical que no se puede recortar).
    """
    acento = _acento(acento)
    if estilo not in ESTILOS:
        raise ErrorCREA(f'El estilo "{estilo}" no existe. Usa uno de: {", ".join(ESTILOS)}')
    if codigo and video:
        raise ErrorCREA('Una lámina lleva una sola animación: o código o video')
    if codigo and estilo != 'marco':
        raise ErrorCREA('La línea de código animada solo va en el estilo "marco"')
    if len(iconos) > marco.MAX_ICONOS:
        raise ErrorCREA(f'Van hasta {marco.MAX_ICONOS} íconos: más se vuelve ruido')
    if foto is None and video is None:
        raise ErrorCREA('La lámina necesita una foto o un video')
    p = Pieza(POST, WHITE, tipo='lamina', nombre=nombre, acento=acento)
    if foto is None:
        primero = next(leer_video(video, desde, hasta), None)
        if primero is None:
            raise ErrorCREA(f'No se pudo leer el video {video} desde el segundo {desde}')
        foto = primero
    if estilo != 'marco':
        from . import arcade
        armar = {'recortes': recortes.armar, 'arcade': arcade.armar}[estilo]
        extra = {'sticker': sticker} if estilo == 'recortes' else {'nivel': nivel}
        que = 'el video es' if video else f'la foto {Path(str(foto)).name} es'
        if not isinstance(foto, Image.Image):
            foto = abrir(foto)
        # Las copias de estos estilos miden unos 840 × 600 px: ampliar más de 1,5 veces se ve borroso.
        if _escala(foto, *recortes.FOTO, ajuste) > 1.5:
            p.notas.append(f'{que} de baja resolución ({foto.width}x{foto.height}) y se verá '
                           f'{"borroso" if video else "borrosa"}')
        encima, colocar, base = armar(p, foto, titulo=titulo, bajada=bajada, chip=chip, acento=acento,
                                      iconos=iconos, foco=foco, ajuste=ajuste, **extra)
        if video:
            video_con(p, video, lambda dest, cuadro: colocar(dest, cuadro, sombra=False), base=base,
                      encima=encima, desde=desde, hasta=hasta)
        return p
    marco.debajo(p, acento)
    p.foto(foto, FOTO_POST, radio=RADIO, foco=foco, ajuste=ajuste)
    # Chip, punto e íconos van sobre la foto: en un video, la misma capa va sobre cada cuadro.
    encima = marco.encima(p, acento, chip=chip, iconos=iconos)
    y = p.texto(titulo, MARGEN, 820, tam=TITULO, peso='b', color=acento, inter=1.08, max_lineas=2)
    if bajada:
        p.texto(bajada, MARGEN, y + 24, ancho=ANCHO_BAJADA, tam=CUERPO, peso='r', color=BODY,
                inter=INTER_BAJADA, max_lineas=_lineas_bajada(y + 24, tope=2 if codigo else 3))
    if codigo:
        p.logo(ancho=110, y=1350 - MARGEN - 110)
        _animar(p, 'codigo', texto=codigo, x=MARGEN, y=1148, ancho=780, tam=30)
    else:
        p.logo(ancho=120, y=Y_LOGO_POST)
    if video:
        video_en_caja(p, video, FOTO_POST, radio=RADIO, foco=foco, desde=desde, hasta=hasta, encima=encima,
                      ajuste=ajuste)
    return p


def convocatoria(titulo, puntos, contacto, pregunta=None, nota='No necesitas experiencia previa.',
                 acento=B, mascota=True, nombre='convocatoria'):
    """Convocatoria (4:5), sin foto: patrón, pregunta, título, qué se aprende y cómo inscribirse."""
    acento = _acento(acento)
    if not 1 <= len(puntos) <= 4:
        raise ErrorCREA('La convocatoria lleva de 1 a 4 puntos de lo que se aprende')
    p = Pieza(POST, tipo='convocatoria', nombre=nombre, acento=acento)
    p.patron(acento)
    ancho_texto = 700 if mascota else ANCHO - 2 * MARGEN
    y = 286
    if pregunta:
        p.chip(pregunta, MARGEN, 160, bg=WHITE, fg=acento, tam=ETIQ - 2, peso='m')
    else:
        y = 160
    y = p.texto(titulo, MARGEN, y, ancho=ancho_texto, tam=TITULO, peso='b', color=WHITE,
                inter=1.08, max_lineas=2) + 80
    # Las viñetas son cuadros de color, no emojis: Montserrat no trae glifos de emoji
    # y saldrían como cajas vacías. Los emojis van en el caption.
    for punto in puntos:
        p.d.rounded_rectangle([MARGEN, y + 8, MARGEN + 22, y + 30], 6, fill=Y)
        y = p.texto(punto, MARGEN + 44, y, ancho=ancho_texto - 44, tam=CUERPO - 2, peso='m',
                    color=WHITE, inter=1.25, max_lineas=2) + 14
    if nota:
        y = p.texto(nota, MARGEN, y + 14, ancho=ancho_texto, tam=CUERPO - 2, peso='r', color=WHITE,
                    max_lineas=1)
    p.chip(contacto, MARGEN, y + 26, bg=Y, fg=DARK, tam=ETIQ, peso='b')
    if mascota:
        alto = 400
        p.mascota(ANCHO - MARGEN - Pieza.ancho_mascota(alto), 1278 - alto, alto=alto)
    p.logo(x=MARGEN, y=1168, ancho=110)
    return p
