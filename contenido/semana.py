#!/usr/bin/env python3
"""
Arma el paquete de una semana de contenido de WGYMADNSPORT Tocopilla.

    python3 contenido/semana.py 3

Deja en  contenido/salida/semana-03/  las 7 laminas del carrusel en PNG
1080x1080 con foto del gimnasio de fondo, mas un archivo de texto con los
siete dias listos para copiar y pegar en Instagram.
"""
import base64, json, pathlib, re, sys

AQUI = pathlib.Path(__file__).resolve().parent

NEGRO = "#111110"
ROJO  = "#C7101B"
ORO   = "#D4AF37"
HUESO = "#F5F1EA"

ENTRADA    = 8               # la foto del letrero de la calle
INTERIORES = [1,2,3,4,5,6,7,9]


def b64(ruta):
    return base64.b64encode((AQUI / ruta).read_bytes()).decode()


PLANTILLA = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Anton';src:url(data:font/woff2;base64,%(anton)s) format('woff2');font-weight:400;font-display:block}
@font-face{font-family:'BC';src:url(data:font/woff2;base64,%(bc)s) format('woff2');font-weight:800;font-display:block}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1080px;overflow:hidden;background:%(negro)s}
.lamina{width:1080px;height:1080px;position:relative;overflow:hidden}
.foto{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;
 filter:grayscale(.20) contrast(1.10) brightness(.95) saturate(.92)}
.velo{position:absolute;inset:0;background:
 linear-gradient(102deg, rgba(17,17,16,.90) 0%%, rgba(17,17,16,.72) 46%%, rgba(17,17,16,.34) 100%%)}
.tinte{position:absolute;inset:0;background:%(tinte)s}
.filo{position:absolute;top:0;left:0;right:0;height:14px;background:%(filo)s;z-index:3}
.capa{position:absolute;inset:0;z-index:2;display:flex;flex-direction:column;
 padding:78px 84px 72px;color:%(texto)s}
.ceja{font-family:'BC',Arial,sans-serif;font-weight:800;font-size:26px;
 letter-spacing:.26em;text-transform:uppercase;color:%(ceja)s;margin-bottom:auto}
.cuerpo{display:flex;align-items:center;gap:38px;flex:1}
.cifra{font-family:'Anton',Impact,sans-serif;font-size:170px;line-height:.78;
 color:%(cifra)s;flex:0 0 auto;letter-spacing:-.02em}
.frase{font-family:'Anton',Impact,sans-serif;font-size:%(tam)spx;line-height:1.02;
 letter-spacing:.005em;text-transform:uppercase;text-wrap:balance;
 text-shadow:0 3px 22px rgba(0,0,0,.55)}
.pie{display:flex;align-items:flex-end;justify-content:space-between;gap:30px;
 margin-top:auto;padding-top:40px}
.marca{font-family:'BC',Arial,sans-serif;font-weight:800;font-size:25px;
 letter-spacing:.2em;text-transform:uppercase;color:%(pie)s;line-height:1.5;
 text-shadow:0 2px 12px rgba(0,0,0,.6)}
.marca b{display:block;color:%(pieFuerte)s}
.logo{width:118px;height:118px;border-radius:50%%;object-fit:cover;flex:0 0 auto;
 box-shadow:0 4px 20px rgba(0,0,0,.5)}
.conteo{font-family:'BC',Arial,sans-serif;font-weight:800;font-size:25px;
 letter-spacing:.16em;color:%(pie)s}
</style></head><body><div class="lamina">
 <img class="foto" src="data:image/jpeg;base64,%(foto)s" alt="">
 <div class="velo"></div>%(tinte_html)s
 <div class="filo"></div>
 <div class="capa">
  <div class="ceja">%(ceja_txt)s</div>
  <div class="cuerpo">%(cifra_html)s<div class="frase">%(frase)s</div></div>
  <div class="pie">
   <div class="marca">@wadnsport.tocopilla<b>WhatsApp +56 9 7519 6394</b></div>
   <div style="display:flex;align-items:center;gap:26px">
    <span class="conteo">%(n)s/%(total)s</span>
    <img class="logo" src="data:image/jpeg;base64,%(logo)s" alt="">
   </div>
  </div>
 </div>
</div></body></html>"""


def tamano(t):
    n = len(t)
    return 118 if n <= 34 else 100 if n <= 52 else 86 if n <= 74 else 74 if n <= 96 else 64


def html_lamina(semana, i, total, txt, recursos):
    portada = (i == 0)
    cierre  = (i == total - 1)

    m = re.match(r"^(\d)\.\s*(.+)$", txt)
    cifra_html, frase = "", txt
    if m and not portada and not cierre:
        cifra_html = '<div class="cifra">%s</div>' % m.group(1)
        frase = m.group(2)
    if cierre:
        # el "guarda este post" ya va arriba en la ceja, no se repite abajo
        frase = re.sub(r"[\s.!¡]*[¡!]?\s*GUARDA ESTE POST[\s!💪🔥🙌]*$", "",
                       frase, flags=re.I).strip(" .")

    if portada:
        foto = ENTRADA if semana % 4 == 0 else INTERIORES[(semana * 3) % len(INTERIORES)]
    else:
        foto = INTERIORES[(semana * 2 + i) % len(INTERIORES)]

    if cierre:
        v = dict(tinte="rgba(199,16,27,.84)", tinte_html='<div class="tinte"></div>',
                 texto=HUESO, filo=NEGRO, ceja=HUESO, cifra=NEGRO,
                 pie="rgba(245,241,234,.78)", pieFuerte=HUESO,
                 ceja_txt="Guarda este post")
    elif portada:
        v = dict(tinte="none", tinte_html="", texto=HUESO, filo=ROJO, ceja=ROJO,
                 cifra=ORO, pie="rgba(245,241,234,.62)", pieFuerte=ORO,
                 ceja_txt="WGYMADNSPORT · Tocopilla")
    else:
        v = dict(tinte="none", tinte_html="", texto=HUESO, filo=ORO, ceja=ORO,
                 cifra=ORO, pie="rgba(245,241,234,.62)", pieFuerte=HUESO,
                 ceja_txt="Semana %d" % semana)

    v.update(anton=recursos["anton"], bc=recursos["bc"], logo=recursos["logo"],
             foto=recursos["fondos"][foto], negro=NEGRO,
             n=i + 1, total=total, cifra_html=cifra_html, frase=frase,
             tam=tamano(frase))
    return PLANTILLA % v


def buscar_chromium():
    """Playwright a veces apunta a un chromium que no esta bajado. Si hay uno
    instalado en la maquina, se usa ese; si no, se deja que Playwright elija."""
    import glob, os
    base = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    for patron in ("chromium-*/chrome-linux/chrome",
                   "chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"):
        encontrados = sorted(glob.glob(os.path.join(base, patron)))
        if encontrados:
            return encontrados[-1]
    return None


def texto_de_la_semana(sem):
    lineas = ["SEMANA %d · %s" % (sem["semana"], sem["tema"].upper()), ""]
    lineas.append(sem["bajada"])
    lineas.append("")
    for d in sem["dias"]:
        lineas.append("=" * 62)
        lineas.append("%s · %s" % (d["dia"].upper(), d["formato"].upper()))
        lineas.append(d["titulo"])
        lineas.append("")
        for b in d["bloques"]:
            lineas.append("--- %s ---" % b["etq"].upper())
            lineas.append(b["txt"])
            lineas.append("")
        if d.get("grabar"):
            lineas.append("QUÉ GRABAR: " + d["grabar"])
            lineas.append("")
        if d.get("ojo"):
            lineas.append("OJO CON ESTO: " + d["ojo"])
            lineas.append("")
    return "\n".join(lineas)


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python3 contenido/semana.py <numero de semana 1-16>")
    n = int(sys.argv[1])

    semanas = json.loads((AQUI / "contenido.json").read_text(encoding="utf-8"))
    sem = next((s for s in semanas if s["semana"] == n), None)
    if sem is None:
        sys.exit("no existe la semana %d (hay %d)" % (n, len(semanas)))

    destino = AQUI / "salida" / ("semana-%02d" % n)
    destino.mkdir(parents=True, exist_ok=True)

    (destino / ("semana-%02d-textos.txt" % n)).write_text(
        texto_de_la_semana(sem), encoding="utf-8")

    carrusel = next((d for d in sem["dias"] if d["formato"] == "carrusel"), None)
    if carrusel is None:
        print("semana %d lista (sin carrusel): %s" % (n, destino))
        return

    laminas = [b["txt"] for b in carrusel["bloques"] if b.get("clase") == "pantalla"]

    from playwright.sync_api import sync_playwright
    recursos = dict(anton=b64("fuentes/anton.woff2"), bc=b64("fuentes/bc800.woff2"),
                    logo=b64("logo.jpg"),
                    fondos={i: b64("fondos/f%d.jpg" % i) for i in range(1, 10)})

    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=buscar_chromium())
        pg = nav.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=1)
        for i, txt in enumerate(laminas):
            tmp = destino / "_lamina.html"
            tmp.write_text(html_lamina(n, i, len(laminas), txt, recursos), encoding="utf-8")
            pg.goto(tmp.resolve().as_uri())
            pg.wait_for_timeout(220)
            pg.screenshot(path=str(destino / ("lamina-%d-de-%d.png" % (i + 1, len(laminas)))))
            tmp.unlink()
        nav.close()

    print("semana %d lista: %s (%d laminas + textos)" % (n, destino, len(laminas)))


if __name__ == "__main__":
    main()
