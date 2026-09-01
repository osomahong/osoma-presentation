#!/usr/bin/env python3
"""고객사 GA4 데이터를 시연물용 JSON으로 추출한다.

GA4 속성 493257809, 기간 2025-08-01 ~ 2026-08-24.
결과는 data/ 아래에 원자료 JSON으로 떨어진다. 가공은 build_*.py가 맡는다.
"""
import json
import subprocess
import sys
from pathlib import Path

GA4_ROOT = Path("/Users/osomahong/orca/projects/ga4 분석 스킬")
PY = GA4_ROOT / ".ga4/venv/bin/python3"
QUERY = GA4_ROOT / ".claude/skills/ga-use/scripts/ga4_query.py"
PROPERTY = "493257809"
START, END = "2025-08-01", "2026-08-24"

OUT = Path(__file__).parent / "data"
OUT.mkdir(exist_ok=True)


def run(spec, name):
    """runReport 한 번. 결과를 data/<name>.json 으로 저장하고 rows를 돌려준다."""
    spec.setdefault("date_ranges", [{"start_date": START, "end_date": END}])
    proc = subprocess.run(
        [str(PY), str(QUERY), "--property", PROPERTY],
        input=json.dumps(spec),
        capture_output=True,
        text=True,
        cwd=str(GA4_ROOT),
    )
    if proc.returncode != 0:
        print(f"[{name}] 실패\n{proc.stdout[:600]}", file=sys.stderr)
        sys.exit(1)
    data = json.loads(proc.stdout)
    if "rows" not in data:
        print(f"[{name}] rows 없음\n{proc.stdout[:600]}", file=sys.stderr)
        sys.exit(1)
    (OUT / f"{name}.json").write_text(
        json.dumps(data["rows"], ensure_ascii=False), encoding="utf-8"
    )
    print(f"[{name}] {data['row_count']}행")
    return data["rows"]


QUERIES = {
    # --- 그래프 뷰 ---
    "nodes": {
        "dimensions": ["hostName", "pagePath", "pageTitle"],
        "metrics": ["screenPageViews", "sessions", "userEngagementDuration"],
        "limit": 100000,
    },
    "edges": {
        "dimensions": ["pagePath", "pageReferrer"],
        "metrics": ["screenPageViews"],
        "limit": 100000,
    },
    "landing_channel": {
        "dimensions": ["landingPage", "sessionDefaultChannelGroup", "sessionSourceMedium"],
        "metrics": ["sessions"],
        "limit": 100000,
    },
    "campaign_pages": {
        "dimensions": ["pagePath", "customEvent:donation_name"],
        "metrics": ["eventCount"],
        "dimension_filter": {"field": "eventName", "value": "view_item"},
        "limit": 5000,
    },
    "funnel_by_campaign": {
        "dimensions": ["eventName", "customEvent:donation_name"],
        "metrics": ["eventCount", "eventValue"],
        "dimension_filter": {
            "field": "eventName",
            "in_list": [
                "begin_checkout",
                "donation_start",
                "add_payment_info",
                "purchase",
                "click_donation",
            ],
        },
        "limit": 5000,
    },
    "mrm_channel": {
        "dimensions": ["hostName", "sessionDefaultChannelGroup", "sessionSourceMedium"],
        "metrics": ["sessions", "ecommercePurchases", "purchaseRevenue"],
        "limit": 5000,
    },
    # --- 레이스 ---
    "daily_purchase": {
        "dimensions": ["date", "customEvent:donation_name"],
        "metrics": ["eventCount", "eventValue"],
        "dimension_filter": {"field": "eventName", "value": "purchase"},
        "limit": 100000,
    },
    "daily_totals": {
        "dimensions": ["date"],
        "metrics": ["sessions", "totalUsers", "ecommercePurchases", "purchaseRevenue"],
        "limit": 1000,
    },
    "channel_totals": {
        "dimensions": ["sessionDefaultChannelGroup"],
        "metrics": ["sessions", "ecommercePurchases", "purchaseRevenue", "engagementRate"],
        "limit": 100,
    },
}


if __name__ == "__main__":
    for name, spec in QUERIES.items():
        run(spec, name)
    print("완료:", OUT)
