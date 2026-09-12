# WGYMADNSPORT — Archivos del gimnasio

## Planilla de socios (regla permanente)

`socios.json` (en la raíz del repo) es la **única planilla de socios** que
el dueño del gimnasio usa. La leen `tarjeta.html` (tarjeta virtual con QR
de ingreso) y todas las apps `entrenar-*.html` (rutinas de entrenamiento).

Sitio en vivo: https://encaladasara363-lang.github.io/wgymadnsport-archivos/

Siempre que el usuario pida **renovar, actualizar o cambiar la fecha de
vencimiento** de uno o varios socios (por ejemplo, pegando el JSON que
exporta el botón "Pasar la lista" de `control.html`, o el que copia el
botón "📋 Copiar" de la ficha de un solo socio — ver más abajo):

1. Editar `socios.json` fusionando los datos nuevos (nombre, apellido,
   plan, monto, fecha de vencimiento `fv`) con los existentes.
2. **Conservar el RUT ya registrado** de cada socio si el dato nuevo no
   trae RUT (el export de `control.html` siempre manda `"rut": "Sin Rut"`
   porque esa herramienta no guarda RUT — nunca hay que borrar un RUT real
   ya cargado en `socios.json`).
3. Mantener el archivo ordenado alfabéticamente por apellido y sin
   duplicados.
4. Actualizar el campo `"actualizado"` con la fecha del día.
5. **Actualizar también `LISTA_BASE` en `control.html` Y `SOCIOS` en
   `pantalla.html`** (ver sección de abajo) — el usuario trabaja con LOS
   DOS aparatos (la compu de recepción con `control.html` y la tablet de
   la puerta con `pantalla.html`), así que TODO cambio de socios.json va
   siempre en los tres archivos juntos, nunca en uno solo.
6. **Publicar el cambio directamente en `main`** (además de guardarlo en
   cualquier rama de trabajo) para que quede reflejado en el link en vivo
   de arriba — el usuario espera que sus socios tengan acceso inmediato a
   su QR de ingreso y a sus rutinas, no un cambio pendiente de fusionar.
7. Confirmarle al usuario qué socios se agregaron, renovaron o cambiaron.

### `control.html` y `pantalla.html` — cómo se enteran de los cambios

La compu de recepción (`control.html`) y la tablet de la puerta
(`pantalla.html`) son DOS APARATOS FÍSICOS DISTINTOS, cada uno con su
propio navegador y su propio `localStorage` — nunca comparten
almacenamiento entre sí aunque abran la misma página. Por eso ningún
mecanismo del lado del cliente puede "avisarle" a uno lo que pasó en el
otro: la única forma de que los dos aparatos vean lo mismo es que cada
uno traiga su propia copia embebida y actualizada de la planilla, para
que se sincronice sola contra lo que está publicado en el sitio.

- `control.html` trae `const LISTA_BASE = [...]` + `const LISTA_VERSION`.
  Al abrirlo, compara `LISTA_VERSION` con la última que vio
  (`versionVista`, guardada en el `localStorage` de ESE equipo): si es
  más nueva, fusiona sola los cambios con la lista del mesón de esa
  compu (agrega socios nuevos, deja la fecha más adelantada de las dos)
  **sin borrar nada de lo que se cargó a mano ahí** — y avisa en pantalla
  cuántos socios agregó o actualizó.
- `pantalla.html` trae, por separado, `const SOCIOS = [...]` + `const
  SOCIOS_VERSION`, con el mismo mecanismo de fusión — independiente del
  de `control.html`, porque corre en otro aparato con otro
  `localStorage`.

**Por eso, cada vez que se edite `socios.json` (alta, renovación, cambio
de plan o de fecha), hay que regenerar LAS DOS copias — `LISTA_BASE` en
`control.html` y `SOCIOS` en `pantalla.html` — con los mismos datos,
subir `LISTA_VERSION` y `SOCIOS_VERSION`, y publicar los tres archivos
juntos en `main`.** Regenerar solo una de las dos deja al otro aparato
con la foto vieja: el socio nuevo o renovado aparece "Sin ficha de
socio" o "No está en la lista de socios" en ESE aparato, aunque
`socios.json` y el otro archivo estén perfectos.

Cómo regenerar cada copia:
- `LISTA_BASE` (control.html): recorrer `socios.json` en el mismo orden
  y armar cada línea como `{n:"...",a:"...",plan:"...",m:MONTO,v:"AAAA-MM-DD"}`
  (sin `rut`: `control.html` no maneja RUT). El campo `v` es la fecha ISO
  que sale de convertir el `fv` (serial tipo Excel) — no el serial mismo.
  Reemplazar todo el contenido entre `const LISTA_BASE = [` y `];`, y
  subir `LISTA_VERSION` a un número mayor (formato `AAAAMMDDNN`, ver el
  valor actual como ejemplo).
- `SOCIOS` (pantalla.html): mismo recorrido, pero cada línea como
  `{n:"...",a:"...",plan:"...",fv:SERIAL}` (con el `fv` serial tal cual,
  no la fecha ISO — `pantalla.html` convierte el serial internamente).
  Reemplazar el contenido entre `const SOCIOS = [` y `];`, y subir
  `SOCIOS_VERSION` al mismo número que `LISTA_VERSION` para no
  confundirse de cuál va con cuál.
- Validar que los dos arrays quedaron bien formados (por ejemplo
  cargándolos con Node: `eval()` del fragmento y contar cuántos socios
  trajo cada uno, comparando contra el total de `socios.json`) antes de
  publicar — un JSON/JS mal cerrado rompe toda la página para todos los
  que abran ese archivo.

Con esto, la próxima vez que el dueño abra o refresque `control.html` en
la compu Y `pantalla.html` en la tablet, cada uno se sincroniza solo con
lo publicado — no hace falta pedirle que cargue cada socio a mano en
ninguno de los dos aparatos.

Si el usuario manda el JSON que exporta el botón "📋 Copiar lista" de
`control.html` (la lista en vivo de la compu, con las fechas reales que
haya tocado directo ahí), tratarlo como la fuente de verdad para esa
fusión: comparar contra `socios.json` por nombre+apellido, aplicar a
`socios.json` cualquier `fv`/`plan`/`monto` que haya cambiado, y avisar
si aparece algún socio repetido (mismo nombre) en el export — eso es un
doble registro hecho sin querer en el mesón, no un socio nuevo: no
agregarlo solo, preguntar cuál de las dos fichas hay que borrar (esa
duplicación vive únicamente en el `localStorage` de esa compu, así que
el usuario tiene que borrar la fila de más él mismo con el ícono de
basurero de esa fila en `control.html` — no es algo que se arregle
editando los archivos).

### Renovar UN solo socio: el botón "📋 Copiar" de la ficha (regla permanente)

`control.html` tiene, dentro del cuadro "Editar ficha" de cada socio
(el que se abre con "Renovar / editar ficha"), un botón **"📋 Copiar"**
que copia SOLO esa ficha, ya en el formato exacto de `socios.json`:
```json
{ "n": "...", "a": "...", "rut": "...", "plan": "...", "monto": ..., "fv": ... }
```
Cuando el usuario pegue uno de estos objetos sueltos (no una lista con
`"socios": [...]`, sino un solo objeto `{n, a, rut, plan, monto, fv}`),
es exactamente lo mismo que pedir renovar/actualizar a esa persona: no
hace falta preguntarle la fecha ni nada más, el objeto ya trae todo
listo. Seguir el mismo proceso de siempre —
1. Buscar a ese socio en `socios.json` por nombre + apellido y
   actualizar `plan`/`monto`/`fv` con lo que llegó (conservando el RUT
   real ya cargado si el que llega es genérico o "Sin Rut").
2. Regenerar `LISTA_BASE` (control.html) y `SOCIOS` (pantalla.html),
   subir versión, validar y publicar en `main`, igual que con
   cualquier otro cambio de `socios.json`.
3. Confirmarle a la usuaria el cambio (nombre, fecha nueva).

Esta es la forma preferida de avisar una renovación de UNA persona —
más simple que pegar la lista completa de "Pasar la lista" para un
solo cambio.

### Borrar solo de la planilla a quien lleve 3 meses o más vencido (regla permanente)

Cada vez que se edite `socios.json` por cualquier motivo (renovación,
socio nuevo, corrección), aprovechar esa misma pasada para revisar la
fecha de vencimiento (`fv`) de TODOS los socios: a cualquiera cuya
fecha ya haya pasado hace **3 meses o más** contados desde hoy, sacarlo
de `socios.json` directamente, sin preguntar antes.

- El corte es por meses calendario, no por 90 días fijos: si hoy es
  11 de septiembre, el corte es el 11 de junio — vencido antes de esa
  fecha se borra, vencido después se queda (aunque ya esté vencido).
- Es SOLO borrar, no una alerta ni un archivo aparte: la persona sale
  de `socios.json`, de `LISTA_BASE` y de `SOCIOS` en la misma tanda,
  como cualquier otro cambio de la planilla.
- Siempre avisar en la confirmación quién se borró por esta regla (
  nombre, apellido y hace cuánto estaba vencido) — nunca borrar en
  silencio, para que la usuaria pueda decir "no, a ese no, todavía me
  va a pagar" si corresponde.
- Si nadie cumple los 3 meses, no hace falta decir nada al respecto.

### Avisos por Gmail sobre vencidos (regla permanente)

Cuando el aviso al dueño del gimnasio sea por Gmail (correo) sobre
socios vencidos, el correo lleva **solo** a los que vencieron **en la
última semana** (los 7 días corridos hasta hoy) — nadie vencido de
antes, nadie por vencer todavía. Se listan **ordenados alfabéticamente
por apellido**, sin agregar otros datos ni socios que no cumplan ese
corte.

### El contador "día X de Y" es un dato aparte — también hay que sincronizarlo

`fv`/`plan`/`monto` no son los únicos datos que viven en dos aparatos:
el contador de días (Turno, 3 Veces por Semana) se arma con `asistencia`
(qué días marcó cada socio) y `ciclos` (desde cuándo le corre el mes),
que se guardan solo en el `localStorage` de cada equipo — **nunca se
sincronizan solos entre la compu y la tablet**, así que pueden mostrar
números distintos aunque las fechas ya estén iguales en los dos.

El export de "📋 Copiar lista" de `control.html` ya incluye `asistencia`
y `ciclos` además de `socios`. Cuando el usuario mande ese JSON (o pida
arreglar un contador que no coincide entre los dos aparatos):
- Tomar `asistencia` y `ciclos` del JSON tal cual y regenerar
  `ASISTENCIA_BASE`/`CICLOS_BASE` en `control.html` y `pantalla.html`
  (mismo bloque, mismos nombres de variable) con esos objetos completos.
- Subir `ASISTENCIA_VERSION` a un número mayor.
- Es un agregado puro: `ASISTENCIA_BASE`/`CICLOS_BASE` solo rellenan lo
  que a cada aparato le falte, nunca pisan ni borran un día o un ciclo
  que ese equipo ya tenía anotado — así nunca hace bajar un contador que
  ya iba bien en alguno de los dos.
- Publicar junto con cualquier otro cambio de `socios.json`/`LISTA_BASE`/
  `SOCIOS` de esa misma tanda.

Si el usuario reclama que los contadores no coinciden y no mandó ese
export todavía, pedírselo (apretar de nuevo "📋 Copiar lista" y pegar el
resultado) — sin él no hay forma de saber los días reales que ya lleva
marcados cada socio en el equipo que el usuario toma como el bueno.

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
10. **Nunca escribir datos de salud reales (peso, grasa corporal, cintura,
    cadera, o cualquier otra medida corporal) directo en el código del
    archivo**, aunque vengan del PDF de la dieta y el pedido sea justo
    "ponle todos sus datos". Este repositorio es público: ya pasó que
    esos números quedaron expuestos ahí por escribirlos fijos en el
    HTML. En vez de eso, esa parte de la "ficha" va como casilleros
    `<input>` vacíos (`placeholder="—"`, clase `finput`/`finput-meta`)
    que la clienta llena ella misma la primera vez desde su teléfono; el
    valor se guarda con `localStorage` (clave propia, ej.
    `wgym_ficha_<nombre>_v1`), nunca en el archivo que se sube al repo.
    El resto de la rutina (ejercicios, series, tips, fechas del corte)
    no es dato de salud y sí puede ir fijo en el código, igual que
    siempre.
11. **Pedir `navigator.storage.persist()`** al arrancar la app (dentro de
    un `try/catch`, sin bloquear nada si falla) para bajar el riesgo de
    que el navegador borre solo el progreso guardado por falta de uso o
    espacio. No es garantía absoluta — si la usuaria borra a mano los
    datos del sitio, eso sí se pierde— pero ayuda contra la limpieza
    automática del celular.
12. El beep de fin de descanso tiene que sonar como una alarma de
    verdad, no un timbrecito: onda `square` (no `sine`, que suena
    débil), volumen cerca del máximo (`gain` ~0.9), varias repeticiones
    alternando dos tonos agudos, más una vibración larga con
    `navigator.vibrate`. Ver `pitar()` en `entrenar-sara.html` como
    referencia ya probada.
