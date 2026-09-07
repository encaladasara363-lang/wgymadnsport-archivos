# WGYMADNSPORT — Archivos del gimnasio

## Planilla de socios (regla permanente)

`socios.json` (en la raíz del repo) es la **única planilla de socios** que
el dueño del gimnasio usa. La leen `tarjeta.html` (tarjeta virtual con QR
de ingreso) y todas las apps `entrenar-*.html` (rutinas de entrenamiento).

Sitio en vivo: https://encaladasara363-lang.github.io/wgymadnsport-archivos/

Siempre que el usuario pida **renovar, actualizar o cambiar la fecha de
vencimiento** de uno o varios socios (por ejemplo, pegando el JSON que
exporta el botón "Pasar la lista" de `control.html`):

1. Editar `socios.json` fusionando los datos nuevos (nombre, apellido,
   plan, monto, fecha de vencimiento `fv`) con los existentes.
2. **Conservar el RUT ya registrado** de cada socio si el dato nuevo no
   trae RUT (el export de `control.html` siempre manda `"rut": "Sin Rut"`
   porque esa herramienta no guarda RUT — nunca hay que borrar un RUT real
   ya cargado en `socios.json`).
3. Mantener el archivo ordenado alfabéticamente por apellido y sin
   duplicados.
4. Actualizar el campo `"actualizado"` con la fecha del día.
5. **Publicar el cambio directamente en `main`** (además de guardarlo en
   cualquier rama de trabajo) para que quede reflejado en el link en vivo
   de arriba — el usuario espera que sus socios tengan acceso inmediato a
   su QR de ingreso y a sus rutinas, no un cambio pendiente de fusionar.
6. Confirmarle al usuario qué socios se agregaron, renovaron o cambiaron.

`control.html` es solo la herramienta de administración local (guarda su
lista en el `localStorage` del dispositivo); no lee `socios.json` y no
hace falta tocarla para estas actualizaciones.
