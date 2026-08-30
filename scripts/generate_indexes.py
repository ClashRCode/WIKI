#!/usr/bin/env python3
"""
generate_indexes.py

Parcourt `fiches_wiki/` et génère un `index.json` pour chaque sous-dossier.

Format produit (liste d'objets):
[
  {"filename": "Mon doc.docx", "title": "Mon doc", "path": "Biologie/Mon doc.docx", "mtime": "2026-08-30T12:34:56", "size": 12345},
  ...
]

Ce script utilise uniquement la bibliothèque standard pour rester compatible
avec GitHub Actions sans dépendances supplémentaires.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]  # c:/.../WIKI
TARGET_DIR = ROOT / 'fiches_wiki'

EXTS = {'.docx', '.doc', '.pdf', '.odt', '.txt'}


def clean_title(name: str) -> str:
    # Retire préfixes entre crochets comme [BIO] et nettoie l'extension
    base = name
    if base.startswith('[') and ']' in base:
        base = base.split(']', 1)[1].strip()
    # retire extension
    base = os.path.splitext(base)[0]
    return base


def generate_for_folder(folder: Path):
    items = []
    for p in sorted(folder.iterdir()):
        if p.is_file() and p.suffix.lower() in EXTS:
            stat = p.stat()
            rel = p.relative_to(TARGET_DIR).as_posix()
            items.append({
                'filename': p.name,
                'title': clean_title(p.name),
                'path': rel,
                'mtime': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'size': stat.st_size,
            })

    out = folder / 'index.json'
    tmp = out.with_suffix('.json.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    tmp.replace(out)
    print(f'Wrote {out} ({len(items)} items)')


def main():
    if not TARGET_DIR.exists():
        print('Target directory not found:', TARGET_DIR)
        return

    # Parcourir dossiers directs dans fiches_wiki
    for entry in sorted(TARGET_DIR.iterdir()):
        if entry.is_dir():
            print('Processing', entry.name)
            generate_for_folder(entry)


if __name__ == '__main__':
    main()
