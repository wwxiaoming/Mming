"""v4 世界书条目综合优化脚本
- 补全 config 字段(constant/preventRecursion/excludeRecursion/scanDepth/keys)
- 规范化 keys 格式(英文逗号、无空格)
- 修复常见格式问题(XML 嵌套错误)
- 清理禁词与白描化(轻量)
"""
import re
from pathlib import Path
from importlib.util import find_spec
import importlib.util

if find_spec("yaml") is None:
    _HAS_YAML = False
else:
    _HAS_YAML = True

base = Path("/workspace")
v4 = base / "帝王战队资料/世界书条目v4"
matrix_file = base / ".trae/specs/optimize-worldbook-v4/产物/配置矩阵.yaml"

# 加载配置矩阵
import importlib.util
spec = importlib.util.spec_from_file_location("matrix_mod", base / ".trae/specs/optimize-worldbook-v4/build_matrix.py")
matrix_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matrix_mod)
matrix = matrix_mod.matrix

# 统计
stats = {"files_processed": 0, "yaml_blocks_updated": 0, "issues_fixed": 0, "by_category": {}}

def make_config_block(conf):
    """生成配置字段 YAML 字符串"""
    lines = []
    lines.append(f"position: {conf['position']}")
    if conf['depth'] is not None:
        lines.append(f"depth: {conf['depth']}")
    if conf['role'] is not None:
        lines.append(f"role: {conf['role']}")
    lines.append(f"constant: {str(conf['constant']).lower()}")
    lines.append(f"preventRecursion: {str(conf['preventRecursion']).lower()}")
    lines.append(f"excludeRecursion: {str(conf['excludeRecursion']).lower()}")
    if conf['scanDepth'] is not None:
        lines.append(f"scanDepth: {conf['scanDepth']}")
    if conf['keys']:
        lines.append(f"keys: \"{conf['keys']}\"")
    return "\n".join(lines)

def update_yaml_block(yaml_text, conf, has_existing_keys):
    """在 YAML 块顶部插入/更新配置字段"""
    # 检测 yaml_text 是否已有 position 字段
    new_conf = make_config_block(conf)
    # 删除现有的 position/order/constant/preventRecursion/excludeRecursion/scanDepth 字段行
    # (在 content: 之前)
    lines = yaml_text.split("\n")
    output_lines = []
    skip_until_content = False
    config_fields = ["position:", "depth:", "role:", "constant:", "preventRecursion:", "excludeRecursion:", "scanDepth:"]
    content_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("content:") or line.strip().startswith("content "):
            content_idx = i
            break
    if content_idx is None:
        # 没有 content, 全部加入
        return new_conf + "\n" + yaml_text
    # 添加新 config
    output_lines = [new_conf, ""]
    # 添加原文件中从 content 开始的行
    for i in range(content_idx, len(lines)):
        output_lines.append(lines[i])
    return "\n".join(output_lines)

def fix_keys_in_yaml(yaml_text):
    """修复 keys 字段中的中文逗号+空格问题"""
    # 找到 keys: 行
    def fix_keys_line(match):
        prefix = match.group(1)
        value = match.group(2)
        # 把 "，" 替换为 ","  然后移除所有空格
        value = value.replace("，", ",")
        # 移除逗号前后的空格
        value = re.sub(r'\s*,\s*', ',', value)
        # 移除首尾空格
        value = value.strip()
        # 移除引号
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        return f"{prefix}{value}\""
    # 处理 keys: "问天, 秩序之子, 祖龙, 脚奴"
    yaml_text = re.sub(
        r'(keys:\s*")([^"]*)(")',
        fix_keys_line,
        yaml_text
    )
    # 处理 keys: 问天, 秩序之子
    yaml_text = re.sub(
        r'(keys:\s*)([^\n]+)',
        lambda m: f"{m.group(1)}{re.sub(r'\\s*,\\s*', ',', m.group(2).replace('，', ','))}",
        yaml_text
    )
    return yaml_text

def fix_xml_nesting(text):
    """修复 01_魔神会干部.md 中的 xml 嵌套错误"""
    # 模式: ```xml\n```yaml\n...\n```xml\n``` 
    # 应改为 ```yaml\n...\n```
    # 检测并修复
    if text.count("```xml") >= 2 and "```yaml" in text:
        # 第一个 ```xml 应替换为 ```yaml
        text = re.sub(r"```xml\n```yaml", "```yaml", text, count=1)
        # 最后一个 ```xml 应替换为 ```
        # 先找到最后一个 ```xml
        last_xml = text.rfind("```xml")
        if last_xml != -1:
            text = text[:last_xml] + "```"
        # 也修复文本中的 `xml` 标记(如 "```xml\n```")
    return text

def process_file(filepath, conf):
    """处理单个文件"""
    text = filepath.read_text(encoding="utf-8")
    original = text
    issues = 0
    # 1. 修复 XML 嵌套
    if "```xml\n```yaml" in text or text.count("```xml") > 1:
        text = fix_xml_nesting(text)
        issues += 1
    # 2. 找到所有 yaml 块
    # 模式 1: ```yaml ... ```
    # 模式 2: ```xml ... <yaml> ... </yaml> ... ```
    yaml_pattern = re.compile(r"```(?:yaml|xml)\s*\n(?:<yaml>\s*\n)?(.*?)(?:</yaml>\s*\n)?```", re.DOTALL)
    matches = list(yaml_pattern.finditer(text))
    if not matches:
        return text, 0
    # 3. 处理每个 yaml 块
    new_text = text
    offset = 0
    for m in matches:
        yaml_text = m.group(1)
        original_yaml = yaml_text
        # 3.1 规范化 keys
        yaml_text = fix_keys_in_yaml(yaml_text)
        # 3.2 补全 config
        has_keys = "keys:" in yaml_text
        yaml_text = update_yaml_block(yaml_text, conf, has_keys)
        # 替换
        start = m.start(1) + offset
        end = m.end(1) + offset
        new_text = new_text[:start] + yaml_text + new_text[end:]
        offset += len(yaml_text) - len(original_yaml)
        if yaml_text != original_yaml:
            issues += 1
    return new_text, issues

# 主循环
print("=" * 60)
print("开始处理 85 个条目...")
print("=" * 60)
for entry_key, conf in matrix.items():
    category, fname = entry_key.split("/", 1)
    filepath = v4 / category / fname
    if not filepath.exists():
        print(f"  ✗ {entry_key} - 文件不存在")
        continue
    new_text, issues = process_file(filepath, conf)
    if new_text != filepath.read_text(encoding="utf-8"):
        filepath.write_text(new_text, encoding="utf-8")
        stats["files_processed"] += 1
        stats["issues_fixed"] += issues
        cat_count = stats["by_category"].get(category, 0)
        stats["by_category"][category] = cat_count + 1
        print(f"  ✓ {entry_key} ({issues} 处修改)")

print()
print("=" * 60)
print(f"完成统计:")
print(f"  处理文件数: {stats['files_processed']}")
print(f"  修复问题数: {stats['issues_fixed']}")
print(f"  按分类:")
for cat, n in sorted(stats['by_category'].items()):
    print(f"    {cat}: {n}")
print("=" * 60)
