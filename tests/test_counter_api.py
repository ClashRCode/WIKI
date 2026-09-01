import json
import shutil
import tempfile
import unittest
from pathlib import Path

from wiki_counter import CounterStore


class CounterStoreTests(unittest.TestCase):
    def test_increment_persists_to_disk(self):
        temp_dir = Path(tempfile.mkdtemp())
        try:
            store = CounterStore(data_dir=temp_dir)
            self.assertEqual(store.increment('Biologie/fiche.docx'), 1)
            self.assertEqual(store.increment('Biologie/fiche.docx'), 2)

            saved = json.loads((temp_dir / 'views.json').read_text(encoding='utf-8'))
            self.assertEqual(saved['Biologie/fiche.docx'], 2)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
