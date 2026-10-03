/* Service worker mínimo de la tarjeta virtual (10/2026).
   Solo existe para que Android ofrezca "Instalar" con el botón
   "Poner en mi pantalla de inicio" de tarjeta.html. No guarda nada en
   caché ni cambia ninguna respuesta: todo sigue llegando de internet,
   así que los cambios del sitio se ven igual que siempre. */
self.addEventListener("install", function(){ self.skipWaiting(); });
self.addEventListener("activate", function(e){ e.waitUntil(self.clients.claim()); });
self.addEventListener("fetch", function(){});
