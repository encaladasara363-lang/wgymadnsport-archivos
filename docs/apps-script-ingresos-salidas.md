# Ingresos completos y MARCAR SALIDA: cambio para el Apps Script del check-in

Este cambio es para el proyecto de Apps Script que recibe los ingresos del
QR (el que guarda en la hoja **"WGYMADNSPORT - Ingresos por Tarjeta QR"**).
Las páginas del sitio (`control.html`, `pantalla.html` y `tarjeta.html`)
**ya están preparadas**: mientras no hagas este cambio, siguen funcionando
como hoy.

## Por qué desaparecían los primeros ingresos

El script, al responder la lista de ingresos, entrega **solo los últimos
20** (`Math.min(20, …)` dentro de `doGet`). Cuando entra la persona número
21 del día, la primera deja de aparecer en pantalla. **Los ingresos nunca
se borraron**: todos siguen guardados en la hoja (al 03-10-2026 había
2.565 ingresos registrados desde el 20-08-2026).

Con este cambio, las pantallas piden **todos los ingresos del día** (fecha
de Chile), y la salida de cada socio queda guardada en la misma hoja
(columnas E "Salida", F "Origen salida" y G "Código tarjeta", que hoy están vacías).

## Pasos (unos 10 minutos, desde el computador)

El proyecto correcto es el que tiene `listarSocios` y empieza con
`var SHEET_ID = "1CST4GI31…"`:
<https://script.google.com/d/1qDGKxf4tAqw4WkMnAdE2d48MKtMiL7MYe-fMq04MBoMzEsSe25_nKoAH/edit>

1. **Archivo nuevo `Ingresos`:** a la izquierda, junto a "Archivos", toca
   **＋ → Secuencia de comandos**, ponle de nombre `Ingresos`, borra el
   `function myFunction() {}` que aparece y pega **todo** el contenido de
   [`docs/apps-script/Ingresos.gs`](apps-script/Ingresos.gs). Guarda (💾).
2. **Línea 1 en `Código.gs` (dentro de `doGet`):** busca (Ctrl + F)
   `/* guardarSocio y borrarSocio NO se atienden` y, **justo en la línea de
   arriba**, pega:

   ```js
   var respIngresos_ = accionIngresos_(e); if (respIngresos_) return respIngresos_;
   ```
3. **Línea 2 en `Código.gs` (dentro de `doPost`):** busca
   `if (p.action === "guardarSocio") {` y, **justo en la línea de arriba**,
   pega:

   ```js
   var respIngresosPost_ = accionIngresosPost_(e); if (respIngresosPost_) return respIngresosPost_;
   ```

   No borres ni cambies nada más. Guarda (💾).
4. **Publicar sin cambiar el link:** **Implementar → Administrar
   implementaciones** → lápiz ✏️ de la implementación activa → "Versión":
   **Nueva versión** → **Implementar**. **No uses "Nueva implementación"**
   (crea otro link y las páginas dejarían de recibir los ingresos).
5. Si Google pide permisos, acéptalos.

## Cómo comprobar que quedó bien

Abre en el navegador el link del script terminado en
`/exec?action=listarIngresos`. Debe mostrar un texto que empieza con
`{"ok":true,"ingresos":true,"dia":"…` con los ingresos de hoy. Si muestra
`{"rows":[…` sin `"ingresos":true`, la versión nueva todavía no está
publicada (repite el paso 4).

## Quién puede hacer qué

| Acción | Quién | Cómo se protege |
| --- | --- | --- |
| `listarIngresos&dia=AAAA-MM-DD` | control.html, pantalla.html | Pública, igual que la lista de ingresos de hoy (nombres y horas, nunca el código de la tarjeta). |
| `miIngreso&nombre&apellido` | tarjeta.html | Solo el estado de esa persona hoy. |
| `ingresoTarjeta&nombre&apellido[&forzar=1]` | tarjeta.html | Registra el ingreso **solo si esa persona no tiene ingreso hoy**. Abrir la tarjeta otra vez no crea filas. `forzar=1` (botón "Volver a ingresar hoy") solo funciona si ya tiene la salida marcada. |
| `salidaSocio&nombre&apellido&codigo` | El socio, desde su tarjeta | Exige el código privado que recibió **su** teléfono al registrar el ingreso (columna G). Sin ese código: "no autorizado". |
| `registrarSalida` (POST) | Recepción (control.html) | Clave de administración (`ADMIN_KEY`), la misma de guardar socios. |
| `quitarSalida` (POST) | Recepción ("Deshacer") | Clave de administración, más la fila y la hora de ingreso exactas. |

Ninguna borra ni mueve filas de la hoja. La respuesta antigua (sin
`action`, los últimos 20) y la acción `checkin` siguen iguales.
