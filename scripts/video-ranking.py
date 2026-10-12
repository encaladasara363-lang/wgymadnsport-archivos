"""Video publicitario del 🏆 Ranking del mes (12-10-2026, pedido de la dueña).

Uso: python3 scripts/video-ranking.py <salida.mp4>

Animación vertical 720x1280 a 30 cuadros, sin video de fuente: logo, trofeo, "¿QUIÉN ENTRENA
MÁS?", contador de días, podio con "¿TÚ?" en el 1.er lugar, los 3 rankings por plan, cómo
unirse desde la tarjeta virtual y cierre con los DOS WhatsApp (regla de CLAUDE.md). Pista
de audio propia sintetizada (sin canciones con derechos). Nunca muestra apodos ni nombres
reales de socios.
"""
import os, sys, subprocess, tempfile, math, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 720, 1280, 30
RED = (227, 6, 19); GOLD = (212, 175, 55); WHITE = (255, 255, 255)
PLATA = (192, 196, 204); BRONCE = (205, 127, 50); OSCURO = (10, 10, 11)
F = lambda f, s: ImageFont.truetype(os.path.join(REPO, f), s)
rubik = lambda s: F('assets/font-rubik-distressed.ttf', s)
anton = lambda s: F('contenido/fuentes/Anton.ttf', s)
barlow = lambda s: F('contenido/fuentes/BarlowCondensed.ttf', s)

# Escenas (inicio en segundos). El audio pone un impacto al comienzo de cada una.
ESC = [0.0, 2.4, 5.4, 9.8, 12.8, 15.6]
DUR = 19.8
out = sys.argv[1]

logo = Image.open(os.path.join(REPO, 'maquinas-wgymadnsport/comun/logo.png')).convert('RGBA')
def logo_a(ancho): return logo.resize((ancho, int(ancho * logo.height / logo.width)), Image.LANCZOS)
LOGO_CHICO = logo_a(190)

def ease(p): p = max(0, min(1, p)); return 1 - (1 - p) ** 3
def rebote(p):
    p = max(0, min(1, p))
    return 1 + 2.2 * (p - 1) ** 3 + 1.2 * (p - 1) ** 2 if p < 1 else 1

def centro(d, y, txt, fnt, fill, cx=W / 2, sombra=True):
    w = d.textlength(txt, font=fnt)
    if sombra: d.text((cx - w / 2 + 4, y + 4), txt, font=fnt, fill=(0, 0, 0))
    d.text((cx - w / 2, y), txt, font=fnt, fill=fill)

def ajustar(txt, tam, maxw, fn=rubik):
    f = fn(tam)
    while ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(txt, font=f) > maxw and tam > 30:
        tam -= 3; f = fn(tam)
    return f

def golpe(img, d, y, txt, tam, color, k, maxw=660):
    """Texto que entra grande y se asienta (golpe de zoom)."""
    if k < 0: return
    f = ajustar(txt, tam, maxw)
    s = 1 + .6 * math.exp(-k * 9)
    if s > 1.02:
        f2 = ajustar(txt, int(tam * s), maxw * s)
        capa = Image.new('RGBA', (W, 400), (0, 0, 0, 0)); dc = ImageDraw.Draw(capa)
        centro(dc, 100, txt, f2, color + (int(255 * min(1, k * 6)),))
        img.paste(capa, (0, int(y - 100 - (f2.size - f.size) / 2)), capa)
    else:
        centro(d, y, txt, f, color)

# Fondo: negro con brillo rojo y franjas diagonales que se mueven.
base = Image.new('RGB', (W, H), OSCURO)
glow = Image.new('L', (W, H), 0); g = ImageDraw.Draw(glow)
g.ellipse((-220, -300, W + 220, 520), fill=110); g.ellipse((-200, H - 420, W + 200, H + 300), fill=90)
glow = glow.filter(ImageFilter.GaussianBlur(110))
base = Image.composite(Image.new('RGB', (W, H), (95, 6, 12)), base, glow)
ruido = (np.random.default_rng(3).random((H, W)) * 14).astype(np.uint8)
base = Image.fromarray(np.clip(np.asarray(base).astype(int) + ruido[..., None] - 7, 0, 255).astype(np.uint8))

def fondo(t):
    img = base.copy(); capa = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    off = (t * 60) % 160
    for x in range(-H, W + 160, 160):
        x0 = x + off
        d.polygon([(x0, 0), (x0 + 34, 0), (x0 + 34 + H * .45, H), (x0 + H * .45, H)], fill=(227, 6, 19, 18))
    img.paste(capa, (0, 0), capa)
    return img

def trofeo(d, cx, cy, esc, brillo=0):
    """Trofeo dibujado (copa, asas, pie) en dorado."""
    s = esc
    if s < .08: return
    oro = tuple(min(255, int(c + brillo * 40)) for c in GOLD)
    d.ellipse((cx - 120 * s, cy - 150 * s, cx - 40 * s, cy - 40 * s), outline=oro, width=int(16 * s))
    d.ellipse((cx + 40 * s, cy - 150 * s, cx + 120 * s, cy - 40 * s), outline=oro, width=int(16 * s))
    d.pieslice((cx - 95 * s, cy - 250 * s, cx + 95 * s, cy + 10 * s), 0, 180, fill=oro)
    d.rectangle((cx - 95 * s, cy - 175 * s, cx + 95 * s, cy - 120 * s), fill=oro)
    d.rectangle((cx - 18 * s, cy - 10 * s, cx + 18 * s, cy + 55 * s), fill=oro)
    d.rounded_rectangle((cx - 70 * s, cy + 50 * s, cx + 70 * s, cy + 90 * s), int(8 * s), fill=oro)
    d.rectangle((cx - 90 * s, cy + 88 * s, cx + 90 * s, cy + 112 * s), fill=(150, 118, 30))
    d.ellipse((cx - 55 * s, cy - 165 * s, cx - 25 * s, cy - 95 * s), fill=(255, 240, 180))
    f = anton(int(70 * s)); w = d.textlength("1", font=f)
    d.text((cx - w / 2, cy - 165 * s), "1", font=f, fill=RED)

def confeti(img, t, t0, n=70):
    if t < t0: return
    d = ImageDraw.Draw(img); rng = np.random.default_rng(11); k = t - t0
    for i in range(n):
        x0 = rng.uniform(0, W); v = rng.uniform(260, 520); fase = rng.uniform(0, 6.3)
        y = -40 + v * k - rng.uniform(0, 300); x = x0 + 30 * math.sin(k * 3 + fase)
        if -20 < y < H:
            c = [RED, GOLD, WHITE][i % 3]; a = rng.uniform(5, 11)
            d.rectangle((x, y, x + a, y + a * 1.8), fill=c)

def cabecera(img, d):
    img.paste(LOGO_CHICO, (22, 26), LOGO_CHICO)
    d.rectangle((W - 230, 46, W - 24, 92), fill=(0, 0, 0)); d.rectangle((W - 230, 46, W - 224, 92), fill=RED)
    centro(d, 52, "TOCOPILLA", barlow(34), GOLD, cx=W - 124, sombra=False)

def escena1(img, d, t):  # logo + trofeo + "RANKING DEL MES"
    if t < 1.0:
        p = ease(t / .4); lg = logo_a(int(560 * (1.4 - .4 * p)))
        img.paste(lg, ((W - lg.width) // 2, 420 - lg.height // 2), lg)
    else:
        cabecera(img, d)
        p = rebote((t - 1.0) / .5)
        trofeo(d, W / 2, 520, .9 * p + .01, brillo=math.sin(t * 6))
        golpe(img, d, 700, "RANKING", 150, GOLD, t - 1.25)
        golpe(img, d, 860, "DEL MES", 110, WHITE, t - 1.5)

def escena2(img, d, t):  # ¿QUIÉN ENTRENA MÁS? + contador
    cabecera(img, d)
    golpe(img, d, 230, "¿QUIÉN", 130, WHITE, t)
    golpe(img, d, 370, "ENTRENA MÁS?", 110, RED, t - .25)
    if t > .9:
        k = t - .9
        dias = min(22, int(k / 1.4 * 22) + 1)
        r = 160; cx, cy = W / 2, 760
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(60, 60, 64), width=18)
        d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * dias / 22, fill=GOLD, width=18)
        f = anton(150); w = d.textlength(str(dias), font=f)
        d.text((cx - w / 2, cy - 110), str(dias), font=f, fill=WHITE)
        centro(d, cy + 60, "DÍAS", barlow(44), GOLD, sombra=False)
    if t > 1.6:
        centro(d, 980, "CADA DÍA QUE VIENES", barlow(52), WHITE)
        centro(d, 1040, "SUMA 1 PUNTO", rubik(78), GOLD)

def escena3(img, d, t):  # podio
    cabecera(img, d)
    golpe(img, d, 170, "EL PODIO", 120, GOLD, t)
    golpe(img, d, 300, "TE ESPERA", 96, WHITE, t - .2)
    piso = 1110
    for i, (cx, alto, col, num, retardo) in enumerate(((W / 2 - 215, 300, PLATA, "2", .4),
                                                       (W / 2, 420, GOLD, "1", .7),
                                                       (W / 2 + 215, 230, BRONCE, "3", 1.0))):
        p = ease((t - retardo) / .5)
        if p <= 0: continue
        h = alto * p; x0, x1 = cx - 100, cx + 100
        d.rectangle((x0, piso - h, x1, piso), fill=(28, 28, 32), outline=col, width=6)
        d.rectangle((x0, piso - h, x1, piso - h + 16), fill=col)
        f = anton(110); w = d.textlength(num, font=f)
        d.text((cx - w / 2, piso - h + 40), num, font=f, fill=col)
        if p >= 1 and num == "1":
            k = t - retardo - .5
            pul = 1 + .08 * math.sin(k * 7)
            r = 82 * pul; cy = piso - h - 105
            d.ellipse((cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8), fill=RED)
            d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GOLD)
            f = rubik(int(60 * pul)); bb = d.textbbox((0, 0), "¿TÚ?", font=f)
            d.text((cx - (bb[0] + bb[2]) / 2, cy - (bb[1] + bb[3]) / 2), "¿TÚ?", font=f, fill=OSCURO)
    d.rectangle((40, piso, W - 40, piso + 12), fill=RED)
    confeti(img, t, 1.6)

def escena4(img, d, t):  # 3 rankings
    cabecera(img, d)
    golpe(img, d, 180, "3 RANKINGS", 120, GOLD, t)
    centro(d, 330, "COMPITES CON LOS DE TU PLAN", barlow(44), WHITE) if t > .3 else None
    for i, (txt, sub) in enumerate((("MENSUAL", "FULL · FUNCIONARIOS · ESTUDIANTES…"),
                                    ("TURNO", "PLAN TURNO"),
                                    ("3 VECES", "POR SEMANA"))):
        p = ease((t - .5 - i * .3) / .45)
        if p <= 0: continue
        y = 450 + i * 210; x = -W + W * p
        d.rounded_rectangle((x + 60, y, x + W - 60, y + 170), 26, fill=(24, 24, 28), outline=GOLD, width=5)
        d.rounded_rectangle((x + 60, y, x + 90, y + 170), 14, fill=RED)
        d.text((x + 120, y + 18), txt, font=rubik(82), fill=WHITE)
        d.text((x + 122, y + 112), sub, font=barlow(36), fill=GOLD)

def escena5(img, d, t):  # cómo unirse
    cabecera(img, d)
    golpe(img, d, 170, "ÚNETE CON", 110, WHITE, t)
    golpe(img, d, 300, "TU APODO", 130, RED, t - .2)
    p = ease((t - .5) / .5)
    if p > 0:  # teléfono simple con el cuadro del ranking
        y0 = 470 + int(200 * (1 - p)); x0, x1 = 170, W - 170
        d.rounded_rectangle((x0, y0, x1, y0 + 640), 50, fill=(18, 18, 20), outline=(90, 90, 96), width=8)
        d.rounded_rectangle((x0 + 30, y0 + 50, x1 - 30, y0 + 590), 24, fill=(30, 30, 34), outline=GOLD, width=4)
        centro(d, y0 + 70, "RANKING DEL MES", ajustar("RANKING DEL MES", 40, x1 - x0 - 90), GOLD, sombra=False)
        d.rounded_rectangle((x0 + 60, y0 + 150, x1 - 60, y0 + 225), 14, fill=WHITE)
        escrito = "TU APODO"[:max(0, int((t - 1.0) * 8))]
        cursor = "|" if int(t * 3) % 2 else ""
        d.text((x0 + 80, y0 + 162), escrito + cursor, font=barlow(46), fill=OSCURO)
        boton = t > 2.0
        d.rounded_rectangle((x0 + 60, y0 + 255, x1 - 60, y0 + 335), 16, fill=GOLD if boton else RED)
        centro(d, y0 + 268, "UNIRME", rubik(50), OSCURO if boton else WHITE, sombra=False)
        for i in range(3):
            yy = y0 + 370 + i * 64
            d.rounded_rectangle((x0 + 60, yy, x1 - 60, yy + 50), 10, fill=(44, 44, 50))
            d.text((x0 + 76, yy + 4), "%d°" % (i + 1), font=anton(36), fill=[GOLD, PLATA, BRONCE][i])
    if t > 1.2:
        centro(d, 1150, "DESDE TU TARJETA VIRTUAL", barlow(46), GOLD)

def cierre(img, d, t):
    e = ease(t / .45); lg = logo_a(int(400 * (1.25 - .25 * e)))
    img.paste(lg, ((W - lg.width) // 2, 80 + int(40 * (1 - e))), lg)
    centro(d, 400, "¿VAS POR EL", rubik(84), WHITE)
    centro(d, 490, "PRIMER LUGAR?", ajustar("PRIMER LUGAR?", 90, 640), GOLD)
    if t > .5:
        centro(d, 625, "ENTRENA EN WGYM ADN SPORT", barlow(42), WHITE)
    for i, n in enumerate(("+56 9 9154 0156", "+56 9 7519 6394")):
        if t < .9 + i * .25: continue
        y = 720 + i * 118
        d.rounded_rectangle((100, y, W - 100, y + 92), 46, fill=(31, 142, 78), outline=GOLD, width=5)
        centro(d, y + 10, n, anton(58), WHITE, sombra=False)
    if t > 1.5:
        centro(d, 960, "WHATSAPP", barlow(34), (220, 255, 225), sombra=False)
        centro(d, 1020, "21 de Mayo 1520, Tocopilla", barlow(42), (230, 230, 230))
        centro(d, 1090, "DONDE HAY CALIDAD NO HAY COMPETENCIA", barlow(30), GOLD, sombra=False)

ESCENAS = [escena1, escena2, escena3, escena4, escena5, cierre]

def cuadro(i):
    t = i / FPS
    n = max(j for j, a in enumerate(ESC) if a <= t)
    img = fondo(t); d = ImageDraw.Draw(img)
    ESCENAS[n](img, d, t - ESC[n])
    d = ImageDraw.Draw(img)
    k = t - ESC[n]
    if k < .07: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), .55)
    d = ImageDraw.Draw(img)
    p = t / DUR
    d.rectangle((0, 0, W, 10), fill=RED)
    d.rectangle((0, H - 10, W, H), fill=(20, 20, 22))
    d.rectangle((0, H - 10, int(W * p * .7), H), fill=RED); d.rectangle((int(W * p * .7), H - 10, int(W * p), H), fill=GOLD)
    return img

tmp = tempfile.mkdtemp(); nfr = int(DUR * FPS)
for i in range(nfr):
    cuadro(i).save(os.path.join(tmp, '%04d.png' % i))

# ── Pista propia: 124 BPM, bombo, platillo, aplauso, impacto en cada escena ──
SR = 44100; N = int(DUR * SR) + SR; mix = np.zeros(N)
rng = np.random.default_rng(7)
def poner(sig, t, vol=1.0):
    i = int(t * SR); j = min(N, i + len(sig)); mix[i:j] += sig[:j - i] * vol
def bombo():
    tt = np.arange(int(.45 * SR)) / SR; f = 45 + 110 * np.exp(-tt * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7)
def platillo():
    s = np.diff(rng.standard_normal(int(.06 * SR)), prepend=0); return s * np.exp(-np.arange(len(s)) / SR * 70) * .25
def aplauso():
    s = rng.standard_normal(int(.18 * SR)); return s * np.exp(-np.arange(len(s)) / SR * 22) * .35
def impacto():
    tt = np.arange(int(1.2 * SR)) / SR; f = 32 + 60 * np.exp(-tt * 6)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 3) * 1.2 + rng.standard_normal(len(tt)) * np.exp(-tt * 9) * .5
def campana(f0=1320):
    tt = np.arange(int(.9 * SR)) / SR
    return (np.sin(2 * np.pi * f0 * tt) + .5 * np.sin(2 * np.pi * f0 * 2.01 * tt)) * np.exp(-tt * 5) * .35
beat = 60 / 124; t = .6; b = 0
while t < ESC[-1]:
    poner(bombo(), t, .95); poner(platillo(), t + beat / 2, .9)
    if b % 2 == 1: poner(aplauso(), t, .8)
    t += beat; b += 1
for a in ESC: poner(impacto(), a, 1.0)
for k in range(3): poner(campana(1320 + k * 220), ESC[2] + 1.2 + k * .15, .8)  # podio
poner(campana(1760), ESC[2] + 2.3, .9)
mix = np.tanh(mix * 1.3); mix = mix / (np.abs(mix).max() + 1e-9) * .89
wav = os.path.join(tmp, 'pista.wav')
with wave.open(wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix[:int(DUR * SR)] * 32767).astype('<i2').tobytes())

subprocess.run([FF, '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'), '-i', wav,
                '-map', '0:v', '-map', '1:a', '-t', '%.3f' % DUR, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19',
                '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], check=True)
print(out, DUR, 's')
