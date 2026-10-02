/* Revisa que el archivo de una rutina (rutinas/*.json) esté completo antes de
   usarlo. Lo usan las páginas de rutina (para no mostrar nunca una rutina
   rota) y la revisión automática de GitHub (scripts/validar-rutinas.js).
   Devuelve una lista de problemas en palabras simples; vacía = todo bien. */
(function(raiz){
"use strict";
function texto(v){return typeof v==="string"&&v.trim()!=="";}
function validarRutina(r){
 var e=[];
 if(!r||typeof r!=="object"||Array.isArray(r))return["El archivo no tiene el formato de una rutina."];
 if(!texto(r.id))e.push("Falta el campo \"id\".");
 if(!texto(r.nombre))e.push("Falta el campo \"nombre\".");
 if(!texto(r.claveProgreso))e.push("Falta el campo \"claveProgreso\" (no cambiarlo: ahí está guardado el progreso de los socios).");
 if(!Array.isArray(r.dias)||!r.dias.length){e.push("La rutina no tiene días (\"dias\").");return e;}
 if(r.dias.length>7)e.push("La rutina tiene más de 7 días.");
 r.dias.forEach(function(d,di){
  var dn="Día "+(di+1)+(d&&texto(d.weekday)?" ("+d.weekday+")":"");
  if(!d||typeof d!=="object"){e.push(dn+": no tiene el formato de un día.");return;}
  ["weekday","title","focus","warmup","cooldown"].forEach(function(k){if(!texto(d[k]))e.push(dn+": falta \""+k+"\".");});
  if(!Array.isArray(d.exercises)||!d.exercises.length){e.push(dn+": no tiene ejercicios.");return;}
  d.exercises.forEach(function(x,ei){
   var xn=dn+", ejercicio "+(ei+1)+(x&&texto(x.name)?" ("+x.name+")":"");
   if(!x||typeof x!=="object"){e.push(xn+": no tiene el formato de un ejercicio.");return;}
   ["name","sets","rest","tip","equip","muscle"].forEach(function(k){if(!texto(x[k]))e.push(xn+": falta \""+k+"\".");});
   var n=parseInt(x.sets,10);
   if(texto(x.sets)&&!(n>=1&&n<=10))e.push(xn+": \"sets\" debe empezar con la cantidad de series, ej. \"3 × 10-12\".");
   if(texto(x.rest)&&!(parseInt(x.rest,10)>0))e.push(xn+": \"rest\" debe empezar con los segundos, ej. \"60 seg\".");
   if(!Array.isArray(x.img)||x.img.length!==2||!x.img.every(texto))e.push(xn+": \"img\" debe traer 2 fotos (inicio y final).");
   if(x.formato!=null&&["ancho","alto","plancha"].indexOf(x.formato)<0)e.push(xn+": \"formato\" solo puede ser ancho, alto o plancha.");
  });
 });
 return e;
}
if(typeof module!=="undefined"&&module.exports)module.exports=validarRutina;
else raiz.validarRutina=validarRutina;
})(this);
