"""统计 4 个参考世界书的设计模式"""
import json
from pathlib import Path

ref_files = {
    "Tavo_小英雄": "帝王战队资料/Tavo_小英雄's Lorebook (小英雄)_SARQ.json",
    "Tavo_夏恋·私奔": "帝王战队资料/Tavo_夏恋·私奔v3.0's Lorebook (3夏恋·私奔)_SAVk.json",
    "Tavo_勇者指引指南": "帝王战队资料/Tavo_勇者指引指南 v1 四叶草编年史's Lorebook (四叶草编年史)_SATY.json",
    "Tavo_异能英雄调教模拟器": "帝王战队资料/Tavo_异能英雄调教模拟器's Lorebook (异能英雄调教模拟器)_SAUt.json",
}

base = Path("/workspace")
report = ["# 4 个参考世界书统计报告\n\n"]

for label, fp in ref_files.items():
    full_path = base / fp
    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    entries = data.get("entries", {})
    n = len(entries)
    pos_dist = {}
    const_dist = {True: 0, False: 0}
    pr_dist = {True: 0, False: 0}
    er_dist = {True: 0, False: 0}
    sd_dist = {}
    for e in entries.values():
        p = e.get("position", 0)
        pos_dist[p] = pos_dist.get(p, 0) + 1
        c = e.get("constant", False)
        const_dist[c] = const_dist.get(c, 0) + 1
        pr = e.get("preventRecursion", False)
        pr_dist[pr] = pr_dist.get(pr, 0) + 1
        er = e.get("excludeRecursion", False)
        er_dist[er] = er_dist.get(er, 0) + 1
        sd = e.get("scanDepth")
        sd_dist[sd] = sd_dist.get(sd, 0) + 1
    report.append(f"## {label}\n")
    report.append(f"- 总条目数: **{n}**\n")
    report.append(f"- position 分布: {pos_dist}\n")
    report.append(f"- constant 分布: 蓝灯 {const_dist[True]} | 绿灯 {const_dist[False]}\n")
    report.append(f"- preventRecursion: True {pr_dist[True]} | False {pr_dist[False]}\n")
    report.append(f"- excludeRecursion: True {er_dist[True]} | False {er_dist[False]}\n")
    report.append(f"- scanDepth 分布: {sd_dist}\n")
    sample_uid = list(entries.keys())[10]
    sample = entries[sample_uid]
    report.append(f"\n### 示例条目 (UID {sample_uid})\n")
    report.append(f"```json\n")
    keep = {k: v for k, v in sample.items() if k != "content"}
    report.append(json.dumps(keep, ensure_ascii=False, indent=2))
    content = sample.get("content", "")
    report.append(f"  // content (前 200 字符): {content[:200]!r}\n")
    report.append(f"```\n\n")

report.append("## 总结\n\n")
report.append("### 主要借鉴目标: Tavo_异能英雄调教模拟器\n\n")
report.append("- 主题最接近(英雄+调教+多角色)\n")
report.append("- 9 个位置 0(世界观蓝灯) + 162 个位置 4(角色/场景/装置绿灯)\n")
report.append("- 161/171 启双递归\n")
report.append("- 所有条目 `scanDepth: 2`\n\n")
report.append("### 配置模板\n\n")
report.append("**世界观光灯条目(position 0, 蓝灯):**\n")
report.append("```\n")
report.append("position: 0\n")
report.append("constant: true\n")
report.append("preventRecursion: true\n")
report.append("excludeRecursion: true\n")
report.append("```\n\n")
report.append("**角色/场景/装置/道具 绿灯条目(position 4 D0):**\n")
report.append("```\n")
report.append("position: 4\n")
report.append("depth: 0\n")
report.append("role: 0\n")
report.append("constant: false\n")
report.append("preventRecursion: true\n")
report.append("excludeRecursion: true\n")
report.append("scanDepth: 2\n")
report.append("keys: 角色名,昵称,外号,能力名\n")
report.append("```\n\n")

out = base / ".trae/specs/optimize-worldbook-v4/参考资料/参考世界书统计.md"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(report), encoding="utf-8")
print(f"Wrote {out}")
print("\n" + "="*60)
print("\n".join(report))
