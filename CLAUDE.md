# WGYMADNSPORT — Archivos del gimnasio

## Reglas generales del dueño (regla permanente)

- **Identidad de marca en todo material de difusión.** Toda publicidad,
  flyer, tarjeta, estrategia de marketing y organización de eventos que
  se cree para el gimnasio debe estar totalmente alineada con la marca y
  el estilo visual de WGYMADNSPORT (ver la sección "Rutinas de
  entrenamiento" más abajo para la paleta e identidad de referencia, y
  las skills `wgymadnsport-plantillas` y `wgymadnsport-marketing` para
  piezas imprimibles y contenido de redes). No usar una identidad visual
  distinta a la ya aprobada.
- **Formatear transcripciones y textos extensos.** Cuando el usuario
  pegue una transcripción o un texto largo, convertirlo automáticamente
  a Markdown estructurado (títulos, listas, párrafos cortos) antes de
  trabajar con él, para ahorrar tokens de contexto.

## Publicación en redes sociales vía Metricool (regla permanente)

La cuenta de Metricool del dueño (marca "Tienda WgymadnSport", brandId
`6700545`, zona horaria `America/Santiago`) tiene conectadas las tres
redes: **Instagram** (`wadnsport.tocopilla`, vía la página de Facebook
"Wadnsport Tocopilla Gimnasio"), **Facebook** (esa misma página) y
**TikTok** (`wadnsport.tocopil...`).

Siempre que se programe o publique una pieza de contenido (post, flyer,
aviso, video) para redes sociales del gimnasio, **publicarla en las
tres redes a la vez por defecto** (Instagram, Facebook y TikTok) usando
las herramientas de Metricool — no preguntar cada vez ni omitir TikTok
salvo que el usuario pida explícitamente lo contrario para esa pieza.
Adaptar el copy al tono de cada plataforma cuando haga falta, pero el
alcance (las tres redes) es siempre el mismo.

Antes de publicar contenido nuevo (no un ajuste de texto/hora a algo ya
creado), mostrarle al usuario una vista previa o el link del planificador
de Metricool y esperar su confirmación antes de dejarlo publicado — igual
que con cualquier acción visible públicamente.

### Números de contacto en toda publicación (regla permanente)

El gimnasio usa **dos** números de contacto y ambos deben aparecer juntos
en todo post, flyer, cartel o pieza nueva que se cree para redes sociales
o para imprimir — nunca solo uno:

- **+56 9 9154 0156** — el que ya está en `index.html`, marcado ahí como
  "WhatsApp (solo WhatsApp)" y en el campo `telephone` del schema.org de
  la página.
- **+56 9 7519 6394** — el que ya usan `cartel-qr-whatsapp.html` y otras
  piezas impresas existentes.

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

### Estándares de Fitness Profesional — inteligencia añadida a la app
### (regla permanente)

Además de la funcionalidad mínima del punto 5, toda app nueva de
`entrenar-<nombre>.html` (y, en la medida de lo posible, actualizar
también las existentes cuando se toquen por otro motivo) debe
incorporar estas tres capas de inteligencia, basadas en la fórmulas y
criterios reales de la sección "Base de conocimiento técnico" de más
abajo — nunca inventar un número o una clasificación que no salga de
ahí:

13. **Indicador automático de intensidad (%1RM).** Cuando la persona
    registra peso y repeticiones en una serie (idealmente cerca del
    fallo, para que el cálculo sea válido), estimar el %1RM de esa
    serie con la fórmula de Brzycki ya documentada
    (`%1RM = 102,78 − 2,78 × reps`, válida hasta ~10 reps) y, si hay
    peso registrado, el 1RM estimado (`1RM = peso ÷ (%1RM ÷ 100)`).
    Clasificar ese %1RM contra la escala de Martin (30-50% escasa,
    50-70% leve, 70-80% media, 80-90% submáxima, 90-100% máxima) y
    mostrarlo como una etiqueta de color junto a la serie — nunca un
    número aislado sin contexto. Si el campo de reps o peso está vacío,
    no mostrar ninguna intensidad calculada ni "rellenar" el dato.
14. **Orden de ejercicios estructurado por fatiga muscular.** Al armar
    o revisar el orden de los ejercicios de un día: primero los
    poliarticulares/compuestos (sentadilla, press banca, peso muerto,
    remo con barra), después los de aislamiento (extensiones, curl,
    elevaciones) — nunca un aislamiento pesado antes que el compuesto
    principal del día, porque la fatiga acumulada le resta rendimiento
    y seguridad a ese compuesto. Alternar cadena flexora/extensora
    (empuje/tracción) entre los días de la semana, siguiendo el
    principio de equilibrio estructural ya documentado (dorsales y
    aductores de escápula necesitan el doble o triple de volumen que
    pectorales para compensar el sedentarismo).
15. **Alertas biomecánicas visuales de postura correcta.** El campo
    `tip` de cada ejercicio (ver estructura JSON de los `entrenar-*.html`
    existentes) debe señalar explícitamente el punto de riesgo
    biomecánico del ejercicio cuando aplique (ej. "no dejes que la
    rodilla sobrepase la punta del pie" en sentadillas, "no arquees la
    zona lumbar" en press militar), priorizando las zonas de mayor
    incidencia real de lesión en sala documentadas (rodilla 30%,
    columna lumbosacra 18%, hombro 15%). En la interfaz, destacar este
    aviso de forma visual (ícono o color de alerta), no como texto
    plano perdido entre los demás campos, y mostrarlo al menos la
    primera vez que la persona ve ese ejercicio en la sesión.

Estas tres capas se **consolidan junto con el resto del sistema ya
construido** en cada app de cliente, sin reemplazar nada de lo
existente: acceso por QR (flyer o tarjeta que enlaza a la app), ficha
de IMC y % de grasa corporal (casilleros vacíos del punto 10, nunca
datos fijos en el código), asesoría de nutrición (del PDF de dieta del
cliente o de `rutinas_oficiales.md` si no hay uno específico),
cronómetro general de sesión y temporizador de descanso.

### Plantilla fija de app VIP: `app_milton.html` (regla permanente)

`app_milton.html` es la plantilla oficial y fija para cualquier cliente
VIP nuevo de ahora en adelante. Para un cliente VIP nuevo: **copiar
`app_milton.html` tal cual** y cambiar únicamente —

1. El nombre del archivo: `app_<nombre-o-apodo-del-cliente>.html` (esta
   plantilla usa el prefijo `app_`, no `entrenar-`, para no chocar con
   los `entrenar-*.html` más antiguos que ya existan de ese cliente).
2. El `<title>`, la meta descripción y el `<h1>` del encabezado, con el
   nombre del cliente nuevo.
3. La clave de `localStorage` del panel de IMC (`IMC_KEY`), cambiando
   `milton` por el nombre del cliente nuevo, para que no se mezcle con
   la ficha de otro cliente en el mismo teléfono.
4. El array `RUTINA`: la rutina de entrenamiento (días, ejercicios,
   series, descansos, alertas biomecánicas), diseñada según los datos
   reales del cliente — edad, biotipo, objetivo, nivel, días
   disponibles, estilo pedido (ej. Heavy Duty) — aplicando siempre la
   sección "Base de conocimiento técnico" de más abajo. **Nunca escribir
   el peso, la edad o el % de grasa real del cliente dentro de este
   array ni en ninguna otra parte del código** — esos datos siguen
   yendo solo en el panel de IMC vacío del punto 10.

Todo lo demás queda **idéntico entre clientes, sin rediseñar nada**: el
cronómetro de sesión, la calculadora de IMC, la duración estimada por
día, el sistema de pestañas por día, el temporizador de descanso con
beep, el estilo de las alertas biomecánicas y el diseño WGYM ADN SPORT
(negro `#000`, tarjetas `#1C1C1C`, acentos rojo/dorado).

Esta plantilla es exclusiva para clientes VIP — no usarla para apps
genéricas o de referencia sin nombre de cliente (esas quedan con la
estructura de `app_wgym_inteligente.html`, que sí puede variar).

La plantilla también incluye, junto a cada ejercicio, un registro
editable real de **peso (kg) y repeticiones al fallo** más un botón de
"hecho" (✓) — con eso el %1RM del punto 13 se calcula con el dato real
que la persona anotó, no solo con el rango objetivo. Cada ejercicio
trae además `repMin`/`repMax` (el rango de reps objetivo, ej. 6 y 10)
para que la sugerencia de abajo funcione — nunca dejar un ejercicio sin
esos dos campos (usar `null`/`null` solo en ejercicios sin reps
numéricas, como planchas por tiempo).

Todo se guarda en `localStorage` bajo `wgym_historial_<nombre>_v1`,
como un **historial completo por día + ejercicio** (no solo el último
dato) — cada vez que marca "hecho" se agrega una entrada nueva con la
fecha de ese día, sin pisar las sesiones anteriores. Con ese historial,
la app calcula sola una **sugerencia de peso para la próxima sesión**
(regla "5 y 10" de la base de conocimiento técnico): si la vez anterior
llegó al techo del rango de reps, sugiere subir ~5% (nunca más del
10%); si quedó bajo el rango, sugiere mantener el peso y priorizar
técnica; en el medio, sugiere mantener el peso e intentar una
repetición más antes de subir. Esta sugerencia se muestra siempre que
haya una sesión anterior registrada — nunca inventar una sugerencia sin
un dato real previo de esa persona en ese ejercicio.

También trae un botón **"Exportar sesión de hoy"** con los tres niveles
de respaldo del punto 5: intenta `window.claude.use('downloads')`, si
no está disponible cae a una descarga por Blob, y si el navegador la
bloquea (pasa en algunos WebView de WhatsApp/Instagram) muestra un
modal para copiar el texto a mano.

## Base de conocimiento técnico: entrenamiento, hipertrofia, nutrición
## y biomecánica (regla permanente)

Esta sección resume los conceptos clave de 23 manuales y libros técnicos
(entrenamiento de fuerza, hipertrofia, biomecánica, prevención de
lesiones, nutrición deportiva y fisiología) que el dueño subió a su
Google Drive. **Usar siempre esta base como referencia al diseñar
rutinas de entrenamiento, planes de alimentación y contenido educativo
de marketing para WGYMADNSPORT** — da rangos numéricos y criterios
concretos en vez de inventar cifras genéricas.

Si el cliente trae su propio PDF de dieta o indicación médica específica
(por ejemplo el plan de un cliente VIP, o una condición como diabetes),
esa indicación puntual siempre tiene prioridad sobre los rangos
generales de aquí. Algunos PDFs se leyeron de forma incompleta por su
tamaño (el manual del entrenador personal solo entregó el índice; el
capítulo de ajuste de insulina de "Diabetes y Ejercicio Físico", págs.
67-109, no se pudo leer) — no inventar cifras que no estén citadas
explícitamente en esta sección, especialmente en temas de salud
sensible como diabetes.

### Metodología del entrenamiento y periodización

- Seis variables de la carga de entrenamiento: frecuencia, volumen,
  intensidad, densidad, progresión y tipo de ejecución.
- Orden metodológico recomendado para subir la carga: 1) frecuencia
  semanal, 2) volumen por sesión, 3) densidad del estímulo, 4)
  intensidad — en ese orden, no todo a la vez.
- Clasificación de métodos de fuerza (Zatsiorski): esfuerzos máximos
  (90-100% 1RM, 3-5 series, 1-3 reps, 5-7 días de recuperación, solo
  alto rendimiento); esfuerzos repetidos (70-80% 1RM, 6x6, 2 días de
  recuperación, apto para principiantes); esfuerzos dinámicos (20-50%
  1RM, 1-8 reps, prioriza velocidad de ejecución).
- Tabla intensidad-objetivo (González-Badillo): 90-100% 1RM (4-8x1-3) =
  fuerza máxima, poca hipertrofia; 80-85% (3-5x5-7) = fuerza máxima con
  hipertrofia moderada; 70-80% (3-5x6-12) = hipertrofia muscular alta;
  60-75% (3-5x6-12, dejando 2-6 reps en reserva) = acondicionamiento
  general para principiantes — antecedente del concepto RIR actual.
- Escala de intensidad (Martin): 30-50% 1RM = escasa, 50-70% = leve,
  70-80% = media, 80-90% = submáxima, 90-100% = máxima.
- Fórmulas de %1RM desde repeticiones al fallo: Brzycki
  `%1RM = 102,78 − 2,78 × reps`; Lander `%1RM = 101,3 − 2,67123 × reps`
  (más precisas hasta 10 reps).
- Protocolo de test de 1RM: calentar 10-12 min + 2 series de 12-15 reps
  al 30-40% 1RM (1 min descanso), subir de a 2-10 kg con 2-3 reps y 1
  min de descanso hasta acercarse al máximo, luego 1 repetición por
  intento con 3 min de descanso hasta fallar.
- Ley de Henneman (reclutamiento de fibras): cargas ligeras reclutan
  solo fibras lentas tipo I; cargas medias suman fibras IIa; solo cargas
  máximas o movimientos explosivos reclutan también fibras rápidas IIb.
- Principio de continuidad: descansos muy largos no generan
  entrenamiento, muy cortos sobreentrenan; el período de transición
  entre bloques no debería superar 14-28 días.
- Calentamiento: eleva la FC a 120-140 ppm y tarda 1-2 min en generar
  régimen cardiorrespiratorio óptimo antes del bloque principal.
- Fórmulas de FC para prescribir cardio: FC máx. clásica = 220 − edad;
  FC máx. de Seals (más exacta) = 208 − (0,7 × edad); FC de
  entrenamiento por Karvonen = FC reposo + (FC máx. − FC reposo) × un
  factor de 0,50 (mínimo) a 0,85 (máximo) según intensidad buscada.
- Principio de multilateralidad: la flexibilidad mejora día a día, la
  fuerza semana a semana, la velocidad mes a mes y la resistencia año a
  año — programar la progresión de cada cualidad con su propio ritmo,
  sin esperar avances iguales en todas a la vez.
- Toda habilidad técnica nueva se enseña en tres mecanismos: percepción
  (leer la información relevante), decisión (elegir la respuesta) y
  ejecución (la técnica en sí) — explicar también el "cuándo y por qué"
  de un ejercicio, no solo el movimiento.

### Hipertrofia muscular

- Hipertrofia sarcoplásmica (más volumen, 12-15RM, agotar todas las
  series de un ejercicio antes de pasar al siguiente) vs. sarcomérica/
  miofibrilar (funcional, 8-10RM, 9 series por grupo repartidas en 3
  ejercicios, 1ª serie de cada ejercicio antes de repetir) — esta
  segunda es la que más aumenta la fuerza real.
- Rango general de hipertrofia: 6 a 20 repeticiones por serie, sin bajar
  del 80% de la potencia máxima testeada con esa carga.
- Descanso entre series (hipertrofia): principiante 1 min, intermedio
  1-2 min, avanzado 1-1:30 a 2 min. Entre sesiones del mismo músculo:
  36-72 h según nivel.
- Volumen semanal orientativo por biotipo: ectomorfo 12-21 series/sesión
  y 2-4 sesiones/semana; mesomorfo y endomorfo 12-24 series/sesión y
  3-6 sesiones/semana (hasta 8-10 series en avanzados). Alternar 6-9
  semanas intensas con 2-3 semanas de descarga.
- El trabajo excéntrico puro no debe superar 3 semanas seguidas ni
  usarse cerca de una competencia.
- Técnicas para romper estancamiento: repeticiones forzadas, series
  descendentes (bajar 10-20% de carga al fallo, máx. 2-3 veces por
  serie), superseries para el mismo grupo, amplitud creciente por
  tercios de rango de movimiento.
- Tipos de hipertrofia según objetivo del cliente: general, estructural,
  compensadora (corrige desequilibrios biomecánicos) y estética (masa +
  reducción de grasa) — cada una con fases de 3 a 5 semanas de
  adaptación y ejercicios distintos.

### Biomecánica, prevención de lesiones y poblaciones especiales

- Equilibrio estructural: la cadena extensora (espalda, dorsales,
  aductores de escápula) se debilita por sedentarismo mientras la
  flexora (pectoral, deltoides anterior) se acorta — causa directa del
  dorso redondo. Dar el doble o triple de volumen a dorsales/aductores
  de escápula que a pectorales para compensar.
- Relación de fuerza cuádriceps:isquiotibiales debe ser 3:2; si se
  desplaza hacia el cuádriceps aumenta la presión rotuliana y el riesgo
  de síndrome rotuliano — nunca entrenar extensores de rodilla sin la
  proporción correcta de flexores.
- Cuatro etapas de adaptación obligatorias y secuenciales (nunca
  saltarlas, sobre todo con principiantes): 1) neuroendocrina —
  movilidad + aeróbico suave 15-30 min 3x/semana, 3-5 semanas mínimo;
  2) cardiovascular — aeróbico 3-5x/semana, 6-15 semanas; 3) aparato
  motor pasivo — fuerza en máxima amplitud, técnica sobre intensidad,
  6-15 semanas; 4) aparato motor activo — recién aquí ejercicios
  poliarticulares e intensidad creciente.
- Regla de supercompensación: cada músculo se entrena cada 3-4 días; un
  principiante necesita 4-5 días de recuperación completa.
- Señales de recuperación insuficiente antes de subir carga: agujetas
  fuertes, falta de ímpetu, cansancio y tensión persistentes, falta de
  concentración, sudor en reposo, trastornos del movimiento.
- Lesiones en sala de pesas por frecuencia: rodillas 30%, columna
  lumbosacra 18%, hombros 15%, muñeca 13%, codos 10%, manos 6%.
- Protocolo RICE ante lesión aguda: reposo inmediato, hielo 15-20 min
  (nunca directo sobre la piel, repetible cada hora durante 24-48h),
  compresión con venda elástica, elevación a la altura del corazón. El
  calor está prohibido en fase aguda y hasta 48 h después.
- Señal de alarma para derivar a un profesional de salud: dolor intenso
  o que se prolonga más de unos días — nunca automedicar ni seguir
  entrenando la zona afectada.
- Regla "5 y 10" de progresión (aplicable también a cargas de sala):
  nunca subir volumen ni intensidad más del 10% (idealmente 5%) de una
  semana a la siguiente. Método duro-fácil: nunca dos sesiones intensas
  seguidas sobre el mismo patrón de movimiento.
- Toda sesión en 3 partes: inicial (calentamiento general y específico,
  10-20 min), medular (el objetivo planificado) y final (vuelta a la
  calma) — omitir la vuelta a la calma empeora la recuperación.
- Niños/adolescentes: sí pueden ganar fuerza real antes de la pubertad
  (por coordinación neuromuscular, no por testosterona) sin dañar el
  cartílago de crecimiento si el entrenamiento está bien supervisado.
  No iniciar cargas altas y específicas (ej. levantamientos olímpicos)
  antes de los 13 años. El entrenamiento con sobrecarga reduce hasta un
  33% las lesiones deportivas generales y un 50% el tiempo de
  rehabilitación en jóvenes deportistas (NSCA). Supervisión mínima: 1
  instructor cada 3 niños.
- Checklist de seguridad de sala válido para cualquier cliente: enseñar
  la técnica antes de cargar, calentamiento general + específico con
  estiramiento al inicio y al final, nunca ignorar el dolor articular,
  registrar cada sesión (ejercicio, volumen, duración, intensidad, si
  se completó o no y por qué).

### Nutrición deportiva: cálculo calórico, macros y timing

- Gasto calórico total (TEE) = metabolismo basal (TMB) + efecto térmico
  de los alimentos + gasto por actividad.
- TMB Harris-Benedict hombres: `66 + (13,7 × kg) + (5 × cm) − (6,8 × edad)`.
  Mujeres: `65,5 + (9,6 × kg) + (1,7 × cm) − (4,7 × edad)`.
- Factor de actividad sobre el TMB (orientativo): reposo ×1, muy ligera
  ×1,5, ligera ×2,5, moderada ×5, intensa ×7 — no reemplaza una
  medición real, es solo referencia rápida.
- Proteína según objetivo: 1,2-2,0 g/kg/día cubre a la mayoría de
  deportistas; subir a ≥2,0 g/kg/día en déficit calórico o lesión para
  proteger masa magra; rango deportivo amplio 1,8-4,4 g/kg, óptimo para
  fuerza/potencia ≈2,0-2,2 g/kg, y en superávit no hace falta superar
  ≈2,2 g/kg (más proteína no mejora más la ganancia muscular).
- Carbohidratos: fuerza/potencia 2,2-5,5 g/kg/día (promedio útil ≈3,3
  g/kg); deportes de equipo 3,3-6,6 g/kg/día.
- Grasas: mínimo 0,66 g/kg/día para soporte hormonal, techo práctico
  ~40% de las calorías totales; en déficit recortar primero grasas
  antes que proteína o carbohidratos.
- Pérdida de grasa: déficit moderado de 250-500 kcal/día, bajar menos
  del 1% del peso corporal por semana para preservar músculo y
  rendimiento; resultados esperables recién en 3-6 semanas. Bajar 1 kg
  de grasa exige un déficit acumulado de ≈7000 kcal.
- Timing: 4-8 comidas/día con 1/8-1/4 de la proteína diaria cada una,
  cada 3-6 h; comer entre 30 min y 4 h antes de entrenar, y entre
  inmediato y 1 h después. Post-entreno: 15-25 g (0,25-0,3 g/kg) de
  proteína de alto valor biológico en las primeras 0-2 h.
- Jerarquía real de importancia: 1) balance calórico, 2) macronutrientes,
  3) timing (un mal timing cuesta como máximo ~10% del resultado — nunca
  es lo primero a corregir en un plan que no está funcionando).
- El exceso de proteína no usada se convierte en grasa corporal y sube
  la carga renal — "más proteína siempre" no es ventaja automática.
- Para medir avance, priorizar composición corporal (pliegues cutáneos,
  perímetros) sobre el peso bruto en la balanza; pesar/medir siempre a
  la misma hora, idealmente en ayunas por la mañana.

### Suplementación deportiva (qué sí tiene evidencia y qué no)

- Creatina monohidrato: única forma con evidencia sólida. Carga 20-30
  g/día (o 0,25-0,35 g/kg/día) durante 5-7 días + mantenimiento de 3-5
  g/día (0,1 g/kg/día); también funciona ir directo a la dosis de
  mantenimiento sin fase de carga, solo tarda más en saturar. Requiere
  buena hidratación por su efecto osmótico.
- Cafeína: 3-6 mg/kg, 45-60 min antes del esfuerzo; usarla de forma
  puntual (no todos los días) para no generar tolerancia.
- Beta-alanina: 4,8-6,4 g/día fraccionados en dosis de 0,8-1,6 g cada
  4-6 h para evitar parestesias (hormigueo).
- BCAA's: evidencia débil — una proteína completa siempre es mejor
  opción que BCAA's aislados; no recomendarlos como suplemento
  prioritario.
- Vitaminas/minerales y picolinato de cromo: sin déficit diagnosticado y
  con dieta balanceada, no mejoran el rendimiento ni actúan como
  anabólicos — no venderlos como tal.
- Vitamina D3: 1000-2000 UI/día solo si hay insuficiencia o deficiencia
  confirmada por examen. Omega 3: 250-500 mg/día en dietas pobres en
  pescado azul.

### Metabolismo energético y composición corporal

- Sistemas energéticos según duración del esfuerzo: 0-30 seg → fosfágeno
  ATP-PC (sprints, saltos); 30 seg-1,5 min → ATP-PC + vía láctica;
  1,5-3 min → láctica + aeróbica; más de 3 min → predominio aeróbico. El
  aporte de las grasas gana peso recién pasados los ~30 min de
  ejercicio continuo.
- Reservas energéticas de un adulto de 70 kg: glucógeno muscular ≈350 g
  y hepático ≈150 g (se agotan en ayuno a las 24-36 h); grasa corporal
  ≈125.000 kcal — la reserva dominante frente a las ~2000 kcal de
  carbohidratos disponibles.
- Gasto energético diario: ~70% metabolismo de reposo, ~20% actividad
  física, ~10% termogénesis de la digestión (mayor con proteínas).
- Equivalencias: 1 g de carbohidrato o proteína = 4 kcal; 1 g de grasa =
  9 kcal.
- Hidratación: se pueden perder hasta 1,5 L de sudor por hora; tomar
  150-250 ml cada 10-15 min. Agua o hipotónica si el ejercicio dura
  menos de 1 h; isotónica entre 1-2 h; con carbohidratos añadidos si
  supera 2 h o hace frío. Electrolitos solo hacen falta si el ejercicio
  supera 3 h — la mayoría de los calambres se deben a deshidratación,
  no a falta de sales.
- Suma de 6 pliegues cutáneos (tríceps + subescapular + supraespinal +
  abdominal + muslo anterior + pantorrilla) como indicador rápido de
  grasa subcutánea: referencia de persona joven normal ≈65 mm en
  hombres y ≈91 mm en mujeres. Medir siempre con el mismo calibre y la
  misma fórmula en el tiempo — mezclar métodos invalida la comparación.
- La grasa abdominal/visceral es el principal factor de riesgo
  cardiovascular y de diabetes, más que la grasa subcutánea general.
  Hasta un 70% de la variación del IMC entre personas se explica por
  factores genéticos — útil para explicarle a un cliente por qué dos
  personas con la misma dieta no bajan de peso igual.

### Referencia antropométrica: CHIREF, sujetos físicamente activos (Chile)

- Estudio chileno (Rodríguez, Almagià, Yuing, Binvignat & Lizana, 2010,
  *Int. J. Morphol.* 28(4):1159-1165) que midió con protocolo ISAK a 100
  hombres y 79 mujeres de 20-29 años, sanos y físicamente activos (sin
  factores de riesgo cardiovascular, IMC normal), entregando tablas de
  referencia con promedio, desviación estándar y percentiles 5/15/25/
  50/75/85/95% de perímetros, pliegues cutáneos y somatotipo.
- Cintura mínima en mujeres activas: promedio 71,4 cm (DS 6,4), mediana
  70,8 cm. Percentiles — 5%: 63,4 cm · 15%: 66,0 cm · 25%: 67,0 cm ·
  50%: 70,8 cm · 75%: 75,1 cm · 85%: 77,5 cm · 95%: 84,2 cm.
- Cintura mínima en hombres activos: promedio 79,0 cm (DS 6,7), mediana
  78,3 cm. Percentiles — 5%: 71,1 cm · 15%: 73,3 cm · 25%: 75,1 cm ·
  50%: 78,3 cm · 75%: 83,3 cm · 85%: 85,6 cm · 95%: 88,0 cm.
- % de grasa corporal de referencia (método Kerr, 5 componentes):
  mujeres activas 29,6% (DS 4,2); hombres activos 21,6% (DS 4,1).
- IMC de referencia: hombres 23,0 kg/m² (DS 2,3), mujeres 22,5 kg/m²
  (DS 3,2) — ambos dentro del rango "normal" OMS (18,5-24,9).
- Somatotipo promedio (Heath-Carter): mujeres endo-mesomórfico (Endo
  4,1 · Meso 4,2 · Ecto 2,1); hombres meso-endomórfico (Endo 2,7 · Meso
  5,1 · Ecto 2,5) — en ambos predomina el componente mesomórfico
  (robustez músculo-esquelética).
- **Uso recomendado**: sirve para ubicar la cintura o el % de grasa de
  un cliente activo dentro de una distribución real de personas
  activas y sanas (no solo contra el umbral de riesgo OMS), y para
  fijar metas de cintura con base en percentiles de gente activa en
  vez de un número arbitrario — por ejemplo, moverse del percentil 50
  hacia el 25 o el 15 como meta realista, nunca hacia el 5% como
  objetivo por defecto.
- **Limitación importante**: la muestra tiene 20-29 años — es la mejor
  referencia de "persona físicamente activa" que tenemos, pero no está
  ajustada a otras edades. Usarla como referencia direccional en
  clientes fuera de ese rango etario, dejando claro que no es una
  medición hecha en su mismo grupo de edad.

### Salud y poblaciones especiales: sobrepeso, obesidad y diabetes

- Clasificación OMS por IMC: sobrepeso 25,0-29,9 kg/m²; obesidad ≥30
  kg/m². El riesgo metabólico (triglicéridos, insulina, presión
  arterial) ya sube de forma clara en el rango de sobrepeso, no solo en
  obesidad franca; 27 kg/m² es un umbral práctico de alerta temprana de
  insulinorresistencia.
- **Diabetes — nunca entrenar a un cliente diabético sin evaluación
  médica previa**, obligatoria en hombres mayores de 40 años y mujeres
  mayores de 50, o con factores de riesgo coronario (hipertensión,
  colesterol alto, tabaquismo, antecedentes familiares tempranos).
  Contraindicación absoluta de esfuerzo: presión arterial mayor a
  200/120 mmHg o arritmia ventricular no controlada.
- Ejercicio recomendado en diabetes: aeróbico de baja intensidad y
  larga duración (caminar, nadar, bici), con frecuencia cardíaca menor
  al 80% de la máxima. Progresión segura: inicio (4-6 semanas, 3
  veces/semana, menos de 45 min, menos del 50% FC máx.) → mejora (5-6
  meses, hasta 70-80% FC máx., 60 min) → mantenimiento (desde el 6º mes,
  de por vida).
- Un solo entrenamiento mejora la sensibilidad a la insulina durante
  12-24 h, pero el beneficio sobre el control glucémico se pierde a las
  72 h de la última sesión — con un cliente diabético la regularidad
  (mínimo 3 veces/semana) no es negociable, entrenar de forma
  esporádica no sirve.
- El miedo a la hipoglucemia es una de las principales barreras
  psicológicas que alejan a un cliente diabético del ejercicio —
  conviene conversarlo explícitamente al motivarlo, no solo entregarle
  la rutina.
- **No improvisar cifras de ajuste de insulina o de manejo de glucemia
  durante el ejercicio** — ese detalle no se pudo leer completo del
  manual fuente; para un cliente diabético, la pauta específica siempre
  debe venir de su propio equipo médico.
