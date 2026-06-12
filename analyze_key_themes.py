#!/usr/bin/env python3
"""对比英雄设定 vs 剧情设定 关键叙事词，找出剧情设定可能遗漏的"优质节点"细节。"""
import os
import re
import glob

base = "/workspace/帝王战队资料/世界书条目v4"

# 关键叙事词（从小说里常出现的主题/桥段/意象/反差点）
KEY_THEMES = [
    "双面", "反差", "晨起", "晚安", "侍奉", "契约", "觉醒",
    "足心", "足弓", "足趾", "三联动", "祖龙", "神纹", "淫纹",
    "队长", "副队长", "副官", "副手",
    "展示", "展演", "案例", "观摩",
    "公开展示",
    "侍寝", "侍奉", "侍候",
    "战间", "战前", "战后",
    "秘密", "暴露", "暴露癖",
    "逆推", "攻略", "沦陷",
    "屈服", "服从",
    "傲慢", "高傲",
    "冷酷", "傲娇",
    "伪装", "掩饰",
    "巡查", "巡检", "检阅",
    "公开", "私密", "私下",
    "仪式", "礼仪", "典礼",
    "投降", "认输", "认败",
    "承欢", "承恩",
    "正装", "制服", "便装",
    "眉眼", "泪光", "含泪",
    "锁骨", "喉结",
    "腿根", "大腿", "腋下",
    "乳尖", "乳头", "乳钉",
    "肛塞", "菊穴", "屁穴",
    "塞子", "撑开",
    "触手", "足底触手",
    "半龙", "化龙",
    "蛇瞳", "竖瞳", "金瞳",
    "队长威严", "队长仪式",
    "脱袜", "跪下", "单膝",
    "投降式", "认主式", "起誓式",
]

results = []
for i in range(1, 16):
    name = f"{i:02d}"
    hfile = glob.glob(f"{base}/英雄设定/{name}_*.md")[0]
    pfile = glob.glob(f"{base}/剧情设定/{name}_*.md")[0]

    hname = os.path.basename(hfile).replace(".md", "")
    pname = os.path.basename(pfile).replace(".md", "")

    with open(hfile) as f:
        htext = f.read()
    with open(pfile) as f:
        ptext = f.read()

    hero_len = len(htext)
    plot_len = len(ptext)

    # 在英雄设定里出现且在剧情设定里没出现的主题
    missing_themes = []
    for theme in KEY_THEMES:
        if theme in htext and theme not in ptext:
            missing_themes.append(theme)

    results.append((hname, pname, hero_len, plot_len, missing_themes))

print(f"{'英雄':<14} {'剧情':<14} {'英雄字':<8} {'剧情字':<8} 剧情中可能缺失的关键词")
print("-" * 130)
for hname, pname, hlen, plen, missing in results:
    miss_str = ", ".join(missing[:8]) if missing else "（无）"
    if len(missing) > 8:
        miss_str += f" 等共 {len(missing)} 项"
    print(f"{hname:<14} {pname:<14} {hlen:<8} {plen:<8} {miss_str}")
