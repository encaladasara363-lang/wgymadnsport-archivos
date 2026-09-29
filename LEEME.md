# Mediciones sin copiar por chat — WGYMADNSPORT

Estado: propuesta preparada y comprobada sintácticamente. **No está publicada.**
No usar los HTML nuevos hasta que el servicio de Apps Script esté actualizado
y se pruebe el guardado. Este paquete preserva las mediciones ya publicadas.

## Qué cambia

- `control-fisico.html` busca socios en la misma hoja compartida que el mesón.
  Al tocar Guardar, envía fecha, sexo, edad, estatura, peso, grasa e IMC al
  servicio con la clave de administración que ya usa `control.html`.
  Si el servidor falla, conserva los números en pantalla y avisa que no guardó.
- `Mediciones.gs` guarda los registros nuevos en una pestaña `Mediciones`
  de la misma planilla, identificados por MedId. Verifica la clave del servidor,
  bloquea escrituras simultáneas y evita duplicar un registro del mismo día.
  Si es la primera medición, asigna MedId al socio de la hoja `Socios`.
- `tarjeta.html` combina los registros nuevos con el historial existente en
  `mediciones.json`, sin borrar ni reescribir ese archivo.

## Integración del proyecto Apps Script

Antes de tocar la aplicación publicada, leer la versión **actual** de
`Código.gs` en el proyecto del gimnasio y guardar una copia. La copia
`Codigo.gs` disponible en ChatGPT puede ser anterior a la versión que hoy
permite renovar socios; no reemplazarla completa.

1. Crear un archivo nuevo `Mediciones.gs` dentro del mismo proyecto y pegar
   el contenido adjunto.
2. En el `doGet(e)` **existente**, antes de la respuesta por defecto, agregar:

```js
if (e.parameter.action === "medicionesSocio") return medicionesSocio_(e);
```

3. En el `doPost(e)` **existente**, antes de la respuesta por defecto, agregar:

```js
if (e.parameter.action === "guardarMedicion") return guardarMedicion_(e);
```

   Si no existe `doPost`, hay que revisar la versión publicada y preservar
   cualquier ruta usada por guardar/borrar socios antes de añadirla. No crear
   un segundo `doPost` que sustituya las renovaciones.
4. Guardar, desplegar **una nueva versión del mismo despliegue web** y verificar
   que la URL `/exec` siga siendo la que usan los HTML. No crear una URL
   distinta sin actualizar todas las páginas que dependen de ella.
5. Confirmar lectura `medicionesSocio` y un guardado controlado con un socio
   que se esté midiendo realmente; comprobar que aparece en su tarjeta QR
   y que las mediciones anteriores siguen presentes. Verificar también que
   Guardar socio, ingresos, bandas y candados continúan funcionando.
6. Publicar los dos HTML en la rama principal solo después de la prueba del
   servicio. Revisar los cambios concurrentes antes de reemplazar archivos.

La clave `ADMIN_KEY` permanece en Propiedades del script. No ponerla en
este paquete ni en GitHub. El navegador del mesón la recuerda como
`wgym_clave_admin_v1`, igual que el control de socios.

## Alcance comprobado

Las dos páginas y el módulo de Apps Script pasaron verificación de sintaxis.
No se ejecutó un guardado real ni una prueba de extremo a extremo porque el
acceso de escritura a GitHub respondió 403 y el editor de Apps Script pidió
autenticación. Ningún dato real de socio fue modificado por esta preparación.
