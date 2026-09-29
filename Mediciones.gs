/*
 * WGYMADNSPORT — mediciones compartidas.
 * Añadir como archivo nuevo al MISMO proyecto Apps Script del control de socios.
 * Código.gs debe enviar action=medicionesSocio a medicionesSocio_(e)
 * y action=guardarMedicion a guardarMedicion_(e), tanto por doPost como
 * por doGet según los métodos ya existentes. Nunca pasar la clave por GET.
 *
 * El historial antiguo permanece en mediciones.json. Esta hoja almacena
 * solo los registros nuevos y los identifica por MedId, sin nombre ni RUT.
 */
function getMedicionesSheet_() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = ss.getSheetByName("Mediciones");
  if (!sheet) {
    sheet = ss.insertSheet("Mediciones");
    sheet.appendRow(["MedId", "Sexo", "Estatura", "Fecha", "Edad",
      "Peso", "Grasa", "IMC", "Actualizado"]);
  }
  return sheet;
}

function medicionesSocio_(e) {
  var medid = String((e.parameter || {}).medid || "").trim().toLowerCase();
  if (!/^[a-f0-9]{8}$/.test(medid)) {
    return respond_(e, { ok:false, error:"identificador inválido" });
  }
  var rows = getMedicionesSheet_().getDataRange().getValues();
  var registros = [], sexo = "", estatura = null;
  for (var i=1; i<rows.length; i++) {
    var r = rows[i];
    if (String(r[0]).toLowerCase() !== medid) continue;
    sexo = String(r[1] || sexo);
    if (r[2] !== "") estatura = Number(r[2]);
    registros.push({
      fecha:String(r[3]), edad:r[4] === "" ? null : Number(r[4]),
      peso:r[5] === "" ? null : Number(r[5]),
      grasa:r[6] === "" ? null : Number(r[6]),
      imc:r[7] === "" ? null : Number(r[7])
    });
  }
  registros.sort(function(a,b){ return a.fecha.localeCompare(b.fecha); });
  return respond_(e, { ok:true, socio:{ id:medid, sexo:sexo,
    estatura:estatura, registros:registros } });
}

function guardarMedicion_(e) {
  var p = e.parameter || {};
  if (!claveValida_(p)) return respond_(e, {ok:false, error:"clave incorrecta"});
  var nombre = String(p.nombre || "").trim();
  var apellido = String(p.apellido || "").trim();
  var sexo = String(p.sexo || "").toUpperCase();
  var fecha = String(p.fecha || "");
  var edad = medNumero_(p.edad, 1, 120);
  var estatura = medNumero_(p.estatura, 80, 250);
  var peso = medNumero_(p.peso, 20, 400, true);
  var grasa = medNumero_(p.grasa, 0, 80, true);
  var imc = medNumero_(p.imc, 8, 80, true);
  if ((p.peso !== "" && p.peso != null && peso === null) ||
      (p.grasa !== "" && p.grasa != null && grasa === null) ||
      (p.imc !== "" && p.imc != null && imc === null)) {
    return respond_(e, {ok:false, error:"resultado fuera de rango"});
  }
  if (!nombre || !apellido || (sexo !== "F" && sexo !== "M") ||
      !/^\d{4}-\d{2}-\d{2}$/.test(fecha) ||
      !edad || !estatura || (peso === null && grasa === null && imc === null)) {
    return respond_(e, {ok:false, error:"revisa los datos de la medición"});
  }
  var fechaObj = new Date(fecha + "T00:00:00Z");
  if (isNaN(fechaObj.getTime()) || fechaObj.toISOString().slice(0,10) !== fecha) {
    return respond_(e, {ok:false, error:"fecha inválida"});
  }
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(20000)) return respond_(e, {ok:false, error:"intenta otra vez"});
  try {
    var sociosSheet = getSociosSheet_();
    var socios = sociosSheet.getDataRange().getValues();
    var fila = -1, candidatos = 0;
    for (var i=1; i<socios.length; i++) {
      if (normNombre_(socios[i][0]) === normNombre_(nombre) &&
          normNombre_(socios[i][1]) === normNombre_(apellido)) {
        fila = i+1; candidatos++;
      }
    }
    if (candidatos !== 1) return respond_(e,
      {ok:false, error:candidatos ? "nombre duplicado" : "socio no encontrado"});
    var medid = String(socios[fila-1][5] || "").trim().toLowerCase();
    var propuesto = String(p.medid || "").trim().toLowerCase();
    if (!medid) {
      if (/^[a-f0-9]{8}$/.test(propuesto)) medid = propuesto;
      else medid = Utilities.getUuid().replace(/-/g,"").slice(0,8);
      for (var j=1; j<socios.length; j++) {
        if (j !== fila-1 && String(socios[j][5] || "").toLowerCase() === medid)
          return respond_(e, {ok:false, error:"identificador repetido"});
      }
      sociosSheet.getRange(fila,6).setValue(medid);
    }
    var sheet = getMedicionesSheet_();
    var rows = sheet.getDataRange().getValues();
    // Un registro por socio y día: repetir Guardar actualiza ese día.
    for (var k=1; k<rows.length; k++) {
      if (String(rows[k][0]).toLowerCase() === medid && String(rows[k][3]) === fecha) {
        sheet.getRange(k+1,1,1,9).setValues([[
          medid,sexo,estatura,fecha,edad,peso,grasa,imc,new Date().toISOString()
        ]]);
        return respond_(e, {ok:true, medid:medid, actualizado:true});
      }
    }
    sheet.appendRow([medid,sexo,estatura,fecha,edad,peso,grasa,imc,
      new Date().toISOString()]);
    return respond_(e, {ok:true, medid:medid, actualizado:false});
  } finally {
    lock.releaseLock();
  }
}

function medNumero_(v,min,max,opcional) {
  if (v === "" || v == null) return opcional ? null : 0;
  var n = Number(String(v).replace(",","."));
  return isFinite(n) && n >= min && n <= max ? n : (opcional ? null : 0);
}
