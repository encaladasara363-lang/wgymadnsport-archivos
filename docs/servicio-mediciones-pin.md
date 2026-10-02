# Cambio para el servicio de mediciones: PIN opcional por socio

Pega este texto completo en la herramienta donde creaste el servicio
`wgymadnsport-mediciones.encaladasara363.chatgpt.site` y pide que lo
implemente tal cual.

---

## Contexto

El servicio guarda las mediciones de los socios (peso, % de grasa, IMC)
por un código `medid`. Hoy cualquiera puede leer las mediciones de un
socio con `GET /api/mediciones?medid=XXXX`, y el `medid` se puede
calcular a partir del nombre. Quiero agregar un **PIN opcional de 4
dígitos por socio**. Las páginas del sitio (`tarjeta.html` y
`control-fisico.html`) **ya están preparadas** para esto. Solo falta el
servicio.

**Importante: no cambiar nada de lo que ya funciona.** Guardar
(`POST /api/mediciones`) y borrar (`DELETE /api/mediciones`) siguen
igual, y también la clave de administración actual (la "clave de
mediciones").

## 1. Guardar el PIN

- Para cada `medid`, guardar opcionalmente un PIN. **Nunca en texto
  plano:** guardar solo un hash (por ejemplo, SHA-256 de un secreto del
  servidor + `medid` + PIN).
- Nunca escribir el PIN en los registros (logs) ni devolverlo en
  ninguna respuesta.

## 2. Leer mediciones: `GET /api/mediciones?medid=XXXX`

Agregar `"pinSoportado": true` a **todas** las respuestas de este GET.

- **Si el `medid` NO tiene PIN:** responder exactamente como hoy, más
  `"pinSoportado": true, "protegido": false`.
- **Si el `medid` SÍ tiene PIN:**
  - Si llega la cabecera `X-Wgym-Clave` con la clave de administración
    correcta, **o** la cabecera `X-Wgym-Pin` con el PIN correcto:
    responder como hoy (con `socio` y `fechasEliminadas`), más
    `"pinSoportado": true, "protegido": true`.
  - Si no llega ninguna de las dos cabeceras: responder `200` con
    `{"ok": true, "pinSoportado": true, "protegido": true}`, **sin**
    `socio` ni ningún dato de mediciones.
  - Si llega `X-Wgym-Pin` incorrecto: responder `401` con
    `{"ok": false, "error": "pin incorrecto"}`.

**Límite de intentos (obligatorio):** después de 5 PIN incorrectos
seguidos para un mismo `medid`, bloquear ese `medid` por 15 minutos y
responder `429` con `{"ok": false, "error": "bloqueado"}`, aunque el
PIN sea correcto. Un PIN correcto o la clave de administración
reinician el contador. Sin este límite, un PIN de 4 dígitos se adivina
en minutos.

## 3. Crear el PIN: `POST /api/mediciones/pin`

Cuerpo JSON: `{"medid": "XXXX", "pin": "1234"}`

- `pin` debe ser exactamente 4 dígitos; si no, `400` con
  `{"ok": false, "error": "pin inválido"}`.
- Si ese `medid` ya tiene PIN: `409` con
  `{"ok": false, "error": "ya tiene pin"}` (no se puede cambiar el PIN
  de otra persona sin saber el actual).
- Si no tiene: guardar el hash y responder `{"ok": true}`.

## 4. Quitar el PIN (socio que lo olvidó): `DELETE /api/mediciones/pin`

Cuerpo JSON: `{"medid": "XXXX", "clave": "<clave de administración>"}`

- Si la clave es incorrecta: `401` con
  `{"ok": false, "error": "clave incorrecta"}` (el mismo texto que ya
  usa el servicio).
- Si es correcta: borrar el PIN de ese `medid`, reiniciar el contador
  de intentos y responder `{"ok": true}`. Las mediciones no se tocan.

## 5. CORS

Permitir, para el origen
`https://encaladasara363-lang.github.io`:

- Métodos: `GET, POST, DELETE, OPTIONS`
- Cabeceras: `Content-Type, X-Wgym-Pin, X-Wgym-Clave`
- Responder bien a las solicitudes `OPTIONS` (preflight).

## 6. Prueba rápida al terminar

1. `GET /api/mediciones?medid=<uno que exista>` → debe traer
   `"pinSoportado": true, "protegido": false` y los datos.
2. `POST /api/mediciones/pin` con un PIN → `{"ok": true}`.
3. Repetir el GET sin cabeceras → `protegido: true` y **sin datos**.
4. GET con `X-Wgym-Pin` correcto → con datos.
5. GET con `X-Wgym-Clave` (clave de administración) → con datos.
6. `DELETE /api/mediciones/pin` con la clave → `{"ok": true}`, y el GET
   vuelve a mostrar datos sin PIN.
