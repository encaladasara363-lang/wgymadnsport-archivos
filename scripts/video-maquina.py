"""Arma el video y el GIF de una máquina con el diseño WGYM ADN SPORT.

Uso: python3 scripts/video-maquina.py videos-maquinas/<maquina>
Lee <maquina>/config.json y deja <maquina>/<maquina>.mp4 y .gif.

Diseño (igual para todas las máquinas):
- Video vertical 720x1280. Si la fuente no es vertical 9:16, se centra sobre
  un fondo difuminado y oscurecido de ella misma.
- Logo oficial (videos-maquinas/comun/logo.png) arriba a la derecha, 320 px.
- Franja inferior negra con línea roja, título en Rubik Distressed y
  series en Anton dorado.
- En las partes con "musculo", el músculo que se trabaja parpadea en rojo
  (2 veces por segundo) solo sobre la piel, siguiendo el movimiento.

config.json:
  titulo, series
  partes: lista en orden; cada una con video, desde, hasta (segundos),
    repetir (opcional; la última parte se repite y su vuelta se empalma sola),
    musculo (opcional): [[cx, cy, rx, ry], ...] óvalos en px de 720x1280,
    seguir (opcional): [y0, y1, x0, x1] zona con textura a media
      resolución para seguir el movimiento del músculo.

Requiere: pip install imageio-ffmpeg pillow numpy scipy
"""
import json, math, os, subprocess, sys, tempfile, glob
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import imageio_ffmpeg

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 720, 1280, 24
RED = (227, 6, 19); GOLD = (212, 175, 55)
font = lambda f, s: ImageFont.truetype(os.path.join(REPO, f), s)
rubik = lambda s: font('assets/font-rubik-distressed.ttf', s)
anton = lambda s: font('contenido/fuentes/Anton.ttf', s)


def leer_frames(path, desde, hasta):
    tmp = tempfile.mkdtemp()
    subprocess.run([FF, '-v', 'error', '-ss', str(desde), '-t', str(hasta - desde),
                    '-i', path, '-map', '0:v:0', '-an', '-r', str(FPS),
                    os.path.join(tmp, '%04d.png')], check=True)
    return [Image.open(f).convert('RGB') for f in sorted(glob.glob(os.path.join(tmp, '*.png')))]


def a_vertical(im):
    if abs(im.width / im.height - W / H) < 0.02:
        return im.resize((W, H), Image.LANCZOS)
    fg = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS)
    bg = im.resize((int(H * im.width / im.height), H), Image.LANCZOS)
    l = (bg.width - W) // 2
    bg = bg.crop((l, 0, l + W, H)).filter(ImageFilter.GaussianBlur(30))
    bg = ImageEnhance.Brightness(bg).enhance(0.45)
    bg.paste(fg, (0, (H - fg.height) // 2 + 30))
    return bg


def seguir(frames, zona):
    if not zona:
        return [(0, 0)] * len(frames)
    gray = lambda im: np.array(im.convert('L').resize((W // 2, H // 2)), dtype=np.float32)
    y0, y1, x0, x1 = zona
    T = gray(frames[0])[y0:y1, x0:x1]; T = T - T.mean()
    offs, prev = [(0, 0)], (0, 0)
    for fr in frames[1:]:
        g = gray(fr); best = None
        for dy in range(prev[0] - 6, prev[0] + 7):
            for dx in range(prev[1] - 6, prev[1] + 7):
                P = g[y0 + dy:y1 + dy, x0 + dx:x1 + dx]
                if P.shape != T.shape: continue
                v = (((P - P.mean()) - T) ** 2).mean()
                if best is None or v < best[0]: best = (v, dy, dx)
        prev = (best[1], best[2]); offs.append(prev)
    return [(dy * 2, dx * 2) for dy, dx in offs]


def musculo_rojo(fr, ovalos, off, i):
    a = np.array(fr).astype(np.float32)
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    piel = (R > 85) & (G > 45) & (B > 25) & (R - G > 12) & (R - B > 22)
    yy, xx = np.mgrid[0:H, 0:W]
    m = np.zeros((H, W), np.float32)
    for cx, cy, rx, ry in ovalos:
        e = ((xx - cx - off[1]) / rx) ** 2 + ((yy - cy - off[0]) / ry) ** 2
        m = np.maximum(m, np.clip(1.3 - e, 0, 1))
    m = ndimage.gaussian_filter(m * piel, 4)
    k = (0.25 + 0.5 * (0.5 + 0.5 * math.sin(2 * math.pi * i / 12))) * m
    for c, v in enumerate((235, 20, 30)):
        a[:, :, c] = a[:, :, c] * (1 - k) + v * k
    return Image.fromarray(a.clip(0, 255).astype('uint8'))


def capa_marca(titulo, series):
    capa = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(capa)
    for y in range(1060, H):
        d.line([(0, y), (W, y)], fill=(10, 10, 11, int(min(1, (y - 1060) / 70) * 230)))
    d.rectangle([0, 1122, W, 1127], fill=RED + (255,))
    tam = 50
    while d.textlength(titulo, font=rubik(tam)) > W - 40: tam -= 2
    d.text((W // 2, 1172), titulo, font=rubik(tam), fill=(255, 255, 255, 255), anchor='mm')
    d.text((W // 2, 1236), series, font=anton(46), fill=GOLD + (255,), anchor='mm')
    logo = Image.open(os.path.join(REPO, 'videos-maquinas/comun/logo.png')).convert('RGBA')
    logo = logo.resize((320, int(320 * logo.height / logo.width)), Image.LANCZOS)
    capa.alpha_composite(logo, (W - 320 - 12, 16))
    return capa


def main(carpeta):
    cfg = json.load(open(os.path.join(carpeta, 'config.json'), encoding='utf-8'))
    marca = capa_marca(cfg['titulo'], cfg['series'])
    X = 8  # cuadros de fundido entre partes
    secuencia, extra = [], []
    for n, p in enumerate(cfg['partes']):
        fr = [a_vertical(f) for f in leer_frames(os.path.join(carpeta, p['video']), p['desde'], p['hasta'])]
        if p.get('repetir') and n == len(cfg['partes']) - 1:
            m = len(fr) - X
            fr = [Image.blend(fr[m + i], fr[i], (i + 1) / (X + 1)) if i < X else fr[i] for i in range(m)]
        if p.get('musculo'):
            offs = seguir(fr, p.get('seguir'))
            fr = [musculo_rojo(f, p['musculo'], offs[i], i) for i, f in enumerate(fr)]
        vuelta = list(fr)
        if secuencia:
            fr[:X] = [Image.blend(secuencia[-X + i], fr[i], (i + 1) / (X + 1)) for i in range(X)]
            secuencia = secuencia[:-X]
        secuencia += fr
        if p.get('repetir'):
            extra = vuelta * (p['repetir'] - 1)
    unico = [Image.alpha_composite(f.convert('RGBA'), marca).convert('RGB') for f in secuencia]
    extra = [Image.alpha_composite(f.convert('RGBA'), marca).convert('RGB') for f in extra]
    nombre = os.path.basename(os.path.normpath(carpeta))
    tmp = tempfile.mkdtemp()
    for i, f in enumerate(unico + extra): f.save(os.path.join(tmp, '%04d.png' % i))
    subprocess.run([FF, '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, '%04d.png'),
                    '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                    os.path.join(carpeta, nombre + '.mp4')], check=True)
    g = [f.resize((360, 640), Image.LANCZOS) for f in unico[::2]]
    pal = g[-20].quantize(colors=160, method=Image.Quantize.MEDIANCUT)
    q = [x.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG) for x in g]
    q[0].save(os.path.join(carpeta, nombre + '.gif'), save_all=True, append_images=q[1:],
              duration=int(2000 / FPS), loop=0, optimize=True)
    print('Listo:', nombre + '.mp4', nombre + '.gif', len(unico + extra), 'cuadros')


if __name__ == '__main__':
    main(sys.argv[1])
