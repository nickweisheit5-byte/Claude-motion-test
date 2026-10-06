---
tags: [skript, zweitaktassis]
projekt: "[[zweitaktassis]]"
erstellt: 2026-10-06
status: fertig
---
# zweitaktassis – Schweiß-Vlog Schnitt

Projekt: [[zweitaktassis]]
- Anlass: Rohvideo IMG_1013.MOV (2:04, Werkstatt, Rahmen schweißen) als TikTok-Highlight schneiden und animieren
- Vorgaben von Nick: ca. 60 s, Vollbild 9:16, keine Namen einblenden

## Umsetzung
- Projekt: `videos/schweiss-vlog/` (HyperFrames). Video: `renders/schweiss-vlog-tiktok.mp4` (9:16, 59,6 s, -14 LUFS)
- Quelle: komprimierte Version (960×540), Original liegt in Google Drive unter „Test Video“
- Schnitt: 17 Segmente, 59,6 s. Liste in `segments.json`, die Clips baut `scripts/cut-segments.py`
- Bild: Crop 304×540 pro Segment auf die Action gesetzt, hochskaliert auf 1080×1920 (lanczos + Schärfen)
- Untertitel Wort für Wort aus ElevenLabs Scribe (ca. 1.700 Credits für 2 min), aktives Wort gelb
- Einblendungen: „TAKE 1 ❌“, WOW-Sticker, 5 Sterne → 1 Stern bei „scheiße“, „AALGLATT ✨ / SPIEGEL-FINISH“ über der Naht, Ring um Lucas Naht, Stempel „ECHTE PROFIS SCHLEIFEN NICHT.“, „AUF DIE FRESSE 💥“, „PFUSCH IST KUNST.“, Endkarte „@zweitaktassis · Teil 2 kommt“
- Ton: O-Ton +6 dB, leiser Beat darunter (lauter bei der Simson-B-Roll), Pops und Impacts bei den Gags

## Schnittliste (Original → Inhalt)
| Original | Inhalt |
|---|---|
| 0:00 | Versprecher „Es geht noch nicht los“ (Cold Open) |
| 0:03 | „Freunde des gepflegten Zweitakt-Motorrennsports … wow“ |
| 0:10 | Moped Nr. 2 / Nr. 3 |
| 0:22 | Rahmen in Bearbeitung |
| 0:26 | Fülldraht-Schweißgerät, „was absolut scheiße geht“ |
| 0:36 (Bild 0:59) | „Schweißnähte aalglatt …“ über Naht-Nahaufnahme |
| 0:50 | Verstärkungsbleche |
| 1:16 | „Wie bei Luca. Nur besser.“ |
| 1:22–1:33 | Lucas Rahmen, „Oh oh“, nicht abgeschliffen |
| 1:34–1:45 | „Wer braucht das schon“, „Echte Profis schweißen ohne abzuschleifen“ |
| 1:46–1:55 | „… zweimal die Woche auf die Fresse …“, Motto |
| 1:55 | B-Roll rote Cross-Simson |
| 2:00 | „Wir müssen immer auf den Punkt“ + Endkarte |

## Nächste Version
- Mit dem 1080p- oder 4K-Original würde das Bild deutlich schärfer (Netzwerk-Freigabe für drive.google.com nötig)
