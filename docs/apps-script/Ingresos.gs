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
  /* Todo lo que escribe en la hoja pasa por aquí: al terminar se borra la
     caché de la lista del día, para que el cambio se vea al tiro. */
  try { return fn(); } finally { borrarCacheIngresos_(e.parameter); lock.releaseLock(); }
}

/* ── públicas (GET) ─────────────────────────────────────────────────── */

/* Caché corta (Versión 11, 06-10-2026): con mesón, tablet y muchos
   celulares preguntando lo mismo, la hoja se leía decenas de veces por
   minuto y todo se ponía lento. La lista del día se guarda 15 s en la
   caché de Apps Script, y cualquier ingreso o salida la borra al tiro,
   así que nunca se muestra un dato viejo después de un cambio. */
var CACHE_SEG_ = 15;
function claveCache_(p, dia) { return "ing_" + (String(p.prueba || "") === "1" ? "p_" : "") + dia; }
function borrarCacheIngresos_(p) {
  try {
    var c = CacheService.getScriptCache(), hoy = diaCL_(Date.now());
    c.removeAll([claveCache_(p, hoy), claveCache_({}, hoy)]);
  } catch (err) {}
}

function listarIngresos_(e) {
  var dia = diaPedido_(e.parameter), clave = claveCache_(e.parameter, dia), cache = null;
  try { cache = CacheService.getScriptCache(); } catch (err) {}
  if (cache) {
    var guardado = cache.get(clave);
    if (guardado) {
      try { return respond_(e, JSON.parse(guardado)); } catch (err) {}
    }
  }
  var rows = filasDelDia_(hojaIngresos_(e.parameter), dia).map(filaPublica_);
  var resp = { ok: true, ingresos: true, dia: dia, hoy: diaCL_(Date.now()), rows: rows };
  if (cache) { try { cache.put(clave, JSON.stringify(resp), CACHE_SEG_); } catch (err) {} }
  return respond_(e, resp);
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


/* Días con ingreso por persona desde una fecha (máximo 75 días atrás),
   para que el mesón y la tablet cuenten el "día X de Y" con los mismos
   datos de la hoja (desde 05-10-2026). Solo nombre y días: sin horas,
   salidas ni códigos. */
function claveDias_(nombre, apellido) {
  return (String(nombre) + " " + String(apellido)).toUpperCase().normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "").replace(/\s+/g, " ").trim();
}

function diasDesde_(p, desde) {
  var sheet = hojaIngresos_(p);
  var dias = {};
  var fin = sheet.getLastRow();
  var TRAMO = 800, anteriores = 0;
  while (fin >= 2 && anteriores < 30) {
    var ini = Math.max(2, fin - TRAMO + 1);
    var vals = sheet.getRange(ini, 1, fin - ini + 1, 3).getValues();
    for (var i = vals.length - 1; i >= 0; i--) {
      var ts = tsDeCelda_(vals[i][0]);
      if (!ts) continue;
      var d = diaCL_(ts);
      if (d >= desde) {
        anteriores = 0;
        var k = claveDias_(vals[i][1], vals[i][2]);
        if (k) { if (!dias[k]) dias[k] = {}; dias[k][d] = 1; }
      } else {
        anteriores++;
        if (anteriores >= 30) break;
      }
    }
    fin = ini - 1;
  }
  return dias;
}

function asistenciaDesde_(e) {
  var p = e.parameter;
  var minimo = diaCL_(Date.now() - 75 * 864e5);
  var desde = String(p.desde || "");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(desde) || desde < minimo) desde = minimo;
  var dias = diasDesde_(p, desde);
  return respond_(e, { ok: true, asistencia: true, desde: desde, dias: dias });
}

/* ── WGYMNUTRI de pago (10-10-2026, la dueña: "venderla a $5.000 al mes") ──
   Hoja aparte "WGYMNUTRI" en la misma planilla: Nombre · Apellido ·
   Activa hasta (AAAA-MM-DD) · Actualizado. La activa la dueña desde la
   ficha del socio en el mesón (POST activarNutri con la clave de
   administración). La app pregunta listarNutri (público: solo nombre y
   fecha, como listarSocios). */
var HOJA_NUTRI_ = "WGYMNUTRI";
function hojaNutri_() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var hoja = ss.getSheetByName(HOJA_NUTRI_);
  if (!hoja) {
    hoja = ss.insertSheet(HOJA_NUTRI_);
    hoja.appendRow(["Nombre", "Apellido", "Activa hasta", "Actualizado"]);
    hoja.getRange("C:C").setNumberFormat("@");
  }
  return hoja;
}
function fechaNutri_(v) {
  if (v instanceof Date) return Utilities.formatDate(v, TZ_INGRESOS_, "yyyy-MM-dd");
  return String(v || "").trim();
}
function listarNutri_(e) {
  var cache = null;
  try { cache = CacheService.getScriptCache(); } catch (err) {}
  if (cache) {
    var g = cache.get("nutri_lista");
    if (g) { try { return respond_(e, JSON.parse(g)); } catch (err) {} }
  }
  var datos = hojaNutri_().getDataRange().getValues(), activos = [];
  for (var i = 1; i < datos.length; i++) {
    var h = fechaNutri_(datos[i][2]);
    if (datos[i][0] && h) activos.push({ n: String(datos[i][0]), a: String(datos[i][1] || ""), hasta: h });
  }
  var resp = { ok: true, nutri: true, hoy: diaCL_(Date.now()), activos: activos };
  if (cache) { try { cache.put("nutri_lista", JSON.stringify(resp), 30); } catch (err) {} }
  return respond_(e, resp);
}
function activarNutri_(e) {
  var p = e.parameter;
  if (!claveValida_(p)) return respond_(e, { ok: false, error: "clave incorrecta" });
  var nombreTxt = String(p.nombre || "").trim(), apellidoTxt = String(p.apellido || "").trim();
  var nombre = normNombre_(nombreTxt), apellido = normNombre_(apellidoTxt);
  var hasta = String(p.hasta || "").trim();          /* "" = quitar la activación */
  if (!nombre) return respond_(e, { ok: false, error: "faltan datos" });
  if (hasta && !/^\d{4}-\d{2}-\d{2}$/.test(hasta)) return respond_(e, { ok: false, error: "fecha inválida" });
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return respond_(e, { ok: false, error: "ocupado, intenta de nuevo" });
  try {
    var hoja = hojaNutri_(), datos = hoja.getDataRange().getValues(), fila = 0;
    for (var i = 1; i < datos.length; i++) {
      if (normNombre_(datos[i][0]) === nombre && normNombre_(datos[i][1]) === apellido) { fila = i + 1; break; }
    }
    var ahora = Utilities.formatDate(new Date(), TZ_INGRESOS_, "yyyy-MM-dd HH:mm");
    /* Si la fecha ya estaba guardada, es el mismo «Activar» tocado de nuevo (22-10-2026: Matías y José
       quedaron con 3 y 4 ventas iguales porque al mesón no le llegaba la respuesta): no se anota otra venta. */
    var repetida = fila && hasta && fechaNutri_(datos[fila - 1][2]) === hasta;
    if (fila) hoja.getRange(fila, 3, 1, 2).setValues([[hasta, ahora]]);
    else hoja.appendRow([nombreTxt, apellidoTxt, hasta, ahora]);
    /* Cada activación pagada queda anotada en «Ventas WGYMNUTRI» (18-10-2026, panel de ventas del mesón). */
    var meses = Number(p.meses) || 0, monto = Number(p.monto) || 0;
    if (hasta && meses > 0 && !repetida) hojaVentasNutri_().appendRow([ahora, nombreTxt, apellidoTxt, meses, monto]);
    try { CacheService.getScriptCache().remove("nutri_lista"); } catch (err) {}
    return respond_(e, { ok: true, nutri: true, hasta: hasta });
  } finally { lock.releaseLock(); }
}

/* ── Ventas de WGYMNUTRI (18-10-2026, la dueña eligió el panel de ventas en el mesón) ──
   Hoja «Ventas WGYMNUTRI»: Fecha · Nombre · Apellido · Meses · Monto. Solo la escribe
   activarNutri (con clave); ventasNutri (POST con la clave) entrega las del mes pedido. */
var HOJA_VENTAS_NUTRI_ = "Ventas WGYMNUTRI";
function hojaVentasNutri_() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var hoja = ss.getSheetByName(HOJA_VENTAS_NUTRI_);
  if (!hoja) {
    hoja = ss.insertSheet(HOJA_VENTAS_NUTRI_);
    hoja.appendRow(["Fecha", "Nombre", "Apellido", "Meses", "Monto"]);
    hoja.getRange("A:A").setNumberFormat("@");
  }
  return hoja;
}
function ventasNutri_(e) {
  if (!claveValida_(e.parameter)) return respond_(e, { ok: false, error: "clave incorrecta" });
  try {
    var mes = String(e.parameter.mes || "").trim();
    if (!/^\d{4}-\d{2}$/.test(mes)) mes = diaCL_(Date.now()).slice(0, 7);
    var datos = hojaVentasNutri_().getDataRange().getValues(), ventas = [], total = 0, totalTodo = 0;
    for (var i = 1; i < datos.length; i++) {
      var f = datos[i][0] instanceof Date ? Utilities.formatDate(datos[i][0], TZ_INGRESOS_, "yyyy-MM-dd HH:mm") : String(datos[i][0] || "");
      totalTodo += Number(datos[i][4]) || 0;   /* todo lo vendido desde que se anotan las ventas (22-10-2026) */
      if (f.slice(0, 7) !== mes) continue;
      var monto = Number(datos[i][4]) || 0; total += monto;
      ventas.push({ fila: i + 1, f: f, n: String(datos[i][1] || ""), a: String(datos[i][2] || ""), meses: Number(datos[i][3]) || 0, monto: monto });
    }
    return respond_(e, { ok: true, ventasNutri: true, borrar: true, mes: mes, ventas: ventas, total: total, totalTodo: totalTodo });
  } catch (err) { return respond_(e, { ok: false, error: String(err && err.message || err) }); }
}
/* 🗑 Borrar una venta desde el mesón (22-10-2026, la dueña: ventas repetidas). POST con la clave: fila +
   nombre, apellido y fecha de esa fila, para no borrar otra si la hoja cambió entre medio. */
function borrarVentaNutri_(e) {
  var p = e.parameter;
  if (!claveValida_(p)) return respond_(e, { ok: false, error: "clave incorrecta" });
  var fila = Number(p.fila) || 0;
  if (fila < 2) return respond_(e, { ok: false, error: "faltan datos" });
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return respond_(e, { ok: false, error: "ocupado, intenta de nuevo" });
  try {
    var hoja = hojaVentasNutri_();
    if (fila > hoja.getLastRow()) return respond_(e, { ok: false, error: "ya no está" });
    var r = hoja.getRange(fila, 1, 1, 3).getValues()[0];
    var f = r[0] instanceof Date ? Utilities.formatDate(r[0], TZ_INGRESOS_, "yyyy-MM-dd HH:mm") : String(r[0] || "");
    if (f !== String(p.f || "") || normNombre_(r[1]) !== normNombre_(p.nombre) || normNombre_(r[2]) !== normNombre_(p.apellido))
      return respond_(e, { ok: false, error: "la hoja cambió, actualiza e intenta de nuevo" });
    hoja.deleteRow(fila);
    return respond_(e, { ok: true });
  } finally { lock.releaseLock(); }
}

/* ── Productos escaneados de WGYMNUTRI (10-10-2026, la dueña: "escanear una
   vez y que quede para todos mis socios") ──────────────────────────────────
   Hoja aparte "Productos": Código · Nombre · Marca · Kcal/100 g · Prot/100 g ·
   Carb/100 g · Grasa/100 g · Porción g · Porción texto · Origen · Agregado ·
   Veces. Solo datos de etiquetas de productos (nada personal), por eso las dos
   acciones son públicas, como listarSocios:
     listarProductos → la lista completa (caché 2 min).
     guardarProducto → agrega un producto nuevo (lo escaneó un socio o lo creó
                       a mano con la etiqueta). Si el código ya existe, solo
                       suma 1 a "Veces": nunca pisa un producto guardado. Los
                       valores se revisan (rangos posibles) antes de guardar.
   Para corregir o borrar un producto, se edita o borra su fila en la hoja. */
var HOJA_PRODUCTOS_ = "Productos";
function hojaProductos_() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var hoja = ss.getSheetByName(HOJA_PRODUCTOS_);
  if (!hoja) {
    hoja = ss.insertSheet(HOJA_PRODUCTOS_);
    hoja.appendRow(["Código", "Nombre", "Marca", "Kcal/100 g", "Prot/100 g", "Carb/100 g", "Grasa/100 g", "Porción g", "Porción texto", "Origen", "Agregado", "Veces"]);
    hoja.getRange("A:A").setNumberFormat("@");
  }
  return hoja;
}
function listarProductos_(e) { try { return listarProductosReal_(e); } catch (err) { return respond_(e, { ok: false, error: String(err && err.message || err) }); } }
function listarProductosReal_(e) {
  var cache = null;
  try { cache = CacheService.getScriptCache(); } catch (err) {}
  if (cache) { var g = cache.get("productos_lista"); if (g) { try { return respond_(e, JSON.parse(g)); } catch (err) {} } }
  var datos = hojaProductos_().getDataRange().getValues(), lista = [];
  for (var i = 1; i < datos.length; i++) {
    var f = datos[i]; if (!f[1]) continue;
    lista.push([String(f[0] || ""), String(f[1]), String(f[2] || ""), Number(f[3]) || 0, Number(f[4]) || 0, Number(f[5]) || 0, Number(f[6]) || 0, Number(f[7]) || 0, String(f[8] || "")]);
  }
  var resp = { ok: true, productos: lista };
  if (cache) { try { cache.put("productos_lista", JSON.stringify(resp), 120); } catch (err) {} }
  return respond_(e, resp);
}
function numProd_(v, max) { var n = Number(String(v == null ? "" : v).replace(",", ".")); return isFinite(n) && n >= 0 && n <= max ? Math.round(n * 10) / 10 : null; }
function guardarProducto_(e) { try { return guardarProductoReal_(e); } catch (err) { return respond_(e, { ok: false, error: String(err && err.message || err) }); } }
function guardarProductoReal_(e) {
  var p = e.parameter;
  var codigo = String(p.codigo || "").replace(/\D/g, "").slice(0, 14);
  var nombre = String(p.nombre || "").trim().slice(0, 80), marca = String(p.marca || "").trim().slice(0, 40);
  /* Carbohidratos en "hc": Google reserva el parámetro "c" en las URL de los
     scripts (elige la cuenta) y con c distinto de 0 la petición nunca llega. */
  var k = numProd_(p.k, 900), pr = numProd_(p.p, 100), c = numProd_(p.hc != null ? p.hc : p.c, 100), g = numProd_(p.g, 100);
  var porcG = numProd_(p.porcG, 2000) || 0, porcTxt = String(p.porcTxt || "").trim().slice(0, 40);
  var origen = String(p.origen || "") === "manual" ? "manual" : "Open Food Facts";
  if (nombre.length < 2 || k === null || pr === null || c === null || g === null) return respond_(e, { ok: false, error: "datos incompletos" });
  if (codigo && codigo.length < 6) return respond_(e, { ok: false, error: "código inválido" });
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return respond_(e, { ok: false, error: "ocupado, intenta de nuevo" });
  try {
    var hoja = hojaProductos_(), datos = hoja.getDataRange().getValues(), clave = normNombre_(nombre + " " + marca);
    for (var i = 1; i < datos.length; i++) {
      var mismo = codigo ? String(datos[i][0]) === codigo : (!datos[i][0] && normNombre_(datos[i][1] + " " + datos[i][2]) === clave);
      if (mismo) { hoja.getRange(i + 1, 12).setValue((Number(datos[i][11]) || 1) + 1); return respond_(e, { ok: true, existia: true }); }
    }
    if (datos.length > 6000) return respond_(e, { ok: false, error: "lista llena" });
    var ahora = Utilities.formatDate(new Date(), TZ_INGRESOS_, "yyyy-MM-dd HH:mm");
    hoja.appendRow([codigo, nombre, marca, k, pr, c, g, porcG, porcTxt, origen, ahora, 1]);
    try { CacheService.getScriptCache().remove("productos_lista"); } catch (err) {}
    return respond_(e, { ok: true, nuevo: true });
  } finally { lock.releaseLock(); }
}

/* porcionProducto (10-10-2026): anota en cuántas láminas/unidades viene la
   porción de un producto ya guardado ("2 láminas (34 g)"). Solo escribe la
   columna "Porción texto" y solo si todavía no dice unidades (no pisa un dato
   bueno). Público, igual que guardarProducto. */
function porcionProducto_(e) { try { return porcionProductoReal_(e); } catch (err) { return respond_(e, { ok: false, error: String(err && err.message || err) }); } }
function porcionProductoReal_(e) {
  var p = e.parameter;
  var codigo = String(p.codigo || "").replace(/\D/g, "").slice(0, 14);
  var clave = normNombre_(String(p.nombre || "") + " " + String(p.marca || ""));
  var txt = String(p.porcTxt || "").trim().slice(0, 40);
  if (!/^\d+([.,]\d+)?\s+[a-zA-ZáéíóúñÁÉÍÓÚÑ]+/.test(txt)) return respond_(e, { ok: false, error: "porción inválida" });
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(10000)) return respond_(e, { ok: false, error: "ocupado, intenta de nuevo" });
  try {
    var hoja = hojaProductos_(), datos = hoja.getDataRange().getValues();
    for (var i = 1; i < datos.length; i++) {
      var mismo = codigo ? String(datos[i][0]) === codigo : normNombre_(datos[i][1] + " " + datos[i][2]) === clave;
      if (!mismo) continue;
      var actual = String(datos[i][8] || "");
      if (/l[aá]mina|rebanada|unidad|galleta|barra|pote|sobre|scoop|cucharada|taza|tajada|trozo/i.test(actual)) return respond_(e, { ok: true, yaTenia: true });
      hoja.getRange(i + 1, 9).setValue(txt);
      var pg = numProd_(p.porcG, 2000);
      if (pg && !(Number(datos[i][7]) > 0)) hoja.getRange(i + 1, 8).setValue(pg);
      try { CacheService.getScriptCache().remove("productos_lista"); } catch (err) {}
      return respond_(e, { ok: true });
    }
    return respond_(e, { ok: false, error: "no encontrado" });
  } finally { lock.releaseLock(); }
}

/* origenNutri (10-10-2026, la dueña: saber qué publicidad funciona): guarda la respuesta a
   «¿Cómo conociste WGYMNUTRI?» en la hoja «Cómo nos conocieron» (fecha y respuesta; sin nombre
   ni datos de salud). Público, como guardarProducto. */
var ORIGENES_NUTRI_ = ["gimnasio", "tarjeta", "amigo", "instagram", "facebook", "tiktok", "otro"];
function origenNutri_(e) {
  try {
    var o = String(e.parameter.origen || "").toLowerCase();
    if (ORIGENES_NUTRI_.indexOf(o) < 0) return respond_(e, { ok: false, error: "respuesta inválida" });
    var ss = SpreadsheetApp.openById(SHEET_ID), hoja = ss.getSheetByName("Cómo nos conocieron");
    if (!hoja) { hoja = ss.insertSheet("Cómo nos conocieron"); hoja.appendRow(["Fecha", "Respuesta"]); }
    hoja.appendRow([Utilities.formatDate(new Date(), TZ_INGRESOS_, "yyyy-MM-dd HH:mm"), o]);
    return respond_(e, { ok: true });
  } catch (err) { return respond_(e, { ok: false, error: String(err && err.message || err) }); }
}

/* ── Ranking del mes en la TARJETA (Versión 17, 11-10-2026, la dueña: "pongámoslo en la
   tarjeta virtual de los socios"). Puntos = días con ingreso al gimnasio en el mes,
   calculados aquí desde la hoja de ingresos (nadie puede inflarlos). La hoja «Retos»
   guarda Mes, Id (código al azar del teléfono), Apodo y Clave (nombre en mayúsculas,
   para contar sus días; la hoja es privada). listarRetos entrega SOLO apodo y días. */
/* La planilla convierte "2026-10" en una fecha: se lee de vuelta como texto «AAAA-MM» y se
   escribe con apóstrofo para que quede como texto (corregido el 10-10-2026, 21:20). */
function mesDe_(v) { return v instanceof Date ? Utilities.formatDate(v, TZ_INGRESOS_, "yyyy-MM") : String(v).replace(/^'/, "").slice(0, 7); }
/* Grupos del ranking (Versión 21, 11-10-2026, la dueña: "los mensuales vienen casi todos
   los días, el turno solo 14 y el 3 veces por semana 12"): cada socio compite solo con su
   grupo. La tarjeta manda g = mensual | turno | tres según su plan (semanal y pase diario no
   participan). Una fila sin grupo (de antes) cuenta como mensual. */
function grupoReto_(v) { v = String(v || ""); return v === "turno" || v === "tres" ? v : "mensual"; }
function guardarReto_(e) {
  try {
    var p = e.parameter, mes = diaCL_(Date.now()).slice(0, 7), id = String(p.id || "").replace(/[^a-z0-9]/gi, "").slice(0, 24);
    var apodo = String(p.apodo || "").replace(/[<>"]/g, "").trim().slice(0, 18), clave = claveDias_(p.n || "", p.a || "");
    if (id.length < 8 || apodo.length < 2 || clave.length < 3) return respond_(e, { ok: false, error: "datos inválidos" });
    var lock = LockService.getScriptLock();
    if (!lock.tryLock(10000)) return respond_(e, { ok: false, error: "ocupado, intenta de nuevo" });
    try {
      var ss = SpreadsheetApp.openById(SHEET_ID), hoja = ss.getSheetByName("Retos");
      if (!hoja) { hoja = ss.insertSheet("Retos"); hoja.appendRow(["Mes", "Id", "Apodo", "Clave", "Actualizado", "Grupo"]); }
      if (!hoja.getRange(1, 6).getValue()) hoja.getRange(1, 6).setValue("Grupo");
      var grupo = grupoReto_(p.g);
      var n = hoja.getLastRow(), ahora = Utilities.formatDate(new Date(), TZ_INGRESOS_, "yyyy-MM-dd HH:mm"), hecho = false;
      if (n >= 2) {
        /* Una sola fila por persona y mes: se busca por el código del teléfono o por el nombre. */
        var vals = hoja.getRange(2, 1, n - 1, 4).getValues();
        for (var i = vals.length - 1; i >= 0; i--) {
          if (mesDe_(vals[i][0]) === mes && (String(vals[i][1]) === id || String(vals[i][3]) === clave)) { hoja.getRange(i + 2, 2, 1, 5).setValues([[id, apodo, clave, ahora, grupo]]); hecho = true; break; }
        }
      }
      if (!hecho) hoja.appendRow(["'" + mes, id, apodo, clave, ahora, grupo]);
      CacheService.getScriptCache().remove("retos_" + mes);
      return respond_(e, { ok: true });
    } finally { lock.releaseLock(); }
  } catch (err) { return respond_(e, { ok: false, error: String(err && err.message || err) }); }
}
function calcularRetos_(p, conNombre) {
  var mes = diaCL_(Date.now()).slice(0, 7);
  var hoja = SpreadsheetApp.openById(SHEET_ID).getSheetByName("Retos"), filas = [];
  if (hoja && hoja.getLastRow() >= 2) {
    /* Si una persona quedó repetida, vale su fila más nueva (la de más abajo). */
    var porClave = {};
    hoja.getRange(2, 1, hoja.getLastRow() - 1, 6).getValues().forEach(function (r) {
      if (mesDe_(r[0]) === mes && r[3]) porClave[String(r[3])] = { id: String(r[1]).slice(0, 6), apodo: String(r[2]), clave: String(r[3]), g: grupoReto_(r[5]) };
    });
    Object.keys(porClave).forEach(function (k) { if (porClave[k].apodo !== "(salió)") filas.push(porClave[k]); });
  }
  var dias = filas.length ? diasDesde_(p, mes + "-01") : {};
  var lista = filas.map(function (f) { var o = { id: f.id, apodo: f.apodo, g: f.g, pts: dias[f.clave] ? Object.keys(dias[f.clave]).length : 0 }; if (conNombre) o.nombre = f.clave; return o; });
  lista.sort(function (a, b) { return b.pts - a.pts; });
  if (!conNombre) {
    /* Lo público: hasta 30 por grupo. */
    var cuenta = {};
    lista = lista.filter(function (x) { cuenta[x.g] = (cuenta[x.g] || 0) + 1; return cuenta[x.g] <= 30; });
  }
  return { ok: true, retos: true, grupos: true, mes: mes, lista: lista };
}
function listarRetos_(e) {
  try {
    var mes = diaCL_(Date.now()).slice(0, 7), cache = CacheService.getScriptCache(), guardado = cache.get("retos_" + mes);
    if (guardado) return respond_(e, JSON.parse(guardado));
    var out = calcularRetos_(e.parameter, false);
    cache.put("retos_" + mes, JSON.stringify(out), 120);
    return respond_(e, out);
  } catch (err) { return respond_(e, { ok: false, error: String(err && err.message || err) }); }
}
/* Ranking con nombres reales, solo para el mesón (POST con la clave de administración). */
function rankingAdmin_(e) {
  if (!claveValida_(e.parameter)) return respond_(e, { ok: false, error: "clave incorrecta" });
  try { return respond_(e, calcularRetos_(e.parameter, true)); }
  catch (err) { return respond_(e, { ok: false, error: String(err && err.message || err) }); }
}

/* ── las dos entradas que llama Código.gs ───────────────────────────── */

function accionIngresos_(e) {
  switch (e.parameter.action) {
    case "listarIngresos": return listarIngresos_(e);
    case "miIngreso": return miIngreso_(e);
    case "ingresoTarjeta": return ingresoTarjeta_(e);
    case "salidaSocio": return salidaSocio_(e);
    case "asistenciaDesde": return asistenciaDesde_(e);
    case "listarNutri": return listarNutri_(e);
    case "listarProductos": return listarProductos_(e);
    case "guardarProducto": return guardarProducto_(e);
    case "porcionProducto": return porcionProducto_(e);
    case "origenNutri": return origenNutri_(e);
    case "guardarReto": return guardarReto_(e);
    case "listarRetos": return listarRetos_(e);
  }
  return null;
}

function accionIngresosPost_(e) {
  switch (e.parameter.action) {
    case "registrarIngreso": return registrarIngreso_(e);
    case "registrarSalida": return registrarSalida_(e);
    case "quitarSalida": return quitarSalida_(e);
    case "activarNutri": return activarNutri_(e);
    case "rankingAdmin": return rankingAdmin_(e);
    case "ventasNutri": return ventasNutri_(e);
    case "borrarVentaNutri": return borrarVentaNutri_(e);
    case "tiendaListar": return tiendaListar_(e);
    case "tiendaProducto": return tiendaProducto_(e);
    case "tiendaVenta": return tiendaVenta_(e);
    case "tiendaEntrada": return tiendaEntrada_(e);
    case "tiendaAnular": return tiendaAnular_(e);
    case "tiendaFiadoPagado": return tiendaFiadoPagado_(e);
  }
  return null;
}

/* ── 🛒 Tienda WGYM (24-10-2026, la dueña: "empezar a vender otros productos… una app que se vea cuánto vendí,
   cuánta plata le saco, el inventario, que se descuente cada vez que venda y escanear con el celular") ──
   Todo es solo de administración (POST con la clave): los costos y las ganancias nunca salen por una acción
   pública. Dos hojas que se crean solas:
     «Tienda productos»: Id · Código · Nombre · Categoría · Detalle · Costo · Precio · Stock · Mínimo · Foto ·
                         Activo · Actualizado
     «Tienda movimientos»: Fecha · Tipo (venta / entrada / ajuste) · Venta · Id producto · Producto · Cantidad ·
                         Precio unit. · Costo unit. · Total · Pago · Cliente · Nota · Estado
   Estado: "" normal · "fiado" (debe) · "pagado …" (fiado ya pagado) · "anulada". Cada venta trae un id que
   inventa el teléfono (vid): si llega dos veces (sin señal, reintento) no se descuenta dos veces. */
var HOJA_TIENDA_P_ = "Tienda productos", HOJA_TIENDA_M_ = "Tienda movimientos";
function hojaTienda_(nombre, cab) {
  var ss = SpreadsheetApp.openById(SHEET_ID), h = ss.getSheetByName(nombre);
  if (!h) { h = ss.insertSheet(nombre); h.appendRow(cab); h.getRange("A:B").setNumberFormat("@"); h.setFrozenRows(1); }
  return h;
}
function hojaTiendaP_() { return hojaTienda_(HOJA_TIENDA_P_, ["Id", "Código", "Nombre", "Categoría", "Detalle", "Costo", "Precio", "Stock", "Mínimo", "Foto", "Activo", "Actualizado"]); }
function hojaTiendaM_() { return hojaTienda_(HOJA_TIENDA_M_, ["Fecha", "Tipo", "Venta", "Id producto", "Producto", "Cantidad", "Precio unit.", "Costo unit.", "Total", "Pago", "Cliente", "Nota", "Estado"]); }
function ahoraTienda_() { return Utilities.formatDate(new Date(), TZ_INGRESOS_, "yyyy-MM-dd HH:mm"); }
function txtFecha_(v) { return v instanceof Date ? Utilities.formatDate(v, TZ_INGRESOS_, "yyyy-MM-dd HH:mm") : String(v || ""); }
function datosTienda_(p) { try { return JSON.parse(String(p.datos || "{}")); } catch (err) { return null; } }
function conClaveTienda_(e, escribe, fn) {
  if (!claveValida_(e.parameter)) return respond_(e, { ok: false, error: "clave incorrecta" });
  if (!escribe) { try { return fn(); } catch (err) { return respond_(e, { ok: false, error: String(err && err.message || err) }); } }
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(15000)) return respond_(e, { ok: false, error: "ocupado, intenta de nuevo" });
  try { return fn(); } catch (err) { return respond_(e, { ok: false, error: String(err && err.message || err) }); }
  finally { lock.releaseLock(); }
}
function filaProducto_(r, i) {
  return { fila: i + 1, id: String(r[0]), cod: String(r[1] || ""), n: String(r[2] || ""), cat: String(r[3] || ""), det: String(r[4] || ""),
    costo: Number(r[5]) || 0, precio: Number(r[6]) || 0, stock: Number(r[7]) || 0, min: Number(r[8]) || 0, foto: String(r[9] || ""),
    activo: String(r[10]) !== "no", act: txtFecha_(r[11]) };
}
function productosTienda_() {
  var d = hojaTiendaP_().getDataRange().getValues(), l = [];
  for (var i = 1; i < d.length; i++) if (d[i][0]) l.push(filaProducto_(d[i], i));
  return l;
}
/* Productos + movimientos desde «desde» (AAAA-MM-DD; por defecto 120 días) + todos los fiados pendientes. */
function tiendaListar_(e) {
  return conClaveTienda_(e, false, function () {
    var desde = String(e.parameter.desde || "");
    if (!/^\d{4}-\d{2}-\d{2}$/.test(desde)) desde = Utilities.formatDate(new Date(Date.now() - 120 * 86400000), TZ_INGRESOS_, "yyyy-MM-dd");
    var d = hojaTiendaM_().getDataRange().getValues(), movs = [], total = { ventas: 0, ganancia: 0, invertido: 0 };
    for (var i = 1; i < d.length; i++) {
      var f = txtFecha_(d[i][0]), tipo = String(d[i][1] || ""), est = String(d[i][12] || ""), cant = Number(d[i][5]) || 0;
      if (est !== "anulada") {
        if (tipo === "venta") { total.ventas += Number(d[i][8]) || 0; total.ganancia += (Number(d[i][8]) || 0) - cant * (Number(d[i][7]) || 0); }
        if (tipo === "entrada") total.invertido += cant * (Number(d[i][7]) || 0);
      }
      if (f.slice(0, 10) < desde && est !== "fiado") continue;
      movs.push({ fila: i + 1, f: f, tipo: tipo, vid: String(d[i][2] || ""), id: String(d[i][3] || ""), n: String(d[i][4] || ""), cant: cant,
        precio: Number(d[i][6]) || 0, costo: Number(d[i][7]) || 0, total: Number(d[i][8]) || 0, pago: String(d[i][9] || ""),
        cliente: String(d[i][10] || ""), nota: String(d[i][11] || ""), est: est });
    }
    return respond_(e, { ok: true, tienda: true, hoy: diaCL_(Date.now()), desde: desde, productos: productosTienda_(), movs: movs, total: total });
  });
}
/* Crear o editar un producto. Si es nuevo y trae stock, ese stock queda como «entrada» (compra) con su costo. */
function tiendaProducto_(e) {
  return conClaveTienda_(e, true, function () {
    var x = datosTienda_(e.parameter); if (!x || !String(x.n || "").trim()) return respond_(e, { ok: false, error: "faltan datos" });
    var h = hojaTiendaP_(), lista = productosTienda_(), ahora = ahoraTienda_(), cod = String(x.cod || "").replace(/\s/g, "");
    var p = x.id ? lista.filter(function (q) { return q.id === String(x.id); })[0] : null;
    if (cod && lista.some(function (q) { return q.activo && q.cod === cod && (!p || q.id !== p.id); })) return respond_(e, { ok: false, error: "ese código ya es de otro producto" });
    var fila = [p ? p.id : "P" + Date.now().toString(36).toUpperCase(), cod, String(x.n).trim(), String(x.cat || ""), String(x.det || ""),
      Number(x.costo) || 0, Number(x.precio) || 0, p ? p.stock : (Number(x.stock) || 0), Number(x.min) || 0, String(x.foto || ""),
      x.activo === false ? "no" : "sí", ahora];
    if (p) h.getRange(p.fila, 1, 1, 12).setValues([fila]);
    else {
      h.appendRow(fila);
      if (fila[7] > 0) hojaTiendaM_().appendRow([ahora, "entrada", "", fila[0], fila[2], fila[7], "", fila[5], fila[7] * fila[5], "", "", "stock inicial", ""]);
    }
    return respond_(e, { ok: true, tienda: true, id: fila[0], productos: productosTienda_() });
  });
}
/* Venta: { vid, items:[{id, cant, precio}], pago, cliente, nota }. Descuenta el stock de cada producto. */
function tiendaVenta_(e) {
  return conClaveTienda_(e, true, function () {
    var x = datosTienda_(e.parameter); if (!x || !x.vid || !x.items || !x.items.length) return respond_(e, { ok: false, error: "faltan datos" });
    var hm = hojaTiendaM_(), vids = hm.getRange(1, 3, hm.getLastRow(), 1).getValues();
    for (var j = 0; j < vids.length; j++) if (String(vids[j][0]) === String(x.vid)) return respond_(e, { ok: true, tienda: true, repetida: true, productos: productosTienda_() });
    var h = hojaTiendaP_(), lista = productosTienda_(), ahora = ahoraTienda_(), pago = String(x.pago || "efectivo"), filas = [];
    x.items.forEach(function (it) {
      var p = lista.filter(function (q) { return q.id === String(it.id); })[0]; if (!p) return;
      var cant = Number(it.cant) || 0, precio = Number(it.precio); if (!(cant > 0)) return; if (isNaN(precio)) precio = p.precio;
      p.stock -= cant; h.getRange(p.fila, 8).setValue(p.stock); h.getRange(p.fila, 12).setValue(ahora);
      filas.push([ahora, "venta", String(x.vid), p.id, p.n, cant, precio, p.costo, cant * precio, pago, String(x.cliente || ""), String(x.nota || ""), pago === "fiado" ? "fiado" : ""]);
    });
    if (!filas.length) return respond_(e, { ok: false, error: "productos no encontrados" });
    hm.getRange(hm.getLastRow() + 1, 1, filas.length, 13).setValues(filas);
    return respond_(e, { ok: true, tienda: true, productos: productosTienda_() });
  });
}
/* Entrada de mercadería (compra) o ajuste de inventario: { id, cant, costo, tipo:"entrada"|"ajuste", nota }.
   En un ajuste, cant puede ser negativa (se rompió, se perdió, se regaló). */
function tiendaEntrada_(e) {
  return conClaveTienda_(e, true, function () {
    var x = datosTienda_(e.parameter); if (!x || !x.id) return respond_(e, { ok: false, error: "faltan datos" });
    var h = hojaTiendaP_(), p = productosTienda_().filter(function (q) { return q.id === String(x.id); })[0];
    if (!p) return respond_(e, { ok: false, error: "producto no encontrado" });
    var tipo = x.tipo === "ajuste" ? "ajuste" : "entrada", cant = Number(x.cant) || 0, costo = Number(x.costo);
    if (!cant || (tipo === "entrada" && cant < 0)) return respond_(e, { ok: false, error: "cantidad inválida" });
    if (isNaN(costo) || costo <= 0) costo = p.costo;
    var ahora = ahoraTienda_(); p.stock += cant;
    h.getRange(p.fila, 8).setValue(p.stock); h.getRange(p.fila, 12).setValue(ahora);
    if (tipo === "entrada") h.getRange(p.fila, 6).setValue(costo);
    hojaTiendaM_().appendRow([ahora, tipo, "", p.id, p.n, cant, "", costo, tipo === "entrada" ? cant * costo : 0, "", "", String(x.nota || ""), ""]);
    return respond_(e, { ok: true, tienda: true, productos: productosTienda_() });
  });
}
/* Anular una venta completa (se equivocó): marca sus filas «anulada» y devuelve el stock. */
function tiendaAnular_(e) {
  return conClaveTienda_(e, true, function () {
    var vid = String(e.parameter.vid || ""); if (!vid) return respond_(e, { ok: false, error: "faltan datos" });
    var hm = hojaTiendaM_(), d = hm.getDataRange().getValues(), h = hojaTiendaP_(), lista = productosTienda_(), n = 0;
    for (var i = 1; i < d.length; i++) {
      if (String(d[i][2]) !== vid || String(d[i][1]) !== "venta" || String(d[i][12]) === "anulada") continue;
      var p = lista.filter(function (q) { return q.id === String(d[i][3]); })[0];
      if (p) { p.stock += Number(d[i][5]) || 0; h.getRange(p.fila, 8).setValue(p.stock); }
      hm.getRange(i + 1, 13).setValue("anulada"); n++;
    }
    if (!n) return respond_(e, { ok: false, error: "venta no encontrada" });
    return respond_(e, { ok: true, tienda: true, productos: productosTienda_() });
  });
}
/* Un fiado pagado: { vid, pago } → Estado «pagado <medio> <fecha>». */
function tiendaFiadoPagado_(e) {
  return conClaveTienda_(e, true, function () {
    var vid = String(e.parameter.vid || ""), pago = String(e.parameter.pago || "efectivo"); if (!vid) return respond_(e, { ok: false, error: "faltan datos" });
    var hm = hojaTiendaM_(), d = hm.getDataRange().getValues(), n = 0;
    for (var i = 1; i < d.length; i++) if (String(d[i][2]) === vid && String(d[i][12]) === "fiado") { hm.getRange(i + 1, 13).setValue("pagado " + pago + " " + ahoraTienda_()); n++; }
    if (!n) return respond_(e, { ok: false, error: "fiado no encontrado" });
    return respond_(e, { ok: true, tienda: true });
  });
}

