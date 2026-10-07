"""Socios que vencen HOY o MAÑANA, para el correo de cada mañana
(pedido de la dueña, 07-10-2026: "para cobrarles a tiempo").
Solo NOMBRE APELLIDO en mayúsculas, ordenados por nombre, sin pases diarios
(igual que el correo de vencidos de la semana).

Uso: python3 scripts/vencen-pronto.py <planilla-completa.xlsx> [AAAA-MM-DD]
Nunca guardar la salida en el repositorio: trae nombres de socios.
"""
import sys, datetime
import openpyxl

hoy = (datetime.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2
       else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).date())
manana = hoy + datetime.timedelta(days=1)

h = openpyxl.load_workbook(sys.argv[1])["Socios"]
filas = list(h.iter_rows(values_only=True))
cab = [str(c or "").strip().lower() for c in filas[0]]
iN, iA, iF = cab.index("nombre"), cab.index("apellido"), cab.index("fv")
iP = cab.index("plan") if "plan" in cab else None
grupos, vistos = {hoy: [], manana: []}, set()
for f in filas[1:]:
    if not f or not f[iN]:
        continue
    if iP is not None and "diario" in str(f[iP] or "").lower():
        continue
    fv = f[iF]
    if isinstance(fv, datetime.datetime):
        venc = fv.date()
    else:
        try:
            venc = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(float(fv)))
        except (TypeError, ValueError):
            continue
    if venc not in grupos:
        continue
    n, a = str(f[iN]).strip().upper(), str(f[iA] or "").strip().upper()
    if (n, a) in vistos:
        continue
    vistos.add((n, a))
    grupos[venc].append(f"{n} {a}".strip())
for titulo, d in (("VENCEN HOY", hoy), ("VENCEN MAÑANA", manana)):
    print(f"{titulo} ({len(grupos[d])})")
    for x in sorted(grupos[d]):
        print(x)
