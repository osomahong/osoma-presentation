#!/usr/bin/env python3
"""재단 웹 전체를 세 겹의 온톨로지 그래프로 배치한다.

바깥 고리는 유입원, 가운데 성운은 merryyear.org 콘텐츠, 안쪽 핵은 결제 층이다.
두 도메인은 링크로 이어지지 않으므로 donation_name을 열쇠로 다리를 놓는다.
배치 좌표는 여기서 계산해 박아 넣는다. 브라우저에서 1,300개를 실시간으로
밀고 당기면 느려진다.
"""
import collections
import json
import random
import zlib
import math
import re
from pathlib import Path

import numpy as np

import campaigns as C

HERE = Path(__file__).parent
DATA = HERE / "data"

# 카테고리. 색은 밤하늘 위에서 서로 구분되도록 골랐다.
CATS = [
    {"key": "home", "label": "홈", "color": "#FFFFFF",
     "desc": "재단 첫 화면입니다. 여기서 길이 갈라져 나갑니다"},
    {"key": "camp", "label": "캠페인", "color": "#FFB454",
     "desc": "후원을 받는 사연 페이지입니다"},
    {"key": "news", "label": "소식", "color": "#5AA9FF",
     "desc": "재단이 올린 공지와 이야기입니다"},
    {"key": "biz", "label": "사업 소개", "color": "#34D3B4",
     "desc": "재단이 하는 일을 설명합니다"},
    {"key": "about", "label": "재단 소개", "color": "#C77DFF",
     "desc": "재단이 어떤 곳인지 알립니다"},
    {"key": "supp", "label": "후원 안내", "color": "#FF6B8A",
     "desc": "후원하는 방법을 안내합니다"},
    {"key": "etc", "label": "그 밖의 페이지", "color": "#7E8CB0",
     "desc": "채용 공고처럼 앞의 어디에도 들지 않는 페이지입니다"},
]
CAT_IDX = {c["key"]: i for i, c in enumerate(CATS)}

# 카테고리를 원 둘레의 어느 방향에 모을지. 라디안.
ANCHOR = {
    "camp": -0.35,
    "news": 1.55,
    "biz": 2.75,
    "about": 3.55,
    "supp": 4.55,
    "etc": 5.45,
    "home": 0.0,
}

FUNNEL = [
    ("begin_checkout", "후원 페이지 진입"),
    ("donation_start", "후원 시작"),
    ("add_payment_info", "결제 정보 입력"),
    ("purchase", "후원 완료"),
]


def category(path: str) -> str:
    if path == "/":
        return "home"
    if path.startswith("/archives/supp"):
        return "camp"
    if path.startswith("/archives/news"):
        return "news"
    if path.startswith("/business"):
        return "biz"
    if path.startswith("/about"):
        return "about"
    if path.startswith("/support"):
        return "supp"
    return "etc"


def norm_path(p: str) -> str:
    """끝의 빗금 하나만 다른 주소를 같은 페이지로 본다."""
    if not p.startswith("/"):
        p = "/" + p
    return p if p == "/" else p.rstrip("/")


def clean_title(t: str, path: str) -> str:
    t = (t or "").split("|")[0].strip()
    t = re.sub(r"\s+", " ", t)
    if not t or t.lower() in ("not found", "(not set)"):
        return path
    return t


# --------------------------------------------------------------------------- #
# 1. 노드
# --------------------------------------------------------------------------- #
def load_pages():
    rows = json.loads((DATA / "nodes.json").read_text())
    agg = {}
    titles = collections.defaultdict(collections.Counter)
    for r in rows:
        if r["hostName"] != "merryyear.org":
            continue
        p = norm_path(r["pagePath"])
        pv = int(r["screenPageViews"])
        a = agg.setdefault(p, {"pv": 0, "sess": 0, "eng": 0})
        a["pv"] += pv
        a["sess"] += int(r["sessions"])
        a["eng"] += int(r["userEngagementDuration"])
        titles[p][clean_title(r["pageTitle"], p)] += pv or 1
    for p, a in agg.items():
        a["title"] = titles[p].most_common(1)[0][0]
        a["cat"] = category(p)

    # "소식 카테고리" 처럼 같은 제목을 쓰는 페이지가 여럿이면 주소 끝을 붙여 가른다
    seen = collections.Counter(a["title"] for a in agg.values())
    for p, a in agg.items():
        if seen[a["title"]] > 1:
            tail = [x for x in p.split("/") if x]
            # 주소 끝이 숫자면 붙여 봐야 뜻이 없다. 그럴 때는 그냥 둔다.
            if tail and not tail[-1].isdigit():
                a["title"] = f'{a["title"]} ({tail[-1]})'
    return agg


def load_edges(pages):
    rows = json.loads((DATA / "edges.json").read_text())
    e = collections.Counter()
    ext = collections.Counter()  # (referrer 호스트, 도착 페이지)
    for r in rows:
        dst = norm_path(r["pagePath"])
        if dst not in pages:
            continue
        ref = r["pageReferrer"] or ""
        pv = int(r["screenPageViews"])
        m = re.match(r"https?://([^/?#]+)([^?#]*)", ref)
        if not m:
            continue
        host, path = m.group(1), norm_path(m.group(2) or "/")
        if host in ("merryyear.org", "www.merryyear.org"):
            if path in pages and path != dst:
                e[(path, dst)] += pv
        else:
            ext[(host, dst)] += pv
    return e, ext


def prune_isolated(pages, edges, ext):
    """어느 이동에도 걸리지 않은 페이지를 지운다.

    조회수는 있지만 들어온 길도 나간 길도 잡히지 않은 페이지가 116개 있었다.
    화면에서는 고리를 채우는 먼지로만 보이고, 흐름을 따라갈 때는 아무것도
    하지 않는다. 유입원이 보내는 도착 페이지와 결제로 잇는 다리는 남긴다.
    """
    keep = set()
    for a, b in edges:
        keep.add(a)
        keep.add(b)
    for _, d in ext:
        keep.add(d)
    for s in load_sources(pages):
        for pth, _ in s["landings"]:
            keep.add(pth)
    for (pth, _), _ in bridge_pages(pages).items():
        keep.add(pth)

    dropped = [pth for pth in pages if pth not in keep]
    for pth in dropped:
        del pages[pth]
    return dropped


# --------------------------------------------------------------------------- #
# 2. 배치
# --------------------------------------------------------------------------- #
def spring(xy, ei, ej, ew, anchor_xy, anchor_k, iters=420, k=None, clamp=None):
    """Fruchterman-Reingold 한 판. 전부 numpy로 돌린다.

    networkx의 spring_layout은 노드마다 파이썬 반복을 돌아 1,300개에서 몇 분씩
    걸린다. 여기서는 밀어내는 힘을 거리 행렬 한 번으로 계산한다.
    """
    n = len(xy)
    k = k or 1.0 / math.sqrt(n)
    temp = 0.16
    import sys, time
    t0 = time.time()
    for it in range(iters):
        if it % 60 == 0:
            print(f"  배치 {it}/{iters} {time.time()-t0:.1f}초", flush=True)
        # 서로 밀어내는 힘
        d = xy[:, None, :] - xy[None, :, :]
        dist2 = np.einsum("ijk,ijk->ij", d, d) + 1e-6
        np.fill_diagonal(dist2, 1.0)
        rep = (k * k / dist2)[:, :, None] * d
        disp = rep.sum(axis=1)

        # 이어진 데끼리 당기는 힘
        dv = xy[ei] - xy[ej]
        dl = np.sqrt(np.einsum("ij,ij->i", dv, dv)) + 1e-6
        att = (dv / dl[:, None]) * (dl * dl / k)[:, None] * ew[:, None]
        np.add.at(disp, ei, -att)
        np.add.at(disp, ej, att)

        # 카테고리 자리로 끌어당기는 힘. 덩어리가 뭉쳐 보이게 한다.
        disp += (anchor_xy - xy) * anchor_k[:, None]

        ln = np.sqrt(np.einsum("ij,ij->i", disp, disp)) + 1e-9
        step = np.minimum(ln, temp) / ln
        xy = xy + disp * step[:, None]
        if clamp:
            # 고리 밖으로 밀려나지 않게 매번 반지름을 눌러 넣는다
            rad = np.sqrt(np.einsum("ij,ij->i", xy, xy)) + 1e-9
            keep = np.clip(rad, clamp[0], clamp[1])
            xy = xy * (keep / rad)[:, None]
        temp = max(0.004, temp * 0.988)
    return xy


R_IN, R_OUT = 0.42, 1.00   # 콘텐츠 고리의 안팎 반지름
SECTOR_GAP = 0.05          # 카테고리 사이 틈(라디안)
MIN_SPAN = 0.24            # 카테고리 최소 폭(라디안). 약 14도
ANG_LIMIT = 0.045          # 스프링이 각도를 밀 수 있는 한계(라디안). 약 2.6도


def sector_seed(pages):
    """카테고리마다 부채꼴을 나눠 주고, 그 안을 고르게 채운다.

    순수 힘 기반 배치는 소식 페이지 928개가 한 덩어리로 뭉쳐 고리 안쪽에
    달라붙었다. 자리부터 고르게 잡아 두고 힘은 다듬는 데만 쓴다.
    """
    keys = list(pages)
    by_cat = collections.defaultdict(list)
    for p in keys:
        by_cat[pages[p]["cat"]].append(p)

    # 부채꼴 폭은 페이지 개수에 정비례한다. 어느 방향을 보아도 점 밀도가 같아진다.
    # 개수의 0.6제곱을 쓰던 때는 소식 928개가 폭 절반에 몰려 왼쪽만 촘촘했다.
    order = [c["key"] for c in CATS if c["key"] in by_cat and c["key"] != "home"]
    counts = {c: len(by_cat[c]) for c in order}
    free = 6.283185 - SECTOR_GAP * len(order)

    # 페이지가 적은 카테고리는 정비례로 두면 실처럼 얇아진다. 최소 폭을 먼저 떼어 준다.
    weight = {}
    rest, prop = free, set(order)
    while prop:
        tot = sum(counts[c] for c in prop) or 1
        small = [c for c in prop if rest * counts[c] / tot < MIN_SPAN]
        if not small:
            for c in prop:
                weight[c] = rest * counts[c] / tot
            break
        for c in small:
            weight[c] = MIN_SPAN
            prop.discard(c)
            rest -= MIN_SPAN
    total = 1.0

    seed = {}
    a0 = ANCHOR.get(order[0], 0.0) if order else 0.0
    cursor = a0
    spans = {}
    for c in order:
        w = weight[c]
        spans[c] = (cursor, w)
        members = sorted(by_cat[c], key=lambda p: -pages[p]["pv"])
        n = len(members)
        # 반지름 순서를 무작위로 섞는다. 규칙적으로 섞으면 나선 무늬가 생긴다.
        shuffled = list(range(n))
        random.Random(zlib.crc32(c.encode())).shuffle(shuffled)
        for i, p in enumerate(members):
            # 각도는 황금비로 흩어 부채꼴을 고르게 채우고,
            # 반지름은 순서를 섞어 조회수가 큰 페이지가 한 줄에 서지 않게 한다.
            ang = cursor + w * ((i * 0.6180339887) % 1.0)
            t = (shuffled[i] + 0.5) / n
            r = math.sqrt(R_IN ** 2 + t * (R_OUT ** 2 - R_IN ** 2))
            seed[p] = (r, ang)
        cursor += w + SECTOR_GAP

    for p in by_cat.get("home", []):
        seed[p] = (R_IN * 0.86, ANCHOR["home"])
    return seed, spans


FLOW_HOT_R = (0.50, 0.80)   # 결제로 이어지는 페이지를 세울 반지름 구간


def flow_seed(pages, hot, landings):
    """흐름 장면에서 쓸 배치. 주제별 부채꼴을 풀고 원 둘레 전체에 흩는다.

    결제로 이어지는 페이지가 '캠페인' 부채꼴 한 곳에 몰려 있어, 구슬이 늘
    같은 방향에서만 날아왔다. 다리를 놓은 페이지부터 원 둘레에 고르게 세우고
    도착 페이지, 나머지 순으로 그 사이를 채운다.
    """
    rank = []
    for p in pages:
        tier = 0 if p in hot else 1 if p in landings else 2
        rank.append((tier, -pages[p]["pv"], p))
    rank.sort()

    n = len(rank)
    # 반지름 순서를 섞는다. 순서대로 두면 나선 무늬가 생긴다.
    shuffled = list(range(n))
    random.Random(20260827).shuffle(shuffled)

    seed = {}
    for i, (tier, _, p) in enumerate(rank):
        # 황금비로 각도를 흩으면 앞에서 자른 어떤 토막도 원 둘레에 고르게 선다.
        # 다리를 놓은 페이지만 따로 보아도 사방에 흩어져 있게 된다.
        ang = ((i * 0.6180339887) % 1.0) * 6.283185
        t = (shuffled[i] + 0.5) / n
        if tier == 0:
            r = FLOW_HOT_R[0] + t * (FLOW_HOT_R[1] - FLOW_HOT_R[0])
        else:
            r = math.sqrt(R_IN ** 2 + t * (R_OUT ** 2 - R_IN ** 2))
        seed[p] = (r, ang)
    return seed, {}


def layout(pages, edges, seed_pair=None):
    keys = list(pages)
    kidx = {p: i for i, p in enumerate(keys)}
    n = len(keys)

    seed, spans = seed_pair if seed_pair is not None else sector_seed(pages)
    seed_ang = np.array([seed[p][1] for p in keys])
    xy = np.zeros((n, 2))
    anchor = np.zeros((n, 2))
    akv = np.zeros(n)
    for i, p in enumerate(keys):
        r, a = seed[p]
        xy[i] = (math.cos(a) * r, math.sin(a) * r)
        anchor[i] = xy[i]
        # 자기 자리로 돌아오려는 힘. 이게 있어야 고리 모양이 무너지지 않는다.
        akv[i] = 0.55

    pairs = [(kidx[a], kidx[b], w) for (a, b), w in edges.items() if a != b]
    ei = np.array([p[0] for p in pairs], dtype=np.int64)
    ej = np.array([p[1] for p in pairs], dtype=np.int64)
    ew = np.array([p[2] for p in pairs], dtype=float)
    ew = 0.04 + 0.14 * (np.log1p(ew) / np.log1p(ew.max()))

    # 짧게만 다듬는다. 이어진 페이지끼리 조금 당겨 붙어 결이 생긴다.
    # 반지름은 부채꼴 배치 그대로 두고, 각도만 조금 다듬는다.
    # 반지름까지 힘에 맡기면 밀어내는 힘이 이겨 안팎 경계로 다 몰린다.
    r0 = np.sqrt(np.einsum("ij,ij->i", xy, xy))
    moved = spring(xy, ei, ej, ew, anchor, akv, iters=45,
                   k=0.30 / math.sqrt(n), clamp=(R_IN, R_OUT))
    rm = np.sqrt(np.einsum("ij,ij->i", moved, moved)) + 1e-9
    xy = moved * (r0 / rm)[:, None]

    # 각도가 제자리에서 얼마나 벗어날 수 있는지 묶는다.
    # 묶지 않으면 서로 많이 이어진 소식 페이지들이 한 방향으로 몰려,
    # 자리를 고르게 잡아 둔 것이 스프링 한 판에 도로 무너진다.
    ang = np.arctan2(xy[:, 1], xy[:, 0])
    d = (ang - seed_ang + math.pi) % (2 * math.pi) - math.pi
    ang = seed_ang + np.clip(d, -ANG_LIMIT, ANG_LIMIT)
    rr = np.sqrt(np.einsum("ij,ij->i", xy, xy))
    rr = np.clip(rr, R_IN * 0.95, R_OUT * 1.06)

    out = {}
    for p, a, r in zip(keys, ang, rr):
        a = float((a + math.pi) % (2 * math.pi) - math.pi)
        out[p] = (math.cos(a) * float(r), math.sin(a) * float(r), a)
    return out, spans


# --------------------------------------------------------------------------- #
# 3. 유입원
# --------------------------------------------------------------------------- #
SRC_LABEL = {
    "kakaobank / banner": "카카오뱅크 배너",
    "kakaotaxi / banner": "카카오택시 배너",
    "beamin / banner": "배달의민족 배너",
    "daum / banner": "다음 배너",
    "cbs_app / banner": "CBS 앱 배너",
    "instagram / banner": "인스타그램 배너",
    "(direct) / (none)": "직접 유입",
    "google / organic": "구글 검색",
    "naver / organic": "네이버 검색",
    "naver / ppc": "네이버 검색 광고",
    "naver / cpc": "네이버 검색 광고",
    "l.instagram.com / referral": "인스타그램 링크",
    "m.search.naver.com / referral": "네이버 모바일 검색",
    "search.naver.com / referral": "네이버 검색 유입",
    "ig / paid": "인스타그램 광고",
    "fb / paid": "페이스북 광고",
    "an / paid": "메타 오디언스 광고",
    "(not set)": "확인되지 않음",
}


def load_sources(pages, keep=16):
    rows = json.loads((DATA / "landing_channel.json").read_text())
    tot = collections.Counter()
    land = collections.defaultdict(collections.Counter)
    chan = {}
    for r in rows:
        sm = r["sessionSourceMedium"]
        s = int(r["sessions"])
        tot[sm] += s
        chan[sm] = r["sessionDefaultChannelGroup"]
        lp = norm_path(r["landingPage"]) if r["landingPage"] not in ("(not set)", "") else None
        if lp and lp in pages:
            land[sm][lp] += s
    top = [sm for sm, _ in tot.most_common(keep)]
    return [
        {
            "sm": sm,
            "label": SRC_LABEL.get(sm, sm),
            "sessions": tot[sm],
            "channel": chan.get(sm, ""),
            "landings": land[sm].most_common(6),
        }
        for sm in top
    ]


# --------------------------------------------------------------------------- #
# 4. 결제 층
# --------------------------------------------------------------------------- #
def load_payment():
    rows = json.loads((DATA / "funnel_by_campaign.json").read_text())
    weights = collections.Counter()
    for r in rows:
        weights[r["customEvent:donation_name"]] += int(r["eventCount"])
    cmap = C.canonical_map(weights)

    per = collections.defaultdict(lambda: collections.Counter())
    rev = collections.Counter()
    for r in rows:
        rep = cmap.get(r["customEvent:donation_name"])
        if not rep:
            continue
        per[rep][r["eventName"]] += int(r["eventCount"])
        if r["eventName"] == "purchase":
            rev[rep] += float(r["eventValue"])

    camps = []
    for name, ev in per.items():
        if ev.get("purchase", 0) <= 0:
            continue
        camps.append({
            "name": name,
            "always": C.is_always_on(name),
            "bc": ev.get("begin_checkout", 0),
            "ds": ev.get("donation_start", 0),
            "api": ev.get("add_payment_info", 0),
            "pu": ev.get("purchase", 0),
            "rev": round(rev[name]),
        })
    camps.sort(key=lambda c: -c["rev"])

    totals = {}
    for key, label in FUNNEL:
        totals[key] = sum(int(r["eventCount"]) for r in rows if r["eventName"] == key)
    return camps, totals


def load_timeline(ftot):
    """하루씩 쌓이는 후원 건수와 모금액. 퍼널 앞 세 단계는 완료 분포로 나눈다.

    daily_totals.json 에는 후원 완료 건수와 모금액만 날짜별로 들어 있다.
    후원 페이지 진입, 후원 시작, 결제 정보 입력은 기간 총계만 있어서
    후원이 일어난 날의 비율대로 갈라 놓았다. 마지막 날 값은 총계와 맞는다.
    """
    rows = json.loads((DATA / "daily_totals.json").read_text())
    rows.sort(key=lambda r: r["date"])
    tot_pu = sum(int(r["ecommercePurchases"]) for r in rows) or 1

    keys = [k for k, _ in FUNNEL]
    out, cum_pu, cum_rev = [], 0, 0.0
    for r in rows:
        cum_pu += int(r["ecommercePurchases"])
        cum_rev += float(r["purchaseRevenue"])
        share = cum_pu / tot_pu
        out.append({
            "d": r["date"],
            "s": int(r["sessions"]),
            "v": round(cum_rev),
            "f": [round(ftot[k] * share) if k != "purchase" else cum_pu for k in keys],
        })
    return out


def bridge_pages(pages):
    """캠페인 페이지와 결제 층 캠페인을 잇는 열쇠."""
    rows = json.loads((DATA / "campaign_pages.json").read_text())
    weights = collections.Counter()
    for r in rows:
        weights[r["customEvent:donation_name"]] += int(r["eventCount"])
    cmap = C.canonical_map(weights)
    out = collections.Counter()
    for r in rows:
        rep = cmap.get(r["customEvent:donation_name"])
        p = norm_path(r["pagePath"])
        if rep and p in pages:
            out[(p, rep)] += int(r["eventCount"])
    return out


def ad_direct():
    """광고에서 결제 층으로 바로 들어온 몫. 세션 채널 구성으로 배분한 추정치."""
    rows = json.loads((DATA / "mrm_channel.json").read_text())
    per = collections.Counter()
    for r in rows:
        if r["hostName"] != "online.mrm.or.kr":
            continue
        per[r["sessionSourceMedium"]] += int(r["sessions"])
    return per


MIN_DEGREE = 2   # 오간 길이 이만큼은 걸려 있어야 정리 뒤에도 남는다


def keep_set(pages, edges, landings, bridged=()):
    """연출 뒷부분에 남길 페이지를 고른다.

    오간 길이 하나도 없거나 하나뿐인 페이지는 화면에서 먼지로만 보인다.
    빼고 나면 그 자리가 비어 남은 페이지를 더 넓게 펼칠 수 있다.
    밖에서 사람을 보내는 도착 페이지와 결제로 이어지는 페이지는
    길 수와 상관없이 남긴다. 다리를 놓은 페이지가 사라지면 흐름 장면에서
    다리 선이 빈자리에서 뻗어 나온다.
    """
    deg = collections.Counter()
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    keep = {p for p in pages if deg[p] >= MIN_DEGREE}
    keep |= set(landings)
    keep |= {p for p in pages if p in bridged}
    keep |= {p for p in pages if pages[p]["cat"] == "home"}
    return keep


# --------------------------------------------------------------------------- #
# 5. 조립
# --------------------------------------------------------------------------- #
def main():
    pages = load_pages()
    edges, ext = load_edges(pages)
    dropped = prune_isolated(pages, edges, ext)
    edges = {k: v for k, v in edges.items() if k[0] in pages and k[1] in pages}
    print(f"이어지지 않아 뺀 페이지 {len(dropped)}개")
    print(f"페이지 {len(pages)}개, 내부 간선 {len(edges)}개")

    pos, spans = layout(pages, edges)
    order = sorted(pages, key=lambda p: -pages[p]["pv"])
    pidx = {p: i for i, p in enumerate(order)}

    # 정리 뒤에 남을 페이지만 따로 배치한다. 화면에서는 앞의 자리에서
    # 뒤의 자리로 미끄러지듯 옮겨 가며 빈틈이 메워진다.
    srcs = load_sources(pages)
    landings = {pth for sc in srcs for pth, _ in sc["landings"]}
    bridges = bridge_pages(pages)
    page_of = {}
    for name_p, cnt in bridges.most_common():
        page_of.setdefault(name_p[1], (name_p[0], cnt))
    bridged = {v[0] for v in page_of.values()}
    keep = keep_set(pages, edges, landings, bridged)
    kept_pages = {pth: pages[pth] for pth in keep}
    kept_edges = {k: v for k, v in edges.items() if k[0] in keep and k[1] in keep}
    pos2, spans2 = layout(kept_pages, kept_edges)
    print(f"정리 뒤 남는 페이지 {len(keep)}개, 간선 {len(kept_edges)}개")

    # 흐름 장면에서 한 번 더 자리를 바꾼다. 결제로 이어지는 페이지가 한쪽에
    # 몰려 있으면 구슬이 늘 같은 방향에서만 날아온다.
    pos3, _ = layout(kept_pages, kept_edges,
                     flow_seed(kept_pages, bridged, landings & keep))
    print(f"흐름 배치: 다리를 놓은 페이지 {len(bridged)}개를 원 둘레에 고르게 세움")

    nodes = []
    for p in order:
        a = pages[p]
        x, y, _ = pos[p]
        n = {
            "p": p, "t": a["title"], "c": CAT_IDX[a["cat"]],
            "pv": a["pv"], "s": a["sess"],
            "e": round(a["eng"] / max(a["sess"], 1)),
            "x": round(x, 4), "y": round(y, 4),
        }
        if p in keep:
            x2, y2, _ = pos2[p]
            x3, y3, _ = pos3[p]
            n["k"] = 1
            n["x2"] = round(x2, 4)
            n["y2"] = round(y2, 4)
            n["x3"] = round(x3, 4)
            n["y3"] = round(y3, 4)
        else:
            n["k"] = 0
            n["x2"] = n["x"]
            n["y2"] = n["y"]
            n["x3"] = n["x"]
            n["y3"] = n["y"]
        nodes.append(n)

    cat_n = collections.Counter(pages[pth]["cat"] for pth in pages)
    cat_top = {}
    for pth in sorted(pages, key=lambda q: -pages[q]["pv"]):
        cat_top.setdefault(pages[pth]["cat"], pages[pth]["title"])

    elist = [[pidx[a], pidx[b], w] for (a, b), w in edges.items()]
    elist.sort(key=lambda e: -e[2])
    print(f"내보내는 간선 {len(elist)}개", flush=True)

    # 유입원을 바깥 고리에 놓는다. 각도는 그 유입원이 주로 보내는 페이지 쪽으로 두되,
    # 겹치지 않도록 원 둘레를 고르게 나눈 자리에 순서대로 맞춘다.
    want = []
    for si, s in enumerate(srcs):
        if s["landings"]:
            vx = sum(math.cos(pos[p][2]) * n for p, n in s["landings"])
            vy = sum(math.sin(pos[p][2]) * n for p, n in s["landings"])
            want.append((math.atan2(vy, vx) % 6.283185, si))
        else:
            want.append(((si / len(srcs)) * 6.283185, si))
    want.sort()
    step = 6.283185 / len(want)
    base = want[0][0] if want else 0.0
    angle_of = {si: base + i * step for i, (_, si) in enumerate(want)}

    src_out, src_edges = [], []
    for si, s in enumerate(srcs):
        ang = angle_of[si]
        src_out.append({
            "n": s["label"], "sm": s["sm"], "ch": s["channel"], "v": s["sessions"],
            "x": round(math.cos(ang) * 1.13, 4), "y": round(math.sin(ang) * 1.13, 4),
        })
        for p, n in s["landings"]:
            src_edges.append([si, pidx[p], n])

    camps, ftot = load_payment()
    ads = ad_direct()
    ad_total = sum(ads.values()) or 1
    src_by_sm = {s["sm"]: i for i, s in enumerate(src_out)}

    camp_out, camp_edges, ad_edges = [], [], []
    n_c = len(camps)
    for ci, c in enumerate(camps):
        hit = page_of.get(c["name"])
        if hit and hit[0] in pos:
            ang = pos[hit[0]][2]
        else:
            ang = (ci / n_c) * 6.283
        # 흐름 장면에서는 다시 흩어 놓은 다리 페이지 쪽을 바라보게 옮긴다.
        if hit and hit[0] in pos3:
            ang3 = pos3[hit[0]][2]
        else:
            ang3 = ((ci * 0.6180339887) % 1.0) * 6.283185
        r = 0.20 + 0.10 * ((ci * 7) % 5) / 4.0
        camp_out.append({
            "n": c["name"], "always": c["always"],
            "bc": c["bc"], "ds": c["ds"], "api": c["api"], "pu": c["pu"], "rev": c["rev"],
            "x": round(math.cos(ang) * r, 4), "y": round(math.sin(ang) * r, 4),
            "x3": round(math.cos(ang3) * r, 4), "y3": round(math.sin(ang3) * r, 4),
        })
        if hit:
            camp_edges.append([pidx[hit[0]], ci, hit[1]])
        # 광고 직행 추정: 결제 층 세션의 채널 구성을 캠페인 규모로 나눈다
        share = c["pu"] / max(sum(x["pu"] for x in camps), 1)
        for sm, sess in ads.most_common(6):
            si = src_by_sm.get(sm)
            if si is None or sm == "(direct) / (none)":
                continue
            w = sess * share
            if w >= 1:
                ad_edges.append([si, ci, round(w)])
    # 추정 경로는 화면을 덮지 않을 만큼만 남긴다
    ad_edges.sort(key=lambda e: -e[2])
    ad_edges = ad_edges[:44]

    payload = {
        "meta": {
            "source": "GA4 속성 493257809",
            "range": "2025.08.01 ~ 2026.08.24",
            "pages": len(nodes),
            "edges": len(elist),
            "pages_kept": len(keep),
            "edges_kept": len(kept_edges),
            "note": "결제 층은 online.mrm.or.kr, 콘텐츠 층은 merryyear.org",
        },
        "cats": [
            dict(c, n=cat_n.get(c["key"], 0), top=cat_top.get(c["key"], ""))
            for c in CATS
        ],
        "sectors": [
            {"c": CAT_IDX[k], "a": round(a + w / 2, 4), "w": round(w, 4)}
            for k, (a, w) in spans.items()
        ],
        "nodes": nodes,
        "edges": elist,
        "srcs": src_out,
        "srcEdges": src_edges,
        "camps": camp_out,
        "campEdges": camp_edges,
        "adEdges": ad_edges,
        "funnel": [{"k": k, "l": l, "v": ftot[k]} for k, l in FUNNEL],
        "timeline": load_timeline(ftot),
    }
    out = DATA / "graph.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"저장: {out} {out.stat().st_size/1024:.0f}KB")
    print(f"유입원 {len(src_out)}개, 결제 캠페인 {len(camp_out)}개, 다리 {len(camp_edges)}개, 직행 {len(ad_edges)}개")
    print("퍼널:", {f['l']: f['v'] for f in payload['funnel']})

    tpl = HERE / "graph_template.html"
    if tpl.exists():
        html = tpl.read_text(encoding="utf-8").replace(
            "/*__GRAPH_DATA__*/null",
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        )
        dest = HERE.parent / "웹구조그래프.html"
        dest.write_text(html, encoding="utf-8")
        print(f"저장: {dest} {dest.stat().st_size/1024:.0f}KB")


if __name__ == "__main__":
    main()
