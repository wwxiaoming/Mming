#!/usr/bin/env python3
"""从 git 历史恢复英雄设定路线分支原内容，与剧情设定做精准对比。"""
import os
import re
import subprocess
import glob

base = "/workspace/帝王战队资料/世界书条目v4"

# 从 git HEAD 之前的某个 commit 拿（dd34297 是修改前的最新版本）
git_cmd = ["git", "show", "dd34297:帝王战队资料/世界书条目v4/英雄设定"]

results = []
for i in range(1, 16):
    name = f"{i:02d}"
    hfile = glob.glob(f"{base}/英雄设定/{name}_*.md")[0]
    pfile = glob.glob(f"{base}/剧情设定/{name}_*.md")[0]

    hname = os.path.basename(hfile).replace(".md", "")
    pname = os.path.basename(pfile).replace(".md", "")

    # 从 git 取原内容
    hfile_rel = "帝王战队资料/世界书条目v4/英雄设定/" + os.path.basename(hfile)
    htext_old = subprocess.run(
        ["git", "show", f"dd34297:{hfile_rel}"],
        capture_output=True, text=True
    ).stdout

    with open(pfile) as f:
        ptext = f.read()

    # 提取原 ## 路线分支 段
    m = re.search(r'  ## 路线分支\n(.*?)(?=\n  ## |\Z)', htext_old, re.DOTALL)
    if not m:
        results.append((hname, pname, "无原路线分支段", 0, 0, []))
        continue
    route_text = m.group(1)

    # 提取每个剧情节点标题
    node_titles = re.findall(r'剧情节点 \d【[^】]+】', route_text)

    # 检查剧情设定里有多少节点标题被覆盖
    covered = 0
    uncovered = []
    for title in node_titles:
        # 提取【】内的章节名
        chapter_m = re.search(r'【(.+?)】', title)
        if chapter_m:
            chapter = chapter_m.group(1)
            if chapter in ptext or chapter.replace("~", "至") in ptext:
                covered += 1
            else:
                uncovered.append(chapter)

    results.append((hname, pname, "OK", len(node_titles), covered, uncovered))

print(f"{'英雄':<14} {'剧情':<14} {'原节点数':<8} {'剧情覆盖':<10} 未覆盖章节")
print("-" * 130)
total_uncovered = []
for hname, pname, status, total, covered, uncovered in results:
    un_str = ", ".join(uncovered) if uncovered else "（全部覆盖）"
    print(f"{hname:<14} {pname:<14} {total:<8} {covered}/{total:<6} {un_str}")
    total_uncovered.extend(uncovered)

print(f"\n总未覆盖节点：{len(total_uncovered)}")
print(f"  全部章节：{total_uncovered}")
