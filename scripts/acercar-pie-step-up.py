# Desliza el pie de atrás hacia la banca en fuentes/ejercicio-gemini.mp4 del step-up en polea (pedido de la dueña,
# 18-10-2026: "que el pie se acerque más a la banca"). Comprime solo el piso entre el pie y la pata de la banca.
# Se usó cuadro a cuadro para generar fuentes/ejercicio-gemini-pie-cerca.mp4.
import numpy as np
from scipy import ndimage
def campo(H=720,W=1280,D=30):
    yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
    wx=np.clip((603-xx)/43,0,1)*np.clip((xx-445)/60,0,1)
    wy=np.clip((yy-470)/70,0,1)*np.clip((660-yy)/30,0,1)
    return yy, xx-D*wx*wy
def aplicar(a,c):
    yy,xs=c
    return np.stack([ndimage.map_coordinates(a[...,k].astype(np.float32),[yy,xs],order=1,mode='nearest') for k in range(3)],-1).clip(0,255).astype('uint8')


# Versión que eligió la dueña (18-10-2026): tramo de ida y vuelta de Grok (720x1264), pie deslizado ~70 px.
# Genera fuentes/tramo-ida-vuelta-pie-cerca.mp4.
def campo_grok(H=1264, W=720, D=70):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    wx = np.clip((362 - xx) / 72, 0, 1) * np.clip(xx / 110, 0, 1)
    wy = np.clip((yy - 640) / 90, 0, 1) * np.clip((960 - yy) / 40, 0, 1)
    return yy, xx - D * wx * wy
