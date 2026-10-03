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
       miIngreso       → el estado de UNA persona hoy, más cuántas personas
                         hay dentro ahora (solo el número, sin nombres).
       ingresoTarjeta  → registra el ingreso desde la tarjeta virtual. La
                         tarjeta solo la llama cuando se abrió con el QR de
                         la PUERTA (tarjeta.html?ingreso=puerta), con
                         forzar=1. Cada escaneo es una visita nueva (hay
                         socios que vienen 2 o 3 veces al día): si quedó
                         abierto un ingreso anterior sin salida, se cierra
                         solo (origen "nueva visita") y se agrega el nuevo.
                         Solo si escanea otra vez antes de MIN_NUEVA_VISITA_
                         minutos desde su último ingreso, no se duplica.
                         Abrir la tarjeta por cualquier otro enlace solo
                         consulta (miIngreso).
       salidaSocio     → el socio marca SU salida desde su tarjeta. Desde
                         el 03-10-2026 no exige el código privado del
                         teléfono (muchos Android escanean en un navegador
                         y abren la tarjeta en otro, y el código no
                         estaba): basta con su nombre, igual que para
                         entrar. Solo cierra los ingresos de ESA persona;
                         sin el código queda con origen "tarjeta sin
                         codigo", y recepción lo deshace si hiciera falta.
   - Solo administración (por POST, con la clave de administración, la
     misma ADMIN_KEY de guardarSocio):
       registrarIngreso → respaldo del mesón: registra la entrada de quien
                         llegó sin escanear (misma regla de visita nueva).
       registrarSalida → marca la salida de cualquier persona.
       quitarSalida    → deshace una salida marcada por error.

   Modo prueba: si la llamada trae prueba=1 (lo mandan solo las páginas
   prueba-*.html), todo se lee y se escribe en otra hoja de la misma
   planilla, "Pruebas ingresos", nunca en la hoja real de ingresos. Así
   las pruebas no aparecen en las pantallas reales ni en ninguna
   estadística, y se pueden borrar después sin tocar nada real.
   ═══════════════════════════════════════════════════════════════════════ */

var TZ_INGRESOS_ = "America/Santiago";
var HOJA_PRUEBAS_ = "Pruebas ingresos";
/* Un escaneo antes de estos minutos desde el último ingreso de la misma
   persona es el mismo ingreso (escaneó dos veces); después, es otra visita. */
var MIN_NUEVA_VISITA_ = 30;

/* La hoja real de ingresos, o la de pruebas si la llamada trae prueba=1. */
function hojaIngresos_(p) {
  if (String(p.prueba || "") !== "1") return getSheet_();
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var hoja = ss.getSheetByName(HOJA_PRUEBAS_);
  if (!hoja) {
    hoja = ss.insertSheet(HOJA_PRUEBAS_);
    hoja.appendRow(["Fecha", "Nombre", "Apellido", "Vencimiento", "Salida", "Origen salida", "Código tarjeta"]);
  }
  return hoja;
}

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

/* Cuántas personas distintas tienen ingreso hoy sin salida (solo el
   número: la tarjeta del socio nunca recibe nombres de otros). */
function contarDentro_(filas) {
  var vistos = {}, n = 0;
  filas.forEach(function (r) {
    if (r.salida) return;
    var k = normNombre_(r.nombre) + "|" + normNombre_(r.apellido);
    if (!vistos[k]) { vistos[k] = true; n++; }
  });
  return n;
}

function estadoDe_(todas, nombre, apellido, codigo) {
  var mias = todas.filter(function (r) { return mismaPersona_(r, nombre, apellido); });
  var estado = estadoPersona_(mias, codigo);
  estado.dentroAhora = contarDentro_(todas);
  return estado;
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
    puedeMarcar: !!codigo && abiertas.some(function (r) { return r.codigo === codigo; }),
    /* La tarjeta muestra "Registrar mi salida" aunque este teléfono no
       tenga el código (ver salidaSocio). */
    salidaLibre: true
  };
}

/* Antes de agregar una visita nueva: si la persona tiene un ingreso
   abierto de hace menos de MIN_NUEVA_VISITA_ minutos, es el mismo ingreso
   (devuelve false: no agregar). Si es más antiguo, se fue sin marcar la
   salida: se cierran sus ingresos abiertos con la hora actual y origen
   "nueva visita" (devuelve true: agregar la visita nueva). */
function prepararNuevaVisita_(sheet, todas, nombre, apellido, ahora) {
  var abiertas = todas.filter(function (r) { return !r.salida && mismaPersona_(r, nombre, apellido); });
  var ultimo = 0;
  abiertas.forEach(function (r) { if (r.ts > ultimo) ultimo = r.ts; });
  if (ultimo && ahora - ultimo < MIN_NUEVA_VISITA_ * 60000) return false;
  if (abiertas.length) marcarHeaders_(sheet);
  abiertas.forEach(function (r) {
    sheet.getRange(r.fila, 5, 1, 2).setValues([[ahora, "nueva visita"]]);
  });
  return true;
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
  var rows = filasDelDia_(hojaIngresos_(e.parameter), dia).map(filaPublica_);
  return respond_(e, { ok: true, ingresos: true, dia: dia, hoy: diaCL_(Date.now()), rows: rows });
}

function miIngreso_(e) {
  var p = e.parameter;
  var nombre = normNombre_(p.nombre), apellido = normNombre_(p.apellido);
  if (!nombre || !apellido) return respond_(e, { ok: false, error: "faltan datos" });
  var todas = filasDelDia_(hojaIngresos_(e.parameter), diaCL_(Date.now()));
  return respond_(e, estadoDe_(todas, nombre, apellido, String(p.codigo || "")));
}

function ingresoTarjeta_(e) {
  var p = e.parameter;
  var nombreTxt = String(p.nombre || ""), apellidoTxt = String(p.apellido || "");
  var nombre = normNombre_(nombreTxt), apellido = normNombre_(apellidoTxt);
  if (!nombre || !apellido) return respond_(e, { ok: false, error: "faltan datos" });
  var forzar = p.forzar === "1";
  return conCandado_(e, function () {
    var sheet = hojaIngresos_(p);
    var todas = filasDelDia_(sheet, diaCL_(Date.now()));
    var estado = estadoDe_(todas, nombre, apellido, String(p.codigo || ""));
    var ahora = Date.now();
    /* Sin forzar (abrir la tarjeta sin el QR de la puerta) y ya vino hoy:
       solo consulta. Con el QR de la puerta, cada visita cuenta. */
    if ((estado.vino && !forzar) || !prepararNuevaVisita_(sheet, todas, nombre, apellido, ahora)) {
      estado.registrado = false;
      return respond_(e, estado);
    }
    marcarHeaders_(sheet);
    var codigo = Utilities.getUuid();
    sheet.appendRow([ahora, nombreTxt, apellidoTxt, "", "", "", codigo]);
    var vencCell = sheet.getRange(sheet.getLastRow(), 4);
    vencCell.setNumberFormat("@");
    vencCell.setValue(String(p.venc || ""));
    var resp = estadoDe_(filasDelDia_(sheet, diaCL_(ahora)), nombre, apellido, codigo);
    resp.registrado = true;
    resp.codigo = codigo;
    return respond_(e, resp);
  });
}

function salidaSocio_(e) {
  var p = e.parameter;
  var nombre = normNombre_(p.nombre), apellido = normNombre_(p.apellido);
  var codigo = String(p.codigo || "");
  if (!nombre || !apellido) return respond_(e, { ok: false, error: "faltan datos" });
  return conCandado_(e, function () {
    var sheet = hojaIngresos_(p);
    var todas = filasDelDia_(sheet, diaCL_(Date.now()));
    var abiertas = todas.filter(function (r) {
      return !r.salida && mismaPersona_(r, nombre, apellido);
    });
    if (!abiertas.length) return respond_(e, { ok: true, ingresos: true, cerradas: 0, dentroAhora: contarDentro_(todas) });
    var suya = !!codigo && abiertas.some(function (r) { return r.codigo === codigo; });
    var origen = suya ? "tarjeta" : "tarjeta sin codigo";
    var ahora = Date.now();
    abiertas.forEach(function (r) {
      sheet.getRange(r.fila, 5, 1, 2).setValues([[ahora, origen]]);
      r.salida = ahora;
    });
    return respond_(e, { ok: true, ingresos: true, cerradas: abiertas.length, salida: ahora,
                         dentroAhora: contarDentro_(todas) });
  });
}

/* ── solo administración (POST con clave) ───────────────────────────── */

function registrarIngreso_(e) {
  var p = e.parameter;
  if (!claveValida_(p)) return respond_(e, { ok: false, error: "clave incorrecta" });
  var nombreTxt = String(p.nombre || ""), apellidoTxt = String(p.apellido || "");
  var nombre = normNombre_(nombreTxt), apellido = normNombre_(apellidoTxt);
  if (!nombre || !apellido) return respond_(e, { ok: false, error: "faltan datos" });
  return conCandado_(e, function () {
    var sheet = hojaIngresos_(p);
    var todas = filasDelDia_(sheet, diaCL_(Date.now()));
    var estado = estadoDe_(todas, nombre, apellido, "");
    var ahora = Date.now();
    if (!prepararNuevaVisita_(sheet, todas, nombre, apellido, ahora)) {
      return respond_(e, { ok: true, ingresos: true, registrado: false, dentro: true, desde: estado.desde,
                           dentroAhora: estado.dentroAhora });
    }
    marcarHeaders_(sheet);
    sheet.appendRow([ahora, nombreTxt, apellidoTxt, "", "", "", ""]);
    var vencCell = sheet.getRange(sheet.getLastRow(), 4);
    vencCell.setNumberFormat("@");
    vencCell.setValue(String(p.venc || ""));
    return respond_(e, { ok: true, ingresos: true, registrado: true, ts: ahora,
                         dentroAhora: estado.dentroAhora + (estado.dentro ? 0 : 1) });
  });
}

function registrarSalida_(e) {
  var p = e.parameter;
  if (!claveValida_(p)) return respond_(e, { ok: false, error: "clave incorrecta" });
  var nombre = normNombre_(p.nombre), apellido = normNombre_(p.apellido);
  if (!nombre || !apellido) return respond_(e, { ok: false, error: "faltan datos" });
  return conCandado_(e, function () {
    var sheet = hojaIngresos_(p);
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
    var sheet = hojaIngresos_(p);
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
    case "registrarIngreso": return registrarIngreso_(e);
    case "registrarSalida": return registrarSalida_(e);
    case "quitarSalida": return quitarSalida_(e);
  }
  return null;
}
