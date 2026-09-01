# Contenido de redes · WGYMADNSPORT Tocopilla

Acá vive el contenido de Instagram del gimnasio: **16 semanas, 112 publicaciones**,
sacadas de los nueve módulos del curso PersonalViral y reescritas para WGYMADNSPORT
(planes reales, precios reales, WhatsApp real, y las rutinas con QR del gimnasio).

## Armar el paquete de una semana

    python3 contenido/semana.py 3

Deja en `contenido/salida/semana-03/`:

- **7 láminas del carrusel** en PNG 1080×1080, con foto del gimnasio de fondo,
  el logo, el Instagram y el WhatsApp en cada una.
- **`semana-03-textos.txt`** con los siete días listos para copiar y pegar:
  guion del Reel, leyenda, llamado a la acción, comentario fijado, hashtags,
  qué grabar ese día y los avisos.

## Qué hay en cada carpeta

| | |
|---|---|
| `contenido.json` | Las 16 semanas completas. Es la fuente de todo. |
| `fondos/` | Nueve fotos del gimnasio recortadas en cuadrado. `f8` es la entrada con el letrero, se usa en las portadas. |
| `fuentes/` | Anton y Barlow Condensed (licencia SIL OFL). |
| `logo.jpg` | El logo que va abajo a la derecha de cada lámina. |
| `salida/` | Lo que genera el script. No se sube al repositorio. |

## Las 16 semanas

| Semanas | Tema | Módulos |
|---|---|---|
| 1 a 4 | Constancia, movilidad, por qué entrenar acá | 10, 11, 12 |
| 5 a 8 | Fuerza, errores del gimnasio, mitos del fitness | 7, 8, 9 |
| 9 a 12 | Mujeres y pesas, empezar sin vergüenza, 40+ | 4, 5, 6 |
| 13 a 16 | Bajar grasa, ganar músculo, dejar de improvisar | 1, 2, 3 |

## Para cambiar un texto

Se edita `contenido.json` y se vuelve a correr `semana.py`. Los precios, los
horarios y el WhatsApp están escritos dentro de los textos: si cambia alguno,
hay que buscarlo y reemplazarlo ahí.
