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
| Sentadilla en Smith | — | ✅ `mujer/sentadilla-smith` (Grok, 14-10-2026) | 3 × 10-12 |
| Curl femoral a una pierna (de pie, máquina n.º 8 del 2.º piso) | — | ✅ `mujer/curl-femoral-de-pie` (Grok, 14-10-2026) | 3 × 10-12 |
| Elevación lateral con discos | — | ✅ `mujer/elevacion-lateral-discos` | 3 × 12 |
| Curl de bíceps con discos | — | ✅ `mujer/curl-biceps-discos` | 3 × 15 |
| Extensión de cuádriceps (máquina n.º 1) | — | ✅ `mujer/extension-cuadriceps` (Grok, 16-10-2026) | 3 × 12-15 |
| Elevación de talones de pie (máquina con hombreras, terraza) | — | ✅ `mujer/elevacion-talones-de-pie` (Grok, 16-10-2026) | 3 × 12-15 |
| Press de pecho sentado (máquina n.º 14, terraza) | — | ✅ `mujer/press-pecho-sentado` (Grok, 16-10-2026) | 3 × 10-12 |
| Remo frontal (máquina n.º 23, terraza) | — | ✅ `mujer/remo-frontal` (Grok, 16-10-2026) | 3 × 10-12 |
| Press militar (máquina n.º 15, terraza) | — | ✅ `mujer/press-militar` (Grok, 16-10-2026) | 3 × 8-10 |
| Extensión de tríceps en polea (n.º 20, cuerda) | — | ✅ `mujer/extension-triceps-polea` (Grok, 16-10-2026) | 3 × 12-15 |
| Crunch abdominal en polea (acostada, n.º 20, barra recta) | — | ✅ `mujer/crunch-acostado-polea` (Grok, 17-10-2026) | 3 × 12-15 |
| Prensa de piernas (inclinada 45°, terraza) | — | ✅ `mujer/prensa-piernas` (Grok, 17-10-2026, sin bloqueo articular) | 3 × 8-10 |
| Sentadilla hack inversa (máquina n.º 12 al revés, terraza) | — | ✅ `mujer/hack-inversa` (Grok, 17-10-2026) | 3 × 10-12 |
| Patada de glúteo en polea (polea n.º 20, tobillera abajo) | — | ✅ `mujer/patada-gluteo-polea` (Grok, 17-10-2026) | 3 × 12-15 |
| Press de pecho con mancuernas (banco plano de la terraza) | — | ✅ `mujer/press-pecho-mancuernas` (Grok, 17-10-2026) | 3 × 10-12 |
| Jalón al pecho (máquina n.º 24, terraza) | — | ✅ `mujer/jalon-al-pecho` (Grok, 17-10-2026) | 3 × 8-10 |
| Face pull en polea (polea n.º 20, cuerda) | — | ✅ `mujer/face-pull-polea` (Grok, 17-10-2026) | 3 × 12-15 |
| Plancha frontal (colchoneta en el pasto de la terraza) | — | ✅ `mujer/plancha-frontal` (Grok, 17-10-2026) | 3 × 30-40 seg |
| Sentadilla goblet (cuñas frente al espejo, terraza; cuádriceps) | — | ✅ `mujer/sentadilla-goblet` (Grok, 17-10-2026) | 3 × 10-12 |
| Zancadas con mancuernas (pie adelante sobre un step, frente al espejo, terraza) | — | ✅ `mujer/zancadas-mancuernas` (Grok, 17-10-2026) | 3 × 10 por pierna |
| Peso muerto sumo con mancuerna (plataforma roja de sumo, de frente) | — | ✅ `mujer/peso-muerto-sumo` (Grok, 17-10-2026) | 3 × 10-12 |
| Abducción de cadera en máquina (palanca roja de patada de glúteo, terraza) | — | ✅ `mujer/abduccion-cadera-maquina` (Gemini, repetido 6 veces, 17-10-2026) | 3 × 12-15 |
