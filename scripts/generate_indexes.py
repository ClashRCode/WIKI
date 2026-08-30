#!/usr/bin/env python3
"""
Génère un `index.json` pour les sous-dossiers de `fiches_wiki/` contenant des fichiers .doc/.docx.

Usage:
  # générer tous les index
  python scripts/generate_indexes.py

  # générer pour une catégorie spécifique
  python scripts/generate_indexes.py Biologie

  # générer pour plusieurs catégories
  python scripts/generate_indexes.py Biologie Maths Physique
"""
import argparse
import json
from pathlib import Path
from typing import Iterable


def collect_docs(directory: Path) -> list[str]:
    return sorted([p.name for p in directory.iterdir() if p.suffix.lower() in ('.doc', '.docx')])


def write_index(directory: Path, files: Iterable[str]) -> None:
    out = directory / 'index.json'
    with out.open('w', encoding='utf-8') as f:
        json.dump(list(files), f, ensure_ascii=False, indent=2)
    print('Wrote', out)


def generate(root: Path, categories: list[str] | None = None) -> None:
    if not root.exists():
        print('Dossier introuvable:', root)
        raise SystemExit(1)

    if categories:
        for name in categories:
            d = root / name
            if not d.exists() or not d.is_dir():
                print('Skip (not found):', d)
                continue
            files = collect_docs(d)
            if files:
                write_index(d, files)
            else:
                print('No .doc/.docx in', d)
    else:
        for d in sorted(root.iterdir()):
            if d.is_dir():
                files = collect_docs(d)
                if files:
                    write_index(d, files)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description='Generate index.json for fiches_wiki categories')
    p.add_argument('categories', nargs='*', help='Optional category names to generate (default: all)')
    args = p.parse_args(argv)

    root = Path(__file__).resolve().parents[1] / 'fiches_wiki'
    generate(root, args.categories if args.categories else None)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
