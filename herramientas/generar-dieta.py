#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera fichas de alimentacion A4 imprimibles con la identidad de WGYMADNSPORT.

    python3 herramientas/generar-dieta.py mi-plan.json

Produce <salida>.html y, si hay Playwright, <salida>.pdf.
El json define socio, dias, semana y ficha de medidas: ver dieta-ejemplo.json.
Sirve igual para el plan de un socio que para el de la duena del gimnasio.
"""
import base64, io, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
LOGO = os.path.join(RAIZ, "contenido", "logo.jpg")
FUENTE_ANTON = os.path.join(RAIZ, "contenido", "fuentes", "Anton.ttf")
FUENTE_BARLOW = os.path.join(RAIZ, "contenido", "fuentes", "BarlowCondensed.ttf")


def logo_incrustado(lado=460):
    from PIL import Image
    im = Image.open(LOGO).convert("RGB")
    im.thumbnail((lado, lado), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=86, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


CSS = """
@page{ size:A4; margin:0; }
*{box-sizing:border-box;margin:0;padding:0}
:root{
 --ink:#0D0D0F; --paper:#FCFCFA; --red:#E1061B; --steel:#6E7278;
 --hair:#D2D2CE; --suave:#EDEDEA;
}
html,body{background:var(--paper);color:var(--ink);
 font-family:'Barlow Condensed','Arial Narrow',Arial,sans-serif}

.hoja{
 position:relative;width:210mm;height:297mm;background:var(--paper);
 padding:13mm 13mm 9mm;display:flex;flex-direction:column;overflow:hidden;
 page-break-after:always;break-after:page
}
.hoja:last-child{page-break-after:auto;break-after:auto}

.barra{position:absolute;top:0;left:0;right:0;height:5mm;background:var(--ink)}
.barra::after{content:"";position:absolute;left:0;top:0;height:5mm;width:58mm;background:var(--red)}

/* ---- cabecera ---- */
.cab{display:flex;align-items:center;gap:5mm;margin-top:3mm}
.logo{width:22mm;height:22mm;border-radius:50%;overflow:hidden;
 border:1.1mm solid var(--ink);flex-shrink:0}
.logo img{width:100%;height:100%;object-fit:cover;display:block}
.ident{flex:1;min-width:0}
.kicker{font-weight:800;letter-spacing:.2em;text-transform:uppercase;font-size:11pt;line-height:1.1}
.kicker span{color:var(--red)}
.doc{font-weight:600;letter-spacing:.13em;text-transform:uppercase;
 font-size:8.5pt;color:var(--steel);margin-top:.6mm}
.socio{font-family:'Anton','Arial Black',Impact,sans-serif;font-weight:900;
 font-size:17pt;letter-spacing:.02em;line-height:1.1;margin-top:1.2mm;text-transform:uppercase}
.tag{
 font-family:'Anton','Arial Black',Impact,sans-serif;font-weight:900;
 font-size:23pt;letter-spacing:.03em;padding:2.4mm 6mm;transform:skewX(-6deg);
 box-shadow:2.2mm 2.2mm 0 var(--ink);flex-shrink:0;text-transform:uppercase;text-align:center
}
.tag span{display:block;transform:skewX(6deg)}
.tag em{display:block;font-family:'Barlow Condensed',sans-serif;font-weight:700;
 font-style:normal;font-size:9pt;letter-spacing:.09em;margin-top:.6mm;text-transform:none}
.hoja[data-n="alto"] .tag{background:var(--red);color:var(--paper)}
.hoja[data-n="medio"] .tag{background:var(--ink);color:var(--paper)}
.hoja[data-n="bajo"] .tag{background:var(--paper);color:var(--ink);border:1.1mm solid var(--ink);
 box-shadow:2.2mm 2.2mm 0 var(--red)}
.hoja[data-n="info"] .tag{background:var(--ink);color:var(--paper)}

.raya{height:1.6mm;background:var(--red);margin-top:4mm;flex-shrink:0}

/* ---- franja de cifras ---- */
.cifras{display:flex;background:var(--ink);flex-shrink:0}
.cifras div{flex:1;text-align:center;padding:2.6mm 1mm;border-left:.4mm solid #34343A}
.cifras div:first-child{border-left:0}
.cifras dt{font-weight:700;letter-spacing:.14em;text-transform:uppercase;
 font-size:7.5pt;color:#9B9DA2}
.cifras dd{font-family:'Anton','Arial Black',Impact,sans-serif;font-weight:900;
 font-size:19pt;color:var(--paper);line-height:1.05;margin-top:.7mm}

/* ---- comidas ---- */
.cuerpo{display:grid;grid-template-columns:1fr 1fr;gap:0 7mm;margin-top:4.5mm;align-items:start;flex:1}
.col{min-width:0}
.bloque{margin-bottom:2.3mm;break-inside:avoid}
.bloque h2{
 font-family:'Anton','Arial Black',Impact,sans-serif;font-weight:900;
 font-size:12.5pt;letter-spacing:.02em;text-transform:uppercase;
 border-bottom:1.1mm solid var(--ink);padding-bottom:.8mm;margin-bottom:1.3mm;
 display:flex;justify-content:space-between;align-items:baseline;gap:2mm
}
.bloque h2 em{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-style:normal;
 font-size:9pt;letter-spacing:.05em;color:var(--steel);text-transform:none;white-space:nowrap}
.bloque li{list-style:none;display:flex;justify-content:space-between;align-items:baseline;
 gap:2.5mm;padding:.6mm 1.4mm;border-bottom:.2mm dotted #A9A9A5;
 font-weight:600;font-size:13pt;line-height:1.14}
.bloque li:last-child{border-bottom:0}
.bloque li b{font-weight:800;white-space:nowrap}
.bloque li.sup{background:var(--suave);justify-content:flex-start}
.bloque li.sup b{margin-left:auto}
.bloque li.sup i{font-style:normal;color:var(--red);font-weight:800;margin-right:1.6mm;font-size:11pt}
.bloque li.agua{border-left:1.1mm solid var(--red);padding-left:2.2mm;font-weight:700}
.bloque li.agua b{color:var(--red)}

.nota{border:.9mm solid var(--ink);padding:2.4mm 3mm;font-weight:600;font-size:12pt;
 line-height:1.3;break-inside:avoid;margin-bottom:3.4mm}
.nota b{font-weight:800}
.nota b.rojo{color:var(--red)}

/* ---- hoja de la semana ---- */
.mapa{border:.9mm solid var(--ink);margin-top:4.5mm;flex-shrink:0}
.mapa div{display:flex;align-items:baseline;gap:3mm;padding:1.5mm 3.4mm;
 border-bottom:.35mm solid var(--ink)}
.mapa div:last-child{border-bottom:0}
.mapa dt{font-family:'Anton',Impact,sans-serif;font-weight:900;font-size:12.5pt;
 letter-spacing:.02em;text-transform:uppercase;width:32mm;flex-shrink:0}
.mapa dd{flex:1;font-weight:600;font-size:11.5pt;color:#33343A}
.mapa b{font-family:'Anton',Impact,sans-serif;font-weight:900;font-size:14pt;white-space:nowrap}
.mapa div[data-n="alto"]{background:#FBE3E5}
.mapa div[data-n="alto"] b{color:var(--red)}
.mapa div[data-n="bajo"]{background:var(--ink)}
.mapa div[data-n="bajo"] dt,.mapa div[data-n="bajo"] b{color:var(--paper)}
.mapa div[data-n="bajo"] dd{color:#B4B6BA}

h3{font-family:'Anton',Impact,sans-serif;font-weight:900;font-size:12.5pt;
 letter-spacing:.03em;text-transform:uppercase;margin:2.3mm 0 1mm;
 border-bottom:1.1mm solid var(--ink);padding-bottom:.9mm}
.info p,.info li{font-weight:600;font-size:12pt;line-height:1.28;margin-top:1.1mm}
.info li{margin-left:5mm}
.info b{font-weight:800}
.caja{border:.7mm solid var(--ink);padding:1.3mm 2.4mm;margin-top:1mm;font-weight:600;font-size:12pt;line-height:1.22}
.caja b{font-weight:800}
.regla{font-family:'Anton',Impact,sans-serif;font-weight:900;font-size:13pt;text-align:center;
 padding:1.3mm 0;background:var(--ink);color:var(--paper);margin-top:1.2mm;letter-spacing:.02em}

/* ---- ficha de medidas ---- */
.arranque{display:flex;border:.9mm solid var(--ink);margin-top:4.5mm;flex-shrink:0}
.arranque div{flex:1;padding:2.2mm 1.2mm;text-align:center;border-left:.35mm solid var(--ink)}
.arranque div:first-child{border-left:0}
.arranque dt{font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:7pt;color:var(--steel)}
.arranque dd{font-family:'Anton',Impact,sans-serif;font-weight:900;font-size:13pt;margin-top:.6mm}
.arranque .vacio{color:#AFAFAB}
.arranque div:nth-last-child(-n+2){background:var(--ink)}
.arranque div:nth-last-child(-n+2) dt{color:#9B9DA2}
.arranque div:nth-last-child(-n+2) dd{color:var(--paper)}
.instru{border:.9mm solid var(--ink);padding:2.4mm 3mm;margin-top:3.4mm;font-weight:600;font-size:12pt;line-height:1.3}
.instru b{font-weight:800}
.instru p{margin-top:1.1mm}
table.ficha{width:100%;border-collapse:collapse;margin-top:3mm}
table.ficha th{font-weight:800;letter-spacing:.03em;text-transform:uppercase;font-size:7.5pt;
 padding:1.6mm .7mm;border:.35mm solid var(--ink);background:var(--ink);color:var(--paper);
 text-align:center;line-height:1.2}
table.ficha td{border:.3mm solid var(--ink);height:8.2mm;text-align:center;font-weight:600;font-size:11.5pt}
table.ficha td.sem{font-family:'Anton',Impact,sans-serif;font-weight:900;font-size:12pt;
 background:var(--suave);width:11mm}
table.ficha td.fec{font-size:9.5pt;width:26mm;color:#33343A}
table.ficha tr[data-hito] td.sem{background:var(--red);color:var(--paper)}
table.ficha td.fot{width:11mm}
table.ficha tr.ejemplo td{background:var(--suave);color:var(--steel);height:7mm;font-style:italic}
table.ficha tr.ejemplo td.sem{background:#DEDEDA;font-style:normal;color:var(--steel)}

/* ---- pie ---- */
.pie{margin-top:auto;padding-top:2.4mm;border-top:.9mm solid var(--ink);
 display:flex;justify-content:space-between;align-items:flex-end;gap:5mm;flex-shrink:0}
.pie .izq{font-weight:600;font-size:10pt;color:#33343A;max-width:110mm;line-height:1.28}
.pie .der{text-align:right;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
 font-size:9pt;color:var(--steel);white-space:nowrap}
.pie .der b{display:block;font-family:'Anton',Impact,sans-serif;font-weight:900;
 color:var(--ink);font-size:12pt;letter-spacing:.05em}
"""

CAB = """  <div class="barra"></div>
  <div class="cab">
   <div class="logo"><img src="{logo}" alt="WGYMADNSPORT"></div>
   <div class="ident">
    <p class="kicker">WGYMADNSPORT · <span>TOCOPILLA</span></p>
    <p class="doc">{doc}</p>
    <p class="socio">{socio}</p>
   </div>
   <div class="tag"><span>{tag}<em>{sub}</em></span></div>
  </div>
  <div class="raya"></div>
"""

PIE = """  <div class="pie">
   <p class="izq">{izq}</p>
   <p class="der">Plan de alimentación<b>WGYMADNSPORT</b></p>
  </div>
"""


def esc(t):
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def dia_html(d, plan, logo):
    cif = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(a), esc(b)) for a, b in d["cifras"])
    cols = [[], []]
    corte = d.get("corte", 3)
    piezas = []
    for c in d["comidas"]:
        li = []
        for it in c["items"]:
            nombre, cant = it[0], it[1]
            marca = it[2] if len(it) > 2 else None
            if marca == "agua":
                li.append('<li class="agua">%s<b>%s</b></li>' % (esc(nombre), esc(cant)))
            elif marca:
                li.append('<li class="sup"><i>&#9679;</i>%s<b>%s</b></li>' % (esc(nombre), esc(cant)))
            else:
                li.append('<li>%s<b>%s</b></li>' % (esc(nombre), esc(cant)))
        piezas.append('   <div class="bloque"><h2>%s<em>%s</em></h2><ul>\n    %s\n   </ul></div>'
                      % (esc(c["nombre"]), esc(c.get("hora", "")), "\n    ".join(li)))
    if d.get("nota"):
        piezas.append('   <div class="nota">%s</div>' % d["nota"])
    cols[0] = piezas[:corte]
    cols[1] = piezas[corte:]
    return """ <div class="hoja" data-n="%s">
%s  <dl class="cifras">%s</dl>
  <div class="cuerpo">
   <div class="col">
%s
   </div>
   <div class="col">
%s
   </div>
  </div>
%s </div>
""" % (d["clave"],
       CAB.format(logo=logo, doc=esc(plan["documento"]), socio=esc(plan["socio"]),
                  tag=esc(d["nombre"]), sub=esc(d["cuando"])),
       cif, "\n".join(cols[0]), "\n".join(cols[1]),
       PIE.format(izq=d.get("pie", "<b>&#9679;</b> = suplemento &nbsp;·&nbsp; Carne, arroz y avena en crudo")))


def semana_html(plan, logo):
    filas = "".join('<div data-n="%s"><dt>%s</dt><dd>%s</dd><b>%s</b></div>'
                    % (f[3], esc(f[0]), esc(f[1]), esc(f[2])) for f in plan["semana"])
    return """ <div class="hoja" data-n="info">
%s  <div class="mapa">%s</div>
  <div class="info">
%s  </div>
%s </div>
""" % (CAB.format(logo=logo, doc=esc(plan["documento"]), socio=esc(plan["socio"]),
                  tag="La semana", sub=esc(plan["periodo"])),
       filas, plan["bloques_semana"],
       PIE.format(izq=esc(plan.get("pie_semana", ""))))


def ficha_html(plan, logo):
    a = plan["partida"]
    arr = "".join('<div><dt>%s</dt><dd%s>%s</dd></div>'
                  % (esc(k), ' class="vacio"' if "_" in str(v) else "", esc(v))
                  for k, v in a)
    dias = plan.get("dias_peso", ["lunes", "miércoles", "viernes"])
    tr = ['   <tr class="ejemplo"><td class="sem">ej.</td><td class="fec">así se llena</td>'
          '<td>70,0</td><td>69,8</td><td>69,6</td><td>69,8</td><td>82</td><td>99</td>'
          '<td class="fot">&#10003;</td></tr>']
    for nn, f, hito in plan["ficha"]:
        at = ' data-hito="1"' if hito else ""
        tr.append('   <tr%s><td class="sem">%s</td><td class="fec">%s</td>'
                  '<td></td><td></td><td></td><td></td><td></td><td></td><td class="fot"></td></tr>'
                  % (at, esc(nn), esc(f)))
    return """ <div class="hoja" data-n="info">
%s  <dl class="arranque">%s</dl>
  <div class="instru">%s</div>
  <table class="ficha">
   <thead><tr><th>Sem</th><th>Semana del</th><th>Peso<br>%s</th><th>Peso<br>%s</th>
   <th>Peso<br>%s</th><th>Promedio<br>de los 3</th><th>Cintura<br>cm</th><th>Cadera<br>cm</th><th>Foto</th></tr></thead>
   <tbody>
%s
   </tbody>
  </table>
%s </div>
""" % (CAB.format(logo=logo, doc=esc(plan["documento"]), socio=esc(plan["socio"]),
                  tag="Medidas", sub=esc(plan["periodo"])),
       arr, plan["instrucciones"], dias[0], dias[1], dias[2], "\n".join(tr),
       PIE.format(izq=esc(plan.get("pie_ficha", ""))))


def construir(plan):
    logo = logo_incrustado()
    partes = [dia_html(d, plan, logo) for d in plan["dias"]]
    partes.append(semana_html(plan, logo))
    partes.append(ficha_html(plan, logo))
    return """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>%s · %s</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Condensed:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>%s</style>
</head>
<body>
%s</body>
</html>
""" % (esc(plan["socio"]), esc(plan["documento"]), CSS, "".join(partes))


MM = 2.834645669  # 1 mm en puntos PDF
INK = "#0D0D0F"
PAPEL = "#FCFCFA"
ROJO = "#E1061B"
ACERO = "#6E7278"
SUAVE = "#EDEDEA"


def _html_a_lineas(txt):
    """Convierte el HTML simple usado en instrucciones/pie (<p>, <b>, <b class=rojo>)
    al mini-marcado que entiende reportlab.platypus.Paragraph."""
    txt = re.sub(r"\s*<p>\s*", "<br/><br/>", txt)
    txt = re.sub(r"</p>\s*", "", txt)
    txt = re.sub(r'<b class="rojo">(.*?)</b>', r'<font color="%s"><b>\1</b></font>' % ROJO, txt, flags=re.S)
    txt = txt.replace("&nbsp;", " ")
    txt = txt.strip()
    if txt.startswith("<br/><br/>"):
        txt = txt[len("<br/><br/>"):]
    return txt


def _sano(s):
    """La fuente Barlow Condensed convertida no trae el glifo de flecha;
    se reemplaza por un guión para que no desaparezca el texto."""
    return str(s).replace("→", "-")


def _fuentes_registradas():
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    if "Anton" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("Anton", FUENTE_ANTON))
        pdfmetrics.registerFont(TTFont("Barlow", FUENTE_BARLOW))
    return True


def pagina_medidas_pdf(plan, ruta_salida, logo_path=LOGO):
    """Genera, como PDF de una sola hoja A4 con campos de formulario reales,
    el reemplazo editable de la hoja 'Medidas' (peso, cintura, cadera y foto
    por semana) para que se llene en el computador o el celular sin imprimir."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT

    tiene_fuentes = False
    try:
        tiene_fuentes = _fuentes_registradas()
    except Exception:
        pass
    F_DISP = "Anton" if tiene_fuentes else "Helvetica-Bold"
    F_TXT = "Barlow" if tiene_fuentes else "Helvetica"
    F_TXTB = "Barlow" if tiene_fuentes else "Helvetica-Bold"

    ANCHO, ALTO = 210 * MM, 297 * MM
    MARGEN_L = MARGEN_R = 13 * MM
    MARGEN_T = 13 * MM
    ANCHO_UTIL = ANCHO - MARGEN_L - MARGEN_R

    c = canvas.Canvas(ruta_salida, pagesize=(ANCHO, ALTO))
    c.setTitle("%s · Medidas · %s" % (plan["socio"], plan["documento"]))

    # ---- barra superior ----
    c.setFillColor(HexColor(INK))
    c.rect(0, ALTO - 5 * MM, ANCHO, 5 * MM, fill=1, stroke=0)
    c.setFillColor(HexColor(ROJO))
    c.rect(0, ALTO - 5 * MM, 58 * MM, 5 * MM, fill=1, stroke=0)

    cursor = ALTO - MARGEN_T - 3 * MM  # tope de la cabecera

    # ---- logo circular ----
    logo_d = 22 * MM
    try:
        c.saveState()
        p = c.beginPath()
        p.circle(MARGEN_L + logo_d / 2, cursor - logo_d / 2, logo_d / 2)
        c.clipPath(p, stroke=0)
        c.drawImage(logo_path, MARGEN_L, cursor - logo_d, width=logo_d, height=logo_d,
                    preserveAspectRatio=True, mask="auto")
        c.restoreState()
        c.setLineWidth(1.1 * MM)
        c.setStrokeColor(HexColor(INK))
        c.circle(MARGEN_L + logo_d / 2, cursor - logo_d / 2, logo_d / 2, fill=0, stroke=1)
    except Exception:
        pass

    # ---- identidad (kicker / doc / socio) ----
    tx = MARGEN_L + logo_d + 5 * MM
    c.setFont(F_TXTB, 11)
    c.setFillColor(HexColor(INK))
    c.drawString(tx, cursor - 3.6 * MM, "WGYMADNSPORT · ")
    ancho_kicker = c.stringWidth("WGYMADNSPORT · ", F_TXTB, 11)
    c.setFillColor(HexColor(ROJO))
    c.drawString(tx + ancho_kicker, cursor - 3.6 * MM, "TOCOPILLA")
    c.setFillColor(HexColor(ACERO))
    c.setFont(F_TXTB, 8)
    c.drawString(tx, cursor - 7.6 * MM, plan["documento"].upper())
    c.setFillColor(HexColor(INK))
    c.setFont(F_DISP, 15)
    c.drawString(tx, cursor - 13.5 * MM, plan["socio"].upper())

    # ---- etiqueta "MEDIDAS" (esquina superior derecha) ----
    et_txt, et_sub = "MEDIDAS", _sano(plan["periodo"])
    c.setFont(F_DISP, 17)
    et_ancho = max(c.stringWidth(et_txt, F_DISP, 17) + 10 * MM, 46 * MM)
    et_x = ANCHO - MARGEN_R - et_ancho
    et_y = cursor - 15.5 * MM
    et_alto = 15.5 * MM
    c.setFillColor(HexColor(INK))
    c.roundRect(et_x + 1.6 * MM, et_y - 1.6 * MM, et_ancho, et_alto, 0, fill=1, stroke=0)
    c.setFillColor(HexColor(PAPEL))
    c.drawCentredString(et_x + et_ancho / 2 + 1.6 * MM, et_y + et_alto - 6.5 * MM, et_txt)
    c.setFont(F_TXTB, 8.5)
    c.drawCentredString(et_x + et_ancho / 2 + 1.6 * MM, et_y + 2.2 * MM, et_sub)

    cursor -= 16 * MM
    # ---- raya roja ----
    c.setFillColor(HexColor(ROJO))
    c.rect(MARGEN_L, cursor, ANCHO_UTIL, 1.6 * MM, fill=1, stroke=0)
    cursor -= 4.5 * MM

    # ---- arranque (punto de partida) ----
    partida = plan.get("partida", [])
    if partida:
        alto_arranque = 13 * MM
        n = len(partida)
        ancho_col = ANCHO_UTIL / n
        c.setLineWidth(0.9 * MM)
        c.setStrokeColor(HexColor(INK))
        c.rect(MARGEN_L, cursor - alto_arranque, ANCHO_UTIL, alto_arranque, fill=0, stroke=1)
        for i, (k, v) in enumerate(partida):
            x0 = MARGEN_L + i * ancho_col
            oscuro = i >= n - 2
            if oscuro:
                c.setFillColor(HexColor(INK))
                c.rect(x0, cursor - alto_arranque, ancho_col, alto_arranque, fill=1, stroke=0)
            if i > 0:
                c.setStrokeColor(HexColor(INK))
                c.setLineWidth(0.35 * MM)
                c.line(x0, cursor - alto_arranque, x0, cursor)
            c.setFont(F_TXTB, 6.3)
            c.setFillColor(HexColor(PAPEL) if oscuro else HexColor(ACERO))
            c.drawCentredString(x0 + ancho_col / 2, cursor - 4.2 * MM, k.upper())
            c.setFont(F_DISP, 11)
            c.setFillColor(HexColor(PAPEL) if oscuro else HexColor(INK))
            c.drawCentredString(x0 + ancho_col / 2, cursor - 9.6 * MM, str(v))
        cursor -= alto_arranque + 3.4 * MM

    # ---- instrucciones ----
    instr = plan.get("instrucciones", "")
    if instr:
        estilo = ParagraphStyle("instru", fontName=F_TXTB, fontSize=9, leading=11.5,
                                 textColor=HexColor(INK), alignment=TA_LEFT)
        parrafo = Paragraph(_html_a_lineas(instr), estilo)
        ancho_p, alto_p = parrafo.wrap(ANCHO_UTIL - 6 * MM, 1000)
        alto_caja = alto_p + 4.8 * MM
        c.setLineWidth(0.9 * MM)
        c.setStrokeColor(HexColor(INK))
        c.rect(MARGEN_L, cursor - alto_caja, ANCHO_UTIL, alto_caja, fill=0, stroke=1)
        parrafo.drawOn(c, MARGEN_L + 3 * MM, cursor - alto_caja + 2.4 * MM)
        cursor -= alto_caja + 3.4 * MM

    # ---- tabla de medidas (editable) ----
    dias_peso = plan.get("dias_peso", ["Miércoles", "Viernes", "Lunes"])
    encabezados = ["Sem", "Semana del", "Peso\n%s" % dias_peso[0], "Peso\n%s" % dias_peso[1],
                   "Peso\n%s" % dias_peso[2], "Promedio\nde los 3", "Cintura\ncm", "Cadera\ncm", "Foto"]
    col_sem, col_fec, col_fot = 11 * MM, 26 * MM, 11 * MM
    resto = ANCHO_UTIL - col_sem - col_fec - col_fot
    col_dato = resto / 6.0
    anchos = [col_sem, col_fec] + [col_dato] * 6 + [col_fot]
    xs = [MARGEN_L]
    for a in anchos:
        xs.append(xs[-1] + a)

    alto_cab = 8 * MM
    alto_fila = 8.2 * MM
    filas = plan.get("ficha", [])
    n_filas_totales = 1 + len(filas)  # incluye la fila de ejemplo
    alto_tabla = alto_cab + n_filas_totales * alto_fila
    y_tabla_top = cursor
    y_tabla_bottom = y_tabla_top - alto_tabla

    # encabezado
    c.setFillColor(HexColor(INK))
    c.rect(MARGEN_L, y_tabla_top - alto_cab, ANCHO_UTIL, alto_cab, fill=1, stroke=0)
    c.setFillColor(HexColor(PAPEL))
    c.setFont(F_TXTB, 6.3)
    for i, txt in enumerate(encabezados):
        cx = (xs[i] + xs[i + 1]) / 2
        lineas = txt.split("\n")
        base_y = y_tabla_top - alto_cab / 2 + (1.6 * MM if len(lineas) > 1 else 0)
        for j, ln in enumerate(lineas):
            c.drawCentredString(cx, base_y - j * 3.1 * MM - 1.2 * MM, ln.upper())

    # fila de ejemplo (no editable, solo referencia visual)
    y = y_tabla_top - alto_cab
    ejemplo = ["ej.", "así se llena", "70,0", "69,8", "69,6", "69,8", "82", "99", "✓"]
    c.setFillColor(HexColor(SUAVE))
    c.rect(MARGEN_L, y - alto_fila, ANCHO_UTIL, alto_fila, fill=1, stroke=0)
    c.setFont(F_TXT, 8.3)
    c.setFillColor(HexColor(ACERO))
    for i, txt in enumerate(ejemplo):
        cx = (xs[i] + xs[i + 1]) / 2
        c.drawCentredString(cx, y - alto_fila / 2 - 1.2 * MM, txt)
    y -= alto_fila

    form = c.acroForm
    for idx, (nn, fecha, hito) in enumerate(filas):
        fila_id = "f%02d" % idx
        if hito:
            c.setFillColor(HexColor(ROJO))
            c.rect(xs[0], y - alto_fila, col_sem, alto_fila, fill=1, stroke=0)
            c.setFillColor(HexColor(PAPEL))
        else:
            c.setFillColor(HexColor(SUAVE))
            c.rect(xs[0], y - alto_fila, col_sem, alto_fila, fill=1, stroke=0)
            c.setFillColor(HexColor(INK))
        c.setFont(F_DISP, 9)
        c.drawCentredString((xs[0] + xs[1]) / 2, y - alto_fila / 2 - 1.4 * MM, str(nn))
        c.setFont(F_TXT, 7.4)
        c.setFillColor(HexColor("#33343A"))
        c.drawCentredString((xs[1] + xs[2]) / 2, y - alto_fila / 2 - 1.2 * MM, fecha)

        # 5 campos de texto: 3 pesos, promedio, cintura, cadera
        for col in range(2, 8):
            x0, x1 = xs[col], xs[col + 1]
            form.textfield(
                name="%s_c%d" % (fila_id, col),
                tooltip="Semana %s" % nn,
                x=x0 + 0.6 * MM, y=y - alto_fila + 0.6 * MM,
                width=(x1 - x0) - 1.2 * MM, height=alto_fila - 1.2 * MM,
                borderStyle="inset", borderWidth=0.4, borderColor=HexColor(INK),
                fillColor=HexColor(PAPEL), textColor=HexColor(INK),
                fontName="Helvetica", fontSize=9, forceBorder=True,
            )
        # casilla de foto
        cxf0, cxf1 = xs[8], xs[9]
        lado = min(alto_fila, cxf1 - cxf0) - 2.4 * MM
        form.checkbox(
            name="%s_foto" % fila_id, tooltip="Foto semana %s" % nn,
            x=(cxf0 + cxf1) / 2 - lado / 2, y=y - alto_fila / 2 - lado / 2,
            size=lado, borderStyle="inset", borderWidth=0.4, borderColor=HexColor(INK),
            fillColor=HexColor(PAPEL), buttonStyle="check", forceBorder=True,
        )
        y -= alto_fila

    # marco general de la tabla + líneas de columnas
    c.setStrokeColor(HexColor(INK))
    c.setLineWidth(0.3 * MM)
    for x in xs:
        c.line(x, y_tabla_top, x, y_tabla_bottom)
    c.line(MARGEN_L, y_tabla_top, MARGEN_L + ANCHO_UTIL, y_tabla_top)
    c.line(MARGEN_L, y_tabla_bottom, MARGEN_L + ANCHO_UTIL, y_tabla_bottom)
    for i in range(n_filas_totales + 1):
        yy = y_tabla_top - alto_cab - i * alto_fila
        c.line(MARGEN_L, yy, MARGEN_L + ANCHO_UTIL, yy)

    # ---- pie ----
    pie_txt = plan.get("pie_ficha", "")
    if pie_txt:
        c.setLineWidth(0.9 * MM)
        c.setStrokeColor(HexColor(INK))
        c.line(MARGEN_L, MARGEN_T * 0.55, MARGEN_L + ANCHO_UTIL, MARGEN_T * 0.55)
        estilo_pie = ParagraphStyle("pie", fontName=F_TXTB, fontSize=8, leading=10,
                                     textColor=HexColor("#33343A"))
        pp = Paragraph(_html_a_lineas(pie_txt), estilo_pie)
        pp.wrap(ANCHO_UTIL * 0.65, 20 * MM)
        pp.drawOn(c, MARGEN_L, MARGEN_T * 0.55 - 9 * MM)
        c.setFont(F_TXTB, 7.5)
        c.setFillColor(HexColor(ACERO))
        c.drawRightString(MARGEN_L + ANCHO_UTIL, MARGEN_T * 0.55 - 5.5 * MM, "PLAN DE ALIMENTACIÓN")
        c.setFont(F_DISP, 10)
        c.setFillColor(HexColor(INK))
        c.drawRightString(MARGEN_L + ANCHO_UTIL, MARGEN_T * 0.55 - 9.5 * MM, "WGYMADNSPORT")

    c.showPage()
    c.save()


def insertar_medidas_editable(pdf_path, plan):
    """Reemplaza la última hoja del PDF ya renderizado (la de Medidas, plana)
    por una versión con campos de formulario reales, dejando intactas todas
    las hojas anteriores. Requiere reportlab y pypdf; si faltan, no hace nada."""
    try:
        from pypdf import PdfReader, PdfWriter
    except Exception:
        print("  (sin pypdf: la hoja de medidas queda como imagen, no editable)")
        return False

    tmp_medidas = pdf_path + ".medidas-tmp.pdf"
    try:
        pagina_medidas_pdf(plan, tmp_medidas)
    except Exception as e:
        print("  (no se pudo generar la hoja editable: %s)" % e)
        return False

    lector_original = PdfReader(pdf_path)
    lector_medidas = PdfReader(tmp_medidas)
    writer = PdfWriter()
    for pagina in lector_original.pages[:-1]:
        writer.add_page(pagina)
    writer.append(lector_medidas)

    tmp_final = pdf_path + ".tmp"
    with open(tmp_final, "wb") as f:
        writer.write(f)
    os.replace(tmp_final, pdf_path)
    os.remove(tmp_medidas)
    return True


def a_pdf(html_path, pdf_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  (sin Playwright: solo HTML)")
        return None
    exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=exe if os.path.exists(exe) else None)
        pg = b.new_page(viewport={"width": 794, "height": 1123})
        pg.goto("file://" + os.path.abspath(html_path))
        pg.emulate_media(media="print")
        altos = pg.evaluate("Array.from(document.querySelectorAll('.hoja'))"
                            ".map(h => h.scrollHeight - h.clientHeight)")
        pg.pdf(path=pdf_path, format="A4", print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        b.close()
    return altos


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    origen = sys.argv[1]
    plan = json.load(open(origen, encoding="utf-8"))
    base = os.path.splitext(origen)[0]
    html, pdf = base + ".html", base + ".pdf"
    open(html, "w", encoding="utf-8").write(construir(plan))
    print("HTML:", html)
    altos = a_pdf(html, pdf)
    if altos:
        print("PDF :", pdf)
        print("desborde por hoja (0 = cabe):", altos)
        malas = [i + 1 for i, h in enumerate(altos) if h > 0]
        if malas:
            print("  OJO: se desbordan las hojas", malas)
        if insertar_medidas_editable(pdf, plan):
            print("  hoja de medidas: editable (campos de formulario)")


if __name__ == "__main__":
    main()
