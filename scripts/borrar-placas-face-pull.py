# Borra las placas de la columna derecha (la que no trabaja) del face pull: pinta de negro columna lo que no es persona ni cuerda.
# Uso: python3 scripts/borrar-placas-face-pull.py <fuente.mp4> <salida.mp4>  (la última línea guarda una vista previa en el scratchpad).
import sys,shutil,importlib.util,numpy as np,subprocess,os,tempfile
from PIL import Image
from scipy import ndimage
spec=importlib.util.spec_from_file_location('vm','scripts/video-maquina.py');vm=importlib.util.module_from_spec(spec);spec.loader.exec_module(vm)
src,dst=sys.argv[1],sys.argv[2]
fr=vm.leer_frames(src,0,11,None)
X0,X1,Y0,Y1=466,562,288,566
a0=np.asarray(fr[0]).astype(np.float32)
PINT=np.median(a0[200:280,480:550].reshape(-1,3),axis=0)
borde=np.zeros((Y1-Y0,X1-X0),np.float32); borde[6:-6,6:-6]=1; borde=ndimage.gaussian_filter(borde,3)
out=[]
for f in fr:
  a=np.asarray(f).astype(np.float32); r=a[Y0:Y1,X0:X1]
  R,G,B=r[...,0],r[...,1],r[...,2]; L=(R+G+B)/3
  persona=((R-B)>14)&(L>35)            # piel, pelo, top
  persona=ndimage.binary_opening(persona,structure=np.ones((5,5)))   # saca la cadena dorada (delgada)
  persona=ndimage.binary_dilation(persona,iterations=2)
  cuerda=(L>55)&(L<125)&(np.abs(R-B)<14)
  # cuerda: componentes grandes y texturadas -> se conservan si tocan el borde izquierdo o al pelo
  lab,n=ndimage.label(ndimage.binary_dilation(cuerda,iterations=1))
  keep=np.zeros_like(cuerda)
  for i in range(1,n+1):
    m=lab==i
    if m.sum()>400: keep|=m
  borrar=~(persona|keep)
  pint=PINT
  r2=r.copy(); r2[borrar]=pint
  sm=(ndimage.gaussian_filter(borrar.astype(np.float32),1.2)*borde)[...,None]
  r=r*(1-sm)+r2*sm
  a[Y0:Y1,X0:X1]=r
  out.append(Image.fromarray(np.clip(a,0,255).astype('uint8')))
tmp=tempfile.mkdtemp()
for i,im in enumerate(out): im.save(os.path.join(tmp,'%04d.png'%i))
FF='/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
subprocess.run([FF,'-v','error','-y','-framerate','24','-i',os.path.join(tmp,'%04d.png'),'-c:v','libx264','-crf','14','-pix_fmt','yuv420p',dst],check=True)
shutil.rmtree(tmp,ignore_errors=True)
W=Image.new('RGB',(5*260,460))
for i,k in enumerate((0,40,90,150,220)): W.paste(out[k].crop((420,100,680,560)),(i*260,0))
W.save('/tmp/claude-0/-home-user-wgymadnsport-archivos/ad6f257a-9f6a-5782-ada4-caec87e4604e/scratchpad/abd/rr2.jpg')
