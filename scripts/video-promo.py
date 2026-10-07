"""Video promocional vertical con la marca WGYM ADN SPORT.

Uso: python3 scripts/video-promo.py <video_fuente> <salida.mp4> ["LÍNEA 1" "LÍNEA 2"]
Variables opcionales: LENTA="desde,hasta" repite ese tramo en cámara lenta
(a la mitad de velocidad, con cuadros intermedios) después del video;
CIERRE=segundos del cierre (2,5 por defecto).

- 720x1280, fondo negro con brillo rojo, el video centrado (fondo difuminado
  de sí mismo si no es vertical).
- Logo oficial arriba, frase en Rubik Distressed abajo que entra con un
  parpadeo rojo/blanco (efecto glitch) y queda fija.
- Cierre de 2,5 s con dirección y los DOS WhatsApp del gimnasio (regla de
  CLAUDE.md: siempre ambos números).
"""
import os, sys, subprocess, tempfile, glob, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import imageio_ffmpeg

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 720, 1280, 24
RED = (227, 6, 19); GOLD = (212, 175, 55); WHITE = (255, 255, 255)
F = lambda f, s: ImageFont.truetype(os.path.join(REPO, f), s)
rubik = lambda s: F('assets/font-rubik-distressed.ttf', s)
anton = lambda s: F('contenido/fuentes/Anton.ttf', s)
barlow = lambda s: F('contenido/fuentes/BarlowCondensed.ttf', s)
CIERRE = float(os.environ.get('CIERRE', 2.5))
LENTA = os.environ.get('LENTA')

src, out = sys.argv[1], sys.argv[2]
L1, L2 = (sys.argv[3], sys.argv[4]) if len(sys.argv) > 4 else ("ROMPE TUS", "LÍMITES")

tmp = tempfile.mkdtemp()
subprocess.run([FF, '-v', 'error', '-i', src, '-map', '0:v:0', '-r', str(FPS), os.path.join(tmp, '%04d.png')], check=True)
frames = [Image.open(f).convert('RGB') for f in sorted(glob.glob(os.path.join(tmp, '*.png')))]
if LENTA:
    a, b = [float(x) for x in LENTA.split(',')]
    tl = tempfile.mkdtemp()
    subprocess.run([FF, '-v', 'error', '-ss', str(a), '-t', str(b - a), '-i', src, '-map', '0:v:0',
                    '-vf', 'setpts=2*PTS,minterpolate=fps=%d:mi_mode=mci' % FPS, os.path.join(tl, '%04d.png')], check=True)
    frames += [Image.open(f).convert('RGB') for f in sorted(glob.glob(os.path.join(tl, '*.png')))]
logo = Image.open(os.path.join(REPO, 'maquinas-wgymadnsport/comun/logo.png')).convert('RGBA')
logo = logo.resize((380, int(380 * logo.height / logo.width)), Image.LANCZOS)

# Fondo fijo: negro con brillo rojo arriba y abajo.
base = Image.new('RGB', (W, H), (10, 10, 11))
glow = Image.new('L', (W, H), 0); g = ImageDraw.Draw(glow)
g.ellipse((-200, -260, W + 200, 420), fill=120); g.ellipse((-200, H - 380, W + 200, H + 260), fill=90)
glow = glow.filter(ImageFilter.GaussianBlur(90))
base = Image.composite(Image.new('RGB', (W, H), (90, 8, 14)), base, glow)

VY = 250  # donde empieza el video

def video_en(im):
    fg = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS)
    return fg

def texto_centrado(d, y, txt, fnt, fill, dx=0):
    w = d.textlength(txt, font=fnt); d.text(((W - w) / 2 + dx, y), txt, font=fnt, fill=fill)

def franjas(d):
    d.rectangle((40, 22, 40 + int((W - 80) * .65), 34), fill=RED); d.rectangle((40 + int((W - 80) * .65), 22, W - 40, 34), fill=GOLD)
    d.rectangle((40, H - 34, 40 + int((W - 80) * .3), H - 22), fill=RED); d.rectangle((40 + int((W - 80) * .3), H - 34, W - 40, H - 22), fill=GOLD)

def frase(img, t):
    """La frase entra en t=1,2 s con 0,6 s de parpadeo y queda fija."""
    t0 = 1.2
    if t < t0: return
    d = ImageDraw.Draw(img)
    f1, f2 = rubik(96), rubik(128)
    y = VY + 720 + 26
    k = t - t0
    if k < 0.6:
        random.seed(int(t * FPS))
        if random.random() < .3: return
        for col, dx in ((RED, random.randint(-14, 14)), (WHITE, random.randint(-5, 5))):
            texto_centrado(d, y, L1, f1, col, dx); texto_centrado(d, y + 92, L2, f2, col if col == RED else GOLD, dx)
    else:
        texto_centrado(d, y + 3, L1, f1, RED, 3); texto_centrado(d, y, L1, f1, WHITE)
        texto_centrado(d, y + 95, L2, f2, RED, 3); texto_centrado(d, y + 92, L2, f2, GOLD)

def cuadro(fr, t):
    img = base.copy(); v = video_en(fr)
    img.paste(v, (0, VY))
    d = ImageDraw.Draw(img)
    d.rectangle((0, VY - 4, W, VY), fill=RED); d.rectangle((0, VY + v.height, W, VY + v.height + 4), fill=GOLD)
    img.paste(logo, ((W - logo.width) // 2, 52), logo)
    franjas(d); frase(img, t)
    return img

def cierre(ultimo, k):
    img = ImageEnhance.Brightness(ultimo.filter(ImageFilter.GaussianBlur(16))).enhance(.15)
    a = min(1, k / .4)
    d = ImageDraw.Draw(img)
    img.paste(logo, ((W - logo.width) // 2, 150), logo)
    texto_centrado(d, 330, "WGYMADNSPORT · TOCOPILLA", barlow(40), GOLD)
    texto_centrado(d, 430, "ENTRENA", rubik(110), WHITE)
    texto_centrado(d, 545, "CON NOSOTROS", rubik(80), RED)
    for i, n in enumerate(("+56 9 9154 0156", "+56 9 7519 6394")):
        y = 720 + i * 120
        d.rounded_rectangle((110, y, W - 110, y + 92), 46, fill=(31, 142, 78), outline=GOLD, width=5)
        texto_centrado(d, y + 10, n, anton(58), WHITE)
    texto_centrado(d, 980, "WHATSAPP", barlow(34), (230, 255, 230))
    texto_centrado(d, 1050, "21 de Mayo 1520, Tocopilla", barlow(40), (220, 220, 220))
    franjas(d)
    return Image.blend(ultimo, img, a)

oscuro = tempfile.mkdtemp(); n = 0
for i, fr in enumerate(frames):
    cuadro(fr, i / FPS).save(os.path.join(oscuro, '%04d.png' % n)); n += 1
ult = cuadro(frames[-1], 99)
for j in range(int(CIERRE * FPS)):
    cierre(ult, j / FPS).save(os.path.join(oscuro, '%04d.png' % n)); n += 1
dur = n / FPS
subprocess.run([FF, '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(oscuro, '%04d.png'),
                '-i', src, '-map', '0:v', '-map', '1:a?', '-af', 'apad', '-t', '%.3f' % dur,
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-c:a', 'aac', '-movflags', '+faststart', out], check=True)
print(out, round(dur, 2), 's')
