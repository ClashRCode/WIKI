import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATEGORY_FILES = [
    ROOT / 'fiches_wiki' / 'biologie.html',
    ROOT / 'fiches_wiki' / 'cryptographie.html',
    ROOT / 'fiches_wiki' / 'histoire.html',
    ROOT / 'fiches_wiki' / 'maths.html',
    ROOT / 'fiches_wiki' / 'personne.html',
    ROOT / 'fiches_wiki' / 'physique.html',
    ROOT / 'fiches_wiki' / 'si.html',
]


class CounterPersistenceRegressionTest(unittest.TestCase):
    def test_all_category_pages_fetch_counts_from_api(self):
        for page in CATEGORY_FILES:
            with self.subTest(page=page.name):
                text = page.read_text(encoding='utf-8')
                self.assertIn("/api/views?file=", text)
                self.assertIn("data-file", text)


if __name__ == '__main__':
    unittest.main()
