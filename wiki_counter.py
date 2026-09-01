import json
from pathlib import Path


class CounterStore:
    def __init__(self, data_dir=None):
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).resolve().parent / 'data'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / 'views.json'
        self._data = self._load()

    def _load(self):
        if not self.file_path.exists():
            return {}
        try:
            raw = self.file_path.read_text(encoding='utf-8')
            if not raw.strip():
                return {}
            data = json.loads(raw)
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {}

    def increment(self, file_key):
        key = str(file_key)
        current = int(self._data.get(key, 0) or 0)
        next_value = current + 1
        self._data[key] = next_value
        self._save()
        return next_value

    def get(self, file_key):
        return int(self._data.get(str(file_key), 0) or 0)

    def _save(self):
        self.file_path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Counter store for wiki page views')
    parser.add_argument('--file', dest='file_key', required=True)
    parser.add_argument('--get', action='store_true')
    args = parser.parse_args()

    store = CounterStore()
    if args.get:
        print(store.get(args.file_key))
    else:
        print(store.increment(args.file_key))
