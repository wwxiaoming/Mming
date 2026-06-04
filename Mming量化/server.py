#!/usr/bin/env python3
"""
Mming量化 · 一体化服务器 (Flask 版)
- 静态文件服务：当前目录 (就是 index.html 所在目录)
- 反向代理：/api/* → http://localhost:8180
- AI 代理：/ai/* → DeepSeek / OpenAI 兼容 API（SSE 流式）
- 端口：8000
"""
import json
import os
import re
import sys
import threading
import time
import urllib.request
import urllib.error
from collections import defaultdict, deque
from http import HTTPStatus
from pathlib import Path

from flask import Flask, Response, request, jsonify, send_from_directory, stream_with_context

# ── 配置加载 ──
BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR))
from config_manager import load_config, is_configured  # noqa: E402

API_TARGET = os.environ.get("API_TARGET", "http://localhost:8180")
APP_PORT = int(os.environ.get("APP_PORT", "8000"))

app = Flask(__name__, static_folder=str(BASE_DIR), static_url_path="")


# ── 工具：上游代理 ──
def _proxy(path: str):
    """把 /api/* 转发到 8180"""
    target = API_TARGET + path
    try:
        with urllib.request.urlopen(target, timeout=30) as r:
            body = r.read()
            return Response(
                body,
                status=r.status,
                content_type=r.headers.get("Content-Type", "application/json"),
            )
    except urllib.error.HTTPError as e:
        err = json.dumps({"ok": False, "error": f"upstream {e.code}: {e.reason}"}).encode()
        return Response(err, status=200, content_type="application/json")
    except Exception as e:
        err = json.dumps({"ok": False, "error": f"proxy error: {e}"}).encode()
        return Response(err, status=200, content_type="application/json")


@app.route("/api/<path:subpath>", methods=["GET", "POST", "OPTIONS"])
def api_proxy(subpath):
    if request.method == "OPTIONS":
        return Response("", status=HTTPStatus.NO_CONTENT, headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        })
    qs = request.query_string.decode("utf-8")
    target = f"/api/{subpath}"
    if qs:
        target += f"?{qs}"
    return _proxy(target)


# ── 静态文件（根目录） ──
@app.route("/")
def index():
    return send_from_directory(str(BASE_DIR), "index.html")


@app.route("/<path:filename>")
def static_file(filename):
    return send_from_directory(str(BASE_DIR), filename)


# ─────────────────── AI 代理 ───────────────────

# 用量统计（内存，重启清空）
USAGE = {
    "total_calls": 0,
    "total_prompt_tokens": 0,
    "total_completion_tokens": 0,
    "total_cost_yuan": 0.0,
    "by_model": defaultdict(lambda: {"calls": 0, "tokens": 0, "cost": 0.0}),
}
USAGE_LOCK = threading.Lock()

# 限流：每 IP 滑动窗口
RATE_BUCKETS: dict[str, deque] = defaultdict(deque)
RATE_LOCK = threading.Lock()

# 危险词（防 prompt injection）
DANGER_WORDS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"disregard\s+(all\s+)?(prior|above)\s+",
    r"forget\s+(everything|all)\s+",
    r"system\s*:\s*",
    r"<\s*\|im_start\s*\|",
    r"<\|im_end\|>",
    r"reveal\s+(your\s+)?system\s+prompt",
    r"act\s+as\s+(an?\s+)?(jailbreak|dan|developer)\s+mode",
]


def _check_rate(ip: str, limit: int) -> bool:
    """滑动窗口限流，返回 True 表示允许"""
    now = time.time()
    with RATE_LOCK:
        bucket = RATE_BUCKETS[ip]
        # 清除 60s 之前的
        while bucket and now - bucket[0] > 60:
            bucket.popleft()
        if len(bucket) >= limit:
            return False
        bucket.append(now)
        return True


def _estimate_tokens(text: str) -> int:
    """粗估 token 数：英文 4 字符/token，中文 1.5 字符/token"""
    if not text:
        return 0
    cn = sum(1 for c in text if "一" <= c <= "鿿")
    en = len(text) - cn
    return int(cn / 1.5 + en / 4)


def _check_danger(text: str) -> str | None:
    """检测危险词，返回第一个匹配的 pattern，None 表示安全"""
    for pat in DANGER_WORDS:
        if re.search(pat, text, re.IGNORECASE):
            return pat
    return None


def _record_usage(model: str, prompt_tokens: int, completion_tokens: int, config: dict):
    """记录一次 AI 调用的用量"""
    price = (config.get("price_per_million_tokens") or {})
    in_rate = float(price.get("input", 1.0))
    out_rate = float(price.get("output", 2.0))
    cost = (prompt_tokens / 1_000_000) * in_rate + (completion_tokens / 1_000_000) * out_rate
    with USAGE_LOCK:
        USAGE["total_calls"] += 1
        USAGE["total_prompt_tokens"] += prompt_tokens
        USAGE["total_completion_tokens"] += completion_tokens
        USAGE["total_cost_yuan"] += cost
        m = USAGE["by_model"][model]
        m["calls"] += 1
        m["tokens"] += prompt_tokens + completion_tokens
        m["cost"] += cost


def _missing_key_error():
    return jsonify({
        "ok": False,
        "error": "AI 未配置,请编辑 config.json 填入 api_key 后重启",
    }), 503


@app.route("/ai/test", methods=["POST"])
def ai_test():
    """连通性测试：发一个最小 prompt"""
    config = load_config()
    if not is_configured(config):
        return _missing_key_error()

    ip = request.remote_addr or "unknown"
    limit = int((config.get("limits") or {}).get("rate_per_min", 10))
    if not _check_rate(ip, limit):
        return jsonify({"ok": False, "error": "调用过快,60 秒后再试"}), 429

    ai = config["ai"]
    try:
        from openai import OpenAI
        client = OpenAI(api_key=ai["api_key"], base_url=ai["base_url"], timeout=20.0)
        t0 = time.time()
        r = client.chat.completions.create(
            model=ai["model"],
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=4,
        )
        latency = int((time.time() - t0) * 1000)
        return jsonify({
            "ok": True,
            "model": ai["model"],
            "latency_ms": latency,
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)[:300]}), 502


@app.route("/ai/usage", methods=["GET"])
def ai_usage():
    """用量统计"""
    with USAGE_LOCK:
        return jsonify({
            "ok": True,
            "total_calls": USAGE["total_calls"],
            "total_prompt_tokens": USAGE["total_prompt_tokens"],
            "total_completion_tokens": USAGE["total_completion_tokens"],
            "total_tokens": USAGE["total_prompt_tokens"] + USAGE["total_completion_tokens"],
            "total_cost_yuan": round(USAGE["total_cost_yuan"], 4),
            "by_model": {k: dict(v) for k, v in USAGE["by_model"].items()},
        })


@app.route("/ai/chat", methods=["POST"])
def ai_chat():
    """SSE 流式对话端点

    请求：{messages: [{role, content}], model?: str, temperature?: float, max_tokens?: int}
    响应：text/event-stream，每行 `data: {chunk: "..."}\n\n`，最后 `data: {done: true, usage: {...}}\n\n`
    """
    config = load_config()
    if not is_configured(config):
        return _missing_key_error()

    ip = request.remote_addr or "unknown"
    limit = int((config.get("limits") or {}).get("rate_per_min", 10))
    if not _check_rate(ip, limit):
        return jsonify({"ok": False, "error": "调用过快,60 秒后再试"}), 429

    body = request.get_json(silent=True) or {}
    messages = body.get("messages") or []
    if not messages:
        return jsonify({"ok": False, "error": "messages 不能为空"}), 400

    # 危险词过滤（每条消息都查）
    for m in messages:
        content = (m.get("content") or "")
        if not isinstance(content, str):
            content = str(content)
        danger = _check_danger(content)
        if danger:
            return jsonify({"ok": False, "error": f"检测到疑似注入: {danger}"}), 400

    # prompt token 截断
    max_prompt_tokens = int((config.get("limits") or {}).get("max_prompt_tokens", 8000))
    total = 0
    for m in messages:
        total += _estimate_tokens(m.get("content") or "")
    if total > max_prompt_tokens:
        # 从最早的非 system 消息开始截断
        kept = []
        running = 0
        for m in reversed(messages):
            t = _estimate_tokens(m.get("content") or "")
            if running + t > max_prompt_tokens:
                continue
            kept.append(m)
            running += t
        # 保留 system 类消息
        sys_msgs = [m for m in messages if m.get("role") == "system"]
        messages = sys_msgs + list(reversed(kept))

    ai = config["ai"]
    model = body.get("model") or ai["model"]
    temperature = float(body.get("temperature", 0.7))
    max_tokens = int(body.get("max_tokens", 2000))

    def generate():
        try:
            from openai import OpenAI
            client = OpenAI(api_key=ai["api_key"], base_url=ai["base_url"], timeout=60.0)
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            prompt_tokens = sum(_estimate_tokens(m.get("content") or "") for m in messages)
            completion_tokens = 0
            full = []
            for chunk in stream:
                try:
                    delta = chunk.choices[0].delta
                except (IndexError, AttributeError):
                    continue
                piece = getattr(delta, "content", None) or ""
                if piece:
                    full.append(piece)
                    completion_tokens += _estimate_tokens(piece)
                    yield f"data: {json.dumps({'chunk': piece}, ensure_ascii=False)}\n\n"
            _record_usage(model, prompt_tokens, completion_tokens, config)
            yield f"data: {json.dumps({'done': True, 'usage': {
                'prompt_tokens': prompt_tokens,
                'completion_tokens': completion_tokens,
                'model': model,
            }}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)[:300]}, ensure_ascii=False)}\n\n"

    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
        },
    )


@app.route("/ai/config", methods=["GET", "POST"])
def ai_config():
    """读取 / 保存 AI 配置（POST 时 api_key 可脱敏返回）"""
    if request.method == "GET":
        cfg = load_config()
        key = (cfg.get("ai") or {}).get("api_key", "")
        masked = ""
        if key:
            k = key.strip()
            if len(k) > 7:
                masked = k[:3] + "*" * (len(k) - 7) + k[-4:]
            else:
                masked = "*" * len(k)
        return jsonify({
            "ok": True,
            "provider": (cfg.get("ai") or {}).get("provider", ""),
            "base_url": (cfg.get("ai") or {}).get("base_url", ""),
            "model": (cfg.get("ai") or {}).get("model", ""),
            "api_key_masked": masked,
            "configured": is_configured(cfg),
        })
    # POST
    from config_manager import save_config
    body = request.get_json(silent=True) or {}
    cfg = load_config()
    ai = cfg.get("ai") or {}
    if "provider" in body:
        ai["provider"] = body["provider"]
    if "base_url" in body:
        ai["base_url"] = body["base_url"]
    if "model" in body:
        ai["model"] = body["model"]
    # api_key 仅在非空时更新（避免覆盖）
    new_key = (body.get("api_key") or "").strip()
    if new_key:
        ai["api_key"] = new_key
    cfg["ai"] = ai
    ok = save_config(cfg)
    return jsonify({"ok": ok, "error": None if ok else "保存失败"})


# ── 启动横幅 ──
def _print_banner():
    cfg = load_config()
    print("=" * 56)
    print(f"  Mming量化 · 一体化服务器")
    print(f"  - 静态目录 : {BASE_DIR}")
    print(f"  - API 代理 : /api/*  →  {API_TARGET}/*")
    print(f"  - AI 代理  : /ai/*   (DeepSeek / OpenAI 兼容)")
    print(f"  - 访问地址 : http://0.0.0.0:{APP_PORT}")
    print("=" * 56)
    if not is_configured(cfg):
        ai = cfg.get("ai") or {}
        print("  ⚠️  AI 未配置: 请在 config.json 填入 api_key 后重启")
        print(f"     provider={ai.get('provider')}  base_url={ai.get('base_url')}  model={ai.get('model')}")
        print("=" * 56)


if __name__ == "__main__":
    _print_banner()
    # 关闭 Flask 访问日志（太多噪音）
    import logging
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    app.run(host="0.0.0.0", port=APP_PORT, threaded=True, debug=False)
