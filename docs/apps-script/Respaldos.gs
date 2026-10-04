/* ═══════════════════════════════════════════════════════════════════════
   RESPALDO SEMANAL (10/2026)
   Archivo aparte del proyecto de Apps Script del check-in ("Respaldos.gs").
   Se pega completo, tal cual: no reemplaza nada de Código.gs ni de
   INGRESOS.gs, y no hace falta volver a implementar.

   Cada sábado a las 23:00 (hora de Chile, la del proyecto) guarda una
   copia completa de la planilla (ingresos, Socios, Candados, Bandas) en
   la carpeta "Respaldos WGYMADNSPORT" de tu Google Drive, con la fecha en
   el nombre, y te avisa por correo con el enlace.

   Solo COPIA: nunca modifica ni borra la planilla original ni los
   respaldos anteriores.

   Para activarlo (una sola vez): elegir la función
   instalarRespaldoSemanal en la barra de arriba → Ejecutar → aceptar los
   permisos. Para probar un respaldo al tiro: elegir respaldoSemanal →
   Ejecutar.
   ═══════════════════════════════════════════════════════════════════════ */

var CARPETA_RESPALDOS_ = "Respaldos WGYMADNSPORT";

function respaldoSemanal() {
  var original = DriveApp.getFileById(SHEET_ID);
  var carpetas = DriveApp.getFoldersByName(CARPETA_RESPALDOS_);
  var carpeta = carpetas.hasNext() ? carpetas.next() : DriveApp.createFolder(CARPETA_RESPALDOS_);
  var fecha = Utilities.formatDate(new Date(), "America/Santiago", "yyyy-MM-dd");
  var copia = original.makeCopy("Respaldo WGYMADNSPORT " + fecha, carpeta);
  var correo = Session.getEffectiveUser().getEmail();
  if (correo) {
    MailApp.sendEmail(correo, "✅ Respaldo semanal WGYMADNSPORT " + fecha,
      "Se guardó el respaldo de tu planilla (ingresos, socios, candados y bandas) " +
      "en la carpeta \"" + CARPETA_RESPALDOS_ + "\" de tu Google Drive:\n\n" + copia.getUrl());
  }
  return copia.getUrl();
}

/* Crea (o vuelve a crear, sin duplicar) el aviso automático de cada sábado. */
function instalarRespaldoSemanal() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === "respaldoSemanal") ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger("respaldoSemanal")
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.SATURDAY)
    .atHour(23)
    .create();
  return "Respaldo semanal activado: todos los sábados a las 23:00.";
}
