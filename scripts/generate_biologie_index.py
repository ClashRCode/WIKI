"""Compatibilité: wrapper qui appelle `generate_indexes.py Biologie`.
Ne pas supprimer si vous avez des automatisations qui appellent ce fichier.
"""
from pathlib import Path
import subprocess
import sys

here = Path(__file__).resolve().parents[0]
script = here / 'generate_indexes.py'
if not script.exists():
  print('Script introuvable:', script)
  raise SystemExit(1)

cmd = [sys.executable, str(script), 'Biologie']
res = subprocess.run(cmd)
raise SystemExit(res.returncode)
