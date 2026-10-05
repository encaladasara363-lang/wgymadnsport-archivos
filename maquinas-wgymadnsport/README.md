# Máquinas WGYMADNSPORT

Un video y un GIF por cada máquina del gimnasio, todos con el mismo diseño,
listos para las rutinas con QR. Hay **dos carpetas paralelas**, una por
modelo, con las mismas máquinas en cada una:

```
maquinas-wgymadnsport/
  comun/
    logo.png            logo oficial (va en todos los videos)
    modelo-hombre.jpg   referencia del MISMO hombre para todas las máquinas
    modelo-mujer.jpg    referencia de la MISMA mujer (se agrega al tenerla)
  hombre/<maquina>/     rutinas de hombre
  mujer/<maquina>/      rutinas de mujer (misma máquina, misma pose)
```

Cada carpeta de máquina:

```
  imagen.jpg        foto final: el modelo en TU máquina, en TU gimnasio
  fuentes/          videos generados con IA (Gemini, Grok), sin editar
  config.json       título, series, tramos a usar y dónde está el músculo
  <maquina>.mp4     video final vertical
  <maquina>.gif     una vuelta, para WhatsApp y páginas
```

Para armar o rehacer un video:
`python3 scripts/video-maquina.py maquinas-wgymadnsport/hombre/<maquina>`

## Reglas fijas

- **Siempre el mismo modelo**: el mismo hombre en todas las máquinas de
  `hombre/` y la misma mujer en todas las de `mujer/`. Al pedir la imagen a
  ChatGPT se sube junto con `comun/modelo-hombre.jpg` o `comun/modelo-mujer.jpg`
  como referencia de cara, cuerpo y ropa.
- **Mismo diseño**: vertical 720×1280, logo arriba a la derecha, franja
  inferior con el nombre (Rubik Distressed) y las series (Anton dorado), y
  el músculo trabajado parpadeando en rojo. Sin flechas ni textos sobre la
  máquina.
- Fondo: la foto real del gimnasio.

## Pasos para una máquina nueva

1. Foto de la máquina real en el gimnasio, vertical, con buena luz.
2. Imagen del modelo (ChatGPT) con la referencia del modelo de esa carpeta.
3. Versión mujer: misma imagen, cambiando solo la persona (prompt en la
   conversación con Claude del 04-10-2026).
4. Video con IA (Gemini → Video o Grok → Imagine), cámara fija, sin agregar
   piezas. Un paso previo (ej. sacar el seguro) va en un video aparte.
5. Claude corta los tramos buenos, los une y aplica el diseño.

## Máquinas listas

| Máquina | Hombre | Mujer | Series |
|---|---|---|---|
| Pantorrilla sentado | ✅ `hombre/pantorrilla-sentado` | ✅ `mujer/pantorrilla-sentado` | 3 × 15 |
| Hip thrust | ✅ `hombre/hip-thrust` | ✅ `mujer/hip-thrust` | 4 × 12 |
