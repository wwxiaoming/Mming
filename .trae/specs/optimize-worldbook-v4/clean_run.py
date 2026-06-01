"""一次性清理脚本 - 去除所有累积的重复 config 块,只保留一个"""
import re
from pathlib import Path
import importlib.util

base = Path("/workspace")
v4 = base / "帝王战队资料/世界书条目v4"

# 加载配置矩阵
spec = importlib.util.spec_from_file_location("matrix_mod", base / ".trae/specs/optimize-worldbook-v4/build_matrix.py")
matrix_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matrix_mod)
matrix = matrix_mod.matrix

def make_config_block(conf):
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

def clean_yaml_block(yaml_text, conf):
    """去除所有 config 字段,只保留一个干净版本"""
    lines = yaml_text.split("\n")
    # 找到 content: | 行
    content_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^\s*content\s*:", line):
            content_idx = i
            break
    # 标记所有要删除的 config 字段
    config_field_pattern = re.compile(r"^\s*(position|depth|role|constant|preventRecursion|excludeRecursion|scanDepth|keys)\s*:")
    # 删除所有匹配的 config 字段行(无论有没有 content: |)
    kept_lines = [l for l in lines if not config_field_pattern.match(l)]
    # 清理连续空行
    result = []
    prev_empty = False
    for l in kept_lines:
        is_empty = (l.strip() == "")
        if is_empty and prev_empty:
            continue
        result.append(l)
        prev_empty = is_empty
    # 清理首尾空行
    while result and result[0].strip() == "":
        result.pop(0)
    while result and result[-1].strip() == "":
        result.pop()
    # 生成新配置
    new_conf = make_config_block(conf)
    return new_conf + "\n\n" + "\n".join(result)

def fix_keys_in_yaml_block(yaml_text):
    """规范化 keys 字段"""
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
        m = re.match(r"^(\s*keys\s*:\s*)(.+)$", line)
        if m:
            prefix = m.group(1)
            value = m.group(2)
            if (value.startswith('"') and value.endswith('"')):
                value = value[1:-1]
            elif (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            value = value.replace("，", ",")
            value = re.sub(r'\s*,\s*', ',', value)
            value = value.strip()
            lines[i] = f"{prefix}\"{value}\""
    return "\n".join(lines)

def process_file(filepath, conf):
    text = filepath.read_text(encoding="utf-8")
    original = text
    issues = 0
    code_block_pattern = re.compile(
        r"```(yaml|xml)\s*\n(.*?)(?:</yaml>\s*\n)?```",
        re.DOTALL
    )
    new_parts = []
    last_end = 0
    for m in code_block_pattern.finditer(text):
        new_parts.append(text[last_end:m.start()])
        block_type = m.group(1)
        block_content = m.group(2)
        if block_type == "xml" and block_content.lstrip().startswith("<yaml>"):
            inner_yaml = block_content.lstrip()[len("<yaml>"):].rstrip()
            if inner_yaml.endswith("</yaml>"):
                inner_yaml = inner_yaml[:-len("</yaml>")].rstrip()
        else:
            inner_yaml = block_content
        new_inner = fix_keys_in_yaml_block(inner_yaml)
        new_inner = clean_yaml_block(new_inner, conf)
        if new_inner != inner_yaml:
            issues += 1
        if block_type == "xml" and block_content.lstrip().startswith("<yaml>"):
            new_block = f"```xml\n<yaml>\n{new_inner}\n</yaml>\n```"
        else:
            new_block = f"```yaml\n{new_inner}\n```"
        new_parts.append(new_block)
        last_end = m.end()
    new_parts.append(text[last_end:])
    new_text = "".join(new_parts)
    return new_text, issues

stats = {"files_processed": 0, "issues_fixed": 0}
for entry_key, conf in matrix.items():
    category, fname = entry_key.split("/", 1)
    filepath = v4 / category / fname
    if not filepath.exists():
        continue
    new_text, issues = process_file(filepath, conf)
    if new_text != filepath.read_text(encoding="utf-8"):
        filepath.write_text(new_text, encoding="utf-8")
        stats["files_processed"] += 1
        stats["issues_fixed"] += issues
        if issues > 0:
            print(f"  ✓ {entry_key} ({issues} 处修改)")

print()
print(f"完成:处理 {stats['files_processed']} 个文件,修复 {stats['issues_fixed']} 处问题")
