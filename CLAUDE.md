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
5. **Actualizar también `LISTA_BASE` en `control.html`** (ver sección de
   abajo) para que el mesón y la pantalla de la puerta se enteren solos.
6. **Publicar el cambio directamente en `main`** (además de guardarlo en
   cualquier rama de trabajo) para que quede reflejado en el link en vivo
   de arriba — el usuario espera que sus socios tengan acceso inmediato a
   su QR de ingreso y a sus rutinas, no un cambio pendiente de fusionar.
7. Confirmarle al usuario qué socios se agregaron, renovaron o cambiaron.

### `control.html` y `pantalla.html` — cómo se enteran de los cambios

`pantalla.html` (la pantalla de acceso en la puerta) **no lee
`socios.json` directamente**: lee el `localStorage` (`wgym_control_v1`)
que llena `control.html` en ese mismo computador — la "lista del mesón".
Si esa lista local tiene aunque sea un socio guardado, `pantalla.html`
la usa SIEMPRE y nunca mira `socios.json` por su cuenta.

Por eso `control.html` trae embebida su propia copia de la planilla,
`const LISTA_BASE = [...]`, con un número de versión `LISTA_VERSION`
justo arriba. Cada vez que se abre `control.html` en un equipo, compara
esa versión con la última que vio (`versionVista`, guardada en ese mismo
`localStorage`): si `LISTA_BASE` es más nueva, fusiona sola los cambios
con la lista del mesón (agrega socios nuevos, deja la fecha más
adelantada de las dos) **sin borrar nada de lo que se cargó a mano en ese
equipo** — y avisa en pantalla cuántos socios agregó o actualizó.

**Por eso, cada vez que se edite `socios.json` (alta, renovación, cambio
de plan), hay que regenerar `LISTA_BASE` en `control.html` con los mismos
datos y subir `LISTA_VERSION`, y publicar ambos archivos juntos en
`main`.** Sin este paso, el mesón y la puerta se quedan con la foto vieja
y el socio nuevo aparece "Sin ficha de socio" o "No está en la lista de
socios" aunque `socios.json` esté perfecto.

Cómo regenerar `LISTA_BASE`:
- Recorrer `socios.json` en el mismo orden y armar cada línea como
  `{n:"...",a:"...",plan:"...",m:MONTO,v:"AAAA-MM-DD"}` (sin `rut`:
  `control.html` no maneja RUT). El campo `v` es la fecha ISO que sale de
  convertir el `fv` (serial tipo Excel) — no el serial mismo.
- Reemplazar todo el contenido entre `const LISTA_BASE = [` y `];`.
- Subir `LISTA_VERSION` a un número mayor (formato `AAAAMMDDNN`, ver el
  valor actual como ejemplo).
- Validar que el array quedó bien formado (por ejemplo cargándolo con
  Node: `eval()` del fragmento y contar cuántos socios trajo) antes de
  publicar — un JSON/JS mal cerrado rompe toda la página para todos los
  que abran `control.html`.

Con esto, la próxima vez que el dueño abra o refresque `control.html` en
el equipo de la recepción, se sincroniza solo — no hace falta pedirle que
cargue cada socio a mano, ni tocar `pantalla.html`.

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
9. **Límite que no tiene arreglo por código: ninguna página web puede
   sonar, vibrar ni avisar mientras el celular tiene OTRA APP nativa en
   primer plano** (por ejemplo TikTok, Instagram, WhatsApp). Es una regla
   de iOS/Android que corta la ejecución de cualquier pestaña de
   navegador en segundo plano — no es un bug de esta app ni algo que se
   arregle con más beeps, `Notification` API o trucos de audio. Si el
   usuario pide que la alarma de descanso "interrumpa" mientras ve un
   video en otra app, la respuesta correcta es explicarle este límite
   (no prometer un intento más de código) y sugerirle usar el
   temporizador/alarma NATIVO del celular (la app Reloj) para ese caso
   puntual, ya que esa sí tiene permiso del sistema para sonar por
   encima de cualquier app. El beep + vibración + aviso visual dentro de
   esta app siguen funcionando perfecto mientras la pestaña está abierta
   y visible — el límite es solo cuando el usuario se va a otra app.
