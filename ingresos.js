/* Panel "INGRESOS DE HOY" (10/2026): todos los ingresos del día, quién
   sigue dentro del gimnasio y el botón MARCAR SALIDA. Lo usan el mesón
   (control.html) y la tablet (pantalla.html), completo: contadores
   Ingresos / Personas / Dentro ahora, lista de quienes están dentro e
   historial. (La tarjeta del socio muestra solo "Dentro ahora", sin
   nombres, y no usa este archivo.)

   De dónde salen los datos: la hoja de Google del check-in (la misma de
   siempre), con la acción "listarIngresos" del Apps Script, que trae TODOS
   los ingresos del día según la fecha de Chile. La salida se guarda en esa
   misma hoja, así que la ven igual la compu, la tablet y la tarjeta del
   socio. Marcar o deshacer la salida de otra persona es solo de
   administración: va por POST con la clave (op.accionAdmin, que pone
   control.html), nunca por la URL.

   Un equipo recién abierto muestra lo que trae la hoja, no lo que haya
   visto antes: la copia guardada en el equipo solo se usa si no hay
   conexión (con aviso) o con el Apps Script antiguo.

   Si el Apps Script todavía no tiene las acciones nuevas, responde como
   antes (solo los últimos 20 ingresos). En ese caso el panel sigue
   funcionando con lo que este equipo alcanzó a ver y avisa que falta
   actualizar el script; MARCAR SALIDA queda desactivado. */
(function(){
"use strict";

var TZ = "America/Santiago";
var PREFIJO = "wgym_ingresos_v1_";
var DIAS_GUARDADOS = 60;

function diaCL(ts){
 try{
  return new Intl.DateTimeFormat("en-CA", { timeZone:TZ, year:"numeric", month:"2-digit", day:"2-digit" })
   .format(new Date(ts == null ? Date.now() : ts));
 }catch(e){
  var d = new Date(ts == null ? Date.now() : ts);
  return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
 }
}
function horaCL(ts){
 try{
  return new Intl.DateTimeFormat("es-CL", { timeZone:TZ, hour:"2-digit", minute:"2-digit", hour12:false })
   .format(new Date(ts));
 }catch(e){
  var d = new Date(ts);
  return String(d.getHours()).padStart(2,"0")+":"+String(d.getMinutes()).padStart(2,"0");
 }
}
function fechaLarga(dia){ var p = dia.split("-"); return p[2]+"-"+p[1]+"-"+p[0]; }
function norm(s){
 return String(s == null ? "" : s).toUpperCase().normalize("NFD")
  .replace(/[̀-ͯ]/g, "").replace(/\s+/g, " ").trim();
}
function persona(r){ return norm(r.nombre) + "|" + norm(r.apellido); }
function llave(r){ return r.ts + "|" + persona(r); }
function esc(s){
 return String(s == null ? "" : s).replace(/[&<>"']/g, function(c){
  return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]; });
}

/* ── copia local por día (respaldo, nunca la fuente principal) ── */
function leerLocal(dia){
 try{ var v = JSON.parse(localStorage.getItem(PREFIJO + dia) || "[]"); return Array.isArray(v) ? v : []; }
 catch(e){ return []; }
}
function guardarLocal(dia, filas){
 try{ localStorage.setItem(PREFIJO + dia, JSON.stringify(filas)); }catch(e){}
}
function limpiarViejos(){
 try{
  var corte = diaCL(Date.now() - DIAS_GUARDADOS * 86400000);
  for(var i = localStorage.length - 1; i >= 0; i--){
   var k = localStorage.key(i);
   if(k && k.indexOf(PREFIJO) === 0 && k.slice(PREFIJO.length) < corte) localStorage.removeItem(k);
  }
 }catch(e){}
}
/* Junta lo que ya tenía este equipo con lo nuevo, sin perder ninguna fila. */
function unir(viejas, nuevas){
 var por = {}, orden = [];
 viejas.concat(nuevas).forEach(function(r){
  var k = llave(r);
  if(!por[k]){ por[k] = r; orden.push(k); }
  else if(r.salida && !por[k].salida) por[k] = r;
 });
 return orden.map(function(k){ return por[k]; }).sort(function(a, b){ return b.ts - a.ts; });
}
function esPase(r){ return String(r && r.venc || "").toUpperCase() === "PASE DIARIO"; }
function limpiarFila(r){
 return { ts:Number(r.ts) || 0, nombre:String(r.nombre || ""), apellido:String(r.apellido || ""),
          fila:Number(r.fila) || 0, salida:Number(r.salida) || 0, origen:String(r.origen || ""),
          venc:String(r.venc || "") };
}

/* ── JSONP, igual que el resto de las llamadas al check-in ── */
var nCb = 0;
function jsonp(url, params, listo){
 var cb = "wgymIng" + (++nCb) + "_" + Date.now();
 var s = document.createElement("script"), hecho = false;
 var plazo = setTimeout(function(){ fin(null); }, 15000);
 function fin(data){
  if(hecho) return; hecho = true; clearTimeout(plazo);
  try{ delete window[cb]; }catch(e){ window[cb] = undefined; }
  s.remove(); listo(data);
 }
 window[cb] = fin;
 var q = Object.keys(params).map(function(k){ return k + "=" + encodeURIComponent(params[k]); }).join("&");
 s.src = url + "?" + q + "&callback=" + cb + "&_=" + Date.now();
 s.onerror = function(){ fin(null); };
 document.body.appendChild(s);
}

/* Acciones de administración por POST con la clave guardada en ESE equipo
   (la misma clave y el mismo lugar que usa control.html para guardar
   socios). La tablet usa esta; control.html pasa la suya propia. */
var CLAVE_ADMIN_LS = "wgym_clave_admin_v1";
function accionAdminPorDefecto(url){
 return function llamar(action, params, cb, reintento){
  var clave = "";
  try{ clave = localStorage.getItem(CLAVE_ADMIN_LS) || ""; }catch(e){}
  if(!clave){
   clave = prompt("Clave de administración (se pide solo esta vez en este equipo):") || "";
   if(!clave){ cb(false, "sin clave"); return; }
   try{ localStorage.setItem(CLAVE_ADMIN_LS, clave); }catch(e){}
  }
  var cuerpo = new URLSearchParams(Object.assign({ action:action, clave:clave }, params));
  fetch(url, { method:"POST", body:cuerpo })
   .then(function(r){ return r.json(); })
   .then(function(data){
    if(data && data.ok){ cb(true, data); return; }
    if(data && data.error === "clave incorrecta"){
     try{ localStorage.removeItem(CLAVE_ADMIN_LS); }catch(e){}
     if(!reintento){ llamar(action, params, cb, true); return; }
    }
    cb(false, (data && data.error) || "no se pudo guardar");
   })
   ["catch"](function(){ cb(false, "sin conexión"); });
 };
}

var CSS = '' +
'.ing-barra{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px}' +
'.ing-barra input{background:var(--surface,#161616);border:1px solid var(--line,#2A2A2A);color:#fff;border-radius:10px;padding:10px 12px;font:600 14px inherit;font-family:inherit}' +
'.ing-barra input[type=search]{flex:1;min-width:180px}' +
'.ing-barra input:focus{outline:none;border-color:var(--dorado,#D4AF37)}' +
'.ing-tot{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:0 0 12px}' +
'.ing-tot div{background:var(--surface,#161616);border:1px solid var(--line,#2A2A2A);border-radius:12px;padding:10px;text-align:center}' +
'.ing-tot b{display:block;font-size:24px;font-weight:900;color:#fff;line-height:1.1}' +
'.ing-tot span{font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--gris-soft,#8C8C8C)}' +
'.ing-tot .dentro{border-color:rgba(92,168,92,.5)}' +
'.ing-est.pase{color:#0A0A0B;background:var(--dorado,#D4AF37);border:1px solid var(--dorado,#D4AF37)}' +
'.ing-pases{background:var(--surface,#161616);border:1px solid rgba(212,175,55,.55);border-radius:12px;padding:10px 12px;margin:0 0 12px;font-size:13px;color:#E8E8E8;line-height:1.5}' +
'.ing-pases b{color:var(--dorado,#D4AF37);letter-spacing:.06em;text-transform:uppercase;font-size:12px}' +
'.ing-tot .dentro b,.ing-tot .dentro span{color:var(--verde,#5CA85C)}' +
'.ing-compacto .ing-tot{grid-template-columns:1fr 1fr}' +
'.ing-compacto .ing-tot .dentro{grid-column:1 / -1}' +
'.ing-compacto .ing-item{flex-wrap:wrap}' +
'.ing-aviso{border:1px solid var(--dorado,#D4AF37);background:rgba(212,175,55,.1);color:#F4D03F;border-radius:10px;padding:9px 12px;font-size:13px;font-weight:700;margin:0 0 10px}' +
'.ing-aviso.mal{border-color:var(--rojo-claro,#E85C5C);background:rgba(232,92,92,.1);color:var(--rojo-claro,#E85C5C)}' +
'.ing-sub{display:flex;align-items:center;justify-content:space-between;margin:14px 0 8px;font-size:12.5px;font-weight:900;letter-spacing:.1em;text-transform:uppercase;color:var(--dorado,#D4AF37)}' +
'.ing-sub .n{color:var(--gris-soft,#8C8C8C)}' +
'.ing-todos{display:block;width:100%;margin:0 0 8px;background:transparent;color:var(--rojo-claro,#E85C5C);border:1px dashed var(--rojo-claro,#E85C5C);border-radius:10px;padding:9px;font:800 12.5px inherit;font-family:inherit;letter-spacing:.06em;text-transform:uppercase;cursor:pointer}' +
'.ing-todos[disabled]{opacity:.5;cursor:default}' +
'.ing-lista{max-height:460px;overflow-y:auto;padding-right:4px;display:flex;flex-direction:column;gap:6px}' +
'.ing-item{display:flex;align-items:center;gap:10px;background:var(--card,#1c1c1c);border:1px solid var(--line,#2A2A2A);border-radius:12px;padding:10px 12px}' +
'.ing-item.dentro{border-left:4px solid var(--verde,#5CA85C)}' +
'.ing-item.salio{border-left:4px solid #555}' +
'.ing-item .inf{flex:1;min-width:0;display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px}' +
'.ing-item .nom{font-weight:800;font-size:15px;cursor:pointer}' +
'.ing-item .hr{font-size:12.5px;color:var(--gris-soft,#8C8C8C);font-weight:700}' +
'.ing-est{font-size:11px;font-weight:900;letter-spacing:.06em;padding:3px 9px;border-radius:999px;white-space:nowrap}' +
'.ing-est.dentro{color:var(--verde,#5CA85C);background:rgba(92,168,92,.13);border:1px solid rgba(92,168,92,.5)}' +
'.ing-est.salio{color:var(--gris,#CFCFCF);background:#262626;border:1px solid #3a3a3a}' +
'.ing-btn{flex:0 0 auto;border:1px solid var(--dorado,#D4AF37);background:var(--rojo,#E30613);color:#fff;font:900 12px inherit;font-family:inherit;letter-spacing:.06em;text-transform:uppercase;border-radius:10px;padding:9px 12px;cursor:pointer}' +
'.ing-btn[disabled]{opacity:.45;cursor:default}' +
'.ing-des{flex:0 0 auto;background:none;border:none;color:var(--gris-soft,#8C8C8C);font:700 12px inherit;font-family:inherit;text-decoration:underline;cursor:pointer;padding:6px}' +
'.ing-vacio{text-align:center;color:var(--gris-soft,#8C8C8C);font-size:13.5px;padding:18px 0}';

function crear(op){
 var raiz = op.raiz, url = op.url;
 if(!op.accionAdmin) op.accionAdmin = accionAdminPorDefecto(url);
 /* Páginas prueba-*.html: todo va a la hoja "Pruebas ingresos". */
 var extraPrueba = window.WGYM_PRUEBA_INGRESOS ? { prueba:"1" } : {};
 var admin = op.accionAdmin;
 op.accionAdmin = function(action, params, cb){ admin(action, Object.assign({}, params, extraPrueba), cb); };
 var hoy = diaCL(), dia = hoy, filas = [], modoNuevo = null, pendientes = {}, mensaje = "", mensajeAccion = "", plazoAccion = null;
 /* cargado: ya llegó al menos una respuesta de la hoja para este día. Antes
    de eso no se muestra la copia del equipo: un aparato recién abierto ve
    lo que dice Google, no lo que haya visto antes. */
 var cargado = false;
 limpiarViejos();

 if(!document.getElementById("ingCss")){
  var st = document.createElement("style"); st.id = "ingCss"; st.textContent = CSS;
  document.head.appendChild(st);
 }
 if(op.compacto) raiz.classList.add("ing-compacto");
 raiz.innerHTML =
  '<div class="ing-barra">' +
   '<input type="date" class="ing-fecha" aria-label="Ver otro día">' +
   '<input type="search" class="ing-q" placeholder="Buscar por nombre…" aria-label="Buscar ingreso por nombre" autocomplete="off">' +
  '</div>' +
  '<div class="ing-avisos"></div>' +
  '<div class="ing-tot"></div>' +
  '<div class="ing-pases" hidden></div>' +
  '<div class="ing-sub"><span>🟢 Dentro del gimnasio</span><span class="n ing-n-dentro"></span></div>' +
  '<button type="button" class="ing-todos" hidden>Marcar salida a todos</button>' +
  '<div class="ing-lista ing-dentro"></div>' +
  '<div class="ing-sub"><span>📋 Historial del día</span><span class="n ing-n-hist"></span></div>' +
  '<div class="ing-lista ing-hist"></div>';
 var $ = function(c){ return raiz.querySelector(c); };
 var fecha = $(".ing-fecha"), q = $(".ing-q");
 fecha.value = dia; fecha.max = hoy;

 function titulo(){
  if(op.alTitulo) op.alTitulo(dia === hoy ? "Ingresos de hoy" : "Ingresos del " + fechaLarga(dia));
 }
 function aplicar(data, deDia){
  if(deDia !== dia) return;            /* llegó tarde, ya se cambió de día */
  if(!data){
   /* Sin respuesta: si nunca llegó nada, se muestra la copia del equipo
      con un aviso; si ya había datos de la hoja, se dejan tal cual. */
   if(!cargado){ filas = leerLocal(deDia); mensaje = "Sin conexión con la hoja de ingresos: se muestra lo último guardado en este equipo (puede estar incompleto)."; }
   else mensaje = "Sin conexión con la hoja de ingresos: reintentando…";
   pintar(); return;
  }
  mensaje = "";
  var nuevas = (data.rows || []).map(limpiarFila).filter(function(r){ return r.ts && diaCL(r.ts) === deDia; });
  if(data.ingresos === true){
   modoNuevo = true;
   /* La hoja manda: trae el día completo con sus salidas, y eso es
      exactamente lo que se muestra (la copia del equipo no se mezcla). */
   filas = nuevas.sort(function(a, b){ return b.ts - a.ts; });
  }else{
   /* Apps Script antiguo (solo los últimos 20): se junta con lo que este
      equipo ya había visto, para no perder a los primeros del día. */
   if(!cargado) filas = leerLocal(deDia);
   modoNuevo = false;
   filas = unir(filas, nuevas);
  }
  cargado = true;
  /* Una salida recién marcada acá todavía no viene en la respuesta. */
  filas.forEach(function(r){ var p = pendientes[persona(r)]; if(p && !r.salida) r.salida = p; });
  guardarLocal(deDia, filas);
  pintar();
 }
 function pedirDia(){
  var d = dia;
  jsonp(url, Object.assign({ action:"listarIngresos", dia:d }, extraPrueba), function(data){ aplicar(data, d); });
 }

 function coincide(r){
  var t = norm(q.value);
  if(!t) return true;
  var nom = norm(r.nombre + " " + r.apellido);
  return t.split(" ").every(function(p){ return nom.indexOf(p) > -1; });
 }
 function itemHtml(r, tipo){
  var abierta = !r.salida;
  /* Pase diario (registrado desde el cuadro "Pase diario" del mesón):
     etiqueta dorada en vez de la nota de ficha de socio, que no tiene. */
  var extra = esPase(r) ? '<span class="ing-est pase">PASE DIARIO</span>' : op.extraHtml ? op.extraHtml(r) : "";
  var est = abierta
   ? '<span class="ing-est dentro">DENTRO</span>'
   : '<span class="ing-est salio">SALIDA REGISTRADA · ' + horaCL(r.salida) + '</span>';
  var hora = tipo === "dentro"
   ? '<span class="hr">desde ' + horaCL(r.desde) + (r.veces > 1 ? ' · ' + r.veces + ' ingresos' : '') + '</span>'
   : '<span class="hr">entró ' + horaCL(r.ts) + (r.de > 1 ? ' · ingreso ' + r.n + ' de ' + r.de : '') + '</span>';
  var btn = "";
  if(abierta){
   var off = modoNuevo !== true || pendientes[persona(r)];
   btn = '<button type="button" class="ing-btn" data-sal="' + esc(persona(r)) + '"' +
    (off ? ' disabled title="' + (modoNuevo === false ? 'Falta actualizar el Apps Script' : 'Guardando…') + '"' : '') + '>Marcar salida</button>';
  }else if(tipo === "hist" && r.fila && modoNuevo === true){
   btn = '<button type="button" class="ing-des" data-fila="' + r.fila + '" data-ts="' + r.ts + '">Deshacer</button>';
  }
  return '<div class="ing-item ' + (abierta ? "dentro" : "salio") + '">' +
   '<span class="inf"><span class="nom" data-k="' + esc(llave(r)) + '">' + esc(r.nombre + " " + r.apellido) + '</span>' +
   hora + est + extra + '</span>' + btn + '</div>';
 }
 function pintar(){
  titulo();
  var avisos = "";
  if(modoNuevo === false) avisos += '<div class="ing-aviso">Falta actualizar el Apps Script del check-in: por ahora se muestran los ingresos que este equipo alcanzó a ver y MARCAR SALIDA queda desactivado.</div>';
  if(mensaje) avisos += '<div class="ing-aviso mal">' + esc(mensaje) + '</div>';
  if(mensajeAccion) avisos += '<div class="ing-aviso mal">' + esc(mensajeAccion) + '</div>';
  $(".ing-avisos").innerHTML = avisos;

  /* Dentro: una fila por persona con al menos un ingreso sin salida. */
  var porP = {}, ordenP = [];
  filas.forEach(function(r){
   var k = persona(r);
   if(!porP[k]){ porP[k] = { nombre:r.nombre, apellido:r.apellido, ts:r.ts, desde:0, veces:0, salida:0, abiertas:0, venc:"" }; ordenP.push(k); }
   if(esPase(r)) porP[k].venc = r.venc;
   var g = porP[k]; g.veces++;
   if(!r.salida){ g.abiertas++; if(!g.desde || r.ts < g.desde) g.desde = r.ts; }
  });
  /* Socios que vienen varias veces al día: cada fila del historial dice
     qué ingreso del día es ("ingreso 2 de 3"). */
  var tsP = {};
  filas.forEach(function(r){ (tsP[persona(r)] = tsP[persona(r)] || []).push(r.ts); });
  filas.forEach(function(r){
   var l = tsP[persona(r)].slice().sort(function(x, y){ return x - y; });
   r.de = l.length; r.n = l.indexOf(r.ts) + 1;
  });
  var dentro = ordenP.map(function(k){ return porP[k]; }).filter(function(g){ return g.abiertas > 0; })
   .sort(function(a, b){ return a.desde - b.desde; });

  $(".ing-tot").innerHTML =
   '<div><b>' + filas.length + '</b><span>Ingresos</span></div>' +
   '<div><b>' + ordenP.length + '</b><span>Personas</span></div>' +
   '<div class="dentro"><b>' + dentro.length + '</b><span>Dentro ahora</span></div>';

  /* Quiénes entraron con pase diario este día (nombre y hora). */
  /* Una persona por pase, aunque entre y salga varias veces en el día. */
  var pases = [], vistosP = {};
  filas.filter(esPase).slice().sort(function(a, b){ return a.ts - b.ts; }).forEach(function(r){
   var k = persona(r);
   if(vistosP[k]){ vistosP[k].veces++; return; }
   vistosP[k] = { r:r, veces:1 }; pases.push(vistosP[k]);
  });
  var bp = $(".ing-pases");
  bp.hidden = !pases.length;
  bp.innerHTML = pases.length ? '<b>🎟 Pases diarios: ' + pases.length + '</b><br>' +
   pases.map(function(p){ return esc(p.r.nombre + " " + p.r.apellido) + ' (' + horaCL(p.r.ts) +
    (p.veces > 1 ? ' · ' + p.veces + ' ingresos' : '') + ')'; }).join(" · ") : "";
  var dVis = dentro.filter(coincide), hVis = filas.filter(coincide);
  $(".ing-n-dentro").textContent = dVis.length + (dVis.length !== dentro.length ? " de " + dentro.length : "");
  $(".ing-n-hist").textContent = hVis.length + (hVis.length !== filas.length ? " de " + filas.length : "");
  /* "Marcar salida a todos": para cerrar el día o limpiar a quienes se
     fueron sin marcar (solo cuando hay 2 o más y el script está al día). */
  var bt = $(".ing-todos");
  bt.hidden = !(modoNuevo === true && dentro.length > 1 && !q.value);
  if(!enCurso) { bt.disabled = false; bt.textContent = "Marcar salida a todos (" + dentro.length + ")"; }
  $(".ing-dentro").innerHTML = dVis.length ? dVis.map(function(g){ return itemHtml(g, "dentro"); }).join("")
   : '<div class="ing-vacio">' + (!cargado ? "Cargando ingresos desde Google…" : q.value ? "Nadie con ese nombre dentro." : "No hay nadie dentro sin salida registrada.") + '</div>';
  $(".ing-hist").innerHTML = hVis.length ? hVis.map(function(r){ return itemHtml(r, "hist"); }).join("")
   : '<div class="ing-vacio">' + (!cargado ? "Cargando ingresos desde Google…" : q.value ? "Ningún ingreso con ese nombre." : "Todavía no hay ingresos registrados este día.") + '</div>';
 }

 /* Los errores de MARCAR SALIDA / Deshacer quedan a la vista 20 segundos
    (el sondeo de cada 4 segundos no los borra). */
 function avisarAccion(t){
  mensajeAccion = t; clearTimeout(plazoAccion);
  plazoAccion = setTimeout(function(){ mensajeAccion = ""; pintar(); }, 20000);
  pintar();
 }
 function textoError(info){
  if(info === "sin clave" || info === "clave incorrecta") return "hace falta la clave de administración.";
  if(info === "sin conexión") return "sin conexión, inténtalo de nuevo.";
  return "inténtalo de nuevo.";
 }
 function marcarSalida(k){
  var r = null;
  filas.forEach(function(x){ if(!r && persona(x) === k) r = x; });
  if(!r) return;
  var ahora = Date.now(), d = dia;
  pendientes[k] = ahora;
  filas.forEach(function(x){ if(persona(x) === k && !x.salida) x.salida = ahora; });
  pintar();
  /* Solo administración: va por POST con la clave (op.accionAdmin). */
  op.accionAdmin("registrarSalida", { nombre:r.nombre, apellido:r.apellido, dia:d }, function(ok, info){
   delete pendientes[k];
   if(!ok){
    filas.forEach(function(x){ if(persona(x) === k && x.salida === ahora) x.salida = 0; });
    avisarAccion("No se guardó la salida de " + r.nombre + " " + r.apellido + ": " + textoError(info));
    return;
   }
   pedirDia();
  });
 }
 /* Una por una (así la clave se pide una sola vez y no se satura el script). */
 var enCurso = false;
 function marcarTodos(){
  var claves = {}, lista = [];
  filas.forEach(function(x){ var k = persona(x); if(!x.salida && !claves[k]){ claves[k] = 1; lista.push(x); } });
  if(lista.length < 2 || !confirm("¿Marcar la salida de las " + lista.length + " personas que siguen dentro?")) return;
  enCurso = true;
  var bt = $(".ing-todos"), hechas = 0, fallas = 0, d = dia;
  bt.disabled = true;
  (function siguiente(i){
   if(i >= lista.length){
    enCurso = false;
    if(fallas) avisarAccion("No se pudo marcar la salida de " + fallas + (fallas === 1 ? " persona" : " personas") + ". Inténtalo de nuevo.");
    pedirDia(); return;
   }
   var r = lista[i], k = persona(r), ahora = Date.now();
   bt.textContent = "Marcando salidas… " + (i + 1) + " de " + lista.length;
   pendientes[k] = ahora;
   filas.forEach(function(x){ if(persona(x) === k && !x.salida) x.salida = ahora; });
   pintar();
   op.accionAdmin("registrarSalida", { nombre:r.nombre, apellido:r.apellido, dia:d }, function(ok, info){
    delete pendientes[k];
    if(!ok){
     filas.forEach(function(x){ if(persona(x) === k && x.salida === ahora) x.salida = 0; });
     fallas++;
     if(info === "sin clave" || info === "clave incorrecta"){ fallas += lista.length - i - 1; siguiente(lista.length); return; }
    }else hechas++;
    siguiente(i + 1);
   });
  })(0);
 }
 function deshacer(fila, ts){
  var r = null;
  filas.forEach(function(x){ if(x.fila === fila && x.ts === ts) r = x; });
  if(!r || !confirm("¿Deshacer la salida de " + r.nombre + " " + r.apellido + "?")) return;
  var antes = r.salida; r.salida = 0; pintar();
  op.accionAdmin("quitarSalida", { fila:fila, ts:ts }, function(ok, info){
   if(!ok){ r.salida = antes; avisarAccion("No se pudo deshacer: " + textoError(info)); return; }
   pedirDia();
  });
 }

 raiz.addEventListener("click", function(ev){
  if(ev.target.closest(".ing-todos")){ if(!enCurso) marcarTodos(); return; }
  var b = ev.target.closest("[data-sal]");
  if(b && !b.disabled){ marcarSalida(b.getAttribute("data-sal")); return; }
  var u = ev.target.closest("[data-fila]");
  if(u){ deshacer(Number(u.getAttribute("data-fila")), Number(u.getAttribute("data-ts"))); return; }
  var n = ev.target.closest(".nom");
  if(n && op.alTocar){
   var k = n.getAttribute("data-k"), r = null;
   filas.forEach(function(x){ if(llave(x) === k) r = x; });
   if(r) op.alTocar(r);
  }
 });
 q.addEventListener("input", pintar);
 fecha.addEventListener("change", function(){
  var v = fecha.value;
  if(!/^\d{4}-\d{2}-\d{2}$/.test(v) || v > hoy){ fecha.value = dia; return; }
  dia = v; filas = []; cargado = false; mensaje = ""; pintar(); pedirDia();
 });

 /* Cada cuanto se vuelve a preguntar por un día pasado (el de hoy llega
    solo con el sondeo de la página). */
 setInterval(function(){
  var h = diaCL();
  if(h !== hoy){                      /* pasó la medianoche */
   var eraHoy = dia === hoy; hoy = h; fecha.max = hoy;
   if(eraHoy){ dia = hoy; fecha.value = hoy; filas = []; cargado = false; pintar(); }
  }
  if(dia !== hoy) pedirDia();
 }, 30000);

 pintar();
 return {
  /* La página le pasa cada respuesta de su propio sondeo (el de hoy). */
  recibir:function(data){ if(dia === hoy) aplicar(data, hoy); },
  diaHoy:function(){ return hoy; },
  filas:function(){ return filas.slice(); }
 };
}

window.WgymIngresos = { crear:crear, diaCL:diaCL, horaCL:horaCL };
})();
