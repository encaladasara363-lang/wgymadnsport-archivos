"""Resumen semanal de la Tienda WGYM, para el correo de los domingos (pedido de la dueña, 27-10-2026, idea 7).

Lee las hojas «Tienda productos» y «Tienda movimientos» de la planilla descargada como xlsx y arma:
lo vendido en los últimos 7 días (hasta hoy), la ganancia, la comparación con la semana anterior, medios de pago,
lo que más se vendió, cada categoría, su parte (30 % de la ganancia), fiados pendientes, qué reponer y qué vence.

Uso: python3 scripts/tienda-semana.py <planilla-completa.xlsx> [AAAA-MM-DD] [--html]
Nunca guardar la salida en el repositorio: trae costos, ganancias y nombres de quienes deben fiado.
"""
import sys, datetime, html
# Fondo blanco y letra negra (27-10-2026): el modo oscuro de Gmail en iPhone dejaba casi invisibles las letras blancas.
import openpyxl

args = [a for a in sys.argv[1:] if not a.startswith("--")]
HTML = "--html" in sys.argv
hoy = (datetime.date.fromisoformat(args[1]) if len(args) > 1
       else datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).date())
desde = hoy - datetime.timedelta(days=6)          # lunes a domingo si se corre el domingo
desde_ant = desde - datetime.timedelta(days=7)
PARTE = 0.30                                       # la dueña quiere el 30 % de la ganancia (CLAUDE.md, 24-10-2026)
UNICAS = ("Ropa", "Zapatillas")                    # prendas de una sola unidad: no se sugiere reponerlas
SIN_STOCK_PROPIO = ("batido ganador",)             # salen del tarro del «Batido de proteína» (USA_PORCION)

wb = openpyxl.load_workbook(args[0], data_only=True)

def filas(nombre):
    h = wb[nombre]
    r = list(h.iter_rows(values_only=True))
    cab = [str(c or "").strip() for c in r[0]]
    return [dict(zip(cab, f)) for f in r[1:] if f and f[0]]

def num(v):
    try: return float(v or 0)
    except (TypeError, ValueError): return 0.0

def dia(v):
    if isinstance(v, datetime.datetime): return v.date()
    if isinstance(v, datetime.date): return v
    try: return datetime.date.fromisoformat(str(v).strip().lstrip("'")[:10])
    except ValueError: return None

def cat(c):
    c = str(c or "Otro")
    return {"Bebidas": "Bebestibles", "Ropa deportiva": "Ropa mujer"}.get(c, c)

def plata(n): return "$" + f"{round(n):,}".replace(",", ".")

prods = {str(p["Id"]): p for p in filas("Tienda productos")}
movs = filas("Tienda movimientos")
ventas = [m for m in movs if m.get("Tipo") == "venta" and str(m.get("Estado") or "") != "anulada" and dia(m.get("Fecha"))]

def resumen(d1, d2):
    vs = [m for m in ventas if d1 <= dia(m["Fecha"]) <= d2]
    tot = sum(num(m["Total"]) for m in vs)
    gan = sum(num(m["Total"]) - num(m["Cantidad"]) * num(m["Costo unit."]) for m in vs)
    return vs, tot, gan

vs, tot, gan = resumen(desde, hoy)
_, tot_ant, gan_ant = resumen(desde_ant, desde - datetime.timedelta(days=1))
uds = sum(num(m["Cantidad"]) for m in vs)
n_ventas = len({str(m.get("Venta") or "") for m in vs})

pagos = {}
for m in vs:
    p = str(m.get("Pago") or "otro"); pagos[p] = pagos.get(p, 0) + num(m["Total"])

por_prod = {}
for m in vs:
    k = str(m.get("Producto") or "")
    x = por_prod.setdefault(k, [0, 0.0])
    x[0] += num(m["Cantidad"]); x[1] += num(m["Total"]) - num(m["Cantidad"]) * num(m["Costo unit."])
top = sorted(por_prod.items(), key=lambda kv: (-kv[1][0], -kv[1][1]))[:5]

por_cat = {}
for m in vs:
    p = prods.get(str(m.get("Id producto") or ""), {})
    c = cat(p.get("Categoría"))
    x = por_cat.setdefault(c, [0.0, 0.0])
    x[0] += num(m["Total"]); x[1] += num(m["Total"]) - num(m["Cantidad"]) * num(m["Costo unit."])

fiados = {}
for m in movs:
    if m.get("Tipo") == "venta" and str(m.get("Estado") or "") == "fiado":
        k = str(m.get("Cliente") or "SIN NOMBRE").upper(); fiados[k] = fiados.get(k, 0) + num(m["Total"])

# Qué reponer: lo que está en el aviso o le alcanza para 10 días o menos (misma regla que «🛍 Qué comprar»)
hace30 = hoy - datetime.timedelta(days=30)
vend30 = {}
for m in ventas:
    if dia(m["Fecha"]) > hace30:
        i = str(m.get("Id producto") or ""); vend30[i] = vend30.get(i, 0) + num(m["Cantidad"])
base = next((i for i, p in prods.items() if str(p.get("Nombre", "")).lower().startswith("batido de prote")), None)
for i, p in prods.items():   # las ventas del ganador cuentan para el tarro
    if base and str(p.get("Nombre", "")).lower().startswith(SIN_STOCK_PROPIO): vend30[base] = vend30.get(base, 0) + vend30.get(i, 0)
reponer = []
for i, p in prods.items():
    if str(p.get("Activo", "sí")) == "no": continue
    nombre = str(p.get("Nombre") or "")
    if nombre.lower().startswith(SIN_STOCK_PROPIO): continue
    st, mi = num(p.get("Stock")), num(p.get("Mínimo"))
    if cat(p.get("Categoría")).startswith(UNICAS): continue   # prenda única: no se repone
    v = vend30.get(i, 0); alcanza = st / (v / 30) if v else float("inf")
    if st <= mi or alcanza <= 10:
        comprar = max(1, max(round(v), mi * 2, mi + 1) - max(0, st))
        reponer.append((nombre, str(p.get("Detalle") or ""), int(st), int(comprar)))
reponer.sort(key=lambda r: r[2])

vencen = []
for p in prods.values():
    if str(p.get("Activo", "sí")) == "no" or num(p.get("Stock")) <= 0: continue
    d = dia(p.get("Vence"))
    if d and (d - hoy).days <= 30: vencen.append((str(p.get("Nombre")), d, (d - hoy).days))
vencen.sort(key=lambda r: r[1])

prendas = [str(m.get("Producto")) for m in vs if cat(prods.get(str(m.get("Id producto") or ""), {}).get("Categoría")).startswith(UNICAS)]

def cambio(a, b):
    if not b: return "primera semana con ventas" if a else "sin ventas"
    d = (a - b) / b * 100
    return ("▲ " if d >= 0 else "▼ ") + f"{abs(d):.0f} % vs. semana anterior ({plata(b)})"

titulo = f"RESUMEN DE LA TIENDA · {desde.strftime('%d-%m')} al {hoy.strftime('%d-%m-%Y')}"
NOMBRES_PAGO = {"efectivo": "💵 Efectivo", "transferencia": "🏦 Transferencia", "tarjeta": "💳 Tarjeta", "fiado": "📒 Fiado"}
sec = []   # (título, [líneas])
sec.append(("💰 La semana", [f"Vendido: {plata(tot)} ({cambio(tot, tot_ant)})",
                             f"Ganancia: {plata(gan)} ({cambio(gan, gan_ant)})",
                             f"Tu parte (30 % de la ganancia): {plata(gan * PARTE)} · para reinvertir: {plata(gan * (1 - PARTE))}",
                             f"{int(uds)} productos en {n_ventas} ventas"]))
if pagos: sec.append(("💳 Cómo te pagaron", [f"{NOMBRES_PAGO.get(k, k)}: {plata(v)}" for k, v in sorted(pagos.items(), key=lambda kv: -kv[1])]))
if top: sec.append(("🏆 Lo que más se vendió", [f"{int(q)} × {n} (ganaste {plata(g)})" for n, (q, g) in top]))
if por_cat: sec.append(("📦 Por categoría", [f"{c}: vendido {plata(v)} · ganancia {plata(g)}" for c, (v, g) in sorted(por_cat.items(), key=lambda kv: -kv[1][0])]))
if prendas: sec.append(("🏷 Prendas vendidas (salen «VENDIDO» 15 días)", prendas))
sec.append(("📒 Fiados por cobrar", [f"{k}: {plata(v)}" for k, v in sorted(fiados.items(), key=lambda kv: -kv[1])] + [f"Total: {plata(sum(fiados.values()))}"] if fiados else ["Nadie te debe ✅"]))
sec.append(("🛍 Para reponer", [f"{n}{' · ' + d if d else ''}: quedan {s} → comprar {c}" for n, d, s, c in reponer] if reponer else ["Tienes de todo ✅"]))
if vencen: sec.append(("⏰ Por vencer (30 días)", [f"{n}: {'VENCIDO' if dd < 0 else 'vence el ' + d.strftime('%d-%m-%Y')}" for n, d, dd in vencen]))

if not HTML:
    print(titulo)
    for t, ls in sec:
        print("\n" + t)
        for l in ls: print("• " + l)
else:
    e = html.escape
    out = [f'<div style="font-family:Arial,sans-serif;max-width:640px;margin:auto;background:#ffffff;color:#111111;padding:18px;border:3px solid #E30613;border-radius:12px">',
           f'<h1 style="font-size:22px;margin:0 0 6px;color:#111111;border-bottom:4px solid #E30613;padding-bottom:8px">🛒 {e(titulo)}</h1>']
    for t, ls in sec:
        out.append(f'<h2 style="font-size:19px;color:#E30613;margin:18px 0 6px">{e(t)}</h2><ul style="margin:0;padding-left:20px">')
        out += [f'<li style="font-size:17px;margin:5px 0;color:#111111">{e(l)}</li>' for l in ls]
        out.append("</ul>")
    out.append('<p style="font-size:14px;color:#444444;margin-top:18px">Abre la tienda para ver el detalle: '
               '<a style="color:#E30613" href="https://encaladasara363-lang.github.io/wgymadnsport-archivos/tienda.html">tienda.html</a></p></div>')
    print("\n".join(out))
