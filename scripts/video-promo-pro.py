"""Video promocional "potente" con un socio entrenando (12-10-2026, pedido de la dueña:
"hazme una publicidad para llamar gente con este socio de mi gym, potente, innovadora, moderna").

Uso: python3 scripts/video-promo-pro.py <video_fuente_vertical> <salida.mp4>
Variable opcional FRASES (JSON) para cambiar las frases sin tocar el script.

- 720x1280 a 30 cuadros, video a pantalla completa con color más intenso y viñeta roja.
- Logo grande que entra con destello y queda chico arriba a la izquierda.
- Frases en Rubik Distressed que entran con golpe de zoom, separación roja/blanca (glitch)
  y destello; barra de avance roja/dorada abajo.
- Cierre de 4 s: logo, "ÚNETE AL EQUIPO", lo que trae el gimnasio en el celular y los DOS
  WhatsApp (regla de CLAUDE.md) más la dirección.
- Pista de audio propia (golpes, platillos e impactos sintetizados): no usa la música del
  video, que podría tener derechos y hacer que las redes silencien la publicación.
"""
import os, sys, subprocess, tempfile, glob, math, random, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
import imageio_ffmpeg

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 720, 1280, 30
RED = (227, 6, 19); GOLD = (212, 175, 55); WHITE = (255, 255, 255)
F = lambda f, s: ImageFont.truetype(os.path.join(REPO, f), s)
rubik = lambda s: F('assets/font-rubik-distressed.ttf', s)
anton = lambda s: F('contenido/fuentes/Anton.ttf', s)
barlow = lambda s: F('contenido/fuentes/BarlowCondensed.ttf', s)

FRASES = [  # (desde, hasta, línea 1, línea 2) en segundos del video
    (0.9, 9.6, "TU ESPALDA", "SE CONSTRUYE AQUÍ"),
    (10.1, 14.4, "CADA REPETICIÓN", "CUENTA"),
    (15.0, 99, "SIN LÍMITES", "SIN EXCUSAS"),
]
if os.environ.get('FRASES'):  # frases propias: FRASES='[[desde,hasta,"LÍNEA 1","LÍNEA 2"],...]'
    import json
    FRASES = [tuple(f) for f in json.loads(os.environ['FRASES'])]
CIERRE = 4.0

src, out = sys.argv[1], sys.argv[2]
tmp = tempfile.mkdtemp()
subprocess.run([FF, '-v', 'error', '-i', src, '-map', '0:v:0', '-r', str(FPS),
                '-vf', 'scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d' % (W, H, W, H),
                os.path.join(tmp, '%04d.png')], check=True)
archivos = sorted(glob.glob(os.path.join(tmp, '*.png')))
DUR_V = len(archivos) / FPS

logo = Image.open(os.path.join(REPO, 'maquinas-wgymadnsport/comun/logo.png')).convert('RGBA')
def logo_a(ancho): return logo.resize((ancho, int(ancho * logo.height / logo.width)), Image.LANCZOS)
logo_chico, logo_cierre = logo_a(200), logo_a(420)

# Viñeta roja y degradado oscuro abajo para que el texto se lea.
vin = Image.new('L', (W, H), 0); g = ImageDraw.Draw(vin)
g.ellipse((-160, -120, W + 160, H + 120), fill=255); vin = vin.filter(ImageFilter.GaussianBlur(140))
capa_roja = Image.new('RGB', (W, H), (70, 0, 6))
grad = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(grad)
for y in range(H):
    v = 0 if y < H * .5 else int(215 * ((y - H * .5) / (H * .5)) ** 1.4)
    gd.line((0, y, W, y), fill=v)
negro = Image.new('RGB', (W, H), (0, 0, 0))

def gradear(im):
    im = ImageEnhance.Contrast(im).enhance(1.18); im = ImageEnhance.Color(im).enhance(1.15)
    im = ImageEnhance.Brightness(im).enhance(.92)
    im = Image.composite(im, capa_roja, vin)
    return Image.composite(negro, im, grad)

def centro(d, y, txt, fnt, fill, dx=0, cx=W / 2):
    w = d.textlength(txt, font=fnt); d.text((cx - w / 2 + dx, y), txt, font=fnt, fill=fill)

def ajustar(txt, tam, ancho_max):
    f = rubik(tam)
    while ImageDraw.Draw(negro).textlength(txt, font=f) > ancho_max and tam > 40:
        tam -= 4; f = rubik(tam)
    return f

def franjas(d):
    d.rectangle((0, H - 10, W, H), fill=(20, 20, 22))

def frase(img, t):
    for a, b, l1, l2 in FRASES:
        if not (a <= t < min(b, DUR_V)): continue
        k = t - a; fin = min(b, DUR_V) - t
        alfa = min(1, fin / .2) if fin < .2 else 1
        f1, f2 = ajustar(l1, 92, W - 70), ajustar(l2, 118, W - 50)
        y = 900
        capa = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
        esc = 1 + .45 * math.exp(-k * 14)            # golpe de tamaño al entrar
        sep = int(16 * math.exp(-k * 9))            # separación roja/blanca que se cierra
        random.seed(int(t * FPS))
        dx2 = int(260 * math.exp(-max(0, k - .12) * 12)) if k >= .12 else W   # línea 2 entra desde la derecha
        for col, off in (((255, 30, 40, 230), -sep), ((40, 220, 255, 140), sep)):
            centro(d, y, l1, f1, col, off); centro(d, y + 96, l2, f2, col, off + dx2)
        centro(d, y + 4, l1, f1, (120, 0, 6, 255), 4); centro(d, y, l1, f1, WHITE)
        centro(d, y + 100, l2, f2, (120, 0, 6, 255), dx2 + 4); centro(d, y + 96, l2, f2, GOLD, dx2)
        if esc > 1.01:
            capa = capa.resize((int(W * esc), int(H * esc)), Image.BICUBIC)
            ox, oy = (capa.width - W) // 2, int((capa.height - H) * (y + 100) / H)
            capa = capa.crop((ox, oy, ox + W, oy + H))
        if alfa < 1: capa.putalpha(capa.getchannel('A').point(lambda p: int(p * alfa)))
        img.paste(capa, (0, 0), capa)
        if k < .09: img.paste(Image.blend(img, Image.new('RGB', (W, H), WHITE), .55))
        return k
    return None

def cuadro(i):
    t = i / FPS
    fr = Image.open(archivos[i]).convert('RGB')
    k = None
    for a, b, *_ in FRASES:
        if a <= t: k = t - a
    zoom = 1 + .08 * math.exp(-k * 5) if k is not None else 1
    if zoom > 1.002:
        fr = fr.resize((int(W * zoom), int(H * zoom)), Image.BICUBIC)
        ox, oy = (fr.width - W) // 2, (fr.height - H) // 2; fr = fr.crop((ox, oy, ox + W, oy + H))
    img = gradear(fr)
    d = ImageDraw.Draw(img)
    if t < .8:  # logo grande que entra con destello
        p = min(1, t / .35); e = 1 - (1 - p) ** 3
        lg = logo_a(int(560 * (1.35 - .35 * e)))
        img.paste(Image.blend(img, negro, .55 * (1 - t / .8)))
        img.paste(lg, ((W - lg.width) // 2, (H - lg.height) // 2 - 120), lg)
        if t < .08: img.paste(Image.blend(img, Image.new('RGB', (W, H), WHITE), .7))
    else:
        img.paste(logo_chico, (22, 26), logo_chico)
        d.rectangle((W - 230, 46, W - 24, 92), fill=(0, 0, 0)); d.rectangle((W - 230, 46, W - 224, 92), fill=RED)
        centro(d, 52, "TOCOPILLA", barlow(34), GOLD, cx=W - 124)
    frase(img, t)
    d = ImageDraw.Draw(img)
    p = t / DUR_V
    d.rectangle((0, H - 10, W, H), fill=(20, 20, 22))
    d.rectangle((0, H - 10, int(W * p * .7), H), fill=RED); d.rectangle((int(W * p * .7), H - 10, int(W * p), H), fill=GOLD)
    return img

def cierre(ultimo, k):
    img = ImageEnhance.Brightness(ultimo.filter(ImageFilter.GaussianBlur(18))).enhance(.14)
    d = ImageDraw.Draw(img)
    e = 1 - (1 - min(1, k / .45)) ** 3
    lg = logo_a(int(420 * (1.25 - .25 * e)))
    img.paste(lg, ((W - lg.width) // 2, 90 + int(40 * (1 - e))), lg)
    centro(d, 410, "ÚNETE AL", rubik(84), WHITE)
    centro(d, 494, "EQUIPO WGYM", rubik(86), RED)
    if k > .5:
        centro(d, 640, "TODO EN TU CELULAR", barlow(38), GOLD)
        centro(d, 686, "TARJETA VIRTUAL · RUTINAS CON QR · APP NUTRICIÓN", barlow(29), (235, 235, 235))
    for i, n in enumerate(("+56 9 9154 0156", "+56 9 7519 6394")):
        if k < .9 + i * .25: continue
        y = 770 + i * 118
        d.rounded_rectangle((100, y, W - 100, y + 92), 46, fill=(31, 142, 78), outline=GOLD, width=5)
        centro(d, y + 10, n, anton(58), WHITE)
    if k > 1.5:
        centro(d, 1010, "WHATSAPP", barlow(34), (220, 255, 225))
        centro(d, 1070, "21 de Mayo 1520, Tocopilla", barlow(42), (230, 230, 230))
        centro(d, 1140, "DONDE HAY CALIDAD NO HAY COMPETENCIA", barlow(30), GOLD)
    d.rectangle((0, 0, W, 10), fill=RED); d.rectangle((0, H - 10, W, H), fill=GOLD)
    if k < .08: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), .6)
    return img

salida = tempfile.mkdtemp(); n = 0
for i in range(len(archivos)):
    cuadro(i).save(os.path.join(salida, '%04d.png' % n)); n += 1
ult = cuadro(len(archivos) - 1)
for j in range(int(CIERRE * FPS)):
    cierre(ult, j / FPS).save(os.path.join(salida, '%04d.png' % n)); n += 1
dur = n / FPS

# ── Pista propia: 128 BPM, bombo, platillo, aplauso, impactos en cada frase y golpe final ──
SR = 44100; N = int(dur * SR) + SR; mix = np.zeros(N)
rng = np.random.default_rng(7)
def poner(sig, t, vol=1.0):
    i = int(t * SR); j = min(N, i + len(sig)); mix[i:j] += sig[:j - i] * vol
def bombo():
    tt = np.arange(int(.45 * SR)) / SR; f = 45 + 110 * np.exp(-tt * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7)
def platillo():
    s = rng.standard_normal(int(.06 * SR)); s = np.diff(s, prepend=0); return s * np.exp(-np.arange(len(s)) / SR * 70) * .25
def aplauso():
    s = rng.standard_normal(int(.18 * SR)); return s * np.exp(-np.arange(len(s)) / SR * 22) * .35
def impacto():
    tt = np.arange(int(1.2 * SR)) / SR; f = 32 + 60 * np.exp(-tt * 6)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3)
    ruido = rng.standard_normal(len(tt)) * np.exp(-tt * 9) * .5
    return sub * 1.2 + ruido
def barrido(lar=.5):
    tt = np.arange(int(lar * SR)) / SR; s = rng.standard_normal(len(tt))
    k = np.linspace(.02, .45, len(tt)); y = np.zeros(len(tt)); acc = 0
    for i in range(len(tt)): acc += k[i] * (s[i] - acc); y[i] = acc
    return y * np.sin(np.pi * tt / lar) * 1.6
beat = 60 / 128; t = .8; b = 0
while t < DUR_V:
    poner(bombo(), t, .95)
    poner(platillo(), t + beat / 2, .9)
    if b % 2 == 1: poner(aplauso(), t, .8)
    t += beat; b += 1
for a, *_ in FRASES:
    if a < DUR_V: poner(barrido(.45), max(0, a - .45), .7); poner(impacto(), a, .9)
poner(impacto(), 0, 1.0); poner(barrido(.6), DUR_V - .6, .8); poner(impacto(), DUR_V, 1.1)
mix = np.tanh(mix * 1.3); mix = mix / (np.abs(mix).max() + 1e-9) * .89
wav = os.path.join(tmp, 'pista.wav')
with wave.open(wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix[:int(dur * SR)] * 32767).astype('<i2').tobytes())

subprocess.run([FF, '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(salida, '%04d.png'), '-i', wav,
                '-map', '0:v', '-map', '1:a', '-t', '%.3f' % dur, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)
print(out, round(dur, 2), 's')
