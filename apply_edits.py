#!/usr/bin/env python3
"""덱에서 화면으로 고친 글을 본문_소개.md 에 되박는다.

덱의 편집은 브라우저 저장소에만 남는다. 그대로 두면 다음 빌드가 만든 글 위에 옛 저장본이
덮여, 어떤 문장은 남고 어떤 문장은 사라진 것처럼 보인다. 고친 글을 본문 파일로 옮겨야
빌드가 그 글로 덱을 만든다.

    1. 덱에서 편집 바를 열고 내보내기를 누른다. 편집본_소개.json 이 내려받아진다
    2. 그 파일을 이 폴더에 두고 python3 apply_edits.py 를 돌린다
    3. python3 build_deck.py --approve 로 문장을 검수하고 승인한다
    4. 덱에서 편집 바의 되돌리기를 눌러 브라우저 저장본을 새 빌드로 맞춘다

내보내기 파일은 [{slide, i, from, to}] 목록이고, from 은 빌드가 만든 원본, to 는 고친 글이다.
본문 파일에서 from 과 같은 줄을 찾아 to 로 바꾼다. 줄을 찾지 못하면 그 항목만 건너뛰고 알린다.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEXT = ROOT / "본문_소개.md"
DEFAULT = ROOT / "편집본_소개.json"
DOWNLOADS = Path.home() / "Downloads"


def find_export(argv):
    """인자로 받은 경로, 이 폴더, 내려받기 폴더 순으로 찾는다."""
    if len(argv) > 1:
        p = Path(argv[1])
        return p if p.exists() else None
    if DEFAULT.exists():
        return DEFAULT
    got = sorted(DOWNLOADS.glob("편집본_소개*.json"), key=lambda p: p.stat().st_mtime)
    return got[-1] if got else None


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def apply(rows):
    lines = TEXT.read_text(encoding="utf-8").split("\n")
    done, miss = [], []
    for r in rows:
        a, b = norm(r["from"]), norm(r["to"])
        if a == b:
            continue
        hit = None
        for i, ln in enumerate(lines):
            # 본문의 굵게 표시와 줄 끝 공백 두 칸은 견줄 때만 걷어낸다
            plain = norm(ln.replace("**", ""))
            if plain and plain == a:
                hit = i
                break
        if hit is None:
            miss.append((r["slide"], a))
            continue
        keep_bold = lines[hit].strip().startswith("**") and lines[hit].strip().endswith("**")
        hard = lines[hit].endswith("  ")
        lines[hit] = (f"**{b}**" if keep_bold else b) + ("  " if hard else "")
        done.append((r["slide"], a, b))
    TEXT.write_text("\n".join(lines), encoding="utf-8")
    return done, miss


def main():
    src = find_export(sys.argv)
    if not src:
        print("✗ 편집본_소개.json 을 찾지 못했습니다. 덱의 편집 바에서 내보내기를 먼저 누릅니다.")
        raise SystemExit(1)
    rows = json.loads(src.read_text(encoding="utf-8"))
    done, miss = apply(rows)
    print(f"✓ {src.name} 에서 {len(rows)}곳을 읽어 {len(done)}곳을 본문에 되박았습니다")
    for slide, a, b in done:
        print(f"  {slide}  {a[:34]} → {b[:34]}")
    if miss:
        print(f"\n본문에서 같은 줄을 찾지 못한 {len(miss)}곳은 건너뛰었습니다. 직접 고칩니다.")
        for slide, a in miss:
            print(f"  {slide}  {a[:60]}")
    print("\n다음: python3 build_deck.py --approve 로 문장을 검수하고 승인합니다")


if __name__ == "__main__":
    main()
