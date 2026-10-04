# Videos de máquinas WGYM ADN SPORT

Un video y un GIF por máquina, todos con el mismo diseño, para las rutinas
de entrenamiento con QR. Cada máquina vive en su propia carpeta:

```
videos-maquinas/<maquina>/
  imagen.jpg        foto final: modelo realista en TU máquina, en TU gimnasio
  fuentes/          videos generados con IA (Gemini, Grok), sin editar
  config.json       título, series, tramos a usar y dónde está el músculo
  <maquina>.mp4     video final vertical (Reels, TikTok, Facebook, rutinas)
  <maquina>.gif     una vuelta, para WhatsApp y páginas
```

Para armar o rehacer el video: `python3 scripts/video-maquina.py videos-maquinas/<maquina>`

## Diseño fijo (no cambiar de una máquina a otra)

- Vertical 720×1280. Si la fuente no es vertical, va centrada sobre un fondo
  difuminado del mismo gimnasio.
- Logo oficial (`comun/logo.png`) arriba a la derecha.
- Franja inferior negra con línea roja: nombre del ejercicio en Rubik
  Distressed blanco y series en Anton dorado.
- El músculo que se trabaja parpadea en rojo durante el ejercicio.
- Sin flechas ni avisos de texto sobre la máquina (la dueña pidió sacar
  "TIRA EL SEGURO" y el círculo rojo, 04-10-2026).

## Pasos para una máquina nueva

1. **Foto de la máquina real** en el gimnasio, vertical, con buena luz.
2. **Imagen del modelo** (ChatGPT): máquina restaurada + persona realista
   haciendo el ejercicio, misma forma y colores, apoyada en el piso.
   Si hace falta, Claude la monta sobre la foto real del gimnasio.
3. **Video con IA** (Gemini → Video, o Grok → Imagine), subiendo la imagen
   vertical o la versión horizontal con costados difuminados (Gemini
   recorta lo vertical). Pedir cámara fija, sin zoom, hombre completo, sin
   agregar piezas. Si la máquina tiene un paso previo (ej. sacar el seguro),
   hacerlo en un video aparte.
4. Pasar los videos a Claude: corta los tramos buenos, los une y aplica el
   diseño con `scripts/video-maquina.py`.

## Máquinas listas

| Máquina | Ejercicio | Series |
|---|---|---|
| `pantorrilla-sentado` | Pantorrilla sentado (con paso previo: sacar el seguro) | 3 × 15 |
