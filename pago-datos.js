/* Planes, precios y cuenta para recibir pagos de WGYMADNSPORT.
   Un solo lugar para estos datos: los usan tarjeta.html (botón "Pagar
   mensualidad") y pagar.html (la página del cartel con QR). Para cambiar
   un precio o la cuenta, editar SOLO este archivo.
   La cuenta es la de la dueña, publicada a propósito por ella para
   recibir transferencias (no son datos de socios). */
window.WGYM_PAGO = {
 cuenta: {
  banco: "Banco Falabella",
  tipo: "Cuenta Corriente",
  numero: "19992903080",
  titular: "Sara Encalada",
  rut: "15.005.638-1",
  correo: "encaladasara363@gmail.com",
  whatsapp: "56975196394"
 },
 /* WGYMNUTRI (contador de calorías) se vende aparte, por mes (10-10-2026). */
 nutri: { nombre: "WGYMNUTRI mensual", precio: 5000 },
 /* Ofertas de WGYMNUTRI (10-10-2026, pedido de la dueña). "meses" = meses de
    app que la dueña activa en el mesón. El pack incluye 1 mes de Full Mensual:
    ese mes de gimnasio se renueva en la ficha como siempre. */
 nutriOfertas: [
  { id: "mes",  nombre: "WGYMNUTRI 1 mes",          precio: 5000,  meses: 1, detalle: "1 mes de app" },
  { id: "tri",  nombre: "WGYMNUTRI 3 meses",        precio: 12000, meses: 3, detalle: "3 meses de app · ahorras $3.000" },
  { id: "pack", nombre: "Full Mensual + WGYMNUTRI", precio: 36000, meses: 1, detalle: "1 mes de gimnasio + 1 mes de app · ahorras $2.000" }
 ],
 /* "re" reconoce el plan tal como está escrito en la ficha del socio
    (sin tildes y en minúsculas). El orden importa: el primero que calce. */
 planes: [
  { nombre: "Full Mensual",              precio: 33000, re: /full/ },
  { nombre: "3 Veces por Semana",        precio: 28000, re: /(3|tres) veces/ },
  { nombre: "Funcionarios Públicos",     precio: 28000, re: /funcionari/ },
  { nombre: "Estudiante / Profesor",     precio: 28000, re: /estudiante|profesor/ },
  { nombre: "Mensual Tercera Edad",      precio: 23000, re: /tercera edad/ },
  { nombre: "Mensual por Turno",         precio: 23000, re: /turno/ },
  { nombre: "Semanal",                   precio: 15000, re: /\bsemanal\b/ },
  { nombre: "Pase Diario",               precio: 4000,  re: /diario/ }
 ]
};
