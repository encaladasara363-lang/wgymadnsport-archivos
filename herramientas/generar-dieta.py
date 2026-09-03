#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera fichas de alimentacion A4 imprimibles con la identidad de WGYMADNSPORT.

    python3 herramientas/generar-dieta.py mi-plan.json

Produce <salida>.html y, si hay Playwright, <salida>.pdf.
El json define socio, dias, semana y ficha de medidas: ver dieta-ejemplo.json.
Sirve igual para el plan de un socio que para el de la duena del gimnasio.
"""
import base64, io, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
LOGO = os.path.join(RAIZ, "contenido", "logo.jpg")


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
.bloque{margin-bottom:2.6mm;break-inside:avoid}
.bloque h2{
 font-family:'Anton','Arial Black',Impact,sans-serif;font-weight:900;
 font-size:12.5pt;letter-spacing:.02em;text-transform:uppercase;
 border-bottom:1.1mm solid var(--ink);padding-bottom:.8mm;margin-bottom:1.3mm;
 display:flex;justify-content:space-between;align-items:baseline;gap:2mm
}
.bloque h2 em{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-style:normal;
 font-size:9pt;letter-spacing:.05em;color:var(--steel);text-transform:none;white-space:nowrap}
.bloque li{list-style:none;display:flex;justify-content:space-between;align-items:baseline;
 gap:2.5mm;padding:.72mm 1.4mm;border-bottom:.2mm dotted #A9A9A5;
 font-weight:600;font-size:13pt;line-height:1.18}
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
.caja{border:.7mm solid var(--ink);padding:1.6mm 2.6mm;margin-top:1.3mm;font-weight:600;font-size:12pt;line-height:1.26}
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


if __name__ == "__main__":
    main()
