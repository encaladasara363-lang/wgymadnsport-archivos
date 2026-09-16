# Video promocional WGYMADNSPORT — Recorrido "dron" (HyperFrames, 9:16, 1080x1920, 24s)

Composición HTML/CSS pura (sin librerías externas) para HeyGen HyperFrames.
Simula un recorrido FPV continuo por el gimnasio usando push-in + parallax
de dos capas sobre cada foto, transiciones con motion blur, logo flotante
de apertura que pasa a marca de agua persistente, y cierre con CTA.

**Timeline de 24s, un solo reloj CSS** (`animation: ... 24s linear forwards`
en cada capa), puntos de corte en porcentajes exactos:
0s=0% · 6s=25% · 12s=50% · 18s=75% · 24s=100%.

**Aviso honesto sobre el efecto "dron":** esto es un push-in + zoom en
2.5D sobre una foto fija (2 capas a distinta velocidad simulan
profundidad) — no es una recreación 3D real del espacio ni un vuelo con
paralaje verdadero como filmaría un dron de verdad. Es la técnica
estándar (tipo "Ken Burns" con parallax) para dar sensación de
movimiento sobre fotos estáticas, y funciona bien para redes, pero no
esperes el mismo resultado que un video filmado con dron real.

Reemplaza los 4 placeholders antes de renderizar:

| Placeholder | Contenido |
|---|---|
| `logo_gym.png` | Logo del gimnasio |
| `gym_foto1.jpg` | Infraestructura general |
| `gym_foto2.jpg` | Zona de máquinas |
| `gym_foto3.jpg` | Foto de entrenamiento/exterior |

## Código completo

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>WGYMADNSPORT — Recorrido dron</title>
<style>
  :root{
    --ink:#050505;
    --panel:#141416;
    --red:#E1061B;
    --paper:#FCFCFA;
    --gold:#FFD400;
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  html,body{ width:1080px; height:1920px; overflow:hidden; background:var(--ink); }
  body{ font-family:'Arial Black', Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif; }

  .stage{
    position:relative;
    width:1080px;
    height:1920px;
    background:var(--ink);
    overflow:hidden;
  }

  /* ============================================================
     CAPAS DE FOTO — cada una simula un push-in de dron con 2
     sub-capas (far/near) a distinta velocidad de escala = parallax
     ============================================================ */
  .photo-scene{
    position:absolute;
    inset:0;
    opacity:0;
    filter:blur(0px);
  }
  .photo-layer{
    position:absolute;
    inset:-6%; /* margen extra para que el zoom nunca deje bordes vacíos */
    overflow:hidden;
  }
  .photo-layer img{
    width:100%; height:100%; object-fit:cover;
    will-change:transform;
  }
  .photo-layer.far img{ filter:brightness(.82) saturate(1.05); }
  .photo-layer.near{ mix-blend-mode:normal; opacity:.35; }
  .photo-layer.near img{ filter:contrast(1.15) brightness(1.05); }

  .photo-scene::after{ /* viñeta para dar profundidad de "vuelo" */
    content:"";
    position:absolute; inset:0;
    background:radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(0,0,0,.55) 100%);
    pointer-events:none;
  }

  /* ---- Escena Foto 1: 0s-6s | 0%-25% ---- */
  .scene-foto1{ animation: sc1Life 24s linear forwards; }
  @keyframes sc1Life{
    0%   { opacity:0; filter:blur(14px); }
    4%   { opacity:1; filter:blur(0px); }
    22%  { opacity:1; filter:blur(0px); }
    25%  { opacity:0; filter:blur(14px); }
    100% { opacity:0; }
  }
  .scene-foto1 .far img{ animation: pushFar1 6.2s linear forwards; }
  .scene-foto1 .near img{ animation: pushNear1 6.2s linear forwards; }
  @keyframes pushFar1{  0%{ transform:scale(1) translate(0,0); } 100%{ transform:scale(1.18) translate(-1%,-1%); } }
  @keyframes pushNear1{ 0%{ transform:scale(1.05) translate(0,0); } 100%{ transform:scale(1.32) translate(-2%,-1.5%); } }

  /* ---- Escena Foto 2: 6s-12s | 25%-50% ---- */
  .scene-foto2{ animation: sc2Life 24s linear forwards; }
  @keyframes sc2Life{
    0%   { opacity:0; filter:blur(0px); }
    25%  { opacity:0; filter:blur(14px); }
    29%  { opacity:1; filter:blur(0px); }
    47%  { opacity:1; filter:blur(0px); }
    50%  { opacity:0; filter:blur(14px); }
    100% { opacity:0; }
  }
  .scene-foto2 .far img{ animation: pushFar2 6.2s linear forwards; }
  .scene-foto2 .near img{ animation: pushNear2 6.2s linear forwards; }
  @keyframes pushFar2{  0%{ transform:scale(1) translate(0,0); } 100%{ transform:scale(1.2) translate(1.5%,-1%); } }
  @keyframes pushNear2{ 0%{ transform:scale(1.05) translate(0,0); } 100%{ transform:scale(1.36) translate(2.5%,-1.8%); } }

  /* ---- Escena Foto 3: 12s-18s | 50%-75% ---- */
  .scene-foto3{ animation: sc3Life 24s linear forwards; }
  @keyframes sc3Life{
    0%   { opacity:0; filter:blur(0px); }
    50%  { opacity:0; filter:blur(14px); }
    54%  { opacity:1; filter:blur(0px); }
    72%  { opacity:1; filter:blur(0px); }
    75%  { opacity:0; filter:blur(14px); }
    100% { opacity:0; }
  }
  .scene-foto3 .far img{ animation: pushFar3 6.2s linear forwards; }
  .scene-foto3 .near img{ animation: pushNear3 6.2s linear forwards; }
  @keyframes pushFar3{  0%{ transform:scale(1) translate(0,0); } 100%{ transform:scale(1.15) translate(-1%,1%); } }
  @keyframes pushNear3{ 0%{ transform:scale(1.05) translate(0,0); } 100%{ transform:scale(1.3) translate(-2%,1.8%); } }

  /* ============================================================
     LOGO — apertura flotante (0-3.5s) → marca de agua esquina
     (3.5s-18s) → centro grande en el cierre (18s-24s)
     ============================================================ */
  .logo-intro{
    position:absolute; inset:0;
    display:flex; align-items:center; justify-content:center;
    z-index:5;
    animation: logoIntroLife 24s linear forwards;
  }
  @keyframes logoIntroLife{
    0%   { opacity:1; }
    13%  { opacity:1; }
    16%  { opacity:0; visibility:hidden; }
    100% { opacity:0; visibility:hidden; }
  }
  .logo-intro img{
    width:420px; height:420px; object-fit:contain;
    opacity:0; transform:scale(.5) translateY(30px);
    animation: logoFloatIn 2.2s cubic-bezier(.19,1,.22,1) forwards;
  }
  @keyframes logoFloatIn{
    0%   { opacity:0; transform:scale(.5) translateY(30px); }
    70%  { opacity:1; transform:scale(1.06) translateY(-6px); }
    100% { opacity:1; transform:scale(1) translateY(0); }
  }

  .logo-watermark{
    position:absolute;
    top:96px; right:64px;
    width:132px; height:132px;
    z-index:6;
    opacity:0;
    animation: watermarkLife 24s linear forwards;
  }
  @keyframes watermarkLife{
    0%   { opacity:0; }
    14%  { opacity:0; }
    17%  { opacity:.72; }
    73%  { opacity:.72; }
    76%  { opacity:0; }
    100% { opacity:0; }
  }
  .logo-watermark img{ width:100%; height:100%; object-fit:contain; }

  /* ============================================================
     TEXTO MOTIVACIONAL — durante Foto 1 (2s-6s aprox.)
     ============================================================ */
  .motiv-text{
    position:absolute;
    left:64px; right:64px;
    top:52%;
    transform:translateY(-50%);
    z-index:4;
    text-align:center;
    animation: motivLife 24s linear forwards;
  }
  @keyframes motivLife{
    0%   { opacity:0; }
    17%  { opacity:0; }
    20%  { opacity:1; }
    24%  { opacity:1; }
    25%  { opacity:0; }
    100% { opacity:0; }
  }
  .motiv-text span{
    display:inline-block;
    font-size:74px;
    line-height:1.18;
    color:var(--paper);
    text-transform:uppercase;
    text-shadow:0 6px 24px rgba(0,0,0,.65);
    opacity:0;
    transform:translateY(30px);
    animation: wordUp .5s cubic-bezier(.19,1,.22,1) forwards;
  }
  .motiv-text span.accent{ color:var(--red); }
  .motiv-text span:nth-child(1){ animation-delay:4.2s; }
  .motiv-text span:nth-child(2){ animation-delay:4.55s; }
  .motiv-text span:nth-child(3){ animation-delay:4.9s; }
  .motiv-text span:nth-child(4){ animation-delay:5.25s; }
  .motiv-text span:nth-child(5){ animation-delay:5.6s; }
  .motiv-text span:nth-child(6){ animation-delay:5.95s; }
  @keyframes wordUp{ 0%{opacity:0; transform:translateY(30px);} 100%{opacity:1; transform:translateY(0);} }

  /* ============================================================
     FRANJA DE SERVICIOS — flota durante Foto 2 (6.5s-11.5s)
     ============================================================ */
  .services-band{
    position:absolute;
    left:0; right:0;
    bottom:230px;
    z-index:4;
    display:flex;
    justify-content:center;
    gap:18px;
    padding:0 48px;
    flex-wrap:wrap;
    opacity:0;
    transform:translateY(50px);
    animation: bandLife 24s linear forwards;
  }
  @keyframes bandLife{
    0%   { opacity:0; transform:translateY(50px); }
    27%  { opacity:0; transform:translateY(50px); }
    30%  { opacity:1; transform:translateY(0); }
    46%  { opacity:1; transform:translateY(0); }
    49%  { opacity:0; transform:translateY(50px); }
    100% { opacity:0; transform:translateY(50px); }
  }
  .services-band .chip{
    background:rgba(20,20,22,.88);
    border:2px solid var(--red);
    border-radius:100px;
    padding:16px 30px;
    font-size:24px;
    color:var(--paper);
    text-transform:uppercase;
    letter-spacing:.03em;
  }

  /* ============================================================
     DIRECCIÓN — persistente y discreta durante las 3 fotos
     ============================================================ */
  .address-tag{
    position:absolute;
    left:0; right:0;
    bottom:130px;
    z-index:4;
    text-align:center;
    opacity:0;
    animation: addrLife 24s linear forwards;
  }
  @keyframes addrLife{
    0%   { opacity:0; }
    17%  { opacity:0; }
    19%  { opacity:.9; }
    74%  { opacity:.9; }
    76%  { opacity:0; }
    100% { opacity:0; }
  }
  .address-tag span{
    font-family:Arial, sans-serif;
    font-weight:700;
    font-size:24px;
    letter-spacing:.16em;
    text-transform:uppercase;
    color:var(--gold);
    background:rgba(5,5,5,.55);
    padding:10px 26px;
    border-radius:8px;
  }

  /* ============================================================
     ESCENA DE CIERRE — 18s-24s | 75%-100%
     ============================================================ */
  .scene-close{
    position:absolute; inset:0;
    display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    gap:44px;
    z-index:7;
    background:var(--ink);
    opacity:0;
    animation: closeLife 24s linear forwards;
  }
  @keyframes closeLife{
    0%   { opacity:0; visibility:hidden; }
    74%  { opacity:0; visibility:hidden; }
    76%  { opacity:1; visibility:visible; }
    100% { opacity:1; }
  }
  .scene-close .close-logo{
    width:300px; height:300px; object-fit:contain;
    opacity:0; transform:scale(.6);
    animation: closeLogoIn .8s cubic-bezier(.19,1,.22,1) forwards;
    animation-delay:18.3s;
  }
  @keyframes closeLogoIn{ 0%{opacity:0; transform:scale(.6);} 100%{opacity:1; transform:scale(1);} }

  .scene-close .close-address{
    font-family:Arial, sans-serif;
    font-weight:700;
    font-size:30px;
    letter-spacing:.14em;
    text-transform:uppercase;
    color:var(--paper);
    opacity:0;
    animation: fadeIn .6s ease-out forwards;
    animation-delay:19s;
  }
  @keyframes fadeIn{ 0%{opacity:0;} 100%{opacity:.9;} }

  .scene-close .cta{
    background:var(--red);
    color:var(--paper);
    font-size:52px;
    text-transform:uppercase;
    padding:32px 64px;
    border-radius:100px;
    letter-spacing:.02em;
    opacity:0;
    transform:scale(.7);
    animation: ctaPulseIn 1s cubic-bezier(.34,1.56,.64,1) forwards;
    animation-delay:19.7s;
  }
  @keyframes ctaPulseIn{
    0%   { opacity:0; transform:scale(.7); }
    70%  { opacity:1; transform:scale(1.08); }
    100% { opacity:1; transform:scale(1); }
  }
</style>
</head>
<body>

  <div class="stage">

    <!-- FOTO 1 · 0s-6s -->
    <section class="photo-scene scene-foto1" data-start="0" data-end="6">
      <div class="photo-layer far"><img src="gym_foto1.jpg" alt="Infraestructura general"></div>
      <div class="photo-layer near"><img src="gym_foto1.jpg" alt=""></div>
    </section>

    <!-- FOTO 2 · 6s-12s -->
    <section class="photo-scene scene-foto2" data-start="6" data-end="12">
      <div class="photo-layer far"><img src="gym_foto2.jpg" alt="Zona de máquinas"></div>
      <div class="photo-layer near"><img src="gym_foto2.jpg" alt=""></div>
    </section>

    <!-- FOTO 3 · 12s-18s -->
    <section class="photo-scene scene-foto3" data-start="12" data-end="18">
      <div class="photo-layer far"><img src="gym_foto3.jpg" alt="Entrenamiento"></div>
      <div class="photo-layer near"><img src="gym_foto3.jpg" alt=""></div>
    </section>

    <!-- LOGO apertura flotante · 0s-3.5s -->
    <div class="logo-intro" data-start="0" data-end="3.5">
      <img src="logo_gym.png" alt="Logo del gimnasio">
    </div>

    <!-- LOGO marca de agua · 3.5s-18s -->
    <div class="logo-watermark" data-start="3.5" data-end="18">
      <img src="logo_gym.png" alt="">
    </div>

    <!-- TEXTO MOTIVACIONAL · dentro de Foto 1, 4.2s-6s -->
    <div class="motiv-text" data-start="4.2" data-end="6">
      <span>LA</span> <span>PERSEVERANCIA</span> <span>ES</span>
      <span class="accent">EL</span> <span class="accent">SECRETO</span>
      <span class="accent">DE&nbsp;TU&nbsp;ÉXITO</span>
    </div>

    <!-- FRANJA DE SERVICIOS · dentro de Foto 2, 6.5s-11.5s -->
    <div class="services-band" data-start="6.5" data-end="11.5">
      <div class="chip">Planes</div>
      <div class="chip">Suplementos</div>
      <div class="chip">Ropa deportiva</div>
      <div class="chip">Pases diarios</div>
    </div>

    <!-- DIRECCIÓN persistente · 4s-18s -->
    <div class="address-tag" data-start="4" data-end="18">
      <span>21 de Mayo 1520</span>
    </div>

    <!-- CIERRE · 18s-24s -->
    <section class="scene-close" data-start="18" data-end="24">
      <img class="close-logo" src="logo_gym.png" alt="Logo del gimnasio">
      <div class="close-address">21 de Mayo 1520 · Tocopilla</div>
      <div class="cta">¡Inscríbete hoy!</div>
    </section>

  </div>

</body>
</html>
```

## Notas de implementación

- **Reloj único de 24s**: las tres fotos y todos los overlays comparten
  `animation-duration:24s`, con cortes en 0/25/50/75/100% (0/6/12/18/24s)
  — así todo queda perfectamente sincronizado sin temporizadores por
  separado.
- **Parallax simulado**: cada foto tiene dos capas (`.far` / `.near`)
  que escalan a velocidades distintas — la de "near" se mueve/escala
  más rápido y con más contraste, dando sensación de profundidad. No es
  un parallax 3D real (solo hay una foto plana), pero se percibe como
  movimiento de cámara.
- **Transición "motion blur"**: cada escena de foto entra/sale con un
  pulso de `filter:blur(14px)→0px` combinado con el fundido de
  opacidad — simula el desenfoque de movimiento de una transición
  rápida sin necesitar procesamiento de video real.
- **Logo**: aparece flotando y centrado los primeros 3.5s, luego pasa a
  marca de agua translúcida en la esquina superior derecha durante las
  tres fotos, desaparece justo antes del cierre, y vuelve a aparecer
  centrado y grande en la pantalla final.
- **Textos**: la frase motivacional entra palabra por palabra sobre la
  Foto 1 (últimos ~1.8s de esa escena), la franja de servicios flota
  sobre la Foto 2, la dirección queda fija y discreta abajo durante las
  tres fotos, y el cierre repite la dirección junto al botón CTA.
- **Sin librerías externas**: tipografía de sistema en negrita, mismo
  criterio que el resto de las piezas del gimnasio — no depende de
  cargar nada desde internet.
- **Reemplazo de imágenes**: solo cambia los 4 `src`
  (`logo_gym.png`, `gym_foto1.jpg`, `gym_foto2.jpg`, `gym_foto3.jpg`)
  por tus archivos reales, manteniendo esos nombres o actualizando las
  rutas en el HTML.
