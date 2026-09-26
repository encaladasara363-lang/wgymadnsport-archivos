---
name: publicar-rutinas-nuevas
description: Renovar, agregar o actualizar socios de WGYMADNSPORT en socios.json, control.html y pantalla.html, y publicar el cambio en el sitio en vivo. Usar cuando el dueño del gimnasio pegue una ficha de socio (formato "📋 Copiar" de una sola persona) o el JSON completo de "📋 Copiar lista" de control.html, o pida renovar/agregar/borrar socios vencidos.
---

# Renovar socios de WGYMADNSPORT

Repositorio: `encaladasara363-lang/wgymadnsport-archivos`
Sitio en vivo: https://encaladasara363-lang.github.io/wgymadnsport-archivos/

`socios.json` (raíz del repo) es la **única planilla de socios**. La leen
`tarjeta.html` (QR de ingreso) y todas las apps `entrenar-*.html`/`app_*.html`
(rutinas de entrenamiento).

## Formatos de entrada que puede mandar el dueño

1. **Un solo socio**: objeto suelto `{ "n", "a", "rut", "plan", "monto", "fv" }`
   — es el que copia el botón "📋 Copiar" de la ficha individual en
   `control.html`. Llega así, es pedido directo de renovar/agregar a esa
   persona: no preguntar la fecha ni nada más, el objeto ya trae todo.
2. **Lista completa**: el JSON que exporta el botón "📋 Copiar lista" de
   `control.html`, con `socios`, `asistencia` y `ciclos`.

## Pasos, siempre en este orden

1. **Editar `socios.json`**: fusionar nombre, apellido, plan, monto y `fv`
   (fecha de vencimiento, serial tipo Excel) con lo ya existente, buscando
   al socio por nombre + apellido.
2. **El campo `"rut"` SIEMPRE queda como `"Sin Rut"`**, aunque el dato que
   llegue traiga un RUT real (de cualquier origen: "📋 Copiar", "Pasar la
   lista", etc.) — se descarta antes de guardar. Este repositorio es
   público y esos archivos se sirven tal cual en el sitio en vivo; nunca
   escribir un RUT real en ningún archivo publicado (`socios.json`,
   `tarjeta.html`, `entrenar-*.html`, `app_*.html`, `control.html`,
   `pantalla.html`).
3. Mantener `socios.json` ordenado alfabéticamente por apellido, sin
   duplicados.
4. Actualizar el campo `"actualizado"` con la fecha del día.
5. **Regenerar en el mismo movimiento, con los mismos datos, LAS DOS
   copias** (nunca solo una, o el aparato que falte muestra al socio como
   "no encontrado"):
   - `LISTA_BASE` en `control.html` — formato
     `{n:"...",a:"...",plan:"...",m:MONTO,v:"AAAA-MM-DD"}` (sin `rut`; `v`
     es la fecha ISO ya convertida del serial, no el serial mismo). Subir
     `LISTA_VERSION` (formato `AAAAMMDDNN`).
   - `SOCIOS` en `pantalla.html` — formato
     `{n:"...",a:"...",plan:"...",fv:SERIAL}` (con el serial tal cual, sin
     convertir). Subir `SOCIOS_VERSION` al mismo número que
     `LISTA_VERSION`.
   - Si el envío trae `asistencia`/`ciclos` (export de "📋 Copiar lista"),
     regenerar también `ASISTENCIA_BASE`/`CICLOS_BASE` en ambos archivos y
     subir `ASISTENCIA_VERSION`. Es un agregado puro: nunca pisa ni borra
     un día o ciclo que un equipo ya tenía anotado.
6. **Validar** que los arrays quedaron bien formados antes de publicar
   (por ejemplo cargando el fragmento con Node y contando socios) — un
   JSON/JS mal cerrado rompe la página para todos los que la abran.
7. **De paso, revisar los 3 meses vencidos**: cualquier socio cuya `fv` ya
   pasó hace **3 meses o más** (meses calendario, no 90 días fijos) se saca
   directo de `socios.json`, `LISTA_BASE` y `SOCIOS` en la misma tanda —
   avisando siempre nombre, apellido y hace cuánto estaba vencido (nunca en
   silencio).
8. **Publicar directo en `main`**: rama nueva → commit → push → PR → merge
   a `main` → resincronizar la rama de trabajo. El sitio es en vivo y el
   socio necesita acceso inmediato a su QR y sus rutinas — no dejarlo
   pendiente de aprobación.
9. **Confirmar al dueño**: quién se agregó, renovó o borró, con la fecha
   nueva de cada uno.

## Casos especiales

- Si en un export de "Pasar la lista" aparece un socio repetido (mismo
  nombre dos veces), es un doble registro hecho sin querer en el mesón —
  avisar y preguntar cuál ficha borrar, no agregarlo ni resolverlo solo (esa
  duplicación vive en el `localStorage` de esa compu; el dueño debe borrar
  la fila de más él mismo en `control.html`).
- Si llega un correo/aviso de vencidos por Gmail, ese es un formato
  distinto (solo vencidos de la última semana, ordenados por apellido,
  nombre y apellido en mayúsculas, sin fecha ni otro dato) — no confundir
  con esta rutina de renovación.
