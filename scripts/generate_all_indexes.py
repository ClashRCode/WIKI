"""
Génère des index JSON pour tous les dossiers de fiches (sauf 'projets').
Usage: python scripts/generate_all_indexes.py
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
FICHES = ROOT / 'fiches_wiki'

EXCLUDE = {'projets'}
EXTS = {'.doc', '.docx'}

def make_index(folder: Path):
    items = [p.name for p in folder.iterdir() if p.suffix.lower() in EXTS and p.is_file()]
    items.sort(key=lambda s: s.lower())
    out = folder / 'index.json'
    out.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Wrote', out)

def main():
    for entry in FICHES.iterdir():
        if not entry.is_dir():
            continue
        if entry.name in EXCLUDE:
            continue
        # create dir if missing
        try:
            make_index(entry)
        except Exception as e:
            print('Failed for', entry, e)

if __name__ == '__main__':
    main()
