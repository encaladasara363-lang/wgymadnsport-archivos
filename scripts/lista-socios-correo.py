"""Arma el texto del correo de respaldo semanal: la lista de socios de la
hoja "Socios" (apellido, nombre, plan, monto, vencimiento), ordenada por
apellido, en texto simple para pegar en el cuerpo del correo.

Uso: python3 scripts/lista-socios-correo.py <planilla-completa.xlsx>
Nunca guardar la salida en el repositorio: trae nombres de socios.
"""
import sys, datetime
import openpyxl

wb = openpyxl.load_workbook(sys.argv[1])
h = wb["Socios"]
filas = list(h.iter_rows(values_only=True))
cab = [str(c or "").strip().lower() for c in filas[0]]
def col(nombre):
    return cab.index(nombre) if nombre in cab else None
iN, iA, iP, iM, iF = col("nombre"), col("apellido"), col("plan"), col("monto"), col("fv")
socios = []
for f in filas[1:]:
    if not f or not f[iN]:
        continue
    fv = f[iF]
    try:
        venc = (datetime.date(1899, 12, 30) + datetime.timedelta(days=int(float(fv)))).strftime("%d-%m-%Y")
    except (TypeError, ValueError):
        venc = str(fv or "")
    monto = f[iM]
    try:
        monto = "$" + format(int(float(monto)), ",").replace(",", ".")
    except (TypeError, ValueError):
        monto = str(monto or "")
    socios.append((str(f[iA] or "").strip(), str(f[iN] or "").strip(), str(f[iP] or "").strip(), monto, venc))
socios.sort(key=lambda s: (s[0], s[1]))
print("SOCIOS (%d) - Apellido, Nombre | Plan | Monto | Vence" % len(socios))
for a, n, p, m, v in socios:
    print("%s, %s | %s | %s | %s" % (a, n, p, m, v))
