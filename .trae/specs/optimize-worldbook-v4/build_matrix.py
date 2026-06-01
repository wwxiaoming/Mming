"""为 v4 世界书条目生成配置矩阵
基于参考世界书最佳实践 + 10 个分类的特性"""
from pathlib import Path

base = Path("/workspace")
v4 = base / "帝王战队资料/世界书条目v4"

# 配置策略定义
STRATEGY = {
    "世界观": {
        "mode": "blue_0",
        "position": 0,
        "depth": None,
        "role": None,
        "constant": True,
        "preventRecursion": True,
        "excludeRecursion": True,
        "scanDepth": None,
        "note": "世界观总纲/帝王战队/神魔号/宇宙之子/天火 - 全局蓝灯常驻",
    },
    "系统规则": {
        "mode": "blue_0",
        "position": 0,
        "depth": None,
        "role": None,
        "constant": True,
        "preventRecursion": True,
        "excludeRecursion": True,
        "scanDepth": None,
        "note": "收服/战斗/补魔/契约等机制层 - 全局蓝灯",
    },
    "阵营": {
        "mode": "blue_0",
        "position": 0,
        "depth": None,
        "role": None,
        "constant": True,
        "preventRecursion": True,
        "excludeRecursion": True,
        "scanDepth": None,
        "note": "核心组织 - 蓝灯常驻",
    },
    "英雄设定": {
        "mode": "green_4",
        "position": 4,
        "depth": 0,
        "role": 0,
        "constant": False,
        "preventRecursion": True,
        "excludeRecursion": True,
        "scanDepth": 2,
        "note": "15 位英雄 - 位置 4 D0 触发",
    },
    "NPC设定": {
        "mode": "green_4",
        "position": 4,
        "depth": 0,
        "role": 0,
        "constant": False,
        "preventRecursion": True,
        "excludeRecursion": True,
        "scanDepth": 2,
        "note": "魔神会干部/反派/龙神等 - 位置 4 D0 触发",
    },
    "专属装置": {
        "mode": "green_4",
        "position": 4,
        "depth": 0,
        "role": 0,
        "constant": False,
        "preventRecursion": True,
        "excludeRecursion": True,
        "scanDepth": 2,
        "note": "15 种榨精装置 - 位置 4 D0 触发",
    },
    "道具设定": {
        "mode": "green_4",
        "position": 4,
        "depth": 0,
        "role": 0,
        "constant": False,
        "preventRecursion": True,
        "excludeRecursion": True,
        "scanDepth": 2,
        "note": "堕落神装/神纹/装备等 - 位置 4 D0 触发",
    },
    "组织势力": {
        "mode": "green_4",
        "position": 4,
        "depth": 0,
        "role": 0,
        "constant": False,
        "preventRecursion": True,
        "excludeRecursion": True,
        "scanDepth": 2,
        "note": "古武世家 - 位置 4 D0 触发",
    },
    "地区设定": {
        "mode": "mixed",
        "position": None,  # 01_人类安全区 用 0, 其余用 4
        "depth": 0,
        "role": 0,
        "constant": None,
        "preventRecursion": True,
        "excludeRecursion": True,
        "scanDepth": 2,
        "note": "01_人类安全区=蓝灯 0; 其余=绿灯 4",
    },
    "剧情设定": {
        "mode": "mixed",
        "position": None,
        "depth": 0,
        "role": 0,
        "constant": None,
        "preventRecursion": True,
        "excludeRecursion": True,
        "scanDepth": 2,
        "note": "00_三条路线总纲=蓝灯 0; 01~15 篇=绿灯 4",
    },
}

# 地区设定特殊规则
REGION_RULES = {
    "01_人类安全区.md": ("blue_0", 0, None, None, True),
}

# 剧情设定特殊规则
PLOT_RULES = {
    "00_三条路线总纲.md": ("blue_0", 0, None, None, True),
}

# 英雄 keys 映射
HERO_KEYS = {
    "01_问天.md": "问天,祖龙,秩序之子,脚奴,六元素掌控者",
    "02_千瑞.md": "千瑞,大地之子,贱虎,土元素掌控者,大地之躯",
    "03_子夜.md": "子夜,乾坤,光暗双修,法则掌控者",
    "04_阚泽.md": "阚泽,超能,魔能结晶,感知强化者",
    "05_凯风.md": "凯风,时空,时空双属性,时空掌控者",
    "06_空耀.md": "空耀,轮回,鬼魂克星,六道轮回",
    "07_嘉陵.md": "嘉陵,神魔,影分身,暗影侵蚀者",
    "08_岚云.md": "岚云,幻术,幻狐血脉,幻术师",
    "09_启润.md": "启润,风系,古武陈家,风元素掌控者",
    "10_星野.md": "星野,星轨,星辰系,卧底",
    "11_诗华.md": "诗华,圣灵,光明系,治疗者",
    "12_战炎.md": "战炎,麒麟血脉,火焰,魔兽后裔",
    "13_暮黎.md": "暮黎,龙凰双脉,水系,战炎义兄",
    "14_准星.md": "准星,烈阳世家,夜鸦战队,古武格斗",
    "15_文斌.md": "文斌,誓约,机械之子,猫奴,弱点洞悉,机械星辉",
}

# 矩阵生成
matrix = {}
for category, strategy in STRATEGY.items():
    cat_path = v4 / category
    if not cat_path.exists():
        continue
    files = sorted(cat_path.glob("*.md"))
    for f in files:
        fname = f.name
        if strategy["mode"] == "mixed":
            if category == "地区设定" and fname in REGION_RULES:
                mode, pos, depth, role, const = REGION_RULES[fname]
            elif category == "剧情设定" and fname in PLOT_RULES:
                mode, pos, depth, role, const = PLOT_RULES[fname]
            else:
                mode = "green_4"
                pos = 4
                depth = 0
                role = 0
                const = False
        else:
            pos = strategy["position"]
            depth = strategy["depth"]
            role = strategy["role"]
            const = strategy["constant"]
            mode = strategy["mode"]
        # keys
        if mode == "green_4":
            if category == "英雄设定" and fname in HERO_KEYS:
                keys = HERO_KEYS[fname]
            elif category == "世界观":
                if "00_世界观总纲" in fname:
                    keys = None
                elif "01_帝王战队" in fname:
                    keys = "帝王战队,S级英雄,少年英雄,宇宙之子"
                elif "02_神魔号" in fname:
                    keys = "神魔号,神魔号系统,共生飞船,少年调教系统"
                elif "03_宇宙之子" in fname:
                    keys = "宇宙之子,容器,容器理论,诸神黄昏"
                elif "04_死寂沙漠" in fname:
                    keys = "死寂沙漠,蒲罗树,沙漠秘境"
                elif "05_天火" in fname:
                    keys = "天火,穿越者,指挥官,神魔号宿主"
                else:
                    keys = None
            elif category == "NPC设定":
                if "01_魔神会干部" in fname:
                    keys = "魔神会干部,皇后,洛基,奥西里斯,休,魔王主教,鼹鼠主教,暗狮,红衣主教,枢机主教"
                elif "02_反派势力" in fname:
                    keys = "反派势力,红衣主教,造神计划,深渊"
                elif "03_帝王战队关联人物" in fname:
                    keys = "帝王战队关联人物,亲友,同学,导师"
                elif "04_系统意志" in fname:
                    keys = "系统意志,神魔号系统,最终反派,诸神黄昏"
                elif "05_黑文斌" in fname:
                    keys = "黑文斌,暴走文斌,机械星辉,失控"
                elif "06_龙神" in fname:
                    keys = "龙神,龙族,秘境守护者"
                else:
                    keys = "NPC"
            elif category == "专属装置":
                # 装置 keys 用文件名去编号
                base_name = fname.split("_", 1)[1].replace(".md", "")
                keys = base_name
            elif category == "道具设定":
                if "01_堕落神装" in fname:
                    keys = "堕落神装,神装,紧身衣"
                elif "02_神纹系统" in fname:
                    keys = "神纹,神纹系统,淫纹,烙印"
                elif "03_魔神会黑科技" in fname:
                    keys = "魔神会黑科技,魔神会科技,改造"
                elif "04_通用调教道具" in fname:
                    keys = "调教道具,通用道具,束缚具"
                elif "05_魔物相关道具" in fname:
                    keys = "魔物道具,魔兽相关,魔物材料"
                elif "06_战斗装备与武器" in fname:
                    keys = "战斗装备,武器,武器库"
                else:
                    keys = "道具"
            elif category == "组织势力":
                if "炎陈世家" in fname:
                    keys = "炎陈世家,陈家,古武世家"
                elif "烈阳世家" in fname:
                    keys = "烈阳世家,烈阳,古武世家"
                else:
                    keys = "组织势力"
            elif category == "地区设定":
                base_name = fname.split("_", 1)[1].replace(".md", "")
                keys = base_name
            elif category == "剧情设定":
                base_name = fname.split("_", 1)[1].replace(".md", "")
                # 加角色名作为 keys
                if "问天篇" in fname:
                    keys = "问天篇,问天,序章"
                elif "千瑞篇" in fname:
                    keys = "千瑞篇,千瑞,序章"
                elif "子夜篇" in fname:
                    keys = "子夜篇,子夜,序章"
                elif "空耀篇" in fname:
                    keys = "空耀篇,空耀,序章"
                elif "阚泽篇" in fname:
                    keys = "阚泽篇,阚泽,序章"
                elif "凯风篇" in fname:
                    keys = "凯风篇,凯风,序章"
                elif "诗华篇" in fname:
                    keys = "诗华篇,诗华,序章"
                elif "嘉陵篇" in fname:
                    keys = "嘉陵篇,嘉陵,序章"
                elif "文斌篇" in fname:
                    keys = "文斌篇,文斌,序章"
                elif "启润篇" in fname:
                    keys = "启润篇,启润,序章"
                elif "岚云篇" in fname:
                    keys = "岚云篇,岚云,序章"
                elif "准星篇" in fname:
                    keys = "准星篇,准星,序章"
                elif "星野篇" in fname:
                    keys = "星野篇,星野,序章"
                elif "战炎篇" in fname:
                    keys = "战炎篇,战炎,序章"
                elif "暮黎篇" in fname:
                    keys = "暮黎篇,暮黎,序章"
                else:
                    keys = base_name
            else:
                keys = None
        else:
            keys = None
        matrix[f"{category}/{fname}"] = {
            "category": category,
            "filename": fname,
            "mode": mode,
            "position": pos,
            "depth": depth,
            "role": role,
            "constant": const,
            "preventRecursion": True,
            "excludeRecursion": True,
            "scanDepth": 2 if const is False else None,
            "keys": keys,
            "note": strategy["note"],
        }

# 写入 YAML
out = base / ".trae/specs/optimize-worldbook-v4/产物/配置矩阵.yaml"
out.parent.mkdir(parents=True, exist_ok=True)

lines = ["# v4 世界书条目配置矩阵", ""]
lines.append("# 基于参考世界书最佳实践,适用于 85 个条目")
lines.append("")
lines.append("categories:")
for cat, strat in STRATEGY.items():
    lines.append(f"  {cat}:")
    lines.append(f"    mode: {strat['mode']}")
    lines.append(f"    note: \"{strat['note']}\"")
lines.append("")
lines.append("entries:")
for key, conf in matrix.items():
    lines.append(f"  - file: {key}")
    lines.append(f"    mode: {conf['mode']}")
    lines.append(f"    position: {conf['position']}")
    if conf['depth'] is not None:
        lines.append(f"    depth: {conf['depth']}")
    if conf['role'] is not None:
        lines.append(f"    role: {conf['role']}")
    lines.append(f"    constant: {str(conf['constant']).lower()}")
    lines.append(f"    preventRecursion: {str(conf['preventRecursion']).lower()}")
    lines.append(f"    excludeRecursion: {str(conf['excludeRecursion']).lower()}")
    if conf['scanDepth'] is not None:
        lines.append(f"    scanDepth: {conf['scanDepth']}")
    if conf['keys']:
        lines.append(f"    keys: \"{conf['keys']}\"")
    lines.append("")

out.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {out}")
print(f"Total entries: {len(matrix)}")
print(f"By category:")
from collections import Counter
counter = Counter(c['category'] for c in matrix.values())
for cat, n in counter.items():
    print(f"  {cat}: {n}")
