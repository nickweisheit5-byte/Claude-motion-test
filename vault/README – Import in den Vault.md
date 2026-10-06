# Import in den Obsidian-Vault

Dieser Ordner ist wie der Vault aufgebaut. Am PC übernehmen:

```bash
git clone https://github.com/nickweisheit5-byte/Claude-motion-test.git   # oder: git pull
```

Dann den Inhalt von `vault/` in den Vault-Stamm kopieren. Ordner zusammenführen und nichts überschreiben, was es schon gibt:
- `Skripte/` → 2 Notizen
- `Analysen/` → Recherche + CSV
- `Ideen/` → YouTube Cross-Video
- `Claude Gedächtnis/Projekte/zweitaktassis.md` → neue Projektnotiz, in `Claude Gedächtnis/00 Übersicht.md` verlinken
- `Claude Gedächtnis/Themen/Claude Cloud – Video-Workflow.md`

Alternativ mit dem Obsidian-Sync-Skript am PC:
`python "D:/Obsidian/obsidian-sync/skills/obsidian-sync/scripts/sync_to_obsidian.py" --project-dir <Pfad zum Repo>/vault --mode copy`
