/* ═══════════════════════════════════════════════════════════════════════
   INGRESOS Y SALIDAS (10/2026)
   Archivo nuevo del proyecto de Apps Script del check-in ("Ingresos.gs").
   Se pega completo, tal cual, como un archivo aparte: no reemplaza nada
   de Código.gs.

   Qué agrega:
   - listarIngresos: TODOS los ingresos de un día (fecha de Chile), no solo
     los últimos 20. Lo usan control.html y pantalla.html.
   - registrarSalida: anota la hora de salida de un socio en la misma hoja
     de ingresos (columna E "Salida" y columna F "Origen salida"). La usan
     el botón "MARCAR SALIDA" de control.html y el de la tarjeta virtual.
   - quitarSalida: deshace una salida marcada por error (control.html).
   - miIngreso: le dice a la tarjeta de UN socio si está dentro o ya salió.

   La hoja de ingresos sigue igual: A Fecha (ts), B Nombre, C Apellido,
   D Vencimiento. Solo se empiezan a usar las columnas E y F, que hoy
   están vacías. Nunca se borra ni se reordena una fila.
   ═══════════════════════════════════════════════════════════════════════ */

var TZ_INGRESOS_ = "America/Santiago";

/* La columna A trae la hora en milisegundos (número). Las primeras filas
   de agosto quedaron como fecha de Sheets: también se aceptan. */
function tsDeCelda_(v) {
  if (v instanceof Date) return v.getTime();
  var n = Number(v);
  return n > 1e12 ? n : 0;
}

function diaCL_(ts) {
  return Utilities.formatDate(new Date(ts), TZ_INGRESOS_, "yyyy-MM-dd");
}

function diaPedido_(p) {
  var d = String(p.dia || "");
  return /^\d{4}-\d{2}-\d{2}$/.test(d) ? d : diaCL_(Date.now());
}

/* Las filas se agregan en orden de llegada, así que se lee de abajo hacia
   arriba, por tramos, y se para cuando ya pasó varias filas seguidas de
   días anteriores. Para "hoy" eso significa leer unas pocas filas, no las
   miles que tiene la hoja. Devuelve lo más nuevo primero. */
function filasDelDia_(sheet, dia) {
  var out = [];
  var fin = sheet.getLastRow();
  var TRAMO = 400, anterioresSeguidas = 0;
  while (fin >= 2 && anterioresSeguidas < 30) {
    var ini = Math.max(2, fin - TRAMO + 1);
    var vals = sheet.getRange(ini, 1, fin - ini + 1, 6).getValues();
    for (var i = vals.length - 1; i >= 0; i--) {
      var ts = tsDeCelda_(vals[i][0]);
      if (!ts) continue;
      var d = diaCL_(ts);
      if (d === dia) {
        anterioresSeguidas = 0;
        out.push({
          fila: ini + i,
          ts: ts,
          nombre: String(vals[i][1]),
          apellido: String(vals[i][2]),
          venc: String(vals[i][3] || ""),
          salida: tsDeCelda_(vals[i][4]),
          origen: String(vals[i][5] || "")
        });
      } else if (d < dia) {
        anterioresSeguidas++;
        if (anterioresSeguidas >= 30) break;
      }
    }
    fin = ini - 1;
  }
  return out;
}

function listarIngresos_(e) {
  var dia = diaPedido_(e.parameter);
  var rows = filasDelDia_(getSheet_(), dia);
  return respond_(e, { ok: true, ingresos: true, dia: dia, hoy: diaCL_(Date.now()), rows: rows });
}

function mismaPersona_(r, nombre, apellido) {
  return normNombre_(r.nombre) === nombre && normNombre_(r.apellido) === apellido;
}

/* Cierra TODOS los ingresos abiertos de esa persona en ese día: si entró
   dos veces sin marcar salida, una sola salida deja las dos cerradas. */
function registrarSalida_(e) {
  var p = e.parameter;
  var nombre = normNombre_(p.nombre), apellido = normNombre_(p.apellido);
  if (!nombre || !apellido) return respond_(e, { ok: false, error: "faltan datos" });
  var origen = String(p.origen || "").slice(0, 20);
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return respond_(e, { ok: false, error: "ocupado, intenta de nuevo" });
  try {
    var sheet = getSheet_();
    if (!sheet.getRange(1, 5).getValue()) sheet.getRange(1, 5, 1, 2).setValues([["Salida", "Origen salida"]]);
    var ahora = Date.now(), cerradas = 0;
    filasDelDia_(sheet, diaPedido_(p)).forEach(function (r) {
      if (!r.salida && mismaPersona_(r, nombre, apellido)) {
        sheet.getRange(r.fila, 5, 1, 2).setValues([[ahora, origen]]);
        cerradas++;
      }
    });
    return respond_(e, { ok: true, ingresos: true, cerradas: cerradas, salida: ahora });
  } finally {
    lock.releaseLock();
  }
}

/* Deshace una salida marcada por error. Pide la fila y la hora de ingreso
   exacta, para no tocar nunca otra fila por equivocación. */
function quitarSalida_(e) {
  var p = e.parameter;
  var fila = Number(p.fila), ts = Number(p.ts);
  if (!(fila >= 2) || !ts) return respond_(e, { ok: false, error: "faltan datos" });
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return respond_(e, { ok: false, error: "ocupado, intenta de nuevo" });
  try {
    var sheet = getSheet_();
    if (fila > sheet.getLastRow() || tsDeCelda_(sheet.getRange(fila, 1).getValue()) !== ts) {
      return respond_(e, { ok: false, error: "no encontrado" });
    }
    sheet.getRange(fila, 5, 1, 2).setValues([["", ""]]);
    return respond_(e, { ok: true, ingresos: true });
  } finally {
    lock.releaseLock();
  }
}

/* Solo el estado de UNA persona (la tarjeta virtual no necesita ver a los
   demás socios). */
function miIngreso_(e) {
  var p = e.parameter;
  var nombre = normNombre_(p.nombre), apellido = normNombre_(p.apellido);
  if (!nombre || !apellido) return respond_(e, { ok: false, error: "faltan datos" });
  var mias = filasDelDia_(getSheet_(), diaPedido_(p)).filter(function (r) {
    return mismaPersona_(r, nombre, apellido);
  });
  var abiertas = mias.filter(function (r) { return !r.salida; });
  var ultimaSalida = 0;
  mias.forEach(function (r) { if (r.salida > ultimaSalida) ultimaSalida = r.salida; });
  return respond_(e, {
    ok: true,
    ingresos: true,
    vino: mias.length > 0,
    dentro: abiertas.length > 0,
    desde: abiertas.length ? abiertas[abiertas.length - 1].ts : 0,
    ultimoIngreso: mias.length ? mias[0].ts : 0,
    salida: abiertas.length ? 0 : ultimaSalida
  });
}

/* Las cuatro acciones nuevas. Código.gs las llama con UNA línea agregada
   dentro de doGet (ver docs/apps-script-ingresos-salidas.md). */
function accionIngresos_(e) {
  switch (e.parameter.action) {
    case "listarIngresos": return listarIngresos_(e);
    case "registrarSalida": return registrarSalida_(e);
    case "quitarSalida": return quitarSalida_(e);
    case "miIngreso": return miIngreso_(e);
  }
  return null;
}
