/* Socios al día para las rutinas (10/2026).
   Desde que la compu de recepción guarda las altas y renovaciones en la hoja
   de Google (Apps Script, la misma que ya leen la tarjeta QR y la tablet),
   socios.json quedaba atrasado y los socios nuevos no podían entrar a su
   rutina. Este script hace que cada vez que una rutina pide socios.json reciba
   la planilla publicada JUNTO con la hoja en vivo:
   - socio que solo está en la hoja → se agrega;
   - socio que está en los dos → se queda la fecha de vencimiento más
     adelantada (nunca se acorta una membresía);
   - si la hoja no responde en 12 s (igual que la tarjeta QR), la rutina sigue con socios.json sola.
   Además, todo socio VIGENTE entra a cualquier rutina aunque escriba su nombre
   con una letra de más o de menos (KATERINE / KATHERINE), sin tildes, con o sin
   segundo apellido, o el apellido primero. Solo se acepta si el nombre escrito
   corresponde a UNA sola persona; si hay dos parecidas, se exige el nombre exacto.
   La hoja se pide apenas abre la página, así ya está lista al ingresar.
   Solo se LEE la lista (sin RUT); no se envía ningún dato a la hoja. */
(function(){
"use strict";
var HOJA="https://script.google.com/macros/s/AKfycbzDpqUW70UbZTQtH8X20EDdAGdQQbxBoKebYg2eDwX42A3yCXEpKacpnjtp8RjkBcNq/exec";
var originalFetch=window.fetch.bind(window);
function norm(s){return String(s||"").normalize("NFD").replace(/[̀-ͯ]/g,"").toUpperCase().replace(/[^A-Z ]/g,"").replace(/\s+/g," ").trim();}
var hojaPromise=null;
function leerHoja(){
 if(hojaPromise)return hojaPromise;
 hojaPromise=new Promise(function(resolve){
  var cb="wgymHoja_"+Date.now()+"_"+Math.floor(Math.random()*1e6),listo=false,script;
  function fin(lista){
   if(listo)return;listo=true;clearTimeout(reloj);
   try{delete window[cb];}catch(e){window[cb]=undefined;}
   if(script)script.remove();
   if(!lista.length)hojaPromise=null; /* falló: se reintenta al ingresar */
   resolve(lista);
  }
  var reloj=setTimeout(function(){fin([]);},12000);
  window[cb]=function(d){fin(d&&Array.isArray(d.socios)?d.socios:[]);};
  script=document.createElement("script");
  script.src=HOJA+"?action=listarSocios&callback="+cb+"&_="+Date.now();
  script.onerror=function(){fin([]);};
  (document.head||document.documentElement).appendChild(script);
 });
 return hojaPromise;
}
function juntar(base,hoja){
 var lista=(base||[]).slice(),idx={};
 lista.forEach(function(s,i){idx[norm(s.n)+"|"+norm(s.a)]=i;});
 hoja.forEach(function(h){
  if(!h||typeof h.n!=="string"||typeof h.a!=="string")return;
  var fv=Number(h.fv);if(!isFinite(fv))return;
  var k=norm(h.n)+"|"+norm(h.a);
  if(k==="|")return;
  if(idx[k]===undefined){
   var nuevo={n:h.n,a:h.a,rut:"Sin Rut",plan:String(h.plan||""),monto:Number(h.monto)||0,fv:fv};
   if(typeof h.medid==="string"&&/^[0-9a-f]{8}$/.test(h.medid))nuevo.medId=h.medid;
   idx[k]=lista.push(nuevo)-1;
  }else{
   var s=lista[idx[k]];
   if(fv>Number(s.fv)){s.fv=fv;if(h.plan)s.plan=String(h.plan);if(Number(h.monto))s.monto=Number(h.monto);}
  }
 });
 return lista;
}
function lev(a,b){
 if(Math.abs(a.length-b.length)>2)return 9;
 var prev=[],i,j;for(j=0;j<=b.length;j++)prev[j]=j;
 for(i=1;i<=a.length;i++){var cur=[i];for(j=1;j<=b.length;j++)cur[j]=Math.min(prev[j]+1,cur[j-1]+1,prev[j-1]+(a[i-1]===b[j-1]?0:1));prev=cur;}
 return prev[b.length];
}
function tokenIgual(t,m){
 if(t===m)return true;
 var tope=Math.min(t.length,m.length)>=7?2:Math.min(t.length,m.length)>=4?1:0;
 return tope>0&&lev(t,m)<=tope;
}
/* ¿Lo escrito (≥2 palabras) calza con este socio? Cada palabra escrita debe
   calzar con una palabra distinta del socio, y debe haber al menos una del
   nombre y una del apellido. */
function calza(escrito,s){
 var nom=norm(s.n).split(" ").filter(Boolean),ape=norm(s.a).split(" ").filter(Boolean);
 var todas=nom.map(function(w){return{w:w,t:"n"};}).concat(ape.map(function(w){return{w:w,t:"a"};}));
 var usado={},hayN=false,hayA=false;
 for(var i=0;i<escrito.length;i++){
  var ok=false;
  for(var k=0;k<todas.length;k++){
   if(usado[k]||!tokenIgual(escrito[i],todas[k].w))continue;
   usado[k]=true;ok=true;if(todas[k].t==="n")hayN=true;else hayA=true;break;
  }
  if(!ok)return false;
 }
 return hayN&&hayA;
}
function hoySerial(){
 var p=new Intl.DateTimeFormat("en-CA",{timeZone:"America/Santiago",year:"numeric",month:"2-digit",day:"2-digit"}).format(new Date()).split("-");
 return Math.round((Date.UTC(+p[0],+p[1]-1,+p[2])-Date.UTC(1899,11,30))/864e5);
}
/* Deja primero, ya con el nombre tal como lo escribió, al socio que corresponde
   (si es uno solo), para que la rutina lo encuentre. Entre fichas de la misma
   persona se queda la de fecha más adelantada. */
function ponerPrimero(lista){
 var campo=document.getElementById("member");
 var elegido=elegir(lista,campo&&campo.value);
 return elegido?[elegido].concat(lista):lista;
}
/* Busca al socio que corresponde a lo escrito (ver reglas arriba). Devuelve
   una copia de su ficha (con el nombre tal como lo escribió si no fue
   exacto) o null si no hay una sola persona que calce. */
function elegir(lista,texto){
 var escrito=norm(texto);
 var palabras=escrito.split(" ").filter(Boolean);
 if(palabras.length<2)return null;
 var exactos=lista.filter(function(s){return norm(s.n+" "+s.a)===escrito||norm(s.a+" "+s.n)===escrito;});
 var parecidos=lista.filter(function(s){return calza(palabras,s);});
 var hoy=hoySerial();
 function vigente(s){return Number(s.fv)>=hoy;}
 /* Si la ficha exacta está vencida pero hay una casi igual vigente (la
    renovación quedó guardada con una letra distinta), se toma esa. */
 if(exactos.length&&!exactos.some(vigente)&&parecidos.some(vigente)){
  var todos=exactos.concat(parecidos.filter(function(s){return exactos.indexOf(s)<0;}));
  var v=todos.filter(vigente),mv=v.reduce(function(a,b){return Number(b.fv)>Number(a.fv)?b:a;});
  if(todos.every(function(c){return calza(norm(c.n+" "+c.a).split(" "),mv);})){
   var c2=Object.assign({},mv);c2.n=exactos[0].n;c2.a=exactos[0].a;
   return c2;
  }
 }
 var cands=exactos.length?exactos:parecidos;
 if(!cands.length)return null;
 function mayorFv(l){return l.reduce(function(a,b){return Number(b.fv)>Number(a.fv)?b:a;});}
 /* ¿Todas las fichas son de la misma persona, escrita casi igual
    (ej. IGLESIA en la planilla e IGLESIAS en la hoja)? */
 function unaPersona(l,m){return l.every(function(c){return calza(norm(c.n+" "+c.a).split(" "),m);});}
 var mejor=mayorFv(cands);
 if(!exactos.length&&!unaPersona(cands,mejor)){
  /* Dos personas parecidas: si solo una está vigente, es ella. */
  var vig=cands.filter(vigente);
  if(!vig.length)return null;
  mejor=mayorFv(vig);
  if(!unaPersona(vig,mejor))return null;
 }
 var copia=Object.assign({},mejor);
 if(!exactos.length){copia.n=palabras[0];copia.a=palabras.slice(1).join(" ");}
 return copia;
}
window.fetch=function(input,options){
 var url=typeof input==="string"?input:(input&&input.url)||"";
 if(/^(?:\.\/)?socios\.json(?:[?#]|$)/.test(url)){
  return Promise.all([
   originalFetch(input,options).then(function(r){return r.json();}).catch(function(){return {socios:[]};}),
   leerHoja()
  ]).then(function(res){
   var j=res[0]||{},base=Array.isArray(j)?j:(j.socios||[]);
   var todos=ponerPrimero(juntar(base,res[1]));
   var out=Array.isArray(j)?todos:Object.assign({},j,{socios:todos});
   return new Response(JSON.stringify(out),{status:200,headers:{"Content-Type":"application/json"}});
  });
 }
 return originalFetch(input,options);
};
window.wgymLeerHojaSocios=leerHoja;
/* Consulta de un socio por nombre, para las páginas que antes usaban
   socios-en-vivo.js (app de socios, Glúteos, Hombre 5 Días): misma
   respuesta (la ficha del socio, o null si no está), pero leyendo la hoja
   de Google + socios.json, con las mismas reglas de nombre parecido. */
window.wgymVerificarSocio=function(nombre){
 return Promise.all([
  originalFetch("socios.json?v="+Date.now(),{cache:"no-store"}).then(function(r){return r.json();}).catch(function(){return {socios:[]};}),
  leerHoja()
 ]).then(function(res){
  var j=res[0]||{},base=Array.isArray(j)?j:(j.socios||[]);
  var todos=juntar(base,res[1]);
  if(!todos.length)throw Error("Sin lista de socios");
  return elegir(todos,nombre);
 });
};
leerHoja();
/* Si vuelve a la pestaña tras un rato, trae la hoja de nuevo (renovaciones). */
window.addEventListener("pageshow",function(e){if(e.persisted){hojaPromise=null;leerHoja();}});
})();
