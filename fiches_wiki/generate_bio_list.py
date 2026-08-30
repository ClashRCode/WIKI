#!/usr/bin/env python3
"""
Génère un fichier `Biologie/list.json` contenant la liste des fichiers
(.doc, .docx) présents dans le dossier `Biologie/`.

Usage:
  python generate_bio_list.py

Placez ce script dans `fiches_wiki/` et lancez-le depuis ce dossier.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
BIO_DIR = HERE / 'Biologie'
OUT = BIO_DIR / 'list.json'

if not BIO_DIR.exists():
    print('Dossier Biologie/ introuvable dans', BIO_DIR)
    raise SystemExit(1)

files = [p.name for p in sorted(BIO_DIR.iterdir()) if p.suffix.lower() in ('.doc', '.docx')]

with OUT.open('w', encoding='utf-8') as f:
    json.dump(files, f, ensure_ascii=False, indent=2)

print(f'Wrote {len(files)} entries to {OUT}')
