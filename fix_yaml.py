#!/usr/bin/env python3
"""修复世界书条目v4的所有 Markdown 文件，恢复正确的 YAML 格式。"""
import os
import re

BASE = "/workspace/帝王战队资料/世界书条目v4"

def parse_keys_block(content):
    m = re.search(r'(?:keys|secondary_keys)\s*[:=]\s*\[?([^\n\]]+)', content)
    if not m:
        return []
    line = m.group(1)
    keys = re.findall(r'[\u4e00-\u9fa5\w]+', line)
    return [k for k in keys if k and not k.isdigit()]

def get_yaml_block(content):
    m = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
    if m:
        return m.group(1)
    m = re.search(r'<yaml>\n(.*?)\n</yaml>', content, re.DOTALL)
    if m:
        return m.group(1)
    return None

def fix_hero_file(content, filepath):
    fname = os.path.basename(filepath)
    expected_key = re.sub(r'^\d+_', '', fname).replace('.md', '').replace(' ', '')

    keys = parse_keys_block(content)
    if not keys:
        keys = [expected_key, '英雄', '调教', '容器']

    yaml_text = get_yaml_block(content)
    if yaml_text:
        m = re.search(r'(##\s+[^\n]+.*)', yaml_text, re.DOTALL)
        content_block = m.group(1) if m else yaml_text
    else:
        m = re.search(r'(##\s+[^\n]+.*)', content, re.DOTALL)
        content_block = m.group(1) if m else content

    keys_yaml = ', '.join(f'"{k}"' for k in keys[:6])
    if not keys_yaml:
        keys_yaml = f'"{expected_key}"'

    # 检查 content_block 是否需要前置缩进（content: | 后面每行都需要缩进）
    lines = content_block.rstrip().split('\n')
    indented = '\n'.join(('  ' + l if l else l) for l in lines)

    new_yaml = f'```yaml\nkey: "{expected_key}"\nsecondary_keys: [{keys_yaml}]\nenabled: true\nposition: 1\norder: 50\ncontent: |\n{indented}\n```\n'
    return new_yaml

def fix_xml_wrapped_file(content, filepath):
    yaml_text = get_yaml_block(content)
    if yaml_text and 'content: |' in yaml_text and 'key:' in yaml_text:
        new_content = '```yaml\n' + yaml_text.rstrip() + '\n```\n'
        return new_content
    return content

def fix_worldview_file(content, filepath):
    yaml_text = get_yaml_block(content)
    if yaml_text and 'content: |' in yaml_text and 'key:' in yaml_text:
        new_content = '```yaml\n' + yaml_text.rstrip() + '\n```\n'
        return new_content
    return content

def fix_plot_file(content, filepath):
    if content.startswith('# '):
        m = re.search(r'(```yaml\n.*?\n```)', content, re.DOTALL)
        if m:
            return m.group(1) + '\n'
    return content

def fix_device_file(content, filepath):
    if not content.startswith('```yaml'):
        m = re.search(r'(```yaml\n.*?\n```)', content, re.DOTALL)
        if m:
            return m.group(1) + '\n'
    return content

def main():
    fixed = {'hero': 0, 'xml_wrapped': 0, 'worldview': 0, 'plot': 0, 'device': 0, 'kept': 0}

    for root, dirs, files in os.walk(BASE):
        for f in files:
            if not f.endswith('.md'):
                continue
            filepath = os.path.join(root, f)
            with open(filepath) as fp:
                content = fp.read()

            original = content
            subdir = os.path.basename(root)

            if subdir == '英雄设定':
                new_content = fix_hero_file(content, filepath)
                kind = 'hero'
            elif subdir == '世界观':
                new_content = fix_worldview_file(content, filepath)
                kind = 'worldview'
            elif subdir in ['系统规则', '道具设定', 'NPC设定', '地区设定', '阵营', '组织势力']:
                new_content = fix_xml_wrapped_file(content, filepath)
                kind = 'xml_wrapped'
            elif subdir == '剧情设定':
                new_content = fix_plot_file(content, filepath)
                kind = 'plot'
            elif subdir == '专属装置':
                new_content = fix_device_file(content, filepath)
                kind = 'device'
            else:
                new_content = content
                kind = 'kept'

            if new_content != original:
                with open(filepath, 'w') as fp:
                    fp.write(new_content)
                fixed[kind] += 1

    print("=== 修复完成 ===")
    for k, v in fixed.items():
        print(f"  {k}: {v}")

if __name__ == '__main__':
    main()
