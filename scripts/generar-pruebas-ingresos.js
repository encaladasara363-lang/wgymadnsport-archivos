/* Genera prueba-control.html, prueba-pantalla.html y prueba-tarjeta.html:
   copias exactas de las páginas reales que mandan prueba=1 al Apps Script,
   así todo lo que se haga en ellas queda en la hoja "Pruebas ingresos" y
   nunca en la hoja real de ingresos. Se borran al terminar las pruebas.
   Uso: node scripts/generar-pruebas-ingresos.js */
const fs = require("fs"), path = require("path");
const raiz = path.join(__dirname, "..");
const banner =
  '<div style="position:sticky;top:0;z-index:9999;background:#D4AF37;color:#0A0A0B;' +
  'font:800 13px Arial,sans-serif;letter-spacing:.06em;text-align:center;padding:7px 10px">' +
  'MODO PRUEBA · se guarda en la hoja "Pruebas ingresos", no en los registros reales</div>';
for (const nombre of ["control", "pantalla", "tarjeta"]) {
  let s = fs.readFileSync(path.join(raiz, nombre + ".html"), "utf8");
  const head = s.match(/<head[^>]*>/i);
  const body = s.match(/<body[^>]*>/i);
  if (!head) throw new Error(nombre + ": no encontré <head>");
  s = s.replace(head[0], head[0] + '\n<script>window.WGYM_PRUEBA_INGRESOS = true;</script>');
  s = s.replace(/<title>/i, "<title>PRUEBA · ");
  if (body) s = s.replace(body[0], body[0] + "\n" + banner);
  else s = s.replace(/(<header|<div)/i, banner + "\n$1");
  s = s.replace(/href="(control|pantalla|tarjeta)\.html"/g, 'href="prueba-$1.html"');
  fs.writeFileSync(path.join(raiz, "prueba-" + nombre + ".html"), s);
  console.log("prueba-" + nombre + ".html");
}
