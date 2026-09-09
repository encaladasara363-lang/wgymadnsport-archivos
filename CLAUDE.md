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

### ⚠️ `pantalla.html` (control de acceso en la puerta) NO lee `socios.json`

`pantalla.html` — la pantalla que se usa en la recepción para dar el
acceso físico al gimnasio — lee exclusivamente el `localStorage`
(`wgym_control_v1`) que llena `control.html` en ese mismo computador.
**No consulta `socios.json` en ningún momento.**

Esto significa que actualizar `socios.json` por chat (agregar, renovar,
cambiar plan) deja al socio perfecto en la tarjeta virtual (`tarjeta.html`)
y en las rutinas, pero **la pantalla de la puerta lo va a seguir marcando
en rojo como "No está en la lista de socios" hasta que el dueño lo
escriba también, a mano, en `control.html` en el computador de la
recepción.** Confirmado con el dueño (2026-09): así se queda por ahora,
no hay que "arreglarlo" automáticamente ni asumir que ya sincroniza.

Por eso, cada vez que se agregue o renueve un socio por chat:
- Aclarar en la confirmación final que ese cambio cubre tarjeta/rutinas,
  pero que además hay que cargarlo en `control.html` en la recepción para
  que la pantalla de acceso lo reconozca.
- Si el usuario reporta que "la pantalla dice que no está en la lista"
  para alguien que ya está en `socios.json`, la causa casi siempre es esta
  desincronización — no un bug de datos. Verificar primero que el socio
  esté bien en `socios.json` (nombre/apellido exactos, sin duplicar) y
  luego recordarle que debe cargarlo también en `control.html` en el
  equipo de la puerta.
- Si en algún momento el usuario pide que esto se una en una sola fuente,
  la opción es modificar `pantalla.html` para que también consulte
  `socios.json` — pero es un cambio al sistema de control de acceso de la
  puerta, así que hay que pedir confirmación explícita antes de tocarlo.

## Rutinas de entrenamiento para clientes exclusivos (regla permanente)

Cuando el usuario pida una app de entrenamiento personalizada para un
cliente VIP/exclusivo (normalmente adjuntando el PDF de su plan de
alimentación WGYMADNSPORT), seguir siempre este proceso:

1. **Leer el PDF de la dieta** y usarlo como fuente de la rutina: nombre
   del cliente, el split semanal y las kcal por día YA vienen definidos
   ahí (día alto/medio/bajo, grupo muscular de cada día) — la rutina de
   6 días debe calzar con ese split y esas calorías, no inventar uno
   distinto. Si la dieta indica explícitamente algo (por ejemplo "nada de
   cardio extra"), respetarlo salvo que el usuario pida lo contrario.
2. **Diseñar los 6 días** con ejercicios reales, series/reps objetivo,
   descanso sugerido y una explicación técnica detallada en MAYÚSCULAS
   por ejercicio (clara, no un one-liner).
3. **Construir la app en HTML + JavaScript puro, sin frameworks ni CDNs
   externos** (nada de React, Babel ni Tailwind vía `<script src>`).
   Esto no es una preferencia de estilo: los socios abren estas apps
   desde WhatsApp en el celular, y ahí un archivo o página que dependa de
   cargar librerías externas para recién entonces ejecutar JSX/Babel
   falla con pantalla negra — ya pasó y cuesta mucho diagnosticar a
   distancia. Los únicos recursos externos permitidos son las hojas de
   Google Fonts (fallan de forma segura si no hay internet: quedan las
   fuentes de reemplazo, nunca pantalla en blanco).
4. **Mantener siempre el mismo diseño WGYM ADN SPORT**: fondo casi negro,
   acento rojo/rosado, dorado para peso/PR, tipografía Bebas Neue
   (títulos) + Inter (texto) + JetBrains Mono (números), logo placeholder
   circular con "W" y etiqueta "ADN". No introducir una identidad visual
   distinta de una rutina a otra.
5. **Funcionalidad mínima esperada**: cronómetro general de sesión
   (iniciar/pausar/reiniciar, persistente), sets editables por ejercicio
   (peso, reps, check de completado, agregar/quitar serie), temporizador
   de descanso por ejercicio con beep sintetizado por Web Audio API +
   `navigator.vibrate` + aviso visual en pantalla (el `AudioContext` hay
   que crearlo/reanudarlo DENTRO del gesto del usuario —el clic en
   "Descanso"—, nunca solo dentro del `setInterval`, o el navegador lo
   deja suspendido y no suena), explicación técnica editable (textarea
   que fuerza MAYÚSCULAS), botón "Exportar" que intente
   `window.claude.use('downloads')` primero y si no está disponible caiga
   a una descarga por Blob y, como último recurso, a un modal para copiar
   el texto a mano. Todo el progreso se guarda en `localStorage` con una
   clave única por cliente.
6. **Publicar como página del sitio, no como archivo suelto ni como link
   de Claude Artifacts.** Nombrar el archivo `entrenar-<nombre-o-apodo
   -del-cliente>.html` en la raíz del repo (mismo patrón que los
   `entrenar-*.html` existentes) y **publicar el cambio directamente en
   `main`** (además de la rama de trabajo), igual que con `socios.json`,
   para que quede vivo de inmediato en
   https://encaladasara363-lang.github.io/wgymadnsport-archivos/entrenar-<nombre>.html
   — esa URL abre en cualquier navegador sin pedir cuenta ni depender de
   cómo WhatsApp maneje archivos o de que el link de Claude esté
   compartido como público.
7. Si ya existe un `entrenar-<nombre>.html` con contenido distinto de una
   sesión anterior, avisar antes de pisarlo — puede haber un QR o link ya
   impreso apuntando ahí — salvo que el usuario ya haya dejado claro que
   siempre hay que reemplazarlo.
8. Confirmarle al usuario la URL final en vivo.
