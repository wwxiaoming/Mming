"""扫描所有 v4 文件,检测缺失的代码块闭合"""
import re
from pathlib import Path

v4 = Path("帝王战队资料/世界书条目v4")
files = list(v4.rglob("*.md"))
unclosed = []
closed_count = 0
for f in files:
    text = f.read_text(encoding="utf-8")
    # 计算 ``` 的数量(应为偶数)
    count = text.count("```")
    if count % 2 != 0:
        # 奇数个 - 缺失闭合
        rel = f.relative_to(v4)
        unclosed.append((str(rel), count))
    else:
        closed_count += 1
print(f"文件总数: {len(files)}")
print(f"闭合正常: {closed_count}")
print(f"缺失闭合: {len(unclosed)}")
print()
print("缺失闭合的文件清单:")
for f, c in unclosed:
    print(f"  {f} (``` 出现 {c} 次)")
