#!/usr/bin/env python3
"""
小宇量化工具 · 一体化服务器
- 静态文件服务:当前目录(就是 index.html 所在目录)
- 反向代理:/api/* → http://localhost:8180(避免 Codespaces 跨域)
- 端口:8000
"""
import http.server
import socketserver
import urllib.request
import urllib.error
import json
import os
import sys
from http import HTTPStatus

PORT = 8000
API_TARGET = "http://localhost:8180"

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 允许任意来源(本地工具,够用)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/"):
            self._proxy()
            return
        return super().do_GET()

    def _proxy(self):
        target = API_TARGET + self.path
        try:
            with urllib.request.urlopen(target, timeout=30) as r:
                body = r.read()
                self.send_response(r.status)
                self.send_header("Content-Type", r.headers.get("Content-Type", "application/json"))
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except urllib.error.HTTPError as e:
            err_body = json.dumps({"ok": False, "error": f"upstream {e.code}: {e.reason}"}).encode()
            self.send_response(200)  # 给前端统一 ok:false 结构
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(err_body)))
            self.end_headers()
            self.wfile.write(err_body)
        except Exception as e:
            err_body = json.dumps({"ok": False, "error": f"proxy error: {e}"}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(err_body)))
            self.end_headers()
            self.wfile.write(err_body)

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), fmt % args))

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"服务启动: http://0.0.0.0:{PORT}")
    print(f"静态目录: {os.getcwd()}")
    print(f"API 代理: /api/*  →  {API_TARGET}/*")
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        httpd.serve_forever()
