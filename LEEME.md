# Mediciones sin copiar por chat — WGYMADNSPORT

Estado: el servicio nuevo se aloja en Sites; estos HTML están en la rama de
trabajo. No publicar los HTML hasta comprobar el servicio y el flujo completo.

## Flujo

- `control-fisico.html` conserva su aspecto y busca socios en la lista actual
  del mesón. Guardar envía la medición al servicio de Sites y después vuelve a
  leerla para confirmar que quedó disponible. Si falla, mantiene los números
  en pantalla y avisa. La primera vez se pide una clave de mediciones, que se
  recuerda en ese navegador; nunca está escrita en el código público.
- El servicio guarda solo MedId, fecha, sexo, estatura, edad, peso, grasa e IMC
  en una base D1. No recibe nombres ni RUT. Repetir Guardar el mismo día
  actualiza ese registro.
- `tarjeta.html` conserva el historial antiguo de `mediciones.json` y añade
  las mediciones nuevas de Sites en la sección de evolución. Las funciones
  actuales de renovación, check-in, bandas y candados siguen con Apps Script.
- Los socios que ya tienen MedId mantienen su identificador. Para quienes no
  lo tienen, ambas páginas calculan el mismo identificador estable a partir
  del nombre y apellido. Si un nombre se modifica después, habrá que mantener
  la vinculación del historial.

## Verificaciones antes de publicar en main

1. Confirmar que el despliegue público de Sites responde a una lectura vacía.
2. Guardar una medición de prueba controlada desde el formulario y verla en
   la tarjeta QR del mismo socio, incluida una segunda carga para comprobar
   que no duplica la fecha.
3. Confirmar que el historial anterior permanece y que las otras funciones
   de la tarjeta y del mesón siguen accesibles.
4. Revisar cambios concurrentes en `main` y recién entonces integrar estos
   dos HTML. No sustituir el Apps Script que hoy maneja renovaciones.

El repositorio público no contiene la clave de mediciones. Su valor se
configura como secreto del servicio y se introduce una vez en el navegador
del mesón.
