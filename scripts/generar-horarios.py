"""Genera horarios.json: cuánta gente suele haber en el gimnasio a cada hora,
por día de la semana, a partir de la hoja de ingresos del check-in.

Uso: python3 scripts/generar-horarios.py ingresos.csv
(ingresos.csv = la hoja "WGYMADNSPORT - Ingresos por Tarjeta QR" descargada
como CSV; NO se sube al repo porque trae nombres).

horarios.json solo guarda promedios por hora: nunca nombres ni horas de
ingreso individuales. "Personas" a una hora = cuántas personas distintas
habían entrado en las VENTANA_HORAS anteriores (la misma regla que usa el
contador "Dentro ahora" de la tarjeta para quien no marcó su salida).
"""
import csv, json, sys, datetime, collections
from zoneinfo import ZoneInfo

VENTANA_HORAS = 2
TZ = ZoneInfo("America/Santiago")
# Horario del cartel: lunes=0 … sábado=5; domingo cerrado.
HORARIO = {0: (8, 23), 1: (8, 23), 2: (8, 23), 3: (8, 23), 4: (9, 23), 5: (10, 22)}

def leer(ruta):
    porDia = collections.defaultdict(list)
    with open(ruta, encoding="utf-8") as f:
        for r in csv.reader(f):
            if not r or not r[0].strip().isdigit():
                continue
            t = datetime.datetime.fromtimestamp(int(r[0]) / 1000, TZ)
            quien = (r[1].strip().upper(), r[2].strip().upper())
            porDia[t.date()].append((t, quien))
    return porDia

def main(ruta):
    porDia = leer(ruta)
    hoy = datetime.datetime.now(TZ).date()
    dias = sorted(d for d in porDia if d < hoy and d.weekday() in HORARIO)
    sumas = collections.defaultdict(float)
    cuantos = collections.Counter()
    for d in dias:
        abre, cierra = HORARIO[d.weekday()]
        cuantos[d.weekday()] += 1
        for h in range(abre, cierra + 1):
            corte = datetime.datetime(d.year, d.month, d.day, h, tzinfo=TZ)
            desde = corte - datetime.timedelta(hours=VENTANA_HORAS)
            gente = {q for t, q in porDia[d] if desde < t <= corte}
            sumas[(d.weekday(), h)] += len(gente)
    salida = {"actualizado": hoy.isoformat(), "desde": dias[0].isoformat(),
              "hasta": dias[-1].isoformat(), "ventanaHoras": VENTANA_HORAS,
              "nota": "Promedio de personas en el gimnasio a cada hora (sin nombres).",
              "dias": {}}
    for wd, (abre, cierra) in HORARIO.items():
        n = cuantos[wd] or 1
        salida["dias"][str(wd + 1)] = [
            {"h": h, "p": round(sumas[(wd, h)] / n, 1)} for h in range(abre, cierra + 1)]
        salida["dias"][str(wd + 1) + "_n"] = cuantos[wd]
    print(json.dumps(salida, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main(sys.argv[1])
