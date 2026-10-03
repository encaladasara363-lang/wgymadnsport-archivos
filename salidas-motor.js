/* Motor compartido para gestión de ingresos/salidas — se carga en control.html, pantalla.html, tarjeta.html */

const SalidasMotor = (function() {
  const VERSION_LOCAL = '1.0';
  const STORAGE_KEY = 'wgym_salidas_cache_v1';
  const ARCHIVO = 'salidas.json';
  const ZONA_HORA = 'America/Santiago';

  let cache = { version: '0', registros: [] };
  let ultimaCarguaLocal = 0;

  function formatoHora(d = new Date()) {
    return new Intl.DateTimeFormat('es-CL', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit',
      timeZone: ZONA_HORA
    }).format(d).replace(/(\d+)\/(\d+)\/(\d+)\s+(\d+):(\d+):(\d+)/, '$3-$2-$1T$4:$5:$6');
  }

  function horaISO(d = new Date()) {
    const h = String(d.getHours()).padStart(2, '0');
    const m = String(d.getMinutes()).padStart(2, '0');
    return `${h}:${m}`;
  }

  function fechaISO(d = new Date()) {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, '0');
    const dy = String(d.getDate()).padStart(2, '0');
    return `${y}-${m}-${dy}`;
  }

  async function cargar() {
    const ahora = Date.now();
    if (ahora - ultimaCarguaLocal < 2000) return cache;

    try {
      const resp = await fetch(ARCHIVO + '?t=' + ahora);
      if (resp.ok) {
        const datos = await resp.json();
        cache = datos;
        ultimaCarguaLocal = ahora;
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(cache));
        } catch (e) {}
      }
    } catch (e) {
      console.warn('No se pudo cargar salidas.json, usando cache local:', e);
      try {
        const local = localStorage.getItem(STORAGE_KEY);
        if (local) cache = JSON.parse(local);
      } catch (e2) {}
    }
    return cache;
  }

  function socioYaAdentro(n, a) {
    const hoy = fechaISO();
    const hoy5d = new Date();
    hoy5d.setDate(hoy5d.getDate() - 5);
    const hace5 = fechaISO(hoy5d);

    const regs = cache.registros.filter(r =>
      r.n === n && r.a === a && r.ingreso?.fecha >= hace5
    );

    if (!regs.length) return false;
    const ult = regs[regs.length - 1];
    return ult.ingreso && !ult.salida;
  }

  function registrarIngreso(n, a, marcadoPor = 'mesón') {
    const hoy = fechaISO();
    const hora = horaISO();

    const key = `${n}|${a}`;
    const regs = cache.registros.filter(r => `${r.n}|${r.a}` === key);

    if (regs.length) {
      const ult = regs[regs.length - 1];
      if (ult.ingreso && !ult.salida) {
        return { ok: false, msg: 'Ya está dentro' };
      }
    }

    const nuevoReg = {
      n, a,
      ingreso: { fecha: hoy, hora, zonaHora: ZONA_HORA, marcadoPor },
      salida: null
    };

    cache.registros.push(nuevoReg);
    subirCambios();
    return { ok: true, msg: 'Ingreso registrado', registro: nuevoReg };
  }

  async function registrarSalida(n, a, marcadoPor = 'mesón') {
    await cargar();

    const hoy = fechaISO();
    const hora = horaISO();

    const key = `${n}|${a}`;
    const regs = cache.registros.filter(r => `${r.n}|${r.a}` === key);

    if (!regs.length) {
      return { ok: false, msg: 'No hay ingreso registrado' };
    }

    const ult = regs[regs.length - 1];
    if (!ult.ingreso) {
      return { ok: false, msg: 'No hay ingreso válido' };
    }

    if (ult.salida) {
      return { ok: false, msg: 'Ya salió' };
    }

    ult.salida = { fecha: hoy, hora, zonaHora: ZONA_HORA, marcadoPor };
    subirCambios();

    return {
      ok: true,
      msg: 'Salida registrada',
      ingreso: ult.ingreso,
      salida: ult.salida
    };
  }

  function subirCambios() {
    const nuevoNum = String(parseInt(cache.version || '0') + 1).padStart(10, '0');
    cache.version = new Date().getFullYear().toString() +
                     String(new Date().getMonth() + 1).padStart(2, '0') +
                     String(new Date().getDate()).padStart(2, '0') +
                     nuevoNum.slice(-3);

    cache.actualizado = formatoHora();

    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cache));
    } catch (e) {}
  }

  function sociosDentro() {
    const hoy = fechaISO();
    const sociosDentroSet = new Set();

    cache.registros
      .filter(r => r.ingreso?.fecha === hoy && r.ingreso && !r.salida)
      .forEach(r => sociosDentroSet.add(`${r.n}|${r.a}`));

    return Array.from(sociosDentroSet).map(key => {
      const [n, a] = key.split('|');
      return { n, a };
    }).sort((a, b) => (a.a + a.n).localeCompare(b.a + b.n));
  }

  function obtenerUltimoIngreso(n, a) {
    const hoy = fechaISO();
    const regs = cache.registros
      .filter(r => r.n === n && r.a === a && r.ingreso?.fecha === hoy)
      .sort((a, b) => b.ingreso.hora.localeCompare(a.ingreso.hora));

    return regs[0] || null;
  }

  function estadisticasHorarias() {
    const haceNDias = 14;
    const haceND = new Date();
    haceND.setDate(haceND.getDate() - haceNDias);
    const limiteMin = fechaISO(haceND);

    const ingresosPorHora = {};
    const diasConDatos = new Set();

    cache.registros
      .filter(r => r.ingreso?.fecha >= limiteMin)
      .forEach(r => {
        diasConDatos.add(r.ingreso.fecha);
        const [hora] = r.ingreso.hora.split(':');
        const key = `${hora}:00`;
        ingresosPorHora[key] = (ingresosPorHora[key] || 0) + 1;
      });

    const diasUnicos = diasConDatos.size;

    if (diasUnicos < 2) {
      return { ok: false, msg: 'Datos insuficientes', diasUnicos };
    }

    const ranking = Object.entries(ingresosPorHora)
      .map(([hora, cant]) => ({ hora, ingresos: cant, promedio: (cant / diasUnicos).toFixed(1) }))
      .sort((a, b) => a.ingresos - b.ingresos);

    return {
      ok: true,
      diasUnicos,
      horariosMasTranquilos: ranking.slice(0, 5),
      horariosMasMovidos: ranking.slice(-5).reverse()
    };
  }

  return {
    cargar,
    registrarIngreso,
    registrarSalida,
    socioYaAdentro,
    sociosDentro,
    obtenerUltimoIngreso,
    estadisticasHorarias,
    getCache: () => cache,
    VERSION_LOCAL,
    ZONA_HORA
  };
})();
