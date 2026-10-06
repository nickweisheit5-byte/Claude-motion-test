---
tags: [thema, video, claude]
erstellt: 2026-10-06
status: fertig
---
# Claude Cloud – Video-Workflow

Erkenntnisse aus dem ersten Videotag mit Claude Code in der Cloud (06.10.2026).

## So funktioniert es
- **HyperFrames:** Der Connector (HeyGen) darf in Claude Code nicht rendern. Claude baut deshalb lokal mit dem HyperFrames-Framework (`npx hyperframes init/check/snapshot/render`). Videos sind HTML + GSAP und lassen sich editieren.
- **Stimme:** ElevenLabs-Connector, ca. 570 Credits pro 30-s-Take. Transkription mit Scribe ca. 850 Credits pro Minute.
- **Zahlen:** Supermetrics (TikTok, Instagram, YouTube verbunden)
- **Musik:** synthetischer Beat per Python. Besser wäre ElevenLabs Music.
- **SFX:** HyperFrames-Bibliothek (Pixabay-Lizenz)

## Was in der Cloud blockiert ist
- TikTok, Instagram, YouTube, Hugging Face, Microsoft TTS, jsdelivr/unpkg
- **drive.google.com** und **drive.usercontent.google.com:** Große Videos lassen sich erst nach einer Freigabe in den Netzwerk-Einstellungen der Umgebung holen (Custom → Allowed domains).
- Der Obsidian-Vault ist in der Cloud nicht gemountet. Notizen landen im Repo unter `vault/` und werden am PC übernommen.

## Video-Upload
- Bis ca. 30 MB direkt im Chat anhängen
- Größer: in Google Drive und Domains freigeben
- Dateien, die Claude schickt, dürfen höchstens 30 MB groß sein

## Ergebnisse
- [[zweitaktassis – Vorstellungsvideo Skript]]
- [[zweitaktassis – Schweiß-Vlog Schnitt (2026-10-06)]]
