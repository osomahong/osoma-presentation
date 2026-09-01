#!/usr/bin/env python3
"""같은 GA4 자료를 표, 대시보드, 자연어 질의 세 화면으로 만든다.

노드 지도와 캠페인 레이스가 무엇을 바꾸었는지 보이려면 비교 대상이 있어야 한다.
여기서 만드는 세 화면이 그 비교 대상이고, 숫자는 그래프와 같은 원본을 쓴다.
꾸며 낸 수치를 쓰면 마지막 장의 그래프와 어긋나 대비가 흐려진다.

빌드: python3 build_analog.py
출력: ../아날로그대비.html
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"

TABLE_ROWS = 26        # 화면에 보이는 만큼만 넣는다. 스크롤은 어차피 안 보인다.
SERIES_MAX = 389       # 일자별 꺾은선에 쓰는 날수


def load(name):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


def table_view():
    """GA4 페이지 보고서를 엑셀로 내려받은 모습. 열 이름도 내보내기 그대로 둔다."""
    rows = load("nodes")
    keep = [r for r in rows if r["hostName"] in ("merryyear.org", "online.mrm.or.kr")]
    keep.sort(key=lambda r: -int(r["screenPageViews"]))
    out = [[r["hostName"], r["pagePath"], r["pageTitle"],
            int(r["screenPageViews"]), int(r["sessions"]), int(r["userEngagementDuration"])]
           for r in keep[:TABLE_ROWS]]
    return {
        "head": ["hostName", "pagePath", "pageTitle",
                 "screenPageViews", "sessions", "userEngagementDuration"],
        "rows": out,
        "total": len(rows),
        "pvSum": sum(int(r["screenPageViews"]) for r in rows),
    }


def dash_view():
    """대시보드. 미리 정해 둔 지표만 걸려 있다는 것이 이 화면의 성격이다."""
    days = load("daily_totals")
    days.sort(key=lambda d: d["date"])
    chans = load("channel_totals")
    chans.sort(key=lambda c: -int(c["sessions"]))

    sess = sum(int(d["sessions"]) for d in days)
    users = sum(int(d["totalUsers"]) for d in days)
    pur = sum(int(d["ecommercePurchases"]) for d in days)
    rev = round(sum(float(d["purchaseRevenue"]) for d in days))

    # 앞뒤 절반을 견줘 증감을 낸다. 대시보드에 늘 붙어 있는 그 화살표다.
    half = len(days) // 2
    def delta(key, cast=int):
        a = sum(cast(d[key]) for d in days[:half]) or 1
        b = sum(cast(d[key]) for d in days[half:])
        return (b - a) / a * 100

    cards = []
    for label, val, key, cast in [
        ("총 사용자", f"{users:,}", "totalUsers", int),
        ("세션", f"{sess:,}", "sessions", int),
        ("후원 완료", f"{pur:,}", "ecommercePurchases", int),
        ("수익", f"{rev:,}원", "purchaseRevenue", float),
    ]:
        d = delta(key, cast)
        cards.append({"k": label, "v": val, "up": d >= 0, "d": f"{abs(d):.1f}%"})

    return {
        "cards": cards,
        "series": [int(d["sessions"]) for d in days[-SERIES_MAX:]],
        "bars": [[c["sessionDefaultChannelGroup"], int(c["sessions"])] for c in chans[:8]],
        "tab": [[c["sessionDefaultChannelGroup"], int(c["sessions"]),
                 float(c["engagementRate"]) * 100, int(c["ecommercePurchases"]),
                 round(float(c["purchaseRevenue"]))] for c in chans[:6]],
    }


def main():
    payload = {"table": table_view(), "dash": dash_view()}
    tpl = HERE / "analog_template.html"
    html = tpl.read_text(encoding="utf-8").replace(
        "/*__ANALOG_DATA__*/null",
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
    )
    dest = HERE.parent / "아날로그대비.html"
    dest.write_text(html, encoding="utf-8")

    t, d = payload["table"], payload["dash"]
    print(f"표: {t['total']:,}행 중 {len(t['rows'])}행 표시, 조회수 합계 {t['pvSum']:,}")
    print(f"대시보드: 카드 {len(d['cards'])}장, 꺾은선 {len(d['series'])}일, 막대 {len(d['bars'])}개")
    print(f"저장: {dest} {dest.stat().st_size/1024:.0f}KB")


if __name__ == "__main__":
    main()
