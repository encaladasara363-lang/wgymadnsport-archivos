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
(columnas E "Salida" y F "Origen salida", que hoy están vacías).

## Pasos (unos 5 minutos, desde el computador)

1. Abre la hoja **"WGYMADNSPORT - Ingresos por Tarjeta QR"** y entra a
   **Extensiones → Apps Script**. Si no aparece ahí, abre
   <https://script.google.com> y entra al proyecto modificado el 28-09-2026
   (se llama "Proyecto sin título" y su archivo `Código.gs` empieza con
   `var SHEET_ID = "1CST4GI31…"`).
2. **Archivo nuevo:** a la izquierda, junto a "Archivos", toca **＋ →
   Secuencia de comandos**, ponle de nombre `Ingresos` y pega **todo** el
   contenido de
   [`docs/apps-script/Ingresos.gs`](apps-script/Ingresos.gs)
   (reemplaza el `function myFunction() {}` que aparece). Guarda (💾).
3. **Una línea en `Código.gs`:** abre `Código.gs`, busca (Ctrl + F) este
   texto:

   ```
   /* guardarSocio y borrarSocio NO se atienden
   ```

   y, **justo en la línea de arriba** de ese comentario, pega:

   ```js
   var respIngresos_ = accionIngresos_(e); if (respIngresos_) return respIngresos_;
   ```

   No borres ni cambies nada más. Guarda (💾).
4. **Publicar la versión nueva sin cambiar el link:** arriba a la derecha,
   **Implementar → Administrar implementaciones** → toca el lápiz ✏️ de la
   implementación activa → en "Versión" elige **Nueva versión** →
   **Implementar**. **No uses "Nueva implementación"**: eso crea otro link
   y las páginas dejarían de recibir los ingresos.
5. Si Google pide permisos, acéptalos (son los mismos de siempre: tu hoja).

## Cómo comprobar que quedó bien

- Abre `control.html`: en **"Ingresos de hoy"** ya no debe aparecer el
  aviso amarillo "Falta actualizar el Apps Script", y los botones
  **MARCAR SALIDA** quedan activos.
- Marca la salida de alguien de prueba (por ejemplo tú misma): debe pasar
  a "SALIDA REGISTRADA" y seguir en el "Historial del día". Si fue un
  error, toca **Deshacer**.
- En la hoja, esa fila tendrá la hora de salida en la columna E y
  "control" o "tarjeta" en la columna F.

## Qué hace cada acción nueva (para quien revise el código)

| Acción | Quién la usa | Qué hace |
| --- | --- | --- |
| `listarIngresos&dia=AAAA-MM-DD` | control.html, pantalla.html | Todos los ingresos de ese día (hora de Chile), con su salida. Sin `dia`, el de hoy. |
| `registrarSalida&nombre&apellido[&dia][&origen]` | MARCAR SALIDA (control y tarjeta) | Anota la hora de salida en **todos** los ingresos abiertos de esa persona ese día. |
| `quitarSalida&fila&ts` | "Deshacer" en control.html | Borra la salida de esa fila (solo si la hora de ingreso coincide exacta). |
| `miIngreso&nombre&apellido` | tarjeta.html | Solo el estado de esa persona hoy: si está dentro, desde qué hora o a qué hora salió. |

Ninguna borra ni mueve filas de la hoja. La respuesta antigua (sin
`action`, los últimos 20) se mantiene igual, por si algo más la usa.
