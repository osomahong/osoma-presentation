#!/usr/bin/env python3
"""원격 지휘 연출의 완성본을 만든다.

data/orchestra.json 의 시나리오를 orchestra_template.html 에 박아
../지휘실.html 한 파일로 떨군다. GA4 조회가 필요 없는 연출물이라
숫자 계산 없이 대본과 화면을 잇기만 한다.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent

BANNED = ["—", "–", "·", "…"]  # 화면 문구에 쓰지 않기로 한 기호


def check(data):
    """화면에 보이는 문구만 훑어 금지 기호를 잡는다."""
    texts = []
    texts.append(data["meta"]["title"])
    texts.append(data["meta"]["sub"])
    for s in data["scenes"]:
        texts += [s["name"], s["cap"]]
    for j in data["jobs"]:
        texts += [j["kind"], j["ask"], j["head"], j["notice"], j["result"]]
        for a in j["agents"]:
            texts += [a["name"], a["run"], a["done"]]
    texts.append(data["wrap"]["text"])
    for e in data["timeline"]["events"]:
        texts.append(e["label"])
    texts += [data["closing"]["l1"], data["closing"]["l2"], data["closing"]["sub"]]
    bad = [(t, ch) for t in texts for ch in BANNED if ch in t]
    if bad:
        for t, ch in bad:
            print(f"✗ 금지 기호 {ch!r}: {t}")
        raise SystemExit(1)


if __name__ == "__main__":
    data = json.loads((HERE / "data" / "orchestra.json").read_text(encoding="utf-8"))
    check(data)
    tpl = (HERE / "orchestra_template.html").read_text(encoding="utf-8")
    html = tpl.replace(
        "/*__ORCHESTRA_DATA__*/null",
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
    )
    dest = HERE.parent / "지휘실.html"
    dest.write_text(html, encoding="utf-8")
    print("저장:", dest, f"{dest.stat().st_size/1024:.0f}KB")
