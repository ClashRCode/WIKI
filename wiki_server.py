import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)
STORE_FILE = DATA_DIR / 'views.json'


def load_store():
    if not STORE_FILE.exists():
        return {}
    try:
        text = STORE_FILE.read_text(encoding='utf-8')
        if not text.strip():
            return {}
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def save_store(data):
    STORE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


class WikiCounterHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        if self.path.startswith('/api/views'):
            self.handle_views()
            return
        super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/views'):
            self.handle_views()
            return
        self.send_error(404, 'Not found')

    def handle_views(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        file_key = params.get('file', [''])[0].strip()
        if not file_key:
            self.send_json(400, {'error': 'Le paramètre file est requis.'})
            return

        store = load_store()
        count = int(store.get(file_key, 0) or 0)
        increment = params.get('increment', ['0'])[0] not in ('', '0', 'false', 'False')

        if increment or self.command == 'POST':
            count += 1
            store[file_key] = count
            save_store(store)

        self.send_json(200, {'file': file_key, 'count': count})

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    handler = lambda *args, **kwargs: WikiCounterHandler(*args, directory=str(ROOT), **kwargs)
    server = ThreadingHTTPServer(('127.0.0.1', 8000), handler)
    print(f'Serving {ROOT} on http://127.0.0.1:8000')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nStopping server...')
    finally:
        server.server_close()
