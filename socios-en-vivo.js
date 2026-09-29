/* Las rutinas consultan a un socio por nombre sin descargar la nómina completa. */
(function(){
"use strict";
var endpoint="https://wgymadnsport-mediciones.encaladasara363.chatgpt.site/api/verificar-socio";
var originalFetch=window.fetch.bind(window);
function verificar(nombre){
 var controller=new AbortController(),timer=setTimeout(function(){controller.abort();},3300);
 return originalFetch(endpoint,{method:"POST",headers:{"Content-Type":"application/json"},
  body:JSON.stringify({nombre:nombre}),signal:controller.signal,cache:"no-store"})
 .then(function(r){if(!r.ok)throw Error("Registro no disponible");return r.json();})
 .then(function(data){if(!data.ok)throw Error("Registro no disponible");return data.socio||null;})
 .finally(function(){clearTimeout(timer);});
}
window.wgymVerificarSocio=verificar;
window.fetch=function(input,options){
 var url=typeof input==="string"?input:(input&&input.url)||"";
 if(/^(?:\.\/)?socios\.json(?:[?#]|$)/.test(url)){
  var field=document.getElementById("member");
  var name=field&&field.value.trim();
  if(name){
   return verificar(name).then(function(socio){
    return new Response(JSON.stringify({socios:socio?[socio]:[]}),
      {status:200,headers:{"Content-Type":"application/json"}});
   });
  }
 }
 return originalFetch(input,options);
};
})();
