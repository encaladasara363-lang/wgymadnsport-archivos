"""Imagen de rutina con el diseño WGYM ADN SPORT: foto del ejercicio (inicio o
final) con el logo oficial arriba a la derecha (sin recuadro), una pastilla "INICIO"/"FINAL"
y el músculo trabajado marcado en rojo (fijo, sin parpadeo).

Uso: python3 scripts/imagen-par.py <foto> <salida.webp> <INICIO|FINAL> [cx,cy,rx,ry ...]
Los óvalos del músculo van en px de la imagen final (600 de ancho).
"""
import sys, os
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RED = (227, 6, 19); GOLD = (212, 175, 55)
W = 600

src, out, etiqueta = sys.argv[1], sys.argv[2], sys.argv[3].upper()
ovalos = [tuple(float(v) for v in a.split(',')) for a in sys.argv[4:]]
im = Image.open(src).convert('RGB')
im = im.resize((W, int(im.height * W / im.width)), Image.LANCZOS)
H = im.height

if ovalos:
    a = np.array(im).astype(np.float32)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    piel = (R > 85) & (G > 45) & (B > 25) & (R - G > 12) & (R - B > 22)
    yy, xx = np.mgrid[0:H, 0:W]
    m = np.zeros((H, W), np.float32)
    for cx, cy, rx, ry in ovalos:
        m = np.maximum(m, np.clip(1.3 - (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2), 0, 1))
    m = ndimage.gaussian_filter(m * piel, 4) * 0.6
    for c, v in enumerate((235, 20, 30)):
        a[..., c] = a[..., c] * (1 - m) + v * m
    im = Image.fromarray(a.clip(0, 255).astype('uint8'))

d = ImageDraw.Draw(im)
logo = Image.open(os.path.join(REPO, 'maquinas-wgymadnsport/comun/logo.png')).convert('RGBA')
logo = logo.resize((200, int(200 * logo.height / logo.width)), Image.LANCZOS)
# Logo arriba a la derecha, sin recuadro: solo una sombra suave para que se lea.
x0, y0 = W - logo.width - 12, 10
alfa = logo.split()[3].point(lambda v: v * 0.7)
sombra = Image.new('RGBA', im.size, (0, 0, 0, 0))
sombra.paste(Image.new('RGBA', logo.size, (0, 0, 0, 255)), (x0 + 2, y0 + 3), alfa)
sombra = sombra.filter(ImageFilter.GaussianBlur(5))
im = Image.alpha_composite(im.convert('RGBA'), sombra)
im.alpha_composite(logo, (x0, y0))
d = ImageDraw.Draw(im)
f = ImageFont.truetype(os.path.join(REPO, 'assets/font-rubik-distressed.ttf'), 40)
tw = d.textlength(etiqueta, font=f)
color = RED if etiqueta == 'INICIO' else GOLD
d.rounded_rectangle((16, H - 84, 16 + tw + 40, H - 24), 30, fill=color + (255,))
d.text((36, H - 54), etiqueta, font=f, fill=(255, 255, 255, 255) if etiqueta == 'INICIO' else (10, 10, 11, 255), anchor='lm')
im.convert('RGB').save(out, quality=88)
print(out, im.size)
