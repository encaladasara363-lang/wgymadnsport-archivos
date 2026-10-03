/* UI para gestión de salidas — se inyecta en control.html, pantalla.html y tarjeta.html */

(async function() {
  'use strict';

  if (!window.SalidasMotor) {
    console.warn('SalidasMotor no cargado, saltando salidas-ui.js');
    return;
  }

  const Motor = window.SalidasMotor;

  async function mostrarSociosDentro() {
    if (!document.getElementById('salidasPanel')) return;

    await Motor.cargar();
    const dentro = Motor.sociosDentro();
    const container = document.getElementById('salidasPanel');

    if (!dentro.length) {
      container.innerHTML = '<div class="feed-empty">Nadie dentro en este momento.</div>';
      return;
    }

    container.innerHTML = dentro.map(s => {
      const reg = Motor.obtenerUltimoIngreso(s.n, s.a);
      const hora = reg?.ingreso?.hora || '—';
      return `
        <div class="feed-item" style="justify-content: space-between;">
          <div class="finfo">
            <span class="fname">${s.n} ${s.a}</span>
            <span style="font-size: 12px; color: var(--gris-soft);">Ingreso: ${hora}</span>
          </div>
          <button class="btn btn-rojo" data-n="${s.n}" data-a="${s.a}" style="flex-shrink: 0;">
            Marcar Salida
          </button>
        </div>
      `;
    }).join('');

    container.querySelectorAll('button').forEach(btn => {
      btn.addEventListener('click', async e => {
        const n = btn.dataset.n;
        const a = btn.dataset.a;
        const res = await Motor.registrarSalida(n, a, 'mesón');
        if (res.ok) {
          btn.disabled = true;
          btn.textContent = '✓ SALIDA MARCADA';
          setTimeout(() => mostrarSociosDentro(), 1000);
        } else {
          alert('Error: ' + res.msg);
        }
      });
    });
  }

  function actualizarContadorDentro() {
    const dentro = Motor.sociosDentro();
    const kpiDentro = document.querySelector('.kpi[data-tipo="dentro"]');
    if (kpiDentro) {
      kpiDentro.querySelector('.kval').textContent = dentro.length;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      mostrarSociosDentro();
      actualizarContadorDentro();
    });
  } else {
    mostrarSociosDentro();
    actualizarContadorDentro();
  }

  setInterval(async () => {
    await Motor.cargar();
    mostrarSociosDentro();
    actualizarContadorDentro();
  }, 3000);
})();
