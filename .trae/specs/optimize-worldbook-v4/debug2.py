"""调试:手工处理 问天.md 一次,看 clean_run 实际产出的内容"""
import re
from pathlib import Path
import importlib.util

base = Path("/workspace")
v4 = base / "帝王战队资料/世界书条目v4"
spec = importlib.util.spec_from_file_location("matrix_mod", base / ".trae/specs/optimize-worldbook-v4/build_matrix.py")
matrix_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(matrix_mod)
matrix = matrix_mod.matrix

# 加载 问天.md
fp = v4 / "英雄设定" / "01_问天.md"
text = fp.read_text(encoding="utf-8")
print("=" * 60)
print("ORIGINAL:")
print(text[:2000])
print("=" * 60)

# 找 yaml 块
code_block_pattern = re.compile(
    r"```(yaml|xml)\s*\n(.*?)(?:</yaml>\s*\n)?```",
    re.DOTALL
)
matches = list(code_block_pattern.finditer(text))
print(f"\nMatches: {len(matches)}")
for i, m in enumerate(matches):
    print(f"  Match {i}: {m.group(1)} from {m.start()} to {m.end()}")
    print(f"  Content: {m.group(2)[:500]!r}")
    print()
