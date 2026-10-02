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
window.fetch=function(input,options){
 var url=typeof input==="string"?input:(input&&input.url)||"";
 if(/^(?:\.\/)?socios\.json(?:[?#]|$)/.test(url)){
  return Promise.all([
   originalFetch(input,options).then(function(r){return r.json();}).catch(function(){return {socios:[]};}),
   leerHoja()
  ]).then(function(res){
   var j=res[0]||{},base=Array.isArray(j)?j:(j.socios||[]);
   var out=Array.isArray(j)?juntar(base,res[1]):Object.assign({},j,{socios:juntar(base,res[1])});
   return new Response(JSON.stringify(out),{status:200,headers:{"Content-Type":"application/json"}});
  });
 }
 return originalFetch(input,options);
};
window.wgymLeerHojaSocios=leerHoja;
leerHoja();
/* Si vuelve a la pestaña tras un rato, trae la hoja de nuevo (renovaciones). */
window.addEventListener("pageshow",function(e){if(e.persisted){hojaPromise=null;leerHoja();}});
})();
