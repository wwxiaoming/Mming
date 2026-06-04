"""
Mming量化 · AI 配置管理
- 启动时加载 config.json，文件不存在则生成默认模板
- 已存在则不覆盖
- 暴露 load_config / save_config / is_configured 三个工具函数
"""
import json
import os
import threading
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"
_LOCK = threading.Lock()

DEFAULT_CONFIG = {
    "ai": {
        "provider": "deepseek",
        "base_url": "https://api.deepseek.com",
        "api_key": "",
        "model": "deepseek-chat",
    },
    "limits": {
        "rate_per_min": 10,
        "max_prompt_tokens": 8000,
        "max_code_chars": 5000,
    },
    "price_per_million_tokens": {
        "input": 1.0,
        "output": 2.0,
    },
}


def _write_default():
    """生成默认 config.json（不覆盖已存在的）"""
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(
            json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return True
    return False


def load_config() -> dict:
    """加载配置，文件不存在/损坏时回退默认"""
    with _LOCK:
        try:
            if not CONFIG_PATH.exists():
                _write_default()
                return json.loads(json.dumps(DEFAULT_CONFIG))
            text = CONFIG_PATH.read_text(encoding="utf-8")
            data = json.loads(text)
            # 缺字段时补全（向后兼容）
            for k, v in DEFAULT_CONFIG.items():
                if k not in data:
                    data[k] = v
            return data
        except Exception as e:
            print(f"[WARN] config.json 解析失败，回退默认: {e}")
            return json.loads(json.dumps(DEFAULT_CONFIG))


def save_config(new_config: dict) -> bool:
    """保存配置（原子写）"""
    with _LOCK:
        try:
            tmp = CONFIG_PATH.with_suffix(".json.tmp")
            tmp.write_text(
                json.dumps(new_config, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            os.replace(tmp, CONFIG_PATH)
            return True
        except Exception as e:
            print(f"[ERROR] config.json 保存失败: {e}")
            return False


def is_configured(config: dict | None = None) -> bool:
    """检查 API key 是否已配置"""
    cfg = config or load_config()
    key = (cfg.get("ai") or {}).get("api_key") or ""
    return bool(key.strip())


if __name__ == "__main__":
    # 单测：缺文件时自动生成
    import sys
    if "--test" in sys.argv:
        # 测试 1: 删除文件再 load → 应自动生成
        if CONFIG_PATH.exists():
            CONFIG_PATH.unlink()
        assert _write_default() is True, "缺文件时应生成"
        assert CONFIG_PATH.exists(), "文件应存在"
        print("✓ 测试 1 通过：缺 config.json 时自动生成")

        # 测试 2: 已存在时不覆盖
        original = CONFIG_PATH.read_text(encoding="utf-8")
        # 改一下内容
        CONFIG_PATH.write_text('{"custom": true}', encoding="utf-8")
        assert _write_default() is False, "已存在时应跳过"
        assert CONFIG_PATH.read_text(encoding="utf-8") == '{"custom": true}', "不应被覆盖"
        # 还原
        CONFIG_PATH.write_text(original, encoding="utf-8")
        print("✓ 测试 2 通过：已存在时不覆盖")

        # 测试 3: load_config 返回有效 dict
        cfg = load_config()
        assert "ai" in cfg and "provider" in cfg["ai"], "应含 ai.provider"
        assert is_configured(cfg) is False, "空 api_key 应返回 False"
        print("✓ 测试 3 通过：load_config / is_configured 正常")

        print("\n✅ 全部测试通过")
