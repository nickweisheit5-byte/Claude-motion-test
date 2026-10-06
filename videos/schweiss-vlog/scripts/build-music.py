# Synthetischer Beat (96 BPM) als Musikbett unter dem O-Ton. Aufruf: python build-music.py <out.wav> <dauer>
import numpy as np, sys, wave
SR=44100; out=sys.argv[1]; T=float(sys.argv[2]); N=int(T*SR)
rng=np.random.default_rng(11); L=np.zeros(N); R=np.zeros(N)
def onepole(x,fc):
    a=np.exp(-2*np.pi*fc/SR); y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc=a*acc+(1-a)*x[i]; y[i]=acc
    return y
def add(sig,start,pan=0.0,g=1.0):
    i=int(start*SR); n=min(len(sig),N-i)
    if n>0: L[i:i+n]+=sig[:n]*g*(1-max(pan,0)); R[i:i+n]+=sig[:n]*g*(1+min(pan,0))
def kick():
    n=int(0.4*SR); t=np.arange(n)/SR; f=48+100*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8)
def snare():
    n=int(0.25*SR); t=np.arange(n)/SR; z=rng.standard_normal(n); z=z-onepole(z,1000); return 0.5*z*np.exp(-t*18)+0.3*np.sin(2*np.pi*200*t)*np.exp(-t*30)
def hat():
    n=int(0.05*SR); t=np.arange(n)/SR; z=rng.standard_normal(n); z=z-onepole(z,7000); return z*np.exp(-t*70)*0.22
K,SN,H=kick(),snare(),hat()
beat=60/96; bar=4*beat; notes=[55.0,55.0,65.41,49.0]; t0=0.0; b=0
while t0<T:
    for k in range(4):
        tb=t0+k*beat
        add(K,tb,0,0.9 if k in (0,2) else 0)
        if k in (1,3): add(SN,tb,0,0.7)
        if k==3 and b%2: add(K,tb+beat/2,0,0.5)
        for h in range(2): add(H,tb+h*beat/2,0.3 if h else -0.3,0.8)
    n=int(bar*SR); t=np.arange(n)/SR; f=notes[b%4]
    gate=((np.mod(t,beat)/beat)<0.6).astype(float)
    add(onepole((np.sin(2*np.pi*f*t)+0.3*np.sign(np.sin(2*np.pi*f*t)))*gate*0.3,350),t0)
    t0+=bar; b+=1
m=np.stack([L,R],1); fade=int(1.5*SR); m[-fade:]*=np.linspace(1,0,fade)[:,None]
m/=np.max(np.abs(m))+1e-9; m*=0.6
w=wave.open(out,"wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m.reshape(-1)*32767).astype(np.int16).tobytes()); w.close()
