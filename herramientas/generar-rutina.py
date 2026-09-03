# -*- coding: utf-8 -*-
"""Arma una rutina de entrenamiento en A4 imprimible, con el sello del gimnasio:
rojo E30613, negro, caja crema para el pictograma y badge rojo con el numero.

    python3 herramientas/generar-rutina.py rutina-fulano.json

El JSON lleva TODO lo que cambia de una persona a otra (ver rutina-ejemplo.json).
Los pictogramas son dibujos propios y viven en herramientas/rutina-iconos/; si
falta uno, se agrega en _dibujar.py con el mismo trazo. Nunca fotos ni iconos
bajados de internet: es tema de derechos de autor, no de gusto.

OJO: las rutinas de socios llevan medidas y datos de salud. No se suben al
repositorio, que es publico. El .gitignore ya las bloquea.
"""
import base64, json, os, sys
from playwright.sync_api import sync_playwright

AQUI    = os.path.dirname(os.path.abspath(__file__))
ICONOS  = os.path.join(AQUI, "rutina-iconos")
LOGO    = os.path.join(AQUI, "..", "contenido", "logo.jpg")

if len(sys.argv) < 2:
    sys.exit("uso: python3 generar-rutina.py rutina-fulano.json")
FUENTE = os.path.abspath(sys.argv[1])
BASE   = os.path.splitext(FUENTE)[0]

def b64(ruta, mime):
    return "data:%s;base64,%s" % (mime, base64.b64encode(open(ruta,"rb").read()).decode())
def icono(n):  return b64(os.path.join(ICONOS, n + ".png"), "image/png")
def esc(t):    return (t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

R = json.load(open(FUENTE, encoding="utf-8"))
DIAS, FRASES, FICHA, METODO = R["dias"], R["frases"], R["ficha"], R["metodo"]
print("%s · %d días" % (R["socio"], len(DIAS)))

CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Arial,Helvetica,sans-serif;color:#141414;background:#fff}
.hoja{width:210mm;height:297mm;padding:11mm 12mm 9mm;display:flex;flex-direction:column;
 page-break-after:always;overflow:hidden}
.hoja:last-child{page-break-after:auto}
.top{display:flex;align-items:center;gap:5mm;margin-bottom:3.5mm;flex-shrink:0}
.top img{width:17mm;height:17mm;border-radius:50%;object-fit:cover;border:.8mm solid #141414}
.top .t1{font-size:12pt;font-weight:800;letter-spacing:.01em}
.top .t2{font-size:8.6pt;font-weight:800;color:#E30613;letter-spacing:.03em}
.banner{display:flex;align-items:stretch;margin-bottom:3.5mm;flex-shrink:0}
.banner .n{background:#E30613;color:#fff;font-size:26pt;font-weight:800;
 display:flex;align-items:center;justify-content:center;width:22mm}
.banner .d{background:#141414;color:#fff;padding:3.4mm 6mm;flex:1;display:flex;
 flex-direction:column;justify-content:center}
.banner .d b{font-size:20pt;font-weight:800;letter-spacing:.01em;line-height:1.05}
.banner .d span{font-size:11pt;font-weight:800;color:#fff;margin-top:1.1mm;letter-spacing:.03em}
.tag{font-size:11.4pt;font-weight:800;margin:3mm 0 1.6mm;flex-shrink:0}
.tag i{color:#E30613;font-style:normal}
ul{list-style:none}
li.p{font-size:10.6pt;color:#333;margin-bottom:1.3mm;padding-left:4.4mm;position:relative}
li.p:before{content:"•";position:absolute;left:0;color:#E30613;font-weight:800}
.ej{display:flex;align-items:stretch;border:.35mm solid #E4E4E4;margin-bottom:1.5mm;flex-shrink:0}
.ej .num{background:#E30613;color:#fff;width:11mm;font-size:14pt;font-weight:800;
 display:flex;align-items:center;justify-content:center}
.ej .ic{background:#FFF7F0;width:20mm;display:flex;align-items:center;justify-content:center;padding:1.4mm}
.ej .ic img{max-width:100%;max-height:16.5mm}
.ej .tx{padding:2mm 4mm;flex:1;display:flex;flex-direction:column;justify-content:center}
.ej .tx b{font-size:12.4pt;font-weight:800;text-transform:uppercase;line-height:1.1}
.ej .tx .dato{font-size:10pt;font-weight:800;color:#E30613;margin:1.1mm 0}
.ej .tx .dato u{text-decoration:none;margin-right:3.4mm;white-space:nowrap}
.ej .tx i{font-size:9.8pt;color:#333;line-height:1.28}
.frase{background:#E30613;color:#fff;text-align:center;font-size:10.6pt;font-weight:800;
 font-style:italic;padding:3.4mm 6mm;margin-top:auto;flex-shrink:0}
/* portada */
.port{justify-content:center;align-items:center;text-align:center}
.port img.logo{width:62mm;height:62mm;border-radius:50%;object-fit:cover;border:1.6mm solid #141414;margin-bottom:7mm}
.port h1{font-size:34pt;font-weight:800;line-height:1.05}
.port h1.rojo{color:#E30613}
.port h2{font-size:19pt;font-weight:800;margin:4mm 0 7mm}
table.ficha{width:100%;border-collapse:collapse;margin-bottom:7mm}
table.ficha td{border:.3mm solid #D8D8D8;padding:2.8mm 4mm;font-size:11pt;text-align:left}
table.ficha td.k{background:#141414;color:#fff;font-weight:800;text-transform:uppercase;
 font-size:10pt;width:38%;letter-spacing:.02em}
/* metodo */
h3.m{font-size:13pt;font-weight:800;text-transform:uppercase;margin:3.6mm 0 1.4mm;
 border-bottom:.8mm solid #141414;padding-bottom:1mm;letter-spacing:.02em}
h3.m:first-of-type{margin-top:1mm}
li.m{font-size:10.8pt;color:#333;margin-bottom:1.5mm;padding-left:4.6mm;position:relative;line-height:1.32}
li.m:before{content:"•";position:absolute;left:0;color:#E30613;font-weight:800}
"""

H = ['<meta charset="utf-8"><style>%s</style>' % CSS]
LG, ICO = b64(LOGO,"image/jpeg"), {}

def top():
    return ('<div class="top"><img src="%s"><div><div class="t1">%s</div>'
            '<div class="t2">%s</div></div></div>') % (LG, esc(R["cabecera"][0]), esc(R["cabecera"][1]))

# ---- portada ----
H.append('<div class="hoja port"><img class="logo" src="%s">' % LG)
H.append('<h1>%s</h1><h1 class="rojo">%s</h1><h2>%s</h2>'
         % (esc(R["titulo"][0]), esc(R["titulo"][1]), esc(R["socio"].upper())))
H.append('<table class="ficha">' + "".join(
    '<tr><td class="k">%s</td><td>%s</td></tr>' % (esc(k), esc(v)) for k,v in FICHA) + '</table>')
H.append('<div class="frase" style="margin-top:0">%s</div></div>' % esc(R["portada_frase"]))

# ---- los seis días ----
for i, d in enumerate(DIAS):
    H.append('<div class="hoja">' + top())
    H.append('<div class="banner"><div class="n">%s</div><div class="d"><b>%s</b><span>%s</span></div></div>'
             % (esc(d["num"]), esc(d["dia"]), esc(d["sub"])))
    H.append('<div class="tag"><i>●</i> CALENTAMIENTO · 10 MIN</div><ul>' +
             "".join('<li class="p">%s</li>' % esc(x) for x in d["calentamiento"]) + '</ul>')
    H.append('<div class="tag"><i>●</i> TRABAJO PRINCIPAL · 85 MIN</div>')
    for k, e in enumerate(d["ejercicios"], 1):
        ic, nom, ser, rep, des, tec = e[:6]
        carga = e[6] if len(e) > 6 else None
        if ic not in ICO: ICO[ic] = icono(ic)
        datos = '<u>SERIES: %s</u><u>REPS: %s</u><u>DESCANSO: %s</u>' % (esc(ser), esc(rep), esc(des))
        if carga and carga.strip("—- "): datos += '<u>CARGA: %s</u>' % esc(carga)
        H.append('<div class="ej"><div class="num">%d</div><div class="ic"><img src="%s"></div>'
                 '<div class="tx"><b>%s</b><div class="dato">%s</div><i>%s</i></div></div>'
                 % (k, ICO[ic], esc(nom), datos, tec))
    H.append('<div class="tag"><i>●</i> ESTIRAMIENTOS · 10 MIN</div><ul>' +
             "".join('<li class="p">%s</li>' % esc(x) for x in d["estiramientos"]) + '</ul>')
    H.append('<div class="frase">%s</div></div>' % esc(FRASES[i]))

# ---- hoja del método ----
# el metodo puede no caber en una hoja: "metodo_corte" dice donde partirlo
CORTE = R.get("metodo_corte", len(METODO))
TRAMOS = [x for x in (METODO[:CORTE], METODO[CORTE:]) if x]
for h, tramo in enumerate(TRAMOS):
    H.append('<div class="hoja">' + top())
    sub = R["metodo_titulo"][1] if h == 0 else R["metodo_titulo"][1] + " · CONTINÚA"
    H.append('<div class="banner"><div class="n">★</div><div class="d"><b>%s</b><span>%s</span></div></div>'
             % (esc(R["metodo_titulo"][0]), esc(sub)))
    for tit, puntos in tramo:
        H.append('<h3 class="m">%s</h3><ul>' % esc(tit) +
                 "".join('<li class="m">%s</li>' % p for p in puntos) + '</ul>')
    if h == len(TRAMOS) - 1:
        H.append('<div class="frase">%s</div>' % esc(R["cierre"]))
    H.append('</div>')

html = "".join(H)
open(BASE + ".html","w",encoding="utf-8").write(html)

exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=exe if os.path.exists(exe) else None)
    pg = b.new_page()
    pg.set_content(html, wait_until="networkidle")
    altos = pg.evaluate("Array.from(document.querySelectorAll('.hoja'))"
                        ".map(h => h.scrollHeight - h.clientHeight)")
    pg.pdf(path=BASE + ".pdf",
           format="A4", print_background=True,
           margin={"top":"0","bottom":"0","left":"0","right":"0"})
    b.close()
print("desborde por hoja (0 = cabe):", altos)
if any(altos): print("  OJO: se desbordan las hojas", [i+1 for i,a in enumerate(altos) if a])

print("HTML:", BASE + ".html")
print("PDF :", BASE + ".pdf")
