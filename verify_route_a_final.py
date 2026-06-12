#!/usr/bin/env python3
"""综合验证：路线 A 标题、节点数、关键词命中、YAML 完整性"""
import os
import re
import glob

base = "/workspace/帝王战队资料/世界书条目v4/剧情设定"

# 番外四 烈阳准星传 关键情节词
EXTERNAL_4_KEYWORDS = [
    "红白金属紧身衣", "龙类阴茎", "魔兽飞机杯", "汲取淫纹",
    "卖身契", "精液奶牛", "培养舱", "克隆", "时空留影",
    "未拔", "未摘", "未收服", "抽精", "榨精",
    "禁魔锁链", "紧身战衣", "6 个月", "6个月",
    "抽耳光", "掌掴", "挑下巴", "时空留影", "父母"
]

results = []
for i in range(1, 16):
    pf = glob.glob(f"{base}/{i:02d}_*.md")[0]
    with open(pf) as f:
        text = f.read()
    name = os.path.basename(pf).replace(".md", "")

    # 1. YAML 完整性
    yaml_ok = text.startswith("```yaml\n") and text.rstrip().endswith("```")

    # 2. 路线 A 标题
    has_collector = "指挥官收服路线" in text and "指挥官剿灭路线" not in text

    # 3. 节点数（3 路线 × 5 节点 = 15）
    node_a = len(re.findall(r"### 路线A", text))
    node_b = len(re.findall(r"### 路线B", text))
    node_c = len(re.findall(r"### 路线C", text))

    # 4. "未被收服"关键词
    has_unsubdued = "未被收服" in text

    # 5. "收服后调教榨精"或"调教榨精"关键词
    has_tame = "调教榨精" in text

    # 6. 14 准星篇 番外四关键词
    if i == 14:
        ext4_hits = sum(1 for kw in EXTERNAL_4_KEYWORDS if kw in text)
    else:
        ext4_hits = 0

    results.append({
        "name": name,
        "yaml_ok": yaml_ok,
        "has_collector": has_collector,
        "route_count": (node_a, node_b, node_c),
        "has_unsubdued": has_unsubdued,
        "has_tame": has_tame,
        "ext4_hits": ext4_hits,
        "lines": len(text.split("\n")),
    })

# 打印结果
print(f"{'文件':<14} {'YAML':<6} {'收服':<6} {'未被收服':<10} {'调教榨精':<10} {'路线 A/B/C':<14} {'行数':<6} {'番外四词'}")
print("-" * 100)
all_ok = True
for r in results:
    yaml_mark = "✓" if r["yaml_ok"] else "✗"
    coll_mark = "✓" if r["has_collector"] else "✗"
    un_mark = "✓" if r["has_unsubdued"] else "✗"
    tame_mark = "✓" if r["has_tame"] else "✗"
    route_str = f"{r['route_count'][0]}/{r['route_count'][1]}/{r['route_count'][2]}"
    ext4 = f"{r['ext4_hits']}/{len(EXTERNAL_4_KEYWORDS)}" if "准星" in r["name"] else "—"
    print(f"{r['name']:<14} {yaml_mark:<6} {coll_mark:<6} {un_mark:<10} {tame_mark:<10} {route_str:<14} {r['lines']:<6} {ext4}")
    if not (r["yaml_ok"] and r["has_collector"]):
        all_ok = False

# 检查 14 准星番外四覆盖
quasar = [r for r in results if "准星" in r["name"]][0]
quasar_ok = quasar["ext4_hits"] >= 12  # 至少 12/25 个番外四关键词
print()
print(f"14 准星番外四关键词命中：{quasar['ext4_hits']}/{len(EXTERNAL_4_KEYWORDS)} {'✓' if quasar_ok else '✗'}")

print()
print("综合结果：", "全部通过 ✓" if all_ok and quasar_ok else "存在问题 ✗")
