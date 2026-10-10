/* Service worker mínimo de WGYMNUTRI (10/2026), igual que sw-tarjeta.js.
   Solo existe para que Android ofrezca "Instalar". NO guarda caché: todo
   llega de internet, así los socios siempre ven la versión nueva. */
self.addEventListener("install", function(){ self.skipWaiting(); });
self.addEventListener("activate", function(e){ e.waitUntil(self.clients.claim()); });
self.addEventListener("fetch", function(){});
