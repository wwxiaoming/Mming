#!/usr/bin/env python3
"""Fix description format: convert block scalar (`|`) to single-line quoted string.

Why: Some frontmatter parsers (Claude Code, IDEs, simple regex extractors) only
read the first line of YAML. They see `description: |` and treat the value as
empty/null. The fix: use `description: "..."` (single-line quoted) for
universal compatibility.

Steps:
  1. Read each SKILL.md
  2. Locate the `description:` block (any form: |, >, plain, quoted)
  3. Replace with a single-line quoted string (escape inner " as \")
  4. Re-zip
"""
import re
import shutil
import zipfile
from pathlib import Path

SKILLS = Path("/workspace/skills_pack/_skills")
ZIPS = Path("/workspace/skills_pack/zips")

FM_RE = re.compile(r'^---\n(.*)\n---\n(.*)$', re.DOTALL)

# Match description: | block (literal) — indented lines after the key
DESC_BLOCK_RE = re.compile(r'(^|\n)description:\s*\|[+-]?\s*\n((?:[ \t]+.*\n)+)', re.MULTILINE)
# Match description: > block (folded)
DESC_FOLD_RE = re.compile(r'(^|\n)description:\s*>[+-]?\s*\n((?:[ \t]+.*\n)+)', re.MULTILINE)
# Match description: "..." (single-line quoted)
DESC_QUOTED_RE = re.compile(r'(^|\n)description:\s*"(.*?)"\s*$', re.DOTALL | re.MULTILINE)
# Match description: bare text (single-line, no quotes)
DESC_BARE_RE = re.compile(r'(^|\n)description:\s*([^\n|>"#]+?)\s*$', re.MULTILINE)


def to_single_line(text: str) -> str:
    """Strip newlines, collapse whitespace, escape inner quotes for YAML."""
    # Replace any newlines/tabs with single space
    s = re.sub(r'\s+', ' ', text).strip()
    # Escape inner double quotes (rare in our Chinese text)
    s = s.replace('\\', '\\\\').replace('"', '\\"')
    return f'description: "{s}"'


def replace_desc(content: str) -> str:
    """Replace description with a single-line quoted string, preserving FM structure."""
    m = FM_RE.match(content)
    if not m:
        raise RuntimeError("No YAML frontmatter found")
    fm, body = m.group(1), m.group(2)

    # Try block scalar (| or >) first
    new_fm, n = DESC_BLOCK_RE.subn(
        lambda mo: f"{mo.group(1)}{to_single_line(mo.group(2))}\n", fm, count=1
    )
    if n:
        return "---\n" + new_fm + "\n---\n" + body

    new_fm, n = DESC_FOLD_RE.subn(
        lambda mo: f"{mo.group(1)}{to_single_line(mo.group(2))}\n", fm, count=1
    )
    if n:
        return "---\n" + new_fm + "\n---\n" + body

    # Quoted single line (might already be in the new format we want)
    new_fm, n = DESC_QUOTED_RE.subn(
        lambda mo: f"{mo.group(1)}{to_single_line(mo.group(2))}\n", fm, count=1
    )
    if n:
        return "---\n" + new_fm + "\n---\n" + body

    # Bare single line
    new_fm, n = DESC_BARE_RE.subn(
        lambda mo: f"{mo.group(1)}{to_single_line(mo.group(2))}\n", fm, count=1
    )
    if n:
        return "---\n" + new_fm + "\n---\n" + body

    raise RuntimeError("description field not found")


ok, errors = [], []
for skill_dir in sorted(SKILLS.iterdir()):
    if not skill_dir.is_dir():
        continue
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        continue

    original = skill_md.read_text(encoding="utf-8")
    try:
        updated = replace_desc(original)
    except Exception as e:
        errors.append((skill_dir.name, f"replace failed: {e}"))
        continue

    if updated == original:
        errors.append((skill_dir.name, "no change applied"))
        continue

    skill_md.write_text(updated, encoding="utf-8")

    # Re-zip
    zip_path = ZIPS / f"{skill_dir.name}.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in skill_dir.rglob("*"):
            if p.is_file():
                zf.write(p, arcname=f"{skill_dir.name}/{p.relative_to(skill_dir)}")
    ok.append(skill_dir.name)

print(f"=== FIXED ({len(ok)}) ===")
for n in ok:
    print(f"  {n}")
print(f"\n=== ERRORS ({len(errors)}) ===")
for n, why in errors:
    print(f"  {n:50s} -> {why}")
