#!/usr/bin/env python3
"""덱을 한 장 한 쪽으로 PDF로 찍는다.

크롬 헤드리스의 인쇄 기능을 그대로 쓴다. 덱의 장이 쪽 크기와 같아
설정 없이 한 장이 한 쪽으로 나온다. 끝나면 pypdf로 쪽수를 대조한다.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT = Path(__file__).parent
SRC = ROOT / "쇼케이스_AX60_인쇄.html"   # 시연물을 내용이 가장 많은 장면에 멈춘 인쇄 전용 판
OUT = ROOT / "쇼케이스_AX60.pdf"


def expected_pages():
    m = re.search(r"TOTAL = (\d+)", (ROOT / "build_ax.py").read_text(encoding="utf-8"))
    return int(m.group(1)) if m else None


if __name__ == "__main__":
    # 인쇄 전용 판을 먼저 새로 굽는다. 시연물이 멈춘 장면으로 박혀 나온다
    subprocess.run([sys.executable, "build_ax.py", "--print"], cwd=ROOT, check=True)
    # 덱 안의 시연물이 끝없이 그림을 갱신해서 크롬이 PDF를 쓰고도 스스로 끝나지
    # 않는다. 파일이 나올 때까지 기다렸다가 프로세스를 거둔다.
    import time
    OUT.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as profile:
        proc = subprocess.Popen(
            [CHROME, "--headless=new", "--disable-gpu", "--no-first-run",
             f"--user-data-dir={profile}", "--no-pdf-header-footer",
             "--virtual-time-budget=20000",
             f"--print-to-pdf={OUT}", SRC.as_uri()],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        deadline = time.time() + 540
        while time.time() < deadline and proc.poll() is None:
            if OUT.exists() and OUT.stat().st_size > 0:
                time.sleep(3)   # 쓰다 만 파일을 잡지 않도록 잠깐 더 기다린다
                break
            time.sleep(2)
        proc.kill()
    if not OUT.exists():
        print("✗ PDF가 나오지 않았다")
        sys.exit(1)
    import pypdf
    pages = len(pypdf.PdfReader(OUT).pages)
    want = expected_pages()
    print(f"저장: {OUT.name} {pages}쪽, {OUT.stat().st_size/1024/1024:.1f}MB")
    if want and pages != want:
        print(f"✗ 덱은 {want}장인데 PDF는 {pages}쪽이다. 인쇄를 다시 확인해야 한다")
        sys.exit(1)
