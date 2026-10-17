"""Arma el video y el GIF de una máquina con el diseño WGYM ADN SPORT.

Uso: python3 scripts/video-maquina.py maquinas-wgymadnsport/<hombre|mujer>/<maquina>
Lee <maquina>/config.json y deja <maquina>/<maquina>.mp4 y .gif.

Diseño (igual para todas las máquinas):
- Video vertical 720x1280. Si la fuente no es vertical 9:16, se centra sobre
  un fondo difuminado y oscurecido de ella misma.
- Logo oficial (maquinas-wgymadnsport/comun/logo.png) arriba a la derecha, 320 px.
- Franja inferior negra con línea roja, título en Rubik Distressed y
  series en Anton dorado.
- En las partes con "musculo", el músculo que se trabaja parpadea en rojo
  (2 veces por segundo) solo sobre la piel, siguiendo el movimiento.

config.json:
  titulo, series
  partes: lista en orden; cada una con video, desde, hasta (segundos),
    repetir (opcional; la última parte se repite y su vuelta se empalma sola),
    recorte (opcional): [x, y, ancho, alto] para recortar la fuente antes,
    encoger (opcional, ej. 0.84): achica el video y lo baja, para que el logo
      no tape algo que llega arriba (discos sobre la cabeza),
    encaje (opcional): {"alto", "x", "y"} pega la fuente (ya recortada) con ese
      alto, sin deformarla, en esa posición sobre su fondo difuminado,
    musculo (opcional): [[cx, cy, rx, ry], ...] óvalos en px de 720x1280,
    solo_piel (opcional, true): false si el músculo está bajo ropa oscura (glúteos): pinta solo lo oscuro;
      "todo" pinta piel y ropa por igual,
    seguir (opcional): [y0, y1, x0, x1] zona con textura a media
      resolución para seguir el movimiento del músculo.
    short_oscuro (opcional): [x0, y0, x1, y1] zona (720x1280) donde está el
      short negro; en cada cuadro se busca la mancha oscura más grande y se
      pinta esa (sin 'musculo'). Sigue los glúteos aunque se muevan mucho.
      intensidad (opcional, 1 = normal): menos de 1 deja el rojo más sutil.
    muslos (opcional, con short_oscuro): true pinta los muslos (cuádriceps)
      bajo el short en vez del short; los óvalos van de pie (bajo el short) a
      sentadilla (muslo hacia la rodilla) según cuánto baja el short.
    espejo_muslos (opcional): [x0, y0, x1, y1] zona (720x1280) del short negro
      del REFLEJO en el espejo (persona de frente); pinta sus cuádriceps: bajo
      el short de pie y a los costados del short en sentadilla.
    musculo_kf (opcional): [[cuadro, cx, cy, rx, ry, (cx2, cy2, rx2, ry2...)], ...] óvalos marcados a mano
      en algunos cuadros (720x1280) e interpolado entre ellos; pinta solo piel
      y respeta 'intensidad'. El más preciso cuando el músculo es chico.
    espejo_bajo (opcional): [x0, y0, x1, y1] igual que espejo_muslos pero solo
      pinta una franja corta justo bajo el short del reflejo (zancadas; elige la
      mancha oscura más baja y ancha, así no toma mancuernas) y respeta
      'intensidad'. Si el reflejo queda tapado, ese cuadro va sin rojo.

Requiere: pip install imageio-ffmpeg pillow numpy scipy
"""
import shutil
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


def leer_frames(path, desde, hasta, recorte=None):
    tmp = tempfile.mkdtemp()
    vf = ['-vf', 'crop=%d:%d:%d:%d' % (recorte[2], recorte[3], recorte[0], recorte[1])] if recorte else []
    subprocess.run([FF, '-v', 'error', '-ss', str(desde), '-t', str(hasta - desde),
                    '-i', path, '-map', '0:v:0', '-an', '-r', str(FPS)] + vf + [
                    os.path.join(tmp, '%04d.png')], check=True)
    fr = [Image.open(f).convert('RGB') for f in sorted(glob.glob(os.path.join(tmp, '*.png')))]
    shutil.rmtree(tmp, ignore_errors=True)
    return fr


def a_vertical(im, encoger=None, encaje=None):
    if encaje:  # {"alto", "x", "y"}: pega la fuente con ese alto (sin deformar) sobre su fondo difuminado
        fh = encaje['alto']; fg = im.resize((int(im.width * fh / im.height), fh), Image.LANCZOS)
        bg = ImageEnhance.Brightness(im.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))).enhance(0.45)
        bg.paste(fg, (encaje['x'], encaje['y']))
        return bg
    if encoger:  # achica el video (ej. 0.84) para que el logo no tape lo de arriba
        fg = im.resize((int(W * encoger), int(H * encoger)), Image.LANCZOS)
        bg = ImageEnhance.Brightness(im.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30))).enhance(0.45)
        bg.paste(fg, ((W - fg.width) // 2, H - fg.height - int(H * (1 - encoger) * 0.15)))
        return bg
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


def musculo_rojo(fr, ovalos, off, i, solo_piel=True, fuerza=1.0):
    a = np.array(fr).astype(np.float32)
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    if solo_piel == 'todo':  # pinta piel y ropa por igual (espalda con peto, face pull)
        piel = np.ones((H, W), bool)
    else:
        piel = ((R > 85) & (G > 45) & (B > 25) & (R - G > 12) & (R - B > 22)) if solo_piel else ((R + G + B) / 3 < 75)  # ropa oscura
    yy, xx = np.mgrid[0:H, 0:W]
    m = np.zeros((H, W), np.float32)
    for cx, cy, rx, ry in ovalos:
        e = ((xx - cx - off[1]) / rx) ** 2 + ((yy - cy - off[0]) / ry) ** 2
        m = np.maximum(m, np.clip(1.3 - e, 0, 1))
    m = ndimage.gaussian_filter(m * piel, 4)
    k = (0.25 + 0.5 * (0.5 + 0.5 * math.sin(2 * math.pi * i / 12))) * m
    if solo_piel == 'todo':  # sobre ropa negra el rojo se pierde: más fuerte
        k = np.clip(k * 1.45, 0, 0.95)
    k = k * fuerza
    for c, v in enumerate((235, 20, 30)):
        a[:, :, c] = a[:, :, c] * (1 - k) + v * k
    return Image.fromarray(a.clip(0, 255).astype('uint8'))


def mancha_short(fr, zona):
    x0, y0, x1, y1 = zona
    a = np.array(fr)
    reg = np.zeros((H, W), bool)
    reg[y0:y1, x0:x1] = a[y0:y1, x0:x1].max(2) < 60
    reg = ndimage.binary_opening(reg, np.ones((17, 17)))
    lab, n = ndimage.label(reg)
    if not n:
        return None
    return ndimage.binary_fill_holes(lab == 1 + int(np.argmax(ndimage.sum(reg, lab, range(1, n + 1)))))


def pintar_muslos(frames, zona):
    sh = [mancha_short(f, zona) for f in frames]
    info = []
    for m in sh:
        ys, xs = np.where(m)
        info.append((np.percentile(ys, 97), np.percentile(xs, 5), np.percentile(xs, 97)))
    yb = ndimage.uniform_filter1d(np.array([v[0] for v in info]), 5)
    lo, hi = np.percentile(yb, 5), np.percentile(yb, 95)
    yy, xx = np.mgrid[0:H, 0:W]
    out = []
    for i, f in enumerate(frames):
        _, xl, xr = info[i]; b = yb[i]; w = xr - xl
        d = float(np.clip((b - lo) / max(hi - lo, 1), 0, 1))
        L = lambda s, e: s + (e - s) * d
        ovs = [(L(xl + 0.75 * w, xr + 55), L(b + 75, b + 5), L(28, 75), L(70, 30)),
               (L(xl + 0.22 * w, xl + 0.3 * w), L(b + 75, b + 20), L(28, 30), L(70, 25))]
        e = np.zeros((H, W), np.float32)
        for cx, cy, rx, ry in ovs:
            e = np.maximum(e, np.clip(1.3 - (((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2), 0, 1))
        a = np.array(f).astype(np.float32); R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        piel = (R > 90) & (B > 45) & (R - G > 10) & (R - B > 25) & ((G - B) < 60)
        piel = ndimage.binary_closing(piel, np.ones((9, 9))) & ~ndimage.binary_dilation(sh[i], iterations=2)
        m = ndimage.gaussian_filter(e * piel, 3)
        k = np.clip((0.25 + 0.5 * (0.5 + 0.5 * math.sin(2 * math.pi * i / 12))) * m * 1.3, 0, 0.9)
        for c, v in enumerate((235, 20, 30)):
            a[:, :, c] = a[:, :, c] * (1 - k) + v * k
        out.append(Image.fromarray(a.clip(0, 255).astype('uint8')))
    return out


def pintar_espejo(frames, zona):
    x0, y0, x1, y1 = zona
    inf = []
    for f in frames:
        a = np.array(f)
        reg = np.zeros((H, W), bool)
        reg[y0:y1, x0:x1] = a[y0:y1, x0:x1].max(2) < 55
        reg = ndimage.binary_opening(reg, np.ones((7, 7)))
        lab, n = ndimage.label(reg)
        m = lab == 1 + int(np.argmax(ndimage.sum(reg, lab, range(1, n + 1))))
        ys, xs = np.where(m)
        inf.append((np.percentile(ys, 95), np.percentile(xs, 3), np.percentile(xs, 97), m))
    ybs = ndimage.uniform_filter1d(np.array([v[0] for v in inf]), 5)
    lo, hi = np.percentile(ybs, 5), np.percentile(ybs, 95)
    out = []
    for i, f in enumerate(frames):
        _, xl, xr, m = inf[i]; yb = ybs[i]
        d = float(np.clip((yb - lo) / max(hi - lo, 1), 0, 1))
        L = lambda s, e: int(s + (e - s) * d)
        a = np.array(f).astype(np.float32); R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        piel = (R > 110) & (B > 60) & (R - G > 12) & (R - B > 30) & ((G - B) < 60)
        z = np.zeros((H, W), bool)
        z[L(yb - 5, yb - 35):L(yb + 50, yb + 12), L(xl - 5, xl - 45):L(xr + 5, xr + 45)] = True
        q = ndimage.binary_opening(piel & z & ~ndimage.binary_dilation(m, iterations=1), np.ones((3, 3)))
        q = ndimage.gaussian_filter(q.astype(np.float32), 1.5)
        k = np.clip((0.3 + 0.55 * (0.5 + 0.5 * math.sin(2 * math.pi * i / 12))) * q * 1.3, 0, 0.92)
        for c, v in enumerate((235, 20, 30)):
            a[:, :, c] = a[:, :, c] * (1 - k) + v * k
        out.append(Image.fromarray(a.clip(0, 255).astype('uint8')))
    return out


def pintar_espejo_bajo(frames, zona, fuerza=1.0):
    """Cuádriceps del reflejo (zancadas). El top del reflejo siempre se ve, el short a veces lo tapa el
    muslo: se ubica el top (mancha oscura ancha más alta) y el short a la distancia top-short medida en
    los cuadros donde se ven los dos."""
    x0, y0, x1, y1 = zona
    tops, dist = [], []
    for f in frames:
        a = np.array(f)
        reg = np.zeros((H, W), bool)
        reg[y0:y1, x0:x1] = a[y0:y1, x0:x1].max(2) < 55
        reg = ndimage.binary_opening(reg, np.ones((5, 5)))
        lab, n = ndimage.label(reg)
        anchas = []
        for k in range(1, n + 1):
            ys, xs = np.where(lab == k)
            if len(ys) < 120 or xs.max() >= x1 - 2 or xs.max() - xs.min() < 30:
                continue
            anchas.append((ys.min(), np.percentile(ys, 95), np.percentile(xs, 5), np.percentile(xs, 95)))
        anchas.sort()
        tops.append(anchas[0] if anchas else None)
        if len(anchas) >= 2 and anchas[1][0] - anchas[0][1] > 5:
            dist.append(anchas[1][1] - anchas[0][1])
    D = float(np.median(dist)) if dist else 60.0
    ys0 = np.array([t[0] if t else np.nan for t in tops])
    out = []
    for i, f in enumerate(frames):
        t = tops[i]
        vec = ys0[max(0, i - 12):i + 13]
        if t is None or abs(t[0] - np.nanmedian(vec)) > 25:  # reflejo tapado o mancha ajena
            out.append(f); continue
        yb = t[1] + D; xl, xr = t[2], t[3]
        a = np.array(f).astype(np.float32)
        R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        piel = (R > 110) & (B > 70) & (R - G > 15) & (R - B > 35) & ((G - B) < 50)
        z = np.zeros((H, W), bool)
        z[int(yb - 3):int(yb + 24), int(xl + 3):int(xr - 3)] = True
        q = ndimage.gaussian_filter((piel & z).astype(np.float32), 2)
        k = np.clip((0.3 + 0.55 * (0.5 + 0.5 * math.sin(2 * math.pi * i / 12))) * q * fuerza, 0, 0.9)
        for ch, v in enumerate((235, 20, 30)):
            a[:, :, ch] = a[:, :, ch] * (1 - k) + v * k
        out.append(Image.fromarray(a.clip(0, 255).astype('uint8')))
    return out


def short_rojo(fr, zona, i, fuerza=1.0):
    a = np.array(fr).astype(np.float32)
    m = mancha_short(fr, zona)
    if m is None:
        return fr
    ys = np.where(m.any(1))[0]
    m[:ys[0] + int(0.18 * (ys[-1] - ys[0]))] = False  # sin la pretina
    m = ndimage.gaussian_filter(m.astype(np.float32), 3)
    k = np.clip((0.25 + 0.5 * (0.5 + 0.5 * math.sin(2 * math.pi * i / 12))) * m * 1.45 * fuerza, 0, 0.95)
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
    logo = Image.open(os.path.join(REPO, 'maquinas-wgymadnsport/comun/logo.png')).convert('RGBA')
    logo = logo.resize((320, int(320 * logo.height / logo.width)), Image.LANCZOS)
    capa.alpha_composite(logo, (W - 320 - 12, 16))
    return capa


def main(carpeta):
    cfg = json.load(open(os.path.join(carpeta, 'config.json'), encoding='utf-8'))
    marca = capa_marca(cfg['titulo'], cfg['series'])
    X = 8  # cuadros de fundido entre partes
    secuencia, extra = [], []
    for n, p in enumerate(cfg['partes']):
        fr = [a_vertical(f, p.get('encoger'), p.get('encaje')) for f in leer_frames(os.path.join(carpeta, p['video']), p['desde'], p['hasta'], p.get('recorte'))]
        if p.get('repetir') and n == len(cfg['partes']) - 1:
            m = len(fr) - X
            fr = [Image.blend(fr[m + i], fr[i], (i + 1) / (X + 1)) if i < X else fr[i] for i in range(m)]
        if p.get('musculo_kf'):
            kf = np.array(sorted(p['musculo_kf']), dtype=float)
            fz = p.get('intensidad', 1.0)
            nov = (kf.shape[1] - 1) // 4  # varios óvalos por fila: [cuadro, cx, cy, rx, ry, cx2, cy2, ...]
            fr = [musculo_rojo(f, [[np.interp(i, kf[:, 0], kf[:, 1 + 4 * o + c]) for c in range(4)] for o in range(nov)],
                               (0, 0), i, True, fz) for i, f in enumerate(fr)]
        elif p.get('espejo_bajo'):
            fr = pintar_espejo_bajo(fr, p['espejo_bajo'], p.get('intensidad', 1.0))
        elif p.get('espejo_muslos'):
            fr = pintar_espejo(fr, p['espejo_muslos'])
        elif p.get('short_oscuro') and p.get('muslos'):
            fr = pintar_muslos(fr, p['short_oscuro'])
        elif p.get('short_oscuro'):
            fr = [short_rojo(f, p['short_oscuro'], i, p.get('intensidad', 1.0)) for i, f in enumerate(fr)]
        elif p.get('musculo'):
            offs = seguir(fr, p.get('seguir'))
            fr = [musculo_rojo(f, p['musculo'], offs[i], i, p.get('solo_piel', True)) for i, f in enumerate(fr)]
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
    pal = g[-min(20, len(g))].quantize(colors=160, method=Image.Quantize.MEDIANCUT)
    q = [x.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG) for x in g]
    q[0].save(os.path.join(carpeta, nombre + '.gif'), save_all=True, append_images=q[1:],
              duration=int(2000 / FPS), loop=0, optimize=True)
    shutil.rmtree(tmp, ignore_errors=True)  # los PNG temporales llenaban el disco
    print('Listo:', nombre + '.mp4', nombre + '.gif', len(unico + extra), 'cuadros')


if __name__ == '__main__':
    main(sys.argv[1])
