"""Lista de socios que vencieron en la última semana (los 7 días antes de
hoy), para el correo de los domingos. Solo NOMBRE APELLIDO en mayúsculas,
ordenados alfabéticamente por nombre (pedido de la dueña, 04-10-2026), sin fechas ni otros datos (regla del CLAUDE.md).
No incluye los pases diarios.

Uso: python3 scripts/vencidos-semana.py <planilla-completa.xlsx> [AAAA-MM-DD]
Nunca guardar la salida en el repositorio: trae nombres de socios.
"""
import sys, datetime
import openpyxl

hoy = (datetime.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2
       else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).date())
desde = hoy - datetime.timedelta(days=7)

h = openpyxl.load_workbook(sys.argv[1])["Socios"]
filas = list(h.iter_rows(values_only=True))
cab = [str(c or "").strip().lower() for c in filas[0]]
iN, iA, iF = cab.index("nombre"), cab.index("apellido"), cab.index("fv")
iP = cab.index("plan") if "plan" in cab else None
vistos, lista = set(), []
for f in filas[1:]:
    if not f or not f[iN]:
        continue
    if iP is not None and "diario" in str(f[iP] or "").lower():
        continue  # el pase diario vence el mismo día: no es una mensualidad por cobrar
    fv = f[iF]
    if isinstance(fv, datetime.datetime):
        venc = fv.date()
    else:
        try:
            venc = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(float(fv)))
        except (TypeError, ValueError):
            continue
    if not (desde <= venc < hoy):
        continue
    n, a = str(f[iN]).strip().upper(), str(f[iA] or "").strip().upper()
    if (n, a) in vistos:
        continue
    vistos.add((n, a))
    lista.append((n, a))
lista.sort()
print(f"VENCIDOS DE LA SEMANA ({len(lista)})")
for n, a in lista:
    print(f"{n} {a}".strip())
