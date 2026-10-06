# Erzeugt index.html (HyperFrames-Komposition) aus timeline.json, dem Wort-Transkript und den Overlays unten.
# Aufruf: python3 scripts/build-html.py <words.json>
import json, sys, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
timeline = json.load(open(os.path.join(ROOT, "timeline.json")))
words = json.load(open(sys.argv[1]))["words"]
TOTAL = round(sum(s["dur"] for s in timeline), 2)
END_HOLD = 0.0
DUR = TOTAL + END_HOLD


def to_out(src):
    """Quellzeit (O-Ton) -> Zeit im Schnitt, oder None wenn rausgeschnitten."""
    for s in timeline:
        a0, a1 = s["a"]
        if a0 - 1e-6 <= src <= a1 + 1e-6:
            return round(s["start"] + (src - a0), 3), s
    return None, None


# ---------- Untertitel ----------
FILLERS = {"äh", "ähm", "äh,", "ähm,", "ähm.", "äh."}
caps = []  # [{start,end,words:[{t,text}]}]
cur = None
for w in words:
    txt = w["text"].strip()
    if not txt or txt.lower() in FILLERS:
        continue
    t, seg = to_out(w["start"])
    te, _ = to_out(w["end"])
    if t is None:
        continue
    if te is None:
        te = seg["start"] + seg["dur"]
    brk = (
        cur is None
        or cur["seg"] != seg["id"]
        or len(cur["words"]) >= 3
        or t - cur["end"] > 0.35
        or cur["words"][-1]["text"][-1] in ".?!:"
    )
    if brk:
        cur = {"seg": seg["id"], "start": t, "end": te, "words": []}
        caps.append(cur)
    cur["words"].append({"t": t, "text": txt.rstrip(",")})
    cur["end"] = te
# Gruppe bleibt stehen bis kurz vor der nächsten (max. Segmentende)
for i, c in enumerate(caps):
    seg_end = next(s["start"] + s["dur"] for s in timeline if s["id"] == c["seg"])
    nxt = caps[i + 1]["start"] if i + 1 < len(caps) else DUR
    c["end"] = round(min(max(c["end"] + 0.25, c["start"] + 0.5), nxt, seg_end), 3)

# ---------- Overlays (Quellzeit, Typ, Text) ----------
OV = [
    (0.75, "stamp red", "TAKE 1 ❌"),
    (4.66, "banner", "ZWEITAKT-MOTORRENNSPORT 🏁"),
    (6.60, "wow w1", "WOW"), (6.92, "wow w2", "WOW"), (7.14, "wow w3", "WOW"), (7.18, "wow w4", "WOW"),
    (7.82, "wow w5", "WOW"), (7.86, "wow w6", "WOW"), (7.90, "wow w7", "WOW"),
    (10.24, "banner", "MOPED NR. 2"),
    (11.16, "banner b2", "… ODER NR. 3? 🤔"),
    (23.34, "banner", "RAHMEN IN BEARBEITUNG 🚧"),
    (27.02, "banner", "DAS WUNDERVOLLSTE FÜLLDRAHT-SCHWEISSGERÄT"),
    (27.90, "stars", "★★★★★"),
    (29.40, "stamp red", "GEHT ABSOLUT SCHEISSE"),
    (37.30, "banner", "AALGLATT ✨"),
    (38.32, "sticker", "🪞 SPIEGEL-FINISH"),
    (39.60, "stamp", "SCHLEIFEN? NÖ."),
    (50.50, "banner", "VERSTÄRKUNGSBLECHE 💪"),
    (53.46, "sticker", "↓ RAHMENFUSS"),
    (77.82, "banner", "WIE BEI LUCA."),
    (78.38, "stamp", "NUR BESSER 😏"),
    (83.04, "banner", "KURZ RÜBER ZU LUCA 👀"),
    (85.45, "big", "OH OH 😬"),
    (88.96, "banner", "„FANTASTISCH ANGEPASST“"),
    (89.40, "ring", ""),
    (92.42, "stamp red", "NICHT ABGESCHLIFFEN ❌"),
    (95.18, "banner", "WER BRAUCHT DAS SCHON? 🤷"),
    (102.32, "stamp", "ECHTE PROFIS SCHLEIFEN NICHT."),
    (106.62, "banner", "ECHTER RENNFAHRER ="),
    (108.70, "big", "2× PRO WOCHE"),
    (109.48, "stamp red", "AUF DIE FRESSE 💥"),
    (112.46, "banner", "ALLES ANDERE = KEINE ECHTEN TUNER"),
    (114.12, "sticker", "DAS MOTTO 👆"),
    (115.25, "stamp", "PFUSCH IST KUNST."),
    (116.40, "sticker", "Moped Nr. 2 · in Arbeit 🔧"),
    (121.36, "banner", "IMMER AUF DEN PUNKT 🎯"),
]
ovs = []
for i, (src, kind, text) in enumerate(OV):
    t, seg = to_out(src)
    assert t is not None, (src, text)
    end = round(seg["start"] + seg["dur"], 3)
    ovs.append({"id": f"ov{i:02d}", "t": t, "end": end, "kind": kind, "text": text})
# Zweites Banner im selben Segment ersetzt das erste nicht: nur "banner" ohne b2 wird vom nächsten "banner" abgelöst
for i, o in enumerate(ovs):
    if o["kind"] == "banner":
        for p in ovs[i + 1:]:
            if p["kind"] == "banner" and p["t"] < o["end"]:
                o["end"] = round(p["t"] - 0.05, 3)
                break

# "big" wird vom nächsten Stempel im selben Segment abgelöst
for i, o in enumerate(ovs):
    if o["kind"] == "big":
        for p in ovs[i + 1:]:
            if p["kind"].startswith("stamp") and p["t"] < o["end"]:
                o["end"] = round(p["t"] - 0.12, 3)
                break

PUNCH = [to_out(x)[0] for x in (29.40, 85.45, 109.48)]
SHAKE = [to_out(x)[0] for x in (0.75, 29.40, 92.42, 109.48, 115.25)]
CUTS = [s["start"] for s in timeline[1:]]
END_CARD = round(DUR - 2.2, 2)

# ---------- HTML ----------
def esc(s):
    return html.escape(s, quote=True)

clips_html = []
for i, s in enumerate(timeline):
    clips_html.append(
        f'      <div class="vwrap" id="w-{s["id"]}"><div class="vpunch"><video id="{s["id"]}" class="clip vid" src="assets/clips/{s["id"]}.mp4" '
        f'data-start="{s["start"]}" data-duration="{s["dur"]}" data-track-index="{1 + i % 2}" data-has-audio="true" playsinline></video></div></div>'
    )

cap_html = []
for i, c in enumerate(caps):
    ws = "".join(f'<span class="cw" id="c{i:03d}w{j}">{esc(w["text"])}</span>' for j, w in enumerate(c["words"]))
    cap_html.append(f'        <div class="cap" id="c{i:03d}">{ws}</div>')

ov_html = []
for o in ovs:
    k = o["kind"]
    if k == "ring":
        ov_html.append(f'      <div class="ov ring" id="{o["id"]}"></div>')
    elif k == "stars":
        ov_html.append(f'      <div class="ov stars" id="{o["id"]}"><span class="s-on">★★★★★</span><span class="s-off">★☆☆☆☆</span></div>')
    else:
        ov_html.append(f'      <div class="ov {k}" id="{o["id"]}"><span>{esc(o["text"])}</span></div>')

sfx = []
def add_sfx(name, t, vol, dur):
    sfx.append(f'      <audio id="sfx-{len(sfx):02d}" src="assets/sfx/{name}.mp3" data-start="{t}" data-duration="{dur}" data-track-index="{30 + len(sfx) % 6}" data-volume="{vol}"></audio>')
for o in ovs:
    k = o["kind"].split()[0]
    if k in ("stamp",):
        add_sfx("impact-bass-1", o["t"], 0.55, 1.5)
    elif k in ("banner", "sticker", "wow"):
        add_sfx("pop", o["t"], 0.25 if k == "wow" else 0.3, 0.7)
    elif k == "big":
        add_sfx("impact-bass-2", o["t"], 0.5, 1.5)
add_sfx("glitch-1", CUTS[0] - 0.05, 0.35, 0.8)
add_sfx("whoosh", to_out(115.0)[0] - 0.1, 0.4, 0.6)

data = json.dumps({"caps": [{"id": f"c{i:03d}", "start": c["start"], "end": c["end"], "words": [w["t"] for w in c["words"]]} for i, c in enumerate(caps)],
                   "ovs": [{"id": o["id"], "t": o["t"], "end": o["end"], "kind": o["kind"]} for o in ovs],
                   "punch": PUNCH, "shake": SHAKE, "cuts": CUTS, "clips": [{"id": s["id"], "start": s["start"], "dur": s["dur"]} for s in timeline],
                   "endCard": END_CARD, "dur": DUR}, ensure_ascii=False)

beat_auto = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
    {"t": 0, "v": 0}, {"t": 1.4, "v": 0}, {"t": 1.6, "v": 0.2}, {"t": to_out(115.0)[0] - 0.2, "v": 0.2},
    {"t": to_out(115.0)[0] + 0.2, "v": 0.7}, {"t": to_out(118.5)[0], "v": 0.7}, {"t": to_out(118.5)[0] + 0.3, "v": 0.22},
    {"t": DUR - 2.2, "v": 0.22}, {"t": DUR - 1.6, "v": 0.5}, {"t": DUR - 0.1, "v": 0}]}]})

tpl = open(os.path.join(ROOT, "scripts", "template.html")).read()
out = (tpl.replace("{{DUR}}", str(DUR))
          .replace("{{CLIPS}}", "\n".join(clips_html))
          .replace("{{CAPS}}", "\n".join(cap_html))
          .replace("{{OVS}}", "\n".join(ov_html))
          .replace("{{SFX}}", "\n".join(sfx))
          .replace("{{BEAT_AUTO}}", esc(beat_auto))
          .replace("{{DATA}}", data))
open(os.path.join(ROOT, "index.html"), "w").write(out)
print("ok", DUR, len(caps), "captions", len(ovs), "overlays", len(sfx), "sfx")
