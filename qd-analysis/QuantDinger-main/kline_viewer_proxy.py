"""
K线查看器静态服务器 + API 反向代理

- 直接 serve backend_api_python/app/static/kline_viewer/ 下的静态文件
- 把 /api/* 反向代理到 QuantDinger 后端(默认 http://backend:5000)
- 默认监听 8000 端口

启动:
  python3 kline_viewer_proxy.py
  或
  BACKEND_URL=http://127.0.0.1:5000 PORT=8000 python3 kline_viewer_proxy.py
"""
import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://backend:5000').rstrip('/')
PORT = int(os.environ.get('PORT', '8000'))
STATIC_DIR = Path(__file__).resolve().parent / 'backend_api_python' / 'app' / 'static' / 'kline_viewer'


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, fmt, *args):
        # 简洁日志
        sys.stderr.write(f"[kline-viewer] {self.address_string()} - {fmt % args}\n")

    def end_headers(self):
        # 允许 iPad Safari 跨域(虽然同源但保险)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/api/'):
            self._proxy('GET')
        else:
            # 默认页
            if self.path == '/' or self.path == '':
                self.path = '/index.html'
            return super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self._proxy('POST')
        else:
            self.send_error(405)

    def do_PUT(self):
        if self.path.startswith('/api/'):
            self._proxy('PUT')
        else:
            self.send_error(405)

    def do_DELETE(self):
        if self.path.startswith('/api/'):
            self._proxy('DELETE')
        else:
            self.send_error(405)

    def _proxy(self, method):
        target = BACKEND_URL + self.path
        # 读 body
        body = None
        if method in ('POST', 'PUT', 'DELETE') and 'Content-Length' in self.headers:
            try:
                length = int(self.headers.get('Content-Length', '0'))
                body = self.rfile.read(length) if length > 0 else None
            except Exception:
                body = None

        req = urllib.request.Request(target, data=body, method=method)
        # 透传部分 header(尤其是 Cookie/Authorization)
        for h in ('Cookie', 'Authorization', 'Content-Type', 'Accept', 'User-Agent'):
            v = self.headers.get(h)
            if v:
                req.add_header(h, v)

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
                self.send_response(resp.status)
                # 透传 response header(过滤 hop-by-hop)
                hop_by_hop = {'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization',
                              'te', 'trailers', 'transfer-encoding', 'upgrade', 'content-encoding',
                              'content-length'}
                for k, v in resp.headers.items():
                    if k.lower() in hop_by_hop:
                        continue
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            try:
                data = e.read()
            except Exception:
                data = b'{"code":0,"msg":"upstream error"}'
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            err = json.dumps({"code": 0, "msg": f"proxy error: {e}"}).encode()
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(err)


def main():
    if not STATIC_DIR.exists():
        print(f"ERROR: Static dir not found: {STATIC_DIR}", file=sys.stderr)
        sys.exit(1)
    print(f"K线查看器启动: http://0.0.0.0:{PORT}/")
    print(f"  静态目录: {STATIC_DIR}")
    print(f"  后端代理: {BACKEND_URL}")
    print(f"  打开: http://localhost:{PORT}/")
    httpd = HTTPServer(('0.0.0.0', PORT), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        httpd.shutdown()


if __name__ == '__main__':
    main()
