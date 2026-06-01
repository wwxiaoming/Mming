"""v4 世界书条目综合优化脚本 v2
- 修复 v1 的重复插入 bug
- 补全 config 字段(constant/preventRecursion/excludeRecursion/scanDepth/keys)
- 规范化 keys 格式(英文逗号、无空格)
- 修复常见格式问题(XML 嵌套错误)
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

# 加载配置矩阵
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

def process_yaml_block(yaml_text, conf):
    """处理一个 yaml 块 - 只在 content: 之前插入配置"""
    lines = yaml_text.split("\n")
    # 找到 content: | 行
    content_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^\s*content\s*:", line):
            content_idx = i
            break
    if content_idx is None:
        # 旧式 yaml,没有 content 字段 - 添加
        new_conf = make_config_block(conf)
        return new_conf + "\n\n" + yaml_text
    # 删除 content: 之前的所有 position/depth/role/constant/preventRecursion/excludeRecursion/scanDepth 字段
    config_field_pattern = re.compile(r"^\s*(position|depth|role|constant|preventRecursion|excludeRecursion|scanDepth|keys)\s*:")
    pre_content_lines = lines[:content_idx]
    content_and_after = lines[content_idx:]
    # 保留非 config 字段
    kept_pre = [l for l in pre_content_lines if not config_field_pattern.match(l)]
    # 删除前导空行
    while kept_pre and kept_pre[0].strip() == "":
        kept_pre.pop(0)
    # 生成新配置
    new_conf = make_config_block(conf)
    # 组合
    result_lines = [new_conf, ""]  # 配置块 + 空行
    if kept_pre:
        result_lines.extend(kept_pre)
        result_lines.append("")
    result_lines.extend(content_and_after)
    return "\n".join(result_lines)

def fix_keys_in_yaml_block(yaml_text):
    """修复 keys 字段中的中文逗号+空格问题(只处理 content: 之前的部分)"""
    lines = yaml_text.split("\n")
    content_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^\s*content\s*:", line):
            content_idx = i
            break
    if content_idx is None:
        process_range = range(len(lines))
    else:
        process_range = range(content_idx)
    for i in process_range:
        line = lines[i]
        # keys: "问天, 秩序之子, 祖龙" 或 keys: 问天, 秩序之子
        m = re.match(r"^(\s*keys\s*:\s*)(.+)$", line)
        if m:
            prefix = m.group(1)
            value = m.group(2)
            # 移除引号
            if (value.startswith('"') and value.endswith('"')):
                value = value[1:-1]
            elif (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            # 替换中文逗号
            value = value.replace("，", ",")
            # 规范化逗号空格
            value = re.sub(r'\s*,\s*', ',', value)
            value = value.strip()
            lines[i] = f"{prefix}\"{value}\""
    return "\n".join(lines)

def process_file(filepath, conf):
    """处理单个文件"""
    text = filepath.read_text(encoding="utf-8")
    original = text
    issues = 0
    # 1. 找到所有 yaml/xml 代码块
    # 模式: ```yaml ... ``` 或 ```xml\n<yaml>...</yaml> ```
    code_block_pattern = re.compile(
        r"```(yaml|xml)\s*\n(.*?)(?:</yaml>\s*\n)?```",
        re.DOTALL
    )
    # 替换每个块
    new_parts = []
    last_end = 0
    for m in code_block_pattern.finditer(text):
        new_parts.append(text[last_end:m.start()])
        block_type = m.group(1)
        block_content = m.group(2)
        # 提取 ```xml\n<yaml>... 的情况
        if block_type == "xml" and block_content.lstrip().startswith("<yaml>"):
            inner_yaml = block_content.lstrip()[len("<yaml>"):].rstrip()
            if inner_yaml.endswith("</yaml>"):
                inner_yaml = inner_yaml[:-len("</yaml>")].rstrip()
        else:
            inner_yaml = block_content
        # 2. 规范化 keys
        new_inner = fix_keys_in_yaml_block(inner_yaml)
        # 3. 处理 config
        new_inner = process_yaml_block(new_inner, conf)
        if new_inner != inner_yaml:
            issues += 1
        # 重新组装
        if block_type == "xml" and block_content.lstrip().startswith("<yaml>"):
            new_block = f"```xml\n<yaml>\n{new_inner}\n</yaml>\n```"
        else:
            new_block = f"```yaml\n{new_inner}\n```"
        new_parts.append(new_block)
        last_end = m.end()
    new_parts.append(text[last_end:])
    new_text = "".join(new_parts)
    return new_text, issues

# 主循环
print("=" * 60)
print("开始处理 85 个条目 (v2)...")
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
        if issues > 0:
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
