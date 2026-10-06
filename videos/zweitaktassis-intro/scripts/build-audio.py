# Baut assets/audio/vo.wav (Voiceover-Segmente neu getimt) und music.wav (synthetischer Beat mit Ducking).
# Aufruf: python build-audio.py <projektordner>  (braucht numpy + ffmpeg); danach zu mp3 encodieren.
import numpy as np, subprocess, json, sys, wave
P=sys.argv[1]; SR=44100
def load(path):
    raw=subprocess.run(["ffmpeg","-v","error","-i",path,"-f","f32le","-ac","1","-ar",str(SR),"-"],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32).copy()
vo=load(P+"/assets/audio/vo-take-a-raw.mp3")
# (src_start, src_end, global_start)
segs=[(0.0,2.81,0.8),(2.81,4.12,4.2),(4.12,5.53,5.85),(5.53,8.88,7.55),(8.88,11.10,11.15),
      (11.10,16.40,13.65),(16.40,19.83,19.25),(19.83,24.08,22.95),(24.08,27.95,27.55),(27.95,31.86,31.75)]
TOTAL=37.5
out=np.zeros(int(TOTAL*SR),dtype=np.float32)
for a,b,g in segs:
    s=vo[int(a*SR):int(b*SR)].copy()
    f=int(0.012*SR); s[:f]*=np.linspace(0,1,f); s[-f:]*=np.linspace(1,0,f)
    i=int(g*SR); out[i:i+len(s)]+=s
json.dump(segs,open(P+"/assets/audio/vo-segments.json","w"))
def save(path,x,ch=1):
    x=np.clip(x,-1,1); d=(x*32767).astype(np.int16)
    w=wave.open(path,"wb"); w.setnchannels(ch); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes()); w.close()
save(P+"/assets/audio/vo.wav",out)
# ---------- music ----------
rng=np.random.default_rng(7)
N=len(out); t=np.arange(N)/SR; L=np.zeros(N); R=np.zeros(N)
def add(sig,start,pan=0.0,gain=1.0):
    i=int(start*SR); n=min(len(sig),N-i)
    if n<=0: return
    L[i:i+n]+=sig[:n]*gain*(1-max(pan,0)); R[i:i+n]+=sig[:n]*gain*(1+min(pan,0))
def env(n,a,d):
    e=np.ones(n); ai=max(1,int(a*SR)); e[:ai]=np.linspace(0,1,ai); e*=np.exp(-np.arange(n)/SR/d); return e
def lp(x,alpha):
    y=np.zeros_like(x); acc=0.0
    for i in range(len(x)): acc+=alpha*(x[i]-acc); y[i]=acc
    return y
def onepole(x,fc):  # vectorised via scipy-free IIR approximation using cumulative trick
    a=np.exp(-2*np.pi*fc/SR); y=np.empty_like(x); acc=0.0
    for i in range(len(x)): acc=a*acc+(1-a)*x[i]; y[i]=acc
    return y
def kick():
    n=int(0.45*SR); tt=np.arange(n)/SR; f=45+110*np.exp(-tt*28); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-tt*7)*1.0 + 0.3*np.sin(ph)*np.exp(-tt*40)
def snare():
    n=int(0.3*SR); tt=np.arange(n)/SR; nz=rng.standard_normal(n)
    nz=nz-onepole(nz,900)
    return (0.55*nz*np.exp(-tt*16)+0.35*np.sin(2*np.pi*190*tt)*np.exp(-tt*25))
def hat(o=False):
    n=int((0.18 if o else 0.05)*SR); tt=np.arange(n)/SR; nz=rng.standard_normal(n); nz=nz-onepole(nz,7000)
    return nz*np.exp(-tt*(18 if o else 70))*0.25
K,SN,H,HO=kick(),snare(),hat(),hat(True)
# intro drone 0..5.85
DROP=5.85
n=int(DROP*SR); tt=np.arange(n)/SR
drone=0.18*(np.sign(np.sin(2*np.pi*55*tt))*0.4+np.sin(2*np.pi*55*tt)+0.5*np.sin(2*np.pi*82.41*tt+0.3)+0.3*np.sin(2*np.pi*110.3*tt))
drone=onepole(drone,350)*np.minimum(1,tt/1.5)
air=onepole(rng.standard_normal(n),600)*0.05*np.minimum(1,tt/2)
add(drone+air,0,0,1.0)
# two-stroke engine rev riser 4.3 -> 5.85
rs,re=4.3,DROP; n=int((re-rs)*SR); tt=np.arange(n)/SR; fr=18+55*(tt/(re-rs))**2
ph=np.cumsum(fr)/SR; pulse=(np.mod(ph,1)<0.18).astype(float)
eng=onepole(pulse*rng.standard_normal(n)*0.5+pulse,1800)*0.5*np.linspace(0.3,1,n)
add(eng,rs,0,0.9)
# beat
BPM=100; beat=60/BPM; bar=4*beat
bass_notes=[55.0,55.0,43.65,49.0]  # A1 A1 F1 G1
tcur=DROP; b=0; END=35.9
while tcur<END:
    calm = 27.55<=tcur<31.6
    for k in range(4):
        tb=tcur+k*beat
        if tb>=END: break
        if not calm or k==0: add(K,tb,0,0.9)
        if k in(1,3) and not calm: add(SN,tb,0,0.8)
        if k==2 and not calm and b%2==1: add(K,tb+beat*0.5,0,0.6)
        for h in range(2 if calm else 4):
            th=tb+h*beat/(2 if calm else 4)
            add(HO if (h==2 and k==3) else H,th,0.3 if h%2 else -0.3,0.0 if calm and h else 0.8)
    # sub bass
    f=bass_notes[b%4]; n=int(bar*SR); tt=np.arange(n)/SR
    gate=((np.mod(tt,beat)/beat)<0.7).astype(float)
    sub=(np.sin(2*np.pi*f*tt)+0.25*np.sin(2*np.pi*2*f*tt))*gate*0.33
    sub=onepole(sub,400)
    add(sub,tcur,0,0.6 if calm else 1.0)
    # pad chord in calm section
    if calm:
        pad=sum(np.sin(2*np.pi*fq*tt) for fq in (220,261.6,329.6))*0.05*np.minimum(1,tt/0.6)
        add(pad,tcur,0,1.0)
    tcur+=bar; b+=1
# final hit
add(K,35.9,0,1.0); add(SN,35.9,0,0.6)
n=int(1.6*SR); tt=np.arange(n)/SR; add(drone[:n]*np.exp(-tt*2)*1.5 if len(drone)>=n else 0,35.9,0,1.0)
mix=np.stack([L,R],1)
# sidechain duck under voice
venv=np.abs(out); w=int(0.05*SR); venv=np.convolve(venv,np.ones(w)/w,mode="same")
duck=1-0.55*np.clip(venv/0.04,0,1); duck=np.convolve(duck,np.ones(int(0.08*SR))/int(0.08*SR),mode="same")
mix*=duck[:,None]
mix/=np.max(np.abs(mix))+1e-9; mix*=0.5
save(P+"/assets/audio/music.wav",mix.reshape(-1),ch=2)
print("ok",len(out)/SR)
