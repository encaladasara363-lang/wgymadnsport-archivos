# -*- coding: utf-8 -*-
"""Pictogramas propios, mismo trazo que los del gimnasio: palitos negros,
fierros en rojo. Dibujo original, nada bajado de internet."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patches as mp
from matplotlib.lines import Line2D
import math, os

OUT = os.environ.get("ICONOS_OUT") or os.path.dirname(os.path.abspath(__file__))
BLACK = os.environ.get('ICONOS_TRAZO', '#1a1a1a')
RED, LW = '#e30613', 5

def fig():
    f, ax = plt.subplots(figsize=(2.6,2.6), dpi=150)
    ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off'); ax.set_aspect('equal')
    return f, ax
def head(ax,x,y,r=.65): ax.add_patch(mp.Circle((x,y),r,fill=False,ec=BLACK,lw=LW))
def ln(ax,p,q,c=BLACK,lw=LW): ax.add_line(Line2D([p[0],q[0]],[p[1],q[1]],color=c,lw=lw,solid_capstyle='round'))
def barra(ax,x,y,ang=0,size=1.6,disco=.42):
    dx,dy = math.cos(math.radians(ang))*size, math.sin(math.radians(ang))*size
    ln(ax,(x-dx,y-dy),(x+dx,y+dy),RED,LW)
    ax.add_patch(mp.Circle((x-dx,y-dy),disco,fc=RED,ec=RED))
    ax.add_patch(mp.Circle((x+dx,y+dy),disco,fc=RED,ec=RED))
def mancuerna(ax,x,y,ang=0,size=.6): barra(ax,x,y,ang,size,.33)
def maquina(ax,pts): 
    for a,b in zip(pts, pts[1:]): ln(ax,a,b,RED,LW)
def save(f,n): f.savefig(os.path.join(OUT,n+".png"),transparent=True,bbox_inches='tight',pad_inches=.15); plt.close(f)

# ── PIERNA ────────────────────────────────────────────────────────────
f,ax = fig()                                            # sentadilla búlgara
head(ax,4.2,8.7); ln(ax,(4.2,8.05),(4.4,6.3))
ln(ax,(4.4,6.3),(3.1,5.0)); ln(ax,(3.1,5.0),(3.0,2.6))          # pierna adelante
ln(ax,(4.4,6.3),(6.0,5.7)); ln(ax,(6.0,5.7),(7.0,3.9))          # pierna atrás
ln(ax,(7.0,3.9),(7.9,4.4),RED,LW); ln(ax,(7.9,4.4),(7.9,2.6),RED,LW)   # banco
ln(ax,(4.1,7.5),(3.2,6.4)); ln(ax,(4.5,7.5),(5.4,6.4))
mancuerna(ax,3.1,5.9,90); mancuerna(ax,5.5,5.9,90)
save(f,'sentadilla_bulgara')

f,ax = fig()                                            # extensión de cuádriceps
head(ax,3.6,7.6); ln(ax,(3.6,6.95),(3.6,4.6))
ln(ax,(3.6,4.6),(5.6,4.6)); ln(ax,(5.6,4.6),(7.4,5.6))          # pierna estirando
maquina(ax,[(2.6,4.4),(2.6,7.2)])                                # respaldo
maquina(ax,[(2.6,4.4),(5.8,4.4)])                                # asiento
ax.add_patch(mp.Circle((7.4,5.6),.42,fc=RED,ec=RED))             # rodillo
ln(ax,(3.6,6.6),(2.7,5.6)); ln(ax,(3.6,6.6),(4.6,5.7))
save(f,'extension_cuadriceps')

f,ax = fig()                                            # curl femoral tumbada
head(ax,2.3,4.2); ln(ax,(2.95,4.0),(6.2,4.0))                    # tronco boca abajo
ln(ax,(6.2,4.0),(7.6,5.6))                                       # pierna flexionando
maquina(ax,[(1.9,3.4),(7.2,3.4)])                                # camilla
ax.add_patch(mp.Circle((7.7,5.8),.42,fc=RED,ec=RED))
save(f,'curl_femoral')

f,ax = fig()                                            # peso muerto rumano
head(ax,4.4,8.6); ln(ax,(4.4,7.95),(5.6,6.4))                    # torso inclinado
ln(ax,(5.6,6.4),(5.9,3.0))                                       # piernas casi rectas
ln(ax,(4.9,7.4),(4.6,5.2)); ln(ax,(5.4,7.3),(5.1,5.2))           # brazos colgando
barra(ax,4.85,4.9,0,1.9)
save(f,'peso_muerto_rumano')

f,ax = fig()                                            # hip thrust
head(ax,2.4,5.4); ln(ax,(3.05,5.3),(5.6,5.3))                    # tronco arriba
ln(ax,(5.6,5.3),(6.6,3.2)); ln(ax,(6.6,3.2),(7.6,3.2))           # pierna doblada
maquina(ax,[(1.6,4.6),(3.4,4.6)]); maquina(ax,[(1.6,4.6),(1.6,3.2)])  # banco
barra(ax,5.3,6.0,0,1.5)
save(f,'hip_thrust')

f,ax = fig()                                            # abducción de cadera
head(ax,5,7.8); ln(ax,(5,7.15),(5,5.0))
ln(ax,(5,5.0),(3.0,3.4)); ln(ax,(5,5.0),(7.0,3.4))               # piernas abriendo
maquina(ax,[(4.0,5.0),(4.0,3.9)]); maquina(ax,[(6.0,5.0),(6.0,3.9)])  # rodillos
ln(ax,(5,6.8),(3.9,5.9)); ln(ax,(5,6.8),(6.1,5.9))
save(f,'abduccion_cadera')

f,ax = fig()                                            # gemelo de pie
head(ax,5,8.6); ln(ax,(5,7.95),(5,4.4))
ln(ax,(5,4.4),(4.4,2.9)); ln(ax,(5,4.4),(5.6,2.9))
ln(ax,(4.4,2.9),(3.7,2.9)); ln(ax,(5.6,2.9),(6.3,2.9))           # puntas de pie
maquina(ax,[(3.2,2.5),(6.8,2.5)])                                # escalón
ln(ax,(5,7.4),(3.9,6.4)); ln(ax,(5,7.4),(6.1,6.4))
mancuerna(ax,3.7,6.0,90); mancuerna(ax,6.3,6.0,90)
save(f,'gemelos')

f,ax = fig()                                            # hiperextensión
head(ax,2.6,5.0); ln(ax,(3.25,5.0),(6.0,5.0))
ln(ax,(6.0,5.0),(6.8,3.0))
maquina(ax,[(5.2,4.4),(5.2,2.6)]); maquina(ax,[(4.4,4.4),(6.0,4.4)])
ln(ax,(3.6,4.9),(3.2,3.9)); ln(ax,(4.2,4.9),(3.8,3.9))
save(f,'hiperextension')

# ── EMPUJE ────────────────────────────────────────────────────────────
f,ax = fig()                                            # press inclinado
head(ax,3.0,4.6); ln(ax,(3.6,4.4),(6.4,3.2))                     # torso inclinado
ln(ax,(6.4,3.2),(7.6,3.2))
maquina(ax,[(2.6,3.9),(6.6,2.7)])                                # respaldo inclinado
ln(ax,(4.2,4.2),(4.4,6.2)); ln(ax,(5.2,3.8),(5.4,5.9))           # brazos arriba
barra(ax,4.9,6.3,10,1.7)
save(f,'press_inclinado')

f,ax = fig()                                            # extensión de tríceps en polea
head(ax,4.6,8.3); ln(ax,(4.6,7.65),(4.6,4.6))
ln(ax,(4.6,4.6),(4.0,2.6)); ln(ax,(4.6,4.6),(5.3,2.6))
ln(ax,(4.6,7.2),(5.8,6.4)); ln(ax,(5.8,6.4),(5.9,5.0))           # codo fijo, antebrazo abajo
maquina(ax,[(7.6,8.8),(7.6,6.0)]); maquina(ax,[(7.6,6.0),(6.1,5.1)])  # cable
barra(ax,5.9,4.9,0,.9,.3)
save(f,'extension_triceps')

f,ax = fig()                                            # elevación frontal / face pull
head(ax,4.4,8.3); ln(ax,(4.4,7.65),(4.4,4.6))
ln(ax,(4.4,4.6),(3.8,2.6)); ln(ax,(4.4,4.6),(5.1,2.6))
ln(ax,(4.4,7.2),(6.0,7.8)); ln(ax,(6.0,7.8),(7.2,7.2))           # tirón a la cara
maquina(ax,[(8.6,8.6),(8.6,7.4)]); maquina(ax,[(8.6,7.4),(7.3,7.2)])
ax.add_patch(mp.Circle((7.3,7.2),.36,fc=RED,ec=RED))
save(f,'face_pull')

# ── TIRÓN ─────────────────────────────────────────────────────────────
f,ax = fig()                                            # dominada
maquina(ax,[(2.2,8.8),(7.8,8.8)])                                # barra fija
head(ax,5,7.0); ln(ax,(5,6.35),(5,4.0))
ln(ax,(5,4.0),(4.3,2.4)); ln(ax,(5,4.0),(5.7,2.4))
ln(ax,(5,6.5),(3.6,8.7)); ln(ax,(5,6.5),(6.4,8.7))               # brazos a la barra
save(f,'dominadas')

# ── ABDOMEN ───────────────────────────────────────────────────────────
f,ax = fig()                                            # rueda abdominal
head(ax,3.4,6.4); ln(ax,(4.0,6.2),(5.4,4.2))                     # torso extendido
ln(ax,(5.4,4.2),(6.4,2.8))                                       # rodillas al piso
ln(ax,(4.0,6.2),(2.6,4.6))                                       # brazos adelante
ax.add_patch(mp.Circle((2.2,4.0),.85,fill=False,ec=RED,lw=LW))
ln(ax,(1.3,4.0),(3.1,4.0),RED,LW)
save(f,'rueda_abdominal')

f,ax = fig()                                            # elevación de piernas colgada
maquina(ax,[(2.4,9.0),(7.6,9.0)])
head(ax,5,7.2); ln(ax,(5,6.55),(5,4.2))
ln(ax,(5,6.9),(4.0,8.9)); ln(ax,(5,6.9),(6.0,8.9))
ln(ax,(5,4.2),(6.9,4.2)); ln(ax,(6.9,4.2),(7.4,5.4))             # piernas al frente
save(f,'elevacion_piernas')

f,ax = fig()                                            # pallof press · anti-giro
head(ax,4.2,8.3); ln(ax,(4.2,7.65),(4.2,4.6))
ln(ax,(4.2,4.6),(3.4,2.6)); ln(ax,(4.2,4.6),(5.2,2.6))
ln(ax,(4.2,7.0),(2.4,7.0))                                       # brazos al frente
maquina(ax,[(8.4,8.4),(8.4,7.0)]); maquina(ax,[(8.4,7.0),(4.3,7.0)])
ax.add_patch(mp.Circle((2.3,7.0),.36,fc=RED,ec=RED))
save(f,'pallof')

f,ax = fig()                                            # vacío abdominal
head(ax,5,8.4); ln(ax,(5,7.75),(5,4.6))
ln(ax,(5,4.6),(4.3,2.6)); ln(ax,(5,4.6),(5.7,2.6))
ln(ax,(5,7.3),(3.7,6.2)); ln(ax,(5,7.3),(6.3,6.2))
ax.add_patch(mp.Arc((5,6.0),2.6,2.2,theta1=200,theta2=340,ec=RED,lw=LW))  # guata adentro
save(f,'vacio_abdominal')

print("pictogramas nuevos listos")
# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patches as mp
from matplotlib.lines import Line2D
import math, os
OUT = os.environ.get("ICONOS_OUT") or os.path.dirname(os.path.abspath(__file__))
BLACK = os.environ.get('ICONOS_TRAZO', '#1a1a1a')
RED, LW = '#e30613', 5
def fig():
    f,ax = plt.subplots(figsize=(2.6,2.6),dpi=150)
    ax.set_xlim(0,10); ax.set_ylim(0,10); ax.axis('off'); ax.set_aspect('equal'); return f,ax
def head(ax,x,y,r=.62): ax.add_patch(mp.Circle((x,y),r,fill=False,ec=BLACK,lw=LW))
def ln(ax,p,q,c=BLACK,lw=LW): ax.add_line(Line2D([p[0],q[0]],[p[1],q[1]],color=c,lw=lw,solid_capstyle='round'))
def maquina(ax,pts):
    for a,b in zip(pts,pts[1:]): ln(ax,a,b,RED,LW)
def barra(ax,x,y,ang=0,size=1.6,disco=.4):
    dx,dy = math.cos(math.radians(ang))*size, math.sin(math.radians(ang))*size
    ln(ax,(x-dx,y-dy),(x+dx,y+dy),RED,LW)
    ax.add_patch(mp.Circle((x-dx,y-dy),disco,fc=RED,ec=RED)); ax.add_patch(mp.Circle((x+dx,y+dy),disco,fc=RED,ec=RED))
def save(f,n): f.savefig(os.path.join(OUT,n+".png"),transparent=True,bbox_inches='tight',pad_inches=.15); plt.close(f)

# dominada — la cabeza queda BAJO la barra, los brazos salen del hombro
f,ax = fig()
maquina(ax,[(1.8,9.2),(8.2,9.2)])
head(ax,5,6.5)
ln(ax,(5,5.88),(5,3.4))                       # tronco
ln(ax,(5,3.4),(4.2,1.6)); ln(ax,(5,3.4),(5.8,1.6))
ln(ax,(4.55,6.9),(3.3,9.15)); ln(ax,(5.45,6.9),(6.7,9.15))   # brazos a la barra
save(f,'dominadas')

# elevación de piernas colgada — igual criterio
f,ax = fig()
maquina(ax,[(1.8,9.2),(8.2,9.2)])
head(ax,4.2,6.5)
ln(ax,(4.2,5.88),(4.2,3.6))
ln(ax,(3.75,6.9),(2.9,9.15)); ln(ax,(4.65,6.9),(5.5,9.15))
ln(ax,(4.2,3.6),(6.6,3.6)); ln(ax,(6.6,3.6),(7.2,4.9))       # piernas al frente
save(f,'elevacion_piernas')

# press inclinado — banco claro, piernas apoyadas
f,ax = fig()
maquina(ax,[(1.7,2.4),(1.7,4.0)]); maquina(ax,[(1.7,4.0),(6.4,2.4)])   # respaldo inclinado
maquina(ax,[(6.4,2.4),(8.3,2.4)])                                      # asiento
head(ax,2.5,4.9)
ln(ax,(3.1,4.7),(6.3,3.0))                                             # torso
ln(ax,(6.3,3.0),(7.6,3.9)); ln(ax,(7.6,3.9),(8.6,2.6))                 # pierna
ln(ax,(3.9,4.3),(4.5,6.6)); ln(ax,(5.1,3.9),(5.6,6.5))                 # brazos arriba
barra(ax,5.05,6.8,8,1.9)
save(f,'press_inclinado')

# hiperextensión — banco romano legible
f,ax = fig()
maquina(ax,[(6.0,5.2),(6.0,2.2)]); maquina(ax,[(4.9,5.2),(7.1,5.2)])   # almohadilla + poste
maquina(ax,[(6.6,3.0),(7.9,3.0)])                                      # tope de tobillos
head(ax,2.3,5.6)
ln(ax,(2.9,5.5),(6.2,5.0))                                             # tronco extendido
ln(ax,(6.2,5.0),(7.4,3.2))                                             # piernas al tope
ln(ax,(3.5,5.4),(3.2,6.6)); ln(ax,(4.1,5.3),(3.8,6.5))                 # brazos al pecho
save(f,'hiperextension')
print("rehechos")


# sentadilla en maquina hack — plataforma inclinada y hombreras
f,ax = fig()
maquina(ax,[(1.5,2.0),(8.5,4.8)])                       # plataforma inclinada
maquina(ax,[(7.6,4.4),(8.8,7.0)])                       # riel de la maquina
ln(ax,(6.3,6.0),(8.2,6.7),RED,LW)                       # hombreras
head(ax,5.6,6.2)
ln(ax,(5.2,5.65),(3.9,4.2))                             # tronco contra el respaldo
ln(ax,(3.9,4.2),(2.9,5.0)); ln(ax,(2.9,5.0),(2.4,3.2))  # pierna flexionada
ln(ax,(3.9,4.2),(3.3,2.9))                              # segunda pierna
save(f,'sentadilla_hack')

# plancha lateral — apoyo en un antebrazo, cuerpo en linea
f,ax = fig()
head(ax,2.2,6.4)
ln(ax,(2.8,6.1),(7.6,3.6))                              # cuerpo en diagonal recta
ln(ax,(7.6,3.6),(8.6,3.2))                              # pies
ln(ax,(3.1,5.95),(2.9,4.2)); ln(ax,(2.9,4.2),(4.1,4.2)) # antebrazo de apoyo
maquina(ax,[(1.8,3.9),(8.9,3.9)])                       # piso
save(f,'plancha_lateral')
print("sentadilla_hack y plancha_lateral dibujadas")


# bicicleta estatica — rueda grande al frente, sillin y manubrio en rojo
f,ax = fig()
ax.add_patch(mp.Circle((6.2,3.0),1.6,fill=False,ec=RED,lw=LW))  # volante, grande y claro
maquina(ax,[(4.3,3.3),(4.3,5.8)])                        # poste del asiento
maquina(ax,[(3.7,5.9),(4.6,5.9)])                        # sillin
maquina(ax,[(4.3,3.3),(6.2,3.0)])                        # tubo al eje
maquina(ax,[(6.2,3.0),(5.6,6.2)])                        # tubo al manubrio
maquina(ax,[(5.1,6.3),(6.1,6.4)])                        # manubrio
head(ax,4.0,7.0)
ln(ax,(4.0,6.38),(4.3,5.8))                              # torso corto sentado
ln(ax,(4.2,6.5),(5.6,6.3))                                # brazo al manubrio
ln(ax,(4.3,5.8),(5.3,4.2)); ln(ax,(5.3,4.2),(6.0,2.6))    # pierna pedaleando
save(f,'bicicleta')
print("bicicleta redibujada")

# abdominales / crunch — acostado, rodilla doblada, hombros curvados hacia arriba
f,ax = fig()
maquina(ax,[(1.0,2.3),(9.0,2.3)])                      # piso
ln(ax,(5.6,2.3),(7.0,4.6))                              # muslo (rodilla doblada)
ln(ax,(7.0,4.6),(8.1,2.3))                              # pantorrilla al piso
ln(ax,(5.6,2.3),(3.4,3.15))                             # torso curvado hacia arriba
ln(ax,(3.5,3.35),(2.9,4.15))                            # brazo hacia la cabeza
head(ax,2.55,4.55)
save(f,'crunch')
print("crunch dibujado")
