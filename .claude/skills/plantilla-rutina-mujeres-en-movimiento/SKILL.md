---
name: plantilla-rutina-mujeres-en-movimiento
description: Plantilla oficial de diseño para crear nuevas apps de rutina de socios/as (login por nombre y apellido contra socios.json, bienvenida animada personalizada, dashboard con comparación semanal, mapa de 5 ejercicios, cronómetro, resumen al terminar). Usar cuando el dueño del gimnasio pida una app de rutina nueva "con el mismo diseño" o "como Mujeres en Movimiento".
---

# Plantilla de app de rutina: mismo diseño que "Mujeres en Movimiento"

Archivo de referencia (ya pulido a fondo, con todos los ajustes que pidió
el dueño): `mujeres-en-movimiento.html`, en la raíz del repo.
Sitio en vivo: https://encaladasara363-lang.github.io/wgymadnsport-archivos/mujeres-en-movimiento.html

Para una rutina nueva con este mismo diseño: **copiar
`mujeres-en-movimiento.html` tal cual** a un archivo nuevo y cambiar
únicamente lo de abajo — nunca rediseñar desde cero, y nunca tocar
`socios.json`.

## Qué cambiar por cada rutina nueva

1. **Nombre del archivo**: uno descriptivo en la raíz del repo (mismo
   patrón que `mujeres-en-movimiento.html`).
2. **`<title>`**, el `<h1>`/subtítulo del hero y el nombre que aparece en
   `.welcome-eyebrow`/`.welcome-sub` si corresponde a otro programa.
3. **El array `PLAN`**: los días, ejercicios, series, descansos y tips
   biomecánicos de la rutina nueva (aplicar la "Base de conocimiento
   técnico" de `CLAUDE.md` para armarlo).
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
- **Mapa de 5 ejercicios** (`.exercise-map`/`.map-points`, grid de 5) y
  **resumen al terminar** (`#sessionSummary`, "RESUMEN DEL
  ENTRENAMIENTO") durante el modo entrenamiento.
- **Cronómetro de sesión**, **registro de peso corporal semanal** y
  **compartir tarjeta de progreso** (canvas → imagen).
- **Diseño visual**: negro casi puro, acento rojo/dorado (`--yellow:#ffd841`),
  tipografía del sistema, mismos estilos de tarjeta/pill/badge.

## Antes de publicar

Igual que se hizo con "Mujeres en Movimiento": servir el archivo en un
servidor local (`python3 -m http.server`) y probar con un socio real de
`socios.json` (login, fecha de vencimiento, bienvenida) antes de
publicar — sobre todo si se toca cualquier parte del login o de
`pintarVencimiento()`. Publicar siguiendo el flujo normal (rama → commit
→ push → PR → merge a `main` → resincronizar rama de trabajo), sin tocar
`socios.json`.
