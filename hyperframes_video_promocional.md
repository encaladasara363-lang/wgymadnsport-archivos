# Video promocional WGYMADNSPORT — HyperFrames (9:16, 1080x1920, 12s)

Composición HTML/CSS pura (sin librerías externas) para HeyGen HyperFrames.
Timeline de 12 segundos dividido en 4 escenas de 3 segundos cada una,
sincronizadas contra un único reloj CSS (`animation: ... 12s linear forwards`
en cada capa de escena, con puntos de corte en porcentajes exactos:
0s=0% · 3s=25% · 6s=50% · 9s=75% · 12s=100%).

Reemplaza los 4 placeholders por tus archivos reales antes de renderizar:

| Placeholder | Contenido |
|---|---|
| `logo_gym.png` | Logo del gimnasio |
| `gym_foto1.jpg` | Foto de la infraestructura general |
| `gym_foto2.jpg` | Foto de una máquina específica |
| `gym_foto3.jpg` | Foto entrenando/atendiendo |

## Código completo

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>WGYMADNSPORT — Video Promocional</title>
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

  .scene{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    opacity:0;
    visibility:hidden;
  }

  /* ============================================================
     ESCENA 1 — Logo + frase motivadora (0s - 3s | 0% - 25%)
     ============================================================ */
  .scene-1{
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    gap:64px;
    animation: scene1Life 12s linear forwards;
  }
  @keyframes scene1Life{
    0%      { opacity:0; visibility:visible; }
    2%      { opacity:1; }
    23%     { opacity:1; }
    25%     { opacity:0; visibility:hidden; }
    100%    { opacity:0; visibility:hidden; }
  }

  .s1-logo{
    width:340px;
    height:340px;
    object-fit:contain;
    animation: logoZoomFade 1.6s cubic-bezier(.19,1,.22,1) forwards;
    opacity:0;
    transform:scale(.6);
  }
  @keyframes logoZoomFade{
    0%   { opacity:0; transform:scale(.6); }
    100% { opacity:1; transform:scale(1); }
  }

  .s1-phrase{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:0 22px;
    max-width:880px;
    text-align:center;
  }
  .s1-phrase span{
    font-size:88px;
    line-height:1.05;
    color:var(--paper);
    text-transform:uppercase;
    letter-spacing:.01em;
    opacity:0;
    transform:translateY(40px);
    animation: wordIn .6s cubic-bezier(.19,1,.22,1) forwards;
  }
  .s1-phrase span.accent{ color:var(--red); }
  /* aparición palabra por palabra, escalonada dentro de 0.9s - 2.4s */
  .s1-phrase span:nth-child(1){ animation-delay:.9s; }
  .s1-phrase span:nth-child(2){ animation-delay:1.35s; }
  .s1-phrase span:nth-child(3){ animation-delay:1.8s; }
  .s1-phrase span:nth-child(4){ animation-delay:2.25s; }
  @keyframes wordIn{
    0%   { opacity:0; transform:translateY(40px); }
    100% { opacity:1; transform:translateY(0); }
  }

  /* ============================================================
     ESCENA 2 — Foto infraestructura + panel de beneficio
     (3s - 6s | 25% - 50%)
     ============================================================ */
  .scene-2{ animation: scene2Life 12s linear forwards; }
  @keyframes scene2Life{
    0%      { opacity:0; visibility:hidden; }
    25%     { opacity:0; visibility:visible; }
    27%     { opacity:1; }
    48%     { opacity:1; }
    50%     { opacity:0; visibility:hidden; }
    100%    { opacity:0; visibility:hidden; }
  }

  .s2-photo{
    position:absolute;
    top:0; left:0; right:0;
    height:55%;
    overflow:hidden;
  }
  .s2-photo img{
    width:100%; height:100%; object-fit:cover;
    transform:scale(1.12);
    animation: photoSettle 3s ease-out forwards;
    animation-delay:0s;
  }
  @keyframes photoSettle{
    0%   { transform:scale(1.12); filter:brightness(.7); }
    100% { transform:scale(1);    filter:brightness(1); }
  }
  .s2-photo::after{
    content:"";
    position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(5,5,5,0) 55%, var(--ink) 100%);
  }

  .s2-panel{
    position:absolute;
    left:56px; right:56px;
    bottom:220px;
    background:var(--panel);
    border:3px solid var(--red);
    border-radius:28px;
    padding:48px 52px;
    opacity:0;
    transform:translateY(60px);
    animation: panelRise .7s cubic-bezier(.19,1,.22,1) forwards;
    animation-delay:.5s;
  }
  @keyframes panelRise{
    0%   { opacity:0; transform:translateY(60px); }
    100% { opacity:1; transform:translateY(0); }
  }
  .s2-panel .kicker{
    font-size:26px;
    letter-spacing:.22em;
    color:var(--red);
    text-transform:uppercase;
    margin-bottom:14px;
  }
  .s2-panel .headline{
    font-size:56px;
    line-height:1.15;
    color:var(--paper);
    text-transform:uppercase;
  }

  /* ============================================================
     ESCENA 3 — Split máquina + entrenamiento
     (6s - 9s | 50% - 75%)
     ============================================================ */
  .scene-3{ animation: scene3Life 12s linear forwards; }
  @keyframes scene3Life{
    0%      { opacity:0; visibility:hidden; }
    50%     { opacity:0; visibility:visible; }
    52%     { opacity:1; }
    73%     { opacity:1; }
    75%     { opacity:0; visibility:hidden; }
    100%    { opacity:0; visibility:hidden; }
  }

  .s3-split{
    position:absolute; inset:0;
    display:flex;
    flex-direction:column;
  }
  .s3-half{
    position:relative;
    width:100%;
    height:50%;
    overflow:hidden;
  }
  .s3-half img{
    width:100%; height:100%; object-fit:cover;
  }
  .s3-half.top{
    animation: slideFromLeft .7s cubic-bezier(.19,1,.22,1) forwards;
  }
  .s3-half.bottom{
    animation: slideFromRight .7s cubic-bezier(.19,1,.22,1) forwards;
    animation-delay:.15s;
  }
  @keyframes slideFromLeft{
    0%   { transform:translateX(-100%); opacity:0; }
    100% { transform:translateX(0);     opacity:1; }
  }
  @keyframes slideFromRight{
    0%   { transform:translateX(100%); opacity:0; }
    100% { transform:translateX(0);    opacity:1; }
  }
  .s3-divider{
    position:absolute;
    top:50%; left:0; right:0;
    height:6px;
    background:var(--red);
    transform:translateY(-50%) scaleX(0);
    transform-origin:center;
    animation: dividerGrow .5s ease-out forwards;
    animation-delay:.55s;
    z-index:2;
  }
  @keyframes dividerGrow{
    0%   { transform:translateY(-50%) scaleX(0); }
    100% { transform:translateY(-50%) scaleX(1); }
  }

  /* ============================================================
     ESCENA 4 — Cierre / CTA
     (9s - 12s | 75% - 100%)
     ============================================================ */
  .scene-4{
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    gap:56px;
    animation: scene4Life 12s linear forwards;
  }
  @keyframes scene4Life{
    0%      { opacity:0; visibility:hidden; }
    75%     { opacity:0; visibility:visible; }
    77%     { opacity:1; }
    100%    { opacity:1; }
  }

  .s4-logo{
    width:300px;
    height:300px;
    object-fit:contain;
    opacity:0;
    transform:scale(.5);
    animation: logoZoomFade .8s cubic-bezier(.19,1,.22,1) forwards;
    animation-delay:.2s;
  }

  .s4-cta{
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
    animation-delay:1s;
  }
  @keyframes ctaPulseIn{
    0%   { opacity:0; transform:scale(.7); }
    70%  { opacity:1; transform:scale(1.08); }
    100% { opacity:1; transform:scale(1); }
  }

  .s4-contact{
    display:flex;
    flex-direction:column;
    align-items:center;
    gap:12px;
    opacity:0;
    transform:translateY(50px);
    animation: contactRise .7s cubic-bezier(.19,1,.22,1) forwards;
    animation-delay:1.8s;
  }
  @keyframes contactRise{
    0%   { opacity:0; transform:translateY(50px); }
    100% { opacity:1; transform:translateY(0); }
  }
  .s4-contact .handle{
    font-size:34px;
    color:var(--gold);
    letter-spacing:.1em;
  }
  .s4-contact .place{
    font-size:26px;
    color:var(--paper);
    letter-spacing:.14em;
    text-transform:uppercase;
    opacity:.85;
  }
</style>
</head>
<body>

  <div class="stage">

    <!-- ESCENA 1 · 0s-3s -->
    <section class="scene scene-1" data-start="0" data-end="3">
      <img class="s1-logo" src="logo_gym.png" alt="Logo del gimnasio">
      <div class="s1-phrase">
        <span>SUPERA</span>
        <span>TUS</span>
        <span class="accent">LÍMITES</span>
        <span>HOY</span>
      </div>
    </section>

    <!-- ESCENA 2 · 3s-6s -->
    <section class="scene scene-2" data-start="3" data-end="6">
      <div class="s2-photo">
        <img src="gym_foto1.jpg" alt="Infraestructura del gimnasio">
      </div>
      <div class="s2-panel">
        <div class="kicker">Beneficio clave</div>
        <div class="headline">Equipamiento completo para todos los niveles</div>
      </div>
    </section>

    <!-- ESCENA 3 · 6s-9s -->
    <section class="scene scene-3" data-start="6" data-end="9">
      <div class="s3-split">
        <div class="s3-half top">
          <img src="gym_foto2.jpg" alt="Máquina específica del gimnasio">
        </div>
        <div class="s3-half bottom">
          <img src="gym_foto3.jpg" alt="Entrenamiento personalizado">
        </div>
      </div>
      <div class="s3-divider"></div>
    </section>

    <!-- ESCENA 4 · 9s-12s -->
    <section class="scene scene-4" data-start="9" data-end="12">
      <img class="s4-logo" src="logo_gym.png" alt="Logo del gimnasio">
      <div class="s4-cta">¡Inscríbete hoy!</div>
      <div class="s4-contact">
        <div class="handle">@wadnsport.tocopilla</div>
        <div class="place">WGYMADNSPORT · Tocopilla</div>
      </div>
    </section>

  </div>

</body>
</html>
```

## Notas de implementación

- **Reloj único**: las 4 escenas comparten `animation-duration: 12s` con
  `linear`, y cada una entra/sale exactamente en su ventana (0-25%,
  25-50%, 50-75%, 75-100%) — así no hay que sincronizar temporizadores
  por separado, todo corre contra el mismo reloj de 12s.
- **`data-start` / `data-end`**: quedaron como atributos explícitos en
  cada `<section class="scene">` en segundos reales (0, 3, 6, 9, 12)
  para que HyperFrames los lea directo si su motor de timeline los
  usa como anclas; si tu versión de HyperFrames espera otro formato de
  marcador de tiempo, son el punto exacto donde ajustarlo sin tocar el
  resto del CSS.
- **Palabra por palabra** (Escena 1): cada `<span>` tiene su propio
  `animation-delay`, repartido dentro de la ventana 0-3s. Si cambias la
  frase, ajusta la cantidad de `nth-child(n)` y sus delays.
- **Sin librerías externas**: tipografía con pila de fuentes de sistema
  en negrita (`Arial Black`, `Impact`) — no depende de ninguna carga de
  red, coherente con la regla de que las apps del gimnasio no deben
  fallar sin internet.
- **Reemplazo de imágenes**: los 4 `src` (`logo_gym.png`, `gym_foto1.jpg`,
  `gym_foto2.jpg`, `gym_foto3.jpg`) son los únicos cambios necesarios
  para usar tus archivos reales — mantén esos nombres exactos o
  actualiza las rutas en el HTML.
