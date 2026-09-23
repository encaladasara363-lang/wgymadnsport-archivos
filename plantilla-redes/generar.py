"""Plantilla definitiva de redes sociales de WGYMADNSPORT.

Todo lo fijo (foto con título "HORARIOS", logo + "GIMNASIO", rayitas
doradas del marco, las 3 redes y los 2 números) sale siempre igual.
Lo único que cambia en cada publicación es el texto de un archivo JSON.

Uso:
    python3 plantilla-redes/generar.py plantilla-redes/textos/horarios.json

Genera plantilla-redes/salidas/<nombre-del-json>.png (1696 x 2528 px).

Formato del JSON:
    {
      "filas": [
        {"izq": "LUNES A JUEVES", "der": "08:00 – 23:30"},   blanco · rojo
        {"texto": "TEXTO DE UNA SOLA LÍNEA"},                  blanco
        {"izq": "DOMINGO", "der": "CERRADO", "gris": true}     todo gris
      ],
      "frase": "La perseverancia es el secreto de tu éxito"   dorado cursiva (opcional)
    }
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.join(AQUI, "fuentes")
FONDO = os.path.join(AQUI, "base", "fondo.jpg")
LOGO = os.path.join(AQUI, "base", "logo.png")

BLANCO, ROJO, GRIS, DORADO = "#FFFFFF", "#E10600", "#9A9A9A", "#D4AF37"
K = 2  # factor de escala sobre el fondo original de 848 x 1264

# Zona útil dentro del marco rojo (coordenadas del original 848 x 1264).
# El marco va de x=32..826, y=586..1222; la parte baja queda para las redes.
FX0, FX1 = 50, 790
FY0, FY1 = 640, 1095
Y_REDES, Y_USUARIO, Y_PIE = 1128, 1158, 1245

REDES = "INSTAGRAM   ·   FACEBOOK   ·   TIKTOK"
USUARIO = "@wadnsport.tocopilla"
PIE = "WhatsApp +56 9 9154 0156 · +56 9 7519 6394"
SEP = " · "

# Tramos del contorno rojo que se pintan de dorado (esquinas y centros)
VENTANAS_DORADAS = [
    (12, 574, 130, 612), (700, 574, 836, 645),
    (12, 1140, 110, 1230), (740, 1195, 836, 1230),
    (370, 580, 480, 592), (370, 1215, 480, 1228),
    (12, 860, 26, 980), (818, 860, 836, 980),
]


def fuente(nombre, tam):
    return ImageFont.truetype(os.path.join(FUENTES, nombre), int(tam))


def base():
    im0 = Image.open(FONDO).convert("RGB")
    im = im0.resize((im0.width * K, im0.height * K), Image.LANCZOS).convert("RGBA")
    px = im.load()
    for x0, y0, x1, y1 in VENTANAS_DORADAS:
        for y in range(y0 * K, y1 * K):
            for x in range(x0 * K, x1 * K):
                r, g, b, a = px[x, y]
                if r > 120 and r > 2.2 * g and r > 2.2 * b:
                    t = min(1.0, r / 225)
                    px[x, y] = (min(255, int(212 * t + g * 0.6)),
                                min(255, int(175 * t + g * 0.6)),
                                min(255, int(55 * t + b * 0.5)), a)
    return im


def poner_logo(out, d):
    W = out.width
    lg = Image.open(LOGO).convert("RGBA")
    lw = round(W * 0.36)
    lh = round(lg.height * lw / lg.width)
    lg = lg.resize((lw, lh), Image.LANCZOS)
    x0, y0 = 22 * K, 140 * K
    pad = 30 * K
    sh = Image.new("L", (lw + 2 * pad, lh + 2 * pad), 0)
    sh.paste(lg.getchannel("A").filter(ImageFilter.MaxFilter(21)), (pad, pad))
    sh = sh.filter(ImageFilter.GaussianBlur(7 * K)).point(lambda v: min(255, int(v * 1.3)))
    negro = Image.new("RGBA", sh.size, (0, 0, 0, 255))
    negro.putalpha(sh)
    out.alpha_composite(negro, (x0 - pad, y0 - pad))
    out.alpha_composite(lg, (x0, y0))
    gf = fuente("Barlow-ExtraBold.ttf", 24 * K)
    esp = 6 * K
    letras = "GIMNASIO"
    tw = sum(d.textlength(c, font=gf) for c in letras) + esp * (len(letras) - 1)
    gx, gy = x0 + lw / 2 - tw / 2, y0 + lh + 4 * K
    for c in letras:
        d.text((gx, gy), c, font=gf, fill=DORADO, anchor="lt")
        gx += d.textlength(c, font=gf) + esp


def texto_fila(f):
    return f["texto"] if "texto" in f else f["izq"] + SEP + f["der"]


def generar(datos, salida):
    out = base()
    d = ImageDraw.Draw(out)
    W = out.width
    x0, x1, y0, y1 = FX0 * K, FX1 * K, FY0 * K, FY1 * K
    cx = (x0 + x1) // 2
    maxw = int((x1 - x0) * 0.85)
    filas = datos["filas"]
    frase = datos.get("frase", "").strip()

    # Mayor tamaño que cabe a lo ancho (85 % del marco) y a lo alto
    size = 70 * K
    while size > 10:
        fnt = fuente("BarlowCondensed-ExtraBold.ttf", size)
        fila_h = int(size * 1.9)
        alto = fila_h * len(filas) + (int(size * 1.5) if frase else 0)
        ancho = max(d.textlength(texto_fila(f), font=fnt) for f in filas)
        frase_f = fuente("BarlowCondensed-SemiBoldItalic.ttf", size * 0.62)
        ancho_frase = d.textlength(frase, font=frase_f) if frase else 0
        if ancho <= maxw and ancho_frase <= maxw and alto <= y1 - y0:
            break
        size -= 1

    y = y0 + (y1 - y0 - alto) // 2
    for i, f in enumerate(filas):
        gris = f.get("gris", False)
        cy = y + fila_h // 2
        if "texto" in f:
            d.text((cx, cy), f["texto"], font=fnt, fill=GRIS if gris else BLANCO, anchor="mm")
        else:
            partes = ((f["izq"], GRIS if gris else BLANCO),
                      (SEP, GRIS if gris else DORADO),
                      (f["der"], GRIS if gris else ROJO))
            x = cx - d.textlength(texto_fila(f), font=fnt) / 2
            for t, color in partes:
                d.text((x, cy), t, font=fnt, fill=color, anchor="lm")
                x += d.textlength(t, font=fnt)
        if i < len(filas) - 1:
            d.line([(cx - maxw / 2, y + fila_h), (cx + maxw / 2, y + fila_h)],
                   fill=ROJO + "B0", width=2 * K)
        y += fila_h

    if frase:
        fy = y + int(size * 0.25)
        d.line([(cx - 60 * K, fy), (cx + 60 * K, fy)], fill=DORADO, width=2 * K)
        d.text((cx, y + int(size * 0.9)), frase, font=frase_f, fill=DORADO, anchor="mm")

    # Fijos: redes, usuario, números y logo
    d.text((cx, Y_REDES * K), REDES, font=fuente("Barlow-ExtraBold.ttf", 17 * K), fill=BLANCO, anchor="mm")
    d.text((cx, Y_USUARIO * K), USUARIO, font=fuente("BarlowCondensed-Bold.ttf", 24 * K), fill=DORADO, anchor="mm")
    d.text((W // 2, Y_PIE * K), PIE, font=fuente("BarlowCondensed-Medium.ttf", 19 * K), fill=BLANCO, anchor="mm")
    poner_logo(out, d)

    out.convert("RGB").save(salida)
    return salida


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 plantilla-redes/generar.py <archivo.json>")
    ruta = sys.argv[1]
    with open(ruta, encoding="utf-8") as fh:
        datos = json.load(fh)
    nombre = os.path.splitext(os.path.basename(ruta))[0]
    salida = os.path.join(AQUI, "salidas", nombre + ".png")
    print(generar(datos, salida))
