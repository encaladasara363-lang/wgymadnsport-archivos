#!/usr/bin/env python3
"""
Arma los tres carteles con el QR de cada app de entrenamiento, uno por
rutina, usando el mismo diseño de los carteles de QR que ya están hechos.

    python3 herramientas/generar-qr-apps.py

Deja qr-app-mujeres.html, qr-app-hombres.html y qr-app-gluteos.html, listos
para abrir e imprimir (Ctrl+P → Guardar como PDF).
"""
import base64, io, json, os, re, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://encaladasara363-lang.github.io/wgymadnsport-archivos/"
BASE = "qr-rutina-mujeres.html"       # el cartel que sirve de molde

CARTELES = {
    "mujeres": {
        "titulo": "QR App Rutina Mujeres",
        "h1": 'MI RUTINA<br><span>MUJERES</span>',
        "sub": "APP · ANOTA TUS PESOS",
    },
    "hombres": {
        "titulo": "QR App Rutina Hombres",
        "h1": 'MI RUTINA<br><span>HOMBRES</span>',
        "sub": "APP · ANOTA TUS PESOS",
    },
    "gluteos": {
        "titulo": "QR App Rutina Glúteos",
        "h1": 'MI RUTINA<br><span>GLÚTEOS</span>',
        "sub": "APP · ANOTA TUS PESOS",
    },
}


def dias_de(clave):
    """Los días salen de la propia app, para que el cartel nunca diga una
    cosa distinta de lo que el socio se va a encontrar adentro."""
    s = io.open(os.path.join(RAIZ, "entrenar-%s.html" % clave), encoding="utf-8").read()
    m = re.search(r"var RUTINAS = (\{.*?\n\});\n", s, re.S)
    o = json.loads(m.group(1))[clave]
    return "".join(
        '<div class="dia"><span class="d">%s</span><span class="t">%s</span></div>'
        % (d["weekday"].upper(), d["title"]) for d in o["DAYS"])


def qr_png(url):
    """El QR con el logo al medio, igual que los otros carteles. Se usa
    corrección de errores alta para que aguante el logo encima."""
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
    from PIL import Image
    q = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_H,
                      box_size=18, border=2)
    q.add_data(url); q.make(fit=True)
    img = q.make_image(fill_color="#0D0D0F", back_color="white").convert("RGB")
    logo = Image.open(os.path.join(RAIZ, "assets/logo.jpg")).convert("RGB")
    lado = img.size[0] // 5
    logo = logo.resize((lado, lado), Image.LANCZOS)
    marco = Image.new("RGB", (lado + 22, lado + 22), "white")
    marco.paste(logo, (11, 11))
    img.paste(marco, ((img.size[0] - marco.size[0]) // 2,
                      (img.size[1] - marco.size[1]) // 2))
    buf = io.BytesIO(); img.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode(), img


def main():
    base = io.open(os.path.join(RAIZ, BASE), encoding="utf-8").read()
    import cv2, numpy as np
    for clave, cfg in CARTELES.items():
        url = SITIO + "entrenar-%s.html" % clave
        b64, img = qr_png(url)

        # el QR tiene que poder leerse de verdad, no solo verse bonito
        arr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        leido, _, _ = cv2.QRCodeDetector().detectAndDecode(arr)
        if leido != url:
            sys.exit("El QR de %s no se deja leer: %r" % (clave, leido))

        s = base
        s = re.sub(r"<title>[^<]*</title>",
                   "<title>%s · WGYMADNSPORT Tocopilla</title>" % cfg["titulo"], s, count=1)
        s = re.sub(r"<h1>.*?</h1>", "<h1>%s</h1>" % cfg["h1"], s, count=1, flags=re.S)
        s = re.sub(r'<div class="sub">[^<]*</div>',
                   '<div class="sub">%s</div>' % cfg["sub"], s, count=1)
        s = re.sub(r'(<div class="qr"><img src="data:image/png;base64,)[A-Za-z0-9+/=]+(")',
                   lambda m: m.group(1) + b64 + m.group(2), s, count=1)
        s = re.sub(r'alt="QR[^"]*"', 'alt="QR de la app %s"' % clave, s, count=1)
        s = re.sub(r'<div class="dias">.*?</div></div>',
                   '<div class="dias">%s</div>' % dias_de(clave), s, count=1, flags=re.S)
        s = re.sub(r"<p>Cada ejercicio.*?</p>",
                   "<p>Anota <b>tus pesos y repeticiones</b> en cada serie y la app "
                   "te lleva la cuenta.<br>Trae videos, descanso con alarma y tus récords."
                   "<br><b>Solo para socios con la mensualidad al día.</b></p>", s,
                   count=1, flags=re.S)

        destino = os.path.join(RAIZ, "qr-app-%s.html" % clave)
        io.open(destino, "w", encoding="utf-8").write(s)
        print("  qr-app-%s.html  %.0f KB  ->  %s" % (clave, len(s.encode()) / 1024, url))


if __name__ == "__main__":
    main()
