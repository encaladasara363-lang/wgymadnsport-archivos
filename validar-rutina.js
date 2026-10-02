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
 var visual=r.visual==null?"pares":r.visual;
 if(["pares","imagen","video"].indexOf(visual)<0)e.push("\"visual\" solo puede ser pares, imagen o video.");
 if(r.cardio!=null&&["elegir","texto"].indexOf(r.cardio)<0)e.push("\"cardio\" solo puede ser elegir o texto.");
 if(!Array.isArray(r.dias)||!r.dias.length){e.push("La rutina no tiene días (\"dias\").");return e;}
 if(r.diasSemana!=null&&(!Array.isArray(r.diasSemana)||r.diasSemana.length!==r.dias.length||!r.diasSemana.every(function(n){return n>=0&&n<=6;})))e.push("\"diasSemana\" debe traer un número (0 = lunes … 6 = domingo) por cada día.");
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
   var n=x.series!=null?Number(x.series):parseInt(x.sets,10);
   if(texto(x.sets)&&!(n>=1&&n<=10))e.push(xn+(x.series!=null?": \"series\" debe ser un número de 1 a 10.":": \"sets\" debe empezar con la cantidad de series, ej. \"3 × 10-12\" (o agregar \"series\")."));
   if(texto(x.rest)&&!(parseInt(x.rest,10)>0)&&x.rest.trim()!=="—")e.push(xn+": \"rest\" debe empezar con los segundos, ej. \"60 seg\" (o \"—\" si no tiene descanso).");
   if(visual==="video"){if(!texto(x.video))e.push(xn+": falta \"video\".");}
   else if(visual==="imagen"){if(!Array.isArray(x.img)||x.img.length!==1||!texto(x.img[0]))e.push(xn+": \"img\" debe traer 1 foto.");}
   else if(!Array.isArray(x.img)||x.img.length!==2||!x.img.every(texto))e.push(xn+": \"img\" debe traer 2 fotos (inicio y final).");
   if(x.formato!=null&&["ancho","alto","plancha"].indexOf(x.formato)<0)e.push(xn+": \"formato\" solo puede ser ancho, alto o plancha.");
  });
 });
 return e;
}
if(typeof module!=="undefined"&&module.exports)module.exports=validarRutina;
else raiz.validarRutina=validarRutina;
})(this);
