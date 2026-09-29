/* La rutina consulta el mismo registro en vivo que Caja y la tarjeta QR. */
(function(){
"use strict";
var originalFetch=window.fetch.bind(window);
var base="https://script.google.com/macros/s/AKfycbzDpqUW70UbZTQtH8X20EDdAGdQQbxBoKebYg2eDwX42A3yCXEpKacpnjtp8RjkBcNq/exec";
function listaViva(){
 return new Promise(function(resolve){
  var cb="wgymRutinas_"+Date.now()+"_"+Math.floor(Math.random()*100000),script=document.createElement("script"),hecho=false;
  function terminar(data){
   if(hecho)return;hecho=true;clearTimeout(reloj);delete window[cb];script.remove();
   resolve(data&&Array.isArray(data.socios)&&data.socios.length?data:null);
  }
  var reloj=setTimeout(function(){terminar(null);},8000);
  window[cb]=terminar;
  script.onerror=function(){terminar(null);};
  script.src=base+"?action=listarSocios&callback="+cb+"&_="+Date.now();
  document.head.appendChild(script);
 });
}
window.fetch=function(input,options){
 var url=typeof input==="string"?input:(input&&input.url)||"";
 if(/^(?:\.\/)?socios\.json(?:[?#]|$)/.test(url)){
  return listaViva().then(function(data){
   if(data)return new Response(JSON.stringify(data),{status:200,headers:{"Content-Type":"application/json"}});
   return originalFetch(input,options);
  });
 }
 return originalFetch(input,options);
};
})();

