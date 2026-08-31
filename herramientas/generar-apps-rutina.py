#!/usr/bin/env python3
"""
Arma las tres apps de entrenamiento, una por rutina:

    entrenar-mujeres.html · entrenar-hombres.html · entrenar-gluteos.html

Cada una lleva SOLO su rutina, para que a la socia no le aparezca la de
hombres ni al revés, y lleva su propio portón: entra el socio que está
vigente y al vencido lo manda a recepción.

Los ejercicios se sacan de las páginas de rutina que ya están publicadas
(rutina-principiantes-mujeres.html y las otras dos), y la lista de socios,
de control.html. Así no hay dos verdades: se corre este archivo de nuevo y
las apps quedan al día.

    python3 herramientas/generar-apps-rutina.py
"""
import io, json, os, re, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RUTINAS = {
    "mujeres": {
        "archivo": "rutina-principiantes-mujeres.html",
        "titulo":  "Rutina Mujeres",
        "corto":   "Rutina Mujeres",
        "marca1":  "RUTINA",
        "marca2":  "MUJERES",
        "bajada":  "Principiantes · 5 días",
    },
    "hombres": {
        "archivo": "rutina-principiantes-hombres.html",
        "titulo":  "Rutina Hombres",
        "corto":   "Rutina Hombres",
        "marca1":  "RUTINA",
        "marca2":  "HOMBRES",
        "bajada":  "Principiantes · 5 días",
    },
    "gluteos": {
        "archivo": "rutina-gluteos.html",
        "titulo":  "Rutina Glúteos",
        "corto":   "Rutina Glúteos",
        "marca1":  "RUTINA",
        "marca2":  "GLÚTEOS",
        "bajada":  "Glúteos y piernas · 5 días",
    },
}


def leer(nombre):
    return io.open(os.path.join(RAIZ, nombre), encoding="utf-8").read()


def datos_de_rutina(archivo):
    """Saca DAYS, VIDEOS, WARMUP_VIDEOS y COOLDOWN_VIDEOS de una página de
    rutina. Se usa node porque son objetos de JavaScript, no JSON."""
    guion = """
      const fs=require("fs");
      const s=fs.readFileSync(process.argv[1],"utf8");
      const get=n=>{const m=s.match(new RegExp("(?:const|var)\\\\s+"+n+
        "\\\\s*=\\\\s*([\\\\s\\\\S]*?);\\\\s*\\\\n"));return m?eval("("+m[1]+")"):null;};
      process.stdout.write(JSON.stringify({DAYS:get("DAYS"),VIDEOS:get("VIDEOS"),
        WARMUP:get("WARMUP_VIDEOS"),COOLDOWN:get("COOLDOWN_VIDEOS")}));
    """
    r = subprocess.run(["node", "-e", guion, os.path.join(RAIZ, archivo)],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit("No pude leer " + archivo + ": " + r.stderr[:300])
    d = json.loads(r.stdout)
    if not d["DAYS"]:
        sys.exit("No encontré los ejercicios en " + archivo)
    return d


def socios_de_rutina():
    """La lista de socios se copia TAL CUAL de rutina-principiantes-mujeres.html,
    línea por línea y sin tocar nada. Así cada socio queda escrito exactamente
    igual que en los demás archivos, y cuando haya que renovar a alguien la
    misma búsqueda encuentra su línea en los doce lados."""
    s = leer("rutina-principiantes-mujeres.html")
    m = re.search(r"const\s+SOCIOS\s*=\s*\[\n(.*?)\n\];", s, re.S)
    if not m:
        sys.exit("No encontré SOCIOS en rutina-principiantes-mujeres.html")
    filas = [l.strip() for l in m.group(1).splitlines() if l.strip().startswith("{n:")]
    if len(filas) < 50:
        sys.exit("La lista de socios salió demasiado corta: " + str(len(filas)))
    return filas


# El portón: reconoce al socio aunque escriba con faltas y le cierra la
# puerta al que tiene el plan vencido. Es el mismo criterio de las páginas
# de rutina, con un solo casillero para el nombre completo.
PORTON = '''
/* ═══ Los socios ════════════════════════════════════════════════════════
   Copia de la lista del mesón (control.html). Se mantiene con el mismo
   formato de una línea por socio que los demás archivos, para que una
   renovación se pueda cambiar igual en todos. */
var SOCIOS = [
__SOCIOS__
];

/* ═══ El portón ═════════════════════════════════════════════════════════
   Reconoce al socio aunque escriba con faltas de ortografía o al revés, y
   solo lo deja pasar si tiene el plan al día. */
function normName(s){
 return (s || "").toString().trim().toUpperCase()
  .normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").replace(/\\s+/g, " ");
}
function claveNombre(s){ return normName(s).replace(/\\s+/g, ""); }
function margen(q){ return q.length <= 8 ? 1 : (q.length <= 14 ? 2 : 3); }
function distanciaNombre(a, b){
 if(a === b) return 0;
 var la = a.length, lb = b.length;
 if(Math.abs(la - lb) > 4) return 99;
 var fila = [];
 for(var j = 0; j <= lb; j++) fila[j] = j;
 for(var i = 1; i <= la; i++){
  var ant = fila[0];
  fila[0] = i;
  for(var k = 1; k <= lb; k++){
   var tmp = fila[k];
   fila[k] = Math.min(fila[k] + 1, fila[k-1] + 1,
                      ant + (a.charAt(i-1) === b.charAt(k-1) ? 0 : 1));
   ant = tmp;
  }
 }
 return fila[lb];
}
/* El número de vencimiento cuenta los días desde el 30-12-1899. La fecha se
   arma en hora de Chile: en hora universal se corre un día para atrás y al
   socio se le cerraría la app el día antes de que se le venza. */
function fechaDeSerial(serial){
 var d = new Date(1899, 11, 30);
 d.setDate(d.getDate() + serial);
 d.setHours(0, 0, 0, 0);
 return d;
}
function diasHastaVencer(s){
 var hoy = new Date(); hoy.setHours(0, 0, 0, 0);
 return Math.round((fechaDeSerial(s.fv) - hoy) / 86400000);
}
function fechaVence(s){
 var d = fechaDeSerial(s.fv);
 return String(d.getDate()).padStart(2,"0") + "-" +
        String(d.getMonth()+1).padStart(2,"0") + "-" + d.getFullYear();
}
function buscarSocio(nombre, apellido){
 var n = normName(nombre), a = normName(apellido);
 if(!n || !a) return null;
 var exacto = null;
 SOCIOS.forEach(function(s){
  if(!exacto && normName(s.n) === n && normName(s.a) === a) exacto = s;
 });
 if(exacto) return exacto;
 /* Si no calza tal cual, el más parecido — salvo que haya dos igual de
    parecidos, porque ahí no se sabe cuál es y es mejor no adivinar. */
 var q = claveNombre(nombre + apellido);
 var mejor = null, mejorD = 99, empate = false;
 SOCIOS.forEach(function(s){
  var d = distanciaNombre(q, claveNombre(s.n + s.a));
  if(d < mejorD){ mejorD = d; mejor = s; empate = false; }
  else if(d === mejorD){ empate = true; }
 });
 if(mejor && mejorD <= margen(q) && !empate) return mejor;
 /* Último intento: si el apellido calza exacto y hay un solo socio con ese
    apellido, basta con que el nombre se le parezca. */
 var mismoApellido = SOCIOS.filter(function(s){ return normName(s.a) === a; });
 if(mismoApellido.length === 1 &&
    distanciaNombre(claveNombre(nombre), claveNombre(mismoApellido[0].n)) <= 3){
  return mismoApellido[0];
 }
 return null;
}
/* En la app se escribe todo junto en un solo casillero, así que hay que
   probar dónde termina el nombre y empieza el apellido. */
function buscarPorNombreCompleto(texto){
 var p = String(texto || "").trim().split(/\\s+/).filter(Boolean);
 if(!p.length) return null;
 if(p.length === 1) return buscarSocio(p[0], p[0]);
 for(var i = 1; i < p.length; i++){
  var s = buscarSocio(p.slice(0, i).join(" "), p.slice(i).join(" "));
  if(s) return s;
 }
 /* Hay gente que lo escribe al revés, primero el apellido. */
 for(var j = 1; j < p.length; j++){
  var r = buscarSocio(p.slice(j).join(" "), p.slice(0, j).join(" "));
  if(r) return r;
 }
 return buscarSocio(p[0], p.slice(1).join(" "));
}
'''

ENTRAR_NUEVO = '''function entrar(){
 var t = $("iNombre").value.trim().replace(/\\s+/g, " ");
 var av = $("avisoIngreso");
 if(t.length < 3){
  av.textContent = "Escribe tu nombre y tu apellido.";
  av.hidden = false; $("iNombre").focus(); return;
 }
 var s = buscarPorNombreCompleto(t);
 if(!s){
  av.innerHTML = "No encontramos ese nombre entre los socios. " +
                 "Revisa cómo lo escribiste o consulta en recepción.";
  av.hidden = false; return;
 }
 var dias = diasHastaVencer(s);
 if(dias < 0){
  /* Al vencido no se le abre, pero se le dice por qué y desde cuándo: es
     mucho más útil que un "no te encontramos" que no explica nada. */
  av.innerHTML = "<b>" + limpio(s.n + " " + s.a) + "</b>, tu plan venció el <b>" +
                 fechaVence(s) + "</b>.<br>Pasa a renovar en recepción y vuelves a entrar.";
  av.hidden = false; return;
 }
 D.socio = s.n + " " + s.a;
 D.avisoVence = (dias <= 3) ? { dias:dias, fecha:fechaVence(s) } : null;
 guardar();
 abrirInicio();
}'''

ARRANQUE_NUEVO = '''/* Al volver a abrir la app se comprueba de nuevo el vencimiento: si se le
   venció el plan desde la última vez, no sigue entrando con el permiso viejo. */
if(D.socio){
 var suyo = buscarPorNombreCompleto(D.socio);
 if(suyo && diasHastaVencer(suyo) >= 0){
  var dv = diasHastaVencer(suyo);
  D.avisoVence = (dv <= 3) ? { dias:dv, fecha:fechaVence(suyo) } : null;
  $("iNombre").value = D.socio;
  abrirInicio();
 }else{
  $("iNombre").value = D.socio;
  mostrar("p-ingreso");
  if(suyo){
   $("avisoIngreso").innerHTML = "<b>" + limpio(suyo.n + " " + suyo.a) +
    "</b>, tu plan venció el <b>" + fechaVence(suyo) +
    "</b>.<br>Pasa a renovar en recepción y vuelves a entrar.";
   $("avisoIngreso").hidden = false;
  }
 }
}else{'''


def una_app(clave, cfg, base, socios):
    d = datos_de_rutina(cfg["archivo"])
    s = base

    def uno(viejo, nuevo, cuantos=1):
        nonlocal s
        assert s.count(viejo) == cuantos, \
            "esperaba %d y hay %d de: %s" % (cuantos, s.count(viejo), viejo[:70])
        s = s.replace(viejo, nuevo)

    # ── nombre de la app en la pestaña, en el icono y en el encabezado
    uno("<title>Mi Entrenamiento · WGYMADNSPORT</title>",
        "<title>%s · WGYMADNSPORT</title>" % cfg["titulo"])
    uno('<link rel="manifest" href="entrenar.webmanifest">',
        '<link rel="manifest" href="entrenar-%s.webmanifest">' % clave)
    uno('<meta name="apple-mobile-web-app-title" content="Mi Entrenamiento">',
        '<meta name="apple-mobile-web-app-title" content="%s">' % cfg["corto"])
    uno("<h2>MI <span>ENTRENAMIENTO</span></h2>",
        "<h2>%s <span>%s</span></h2>" % (cfg["marca1"], cfg["marca2"]))
    uno("<h1>MI <span>ENTRENAMIENTO</span></h1>",
        "<h1>%s <span>%s</span></h1>" % (cfg["marca1"], cfg["marca2"]))
    uno('<p class="baja">Tu rutina, tus pesos y tu progreso.<br>Escribe tu nombre para empezar.</p>',
        '<p class="baja">%s<br>Escribe tu nombre y apellido para entrar.</p>' % cfg["bajada"])
    uno('content="App de entrenamiento para socios de WGYMADNSPORT Tocopilla: '
        'sigue tu rutina, anota tus pesos y tu progreso y mira cómo progresas."'
        if 'y tu progreso y mira' in base else
        'content="App de entrenamiento para socios de WGYMADNSPORT Tocopilla: '
        'sigue tu rutina, anota tus pesos y repeticiones y mira cómo progresas."',
        'content="%s de WGYMADNSPORT Tocopilla: sigue tu rutina, anota tus pesos '
        'y repeticiones y mira cómo progresas."' % cfg["titulo"])

    # ── esta app lleva una sola rutina, así que sobra el selector
    uno("""    <div class="seccion">
      <span class="etq">Mi rutina</span>
      <div class="rutinas" id="selRutina"></div>
    </div>

""", "")
    uno(" pintarRutinas();\n", "")
    uno("   pintarRutinas(); pintarDias();", "   pintarDias();")
    uno("""function pintarRutinas(){
 var cont = $("selRutina");
 cont.innerHTML = "";
 ORDEN.forEach(function(k){
  var b = document.createElement("button");
  b.type = "button";
  b.innerHTML = NOMBRE_RUTINA[k];
  b.setAttribute("aria-pressed", k === D.rutina ? "true" : "false");
  b.addEventListener("click", function(){
   D.rutina = k; guardar();
   pintarDias();
  });
  cont.appendChild(b);
 });
}

""", "")

    # ── los ejercicios: solo los de esta rutina
    viejo = re.search(r"var RUTINAS = \{.*?\n\};\n", s, re.S)
    assert viejo, "no encontré los ejercicios en la plantilla"
    s = s.replace(viejo.group(0),
                  "var RUTINAS = " + json.dumps({clave: d}, ensure_ascii=False, indent=1)
                  .replace("</", "<\\/") + ";\n")
    uno('var ORDEN = ["mujeres","hombres","gluteos"];',
        'var ORDEN = ["%s"];' % clave)
    uno('if(!D.rutina || !RUTINAS[D.rutina]) D.rutina = "mujeres";',
        'D.rutina = "%s";   /* esta app trae una sola rutina */' % clave)

    # ── cada app guarda lo suyo aparte, por si dos socios usan un mismo
    #    teléfono o alguien tiene dos rutinas
    uno('var KEY = "wgym_entrena_v1";', 'var KEY = "wgym_entrena_%s_v1";' % clave)

    # ── el portón, con la lista de socios
    uno("/* ═══ Ayudantes ════", PORTON.replace("__SOCIOS__", "\n".join(socios)) +
        "\n/* ═══ Ayudantes ════")

    # ── entrar ahora comprueba que esté vigente
    viejo_entrar = re.search(r"function entrar\(\)\{.*?\n\}\n", s, re.S)
    assert viejo_entrar, "no encontré entrar()"
    s = s.replace(viejo_entrar.group(0), ENTRAR_NUEVO + "\n")
    uno("if(D.socio){\n $(\"iNombre\").value = D.socio;\n abrirInicio();\n}else{",
        ARRANQUE_NUEVO)

    # ── el aviso de "te vence pronto" en la pantalla de inicio
    uno(' $("hQuien").textContent = D.socio || "";',
        ''' $("hQuien").textContent = D.socio || "";
 var av = $("avisoVence");
 if(D.avisoVence){
  av.hidden = false;
  av.innerHTML = D.avisoVence.dias === 0
   ? "Tu plan <b>vence hoy</b>. Pasa a renovar en recepción."
   : "Tu plan vence el <b>" + D.avisoVence.fecha + "</b>" +
     (D.avisoVence.dias === 1 ? " · mañana" : " · en " + D.avisoVence.dias + " días") +
     ". Acuérdate de renovar.";
 }else{ av.hidden = true; }''')
    uno('  <main id="p-inicio" hidden>\n', '''  <main id="p-inicio" hidden>
    <p class="avisovence" id="avisoVence" hidden></p>
''')
    uno(""".seguir p b{color:#fff}""",
        """.seguir p b{color:#fff}

/* Aviso de que se le viene el vencimiento encima. */
.avisovence{background:rgba(212,175,55,.13);border:1.5px solid var(--dorado);
  border-radius:12px;padding:13px 15px;margin-bottom:20px;font-size:16px;
  line-height:1.45;color:var(--crema)}
.avisovence b{color:var(--dorado)}""")

    return s


def manifest(clave, cfg):
    return json.dumps({
        "name": cfg["titulo"] + " · WGYMADNSPORT",
        "short_name": cfg["corto"],
        "description": cfg["titulo"] + " de WGYMADNSPORT Tocopilla.",
        "lang": "es-CL",
        "start_url": "entrenar-%s.html" % clave,
        "scope": ".",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#0A0A0A",
        "theme_color": "#0A0A0A",
        "icons": [
            {"src": "assets/logo.jpg", "sizes": "512x512", "type": "image/jpeg", "purpose": "any"},
            {"src": "assets/logo.jpg", "sizes": "192x192", "type": "image/jpeg", "purpose": "any"},
        ],
    }, ensure_ascii=False, indent=2) + "\n"


def main():
    base = leer("herramientas/base-app.html")
    socios = socios_de_rutina()
    print("socios en la lista: %d" % len(socios))
    for clave, cfg in RUTINAS.items():
        html = una_app(clave, cfg, base, socios)
        io.open(os.path.join(RAIZ, "entrenar-%s.html" % clave), "w",
                encoding="utf-8").write(html)
        io.open(os.path.join(RAIZ, "entrenar-%s.webmanifest" % clave), "w",
                encoding="utf-8").write(manifest(clave, cfg))
        print("  entrenar-%s.html  %.1f KB" % (clave, len(html.encode()) / 1024))


if __name__ == "__main__":
    main()
