/* Panel "DENTRO DEL GIMNASIO" (10/2026) de control.html: el contador
   "DENTRO AHORA" (cada socio una sola vez), la lista de quienes tienen
   ingreso de hoy sin salida, con su botón MARCAR SALIDA, y el historial
   completo de cualquier día detrás del botón "VER HISTORIAL".

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
function limpiarFila(r){
 return { ts:Number(r.ts) || 0, nombre:String(r.nombre || ""), apellido:String(r.apellido || ""),
          fila:Number(r.fila) || 0, salida:Number(r.salida) || 0, origen:String(r.origen || "") };
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

var CSS = '' +
'.ing-aviso{border:1px solid var(--dorado,#D4AF37);background:rgba(212,175,55,.1);color:#F4D03F;border-radius:10px;padding:9px 12px;font-size:13px;font-weight:700;margin:0 0 10px}' +
'.ing-aviso.mal{border-color:var(--rojo-claro,#E85C5C);background:rgba(232,92,92,.1);color:var(--rojo-claro,#E85C5C)}' +
'.ing-contador{background:var(--surface,#161616);border:1px solid rgba(92,168,92,.45);border-radius:16px;padding:14px 12px 12px;text-align:center;margin:0 0 12px}' +
'.ing-contador b{display:block;font-size:68px;font-weight:900;line-height:1;color:var(--verde,#5CA85C);font-variant-numeric:tabular-nums}' +
'.ing-contador span{display:block;margin-top:6px;font-size:13px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:var(--verde,#5CA85C)}' +
'.ing-q,.ing-fecha{background:var(--surface,#161616);border:1px solid var(--line,#2A2A2A);color:#fff;border-radius:10px;padding:10px 12px;font:600 14px inherit;font-family:inherit;box-sizing:border-box}' +
'.ing-q{width:100%;margin:0 0 10px}' +
'.ing-q:focus,.ing-fecha:focus{outline:none;border-color:var(--dorado,#D4AF37)}' +
'.ing-lista{display:flex;flex-direction:column;gap:6px}' +
'.ing-hist .ing-lista{max-height:460px;overflow-y:auto;padding-right:4px}' +
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
'.ing-vacio{text-align:center;color:var(--gris-soft,#8C8C8C);font-size:13.5px;padding:18px 0}' +
'.ing-verhist{display:block;width:100%;margin:14px 0 0;background:transparent;color:var(--dorado,#D4AF37);border:1px solid var(--dorado,#D4AF37);border-radius:12px;padding:12px;font:900 13px inherit;font-family:inherit;letter-spacing:.1em;text-transform:uppercase;cursor:pointer}' +
'.ing-hist{margin-top:12px;border-top:1px solid var(--line,#2A2A2A);padding-top:12px}' +
'.ing-hist-barra{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 10px}' +
'.ing-hist-barra .ing-q{flex:1;min-width:160px;width:auto;margin:0}' +
'.ing-resumen{font-size:12.5px;color:var(--gris-soft,#8C8C8C);font-weight:700;margin:0 0 8px}';

/* Un "estado" por día: sus filas y si ya llegó respuesta de la hoja.
   cargado=false → todavía no se muestra la copia del equipo: un aparato
   recién abierto ve lo que dice Google, no lo que haya visto antes. */
function nuevoEstado(dia){ return { dia:dia, filas:[], cargado:false, mensaje:"" }; }

function crear(op){
 var raiz = op.raiz, url = op.url;
 var hoy = diaCL();
 var eHoy = nuevoEstado(hoy);          /* vista principal: siempre hoy */
 var eHist = null;                     /* historial de otro día (si se elige) */
 var histAbierto = false, modoNuevo = null, pendientes = {};
 var mensajeAccion = "", plazoAccion = null;
 limpiarViejos();

 if(!document.getElementById("ingCss")){
  var st = document.createElement("style"); st.id = "ingCss"; st.textContent = CSS;
  document.head.appendChild(st);
 }
 raiz.innerHTML =
  '<div class="ing-avisos"></div>' +
  '<div class="ing-contador"><b class="ing-n">—</b><span>Dentro ahora</span></div>' +
  '<input type="search" class="ing-q ing-q-dentro" placeholder="Buscar socio dentro…" aria-label="Buscar socio dentro del gimnasio" autocomplete="off">' +
  '<div class="ing-lista ing-dentro"></div>' +
  '<button type="button" class="ing-verhist" aria-expanded="false">📋 Ver historial</button>' +
  '<div class="ing-hist" hidden>' +
   '<div class="ing-hist-barra">' +
    '<input type="date" class="ing-fecha" aria-label="Día del historial">' +
    '<input type="search" class="ing-q ing-q-hist" placeholder="Buscar en el historial…" aria-label="Buscar en el historial" autocomplete="off">' +
   '</div>' +
   '<p class="ing-resumen"></p>' +
   '<div class="ing-lista ing-hist-lista"></div>' +
  '</div>';
 var $ = function(c){ return raiz.querySelector(c); };
 var fecha = $(".ing-fecha"), qD = $(".ing-q-dentro"), qH = $(".ing-q-hist");
 fecha.value = hoy; fecha.max = hoy;
 if(op.alTitulo) op.alTitulo("Dentro del gimnasio");

 function estadoHist(){ return eHist || eHoy; }

 function aplicar(e, data){
  if(!data){
   /* Sin respuesta: si nunca llegó nada, se muestra la copia del equipo
      con un aviso; si ya había datos de la hoja, se dejan tal cual. */
   if(!e.cargado){ e.filas = leerLocal(e.dia); e.mensaje = "Sin conexión con la hoja de ingresos: se muestra lo último guardado en este equipo (puede estar incompleto)."; }
   else e.mensaje = "Sin conexión con la hoja de ingresos: reintentando…";
   pintar(); return;
  }
  e.mensaje = "";
  var nuevas = (data.rows || []).map(limpiarFila).filter(function(r){ return r.ts && diaCL(r.ts) === e.dia; });
  if(data.ingresos === true){
   modoNuevo = true;
   /* La hoja manda: el día completo con sus salidas, tal cual. */
   e.filas = nuevas.sort(function(a, b){ return b.ts - a.ts; });
  }else{
   /* Apps Script antiguo (solo los últimos 20): se junta con lo que este
      equipo ya había visto, para no perder a los primeros del día. */
   if(!e.cargado) e.filas = leerLocal(e.dia);
   modoNuevo = false;
   e.filas = unir(e.filas, nuevas);
  }
  e.cargado = true;
  if(e === eHoy){
   /* Una salida recién marcada acá todavía no viene en la respuesta. */
   e.filas.forEach(function(r){ var p = pendientes[persona(r)]; if(p && !r.salida) r.salida = p; });
  }
  guardarLocal(e.dia, e.filas);
  pintar();
 }
 function pedir(e){
  jsonp(url, { action:"listarIngresos", dia:e.dia }, function(data){
   if(e === eHoy || e === eHist) aplicar(e, data);
  });
 }

 function coincide(q){
  var t = norm(q.value);
  return function(r){
   if(!t) return true;
   var nom = norm(r.nombre + " " + r.apellido);
   return t.split(" ").every(function(p){ return nom.indexOf(p) > -1; });
  };
 }
 /* Cada socio una sola vez: los que tienen al menos un ingreso de hoy sin
    salida, con la hora de su primer ingreso abierto. */
 function dentroDe(filas){
  var porP = {}, orden = [];
  filas.forEach(function(r){
   if(r.salida) return;
   var k = persona(r);
   if(!porP[k]){ porP[k] = { nombre:r.nombre, apellido:r.apellido, ts:r.ts, desde:r.ts }; orden.push(k); }
   else if(r.ts < porP[k].desde) porP[k].desde = r.ts;
  });
  return orden.map(function(k){ return porP[k]; }).sort(function(a, b){ return a.desde - b.desde; });
 }
 function itemDentro(g){
  var extra = op.extraHtml ? op.extraHtml(g) : "";
  var off = modoNuevo !== true || pendientes[persona(g)];
  return '<div class="ing-item dentro"><span class="inf">' +
   '<span class="nom" data-k="' + esc(llave(g)) + '">' + esc(g.nombre + " " + g.apellido) + '</span>' +
   '<span class="hr">desde ' + horaCL(g.desde) + '</span>' + extra + '</span>' +
   '<button type="button" class="ing-btn" data-sal="' + esc(persona(g)) + '"' +
   (off ? ' disabled title="' + (modoNuevo === false ? 'Falta actualizar el Apps Script' : 'Guardando…') + '"' : '') +
   '>Marcar salida</button></div>';
 }
 function itemHist(r){
  var abierta = !r.salida;
  var extra = op.extraHtml ? op.extraHtml(r) : "";
  return '<div class="ing-item ' + (abierta ? "dentro" : "salio") + '"><span class="inf">' +
   '<span class="nom" data-k="' + esc(llave(r)) + '">' + esc(r.nombre + " " + r.apellido) + '</span>' +
   '<span class="hr">entró ' + horaCL(r.ts) + '</span>' +
   (abierta ? '<span class="ing-est dentro">DENTRO</span>'
            : '<span class="ing-est salio">SALIDA REGISTRADA · ' + horaCL(r.salida) + '</span>') +
   extra + '</span>' +
   (!abierta && r.fila && modoNuevo === true
    ? '<button type="button" class="ing-des" data-fila="' + r.fila + '" data-ts="' + r.ts + '">Deshacer</button>' : '') +
   '</div>';
 }
 function pintar(){
  var avisos = "";
  if(modoNuevo === false) avisos += '<div class="ing-aviso">Falta actualizar el Apps Script del check-in: por ahora se muestran los ingresos que este equipo alcanzó a ver y MARCAR SALIDA queda desactivado.</div>';
  if(eHoy.mensaje) avisos += '<div class="ing-aviso mal">' + esc(eHoy.mensaje) + '</div>';
  if(mensajeAccion) avisos += '<div class="ing-aviso mal">' + esc(mensajeAccion) + '</div>';
  $(".ing-avisos").innerHTML = avisos;

  var dentro = dentroDe(eHoy.filas);
  $(".ing-n").textContent = eHoy.cargado ? dentro.length : "—";
  var dVis = dentro.filter(coincide(qD));
  $(".ing-dentro").innerHTML = dVis.length ? dVis.map(itemDentro).join("")
   : '<div class="ing-vacio">' + (!eHoy.cargado ? "Cargando ingresos desde Google…" : qD.value ? "Nadie con ese nombre dentro." : "No hay nadie dentro sin salida registrada.") + '</div>';

  if(!histAbierto) return;
  var e = estadoHist();
  var personas = {}; e.filas.forEach(function(r){ personas[persona(r)] = 1; });
  $(".ing-resumen").textContent = !e.cargado ? "" :
   (e.dia === hoy ? "Hoy" : fechaLarga(e.dia)) + ": " + e.filas.length + (e.filas.length === 1 ? " ingreso" : " ingresos") +
   " · " + Object.keys(personas).length + (Object.keys(personas).length === 1 ? " persona" : " personas") +
   (e.mensaje ? " · " + e.mensaje : "");
  var hVis = e.filas.filter(coincide(qH));
  $(".ing-hist-lista").innerHTML = hVis.length ? hVis.map(itemHist).join("")
   : '<div class="ing-vacio">' + (!e.cargado ? "Cargando historial desde Google…" : qH.value ? "Ningún ingreso con ese nombre." : "No hay ingresos registrados ese día.") + '</div>';
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
 function refrescar(){ pedir(eHoy); if(eHist) pedir(eHist); }
 function marcarSalida(k){
  var r = null;
  eHoy.filas.forEach(function(x){ if(!r && persona(x) === k) r = x; });
  if(!r) return;
  /* Sale de la lista y baja el contador al tiro; si no se pudo guardar,
     vuelve a aparecer con el aviso. */
  var ahora = Date.now();
  pendientes[k] = ahora;
  eHoy.filas.forEach(function(x){ if(persona(x) === k && !x.salida) x.salida = ahora; });
  pintar();
  /* Solo administración: va por POST con la clave (op.accionAdmin). */
  op.accionAdmin("registrarSalida", { nombre:r.nombre, apellido:r.apellido, dia:hoy }, function(ok, info){
   delete pendientes[k];
   if(!ok){
    eHoy.filas.forEach(function(x){ if(persona(x) === k && x.salida === ahora) x.salida = 0; });
    avisarAccion("No se guardó la salida de " + r.nombre + " " + r.apellido + ": " + textoError(info));
    return;
   }
   refrescar();
  });
 }
 function deshacer(fila, ts){
  var e = estadoHist(), r = null;
  e.filas.forEach(function(x){ if(x.fila === fila && x.ts === ts) r = x; });
  if(!r || !confirm("¿Deshacer la salida de " + r.nombre + " " + r.apellido + "?")) return;
  var antes = r.salida; r.salida = 0; pintar();
  op.accionAdmin("quitarSalida", { fila:fila, ts:ts }, function(ok, info){
   if(!ok){ r.salida = antes; avisarAccion("No se pudo deshacer: " + textoError(info)); return; }
   refrescar();
  });
 }

 raiz.addEventListener("click", function(ev){
  var b = ev.target.closest("[data-sal]");
  if(b && !b.disabled){ marcarSalida(b.getAttribute("data-sal")); return; }
  var u = ev.target.closest("[data-fila]");
  if(u){ deshacer(Number(u.getAttribute("data-fila")), Number(u.getAttribute("data-ts"))); return; }
  if(ev.target.closest(".ing-verhist")){
   histAbierto = !histAbierto;
   $(".ing-hist").hidden = !histAbierto;
   var vb = $(".ing-verhist");
   vb.textContent = histAbierto ? "Ocultar historial" : "📋 Ver historial";
   vb.setAttribute("aria-expanded", String(histAbierto));
   if(histAbierto && eHist) pedir(eHist);
   pintar(); return;
  }
  var n = ev.target.closest(".nom");
  if(n && op.alTocar){
   var k = n.getAttribute("data-k"), r = null;
   eHoy.filas.concat(eHist ? eHist.filas : []).forEach(function(x){ if(llave(x) === k) r = x; });
   if(r) op.alTocar(r);
  }
 });
 qD.addEventListener("input", pintar);
 qH.addEventListener("input", pintar);
 fecha.addEventListener("change", function(){
  var v = fecha.value;
  if(!/^\d{4}-\d{2}-\d{2}$/.test(v) || v > hoy){ fecha.value = estadoHist().dia; return; }
  eHist = v === hoy ? null : nuevoEstado(v);
  pintar();
  if(eHist) pedir(eHist);
 });

 /* Medianoche y refresco del historial de un día pasado (el de hoy llega
    solo con el sondeo de la página, cada 4 segundos). */
 setInterval(function(){
  var h = diaCL();
  if(h !== hoy){
   hoy = h; fecha.max = hoy; eHoy = nuevoEstado(hoy);
   if(!eHist) fecha.value = hoy;
   pintar();
  }
  if(histAbierto && eHist) pedir(eHist);
 }, 30000);

 pintar();
 return {
  /* La página le pasa cada respuesta de su propio sondeo (el de hoy). */
  recibir:function(data){ if(data) aplicar(eHoy, data); },
  diaHoy:function(){ return hoy; },
  dentro:function(){ return dentroDe(eHoy.filas); }
 };
}

window.WgymIngresos = { crear:crear, diaCL:diaCL, horaCL:horaCL };
})();
