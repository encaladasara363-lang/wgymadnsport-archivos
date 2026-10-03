/* ═══════════════════════════════════════════════════════════════════════
   INGRESOS Y SALIDAS (10/2026)
   Archivo nuevo del proyecto de Apps Script del check-in ("Ingresos.gs").
   Se pega completo, tal cual, como un archivo aparte: no reemplaza nada
   de Código.gs.

   Hoja de ingresos (la primera de la planilla):
     A Fecha (ts) · B Nombre · C Apellido · D Vencimiento   ← como siempre
     E Salida · F Origen salida · G Código tarjeta           ← nuevas
   Nunca se borra ni se reordena una fila.

   Quién puede hacer qué:
   - Cualquiera (sin clave, como hoy la lista de ingresos):
       listarIngresos  → todos los ingresos de un día (fecha de Chile).
       miIngreso       → el estado de UNA persona hoy.
       ingresoTarjeta  → registra el ingreso desde la tarjeta virtual, pero
                         SOLO si esa persona todavía no tiene ingreso hoy.
                         Abrir la tarjeta otra vez (dentro o ya salida) no
                         crea otra fila. Volver a entrar después de salir
                         se pide aparte (forzar=1).
       salidaSocio     → el socio marca SU salida. Exige el código privado
                         que recibió SU teléfono al registrar el ingreso.
   - Solo administración (por POST, con la clave de administración, la
     misma ADMIN_KEY de guardarSocio):
       registrarSalida → marca la salida de cualquier persona.
       quitarSalida    → deshace una salida marcada por error.
   ═══════════════════════════════════════════════════════════════════════ */

var TZ_INGRESOS_ = "America/Santiago";

/* La columna A trae la hora en milisegundos. Las primeras filas de agosto
   quedaron como fecha de Sheets: también se aceptan. */
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

/* Las filas se agregan en orden de llegada: se lee de abajo hacia arriba,
   por tramos, y se para después de 30 filas seguidas de días anteriores.
   Para "hoy" son unas pocas filas, no las miles de la hoja. Lo más nuevo
   primero. */
function filasDelDia_(sheet, dia) {
  var out = [];
  var fin = sheet.getLastRow();
  var TRAMO = 400, anteriores = 0;
  while (fin >= 2 && anteriores < 30) {
    var ini = Math.max(2, fin - TRAMO + 1);
    var vals = sheet.getRange(ini, 1, fin - ini + 1, 7).getValues();
    for (var i = vals.length - 1; i >= 0; i--) {
      var ts = tsDeCelda_(vals[i][0]);
      if (!ts) continue;
      var d = diaCL_(ts);
      if (d === dia) {
        anteriores = 0;
        out.push({
          fila: ini + i,
          ts: ts,
          nombre: String(vals[i][1]),
          apellido: String(vals[i][2]),
          venc: String(vals[i][3] || ""),
          salida: tsDeCelda_(vals[i][4]),
          origen: String(vals[i][5] || ""),
          codigo: String(vals[i][6] || "")
        });
      } else if (d < dia) {
        anteriores++;
        if (anteriores >= 30) break;
      }
    }
    fin = ini - 1;
  }
  return out;
}

/* Lo que se publica de cada fila: nunca el código de la tarjeta. */
function filaPublica_(r) {
  return { fila: r.fila, ts: r.ts, nombre: r.nombre, apellido: r.apellido,
           venc: r.venc, salida: r.salida, origen: r.origen };
}

function mismaPersona_(r, nombre, apellido) {
  return normNombre_(r.nombre) === nombre && normNombre_(r.apellido) === apellido;
}

function estadoPersona_(mias, codigo) {
  var abiertas = mias.filter(function (r) { return !r.salida; });
  var ultimaSalida = 0;
  mias.forEach(function (r) { if (r.salida > ultimaSalida) ultimaSalida = r.salida; });
  return {
    ok: true,
    ingresos: true,
    vino: mias.length > 0,
    dentro: abiertas.length > 0,
    desde: abiertas.length ? abiertas[abiertas.length - 1].ts : 0,
    salida: abiertas.length ? 0 : ultimaSalida,
    /* true solo si este teléfono registró uno de los ingresos abiertos */
    puedeMarcar: !!codigo && abiertas.some(function (r) { return r.codigo === codigo; })
  };
}

function marcarHeaders_(sheet) {
  if (!sheet.getRange(1, 5).getValue()) {
    sheet.getRange(1, 5, 1, 3).setValues([["Salida", "Origen salida", "Código tarjeta"]]);
  }
}

function conCandado_(e, fn) {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return respond_(e, { ok: false, error: "ocupado, intenta de nuevo" });
  try { return fn(); } finally { lock.releaseLock(); }
}

/* ── públicas (GET) ─────────────────────────────────────────────────── */

function listarIngresos_(e) {
  var dia = diaPedido_(e.parameter);
  var rows = filasDelDia_(getSheet_(), dia).map(filaPublica_);
  return respond_(e, { ok: true, ingresos: true, dia: dia, hoy: diaCL_(Date.now()), rows: rows });
}

function miIngreso_(e) {
  var p = e.parameter;
  var nombre = normNombre_(p.nombre), apellido = normNombre_(p.apellido);
  if (!nombre || !apellido) return respond_(e, { ok: false, error: "faltan datos" });
  var mias = filasDelDia_(getSheet_(), diaCL_(Date.now())).filter(function (r) {
    return mismaPersona_(r, nombre, apellido);
  });
  return respond_(e, estadoPersona_(mias, String(p.codigo || "")));
}

function ingresoTarjeta_(e) {
  var p = e.parameter;
  var nombreTxt = String(p.nombre || ""), apellidoTxt = String(p.apellido || "");
  var nombre = normNombre_(nombreTxt), apellido = normNombre_(apellidoTxt);
  if (!nombre || !apellido) return respond_(e, { ok: false, error: "faltan datos" });
  var forzar = p.forzar === "1";
  return conCandado_(e, function () {
    var sheet = getSheet_();
    var mias = filasDelDia_(sheet, diaCL_(Date.now())).filter(function (r) {
      return mismaPersona_(r, nombre, apellido);
    });
    var estado = estadoPersona_(mias, String(p.codigo || ""));
    /* Ya vino hoy: abrir la tarjeta es solo una consulta. Volver a entrar
       (forzar) solo se acepta si ya tiene la salida marcada. */
    if (mias.length && (!forzar || estado.dentro)) {
      estado.registrado = false;
      return respond_(e, estado);
    }
    marcarHeaders_(sheet);
    var codigo = Utilities.getUuid();
    var ahora = Date.now();
    sheet.appendRow([ahora, nombreTxt, apellidoTxt, "", "", "", codigo]);
    var vencCell = sheet.getRange(sheet.getLastRow(), 4);
    vencCell.setNumberFormat("@");
    vencCell.setValue(String(p.venc || ""));
    return respond_(e, { ok: true, ingresos: true, registrado: true, codigo: codigo,
                         vino: true, dentro: true, desde: ahora, salida: 0, puedeMarcar: true });
  });
}

function salidaSocio_(e) {
  var p = e.parameter;
  var nombre = normNombre_(p.nombre), apellido = normNombre_(p.apellido);
  var codigo = String(p.codigo || "");
  if (!nombre || !apellido || !codigo) return respond_(e, { ok: false, error: "faltan datos" });
  return conCandado_(e, function () {
    var sheet = getSheet_();
    var abiertas = filasDelDia_(sheet, diaCL_(Date.now())).filter(function (r) {
      return !r.salida && mismaPersona_(r, nombre, apellido);
    });
    if (!abiertas.length) return respond_(e, { ok: true, ingresos: true, cerradas: 0 });
    var suya = abiertas.some(function (r) { return r.codigo === codigo; });
    if (!suya) return respond_(e, { ok: false, error: "no autorizado" });
    var ahora = Date.now();
    abiertas.forEach(function (r) { sheet.getRange(r.fila, 5, 1, 2).setValues([[ahora, "tarjeta"]]); });
    return respond_(e, { ok: true, ingresos: true, cerradas: abiertas.length, salida: ahora });
  });
}

/* ── solo administración (POST con clave) ───────────────────────────── */

function registrarSalida_(e) {
  var p = e.parameter;
  if (!claveValida_(p)) return respond_(e, { ok: false, error: "clave incorrecta" });
  var nombre = normNombre_(p.nombre), apellido = normNombre_(p.apellido);
  if (!nombre || !apellido) return respond_(e, { ok: false, error: "faltan datos" });
  return conCandado_(e, function () {
    var sheet = getSheet_();
    marcarHeaders_(sheet);
    var ahora = Date.now(), cerradas = 0;
    filasDelDia_(sheet, diaPedido_(p)).forEach(function (r) {
      if (!r.salida && mismaPersona_(r, nombre, apellido)) {
        sheet.getRange(r.fila, 5, 1, 2).setValues([[ahora, "recepcion"]]);
        cerradas++;
      }
    });
    return respond_(e, { ok: true, ingresos: true, cerradas: cerradas, salida: ahora });
  });
}

function quitarSalida_(e) {
  var p = e.parameter;
  if (!claveValida_(p)) return respond_(e, { ok: false, error: "clave incorrecta" });
  var fila = Number(p.fila), ts = Number(p.ts);
  if (!(fila >= 2) || !ts) return respond_(e, { ok: false, error: "faltan datos" });
  return conCandado_(e, function () {
    var sheet = getSheet_();
    if (fila > sheet.getLastRow() || tsDeCelda_(sheet.getRange(fila, 1).getValue()) !== ts) {
      return respond_(e, { ok: false, error: "no encontrado" });
    }
    sheet.getRange(fila, 5, 1, 2).setValues([["", ""]]);
    return respond_(e, { ok: true, ingresos: true });
  });
}

/* ── las dos entradas que llama Código.gs ───────────────────────────── */

function accionIngresos_(e) {
  switch (e.parameter.action) {
    case "listarIngresos": return listarIngresos_(e);
    case "miIngreso": return miIngreso_(e);
    case "ingresoTarjeta": return ingresoTarjeta_(e);
    case "salidaSocio": return salidaSocio_(e);
  }
  return null;
}

function accionIngresosPost_(e) {
  switch (e.parameter.action) {
    case "registrarSalida": return registrarSalida_(e);
    case "quitarSalida": return quitarSalida_(e);
  }
  return null;
}
