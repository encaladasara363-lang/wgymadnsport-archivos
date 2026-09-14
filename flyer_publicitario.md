# Flyer publicitario — WGYMADNSPORT

Contenido y estructura para un flyer/cartel general del gimnasio.
Formato base sugerido: A4 vertical, siguiendo la plantilla "cartel"
del sistema de diseño ya aprobado (`assets/plantilla-aviso-informacion.html`
de la skill `wgymadnsport-plantillas`) — este archivo es el guion de
contenido; el HTML/PDF final se arma a partir de esa plantilla.

---

## 1. Título llamativo (zona superior, tipografía Anton, mayúsculas)

```
ENTRENA
CON CIENCIA.
CAMBIA
DE VERDAD.
```

**Kicker** (línea pequeña sobre el título, Barlow Condensed, mayúsculas,
letter-spacing amplio):
```
WGYMADNSPORT · TOCOPILLA
```

---

## 2. Bloque "Entrenamos con ciencia" (cuerpo central)

**Etiqueta del bloque** (en rojo de marca, mayúsculas):
```
NO ENTRENAMOS AL OJO
```

**Texto de respaldo** (Barlow Condensed, peso 700-800):
```
Tus rutinas y tu nutrición se arman con principios reales de
entrenamiento, hipertrofia y biomecánica — no con rutinas genéricas
copiadas de internet.
```

**3 puntos de credibilidad** (formato de lista corta, un ícono o número
por punto, cada uno con máximo 2 líneas):

1. **SOBRECARGA PROGRESIVA REAL**
   Tu carga sube con un criterio técnico, no al azar — así tu cuerpo
   progresa sin lesionarte.

2. **DESCANSO QUE SÍ RINDE**
   Tu músculo no crece entrenando, crece descansando. Programamos tus
   días de recuperación para que cada sesión valga la pena.

3. **NUTRICIÓN CALCULADA, NO ADIVINADA**
   Tus macros y tus calorías se calculan con fórmulas reales, ajustadas
   a tu objetivo — bajar de peso, ganar músculo o rendir mejor.

---

## 3. Zona de horarios (bloque destacado, línea de relleno gruesa entre
día y hora, estilo tabla del cartel de horarios ya existente)

**Etiqueta del bloque:**
```
HORARIOS
```

| Día                   | Horario         |
|-----------------------|------------------|
| Lunes a Jueves         | 8:00 a 23:30     |
| Viernes                | 9:00 a 23:30     |
| Sábados y Feriados     | 10:00 a 22:00    |

---

## 4. Zona de datos de contacto (pie del flyer, jerarquía menor al
título pero igual de legible — Barlow Condensed 700-800, nunca más fino)

**Etiqueta del bloque:**
```
VISÍTANOS
```

```
📍 Calle 21 de Mayo 1520, Tocopilla
📱 WhatsApp: +56 9 9154 0156
✉️ wadnsporttocopilla@gmail.com
📸 Instagram: @wadnsport.tocopilla
```

**Llamado a la acción final** (línea de cierre, en rojo, mayúsculas):
```
NO HAY EXCUSA. VEN Y COMPRUÉBALO.
```

---

## Notas de diseño (para armar el HTML/PDF final)

- Colores: negro tinta `#0D0D0F` y blanco papel `#FCFCFA` como base;
  rojo de marca `#E1061B` como único acento, usado en el kicker "NO
  ENTRENAMOS AL OJO" y en el llamado a la acción final — sin saturar
  el resto de la pieza de rojo.
- Tipografía: títulos y el número de cada punto de credibilidad en
  `Anton` (peso 900); todo el resto del texto en `Barlow Condensed`,
  nunca por debajo de peso 700 para que se lea bien impreso.
- Layout: letras grandes y muy espaciadas, zona de logo (`logo.jpeg`
  real) despejada en la parte superior o inferior, línea de relleno
  gruesa (4px) para separar la tabla de horarios.
- Fuente de los datos científicos: sección "Base de conocimiento
  técnico" de `CLAUDE.md` (principios de sobrecarga progresiva,
  supercompensación muscular y cálculo de macros) — si se actualiza
  el flyer más adelante, sacar cualquier dato nuevo de esa misma
  sección para no inventar cifras.
- Datos de contacto y horarios tomados tal cual de `index.html` y
  `cartel-horarios.html` — si alguno cambia, actualizarlos también
  ahí para que no queden desalineados entre piezas.
