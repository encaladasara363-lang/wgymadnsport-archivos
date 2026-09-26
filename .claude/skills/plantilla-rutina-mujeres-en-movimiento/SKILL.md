---
name: plantilla-rutina-mujeres-en-movimiento
description: Plantilla oficial y OBLIGATORIA de diseño para crear cualquier app de rutina nueva de socios/as (login por nombre y apellido contra socios.json, bienvenida animada personalizada, dashboard con comparación semanal, cronómetro, resumen al terminar) y su cartel QR a juego. Usar siempre que el dueño del gimnasio mande o pida una rutina nueva para una socia (no VIP) — es el diseño único desde 09/2026, no hace falta que lo pida explícitamente "con el mismo diseño".
---

# Plantilla de app de rutina: mismo diseño que "Mujeres en Movimiento"

**Regla permanente (ver CLAUDE.md → "Diseño único de app y cartel QR
para toda rutina nueva de socias"): esta plantilla se usa siempre para
cualquier rutina nueva de socia, aunque el dueño no lo pida
explícitamente.** Solo los clientes VIP/exclusivos usan otra plantilla
(`app_milton.html`).

Archivo de referencia (ya pulido a fondo, con todos los ajustes que pidió
el dueño): `mujeres-en-movimiento.html`, en la raíz del repo.
Sitio en vivo: https://encaladasara363-lang.github.io/wgymadnsport-archivos/mujeres-en-movimiento.html

Para una rutina nueva con este mismo diseño: **copiar
`mujeres-en-movimiento.html` tal cual** a un archivo nuevo y cambiar
únicamente lo de abajo — nunca rediseñar desde cero, y nunca tocar
`socios.json`.

**El dueño manda el archivo de la rutina (con sus ejercicios, series,
descansos, tips e imágenes ya definidos) y espera que Claude solo la
"adapte" a este diseño — nunca que rediseñe o reemplace lo que ya
viene en ese archivo.** En particular, **las imágenes de los
ejercicios de esa rutina nunca se tocan**: se transplantan tal cual
(mismo archivo/base64/URL) al array de imágenes correspondiente
(`EXERCISE_IMAGES`/`POSE_IMAGES`), nunca se buscan fotos nuevas, se
recortan, se editan ni se reemplazan por otras — a diferencia de la
foto del cartel QR impreso (esa sí se elige aparte y debe variar de un
cartel a otro, ver más abajo). Lo único que cambia es la estructura,
el diseño visual y el armado alrededor (PLAN, claves de localStorage,
textos), nunca el contenido ni las imágenes que trae la rutina
original.

## Qué cambiar por cada rutina nueva

1. **Nombre del archivo**: uno descriptivo en la raíz del repo (mismo
   patrón que `mujeres-en-movimiento.html`).
2. **`<title>`**, el `<h1>`/subtítulo del hero y el nombre que aparece en
   `.welcome-eyebrow`/`.welcome-sub` si corresponde a otro programa.
3. **El array `PLAN`**: los días, ejercicios, series, descansos, tips
   biomecánicos e **imágenes** de la rutina nueva, transplantados tal
   cual del archivo que mandó el dueño (aplicar la "Base de
   conocimiento técnico" de `CLAUDE.md` solo para completar algo que
   ese archivo no traiga, nunca para reemplazar lo que sí trae).
4. **Claves de `localStorage`** (`key()`, y cualquier otra clave tipo
   `wgym_..._v1`): cambiar el sufijo para que no se mezcle con el
   progreso guardado de otra rutina en el mismo celular.
5. **Textos de bienvenida** (`#welcomeName`, `.welcome-sub`) si el saludo
   debe mencionar otro nombre de programa — pero MANTENER "Bienvenido a
   WGYM ADN Sport Tocopilla" salvo que el dueño pida otro texto.

## Qué NUNCA se toca ni se rediseña (ya está aprobado y probado)

- **Login por nombre y apellido contra `socios.json`**: `fetch("socios.json...")`,
  `norm()`, `expired(m.fv)` bloqueando el acceso si está vencida. Nunca
  quitar esta validación ni inventar otro origen de datos.
- **Fecha de hoy + aviso de vencimiento**: `.date-bar` (fondo blanco,
  color de texto oscuro explícito — nunca `var(--muted)`, que es un gris
  claro pensado para fondo oscuro y queda invisible sobre blanco) y
  `.notice-bar`/`pintarVencimiento()`, que muestra "Vence el DD-MM-AAAA ·
  quedan N días" con el mismo criterio que `tarjeta.html`.
- **Bienvenida animada personalizada** (`#welcome`, `mostrarBienvenida()`):
  logo del gimnasio + nombre en rojo + "¡Hola, NOMBRE!" + "Bienvenido a
  WGYM ADN Sport Tocopilla" + botón "Saltar introducción", con destellos
  alrededor. Detalles importantes que costó ajustar:
  - **Los destellos van dibujados en CSS puro** (`.sparkle` con
    `::before`/`::after` en cruz + `box-shadow` de brillo), nunca con el
    emoji ✨ — en varios navegadores/WebViews de celular el emoji no
    renderiza a color y el destello queda invisible (solo se veía en
    computador). Reusar tal cual las reglas `.sparkle`/`@keyframes sparkle`.
  - **El logo se reutiliza por JS** copiando el `src` del `<img>` del
    header (`document.querySelector(".top img").src`) al `<img id="welcomeLogo">`
    de la bienvenida — nunca volver a pegar el base64 del logo una
    segunda vez en el archivo (duplicaría varios MB de peso).
  - Duración por defecto: **25 segundos**, con el botón "Saltar
    introducción" (`saltarBienvenida()`) que cancela el `setTimeout`
    guardado en `welcomeTimer` y pasa directo al panel.
- **Dashboard de progreso**: barra de progreso semanal, grilla de 5 días,
  racha (`streakCount`), "Mis récords", "Semanas anteriores", y el
  comparativo `#weekCompare`/`semanaAnteriorCompletados()` que compara
  esta semana contra la semana inmediatamente anterior (se oculta solo
  si todavía no hay una semana previa registrada).
- **Resumen al terminar** (`#sessionSummary`, "RESUMEN DEL
  ENTRENAMIENTO") durante el modo entrenamiento. (El bloque "MAPA DE TU
  ENTRENAMIENTO" con números tocables que aparecía sobre la lista de
  ejercicios se sacó a pedido del dueño — `renderExerciseMap()` queda
  con un guard `if(!$("mapPoints"))return` en vez de borrarse, así no
  hace falta tocar sus llamadas si en algún momento se reincorpora.)
- **Cronómetro de sesión**, **registro de peso corporal semanal** y
  **compartir tarjeta de progreso** (canvas → imagen).
- **Diseño visual**: negro casi puro, acento rojo/dorado (`--yellow:#ffd841`),
  tipografía del sistema, mismos estilos de tarjeta/pill/badge.

## El cartel QR también sigue una sola línea

El dueño quiere que **todos** los carteles QR para imprimir usen el
mismo diseño (a pedido explícito: "quiero mantener una línea"). Copiar
`cartel-qr-mujeres-movimiento.html` (o `cartel-qr-perdida-grasa.html`,
la segunda referencia ya con foto) tal cual, y cambiar solo:

- Título/subtítulo (mismo patrón: "Rutina de N Días de NOMBRE").
- El badge sobre el QR (`.qr-badge`) lleva **solo el nivel**
  ("Principiante", "Intermedia", etc.) — nunca "N Días · Nivel", el
  dueño pidió sacar la cantidad de días de ahí.
- El QR (regenerar apuntando al archivo de la rutina correspondiente,
  PNG plano `ERROR_CORRECT_M`, sin logo incrustado — el logo ya está
  arriba del cartel).
- **La foto junto al QR**: dentro de `.medio`, una tarjeta `.foto-frame`
  (mismo borde dorado/sombra que `.qr-frame`) con una foto real de la
  app mostrando a alguien ejecutando un ejercicio de esa rutina — nunca
  un mockup de celular ni una captura de pantalla de la app. Se puede
  sacar directo del array de imágenes de ejercicios del archivo de la
  rutina (`EXERCISE_IMAGES`/`POSE_IMAGES`, según cuál tenga esa app).
  **Variar el ejercicio elegido de un cartel a otro** (a pedido
  explícito del dueño: "que valla variando") — nunca repetir el mismo
  tipo de ejercicio/misma máquina en dos carteles seguidos solo porque
  fue la primera imagen del array. Antes de elegir, mirar qué ejercicio
  se usó en el cartel anterior más reciente (ej. `cartel-qr-mujeres-movimiento.html`
  usa prensa de piernas, `cartel-qr-perdida-grasa.html` usa hip thrust —
  ambas de piernas, sería mejor la próxima vez elegir uno de tren
  superior, core o cardio) y preferir un grupo muscular distinto, para
  que la colección de carteles en el gimnasio se vea variada.
  Con `.qr-frame img` a 62mm y `.foto-frame img` a 56×70mm (object-fit
  cover) ambas tarjetas entran lado a lado sin volver a topar la franja
  de color de abajo — si se agranda cualquiera de las dos, volver a
  verificar con captura que `.nota p` sigue por sobre `.pie`.
- **Banner "🔥 Dentro de tu app"** (`.logros`/`.logros-tag`/`.logros-fila`/
  `.logro`): franja destacada con fondo degradado rojo/dorado y borde
  dorado, entre `.chips` y `.rule`, con las tres funciones gamificadas
  del dashboard en una sola línea: "⚖️ Registra tu peso · 🏆 Mis récords
  · 🥇 Gana tu medalla". Copiar tal cual (mismo texto, no hace falta
  adaptarlo por rutina). Es un elemento más que compite por el espacio
  vertical ya ajustado de la hoja — si el cartel de referencia cambia de
  tamaño de fuente/imágenes, volver a probar con captura que `.logros`,
  `.nota` y `.pie` no se pisen ni se corten (ya pasó una vez: agregar
  este bloque sin achicar nada más empujó `.nota` fuera del área visible
  de `.hoja`).

## Antes de publicar

Igual que se hizo con "Mujeres en Movimiento": servir el archivo en un
servidor local (`python3 -m http.server`) y probar con un socio real de
`socios.json` (login, fecha de vencimiento, bienvenida) antes de
publicar — sobre todo si se toca cualquier parte del login o de
`pintarVencimiento()`. Publicar siguiendo el flujo normal (rama → commit
→ push → PR → merge a `main` → resincronizar rama de trabajo), sin tocar
`socios.json`.
