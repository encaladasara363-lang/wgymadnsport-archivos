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
| `ingresoTarjeta&nombre&apellido&forzar=1` | tarjeta.html, **solo** abierta con el QR de la puerta (`?ingreso=puerta`) | Cada escaneo es una visita nueva: si quedó abierto un ingreso anterior sin salida, se cierra solo (origen "nueva visita") y se agrega el nuevo. Solo si vuelve a escanear antes de 30 minutos desde su último ingreso, no se duplica. Abierta por cualquier otro enlace, la tarjeta solo consulta (`miIngreso`). |
| `salidaSocio&nombre&apellido&codigo` | El socio, desde su tarjeta | Desde el 03-10-2026 basta con su nombre, igual que para entrar (muchos Android escanean en un navegador y abren la tarjeta en otro, y el código no estaba). Solo cierra los ingresos de esa persona; sin el código queda con origen "tarjeta sin codigo" y recepción puede deshacerlo. |
| `registrarIngreso` (POST) | Recepción: botón "Registrar ingreso" de "¿No alcanzó a escanear?" | Clave de administración. Misma regla de visita nueva (no duplica antes de 30 minutos). |
| `registrarSalida` (POST) | Recepción (control.html) | Clave de administración (`ADMIN_KEY`), la misma de guardar socios. |
| `quitarSalida` (POST) | Recepción ("Deshacer") | Clave de administración, más la fila y la hora de ingreso exactas. |

**Modo prueba:** las páginas `prueba-control.html`, `prueba-pantalla.html`
y `prueba-tarjeta.html` (generadas con `node scripts/generar-pruebas-ingresos.js`)
mandan `prueba=1` en todas las llamadas: todo se guarda en la hoja
**"Pruebas ingresos"** (se crea sola), nunca en la hoja real, así que no
aparecen en las pantallas reales ni alteran estadísticas. Al terminar las
pruebas se borran esas páginas y esa hoja.

Ninguna borra ni mueve filas de la hoja. La respuesta antigua (sin
`action`, los últimos 20) y la acción `checkin` siguen iguales.

## Actualización WGYMNUTRI de pago (10-10-2026)

`Ingresos.gs` trae dos acciones nuevas: `listarNutri` (la app WGYMNUTRI
pregunta quién la tiene activa) y `activarNutri` (el botón «Activar 1 mes
($5.000)» de la ficha del socio en el mesón, con la clave de
administración). Guardan todo en una hoja nueva, **«WGYMNUTRI»**, que se crea
sola la primera vez. No hay que tocar `Código.gs`.

1. Abre el proyecto del script (enlace de arriba) y entra al archivo
   **Ingresos**.
2. Selecciona todo (Ctrl + A), bórralo y pega **todo** el contenido nuevo de
   [`docs/apps-script/Ingresos.gs`](apps-script/Ingresos.gs). Guarda (💾).
3. **Implementar → Administrar implementaciones** → lápiz ✏️ → "Versión":
   **Nueva versión** → **Implementar** (no "Nueva implementación").

Comprobar: el link del script terminado en `/exec?action=listarNutri` debe
mostrar `{"ok":true,"nutri":true,...`. Mientras no se instale, nadie puede
usar WGYMNUTRI (todos ven la pantalla de pago) y la ficha del mesón dice
«falta instalar».

## Actualización productos escaneados de WGYMNUTRI (10-10-2026)

`Ingresos.gs` trae dos acciones nuevas más: `listarProductos` y
`guardarProducto`. Cuando alguien escanea un producto en WGYMNUTRI (o lo crea
con la etiqueta), queda guardado en una hoja nueva, **«Productos»**, que se
crea sola, y desde ahí lo ven todos los socios en la búsqueda. Solo guarda
datos de etiquetas (nombre, marca, calorías y macros por 100 g), nada
personal. Para corregir o borrar un producto, se edita o borra su fila en esa
hoja.

Se instala igual que la vez anterior: pegar **todo** el `Ingresos.gs` nuevo en
el archivo **Ingresos**, guardar y **Implementar → Administrar
implementaciones → lápiz ✏️ → Nueva versión → Implementar**.

Comprobar: el link del script terminado en `/exec?action=listarProductos`
debe mostrar `{"ok":true,"productos":[...]}`. Mientras no se instale, la app
funciona igual que antes (cada teléfono recuerda lo que escaneó él mismo).

## Actualización ranking del mes en la tarjeta (Versión 17, 11-10-2026)

`Ingresos.gs` trae dos acciones nuevas: `guardarReto` y `listarRetos`. En la
**tarjeta virtual** aparece «🏆 Ranking del mes»: el socio se une con un
**apodo** y el ranking muestra solo apodos y **días con ingreso al gimnasio en
el mes**. Los días los cuenta el script desde la hoja de ingresos (nadie puede
inventarlos). Se crea sola una hoja nueva, **«Retos»** (mes, código del
teléfono, apodo y nombre para contar sus días; la hoja es privada). Para sacar a
alguien del ranking, se borra su fila en esa hoja.

Se instala igual que las veces anteriores: pegar **todo** el `Ingresos.gs`
nuevo en el archivo **Ingresos**, guardar y **Implementar → Administrar
implementaciones → lápiz ✏️ → Nueva versión → Implementar**.

Comprobar: el link del script terminado en `/exec?action=listarRetos` debe
mostrar `{"ok":true,"retos":true,...`. Mientras no se instale, la tarjeta dice
«El ranking se activa cuando el gimnasio actualice su sistema».

### Versión 20 (11-10-2026): ranking con nombres en el mesón

Acción nueva `rankingAdmin` (POST con la clave de administración): el mesón
(`control.html`) muestra el ranking del mes con el apodo, el **nombre real** y
los días de cada socio, para saber a quién premiar. Se instala igual: pegar todo
`Ingresos.gs` en **INGRESOS.gs**, guardar, **Implementar → Administrar
implementaciones → lápiz ✏️ → Nueva versión → Implementar**.
