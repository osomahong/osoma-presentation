#!/usr/bin/env python3
"""캠페인 점유율 레이스용 프레임 데이터를 만든다.

30일 롤링 모금액을 하루 단위로 계산해, 각 날짜의 순위와 값을 JSON으로 떨군다.
렌더는 race.html이 맡는다. 여기서는 숫자만 만든다.
"""
import collections
import datetime as dt
import json
from pathlib import Path

import campaigns

HERE = Path(__file__).parent
DATA = HERE / "data"
START = dt.date(2025, 8, 1)
END = dt.date(2026, 8, 24)
WINDOW = 30  # 롤링 창 길이(일)
TOP_N = 8  # 화면에 띄우는 막대 수
STORE_N = 12  # 저장하는 순위 깊이. 아래에서 밀고 올라오는 막대가 부드럽게 들어온다


# 화면에 짧게 띄우는 설명. 날짜는 GA4에서 확인한 실제 변곡점이다.
ANNOTATIONS = [
    ("20250903", "카카오뱅크 배너 유입 시작"),
    ("20251224", "연말 집중 구간"),
    ("20260423", "인스타그램 캠페인 시작"),
    ("20260424", "하루 57건, 1년 최다"),
    ("20260809", "단일 고액 후원 403만 원"),
]


def load_daily():
    """{날짜: {캠페인: (건수, 금액)}} 와 캠페인 메타를 돌려준다."""
    rows = json.loads((DATA / "daily_purchase.json").read_text())
    weights = collections.Counter()
    for r in rows:
        weights[r["customEvent:donation_name"]] += int(r["eventCount"])
    cmap = campaigns.canonical_map(weights)

    daily = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0]))
    for r in rows:
        rep = cmap.get(r["customEvent:donation_name"])
        if not rep:
            continue
        cell = daily[r["date"]][rep]
        cell[0] += int(r["eventCount"])
        cell[1] += float(r["eventValue"])
    return daily


def build(include_always_on=False, window=WINDOW):
    """window가 None이면 첫날부터 그날까지 전부 더한 누적으로 만든다."""
    daily = load_daily()
    days = [
        (START + dt.timedelta(i)).strftime("%Y%m%d")
        for i in range((END - START).days + 1)
    ]

    names = set()
    for d in daily.values():
        names.update(d)
    if not include_always_on:
        names = {n for n in names if not campaigns.is_always_on(n)}
    names = sorted(names)
    idx = {n: i for i, n in enumerate(names)}

    frames = []
    for i, day in enumerate(days):
        win_amt = collections.Counter()
        win_cnt = collections.Counter()
        lo = 0 if window is None else max(0, i - window + 1)
        for d in days[lo : i + 1]:
            for name, (c, v) in daily.get(d, {}).items():
                if name not in idx:
                    continue
                win_amt[name] += v
                win_cnt[name] += c
        top = [n for n, v in win_amt.most_common(STORE_N) if v > 0]
        frames.append(
            {
                "d": day,
                "t": round(sum(win_amt.values())),
                "b": [
                    [idx[n], round(win_amt[n]), win_cnt[n]] for n in top
                ],
            }
        )
    return names, frames, daily


def churn_report(frames):
    prev = None
    churn = 0
    lead = None
    lead_changes = 0
    live = 0
    for f in frames:
        top = [b[0] for b in f["b"]][:TOP_N]
        if not top:
            continue
        live = max(live, len(top))
        if prev is not None and top != prev:
            churn += 1
        if top[0] != lead:
            lead = top[0]
            lead_changes += 1
        prev = top
    return churn, lead_changes, live


if __name__ == "__main__":
    import sys

    for win, wl in ((None, "전체 누적"), (WINDOW, f"{WINDOW}일 롤링")):
        for flag in (False, True):
            names, frames, _ = build(include_always_on=flag, window=win)
            c, lc, live = churn_report(frames)
            label = "상시 포함" if flag else "캠페인만"
            print(f"[{wl} / {label}] 캠페인 {len(names)}개, 순위변동 {c}일, 1위교체 {lc}회, 동시 막대 최대 {live}")

    if "--write" in sys.argv:
        names, frames, daily = build(include_always_on=False, window=None)
        _, frames_roll, _ = build(include_always_on=False, window=WINDOW)
        # 후원이 아직 하나도 없는 앞머리는 잘라낸다. 빈 화면으로 시작하면
        # 0원짜리 막대 하나만 떠서 고장 난 것처럼 보인다.
        first = next(i for i, f in enumerate(frames) if f["b"])
        frames = frames[first:]
        frames_roll = frames_roll[first:]

        totals = collections.Counter()
        counts = collections.Counter()
        first_seen = {}
        for day in sorted(daily):
            for n, (c, v) in daily[day].items():
                if n not in names:
                    continue
                totals[n] += v
                counts[n] += c
                first_seen.setdefault(n, day)
        payload = {
            "meta": {
                "start": frames[0]["d"],
                "end": frames[-1]["d"],
                "window": WINDOW,
                "mode": "cum",
                "label_cum": "첫날부터 그날까지 누적 모금액 기준",
                "label_roll": f"최근 {WINDOW}일 누적 모금액 기준",
                "foot_cum": "전체 누적",
                "foot_roll": f"최근 {WINDOW}일 누적",
                "top_n": TOP_N,
                "source": "GA4 속성 493257809",
            },
            "names": names,
            "totals": [
                {"name": n, "amount": round(totals[n]), "count": counts[n], "first": first_seen.get(n)}
                for n in names
            ],
            "notes": [{"d": d, "t": t} for d, t in ANNOTATIONS],
            "frames": frames,
            "frames_roll": frames_roll,
        }
        out = DATA / "race.json"
        out.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print("저장:", out, f"{out.stat().st_size/1024:.0f}KB, 프레임 {len(frames)}")

        # 템플릿에 데이터를 박아 단일 HTML로 만든다.
        tpl = HERE / "race_template.html"
        if tpl.exists():
            html = tpl.read_text(encoding="utf-8").replace(
                "/*__RACE_DATA__*/null",
                json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
            )
            dest = HERE.parent / "캠페인레이스.html"
            dest.write_text(html, encoding="utf-8")
            print("저장:", dest, f"{dest.stat().st_size/1024:.0f}KB")
