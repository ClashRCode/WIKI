#!/usr/bin/env python3
"""
Génère fiches_wiki/Maths/index.json
Usage: python scripts/generate_maths_index.py
"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'fiches_wiki' / 'Maths'
if not root.exists():
    print('Dossier introuvable:', root)
    raise SystemExit(1)

files = sorted([p.name for p in root.iterdir() if p.suffix.lower() in ('.doc', '.docx')])
out = root / 'index.json'
with out.open('w', encoding='utf-8') as f:
    json.dump(files, f, ensure_ascii=False, indent=2)
print('Wrote', out)
