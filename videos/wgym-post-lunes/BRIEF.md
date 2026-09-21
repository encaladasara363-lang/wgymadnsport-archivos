---
workflow: motion-graphics
flow: automation
storyboard: no
message: "Motivación de lunes para arrancar la semana en WGYMADNSPORT, reutilizando el sistema visual ya aprobado (panel diagonal, logo, headline Bebas Neue, tagline de marca, dirección)."
destination: Instagram / Facebook / TikTok (Metricool, brandId 6700545)
aspect: "1080x1080 (igual que videos/wgym-post-moderno)"
language: es
length: "3.2s"
---

## Intent

Pieza corta de "lunes de arranque" para publicar hoy en las tres redes del
gimnasio a la vez. El usuario pidió que se creara sin ronda de preguntas
("créame una publicidad hoy... y lo publicas en la hora pico") y corrigió
que WGYMADNSPORT **no** es un gimnasio de barrio — evitar ese lenguaje en
cualquier copy, mantener el tono de instalación seria/profesional que ya
usa `flyer_publicitario.md` ("Entrena con ciencia").

## Customizations

- Reutiliza tal cual el sistema visual de `videos/wgym-post-moderno`:
  fondo casi negro, panel diagonal rojo→dorado, logo circular, tipografía
  Bebas Neue (headline) + Inter (tag/dirección), acento dorado en la
  segunda línea del headline.
- Cambia solo el copy del headline para el tema "lunes"; mantiene la
  frase de marca "La perseverancia es el secreto de tu éxito" y la
  dirección 21 de Mayo 1520.
- Mismos assets (`foto-maquinas.jpg`, `logo.jpg`), misma duración (3.2s),
  mismo timeline de entrada (panel → logo → headline → tag → dirección).

## Notes

- Inferido (sin pregunta al usuario, por señal de "no preguntes / hazlo"):
  `flow: automation`, `storyboard: no`, aspecto y duración heredados del
  proyecto de referencia.
- Publicación: se consulta `getBestTimeToPostByNetwork` en Metricool para
  Instagram, Facebook y TikTok y se muestra el borrador + horario propuesto
  al usuario antes de dejarlo agendado/publicado, por la regla permanente
  de confirmar contenido nuevo antes de publicar.
