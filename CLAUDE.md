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

### Tipografía de titulares: Rubik Distressed (regla permanente, desde 09/2026)

Desde septiembre de 2026, **Rubik Distressed** (Google Fonts, gratis) es la
tipografía oficial de titulares/headlines de WGYMADNSPORT — reemplaza a
Anton para títulos grandes (nombre de sección, frases motivacionales,
"HORARIOS", etc.). Mantiene el look de letra gruesa con borde
desgastado/pincel que el dueño aprobó.

- El archivo de la fuente vive en `assets/font-rubik-distressed.ttf`
  (descargado una vez de Google Fonts) — usarlo como fuente para generar
  el `@font-face` en base64 embebido, igual que se hace con Anton y
  Barlow Condensed en los carteles impresos existentes.
- **Sigue usándose en mayúsculas** (`text-transform:uppercase`) — en
  minúsculas pierde el efecto de letra rugosa/pincel.
- Anton se mantiene solo para textos numéricos grandes (horas, precios,
  cantidades) donde Rubik Distressed no calza tan bien; Barlow Condensed
  sigue siendo la fuente de cuerpo/etiquetas pequeñas.
- Paleta sin cambios: negro `#0A0A0B`/`#0D0D0F`, rojo `#E30613`, dorado
  `#D4AF37`, blanco.
- Ver `plantilla-post-horarios.html` como referencia de la plantilla ya
  actualizada a este estilo (fondo con textura sutil, franja de 4
  iconos de valores, franjas rojas de horario tipo pastilla, logo real
  grande arriba a la izquierda, bloque de contacto con ambos números).
- Al tocar otra pieza por otro motivo, aprovechar de migrarla a este
  estilo si es razonable — no hace falta salir a rehacer todo el sitio
  de una sola vez.

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

**Única excepción, a pedido explícito de la dueña (10/2026):** el cartel
de pago (`cartel-pago-qr.html`/`.pdf`) y `pagar.html` llevan **solo el
WhatsApp de Sara (+56 9 7519 6394)**, en grande, porque los pagos y
comprobantes van a ella. No volver a poner los dos ahí.

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
2. **Nunca escribir un RUT real en `socios.json` ni en ningún archivo que
   se publique en el sitio** (`tarjeta.html`, `entrenar-*.html`,
   `rutina-*.html`, `control.html`, `pantalla.html`). El campo `"rut"`
   siempre va como `"Sin Rut"`, aunque el dato que llegue (del botón
   "📋 Copiar", de "Pasar la lista" o de cualquier otro origen) traiga un
   RUT real — se descarta antes de guardar. Motivo: este repositorio es
   público y esos archivos se sirven tal cual en el sitio en vivo; en
   septiembre de 2026 se encontró que el RUT real de todos los socios
   estaba expuesto sin protección en 16 archivos y se limpió por completo
   (ver commit correspondiente). Si el dueño necesita llevar un registro
   de RUT para algún trámite, debe guardarlo aparte, fuera de este
   repositorio (papel, planilla privada, etc.), nunca en estos archivos.
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
   actualizar `plan`/`monto`/`fv` con lo que llegó, dejando siempre el
   campo `"rut"` en `"Sin Rut"` (no se guarda RUT real en este archivo —
   ver regla permanente de arriba).
2. Regenerar `LISTA_BASE` (control.html) y `SOCIOS` (pantalla.html),
   subir versión, validar y publicar en `main`, igual que con
   cualquier otro cambio de `socios.json`.
3. Confirmarle a la usuaria el cambio (nombre, fecha nueva).

Esta es la forma preferida de avisar una renovación de UNA persona —
más simple que pegar la lista completa de "Pasar la lista" para un
solo cambio.

### Botón "Pagar mensualidad" en la tarjeta (desde 10/2026)

`tarjeta.html` muestra a cada socio "Tu mensualidad" con el precio de
su plan y un botón "Pagar mensualidad" con los datos de transferencia
(📋 Copiar datos + enviar comprobante por WhatsApp a Sara,
+56 9 7519 6394). Precios oficiales en `PRECIOS_PLANES` (Full Mensual
$33.000; 3 Veces por Semana, Funcionarios Públicos y Estudiante/Profesor
$28.000; Tercera Edad y Turno $23.000; Semanal $15.000; Pase Diario
$4.000); un plan que no esté ahí (ej. Plan Especial) usa el `monto` de
la ficha. Planes, precios y cuenta viven en **`pago-datos.js`** (un solo
lugar, lo leen `tarjeta.html` y `pagar.html`). `pagar.html` es la página
para clientes nuevos (eligen plan, escriben su nombre, Copiar datos,
WhatsApp); la abre el QR de `cartel-pago-qr.html`/`.pdf` (A4, fuentes
embebidas). **Si cambia un precio**: editar `pago-datos.js` y además
regenerar el cartel, que trae los precios impresos. La cuenta es la de la propia
dueña (Banco Falabella), publicada a propósito por ella para recibir
transferencias; la regla de "nunca escribir un RUT real" es para los
RUT de los socios, no para estos datos de cobro. El pago NO renueva
solo: la dueña registra la renovación en el mesón como siempre. Se
evaluó Mercado Pago (links de pago por plan) y se dejó para más
adelante; si se agrega, nunca poner claves/tokens en el repo, solo los
links públicos.

### Ingresos de hoy y MARCAR SALIDA (desde 10/2026)

**Mesón (`control.html`) y tablet (`pantalla.html`)** muestran el panel
completo **"Ingresos de hoy"** (`ingresos.js`), sin simplificar (pedido
explícito de la dueña, 10/2026): contadores **Ingresos / Personas /
Dentro ahora**, la lista de quienes siguen dentro con **MARCAR SALIDA**,
búsqueda, selector de fecha e historial del día (DENTRO / SALIDA
REGISTRADA, "Deshacer"), más el botón **"Marcar salida a todos"** para
cerrar el día o limpiar a quienes se fueron sin marcar. Desde 06-10-2026
el historial va en una "carpeta" (📁 Historial del día · ▼ Ver), cerrada
por defecto; cada equipo recuerda si quedó abierta
(`wgym_historial_abierto_v1`) y al buscar un nombre se abre sola. Desde
07-10-2026 la lista "Dentro del gimnasio" va del último que entró
(arriba) al primero. En la tablet,
MARCAR SALIDA pide la clave de administración una sola vez y la guarda en
ese equipo.

**Tarjeta virtual (`tarjeta.html`)**: muestra **solo** el contador verde
**"DENTRO AHORA"** (número de personas con ingreso hoy sin salida, que
`miIngreso` entrega como `dentroAhora`), nunca los contadores
Ingresos/Personas ni nombres de otros socios, más el botón **"Registrar
mi salida"** cuando el socio está dentro. Se refresca
mientras la tarjeta está a la vista (cada 30 s desde 05-10-2026, para no saturar la hoja; mientras carga muestra "Viendo cuánta gente hay…" y, si falla, "Reintentar"). Desde la casa (ícono o enlace de
siempre) el socio lo consulta sin registrar ingreso: ese es el objetivo,
ver cuándo el gym está más vacío.
- **"Ahora" del celular** cuenta solo ingresos sin salida de las últimas
  `VENTANA_DENTRO_H` (2) horas (05-10-2026: la tablet marcaba 7 y había 1; antes 3) — a quien olvidó marcar salida se le deja
  de contar. **Desde 11-10-2026 (la dueña: "las personas no se me salen en dos
  horas") mesón y tablet hacen lo mismo:** en `ingresos.js` (`salidaAuto`,
  `AUTO_SALIDA_MS`) quien no marcó salida sale solo de "Dentro" a las 2 h de su
  ingreso y el historial dice "SALIDA AUTOMÁTICA · HH:MM" (sin "Deshacer"). Es
  solo de pantalla: la hoja no se toca. Al cambiar `ingresos.js`, subir su `?v=`
  en `control.html` y `pantalla.html`.
- **"Elige tu horario"**: gráfico por hora y día con el promedio de
  personas, de `horarios.json` (solo promedios, sin nombres), generado con
  `scripts/generar-horarios.py` desde la hoja de ingresos descargada como
  CSV (el CSV no se sube: trae nombres). Regenerarlo cada tanto.
- **Cartel "TODO AL ALCANCE DE TU CELULAR"** (impreso por la dueña): su QR
  apunta a `prueba-tarjeta.html?ingreso=puerta`. Al publicar,
  `prueba-tarjeta.html` se reemplaza por un puente que redirige a
  `tarjeta.html` conservando `?ingreso=puerta` — no borrar ese archivo.

- **La fuente es la hoja de Google del check-in**, nunca un archivo del
  repo: el Apps Script (acciones `listarIngresos`, `registrarSalida`,
  `quitarSalida`, `miIngreso`, `ingresoTarjeta`, `salidaSocio`; código en
  `docs/apps-script/Ingresos.gs`)
  guarda la salida en las columnas E/F de la misma hoja de ingresos. La
  dueña lo instala siguiendo `docs/apps-script-ingresos-salidas.md`.
- Causa del problema original: la respuesta antigua del script trae solo
  los **últimos 20** ingresos; los demás nunca se borraron de la hoja.
- Mientras el script no tenga las acciones nuevas, las páginas siguen
  funcionando como antes (el panel guarda en el equipo lo que alcanzó a
  ver y desactiva MARCAR SALIDA con un aviso).
- Una salida cierra **todos** los ingresos abiertos de esa persona ese
  día.
- **Abrir la tarjeta no es ingresar (regla permanente):** el ingreso se
  registra SOLO cuando la tarjeta se abre con el QR de la puerta
  (`tarjeta.html?ingreso=puerta`, sticker en `qr-entrada-puerta.pdf`
  pegado sobre el QR antiguo del cartel "TARJETA VIRTUAL"). El socio
  hace lo mismo de siempre: escanea y escribe su nombre. Abierta por
  cualquier otro enlace solo consulta. La marca se borra de la dirección
  al cargar (un enlace guardado o compartido no registra). El QR antiguo
  del cartel abría `tarjeta.html` sin marca.
- **Botón "Registrar mi ingreso" en la tarjeta (03-10-2026, pedido de la
  dueña: la mayoría de los socios entra con su acceso directo, no con el
  QR):** abierta por cualquier vía, la tarjeta muestra este botón cuando
  el socio no está dentro; al llegar lo toca (mismo `ingresoTarjeta` con
  `forzar=1` que el QR de la puerta). Desde la casa no lo toca: abrir la
  tarjeta sigue sin registrar nada solo. Si está dentro hace más de 30
  min sin salida, aparece "Volví: registrar nuevo ingreso".
  **Desde 06-10-2026** (la dueña: "la gente se aburre esperando que cargue
  el botón y cree que ya está registrada") el botón aparece **al instante**
  (en `pintarCargando()`, sin esperar a la hoja) y el cuadro `#salidaCard`
  va **primero**, arriba de todo. Al registrarse se ve "✅ Tu ingreso está
  registrado (HH:MM)"; una lista atrasada de la hoja no vuelve a mostrar
  el botón durante 2 min (`ingresoHecho`).
- **Diseño de la tablet en la tarjeta (10-10-2026, pedido de la dueña: "ese
  diseño", mismo de `pantalla.html`, fondo oscuro):** `tarjeta-deportivo.css`
  va encima del CSS de `tarjeta.html` (solo apariencia): logo grande + franja
  roja/dorada, ficha del socio como el cuadro «Último ingreso» (degradado rojo
  con rayas doradas, borde verde/dorado/rojo según el estado), cuadros con
  borde dorado y títulos en Rubik Distressed amarillo, botones secundarios
  amarillos. Al cambiarlo, subir su `?v=` y `TARJETA_VERSION`.
- **Logo animado en la entrada (10-10-2026, pedido de la dueña):** en la
  pantalla donde se escribe el nombre, `#gateVideo` reproduce en bucle y sin
  sonido `assets/intro-tarjeta.mp4`/`.webm` (logo ADN Sport 3D) en vez del logo
  fijo; si no carga, vuelve `#gateLogoImg`. (Primero se puso como intro a
  pantalla completa y la dueña pidió moverla aquí.)
- **Entrada rápida (05-10-2026, la dueña: "sale Buscando... y se demora"):**
  la tarjeta guarda en el teléfono la lista de socios (`wgym_lista_socios_v1`,
  mismo dato público sin RUT) y el último nombre escrito
  (`wgym_ultimo_socio_v1`, aparece ya puesto). Busca primero ahí y abre al
  instante; la lista de la hoja llega por detrás y corrige fecha/plan.
- **Bienvenida a socios nuevos (05-10-2026, pedido de la dueña: "solo
  nuevos y solo una vez"):** al abrir su tarjeta, `revisarBienvenida()`
  consulta `asistenciaDesde` (75 días) y, si el socio tiene 2 días o menos
  con ingreso, muestra un saludo a pantalla completa ("¡Hola, NOMBRE!",
  3 pasos, lema, confeti rojo/dorado). Nunca a socios antiguos ni a pases
  diarios. El teléfono guarda en `wgym_bienvenida_v1` a quién ya revisó y
  no vuelve a consultar.
- **"🔥 Mis calorías del día" — SACADO de la tarjeta el 10-10-2026** (la dueña
  vende WGYMNUTRI aparte y no quiere que la tarjeta lo regale; `renderCalorias`
  ya no se llama y `#calCard` queda oculto; no volver a mostrarlo). Era un cuadro
  `#calCard` en la tarjeta (`renderCalorias()`). El socio elige sexo,
  edad, peso, estatura, actividad (×1,2 a ×1,9) y objetivo (bajar grasa /
  mantenerme / ganar músculo) y ve calorías, proteína, grasas y
  carbohidratos según la base técnica (Harris-Benedict corregida,
  déficit 250-500 kcal sin bajar del TMB, proteína 2,0 g/kg en déficit,
  2,0-2,2 para ganar, 1,2-2,0 para mantener, grasas ≥0,66 g/kg y ≤40 %).
  Para ganar músculo no se inventa un superávit: se muestra la mantención
  como base. Los datos son de salud: se guardan SOLO en el teléfono
  (`wgym_calorias_v1`), nunca en la hoja ni en el repo.
- **"🤖 Mi coach virtual" (07-10-2026, la dueña eligió la opción de preguntas
  para elegir, sin IA ni costo):** cuadro `#coachCard` en la tarjeta
  (`renderCoach()`, después de las calorías). Preguntas: ¿qué me toca hoy?
  (día de hoy en Chile según `weekday` de la rutina), ¿cómo hago un ejercicio?
  (foto/video, músculo, series, descanso y `tip` del JSON), 3 × 12, descanso,
  orden, progreso y dolor (siempre deriva al profesor/profesional). Lee
  `rutinas/<id>.json`; la rutina del socio sale de su clave de progreso en
  ese teléfono o la elige él (`wgym_coach_rutina_v1`). Si se agrega una
  rutina nueva al formato JSON, sumarla a `COACH_RUTINAS`.
  **"🔄 La máquina está ocupada" (07-10-2026):** propone hasta 4
  reemplazos sacados SOLO de ejercicios que ya están en alguna rutina del
  gimnasio (así existen las máquinas), con el mismo músculo principal
  (`COACH_GRUPOS`), primero los que comparten más músculos y usan otro
  equipo, sin repetir el mismo ejercicio con otro nombre. Se hacen las
  mismas series y repeticiones de la rutina.
  **Rutinas desde la tarjeta (07-10-2026, la dueña: "así mi gente no tiene
  que escanear su rutina a cada rato"):** se abren SOLO desde "📚 Ver todas
  las rutinas" (vista `rutinas`); el botón rojo "Abrir mi rutina" se sacó a
  pedido de ella ("no debería abrir nada").
  La lista muestra las rutinas y cada una abre su página al tocarla, guardando la elegida.
  Desde 07-10-2026 (la dueña) muestra solo las de mujer (7) o las de hombre (5)
  según el socio: 4.º campo "F"/"M" de `COACH_RUTINAS`. El sexo sale del
  PRIMER NOMBRE (`coachSexoNombre`: termina en "A" → mujer, si no → hombre,
  con las excepciones de `COACH_F`/`COACH_M`); solo los nombres de
  `COACH_DUDA` se preguntan una vez (`wgym_coach_sexo_v1`). Sin enlace para
  ver las del otro grupo (pedido de la dueña). Si llega un socio con nombre
  femenino que no termina en "A" (o al revés), sumarlo a la lista que toque.
- **Bloqueo por mensualidad vencida (07-10-2026, la dueña: "si se le vence
  la mensualidad se le bloquee y, si paga, yo se la activo del mesón"):**
  en la tarjeta, con el plan vencido el coach y "Ver todas las rutinas"
  muestran "🔒 Tus rutinas están bloqueadas" + "💳 Pagar mi mensualidad"
  (abre el cuadro de pago); al renovar en el mesón la tarjeta recibe la fecha
  nueva de la hoja (`actualizarTarjeta_` → `renderCoach`) y se desbloquea.
  En las rutinas (`motor-rutina.js`, `login()`) se consulta `socios.json` Y
  la hoja (`listarSocios`) y vale la fecha MÁS NUEVA: la renovación del mesón
  desbloquea al tiro y un socio cargado solo en el mesón también entra.
  Al cambiar el motor, subir `motor-rutina.js?v=` en las 12 páginas.
  **Tarjeta completa bloqueada (07-10-2026, la dueña: "los vencidos aún
  entran a su tarjeta virtual"):** con el plan vencido (`tarjetaBloqueada_`,
  pase diario vencido incluido) `unlockCardView` muestra solo `#bloqueoCard`
  ("🔒 Tarjeta bloqueada" + "💳 Pagar mi mensualidad"), la ficha
  (MEMBRESÍA VENCIDA) y el cuadro de pago: no registra ingreso (ni con el QR
  de la puerta), sin "en vivo", calorías, coach, evolución, bandas ni
  candados. Si la hoja trae otra fecha, `actualizarTarjeta_` vuelve a llamar
  a `unlockCardView` y la tarjeta se desbloquea (o bloquea) sola.
  **Nombre ya escrito (07-10-2026):** la tarjeta abre cada rutina con
  `?socio=Nombre Apellido`; `ponerNombre()` del motor lo pone en el casillero
  y lo borra de la dirección. Sin parámetro usa el último nombre que entró en
  ese teléfono (`wgym_rutina_nombre_v1`) o el de la tarjeta
  (`wgym_ultimo_socio_v1`). El socio solo toca "Ingresar a mi rutina".
- **🏆 Ranking del mes en la tarjeta (11-10-2026, la dueña: "pongámoslo en la tarjeta virtual
  de los socios"):** cuadro `#rankCard` (`renderRanking_`, oculto con tarjeta bloqueada y en
  pases diarios). Sin unirse muestra «Este mes llevas N días entrenando» (`asistenciaDesde`) y
  pide un APODO; unido muestra su lugar y el top 10 (solo apodo y días) con «Salir del
  ranking». Los puntos = días con ingreso en el mes, calculados por el Apps Script
  (`guardarReto` guarda mes, id al azar del teléfono, apodo y nombre en la hoja privada
  «Retos»; `listarRetos` cuenta los días con `diasDesde_` y entrega solo apodo + días, caché
  120 s). El teléfono recuerda su apodo e id en `wgym_ranking_v1`. **Versión 17 del Apps
  Script instalada por la dueña el 10-10-2026 a las 21:13** (misma implementación y enlace;
  INGRESOS.gs verificado idéntico al repo vía Drive; para volver atrás: lápiz → Versión 16).
  **Versión 18 (instalada por la dueña el 10-10-2026 a las 21:23, verificada idéntica al repo):** la planilla convertía el mes «2026-10» en fecha y el
  ranking salía vacío («Todavía nadie se une»); `mesDe_` lo lee como texto y se escribe con
  apóstrofo. Nunca guardar textos tipo «AAAA-MM» sin apóstrofo en la planilla.
  Con la Versión 17 quedaron filas repetidas de una misma persona («Sari» ×3). **Versión 19,
  instalada por la dueña el 10-10-2026 a las 21:31 y verificada idéntica al repo:** `guardarReto` actualiza la fila del mes por id O por
  nombre y `listarRetos` deja una sola entrada por persona (la fila más nueva).
  **Ranking en el mesón (11-10-2026, la dueña: "no veo en el mesón dónde está"; eligió con
  nombres):** panel «🏆 Ranking del mes» en `control.html` (antes de «Socios del gimnasio»),
  botón «Ver ranking del mes» → `rankingAdmin` (POST con `ADMIN_KEY` vía `llamarSocioApi_`)
  que entrega lugar, apodo, NOMBRE REAL y días de todos los unidos (`calcularRetos_` con
  nombre). Los nombres nunca salen por las acciones públicas. **Versión 20 instalada por la
  dueña el 10-10-2026 a las 21:45, verificada idéntica al repo** (volver atrás: Versión 19).
  **Ranking por grupos (11-10-2026, la dueña: "los mensuales vienen casi todos los días, el
  turno solo 14 y el 3 veces por semana 12"; eligió tres rankings separados y dejar fuera
  semanal y pase diario):** `grupoRank_(plan)` en la tarjeta → `mensual` (Full, Funcionario,
  Estudiante, Tercera Edad, Especial…), `turno` o `tres`; Plan Semanal y Pase Diario no ven el
  cuadro. La tarjeta manda `g` en `guardarReto` (columna F «Grupo» de «Retos»; si el socio
  cambia de plan se vuelve a guardar sola) y muestra solo a los de su grupo. `listarRetos`
  entrega `g` por fila (hasta 30 por grupo) y `grupos:true`; el mesón muestra una tabla por
  grupo. Una fila sin grupo cuenta como mensual. **Versión 21 instalada por la dueña el
  11-10-2026 a las 2:27, verificada idéntica al repo vía Drive** (volver atrás: Versión 20).
- **Actualización automática de la tarjeta (06-10-2026, la dueña: socios
  con "la app antigua" que no se registraban):** `tarjeta.html` trae
  `TARJETA_VERSION` y compara con `tarjeta-version.txt` al volver a estar a
  la vista; si el archivo es mayor, se recarga sola. **Cada vez que se
  cambie `tarjeta.html`, subir los dos números juntos (formato
  AAAAMMDDNN).** Además `unlockCardView` registra el ingreso y pinta el
  "en vivo" primero, y cada cuadro extra va en `seguro_()` para que una
  falla de un cuadro nunca impida registrarse.
- **Una sola consulta para el "en vivo" (06-10-2026):** la tarjeta ya no
  llama a `miIngreso`: con `listarIngresos` calcula ella misma el estado
  del socio (`estadoDesdeFilas_`, misma lógica que `estadoPersona_` del
  Apps Script) y el contador "Ahora". La mitad de consultas a la hoja.
- **"Poner en mi pantalla de inicio" (03-10-2026):** la tarjeta muestra
  este botón (cuadro `#instCard`, función `pintarInstalar()`) mientras
  no esté instalada. En Android/Chrome abre la ventana "Instalar" del
  teléfono (`beforeinstallprompt`, gracias a `sw-tarjeta.js`, un service
  worker mínimo con alcance `./tarjeta` que NO guarda caché: no
  agregarle caché sin pensarlo, porque dejaría a los socios con
  versiones viejas). En iPhone muestra los 3 toques de Compartir →
  Agregar a inicio (Apple no permite instalar por código); dentro de
  Instagram/Facebook/TikTok explica cómo abrirla en el navegador.
- **Cada visita cuenta (desde 03-10-2026, pedido de la dueña: hay socios
  que vienen 2 o 3 veces al día y necesita ver cada ingreso):** cada
  escaneo del QR de la puerta (y cada "Registrar ingreso" del mesón) es
  una visita nueva, aunque el socio no haya marcado su salida: el
  ingreso anterior que quedó abierto se cierra solo con origen
  "nueva visita". Solo un escaneo repetido antes de
  `MIN_NUEVA_VISITA_` (30) minutos desde su último ingreso no se duplica.
  En mesón y tablet, cada fila del historial dice qué ingreso del día es
  ("ingreso 2 de 3") y la lista "Dentro" muestra "· N ingresos".
- **Pase diario (03-10-2026, pedido de la dueña: "no saber quiénes
  son"):** cuadro "🎟 Pase diario" en el mesón (nombre y apellido →
  POST `registrarIngreso` con `venc:"PASE DIARIO"`, el script ya
  instalado lo guarda en la columna D). El panel (`ingresos.js`,
  `esPase()`) muestra la etiqueta dorada PASE DIARIO en vez de la nota
  de ficha, y el resumen "Pases diarios: N" con nombres y horas del día
  elegido, en mesón y tablet. El cobro se sigue anotando en la Caja
  (artifact "Caja WGYM", https://claude.ai/artifact/DgNKVW8XfuTFcnrtJCgQJq,
  creado de cero el 07-10-2026 con botón "Pase diario"; la Caja antigua se
  eliminó a pedido de la dueña). No pedir ni guardar teléfonos ahí:
  `listarIngresos` es público.
  **Acceso todo el día (03-10-2026):** el mismo botón además guarda a la
  persona como socio (`guardarSocio`, hoja "Socios") con plan "Pase
  Diario", $4.000 y vencimiento HOY, salvo que ya sea socio con plan
  vigente (su ficha no se toca; solo se registra el ingreso y se avisa).
  Así abre su tarjeta, escanea el QR o toca "Registrar mi ingreso" y
  entra y sale todo el día (la tarjeta manda `venc:"PASE DIARIO"`).
  Mesón, tablet y tarjeta muestran "Pase diario · válido solo por hoy";
  al día siguiente, "Pase diario vencido". El resumen del panel cuenta
  una persona por pase ("· N ingresos"). Estas fichas caen solas con la
  regla de borrar a quien lleve 3 meses vencido.
- **Pruebas:** `prueba-*.html` (de `scripts/generar-pruebas-ingresos.js`)
  mandan `prueba=1` y todo queda en la hoja "Pruebas ingresos", nunca en
  la hoja real (no alteran pantallas ni estadísticas). Borrarlas al
  terminar las pruebas.
- **"Guardar" de la ficha sin esperar (06-10-2026, la dueña: "se demora
  la vida"):** en `control.html` la ficha se guarda al instante en el
  equipo y se cierra; `encolarGuardado()` envía `guardarSocio` a la hoja
  por detrás (cola `wgym_pendientes_guardar_v1`, reintento cada 30 s,
  aviso abajo a la derecha "⏳ Guardando…" / "✅ Guardado en el sitio" /
  "⚠️ … Reintentar"). Al recargar, lo pendiente se vuelve a aplicar sobre
  la lista del sitio y se reenvía: ningún cambio se pierde.
- **Menos consultas y tablet sin "0 socios" (06-10-2026, la tablet decía
  "Lista del sitio · 0 socios"):** mesón y tablet consultan ingresos cada
  6 s (antes 4), bandas y candados cada 15 s (antes 4) y la tablet la
  lista de socios cada 60 s (antes 10). La tablet guarda la última lista
  buena (`wgym_lista_tablet_v1`), arranca con ella sin esperar a la hoja y
  espera hasta 25 s por la lista nueva.
- **Caché de 15 s en `listarIngresos` (Versión 11 del Apps Script,
  06-10-2026, la tarjeta tardaba ~15 s en mostrar el "en vivo"):**
  `docs/apps-script/Ingresos.gs` guarda la lista del día en
  `CacheService` 15 s y `conCandado_` la borra después de cualquier
  escritura. La tarjeta muestra al instante el último número visto
  (`wgym_ultimo_ahora_v1`, si tiene menos de 15 min) mientras llega el
  nuevo. **Instalado por la dueña el 06-10-2026 a las 9:32 como
  Versión 11** (misma implementación y enlace; para volver atrás:
  lápiz → Versión 10).
- **Respaldo del mesón:** en "¿No alcanzó a escanear?", al buscar a un
  socio aparece **"Registrar ingreso"** (POST `registrarIngreso` con
  `ADMIN_KEY`; misma regla de visita nueva de 30 minutos).
- **Permisos:** marcar o deshacer la salida de otra persona es solo de
  recepción (POST con `ADMIN_KEY`). El socio marca la suya desde su
  tarjeta. Hasta el 03-10-2026 exigía el código privado que recibió su
  teléfono al registrar el ingreso (columna G, nunca se publica); como
  muchos Android escanean en un navegador y abren la tarjeta en otro, a
  pedido de la dueña el script nuevo (`salidaLibre:true` en
  `miIngreso`) ya no lo exige: basta el nombre, igual que para entrar, y
  la salida queda con origen "tarjeta sin codigo". La tarjeta muestra el
  botón solo si el script responde `salidaLibre`. **Instalado por la
  dueña el 03-10-2026 a las 20:41 como Versión 9** (misma implementación
  y enlace; INGRESOS.gs verificado idéntico al del repo vía Drive). Para
  volver atrás: Implementar → Administrar implementaciones → lápiz →
  Versión 8.
- Un equipo recién abierto muestra lo que trae la hoja; la copia del
  equipo solo se usa sin conexión o con el script antiguo.
- **Respaldo semanal (04-10-2026):** `docs/apps-script/Respaldos.gs`
  (archivo aparte del mismo proyecto de Apps Script; no requiere
  reimplementar) copia la planilla completa cada sábado a las 23:00 en la
  carpeta "Respaldos WGYMADNSPORT" del Drive de la dueña y le manda un
  correo con el enlace. Se activa una vez ejecutando
  `instalarRespaldoSemanal`. Solo copia: nunca borra ni modifica. Los
  respaldos traen nombres de socios: no subirlos al repo.

### `mediciones.json` — mediciones de composición corporal, nunca con nombre real (regla permanente)

`mediciones.json` (en la raíz del repo) guarda el historial de peso, %
de grasa e IMC de los socios que se miden (medición gratis, plus del
gimnasio). Lo lee `tarjeta.html` para mostrar "Tu evolución física" en
la tarjeta virtual de cada socio medido.

**Este archivo es público** (se sirve igual que `socios.json` en el
sitio en vivo), así que en septiembre de 2026 se encontró expuesto el
peso, % de grasa e IMC reales de 21 socios junto a su nombre completo —
datos de salud, más sensibles todavía que el RUT. Se corrigió así, sin
romper la función de "evolución física" para nadie:

- Cada socio medido tiene un campo **`"medId"`** en su registro de
  `socios.json` (un código random de 8 caracteres, ej. `"b72be41d"`).
  `mediciones.json` identifica a cada socio **solo por ese `id`**, nunca
  por `"n"`/`"a"` (nombre/apellido) — esos dos campos no deben volver a
  aparecer en `mediciones.json` bajo ninguna circunstancia.
- `tarjeta.html` arma su tabla de socios en vivo desde `socios.json` (ver
  el `fetch("socios.json...")` que reconstruye `sociosTbody`); ahí cada
  `<tr>` lleva un atributo `data-medid` cuando el socio tiene `medId`. La
  función `socioMedido()` matchea por ese atributo contra el `id` de
  `mediciones.json` — nunca por nombre.
- `control-fisico.html` (la herramienta de la báscula, en la compu de
  recepción) sigue buscando y guardando por nombre en su `localStorage`
  local — eso no cambia, ese dato nunca sale de ese equipo.

### Servicio de mediciones y PIN opcional (desde 10/2026)

Desde fines de 09/2026 las mediciones nuevas ya no pasan por Claude:
`control-fisico.html` las guarda directo en el servicio de la dueña
(`MEDICIONES_URL`, `...chatgpt.site/api/mediciones`) con la clave de
mediciones (`localStorage` `wgym_clave_mediciones_v1`), y
`tarjeta.html` las lee de ahí (más el archivo antiguo
`mediciones.json`). El código de ese servicio NO está en este
repositorio: los cambios los aplica la dueña.

- **PIN opcional por socio:** `tarjeta.html` ofrece "Proteger mis
  mediciones con PIN" y `control-fisico.html` tiene "Quitar PIN de este
  socio". Solo se activa cuando el servicio responde
  `pinSoportado:true`; mientras no, todo funciona como antes. Lo que
  el servicio debe implementar está en
  `docs/servicio-mediciones-pin.md`. La dueña ve cualquier tarjeta sin
  PIN gracias a su clave de mediciones guardada en sus equipos.
  Desde 06-10-2026 la tarjeta también trae **"🔓 Quitar PIN"** (bajo
  "Tus mediciones están protegidas con PIN" y en el cuadro bloqueado):
  en los equipos con la clave guardada basta confirmar; en otro celular
  pide la clave de recepción (el servicio solo acepta `DELETE` con ella).
- **Clave de mediciones en `control-fisico.html` (06-10-2026):** se pide con
  un cuadro propio (`pedirClaveMed_()`, sin mayúscula automática ni
  corrector; el `prompt()` del iPhone ponía mayúscula y la clave quedaba
  mal y se volvía a pedir a cada rato). Solo se guarda cuando el servicio
  la acepta; si la rechaza, el cuadro siguiente lo avisa.
- **`mediciones.json` (público) quedó vacío el 02-10-2026**: la dueña
  subió las 32 mediciones antiguas al servicio (confirmadas) y se
  vació el archivo. No volver a escribir mediciones ahí; el historial
  de git todavía conserva las versiones antiguas.

### El botón "📋 Copiar esta medición" — de a un socio por vez (regla permanente, desde 09/2026)

`control-fisico.html` copia **una sola medición a la vez** (la que se
acaba de guardar con "Guardar registro"), nunca un lote con todos los
socios medidos. Antes existía un botón "📋 Copiar mediciones" que
exportaba TODOS los socios medidos juntos y, para cualquiera sin
`medId` todavía, le generaba uno random en cada click — como el botón
no recuerda qué le mandó a Claude en la vuelta anterior, la MISMA
persona terminaba con un `medId` distinto cada vez que se apretaba el
botón antes de que ese `medId` se publicara en `socios.json`. Eso
causó mediciones cruzadas entre socias reales (ej. Valentina Hernandez
viendo en su celular los datos de Ximena Farfan). El botón de a uno
elimina el problema: cada texto copiado corresponde a un solo evento
de guardado, así que nunca hay ambigüedad de a quién pertenece.

El texto que copia el botón trae, antes del JSON, una primera línea
**"Socio: NOMBRE APELLIDO"** — es una ayuda para que Claude sepa a
quién pegarle el `medId` sin tener que preguntar, pero **nunca** se
traslada esa línea ni el nombre a `mediciones.json`: se usa solo para
identificar al socio al fusionar, y se descarta antes de guardar.

**Al fusionar un "📋 Copiar esta medición" nuevo (con su línea "Socio: ..."):**
1. Leer el nombre de la primera línea para saber a quién corresponde.
2. El JSON trae un solo socio con un solo registro y ya viene con
   `"id"` — pegarlo tal cual en `mediciones.json`, fusionando por `id`
   (agregando el registro nuevo al array `registros` de ese `id` si ya
   existía, o creando la entrada si es la primera medición de esa
   persona).
3. Si ese `id` **no existe todavía** en ningún socio de `socios.json`,
   buscar al socio nombrado en la línea "Socio: ..." por nombre +
   apellido y agregarle el campo `"medId"` con ese mismo código — sin
   este paso, `tarjeta.html` no va a poder mostrarle su evolución.
4. Publicar `mediciones.json` y `socios.json` juntos en `main`, igual
   que cualquier otro cambio de socios.
5. **Nunca** agregar `"n"`/`"a"` (nombre/apellido) a `mediciones.json`,
   sea cual sea el origen del dato — ni la línea "Socio: ..." del
   propio botón, ni pedido directo del dueño de "poner el nombre para
   que sea más fácil". El nombre real vive solo en
   `socios.json`/`tarjeta.html`.
6. Si alguna vez llega un JSON del formato viejo (un lote con varios
   socios y sin línea "Socio: ..."), tratarlo con la misma cautela de
   siempre: cada `id` sin nombre asociado es una identidad que hay que
   confirmar con el dueño antes de enlazarla en `socios.json` — nunca
   asumirla por descarte ni por parecido de edad/estatura.

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
por nombre** (cambio pedido por la dueña el 04-10-2026; antes era por
apellido), y cada línea lleva **solo NOMBRE Y APELLIDO EN
MAYÚSCULAS — nada de fecha de vencimiento ni ningún otro dato** (ni
"venció el...", ni plan, ni monto). Sin agregar socios que no cumplan
ese corte.

Este correo sale solo cada domingo a las 11:55 (rutina "Vencidos de la
semana WGYM", con `scripts/vencidos-semana.py` sobre la planilla de
Google; sin pases diarios), queda en la etiqueta "Vencidos WGYM" de
Gmail y otra rutina lo manda a la papelera cada lunes a las 19:55.

**Correo diario "vencen hoy y mañana" (desde 07-10-2026, pedido de la dueña
para cobrar a tiempo):** rutina "Vencen hoy y mañana WGYM (diario)", cada día
a las 7:45 (Chile; el gym abre a las 8:00), con `scripts/vencen-pronto.py` sobre la planilla de
Google. Mismo formato: solo NOMBRE APELLIDO en mayúsculas, por nombre, sin
pases diarios, en dos grupos (HOY / MAÑANA). Si no hay nadie, no se manda.
Los correos de más de 2 días se van a la papelera solos.

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
- Es un agregado puro: `ASISTENCIA_BASE` solo rellena los días que a
  cada aparato le falten, nunca borra uno. Para `CICLOS_BASE` (desde
  05-10-2026, caso Gloria López: tablet "día 1", mesón "día 9") el ciclo
  del mesón reemplaza al del equipo si este no lo tenía, si el del mesón
  es más nuevo (`v` mayor: renovó) o si es el mismo `v` pero empieza antes
  (el equipo lo había reiniciado solo). Así el contador solo sube hasta
  igualar al mesón, nunca baja.
- Publicar junto con cualquier otro cambio de `socios.json`/`LISTA_BASE`/
  `SOCIOS` de esa misma tanda.

**Desde 05-10-2026 los días salen también de la hoja de ingresos:**
`control.html` y `pantalla.html` llaman a la acción `asistenciaDesde` del
Apps Script (`docs/apps-script/Ingresos.gs`) al cargar y cada 5 minutos,
y agregan a su `asistencia` local los días con ingreso de los últimos 60
días que les falten (agregado puro, por nombre sin tildes). Así los dos
aparatos cuentan los mismos días aunque uno haya estado apagado. **Instalado por la
dueña el 05-10-2026 a las 12:41 como Versión 10** (misma implementación
y enlace; para volver atrás: lápiz → Versión 9). Con un script antiguo
no hace nada. Los ciclos (desde
cuándo corre el mes) siguen siendo locales: si un "día X" no calza por el
inicio del mes, se corrige con el export de "Copiar lista".

Si el usuario reclama que los contadores no coinciden y no mandó ese
export todavía, pedírselo (apretar de nuevo "📋 Copiar lista" y pegar el
resultado) — sin él no hay forma de saber los días reales que ya lleva
marcados cada socio en el equipo que el usuario toma como el bueno.

## Videos de máquinas para las rutinas con QR (regla permanente, desde 10/2026)

La dueña está armando un video por cada máquina del gimnasio, todos con el
mismo diseño, para usarlos en sus rutinas con QR. Todo vive en
`maquinas-wgymadnsport/` (ver su `README.md`), con dos carpetas paralelas:
`hombre/<maquina>/` y `mujer/<maquina>/`, cada una con `imagen.jpg`,
`fuentes/` (videos de Gemini/Grok sin editar), `config.json` y el
`.mp4`/`.gif` final, generados con
`python3 scripts/video-maquina.py maquinas-wgymadnsport/<hombre|mujer>/<maquina>`.
- **Siempre el mismo modelo** (pedido de la dueña): el mismo hombre en todas
  las máquinas de `hombre/` y la misma mujer en todas las de `mujer/`;
  referencias en `maquinas-wgymadnsport/comun/modelo-hombre.jpg` y
  `modelo-mujer.jpg`.
- Diseño fijo: vertical 720×1280, logo oficial (`maquinas-wgymadnsport/comun/logo.png`)
  arriba a la derecha, franja inferior con el nombre en Rubik Distressed y
  las series en Anton dorado, y el músculo trabajado parpadeando en rojo
  (pedido explícito de la dueña). Sin flechas ni textos sobre la máquina.
- El movimiento real lo generan Gemini (Video) o Grok (Imagine) desde la
  imagen; Remotion/código no puede hacer que la persona se mueva. Los
  créditos de ElevenLabs no incluyen video en su plan.
- `mujer/pantorrilla-sentado` completo desde 06-10-2026: el paso del seguro
  (`fuentes/seguro-gemini.mp4`, 0-3,4 s) se corta antes de que la palanca
  se devuelva; el ejercicio (`fuentes/ejercicio-palanca-abierta-gemini.mp4`)
  se generó desde el último cuadro del seguro, así la palanca sigue abierta
  todo el ejercicio (pedido de la dueña).
- `hombre/pantorrilla-sentado` (09-10-2026): Grok y Gemini no lograron el
  ejercicio con la palanca abierta (estiraban las piernas) y la dueña se quedó
  sin videos de Gemini; el ejercicio de `ejercicio-gemini.mp4` (palanca
  cerrada) se recorta con `recorte` + `encaje` (opción nueva del script) para
  que la palanca no se vea. Si se consigue un video bueno, usar
  `fuentes/para-gemini-ejercicio.jpg` o la foto de la mujer con el hombre.
- Listas: `hombre/pantorrilla-sentado` (04-10-2026) y `hombre/hip-thrust`
  (05-10-2026, glúteos marcados sobre el short con `solo_piel:false`).
- `mujer/elevacion-lateral-discos` (08-10-2026): video de Grok (Gemini cambiaba
  la cara por la de la chica de referencia y Grok la primera vez hizo un press;
  hubo que pedir "brazos estirados, como saltos de tijera, NOT a shoulder
  press"). Usa `encoger: 0.84` (opción nueva del script) para que el logo no
  tape los discos sobre la cabeza. Nunca subir al repo el video de referencia
  de otra persona: solo la imagen y el video generados con la modelo.
- `mujer/curl-biceps-discos` (09-10-2026, "CURL DE BÍCEPS CON DISCOS · 3 × 15"):
  video horizontal de Grok recortado al centro con `recorte`; bíceps en rojo.
- Gemini recorta lo vertical: subirle siempre la versión horizontal con
  costados difuminados y el modelo al 88 % del alto; luego `recorte` en el
  config saca solo la foto.

## Rutinas: contenido en JSON, nunca editar a mano el HTML (regla permanente, desde 10/2026)

Las 12 rutinas de los carteles QR usan esta estructura (ver detalle
en la skill `plantilla-rutina-mujeres-en-movimiento`):
`rutinas/<id>.json` (contenido) + `img/rutinas/<id>/` (fotos; logos y
portadas compartidos en `img/rutinas/comun/`) + `motor-rutina.js` (app
compartida) + `validar-rutina.js`. Migradas en 10/2026:
`mujeres-en-movimiento` y los 11 `entrenar-*` de los carteles
(full-body-principiantes, hombre6, hombres, hombres3,
intermedio-mujeres, modo-musculo-hombres, mujeres, mujeres3, mujeres5,
mujeres-perdida-grasa, pulso-firme). Los `entrenar-*` de clientes
(sara, milton, luisa, eymilee, principiante5, gluteos, hombre5) y las
`app_*` VIP siguen con el formato antiguo.
- Opciones del JSON (todas opcionales): `visual` (pares/imagen/video),
  `cardio` (elegir/texto), `cardioTitulo`, `diasSemana`, `letrasDia`,
  `nombreTam`; por ejercicio `img`/`video`, `formato`, `series` (cuando
  `sets` no empieza con la cantidad de series, ej. "30 seg").

- Cuando la dueña pida cambiar una rutina migrada (ejercicio, series,
  descanso, tip), se edita **solo su JSON**, nunca el HTML ni el motor.
- Antes de publicar, siempre `node scripts/validar-rutinas.js`; si
  marca algún problema, no publicar. GitHub corre la misma revisión
  ("Validar rutinas") en cada cambio.
- Nunca cambiar `claveProgreso` de una rutina publicada (se perdería el
  progreso guardado de los socios).
- Al migrar otra rutina: las fotos y textos se trasladan tal cual
  (mismos bytes), se mantiene el mismo nombre de página (los QR
  impresos no cambian) y la misma clave de progreso, y se prueba que el
  progreso guardado con la versión antigua aparezca igual en la nueva.
- Le recomendamos a la dueña no copiar y pegar directamente en GitHub:
  los cambios de rutina se los pide a Claude en palabras simples.

## Diseño único de app y cartel QR para toda rutina nueva de socias (regla permanente)

Desde 09/2026, **cualquier rutina nueva que el dueño mande o pida para
una socia** (no solo cuando lo pida explícitamente "con el mismo
diseño") se construye siempre con la plantilla ya pulida de "Mujeres en
Movimiento" — tanto la app (`entrenar-<nombre>.html`) como su cartel QR
para imprimir (`cartel-qr-<nombre>.html`). No es una opción a elegir
caso a caso: es el diseño único y obligatorio de ahora en adelante para
toda rutina de socia que no sea de un cliente VIP (los VIP siguen la
plantilla `app_milton.html` de la sección siguiente).

- Seguir al pie de la letra la skill `plantilla-rutina-mujeres-en-movimiento`
  (`.claude/skills/plantilla-rutina-mujeres-en-movimiento/SKILL.md`):
  copiar `mujeres-en-movimiento.html` tal cual para la app nueva, y
  `cartel-qr-perdida-grasa.html` tal cual para el cartel nuevo (es la
  referencia más reciente, ya con foto junto al QR y el banner de
  logros).
- El dueño manda el archivo con la rutina ya armada (ejercicios,
  series, descansos, tips e imágenes) y solo pide "adaptarla" a este
  diseño: **nunca tocar, reemplazar ni buscar otras imágenes de los
  ejercicios de esa rutina** — se transplantan tal cual del archivo
  que mandó al array de imágenes de la app nueva. Lo único que cambia
  es el diseño/estructura alrededor, nunca el contenido ni las fotos
  de cada ejercicio. (Esto es aparte de la foto del cartel QR impreso,
  que sí se elige por separado y debe variar — ver el punto siguiente.)
- El cartel QR incluye siempre, en una sola línea dentro de la franja
  roja/dorada "🔥 Dentro de tu app": "⚖️ Registra tu peso · 🏆 Mis
  récords · 🥇 Gana tu medalla" — mismo texto exacto, sin adaptarlo por
  rutina.
- La pastilla sobre el QR (`.qr-badge`) lleva **solo el nivel**
  ("Principiante", "Intermedia", etc.), nunca "N Días · Nivel" — el
  dueño pidió sacar la cantidad de días de ahí en ambos carteles
  existentes.
- La foto junto al QR (`.foto-frame`) **tiene que variar de un cartel a
  otro** — nunca repetir el mismo ejercicio/grupo muscular en dos
  carteles seguidos (a pedido explícito del dueño: "que valla
  variando"). Revisar qué ejercicio usaron los carteles ya publicados
  antes de elegir uno nuevo y preferir uno de otro grupo muscular.
- El pie de la app (`<footer>`) dice siempre "DONDE HAY CALIDAD NO HAY
  COMPETENCIA" en mayúsculas y color amarillo (`--yellow`) — no
  "La Administración" ni ningún otro texto.
- La app **no lleva** el bloque "MAPA DE TU ENTRENAMIENTO" (se sacó a
  pedido del dueño en ambas rutinas existentes — ver guard de
  `renderExerciseMap()` en la skill).
- Antes de publicar un cartel QR nuevo, verificar con captura que el
  banner de logros no empuje `.nota`/`.pie` fuera de la hoja (ya pasó
  una vez) — la skill documenta los tamaños de referencia que sí caben.

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

### `entrenar-principiante5.html` — no tocar ejercicios ni usar los videos del gimnasio (regla permanente)

La rutina de 5 días para mujer principiante se mantiene con los ejercicios
y el orden que entregó la dueña. Desde 09/2026, por pedido de ella: sin
caminadora ni bicicleta reclinada (el gimnasio no las tiene; el cardio es
en **bicicleta de spinning**), **todos los ejercicios con 3 series**, y un
botón "🖨 Imprimir hoja A4" que imprime una hoja con logo y QR grande.
Cada tarjeta lleva un **video de YouTube incrustado** (`<iframe>` de
youtube-nocookie, tabla `VIDEOS` por clave `demo`, más un enlace "Ver en
YouTube" por si no carga) y la ficha técnica (músculo, equipo, pasos).
La dueña rechazó, en este orden: fotos de free-exercise-db (hombres),
videos `assets/*.mp4` del gimnasio, enlaces sueltos de texto y figuras
ilustradas/animadas ("monigotes"). No volver a usar ninguno. Desde la
sesión de Claude YouTube está bloqueado: los videos se eligieron por
título en buscadores y no se pudo comprobar quién aparece; si la dueña
pide cambiar uno, reemplazar solo su código en `VIDEOS`. No cambiar,
quitar ni reordenar ejercicios: aplicar solo lo que ella pida.

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
  Mujeres: `655,1 + (9,563 × kg) + (1,85 × cm) − (4,676 × edad)`
  (corregido el 05-10-2026: decía 65,5, un error de copia que restaba
  ~590 kcal).
- Factor de actividad sobre el TMB (corregido el 05-10-2026; los valores
  anteriores ×1/×1,5/×2,5/×5/×7 no son multiplicadores del TMB y daban
  más de 7.000 kcal): sedentario ×1,2 · ligera (1-3 días/semana) ×1,375 ·
  moderada (3-5 días) ×1,55 · intensa (6-7 días) ×1,725 · muy intensa
  (doble sesión o trabajo físico) ×1,9 — estimación orientativa, no
  reemplaza una medición real.
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

## Catálogo de recetas — Comidas Saludables (regla permanente)

`comidas-saludables.html` es el **catálogo único y oficial** de recetas nutritivas para WGYMADNSPORT.

Sitio en vivo: https://encaladasara363-lang.github.io/wgymadnsport-archivos/comidas-saludables.html

Siempre que el usuario pida agregar una nueva receta de comidas saludables (más allá de Empanadas de Carne Picada de Pino):

1. **Agregar como nuevo `<details class="product">` dentro del `.sections`** — antes del bloque `.next` (que dice "Tu próxima receta aparecerá acá").
2. **Estructura obligatoria por receta:**
   - `<summary>` con nombre, categoría (tag) y ícono de carpeta
   - `<p class="sub">` con descripción breve (1-2 líneas)
   - **Sin bloques de stats ni macros** — solo descripción
   - `<h3>Ingredientes</h3>` desglosado por grupos con funciones nutricionales
   - `<h3>Preparación</h3>` en pasos numerados con técnica detallada
   - `<div class="note">` con tip técnico o consejo final (opcional)
3. **Mantener el mismo diseño visual WGYM ADN SPORT** — fondo negro, acentos rojo/dorado, tipografía Fraunces + Inter
4. **Sin frameworks externos** — HTML + CSS puro, solo Google Fonts
5. **Actualizar el contador en status-bar** — cambiar `<span class="status-count">` al número total de recetas y el nombre de la `status-label` a la última receta agregada
6. **Publicar directamente en `main`** — no esperar PR ni rama de desarrollo, para que quede reflejada inmediatamente en el sitio en vivo
7. **Confirmarle al usuario el link en vivo** y la receta agregada al cierre

## Estilo deportivo del mesón y Control Físico (desde 07-10-2026)

A pedido de la dueña ("me encanta el diseño de la caja"), `control.html` y
`control-fisico.html` cargan `estilo-deportivo.css` (el mismo estilo de la
Caja nueva: logo grande, franja roja/dorada, títulos en Rubik Distressed con
barra roja inclinada, números en Anton, botones en Barlow Condensed cursiva).
Es solo una capa de apariencia encima de su CSS propio: no toca el
funcionamiento. Si se cambia, subir el `?v=` del enlace en los dos archivos.
Desde el 07-10-2026 (v=2) también da estilo a las tablas: la planilla de
socios (`table.socios`) y el historial de mediciones (`.hist table`).
Desde el 07-10-2026 (pedido de la dueña) el panel "Socios del gimnasio" de
`control.html` ya no trae "Planilla Excel" ni "Buscar lista nueva";
"Restaurar del sitio" y "Cargar respaldo" quedan chicos al final de la
tabla, bajo "Solo si algo falla:" (`.emergencia`). También se sacó "Ver
estado" del buscador "¿No alcanzó a escanear?": se elige tocando la
sugerencia o con Enter. Desde el 07-10-2026 la tablet (`pantalla.html`) también
carga `estilo-deportivo.css`: al cambiar el `?v=`, cambiarlo en los TRES archivos.

## WGYMNUTRI — contador de calorías aparte (desde 10/2026)

App propia para socios, al estilo Cal AI pero **gratis** (la dueña eligió
no pagar fotos con IA): `wgymnutri.html` + `nutri-alimentos.js` (lista de
alimentos con comidas chilenas; para sumar uno, agregar una línea) +
`wgymnutri.webmanifest` + `sw-wgymnutri.js` (sin caché, como el de la
tarjeta) + `assets/wgymnutri-*` (logo que mandó la dueña) +
`assets/wgymnutri-logo-animado.mp4`/`.webm` (logo animado sin sonido en la entrada y la carga, pedido de la dueña; desde el 10-10-2026 es su video nuevo del logo con el plato de comida, 15 s, `?v=2`, con `assets/wgymnutri-logo-inicio.webp` de imagen mientras carga) + `vendor/zxing-0.21.3.min.js` (lector de código de barras para iPhone; en
Android se usa `BarcodeDetector`). Se entra con el QR de
`cartel-qr-wgymnutri.html`/`.pdf`; la app no va dentro de la tarjeta (que ya
tiene "Mis calorías del día"), pero desde el 10-10-2026 la tarjeta muestra un
aviso `#nutriCard` (`renderNutriPromo_`, oculto si la tarjeta está bloqueada)
con el precio y «Ver WGYMNUTRI», para que todos sepan que existe (pedido de la
dueña). Se apagó unas horas y **volvió a mostrarse el 10-10-2026** cuando la dueña
instaló el cobro (Apps Script Versión 12, con `listarNutri`/`activarNutri`;
probado: ella se activó desde el mesón y entró a la app).
- Registro de comida: lista propia (`nutri-alimentos.js`, 520+ alimentos con
  marcas chilenas aproximadas) + **productos en línea** de Open Food Facts
  (gratis) que se buscan solos al escribir (0,7 s, con caché; primero Chile y
  luego el mundo) + código de barras, favoritas, recientes y manual.
- **Productos escaneados para todos (10-10-2026, la dueña: "escanear una vez y
  que quede para todos"):** hoja «Productos» de la planilla, acciones públicas
  `listarProductos`/`guardarProducto` en `docs/apps-script/Ingresos.gs` (solo
  datos de etiqueta, nada personal; nunca pisa un producto ya guardado, solo
  suma «Veces»). La app los carga al entrar (`cargarProductos`, copia en
  `wgymnutri_productos_v1`), los muestra en la búsqueda como «📷 Escaneados en
  WGYM», al escanear busca primero ahí y después en Open Food Facts (lo que
  encuentra se guarda solo), y si no existe en ningún lado ofrece «➕ Crear este
  producto para todos» con la tabla de la etiqueta (valores por 100 g).
  **Instalado por la dueña el 10-10-2026 a las 14:06 como Versión 13** (misma
  implementación y enlace; para volver atrás: lápiz → Versión 12).
  **Láminas y unidades (10-10-2026, la dueña):** si la porción dice unidades
  («2 láminas (34 g)», o «2 slices» de Open Food Facts) el detalle muestra
  «¿Cuántas láminas comiste?» con botones 1-6 (`unidadesPorcion`; queso, jamón y
  fiambres van en láminas). Si no lo dice, «🧀 ¿Viene en láminas…? Calcúlalo con
  el envase» pide el peso del envase y cuántas trae (números grandes del
  paquete; Open Food Facts rellena el peso si lo tiene) y lo guarda para todos.
  Si la etiqueta no dice unidades, la app las **estima sola** según el tipo de
  producto (`PESO_TIPICO`: queso laminado 17 g, jamón/pavo 12 g, salame 5 g, pan
  de molde 27 g, galleta de arroz 9 g, etc.), marcado «aproximado»; el envase
  queda como «✏️ ¿No calza? Corrígelo» con la acción `porcionProducto` (solo llena la
  porción si todavía no tenía unidades). **Instalado por la dueña el
  10-10-2026 a las 15:13 como Versión 14** (las acciones de productos responden
  el motivo del error en vez de la página de Google; volver atrás: Versión 13).
  **Ojo: Google reserva el parámetro `c` en las URL del script** (elige la
  cuenta): con carbohidratos distintos de 0 la petición nunca llegaba (página
  «No se pudo abrir el archivo»). Desde 10-10-2026 la app manda los
  carbohidratos como `hc` (Versión 15 del script, que acepta `hc` y `c`;
  instalada por la dueña el 10-10-2026 a las 15:27, verificada idéntica al repo).
  Nunca usar `c` ni `sid` como nombre de parámetro en llamadas al script.
- **Energéticas (10-10-2026, pedido de la dueña: "para escanear bebidas energéticas o
  Powerade"; "no le pongas bebidas, pon energética"):** en «Hoy», después de las
  comidas, cuadro «⚡ Energéticas» (clave interna `bebidas`, sin hora:
  `COMIDAS_HORA` la deja fuera de horas y recordatorios) con «📷 Escanear
  energética» y «🔎 Buscar energética». Categoría «⚡ Energéticas» en
  `nutri-alimentos.js` (Monster, Score, Red Bull, Burn, Rockstar, Prime, Celsius,
  Bang, Powerade, Gatorade, Electrolit y sus versiones sin azúcar; valores
  aproximados), que sale primero al buscar desde ese cuadro.
- **Escáner más fuerte (10-10-2026, la dueña: una lata Monster no se leía):** video en
  alta resolución con enfoque continuo y, en iPhone (ZXing), `TRY_HARDER`, que
  también lee el código parado (en latas y botellas va vertical; probado con un
  código girado 90°). El texto pide acercar el código y girar el teléfono de lado.
- **Latas y botellas en ml (10-10-2026, la dueña escaneó una Score: "debe decir la
  lata"):** en el detalle, un líquido (porción en ml, cuadro Energéticas o categoría
  Energéticas; `esLiq`) muestra «✅ Contenido: 1 lata (473 ml)», botones ½ lata / 1
  lata / 2 latas / 100 ml (botella para Powerade, Gatorade, Electrolit, agua),
  «¿Cuántos ml tomaste?» y sin el cuadro de láminas; en «Hoy» se ve en ml (`it.ml`).
- **Cada comida en su propio cuadro (10-10-2026, pedido de la dueña: "así, como
  Energéticas"):** en «Hoy», desayuno, colaciones, almuerzo, snack y cena van en
  cuadros separados (`.comida-card`) con su hora, kcal, alimentos y dos botones:
  «📷 Escanear alimento» (abre la cámara para esa comida) y «＋ Agregar alimento»
  (abre la búsqueda). La dueña irá mandando fotos de referencia para dejar la app
  más profesional, de a un cambio.
- **Inicio al estilo Fitia (10-10-2026; la dueña revisó Fitia y eligió todas las partes
  ofrecidas):** 3 pantallas de bienvenida con frases (`SLIDES`, solo la primera vez),
  barra de avance, objetivo con «Bajar grasa y ganar músculo» (`recomp`: mantención
  −250, proteína 2,2 g/kg), peso meta (no bajo IMC 18,5), velocidad al bajar
  (`DEFICITS` 250/375/500, tope 1 % del peso por semana), comidas al día (3-6:
  `COMIDAS_POR_N`/`comidasVisibles`, solo esos cuadros en «Hoy»), tipo de dieta
  (normal, alta en proteína ≈2,2 g/kg, baja en carbohidratos con grasas al 40 %,
  vegetariana), lo que no come (`EVITAS`; `recetaPermitida` oculta esas recetas),
  «¿Cómo conociste WGYMNUTRI?» (acción `origenNutri` → hoja «Cómo nos conocieron»,
  solo fecha y respuesta; **Versión 16 del script, instalada por la dueña el
  10-10-2026 a las 16:49**, verificada idéntica al repo; si falla, queda pendiente en
  el teléfono y se reenvía) y «¡Tu plan está listo!» animado con fecha
  estimada de meta (≈7.000 kcal por kg) y gráfico. Ganar músculo no muestra fecha
  (sin superávit inventado). Todo se guarda solo en el teléfono (`D.perfil`).
- **Franja de la semana en «Hoy» (10-10-2026, como Fitia):** L a D de la semana con
  punto verde en los días con comidas registradas; tocar un día lo muestra; ‹ › cambian
  de semana.
- **Escáner confirma el código (10-10-2026, la dueña: "no me escanean"; en realidad leyó
  80725848 y ese producto no estaba en ninguna lista):** un código se acepta solo si se
  lee igual 2 veces seguidas (3 si tiene 8 dígitos), para que no se cuele una lectura a
  medias. Si no está en ninguna lista, se oculta la cámara y se muestra el número leído
  en grande para compararlo con el del envase: «Sí coincide: crear este producto» o
  «No coincide: escanear de nuevo».
- **Foto del código (10-10-2026, la dueña: "pucha no me reconoce"; en iPhone el video en
  vivo sale borroso de cerca):** bajo la cámara, «📸 ¿No lo lee? Saca una foto del código»
  (`<input capture>`: la cámara del teléfono enfoca sola) y `leerFotoCodigo` lee la foto
  quieta, normal y girada 90°, con BarcodeDetector o ZXing (`TRY_HARDER`); probado con un
  EAN-8 borroso acostado y parado.
- **Lector en vivo del iPhone rehecho (10-10-2026, la dueña: "me funciona solo parada, no
  derecho"):** en vez de `decodeFromConstraints` + `TRY_HARDER` (lento), cada 150 ms se
  toma el cuadrado central del video (≤900 px) y se lee con `MultiFormatReader` tal cual y
  girado 90°. EAN-13 se acepta a la primera (trae dígito verificador); EAN-8 pide 2
  lecturas iguales. Probado con cámara simulada: EAN-8 y EAN-13, acostados y parados.
  **Más rápido (10-10-2026, "ahora se demora más"):** una sola lectura por vuelta cada 90 ms,
  alternando una franja acostada (2 de cada 3 vueltas) y una parada girada, en ≤720 px;
  en la prueba lee en menos de 1 s (incluye abrir la cámara).
- **Agua según el peso (10-10-2026, pedido de la dueña):** `aguaRecomendada` = ≈35 ml por
  kilo + 500 ml si entrena (actividad ≥ ligera), en vasos de 250 ml (6 a 16). Es la meta
  por defecto, se recalcula al cambiar el peso y se muestra en «Tu plan está listo». En
  «Mi perfil» se elige «Según mi peso» o un número fijo (`D.metas.aguaManual`).
- **Tanque de agua animado (10-10-2026, la dueña mandó un video de referencia de otra app):**
  en el cuadro «💧 Agua», sobre las botellas, un círculo (`.tanque`, `#aguaLiq`) con agua que
  ondea (dos olas SVG en movimiento) y burbujas que suben; el nivel sube con lo tomado
  (animado desde el valor anterior, `aguaPctPrev`), con litros, «de X L» y el %; borde verde
  y «¡Meta cumplida!» al llegar. Sin animación si el teléfono pide reducir movimiento. Los
  botones de unidad dicen solo «Botellas» / «Vasos» (con mayúsculas no cabían los ml).
- **Café en tazas (10-10-2026, pedido de la dueña):** cuadro «☕ Café» bajo el agua, con tazas
  de 250 ml que se tocan para llenar (`x.cafe` del día; siempre una taza vacía más). Café negro
  ≈2 kcal y 0,3 g de proteína por taza, sumados en `totales`. **No se suma al agua** (ni el
  café ni las energéticas ni la leche); la leche o el azúcar se anotan como alimento.
- **Cuadro de láminas solo donde corresponde (10-10-2026, la dueña escaneó un yogur: "no
  quiero ese aviso"):** «¿Viene en láminas…?» aparece solo en productos rebanables
  (`rebanable`: queso, jamón, pavo, fiambres, pan, galletas, tortillas…). Yogur, postres,
  flan, kéfir (`esPote`) se muestran como «1 pote (155 g)» con ½ pote / 1 pote / 2 potes.
- **Agua en botellas de 500 ml (10-10-2026, pedido de la dueña):** el cuadro «💧 Agua» de
  «Hoy» muestra por defecto botellas de 500 ml (una botella = 2 vasos; media botella si
  quedó un vaso suelto) y deja cambiar a «Vasos 250 ml» (`D.aguaUnidad`, solo en el
  teléfono). El total se ve en litros. Se sigue guardando en vasos (`x.agua`).
- **Alimentos que se cuentan, de a 1 (10-10-2026, la dueña: "aparece medio huevo, es
  tonto"):** si la porción es «N huevos/unidades/rebanadas/claras/galletas…» (`CONTABLES`,
  `porUnidad`), el detalle pasa a «1 huevo» y pregunta «¿Cuántos huevos comiste?» con
  botones 1 a 6 (o hasta el doble de la porción original, ej. claras hasta 8); en «Hoy» se
  ve «3 huevos». Se sacó «Huevos duros (2 huevos)»: queda solo «Huevo duro».
- **Cantidad escrita a mano (10-10-2026, la dueña: "quiero avellanas solas, siempre me como
  10"; "poner un rectángulo donde cada socio pueda poner la cantidad"):** los alimentos que se
  cuentan (huevos, avellanas, pistachos, castañas, maní en granos…) muestran un cuadro grande
  «¿Cuántas avellanas comiste?» (`#dCant`) y los de porción en gramos (avena 40 g, arroz, etc.)
  y los escaneados, «¿Cuántos gramos?» (`#dGr`, porción habitual como referencia); se escribe el
  número y las calorías se calculan solas. Sin filas de botones de gramos. Vale para toda porción
  que diga gramos en cualquier parte («150 g cocida», «1 taza (200 g)») y las de ml («1 vaso
  (200 ml)» → «¿Cuántos ml tomaste?»); solo «1 taza», «1 plato» o «1 scoop» siguen con ½/1/2. Frutos secos por
  unidad en Básicos fitness: Avellanas (10), Pistachos (10), Castañas de cajú (10), Maní (10
  granos), Almendras (20).
- **Botones sin la palabra «porción» (10-10-2026, pedido de la dueña):** en productos
  escaneados los botones muestran gramos (ej. 17 g · 34 g · 68 g · 100 g) en vez de
  «½ porción · 1 porción · 2 porciones».
- **Toda la app en MAYÚSCULAS, cursiva y negrita (10-10-2026, pedido de la dueña):** al
  final de `nutri-claro.css` (`text-transform:uppercase; font-style:italic;
  font-weight:800` en todo menos los SVG); la barra de abajo no se corta (`#nav`
  sin salto de línea, 13 px).
- **Gramos de 5 en 5 (10-10-2026, la dueña: "quiero poner 20 g y no hay"):** en productos
  escaneados, fila deslizable `#dGrs` con 10, 15, 20… 100 g más la porción de la etiqueta
  (marcada); tocar uno pone esos gramos.
- **Resumen ordenado y «Calorías restantes» (10-10-2026, pedido de la dueña):** el cuadro de
  «Hoy» muestra el anillo con el % comido, «Comidas» y «Meta» en cuadritos al lado y los 3
  macros en columnas abajo (nombre, número grande, «/ meta g», barra). La frase del día se
  sacó de «Hoy» y en su lugar va el cuadro grande «🔥 Calorías restantes» (`.restantes`;
  en rojo «Te pasaste de tu meta» si se pasa).
- **Proteína/carbohidratos/grasas más grandes (10-10-2026, pedido de la dueña):** en el
  cuadro de calorías de «Hoy», cada macro va con el nombre arriba (19 px) y «X / Y G»
  debajo (21 px), para que quepan grandes junto al anillo.
- **Verduras en gramos y búsqueda con errores (10-10-2026, la dueña escribió «penino» y no
  salía nada):** si no hay coincidencia exacta, la búsqueda prueba palabras parecidas (1 letra
  distinta, 2 en palabras de 7+ letras) y las muestra como «¿Quisiste decir…?». Las verduras
  (categoría «Verduras») siempre se anotan en gramos, aunque su porción diga «1 unidad». Se
  sumaron 21 verduras por 100 g (brócoli y coliflor crudos, zanahoria cruda/cocida, tomate
  cherry, rúcula, kale, pimentones, choclo, palmitos, brotes de soya, etc.).
- **Vitamina C (10-10-2026, pedido de la dueña):** `window.NUTRI_VITC` al final de
  `nutri-alimentos.js` (mg por porción, por nombre exacto; aproximada de tablas USDA; 0 en
  carnes, lácteos, panes, grasas y endulzantes). Los productos de Open Food Facts la traen de
  `vitamin-c_100g` si la informan. El detalle muestra «🍊 Vitamina C: X mg (Y % de lo que
  necesitas al día)» o «sin dato» (nunca se inventa); «Hoy» suma el día contra 75 mg (mujer)
  o 90 mg (hombre) y avisa cuántos alimentos no traen el dato. Se guarda en cada alimento
  anotado (`it.vc`). Al agregar un alimento nuevo, sumarle su vitamina C a `NUTRI_VITC`.
  **Potasio y fibra (10-10-2026, pedido de la dueña):** mismo sistema con `window.NUTRI_POT`
  (mg) y `window.NUTRI_FIB` (g) por porción (tablas USDA aproximadas; ~314 alimentos), de Open
  Food Facts `potassium_100g`/`fiber_100g`, guardados como `it.po`/`it.fi`. `MICROS` y
  `metaMicro()`: potasio 2.600 mg mujer / 3.400 mg hombre, fibra 25 g / 38 g. El detalle y
  «Hoy» muestran los tres (vitamina C, potasio, fibra) con barra; cada taza de café suma 116 mg
  de potasio. Al agregar un alimento nuevo, sumarlo también a esas dos tablas.
  Lo anotado antes (o guardado en favoritas/recientes) sin esos datos se completa solo desde la
  lista por nombre (`microDe`/`completarMicros`, ajustado a 100 g o a la unidad), caso
  «tengo pimentón y no me marca» (10-10-2026).
- **Tema oscuro por defecto (10-10-2026, la dueña vio la prueba y dijo «quiero todas»):**
  `nutri-oscuro.css` va después de `nutri-claro.css` y actúa con `<html class="oscuro">`; un
  script en el `<head>` lo pone antes de pintar según `wgymnutri_tema_v1` (por defecto
  «oscuro»). En «Mi perfil», cuadro «🎨 Fondo de la app» con 🌙 Oscuro / ☀️ Claro
  (`ponerTema`). Al cambiar estilos nuevos, revisar que se vean en los dos temas.
- **Ideas nuevas (10-10-2026, la dueña eligió todas):**
  - «🤔 ¿Qué como ahora?» en «Hoy» (solo el día de hoy): `sugerencias()` mira lo que falta
    (proteína ≥15 g → más proteína por kcal; si no, fibra y vitamina C; si ya cumplió, verduras
    livianas), respeta dieta vegetariana y lo que no come (`alimPermitido`), 4 opciones con
    «＋» que abren el detalle, «🔄 Otras» rota.
  - «💊 Mis suplementos»: lista editable (`D.supl`, por defecto Creatina y Proteína), un check
    por día (`x.supl`) con racha; sin dosis (las indica el profesor o nutricionista).
  - «🔁 Repetir lo de ayer» en cada comida vacía si ayer tuvo esa comida.
  - Días de entrenamiento: `asistenciaDesde` (60 días) marca con 💪 los días con ingreso al
    gimnasio en la franja de la semana y muestra «Hoy entrenaste en WGYM» con el recordatorio
    de 15 a 25 g de proteína en las 2 horas siguientes (base técnica). Solo se guardan los días
    del propio socio (`wgymnutri_entreno_v1`).
  - «🎤 Voz» en Agregar comida: dictado del teléfono (`SpeechRecognition`, es-CL) o frase
    escrita («2 huevos, una marraqueta y 150 gramos de pollo»); `interpretarVoz` separa por
    comas/«y»/«con», entiende números en palabra y gramos, `mejorAlimento` busca en la lista y
    «Agregar todo» suma todo de una vez (`agregarVarios`). **Micrófono siempre visible (11-10-2026, la dueña: "no me
    aparece el micrófono"):** en iPhone (app en la pantalla de inicio o Chrome) la página no
    puede escuchar; el botón 🎤 abre el casillero con el teclado y explica usar el 🎤 del
    teclado (`porTeclado`), también si el dictado falla con `not-allowed`/`service-not-allowed`.
  - «🛒 Mi lista de compras» arriba de las recetas: en cada receta «🛒 Agregar a mi lista de
    compras» suma sus ingredientes (`D.compras`, sin repetir), se marcan al comprar, «📋 Copiar
    lista» para WhatsApp/Notas y «🗑 Vaciar».
  - «📲 Mi semana para Instagram» en Progreso: imagen 1080×1920 (`compartirSemana`) con logo,
    días en meta de los últimos 7, días entrenados, racha, proteína y agua promedio; se comparte
    o se descarga. El botón antiguo quedó como «Compartir mi racha y medallas».
  - «📷 Mis fotos de progreso» en Progreso: fotos achicadas a 1000 px guardadas SOLO en el
    teléfono (IndexedDB `wgymnutri_fotos`, por socio; nunca se suben); tocar 2 muestra
    ANTES/DESPUÉS con fecha; ✕ borra.
  - «🍔 Comer fuera»: al abrir Buscar sin escribir, Comida chilena y Comida rápida salen
    segundas. Si la dueña manda menús de locales de Tocopilla, se suman a esas categorías.
  - «🏆 Retos del mes» en Progreso: 3 retos automáticos y personales (días con meta de agua,
    con meta de proteína y con comidas anotadas; 1 punto por reto y día, `retosMes`). **Sin
    ranking** (la dueña, 10-10-2026: «el ranking no lo quiero aquí»): se sacó el apodo y la
    lista. El ranking se movió a la tarjeta virtual (ver «🏆 Ranking del mes» en la sección de
    la tarjeta).
  - «📸 Leer la etiqueta con la cámara» en «Crear este producto para todos» (valores por 100 g)
    y en «✍️ Manual» (por porción): Tesseract gratis dentro del repo
    (`vendor/tesseract-5.1.1/`, español `best_int`; ~6 MB que el teléfono baja solo la primera
    vez que se usa). `parseEtiqueta` busca Energía (kcal, ignora kJ), Proteínas, Grasas totales
    (no saturadas/trans) y H. de C. disponibles (no azúcares), elige la columna «100 g» según
    el encabezado y lee la porción. Siempre pide revisar los números antes de guardar. Probado
    con una etiqueta chilena: 4 de 4 valores correctos.
- **Básicos fitness (10-10-2026, pedido de la dueña):** categoría «⭐ Básicos
  fitness» al comienzo de `nutri-alimentos.js` (pechuga, claras, atún, whey,
  avena, arroz, camote, cottage, etc., con porciones de gimnasio). La búsqueda
  acepta singular/plural, muestra primero los básicos fitness y lo que empieza
  con lo escrito, deja marcas y comida rápida al final y no repite nombres.
- Encuesta inicial paso a paso con la misma fórmula que la tarjeta
  (Harris-Benedict, base técnica); rellena con `wgym_calorias_v1` si existe.
- Extras: agua, peso con gráfico, racha, medallas con confeti, resumen
  semanal (verde/rojo), tarjeta para compartir, recordatorios al abrir,
  comidas por momento (la once se llama «Snack» desde el 10-10-2026, la clave interna sigue siendo `once`) y frase del día. Recetas: recetario
  propio en `nutri-recetas.js` (la dueña NO quiere sus recetas de
  `comidas-saludables.html` aquí), cada una con «Agregar a mi día».
- **Bloqueo igual a la tarjeta:** plan vencido → app bloqueada entera con
  "Pagar mi mensualidad" (`pagar.html`). Pase diario: solo ese día. Vale la
  fecha más nueva entre la copia del teléfono, `socios.json` y la hoja.
- **Datos de salud solo en el teléfono** (`wgymnutri_v1_<NOMBRE>`): nunca en
  la hoja ni en el repo.
- **De pago: $5.000 al mes (10-10-2026, pedido de la dueña).** Precio en
  `pago-datos.js` (`nutri`). Quien no la tiene activa ve la pantalla
  «Activa WGYMNUTRI» (`#vPago`: datos de transferencia, copiar, WhatsApp a
  Sara, «Ya pagué: revisar de nuevo»). La dueña la activa desde la **ficha
  del socio en el mesón** (`control.html`, caja «🥗 WGYMNUTRI»: «Activar 1
  mes ($5.000)» suma un mes desde hoy o desde la fecha vigente; «Quitar» la
  borra), que guarda en la hoja «WGYMNUTRI» con `activarNutri` (POST con la
  clave de administración); la app lee `listarNutri`. Ambas acciones viven en
  `docs/apps-script/Ingresos.gs` (instrucciones en
  `docs/apps-script-ingresos-salidas.md`). Nunca es gratis (la dueña, 10-10-2026): si el script no
  tiene `listarNutri`, nadie la tiene activa y todos ven la pantalla de pago. El teléfono
  guarda la última fecha vista (`wgymnutri_activa_v1`) para abrir al instante.
- **Ofertas (10-10-2026, pedido de la dueña):** en `pago-datos.js`
  (`nutriOfertas`): 1 mes $5.000 · 3 meses $12.000 · pack «Full Mensual +
  WGYMNUTRI» $36.000. La pantalla de pago deja elegir la opción (cambia monto,
  comentario y el WhatsApp a Sara). En el mesón la caja «🥗 WGYMNUTRI» trae
  «Activar 1 mes» y «Activar 3 meses»; el pack se registra renovando el Full
  Mensual en la ficha como siempre + «Activar 1 mes».
- **Actualización automática (10-10-2026):** `wgymnutri.html` trae `NUTRI_VERSION`
  y compara con `nutri-version.txt`; si el archivo es mayor, se recarga sola.
  **Cada vez que se cambie `wgymnutri.html`, subir los dos números juntos
  (AAAAMMDDNN).** Los números se escriben en casilleros de texto con
  `inputmode="decimal"` (los `type="number"` del iPhone borraban la coma: 63,1 → 631).
- **Horas de comida (10-10-2026, pedido de la dueña):** en «Mi perfil», cuadro
  «🕒 Mis horas de comida» (una hora por comida, `D.horas`, solo en el teléfono;
  por defecto `HORAS_DEF`). La hora aparece junto a cada comida en «Hoy»,
  `comidaPorHora()` elige la comida según esas horas al tocar «+», y el
  recordatorio «Mis horas de comida» avisa si pasaron 30 min sin anotarla.
- **Recordatorios opcionales (10-10-2026):** en «Mi perfil», cuadro «🔔 Mis
  recordatorios» con interruptores (desayuno, agua, proteína, aviso al pasar la
  meta; `RECORDATORIOS`/`recOn`, guardado en `D.recordar` del teléfono). Son
  avisos al abrir la app: una página web no puede mandar notificaciones con la
  app cerrada sin un servicio de envío (push) aparte.
- **Logo de la cabecera que resalta (10-10-2026, la dueña mandó un video de su logo):**
  arriba a la izquierda de la app, `.logo-top` con `assets/wgymnutri-logo-cabecera.mp4`/`.webm`
  (los primeros 4,4 s del video, de frente, ida y vuelta para que el bucle no salte; sin
  sonido, 320 px), aro dorado/rojo que gira y brillo dorado que pulsa. Nombre y saludo en una
  sola línea (con «…» si no cabe).
- **Diseño (10-10-2026):** fondo blanco con el estilo de la tablet de la puerta
  (`nutri-claro.css`, va encima del CSS de la app; subir `?v=` al cambiarlo),
  letras grandes y negras a pedido de la dueña. Recetario solo saludable
  (438 recetas, sin pan blanco, frituras, embutidos ni postres con azúcar).
  Al abrir una receta se usa `history.pushState`: el gesto «atrás» del
  teléfono vuelve a la lista.

