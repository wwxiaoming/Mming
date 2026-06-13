"""综合验证脚本：世界观重构 + 天火移至英雄设定"""
import os
import re
import yaml

ROOT = "/workspace/解压我的世界书文档 5/帝王战队资料/世界书条目v4"
WORLD_DIR = f"{ROOT}/世界观"
HERO_DIR = f"{ROOT}/英雄设定"

print("=" * 60)
print("世界观重构 + 天火移至英雄设定 · 综合验证")
print("=" * 60)

# 1. 世界观/ 下仅剩 3 个文件
world_files = sorted([f for f in os.listdir(WORLD_DIR) if f.endswith(".md")])
print(f"\n[1] 世界观/ 文件列表: {world_files}")
assert world_files == ["00_世界观总纲.md", "01_帝王战队.md", "02_神魔号系统.md"], f"Expected 3 files, got {len(world_files)}"
print("    PASS: 仅剩 3 个文件")

# 2. 英雄设定/00_天火.md 存在且 YAML 解析
tianhuo_path = os.path.join(HERO_DIR, "00_天火.md")
assert os.path.exists(tianhuo_path)
with open(tianhuo_path) as f:
    tianhuo_content = f.read()
m = re.match(r"^```yaml\n(.*?)\n```", tianhuo_content, re.DOTALL)
assert m
d = yaml.safe_load(m.group(1))
assert d["key"] == "天火"
assert d["order"] == 0
assert d["position"] == 1
assert len(d["secondary_keys"]) >= 7
print(f"\n[2] 00_天火.md YAML 解析:")
print(f"    key={d['key']} | position={d['position']} | order={d['order']}")
print(f"    secondary_keys ({len(d['secondary_keys'])}): {d['secondary_keys']}")
print("    PASS")

# 3. 禁词扫描
forbidden = [
    "一丝","一缕","一抹","不易察觉","不易觉察","难以察觉",
    "弧度","弯起嘴角","翘起嘴角","喉结","纽扣","指节发白",
    "石子","湖面","涟漪","拉满的弓","琴弦","闪电","晨光",
    "似乎","几乎","仿佛","如同","宛如","好像",
    "极度","万分","无比","深深的","——",
]
print("\n[3] 禁词扫描:")
all_ok = True
for fname in ["00_世界观总纲.md","01_帝王战队.md","02_神魔号系统.md"]:
    p = os.path.join(WORLD_DIR, fname)
    with open(p) as fp:
        c = fp.read()
    hits = [w for w in forbidden if w in c]
    status = "PASS 0 命中" if not hits else f"FAIL 命中 {hits}"
    if hits: all_ok = False
    print(f"    世界观/{fname}: {status}")
p = os.path.join(HERO_DIR, "00_天火.md")
with open(p) as fp:
    c = fp.read()
hits = [w for w in forbidden if w in c]
status = "PASS 0 命中" if not hits else f"FAIL 命中 {hits}"
if hits: all_ok = False
print(f"    英雄设定/00_天火.md: {status}")

# 4. 00_世界观 含 7 个 XML 段标签
with open(os.path.join(WORLD_DIR, "00_世界观总纲.md")) as f:
    wc = f.read()
xml_tags = re.findall(r"^<([^>]+)>", wc, re.MULTILINE)
print(f"\n[4] 00_世界观 XML 段标签: {xml_tags}")
print(f"    总计: {len(xml_tags)} (要求 >= 6, 目标 7)")
assert len(xml_tags) >= 6
print("    PASS")

# 5. 行数检查
print("\n[5] 行数检查:")
for fname, (lo, hi, base) in [
    ("00_世界观总纲.md", (100, 140, WORLD_DIR)),
    ("01_帝王战队.md", (50, 80, WORLD_DIR)),
    ("02_神魔号系统.md", (50, 80, WORLD_DIR)),
    ("00_天火.md", (60, 90, HERO_DIR)),
]:
    p = os.path.join(base, fname)
    with open(p) as fp:
        n = len(fp.readlines())
    ok = lo <= n <= hi
    print(f"    {fname}: {n} 行 (要求 {lo}~{hi}) {'PASS' if ok else 'FAIL'}")

# 6. 4 个引用文件无悬空引用
print("\n[6] 跨文件引用悬空检查:")
for p in [
    f"{ROOT}/剧情设定/003_路线C_已收服8位.md",
    f"{ROOT}/地区设定/04_秘境遗迹.md",
    f"{ROOT}/地区设定/09_龙渊秘境.md",
    f"{ROOT}/地区设定/10_魔神会化妆舞会场.md",
]:
    with open(p) as f:
        c = f.read()
    bad = []
    if "03_宇宙之子与容器理论" in c: bad.append("03_宇宙之子与容器理论")
    if "04_死寂沙漠与蒲罗树" in c: bad.append("04_死寂沙漠与蒲罗树")
    if "05_天火.md" in c: bad.append("05_天火.md")
    status = "PASS 无悬空" if not bad else f"FAIL 悬空: {bad}"
    print(f"    {os.path.basename(p)}: {status}")

# 7. 4 个被删文件不存在
print("\n[7] 被删文件状态:")
for p in [
    f"{WORLD_DIR}/03_宇宙之子与容器理论.md",
    f"{WORLD_DIR}/04_死寂沙漠与蒲罗树.md",
    f"{WORLD_DIR}/05_天火.md",
    f"{WORLD_DIR}/天火设定.txt",
]:
    status = "FAIL 仍存在" if os.path.exists(p) else "PASS 已删除"
    print(f"    {os.path.basename(p)}: {status}")

print("\n" + "=" * 60)
print("=== 验证完成 ===")
print("=" * 60)
