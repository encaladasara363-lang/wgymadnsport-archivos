#!/usr/bin/env python3
"""
Arma los tres carteles A4 para imprimir que anuncian las apps de
entrenamiento, uno por rutina.

La idea del cartel: que el socio vea de una que esto es una APP del
gimnasio, no un papel más. Por eso al centro va un celular dibujado con
una captura de verdad de la app adentro, y al lado el QR para bajarla.

    python3 herramientas/generar-cartel-app.py

Deja qr-app-mujeres.html y su PDF, y lo mismo para hombres y glúteos.
"""
import base64, io, json, os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://encaladasara363-lang.github.io/wgymadnsport-archivos/"
# Las capturas de la app que van dentro del celular del cartel. Si la app
# cambia de cara, se sacan de nuevo y se corre este archivo otra vez.
PANTALLAS = os.path.join(RAIZ, "herramientas/pantallas")

CARTELES = {
    "mujeres": {"linea1": "RUTINA PRINCIPIANTE", "linea2": "MUJERES"},
    "hombres": {"linea1": "RUTINA INTERMEDIO",   "linea2": "HOMBRES"},
    "gluteos": {"linea1": "RUTINA ENFOCADA EN",  "linea2": "GLÚTEOS"},
}

VENTAJAS = [
    ("ANOTA TUS KILOS",   "cada serie, y te recuerda lo de la vez pasada"),
    ("DESCANSO CON ALARMA", "el reloj corre solo y suena al terminar"),
    ("TUS RÉCORDS",       "mira cómo vas subiendo semana a semana"),
    ("VIDEO DE CADA EJERCICIO", "para no hacerlo mal nunca más"),
]


def b64(ruta):
    return base64.b64encode(io.open(ruta, "rb").read()).decode()


def qr_png(url):
    """QR con el logo al medio, igual que los otros carteles del gimnasio."""
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
    from PIL import Image
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=18, border=2)
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


def dias_de(clave):
    s = io.open(os.path.join(RAIZ, "entrenar-%s.html" % clave), encoding="utf-8").read()
    m = re.search(r"var RUTINAS = (\{.*?\n\});\n", s, re.S)
    return json.loads(m.group(1))[clave]["DAYS"]


PLANTILLA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>__TITULO__ · WGYMADNSPORT Tocopilla</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Condensed:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root{ --ink:#0D0D0F; --paper:#FCFCFA; --red:#E1061B; --steel:#6E7278; --hairline:#D9D9D6; }
  *{box-sizing:border-box; margin:0; padding:0;}
  body{ background:#E7E7E3; font-family:'Barlow Condensed','Arial Narrow',Arial,sans-serif;
        display:flex; flex-direction:column; align-items:center; padding:40px 16px 60px; }

  .poster{ position:relative; width:794px; height:1123px; background:var(--paper);
           overflow:hidden; box-shadow:0 30px 60px -20px rgba(0,0,0,.35);
           display:flex; flex-direction:column; align-items:center; padding:40px 52px 0; }

  .top-bar{ position:absolute; top:0; left:0; right:0; height:16px; background:var(--ink); }
  .top-bar::after{ content:""; position:absolute; left:0; top:0; height:16px; width:250px; background:var(--red); }
  .bot-bar{ position:absolute; bottom:0; left:0; right:0; height:16px; background:var(--ink); }
  .bot-bar::after{ content:""; position:absolute; right:0; top:0; height:16px; width:250px; background:var(--red); }

  /* ── Encabezado: logo al centro y la marca ───────────────────────── */
  .cab{ display:flex; align-items:center; gap:18px; margin-top:6px; }
  .logo{ width:96px; height:96px; border-radius:50%; overflow:hidden;
         border:4px solid var(--ink); flex-shrink:0; }
  .logo img{ width:100%; height:100%; object-fit:cover; }
  .cab .marca{ text-align:left; }
  .cab .marca b{ display:block; font-family:'Anton','Arial Black',Impact,sans-serif;
                 font-weight:900; font-size:30px; letter-spacing:.02em; color:var(--ink); line-height:1; }
  .cab .marca span{ display:block; margin-top:7px; font-weight:800; letter-spacing:.26em;
                    text-transform:uppercase; font-size:15px; color:var(--steel); }

  /* ── El anuncio ──────────────────────────────────────────────────── */
  .tag{ margin-top:24px; background:var(--red); color:var(--paper);
        font-family:'Anton','Arial Black',Impact,sans-serif; font-weight:900;
        font-size:40px; letter-spacing:.06em; padding:11px 40px;
        transform:skewX(-6deg); box-shadow:9px 9px 0 var(--ink); flex-shrink:0; }
  .tag span{ display:inline-block; transform:skewX(6deg); }

  h1{ margin-top:26px; text-align:center; font-family:'Anton','Arial Black',Impact,sans-serif;
      font-weight:900; font-size:47px; line-height:1.04; color:var(--ink); letter-spacing:0; }
  h1 em{ font-style:normal; color:var(--red); }
  .sub{ margin-top:12px; font-weight:800; letter-spacing:.3em; text-transform:uppercase;
        font-size:17px; color:var(--ink); }

  /* ── Celular + QR ────────────────────────────────────────────────── */
  .medio{ margin-top:18px; display:flex; align-items:flex-start; gap:34px; width:100%; }

  .fono{ position:relative; width:246px; flex-shrink:0; }
  .fono .cuerpo{ background:var(--ink); border-radius:32px; padding:24px 9px 13px;
                 box-shadow:12px 12px 0 rgba(13,13,15,.14); }
  .fono .muesca{ position:absolute; top:8px; left:50%; transform:translateX(-50%);
                 width:60px; height:7px; background:#3A3A3E; border-radius:4px; z-index:2; }
  .fono img{ display:block; width:100%; border-radius:23px; }
  .fono .pie{ margin-top:12px; text-align:center; font-weight:800; letter-spacing:.15em;
              text-transform:uppercase; font-size:13px; color:var(--steel); }

  .lado{ flex:1; min-width:0; display:flex; flex-direction:column; }
  .qrcaja{ position:relative; align-self:flex-start; }
  .qrcaja::after{ content:""; position:absolute; right:-13px; bottom:-13px; top:13px; left:13px;
                  background:var(--red); z-index:0; }
  .qrcaja img{ position:relative; z-index:1; display:block; width:214px; height:214px;
               border:5px solid var(--ink); background:#fff; }
  .comoa{ margin-top:20px; font-family:'Anton','Arial Black',Impact,sans-serif; font-weight:900;
          font-size:25px; line-height:1.15; color:var(--ink); }
  .comoa em{ font-style:normal; color:var(--red); }

  .ventajas{ margin-top:20px; list-style:none; }
  .ventajas li{ display:flex; gap:11px; align-items:flex-start; padding:9px 0;
                border-bottom:2px solid var(--hairline); }
  .ventajas li:last-child{ border-bottom:none; }
  .ventajas .check{ flex-shrink:0; width:23px; height:23px; background:var(--ink); color:var(--paper);
                    display:grid; place-items:center; font-size:14px; font-weight:800; margin-top:1px; }
  .ventajas b{ display:block; font-weight:800; letter-spacing:.06em; text-transform:uppercase;
               font-size:17px; color:var(--ink); line-height:1.15; }
  .ventajas span{ display:block; font-weight:600; font-size:15.5px; color:var(--steel); line-height:1.25; }

  /* ── Pasos y pie ─────────────────────────────────────────────────── */
  .pasos{ margin-top:20px; width:100%; display:flex; gap:14px; border-top:5px solid var(--ink);
          padding-top:18px; }
  .pasos .p{ flex:1; display:flex; gap:10px; align-items:flex-start; }
  .pasos .n{ flex-shrink:0; font-family:'Anton','Arial Black',Impact,sans-serif; font-weight:900;
             font-size:28px; color:var(--red); line-height:.9; }
  .pasos .t{ font-weight:700; font-size:15.5px; line-height:1.25; color:var(--ink); }

  .pie{ margin-top:auto; width:100%; display:flex; justify-content:space-between; align-items:flex-end;
        padding-bottom:26px; }
  .pie .solo{ font-weight:800; letter-spacing:.1em; text-transform:uppercase; font-size:15px;
              color:var(--paper); background:var(--ink); padding:8px 15px; }
  .pie .firma{ text-align:right; }
  .pie .firma b{ display:block; font-family:'Anton','Arial Black',Impact,sans-serif; font-weight:900;
                 font-size:19px; color:var(--ink); letter-spacing:.02em; }
  .pie .firma span{ display:block; font-weight:700; letter-spacing:.2em; text-transform:uppercase;
                    font-size:12px; color:var(--steel); margin-top:3px; }

  @media print{
    @page{ size:A4; margin:0; }
    body{ background:#fff; padding:0; display:block; }
    .poster{ width:210mm; height:297mm; box-shadow:none; }
  }
</style>
</head>
<body>
  <div class="poster">
    <div class="top-bar"></div>

    <div class="cab">
      <div class="logo"><img src="data:image/jpeg;base64,__LOGO__" alt="WGYMADNSPORT"></div>
      <div class="marca"><b>WGYMADNSPORT</b><span>Tocopilla</span></div>
    </div>

    <div class="tag"><span>YA TENEMOS APP</span></div>

    <h1>__LINEA1__<br><em>__LINEA2__</em></h1>
    <div class="sub">5 días · __DIAS__</div>

    <div class="medio">
      <div class="fono">
        <div class="muesca"></div>
        <div class="cuerpo"><img src="data:image/png;base64,__PANTALLA__" alt="Pantalla de la app"></div>
        <div class="pie">Así se ve en tu celular</div>
      </div>

      <div class="lado">
        <div class="qrcaja"><img src="data:image/png;base64,__QR__" alt="Código QR de la app"></div>
        <p class="comoa">ESCANEA<br>Y ES <em>TUYA</em></p>
        <ul class="ventajas">__VENTAJAS__</ul>
      </div>
    </div>

    <div class="pasos">
      <div class="p"><span class="n">1</span><span class="t">Abre la cámara de tu celular</span></div>
      <div class="p"><span class="n">2</span><span class="t">Apunta al código de aquí arriba</span></div>
      <div class="p"><span class="n">3</span><span class="t">Escribe tu nombre y a entrenar</span></div>
    </div>

    <div class="pie">
      <span class="solo">Solo socios con la mensualidad al día</span>
      <span class="firma"><b>WGYMADNSPORT</b><span>21 de Mayo 1520 · Tocopilla</span></span>
    </div>

    <div class="bot-bar"></div>
  </div>
</body>
</html>
"""


def main():
    logo = b64(os.path.join(RAIZ, "assets/logo.jpg"))
    ventajas = "".join(
        '<li><span class="check">&#10003;</span><span><b>%s</b><span>%s</span></span></li>' % v
        for v in VENTAJAS)
    import cv2, numpy as np
    for clave, cfg in CARTELES.items():
        url = SITIO + "entrenar-%s.html" % clave
        qr, img = qr_png(url)
        leido, _, _ = cv2.QRCodeDetector().detectAndDecode(
            cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
        if leido != url:
            sys.exit("El QR de %s no se deja leer: %r" % (clave, leido))

        pant = os.path.join(PANTALLAS, "pant_%s.png" % clave)
        if not os.path.exists(pant):
            sys.exit("Falta la captura de la app: " + pant)

        dias = dias_de(clave)
        s = (PLANTILLA
             .replace("__TITULO__", "QR App " + cfg["linea2"].title())
             .replace("__LOGO__", logo)
             .replace("__LINEA1__", cfg["linea1"])
             .replace("__LINEA2__", cfg["linea2"])
             .replace("__DIAS__", " · ".join(d["weekday"][:3].upper() for d in dias))
             .replace("__PANTALLA__", b64(pant))
             .replace("__QR__", qr)
             .replace("__VENTAJAS__", ventajas))
        destino = os.path.join(RAIZ, "qr-app-%s.html" % clave)
        io.open(destino, "w", encoding="utf-8").write(s)
        print("  qr-app-%s.html  %.0f KB" % (clave, len(s.encode()) / 1024))


if __name__ == "__main__":
    main()
