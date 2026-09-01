#!/usr/bin/env python3
"""donation_name 정리 규칙.

GA4에 들어온 캠페인 이름은 페이지 제목, 안내 문구, 이모지가 섞여 있다.
화면에 실명을 그대로 띄우기로 했으므로, 사람이 읽을 수 있는 형태로만 다듬고
같은 캠페인의 표기 차이는 하나로 합친다. 뜻을 바꾸는 축약은 하지 않는다.
"""
import difflib
import re
import unicodedata

# 캠페인이 아닌 값. 페이지 제목, 빈값, 안내 문구가 여기 들어온다.
DROP_EXACT = {
    "",
    "(not set)",
    "| 완료",
    "열매나눔재단",
    "후원가이드 - ",
    "후원 신청 완료 후 후원 동기에 사연을 꼭 적어주세요!",
}

# 개별 캠페인이 아니라 상시로 열려 있는 후원 창구.
ALWAYS_ON = {
    "열매나눔재단 후원하기",
    "열매나눔재단 정기 후원",
    "열매나눔재단 일시 후원",
    "열매나눔재단 기념일 후원",
    "열매나눔재단 씨앗가게 후원",
    "열매나눔재단 아동청소년 일시후원",
    "기업 및 단체후원",
}

_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0000FE00-\U0000FE0F\U00002190-\U000021FF\U00002B00-\U00002BFF]"
)
_QUOTES = "\"'“”‘’「」『』"


def _tidy(name: str) -> str:
    """이모지, 따옴표, 끝의 느낌표, 겹친 공백을 걷어낸다."""
    s = unicodedata.normalize("NFC", name).strip()
    s = _EMOJI.sub("", s)
    s = s.strip().strip(_QUOTES).strip()
    s = re.sub(r"\s+", " ", s)
    s = s.rstrip("!").strip()  # 끝의 느낌표만 뗀다. 문장 안의 것은 둔다
    return s.replace("·", "")  # 가운뎃점


# 버릴 값도 같은 규칙으로 다듬어 두어야 표기 차이로 새어 나가지 않는다.
_DROP_CLEANED = {_tidy(x) for x in DROP_EXACT}


def clean(name: str) -> str | None:
    """표시용 이름으로 다듬는다. 캠페인이 아니면 None."""
    if name is None or "|" in name:  # "후원가이드 | 열매나눔재단" 같은 페이지 제목
        return None
    s = _tidy(name)
    if s in _DROP_CLEANED or len(s) < 2:
        return None
    return s


def _key(s: str) -> str:
    """표기 차이를 무시한 비교용 키."""
    return re.sub(r"[^\w가-힣]", "", s)


# 상시 창구는 이름이 서로 비슷해서 유사도로 묶으면 하나로 뭉개진다.
# "정기 후원"과 "기념일 후원"은 다른 창구이므로 각자 이름을 지킨다.
_ALWAYS_KEYS = {_key(x) for x in ALWAYS_ON}


def canonical_map(names, cutoff: float = 0.82) -> dict:
    """원본 이름 -> 대표 이름. 등장 빈도가 높은 표기를 대표로 삼는다.

    names: {원본 이름: 가중치} 또는 원본 이름들의 시퀀스
    """
    if not isinstance(names, dict):
        weights = {}
        for n in names:
            weights[n] = weights.get(n, 0) + 1
        names = weights

    cleaned = {}
    for raw, w in names.items():
        c = clean(raw)
        if c:
            cleaned.setdefault(c, 0)
            cleaned[c] += w

    # 가중치가 큰 표기부터 대표로 확정한다.
    reps: list[str] = []
    rep_of: dict[str, str] = {}
    for c, _ in sorted(cleaned.items(), key=lambda x: (-x[1], x[0])):
        ck = _key(c)
        hit = None
        if ck in _ALWAYS_KEYS:  # 상시 창구는 유사도 병합에서 뺀다
            reps.append(c)
            rep_of[c] = c
            continue
        for r in reps:
            if _key(r) in _ALWAYS_KEYS:
                continue
            rk = _key(r)
            if ck == rk or ck in rk or rk in ck:
                hit = r
                break
            if difflib.SequenceMatcher(None, ck, rk).ratio() >= cutoff:
                hit = r
                break
        if hit:
            rep_of[c] = hit
        else:
            reps.append(c)
            rep_of[c] = c

    out = {}
    for raw in names:
        c = clean(raw)
        out[raw] = rep_of.get(c) if c else None
    return out


def is_always_on(display: str) -> bool:
    return _key(display) in {_key(x) for x in ALWAYS_ON}


if __name__ == "__main__":
    import collections
    import json
    from pathlib import Path

    rows = json.loads((Path(__file__).parent / "data/daily_purchase.json").read_text())
    w = collections.Counter()
    for r in rows:
        w[r["customEvent:donation_name"]] += int(r["eventCount"])
    m = canonical_map(w)
    grouped = collections.Counter()
    for raw, n in w.items():
        rep = m.get(raw)
        grouped[rep if rep else "(제외)"] += n
    for k, v in grouped.most_common():
        tag = "상시" if k != "(제외)" and is_always_on(k) else "캠페인"
        print(f"{v:>4}건 [{tag}] {k}")
