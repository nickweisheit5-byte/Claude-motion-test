# Schneidet die Segmente aus dem Rohvideo, croppt auf 9:16, skaliert auf 1080x1920 (lanczos + unsharp)
# und normalisiert den O-Ton. Aufruf: python3 scripts-cut.py <rohvideo> <projektordner>
import json, subprocess, sys, os
src, proj = sys.argv[1], sys.argv[2]
segs = json.load(open(os.path.join(proj, "segments.json")))
W, H, CW = 960, 540, 304
t_out = 0.0
timeline = []
for s in segs:
    a0, a1 = s["a"]; d = round(a1 - a0, 3); v0 = s["v"]
    x = max(0, min(W - CW, int(s["cx"] - CW / 2)))
    vf = (f"crop={CW}:{H}:{x}:0,scale=1080:1920:flags=lanczos,hqdn3d=1.5:1.5:4:4,"
          f"unsharp=5:5:0.9:5:5:0.0,eq=contrast=1.06:saturation=1.12,fps=30,format=yuv420p")
    af = f"volume=6dB,alimiter=limit=0.89,afade=t=in:d=0.02,afade=t=out:st={d-0.03:.3f}:d=0.03,aresample=48000"
    out = os.path.join(proj, "assets/clips", f"{s['id']}.mp4")
    cmd = ["ffmpeg", "-v", "error", "-y",
           "-ss", f"{v0}", "-t", f"{d}", "-i", src,
           "-ss", f"{a0}", "-t", f"{d}", "-i", src,
           "-map", "0:v:0", "-map", "1:a:0", "-vf", vf, "-af", af,
           "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-g", "15",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    timeline.append({**s, "dur": d, "start": round(t_out, 3)})
    t_out += d
json.dump(timeline, open(os.path.join(proj, "timeline.json"), "w"), indent=1)
print("total", round(t_out, 2))
