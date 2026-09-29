#!/usr/bin/env node
/**
 * generar-carteles-pdf.js
 *
 * Genera un PDF desde un archivo HTML de carteles usando Playwright.
 * Uso: node scripts/generar-carteles-pdf.js <input-html> <output-pdf>
 *
 * Ejemplo:
 *   node scripts/generar-carteles-pdf.js plantilla-carteles-wgym.html carteles-output.pdf
 */

const playwright = require('playwright');
const path = require('path');
const fs = require('fs');

async function generarCartelesPDF(inputHtml, outputPdf) {
  const inputPath = path.resolve(inputHtml);
  const outputPath = path.resolve(outputPdf);

  // Verificar que el archivo de entrada existe
  if (!fs.existsSync(inputPath)) {
    console.error(`❌ Archivo no encontrado: ${inputPath}`);
    process.exit(1);
  }

  try {
    const browser = await playwright.chromium.launch({
      executablePath: '/opt/pw-browsers/chromium'
    });
    const page = await browser.newPage();

    // Cargar el HTML desde archivo local
    await page.goto(`file://${inputPath}`, { waitUntil: 'networkidle' });

    // Generar PDF con formato A4
    await page.pdf({
      path: outputPath,
      format: 'A4',
      margin: { top: 0, bottom: 0, left: 0, right: 0 }
    });

    console.log(`✓ PDF creado correctamente: ${outputPath}`);
    await browser.close();
  } catch (error) {
    console.error(`❌ Error al generar PDF: ${error.message}`);
    process.exit(1);
  }
}

// Obtener argumentos de línea de comandos
const args = process.argv.slice(2);

if (args.length < 2) {
  console.log('Uso: node scripts/generar-carteles-pdf.js <input-html> <output-pdf>');
  console.log('Ejemplo: node scripts/generar-carteles-pdf.js plantilla-carteles-wgym.html carteles-output.pdf');
  process.exit(1);
}

const inputHtml = args[0];
const outputPdf = args[1];

generarCartelesPDF(inputHtml, outputPdf);
