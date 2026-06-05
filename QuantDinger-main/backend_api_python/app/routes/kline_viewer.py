"""
K 线查看器 — 静态 HTML 单页应用.

通过 Flask 蓝图在以下路径提供:
  GET  /kline-viewer/         → 单页 HTML
  GET  /kline-viewer/<path>   → 静态文件(若有)

HTML 文件位于:
  backend_api_python/app/static/kline_viewer/index.html

环境开关:
  KLINE_VIEWER_ENABLED=true|false
"""
from __future__ import annotations

import os
from pathlib import Path

from flask import abort, jsonify, send_from_directory

from app.openapi.blueprint import HumanBlueprint as Blueprint
from app.utils.logger import get_logger

logger = get_logger(__name__)

kline_viewer_blp = Blueprint(
    "kline-viewer",
    __name__,
    description="多市场 K 线查看器(A 股/港股/美股/加密/外汇/期货)",
)

_STATIC_DIR = Path(__file__).resolve().parent.parent / "static" / "kline_viewer"


def _is_enabled() -> bool:
    return os.environ.get("KLINE_VIEWER_ENABLED", "true").strip().lower() in (
        "1", "true", "yes", "on",
    )


@kline_viewer_blp.route("/kline-viewer/", methods=["GET"])
@kline_viewer_blp.route("/kline-viewer", methods=["GET"])
def kline_viewer_index():
    if not _is_enabled():
        return jsonify({
            "code": 0,
            "msg": "K 线查看器未启用(设置 KLINE_VIEWER_ENABLED=true)",
            "data": None,
        }), 404
    index_file = _STATIC_DIR / "index.html"
    if not index_file.exists():
        logger.error("K线查看器静态文件不存在: %s", index_file)
        return jsonify({
            "code": 0,
            "msg": f"K线查看器静态文件不存在: {index_file}",
            "data": None,
        }), 500
    return send_from_directory(_STATIC_DIR, "index.html")


@kline_viewer_blp.route("/kline-viewer/<path:filename>", methods=["GET"])
def kline_viewer_static(filename: str):
    if not _is_enabled():
        abort(404)
    # 安全检查:不允许跳出 kline_viewer 目录
    target = (_STATIC_DIR / filename).resolve()
    if not str(target).startswith(str(_STATIC_DIR.resolve())):
        abort(404)
    if not target.exists():
        abort(404)
    return send_from_directory(_STATIC_DIR, filename)
