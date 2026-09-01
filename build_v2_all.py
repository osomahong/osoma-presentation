"""52장 전부의 시각 안 후보.

`후보목록_시각안.md`에 적어 둔 안을 실제 판으로 만든 것이다. 장마다 재료가 다른 안을 셋씩 두고,
`후보비교_전장.html`에서 한 줄에 셋씩 놓고 견준다.

- 글은 원본에서 뽑아 그대로 옮긴다. 여기서 새 문장을 지어내지 않는다.
- 재료는 다섯 가지다. 실제 화면, 실제 자료와 수치, 손그림, 생성 이미지, 그림 없이 판만.
- 그림이나 화면이 필요한 안은 구획과 안내문만 먼저 넣어 두고, 준비되면 끼운다.

빌드: python3 build_ax.py --all
출력: 후보비교_전장.html
"""
import re

from build_ax_v2 import _fig_stack, _fig_fall
from build_v2_variants import _v4_shots, _v4_amp, _v40_domino, _v40_axis
from v2_parts import (band, cards, steps, step_rows, papers, points, asks, versus,
                      facts, flow, tools, columns, hours, qacards, embed, plain,
                      slot, img_prompt, shot_guide, data_guide)
from v2_sketch import wrap as sk
from v2_pick import pick_bar, pick_button, pick_memo, pick_panel
import v2_layouts as L
from v2_layouts import frame, side, two, top, grid

# ── 재단의 실제 기록 ──────────────────────────────────────────────
# 2025년 8월부터 2026년 8월 24일까지 13개월. 데이터재료_최근1년.md에서 가져왔다.
DONATE = [104, 61, 31, 41, 70, 34, 37, 30, 123, 31, 26, 67, 57]
SESSION = [38302, 274036, 6098, 5203, 10283, 5191, 4311, 69331, 20117, 5512, 4693, 4806, 3985]
MONTHS = ["25.08", "25.09", "25.10", "25.11", "25.12", "26.01", "26.02",
          "26.03", "26.04", "26.05", "26.06", "26.07", "26.08"]


def _pct(vals, top=92):
    hi = max(vals)
    return [v / hi * top for v in vals]


def _spark():
    """세션 흐름을 옅은 선으로. 큰 값이 화면을 다 먹지 않게 제곱근으로 눌렀다."""
    v = [x ** 0.5 for x in SESSION]
    hi, lo = max(v), min(v)
    return L.spark([12 + (x - lo) / (hi - lo) * 74 for x in v])


# ══ 되풀이해 쓰는 조각 ═════════════════════════════════════════════
def keep(html):
    """지금 판을 그대로 둔다."""
    return html


def _sub(p, b):
    """설명 아래에 카드 라벨 문장을 작게 붙인다. 두 문장을 모두 남긴다."""
    return f'{p}<span class="Lsub">{b}</span>' if b else p


def _num(i):
    return f"{i + 1:02d}"


def _screen(tag, desc, what, ratio=None, pinned=False):
    return slot(tag, desc, shot_guide(what), kind="SCREEN", ratio=ratio, pinned=pinned)


def _data(tag, desc, what, ratio=None, pinned=False):
    return slot(tag, desc, data_guide(what), kind="DATA", ratio=ratio, pinned=pinned)


def _image(tag, desc, scene, ratio=None, pinned=False):
    return slot(tag, desc, img_prompt(scene), kind="IMAGE", ratio=ratio, pinned=pinned)


# ══ 01 표지 ════════════════════════════════════════════════════════
_SIGNAL = r'<svg class="signal".*?</svg>'


def s01_a(h):
    h = re.sub(_SIGNAL, "", h, count=1, flags=re.S)
    return re.sub(r'<div class="mchips">.*?</div>\s*(?=</div>)', "", h, count=1, flags=re.S)


def s01_b(h):
    fig = _image("넣을 그림", "사람과 화면이 마주 본 넓은 장면을 뒤에 깔고 제목을 얹습니다.",
                 "A wide, quiet establishing scene. On the left an abstract human figure "
                 "sits at a simple desk seen in profile; on the right a large rounded screen panel "
                 "glows softly. Between them a single thin gradient line arcs both ways. "
                 "Horizontal composition, aspect ratio 16:9, subject in the lower half with a wide "
                 "empty band across the top so a title can sit over it.",
                 ratio="16/9", pinned=True)
    return re.sub(_SIGNAL, f'<div class="Lcovfig">{fig}</div>', h, count=1, flags=re.S)


def s01_c(h):
    h = re.sub(_SIGNAL, "", h, count=1, flags=re.S)
    return h.replace('<div class="fg">', _spark() + '<div class="fg">', 1)


# ══ 02 끝나면 할 수 있게 되는 것 셋 ════════════════════════════════
def s02_a(h):
    return frame(h, L.bignum(points(h)))


def s02_b(h):
    return frame(h, L.axis(points(h), "오늘", "끝난 뒤"))


def s02_c(h):
    it = points(h)
    return frame(h, two(sk("checkpaper", "확인란 세 줄이 있는 종이 한 장입니다. 끝나면 표를 칠 수 있는 것만 적었습니다."),
                        side(L.rows(it)), "narrow"))


# ══ 03 맡기는 범위 ════════════════════════════════════════════════
def s03_a(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, two(sk("band4", "가로 띠 하나를 네 구간으로 나누고, 구간마다 사람 몫과 AI 몫의 면적을 다르게 칠했습니다."),
                        side(L.rows(it))))


def s03_b(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    a = _screen("넣을 화면 1", "같은 일을 대화로 시킨 화면입니다.",
                "재단 업무 하나를 고르고, 그 일을 AI와 주고받으며 시킨 대화 화면을 갈무리합니다. "
                "질문과 답이 번갈아 이어진 부분을 씁니다.", ratio="22/9")
    b_ = _screen("넣을 화면 2", "같은 일을 위임으로 시킨 화면입니다.",
                 "같은 일을 이번에는 목적과 기준만 적어 한 번에 맡긴 화면을 갈무리합니다. "
                 "지시문 한 덩이와 그 결과가 함께 보이게 자릅니다.", ratio="22/9")
    return frame(h, top(grid([a, b_]), L.cols(it, 4)))


def s03_c(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, L.axis(it, "사람이 더 많이", "AI가 더 많이"))


# ══ 04 AI는 왜 내 말을 이렇게 잘 들을까요 ══════════════════════════
def s04_a(h):
    return _fig_stack(h, key="a4")


def s04_b(h):
    return _v4_shots(h)


def s04_c(h):
    return _v4_amp(h)


# ══ 05 내 마음에 든 결과 ══════════════════════════════════════════
def s05_a(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, L.pair(lt, rt, list(zip(ll, rl)), lr, rr))


def s05_b(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    body = L.pair(lt, rt, list(zip(ll, rl)), lr, rr)
    return frame(h, two(sk("pairview", "같은 문서를 두 사람이 볼 때, 한쪽에는 채워져 보이고 다른 쪽에는 빈 곳이 보입니다."),
                        side(body), "narrow"))


def s05_c(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    fig = _data("넣을 자료", "실제로 만든 산출물 하나에 만든 사람의 표시와 받은 사람의 표시를 겹칩니다.",
                "재단에서 실제로 만든 산출물 하나를 고릅니다. 보고서나 캠페인 문안이면 됩니다. "
                "만든 사람이 당연하게 여긴 곳과 받은 사람이 되물은 곳에 각각 다른 색으로 표시를 겹칩니다.",
                ratio="16/9")
    return frame(h, two(fig, side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr))))


# ══ 06 조직의 다섯 단계 ═══════════════════════════════════════════
def s06_a(h):
    return frame(h, L.stair(steps(h), here=1))


def s06_b(h):
    it = steps(h)
    aside = side(L.rows([(a, b, c) for a, b, c in it]))
    return frame(h, L.chart(_pct([18, 34, 24, 16, 8]), [1], [], aside))


def s06_c(h):
    return frame(h, two(sk("five", "단계마다 조직이 어떻게 달라지는지 작은 그림 다섯 개로 그렸습니다."),
                        side(L.rows(steps(h)))))


# ══ 07 좋은 AI가 있어도 멀어지는 이유 ══════════════════════════════
def s07_a(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    pts = [(f"막히는 곳 {i + 1:02d}", x, y) for i, (x, y) in enumerate(zip(ll, rl))][:3]
    return frame(h, L.axis(pts, "업무", "AI", cuts=tuple(range(len(pts)))))


def s07_b(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, two(sk("bridge", "두 곳이 끊긴 다리입니다. 업무와 AI 사이가 어디에서 끊기는지 보입니다."),
                        side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr)), "narrow"))


def s07_c(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    a = _screen("넣을 화면 1", "업무 자료를 넣지 못해 막힌 화면입니다.",
                "실제로 AI에 재단 자료를 넣으려다 막힌 화면을 갈무리합니다. "
                "파일 형식이나 용량, 접근 권한 때문에 멈춘 순간이면 됩니다.", ratio="22/9")
    b_ = _screen("넣을 화면 2", "답을 받고도 업무로 옮기지 못한 화면입니다.",
                 "답은 돌아왔지만 그대로 쓰지 못해 다시 손질해야 했던 화면을 갈무리합니다.",
                 ratio="22/9")
    return frame(h, top(grid([a, b_]), L.pair(lt, rt, list(zip(ll, rl)), lr, rr)))


# ══ 08 AI를 쓰면 바로 빨라질까요 ═══════════════════════════════════
def s08_a(h):
    return keep(h)


def s08_b(h):
    return frame(h, two(sk("twocurve", "곡선을 둘로 늘려, 도구만 들인 조직과 일하는 방식을 바꾼 조직을 겹쳤습니다."),
                        side(L.rows(points(h)))))


def s08_c(h):
    return frame(h, L.spans([
        ("느려지는 기간", 34, "", False, ""),
        ("빨라지는 기간", 92, "", True, ""),
    ], compact=True), L.rows(points(h)))


# ══ 09 재단 자료 읽히기 ═══════════════════════════════════════════
def s09_a(h):
    qa = qacards(h)
    a = _screen("넣을 화면 1", qa[0][0] if qa else "맥락 없이 물었을 때",
                "재단 자료를 넣지 않은 채 캠페인 문구를 써 달라고 물은 화면을 갈무리합니다.",
                ratio="22/9")
    b_ = _screen("넣을 화면 2", qa[1][0] if len(qa) > 1 else "자료를 읽힌 뒤 같은 질문",
                 "같은 질문을 재단 자료를 읽힌 뒤에 다시 물은 화면을 갈무리합니다. "
                 "두 화면은 같은 날 같은 도구에서 뽑아 조건을 맞춥니다.", ratio="22/9")
    return frame(h, top(grid([a, b_]), L.rows(points(h))))


def s09_b(h):
    qa = qacards(h)
    return frame(h, L.pair(qa[0][0], qa[1][0],
                           [(qa[0][1], qa[1][1]), (qa[0][2], qa[1][2])]),
                 L.rows(points(h)))


def s09_c(h):
    return frame(h, two(sk("readflow", "자료 더미가 들어가고 답이 달라져 나오는 흐름입니다."),
                        side(L.rows(points(h)))))


# ══ 10 네 가지 방식 예고 ══════════════════════════════════════════
def s10_a(h):
    it = cards(h)
    ss = [_screen(f"넣을 화면 {i+1}", plain(b),
                  f"뒤에 나올 {plain(b)} 화면을 작게 갈무리합니다. 예고편이라 크게 보이지 않아도 됩니다.",
                  ratio="4/3") for i, (a, b, c) in enumerate(it)]
    return frame(h, top(grid(ss, "g4"), L.rows([(_num(i), b, c) for i, (a, b, c) in enumerate(it)])))


def s10_b(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, L.axis(it, "질문 하나 더 던지기 어려움", "질문 하나 더 던지기 쉬움"))


def s10_c(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, two(sk("fan4", "같은 자료 한 묶음에서 네 방향으로 뻗어 나가는 그림입니다."),
                        side(L.rows(it))))


# ══ 11 엑셀 1,598줄 ═══════════════════════════════════════════════
def s11_a(h):
    return keep(h)


def s11_b(h):
    ifr, rows_, note = embed(h)
    fig = _data("넣을 자료", "표 전체를 한 화면에 아주 작게 축소해, 읽어야 할 양을 면적으로 보입니다.",
                "GA4에서 내려받은 표 전체를 한 화면에 담기도록 배율을 줄여 갈무리합니다. "
                "글자가 읽히지 않아도 됩니다. 읽어야 할 양이 면적으로 보이는 것이 목적입니다.",
                ratio="16/9")
    aside = side(L.rows([(a, b, "") for a, b in rows_]), f'<div class="Lbnote">{note}</div>')
    return frame(h, two(fig, aside))


def s11_c(h):
    ifr, rows_, note = embed(h)
    aside = side(L.rows([(f"항목 {i+1:02d}", a, b) for i, (a, b) in enumerate(rows_[1:])]),
                 f'<div class="Lbnote">{note}</div>')
    return frame(h, L.onenum(rows_[0][0], rows_[0][1], aside))


# ══ 12 답이 나오는 질문과 막히는 질문 ══════════════════════════════
def s12_a(h):
    cs = asks(h)
    return frame(h, L.marks([("ok" if k == "yes" else "no", qs) for k, _, qs in cs]))


def s12_b(h):
    cs = asks(h)
    qs = [q for _, _, arr in cs for q in arr]
    ss = [_screen(f"넣을 화면 {i + 1}", plain(q),
                  "이 질문을 실제로 표에서 돌린 결과를 작게 갈무리합니다. "
                  "막히는 질문은 막힌 화면을 그대로 씁니다.", ratio="4/3")
          for i, (q, d) in enumerate(qs[:4])]
    return frame(h, top(grid(ss, "g4"),
                        L.marks([("ok" if k == "yes" else "no", arr[:2]) for k, _, arr in cs])))


def s12_c(h):
    cs = asks(h)
    return frame(h, two(sk("sieve", "질문이 표를 통과하거나 튕겨 나오는 그림입니다."),
                        side(L.marks([("ok" if k == "yes" else "no", arr[:2]) for k, _, arr in cs])),
                        "narrow"))


# ══ 13 대시보드 ═══════════════════════════════════════════════════
def s13_a(h):
    return keep(h)


def s13_b(h):
    ifr, rows_, note = embed(h)
    fig = _screen("넣을 화면", "재단이 아침마다 여는 화면입니다.",
                  "재단에서 실제로 매일 여는 보고 화면을 갈무리합니다. "
                  "숫자가 읽히도록 배율을 키우고 기간 표시가 함께 보이게 자릅니다.", ratio="16/9")
    aside = side(L.rows([(a, b, "") for a, b in rows_]), f'<div class="Lbnote">{note}</div>')
    return frame(h, two(fig, aside))


def s13_c(h):
    ifr, rows_, note = embed(h)
    qs = [(a, b, "") for a, b in rows_]
    return frame(h, two(L.full(ifr), side(L.rows(qs), f'<div class="Lbnote">{note}</div>'), "wide"))


# ══ 14 대시보드도 담을 수 없는 질문 ════════════════════════════════
def s14_a(h):
    cs = asks(h)
    ins, outs = cs[0][2], cs[1][2]
    fig = _screen("넣을 화면", "대시보드 화면을 가운데 놓습니다.",
                  "13장에서 쓴 대시보드 화면을 같은 배율로 다시 갈무리합니다. "
                  "화면 안에 답이 있는 질문과 없는 질문을 나중에 양옆에 붙입니다.", ratio="16/9")
    return frame(h, two(fig, side(L.marks([("ok", ins[:2]), ("no", outs[:2])]))))


def s14_b(h):
    cs = asks(h)
    return frame(h, L.screen_split(cs[0][2], cs[1][2], cs[0][1], cs[1][1]))


def s14_c(h):
    cs = asks(h)
    return frame(h, two(sk("pushout", "미리 골라 둔 화면 밖으로 질문이 밀려나는 그림입니다."),
                        side(L.marks([("ok", cs[0][2][:2]), ("no", cs[1][2][:2])])), "narrow"))


# ══ 15 자연어 질의 ════════════════════════════════════════════════
def s15_a(h):
    return keep(h)


def s15_b(h):
    ifr, rows_, note = embed(h)
    fig = _screen("넣을 화면", "실제 도구에 재단 자료를 읽히고 물은 화면입니다.",
                  "재단 자료를 읽힌 뒤 지표 이름을 모르는 채 말로 물은 화면을 갈무리합니다. "
                  "답과 근거 표가 함께 보이게 자릅니다.", ratio="22/9")
    aside = side(L.rows([(a, b, "") for a, b in rows_]), f'<div class="Lbnote">{note}</div>')
    return frame(h, top(fig, aside))


def s15_c(h):
    ifr, rows_, note = embed(h)
    up = ("답", L.full(ifr))
    dn = ("근거 표", "<ul>" + "".join(f"<li>{a} {b}</li>" for a, b in rows_) + "</ul>")
    return frame(h, L.updown(up, dn, hot_b=False, big=True),
                 f'<div class="Lbnote">{note}</div>')


# ══ 16 화면을 만드는 대신 질문을 이어감 ════════════════════════════
def s16_a(h):
    fl, fs = flow(h), facts(h)
    return frame(h, L.bars([
        ("화면을 만들면", [(7, "", "m"), (1, "", "g")], ""),
        ("질문을 이어가면", [(1, "", "m"), (7, "", "g")], ""),
    ]), L.cols([(a, b, c) for a, b, c in fl], 4, plain=True))


def s16_b(h):
    fl = flow(h)
    fig = _screen("넣을 화면", "질문을 이어 던진 대화 한 판입니다.",
                  "같은 자료를 두고 네 번 이어 물은 대화를 한 판으로 갈무리합니다. "
                  "되묻는 대목이 보이도록 자릅니다.", ratio="22/9")
    return frame(h, top(fig, L.cols([(a, b, c) for a, b, c in fl], 4, plain=True)))


def s16_c(h):
    fl = flow(h)
    return frame(h, two(sk("twopath", "화면을 짓는 길과 질문을 잇는 길, 두 가지입니다."),
                        side(L.rows(fl))))


# ══ 17 판단까지 맡길 수는 없음 ════════════════════════════════════
def s17_a(h):
    cs = asks(h)
    fig = _screen("넣을 화면", "근거 표가 붙은 답 화면입니다.",
                  "15장에서 쓴 화면을 그대로 다시 갈무리합니다. "
                  "사람이 확인해야 할 숫자에 나중에 표시를 겹칩니다.", ratio="16/9")
    return frame(h, two(fig, side(L.marks([("ok", cs[0][2][:2]), ("no", cs[1][2][:2])]))))


def s17_b(h):
    cs = asks(h)
    lb = "".join(f'<li><b>{q}</b><span class="Lsub">{d}</span></li>' for q, d in cs[0][2])
    rb = "".join(f'<li><b>{q}</b><span class="Lsub">{d}</span></li>' for q, d in cs[1][2])
    return frame(h, L.tone(cs[0][1], cs[1][1], f"<ul>{lb}</ul>", f"<ul>{rb}</ul>"))


def s17_c(h):
    cs = asks(h)
    return frame(h, two(sk("stopline", "답까지는 이어지고 결정 앞에서 멈추는 선입니다."),
                        side(L.marks([("ok", cs[0][2][:2]), ("no", cs[1][2][:2])])), "narrow"))


# ══ 18 웹 구조 지도 ═══════════════════════════════════════════════
def s18_a(h):
    return keep(h)


def s18_b(h):
    ifr, rows_, note = embed(h)
    fig = _screen("넣을 화면", "지도에서 점 하나를 눌러 나온 상세입니다.",
                  "구조 지도를 띄우고 점 하나를 눌러 상세가 열린 화면을 갈무리합니다. "
                  "지도와 상세가 한 화면에 함께 보이게 자릅니다.", ratio="16/9")
    aside = side(L.rows([(a, b, "") for a, b in rows_]), f'<div class="Lbnote">{note}</div>')
    return frame(h, two(fig, aside))


def s18_c(h):
    ifr, rows_, note = embed(h)
    return frame(h, L.full(ifr))


# ══ 19 캠페인 레이스 ══════════════════════════════════════════════
def s19_a(h):
    return keep(h)


def s19_b(h):
    ifr, rows_, note = embed(h)
    fig = _data("넣을 그림", "레이스가 끝난 순간의 순위입니다.",
                "캠페인 레이스를 끝까지 재생한 뒤 마지막 순위가 보이는 화면을 갈무리합니다. "
                "1위부터 5위까지 이름과 건수가 읽히게 배율을 키웁니다.", ratio="16/9")
    aside = side(L.rows([(a, b, "") for a, b in rows_]), f'<div class="Lbnote">{note}</div>')
    return frame(h, two(fig, aside))


def s19_c(h):
    ifr, rows_, note = embed(h)
    it = [(MONTHS[i], f"{DONATE[i]}건", "") for i in (0, 4, 8, 11, 12)]
    return frame(h, L.axis(it, "2025년 8월", "2026년 8월"),
                 L.cols([(a, b, "") for a, b in rows_], 3, plain=True),
                 f'<div class="Lbnote">{note}</div>')


# ══ 20 사람과 AI가 같은 맥락을 공유 ════════════════════════════════
def s20_a(h):
    cs = asks(h)
    fig = _screen("넣을 화면", "18장의 구조 지도를 가운데 둡니다.",
                  "구조 지도를 띄운 화면을 갈무리합니다. 사람의 질문과 AI의 답을 나중에 양옆에 붙입니다.",
                  ratio="16/9")
    return frame(h, two(fig, side(L.marks([("ok", cs[0][2][:2]), ("no", cs[1][2][:2])]))))


def s20_b(h):
    cs = asks(h)
    return frame(h, two(sk("faceoff", "같은 그림을 사이에 두고 사람과 AI가 마주 보는 모습입니다."),
                        side(L.marks([("ok", cs[0][2][:2]), ("no", cs[1][2][:2])])), "narrow"))


def s20_c(h):
    cs = asks(h)
    lq = "<br>".join(q for q, d in cs[0][2])
    rq = "<br>".join(q for q, d in cs[1][2])
    return frame(h, L.arrows((cs[0][1], lq), ("같은 기준", cs[0][2][0][1]), (cs[1][1], rq)))


# ══ 21 전문성을 문서로 옮김 ═══════════════════════════════════════
def s21_a(h):
    return frame(h, L.axis(steps(h), "머릿속", "다른 담당자"))


def s21_b(h):
    fig = _data("넣을 자료", "실제로 남긴 문서입니다. 조직 이름은 가립니다.",
                "다른 조직이 전문성을 옮겨 적은 문서를 한 장 갈무리합니다. "
                "조직 이름과 담당자 이름은 가리고 항목의 짜임만 보이게 합니다.", ratio="16/9")
    return frame(h, two(fig, side(L.rows(steps(h)))))


def s21_c(h):
    return frame(h, two(sk("spread", "한 사람 머리에서 나온 것이 여러 사람에게 닿는 그림입니다."),
                        side(L.rows(steps(h)))))


# ══ 22 AI의 평균과 우리의 기준 ════════════════════════════════════
def s22_a(h):
    pts = points(h)
    aside = side(L.rows(pts))
    hi = max(DONATE)
    lines = [("avg", 55 / hi * 92, "세상의 평균"), ("ours", 104 / hi * 92, "재단의 기준")]
    return frame(h, L.chart(_pct(DONATE), [8], lines, aside, ticks=MONTHS))


def s22_b(h):
    qa = qacards(h)
    fig = _screen("넣을 화면", qa[0][0] if qa else "AI가 평균으로 판단한 답",
                  "재단 자료 없이 물었을 때 평균적인 답이 돌아온 화면을 갈무리합니다. "
                  "질문과 답이 한 화면에 보이게 자릅니다.", ratio="22/9")
    return frame(h, top(fig, L.rows(points(h))))


def s22_c(h):
    qa = qacards(h)
    return frame(h, L.pair(qa[0][0], qa[1][0],
                           [(qa[0][1], qa[1][1]), (qa[0][2], qa[1][2])]),
                 L.rows(points(h)))


# ══ 23 생산은 늘고 이해는 줄어듦 ══════════════════════════════════
def s23_a(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, two(sk("gapcurve", "만든 양과 읽은 양 두 곡선이 시간이 갈수록 벌어집니다."),
                        side(L.rows(it))))


def s23_b(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, L.spans([
        ("만든 분량", 96, "", True, ""),
        ("읽은 분량", 38, "", False, ""),
    ], compact=True), L.rows(it))


def s23_c(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    fig = _image("넣을 그림", "쌓이는 종이와 줄어드는 읽는 시간입니다.",
                 "A wide horizontal scene. On the left, rounded sheets of paper stack higher and higher "
                 "in a warm orange to coral gradient, overflowing beyond the frame. "
                 "On the right, a thin violet arc shrinks to a short stub, and one small abstract figure "
                 "stands beside it looking up at the stack. "
                 "Aspect ratio 22:9, action along the lower two thirds with wide empty space above.",
                 ratio="22/9")
    return frame(h, top(fig, L.rows(it)))


# ══ 24 되짚을 수 있는 여섯 단계 ═══════════════════════════════════
def s24_a(h):
    return frame(h, L.fold(steps(h), per=3))


def s24_b(h):
    return frame(h, two(sk("climbback", "결론에서 원본까지 거슬러 올라가는 선 하나입니다."),
                        side(L.rows(steps(h)))))


def s24_c(h):
    a = _screen("넣을 화면 1", "근거 표가 붙은 답 화면입니다.",
                "답과 근거 표가 함께 보이는 화면을 갈무리합니다. 어느 줄을 보고 답했는지가 읽혀야 합니다.",
                ratio="22/9")
    b_ = _screen("넣을 화면 2", "근거에서 원본으로 간 화면입니다.",
                 "근거 표의 한 줄을 눌러 원본 자료로 옮겨 간 화면을 갈무리합니다. "
                 "같은 숫자가 양쪽에 보이게 자릅니다.", ratio="22/9")
    return frame(h, top(grid([a, b_]), L.fold(steps(h)[:3], per=3)))


# ══ 25 검수는 다른 AI에게 ═════════════════════════════════════════
def s25_a(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    a = _screen("넣을 화면 1", "만든 도구에 그대로 검수시킨 화면입니다.",
                "결과를 만든 도구에 같은 결과를 검수시킨 화면을 갈무리합니다.", ratio="22/9")
    b_ = _screen("넣을 화면 2", "다른 도구에 검수시킨 화면입니다.",
                 "같은 결과를 다른 도구에 넣어 검수시킨 화면을 갈무리합니다. "
                 "두 화면은 같은 날 같은 결과물로 뽑아 조건을 맞춥니다.", ratio="22/9")
    return frame(h, top(grid([a, b_]), L.pair(lt, rt, list(zip(ll, rl)), lr, rr)))


def s25_b(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, L.arrows((lt, ll[0] if ll else ""), ("결과물 하나", lr),
                             (rt, rl[0] if rl else "")),
                 L.pair("", "", list(zip(ll[1:], rl[1:]))))


def s25_c(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, two(sk("blindspot", "자기 글을 자기가 읽을 때 보이지 않는 곳입니다."),
                        side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr)), "narrow"))


# ══ 26 규칙 파일 ══════════════════════════════════════════════════
def s26_a(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    fig = _data("넣을 자료", "실제 규칙 파일입니다.",
                "재단과 정한 규칙 파일을 그대로 갈무리합니다. 항목 이름과 짜임이 읽히게 합니다. "
                "진행노트에 예시 문안을 재단과 정한 뒤 고친다고 적어 두었으니, 그때 실제 파일로 바꿉니다.",
                ratio="22/9")
    return frame(h, top(fig, L.pair(lt, rt, list(zip(ll, rl)), lr, rr)))


def s26_b(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, L.pair(lt, rt, list(zip(ll, rl)), lr, rr))


def s26_c(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, two(sk("harden", "말로 하던 것이 글로 굳는 그림입니다."),
                        side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr)), "narrow"))


# ══ 27 기록을 모으면 지식이 되나 ══════════════════════════════════
def s27_a(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, L.spans([
        (lt, 96, lr, False, ""),
        (rt, 30, rr, True, ""),
    ], compact=True), L.pair("", "", list(zip(ll, rl))))


def s27_b(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, two(sk("sieve", "체 하나를 지나 남는 것입니다."),
                        side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr)), "narrow"))


def s27_c(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    fig = _data("넣을 자료", "실제로 모은 기록과 그중 남긴 것입니다.",
                "재단에서 실제로 모은 기록 묶음과 그중 다시 쓰인 것을 나란히 갈무리합니다. "
                "남긴 쪽의 양이 훨씬 적다는 것이 보여야 합니다.", ratio="22/9")
    return frame(h, top(fig, L.pair(lt, rt, list(zip(ll, rl)), lr, rr)))


# ══ 28 더 적어야 할 여섯 가지 ═════════════════════════════════════
def s28_a(h):
    fig = _data("넣을 자료", "규칙 파일 안에서 여섯 항목이 각각 어디에 적히는지 표시를 겹칩니다.",
                "26장에서 쓴 규칙 파일을 그대로 다시 갈무리합니다. "
                "여섯 항목이 파일 어느 자리에 들어가는지 나중에 표시를 겹칩니다.", ratio="16/9")
    return frame(h, two(fig, side(L.rows(tools(h)))))


def s28_b(h):
    return frame(h, L.fold(tools(h), per=3))


def s28_c(h):
    return frame(h, two(sk("harden", "문장 하나만 복사했을 때 빠지는 것들입니다."),
                        side(L.rows(tools(h))), "narrow"))


# ══ 29 AI가 물어보게 하는 지시문 ══════════════════════════════════
def s29_a(h):
    fig = _screen("넣을 화면", "시연 전에 한 번 돌려 보기로 한 그 대화입니다.",
                  "AI가 먼저 되묻게 하는 지시문을 넣고 실제로 돌린 대화를 갈무리합니다. "
                  "지시문과 돌아온 질문 목록이 한 화면에 보이게 자릅니다.", ratio="22/9")
    return frame(h, top(fig, L.rows(points(h))))


def s29_b(h):
    pts = points(h)
    up = ("지시문", f"<h4>{pts[0][1]}</h4><p>{pts[0][2]}</p>")
    dn = ("돌아온 질문", "<ul>" + "".join(f"<li>{b} {c}</li>" for a, b, c in pts[1:]) + "</ul>")
    return frame(h, L.updown(up, dn))


def s29_c(h):
    return frame(h, two(sk("faceoff", "묻는 쪽과 답하는 쪽이 뒤바뀌는 그림입니다."),
                        side(L.rows(points(h))), "narrow"))


# ══ 30 공용 기억 ══════════════════════════════════════════════════
def s30_a(h):
    st = steps(h)
    n = len(st)
    return frame(h, L.twoline([
        ("한 사람이 걸은 길", [("", True) for _ in st]),
        ("다음 사람이 시작하는 지점", [("", i >= n - 2) for i in range(n)]),
    ], compact=True), L.rows(st))


def s30_b(h):
    return frame(h, two(sk("standshift", "같은 곳에서 두 번 넘어지지 않는 그림입니다."),
                        side(L.rows(steps(h)))))


def s30_c(h):
    fig = _data("넣을 자료", "실제로 남긴 시행착오 기록입니다.",
                "재단에서 한 번 막혔던 일과 그 뒤에 남긴 기록을 나란히 갈무리합니다.", ratio="16/9")
    return frame(h, two(fig, side(L.rows(steps(h)))))


# ══ 31 안내 문자 발송 ═════════════════════════════════════════════
def s31_a(h):
    rows_ = step_rows(h)
    (la, sa), (lb, sb) = rows_[0], rows_[1]
    pairs = []
    for i in range(max(len(sa), len(sb))):
        left = f"<b>{sa[i][0]}</b>&ensp;{sa[i][1]}" if i < len(sa) else ""
        right = f"{sb[i][1]}&ensp;<b>{sb[i][0]}</b>" if i < len(sb) else ""
        pairs.append((left, right))
    return frame(h, L.pair(plain(la), plain(lb), pairs))


def s31_b(h):
    rows_ = step_rows(h)
    fig = _data("넣을 자료", "재단의 실제 발송 절차 문서입니다.",
                "안내 문자를 보낼 때 실제로 밟는 순서가 적힌 문서를 갈무리합니다. "
                "진행노트에 실제 순서를 확인한 뒤 문안을 바꾼다고 적어 두었습니다.", ratio="16/9")
    return frame(h, two(fig, side(L.rows(rows_[1][1]))))


def s31_c(h):
    rows_ = step_rows(h)
    return frame(h, two(sk("standshift", "사람이 서 있던 지점이 앞뒤 두 곳으로 옮겨 가는 그림입니다."),
                        side(L.rows(rows_[1][1]))))


# ══ 32 시키는 사람의 세 능력 ══════════════════════════════════════
def s32_a(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, L.axis(it, "일을 시작할 때", "일을 끝낼 때"))


def s32_b(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, two(sk("three_act", "실행이 넘어간 뒤 남는 세 가지입니다."),
                        side(L.rows(it))))


def s32_c(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    fig = _image("넣을 그림", "나누고 바로잡고 잇는 세 동작입니다.",
                 "Three abstract gestures side by side on one horizontal band. "
                 "First, a single rounded block splits into three smaller blocks. "
                 "Second, a tilted block is nudged back upright by a thin arc. "
                 "Third, two separated blocks are joined by a short bridging stroke. "
                 "Each gesture carries a different gradient from the palette. "
                 "Aspect ratio 2:1, evenly spaced with wide empty margins.", ratio="2/1")
    return frame(h, two(fig, side(L.rows(it))))


# ══ 33 어떤 업무 ══════════════════════════════════════════════════
def s33_a(h):
    lh, rh, rows_ = versus(h)
    return frame(h, two(sk("twinframe", "도구를 하나 더 얹은 그림과 일을 다시 그린 그림입니다."),
                        side(L.versus_rows(lh, rh, rows_)), "narrow"))


def s33_b(h):
    lh, rh, rows_ = versus(h)
    return frame(h, L.versus_rows(lh, rh, rows_))


def s33_c(h):
    lh, rh, rows_ = versus(h)
    fig = _data("넣을 자료", "재단 업무 하나를 골라 지금 흐름과 다시 그린 흐름을 나란히 놓습니다.",
                "재단 업무 하나를 골라 지금 밟는 순서를 적고, 그 옆에 다시 그린 순서를 적습니다. "
                "두 흐름의 단계 수가 한눈에 견주어져야 합니다.", ratio="16/9")
    return frame(h, two(fig, side(L.versus_rows(lh, rh, rows_))))


# ══ 34 사는 것과 잇는 것 ══════════════════════════════════════════
def s34_a(h):
    lh, rh, rows_ = versus(h)
    fig = _data("넣을 자료", "재단이 쓰는 도구를 실제로 적고 그 사이를 잇는 선을 그립니다.",
                "재단이 지금 쓰는 도구 이름을 모두 적고, 자료가 오가는 곳끼리 선으로 잇습니다. "
                "이어지지 않은 도구가 어디인지 보여야 합니다.", ratio="16/9")
    return frame(h, two(fig, side(L.versus_rows(lh, rh, rows_))))


def s34_b(h):
    lh, rh, rows_ = versus(h)
    return frame(h, two(sk("island", "따로 떨어진 섬 하나와 이어 붙인 다리입니다."),
                        side(L.versus_rows(lh, rh, rows_)), "narrow"))


def s34_c(h):
    lh, rh, rows_ = versus(h)
    return frame(h, L.versus_rows(lh, rh, rows_))


# ══ 35 취향과 기준 ════════════════════════════════════════════════
def s35_a(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, L.tone(lt, rt,
                           "<ul>" + "".join(f"<li>{x}</li>" for x in ll) + f"</ul><p>{lr}</p>",
                           "<ul>" + "".join(f"<li>{x}</li>" for x in rl) + f"</ul><p>{rr}</p>"))


def s35_b(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, two(sk("meet", "서로 다른 길이 한 지점에서 만나는 그림입니다."),
                        side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr)), "narrow"))


def s35_c(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    fig = _data("넣을 자료", "재단 안에서 실제로 달라도 됐던 것과 같아야 했던 것입니다.",
                "재단에서 담당자마다 방식이 달라도 문제가 없었던 일과, 달라서 문제가 됐던 일을 "
                "각각 적어 나란히 놓습니다.", ratio="16/9")
    return frame(h, two(fig, side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr))))


# ══ 36 만들지 않을 것 ═════════════════════════════════════════════
def s36_a(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, L.spans([
        (lt, 96, lr, False, ""),
        (rt, 34, rr, True, ""),
    ], compact=True), L.pair("", "", list(zip(ll, rl))))


def s36_b(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, two(sk("pick", "넘치게 쌓인 것에서 몇 개만 골라 내는 그림입니다."),
                        side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr)), "narrow"))


def s36_c(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    fig = _image("넣을 그림", "비용이 사라진 자리에 남는 선택입니다.",
                 "On the left, a dense crowd of small rounded blocks fills the frame in pale grey, "
                 "suggesting everything that could be made. "
                 "Toward the right the crowd thins out until only three blocks remain, "
                 "each filled with a distinct gradient from the palette. "
                 "A single thin ink line traces the narrowing. "
                 "Aspect ratio 2:1 with wide empty margins.", ratio="2/1")
    return frame(h, two(fig, side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr))))


# ══ 37 먼저 맡길 일 네 조건 ═══════════════════════════════════════
def s37_a(h):
    it = cards(h)
    head = ["재단 업무"] + [f'{b}<span class="Lsub">{c}</span>' for a, b, c in it]
    body = [[f"업무 {i + 1}"] + ['<span class="maybe">&#9675;</span>'] * len(it) for i in range(4)]
    return frame(h, L.table(head, body),
                 '<div class="Lbnote">시연에 올릴 업무를 재단과 정할 때 이 표를 그대로 씁니다.</div>')


def s37_b(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, L.overlap(it))


def s37_c(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, two(sk("funnel", "조건을 하나씩 통과하며 좁아지는 통로입니다."),
                        side(L.rows(it))))


# ══ 38 검수 기준 세 모양 ══════════════════════════════════════════
def s38_a(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, L.doc_marks(it))


def s38_b(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    fig = _screen("넣을 화면", "실제 결과물에 세 방식의 검수 표시를 얹은 화면입니다.",
                  "재단에서 실제로 만든 결과물 하나를 띄우고, 세 가지 검수 방식이 각각 어디를 보는지 "
                  "다른 색으로 표시를 겹친 화면을 갈무리합니다.", ratio="16/9")
    return frame(h, two(fig, side(L.rows(it))))


def s38_c(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, two(sk("cut3", "같은 것을 다르게 자르는 세 가지입니다."),
                        side(L.rows(it))))


# ══ 39 좋은 답과 좋은 결정 ════════════════════════════════════════
def s39_a(h):
    lh, rh, rows_ = versus(h)
    return frame(h, two(sk("converge", "답은 한 곳으로 모이고 결정은 여러 곳으로 뻗습니다."),
                        side(L.versus_rows(lh, rh, rows_)), "narrow"))


def s39_b(h):
    lh, rh, rows_ = versus(h)
    return frame(h, L.versus_rows(lh, rh, rows_))


def s39_c(h):
    lh, rh, rows_ = versus(h)
    fig = _image("넣을 그림", "빠른 답과 느린 결정입니다.",
                 "Left half: several thin gradient lines rush inward and converge into one sharp point, "
                 "drawn with quick straight strokes. "
                 "Right half: from a single point, four slow curving lines spread outward and end unresolved, "
                 "each in a different palette colour, with wider spacing between them. "
                 "A thin vertical pale line separates the halves. "
                 "Aspect ratio 2:1 with generous empty margins.", ratio="2/1")
    return frame(h, two(fig, side(L.versus_rows(lh, rh, rows_))))


# ══ 40 신뢰의 붕괴 ════════════════════════════════════════════════
def s40_a(h):
    return _fig_fall(h, key="a40")


def s40_b(h):
    return _v40_domino(h)


def s40_c(h):
    return _v40_axis(h)


# ══ 41 공익 원칙 일곱 ═════════════════════════════════════════════
def s41_a(h):
    fs = facts(h)
    seven = [(a, b, c) for a, b, c in fs if b]
    last = [(a, b, c) for a, b, c in fs if not b]
    body = L.fold(seven, per=4)
    tail = f'<div class="Lbnote">{last[0][2]}</div>' if last else ""
    return frame(h, body, tail)


def s41_b(h):
    fs = facts(h)
    seven = [(a, b, c) for a, b, c in fs if b]
    return frame(h, two(sk("sevenman", "숫자 뒤에 사람이 있는 그림입니다."),
                        side(L.rows(seven)), "narrow"))


def s41_c(h):
    fs = facts(h)
    seven = [(a, b, c) for a, b, c in fs if b]
    fig = _data("넣을 자료", "재단의 실제 개인정보 처리 문구를 한 줄 인용합니다.",
                "재단 홈페이지의 개인정보 처리방침에서 수집 목적과 이용 범위를 밝힌 문장을 한 줄 고릅니다. "
                "원문 그대로 인용하고 출처 위치를 함께 적습니다.", ratio="22/9")
    return frame(h, top(fig, L.fold(seven[:4], per=4)))


# ══ 42 단순한 규칙 셋 ═════════════════════════════════════════════
def s42_a(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, L.spans([
        (lt, 96, lr, False, ""),
        (rt, 42, rr, True, ""),
    ], compact=True), L.pair("", "", list(zip(ll, rl))))


def s42_b(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    fig = _data("넣을 자료", "매일 확인하는 실제 확인표입니다.",
                "재단에서 실제로 쓰는 확인표를 갈무리합니다. 항목 수가 적다는 것이 보여야 합니다.",
                ratio="22/9")
    return frame(h, top(fig, L.pair(lt, rt, list(zip(ll, rl)), lr, rr)))


def s42_c(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, two(sk("fold7", "일곱 개가 셋으로 접히는 그림입니다."),
                        side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr)), "narrow"))


# ══ 43 누가 끌고 갈지 ═════════════════════════════════════════════
def s43_a(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, L.axis(it, "기술 쪽", "현장 쪽"))


def s43_b(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, two(sk("carry", "두 세계 사이에서 말을 옮기는 사람입니다."),
                        side(L.rows(it)), "narrow"))


def s43_c(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    fig = _data("넣을 자료", "재단 안에서 그 역할에 가까운 담당자의 일입니다.",
                "재단에서 기술과 현장 사이를 이미 잇고 있는 담당자를 한 명 고르고, "
                "그 사람이 하루에 하는 일을 한 줄로 적습니다. 이름은 적지 않습니다.", ratio="16/9")
    return frame(h, two(fig, side(L.rows(it))))


# ══ 44 90일 ═══════════════════════════════════════════════════════
def s44_a(h):
    cs = columns(h)
    it = [(a, b, "<br>".join(f"{n} {t}" for n, t in items)) for a, b, items in cs]
    return frame(h, L.axis(it, "시작", "90일"))


def s44_b(h):
    cs = columns(h)
    fig = _data("넣을 자료", "재단 일정에 맞춘 실제 날짜입니다.",
                "재단의 연간 일정표를 보고 30일과 60일과 90일이 실제로 어느 달에 걸리는지 적습니다. "
                "연말 캠페인처럼 손이 바쁜 기간과 겹치는지 함께 표시합니다.", ratio="22/9")
    body = L.cols([(a, b, "<br>".join(f"{n} {t}" for n, t in items)) for a, b, items in cs], 3)
    return frame(h, top(fig, body))


def s44_c(h):
    cs = columns(h)
    it = [(a, b, "<br>".join(f"{n} {t}" for n, t in items)) for a, b, items in cs]
    return frame(h, two(sk("flow4", "한 업무가 관찰에서 기준으로 옮겨 가는 흐름입니다."),
                        side(L.rows(it)), "narrow"))


# ══ 45 귀찮은 일을 덜어 준다는 설득 ════════════════════════════════
def s45_a(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, L.pair(lt, rt, list(zip(ll, rl)), lr, rr))


def s45_b(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    fig = _screen("넣을 화면", "실제로 줄어든 시간을 보이는 화면입니다.",
                  "같은 일을 예전 방식으로 했을 때와 지금 방식으로 했을 때 걸린 시간이 남은 기록을 "
                  "갈무리합니다. 두 숫자가 함께 보이게 자릅니다.", ratio="22/9")
    return frame(h, top(fig, L.pair(lt, rt, list(zip(ll, rl)), lr, rr)))


def s45_c(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, two(sk("hands", "밀어내는 손과 당기는 손입니다."),
                        side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr)), "narrow"))


# ══ 46 리더가 마련할 것 ═══════════════════════════════════════════
def s46_a(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, L.fold(it, per=3))


def s46_b(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, two(sk("narrow", "빨라진 실행 뒤에 좁아지는 곳입니다."),
                        side(L.rows(it)), "narrow"))


def s46_c(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    fig = _data("넣을 자료", "재단의 실제 결재 흐름에서 좁아지는 곳입니다.",
                "재단에서 결정을 받는 순서를 적고, 기다리는 시간이 가장 긴 구간에 표시를 겹칩니다. "
                "담당자 이름은 적지 않고 자리 이름만 적습니다.", ratio="16/9")
    return frame(h, two(fig, side(L.rows(it))))


# ══ 47 담당자 몫 세 가지 ══════════════════════════════════════════
def s47_a(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    it = [(f"남는 몫 {i + 1:02d}", x, "") for i, x in enumerate(rl)]
    return frame(h, L.axis(it, lt, rt), L.strip(lt, ll, lr))


def s47_b(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    return frame(h, two(sk("shrinkclear", "줄어드는 것과 또렷해지는 것입니다."),
                        side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr)), "narrow"))


def s47_c(h):
    (lt, ll, lr), (rt, rl, rr) = papers(h)
    fig = _data("넣을 자료", "재단 담당자의 하루에서 실제로 줄어든 일입니다.",
                "담당자 한 명의 하루 일과를 적고, AI를 쓰기 전과 뒤에 각 항목에 든 시간을 나란히 적습니다.",
                ratio="16/9")
    return frame(h, two(fig, side(L.pair(lt, rt, list(zip(ll, rl)), lr, rr))))


# ══ 48 8시간 구성 ═════════════════════════════════════════════════
def s48_a(h):
    hs = hours(h)
    rows_ = []
    for lab, segs in hs:
        rows_.append((lab, [(f, t, "v" if j else "m") for f, t, j in segs], ""))
    return frame(h, L.bars(rows_))


def s48_b(h):
    return keep(h)


def s48_c(h):
    hs = hours(h)
    it = [(lab, " / ".join(t for f, t, j in segs), "") for lab, segs in hs]
    return frame(h, two(sk("density", "같은 8시간 안에서 밀도가 달라지는 그림입니다."),
                        side(L.rows(it))))


# ══ 49 가짜를 거르는 사람 ═════════════════════════════════════════
def s49_a(h):
    qa = qacards(h)
    fig = _screen("넣을 화면", "그럴듯하지만 틀린 답 화면입니다.",
                  "AI가 그럴듯하게 답했지만 사실이 틀렸던 화면을 갈무리합니다. "
                  "틀린 곳에 나중에 표시를 겹칩니다. 틀린 숫자나 없는 출처가 보여야 합니다.",
                  ratio="22/9")
    return frame(h, top(fig, L.rows(points(h))))


def s49_b(h):
    pts, qa = points(h), qacards(h)
    cells = [(pts[0][1], pts[0][2], False), (qa[0][1], qa[0][2], True),
             (pts[1][1], pts[1][2], False), (qa[1][1], qa[1][2], True)]
    return frame(h, L.quad("그럴듯함", ["낮음", "높음", qa[0][0], qa[1][0]], cells),
                 f'<div class="Lbnote"><b>{pts[2][1]}</b> {pts[2][2]}</div>')


def s49_c(h):
    return frame(h, two(sk("surface", "매끄러운 겉과 틀린 속입니다."),
                        side(L.rows(points(h))), "narrow"))


# ══ 50 사람에게 남는 다섯 가지 ════════════════════════════════════
def s50_a(h):
    it = cards(h)
    return frame(h, L.words([(b, _sub(c, a)) for a, b, c in it]))


def s50_b(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, two(sk("remain5", "실행이 빠져나간 뒤 남는 다섯입니다."),
                        side(L.rows(it)), "narrow"))


def s50_c(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    fig = _image("넣을 그림", "남는 것들입니다.",
                 "An extremely wide banner. Most of the frame is empty white. "
                 "Along the lower third, a pale grey wash recedes to the left like something draining away, "
                 "and five small rounded shapes remain standing in a row on the right, "
                 "each filled with a different gradient from the palette. "
                 "One thin ink baseline runs under all five. "
                 "Aspect ratio 9:2 with a wide empty band above.", ratio="9/2")
    return frame(h, top(fig, L.rows(it)))


# ══ 51 어려운 결정 ════════════════════════════════════════════════
def s51_a(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, L.axis(it, "쉬운 결정", "어려운 결정", cuts=(0,)))


def s51_b(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    return frame(h, two(sk("onemany", "답이 하나인 문제와 답이 여럿인 문제입니다."),
                        side(L.rows(it))))


def s51_c(h):
    it = [(_num(i), b, _sub(c, a)) for i, (a, b, c) in enumerate(cards(h))]
    fig = _image("넣을 그림", "남은 결정 앞에 선 사람입니다.",
                 "A single small abstract human figure seen from behind stands on the left, "
                 "facing right toward three diverging paths that fan out and fade before they resolve. "
                 "Behind the figure, a row of short resolved paths already ends in solid dots. "
                 "The unresolved paths are drawn in soft violet and blue; the resolved ones in pale grey. "
                 "Aspect ratio 2:1 with wide empty margins.", ratio="2/1")
    return frame(h, two(fig, side(L.rows(it))))


# ══ 52 마지막 질문 ════════════════════════════════════════════════
def s52_a(h):
    return h.replace('<h2 class="big">', '<h2 class="big Lbigq">', 1)


def s52_b(h):
    return h.replace('<div class="fg">', _spark() + '<div class="fg">', 1)


def s52_c(h):
    fig = _image("넣을 그림", "다음으로 이어지는 길입니다.",
                 "An extremely wide banner, mostly empty white. "
                 "A single thin path starts at the left edge as a solid ink line, "
                 "then continues to the right shifting into a warm orange to violet to blue gradient, "
                 "and leaves the frame at the right edge without ending. "
                 "Two small abstract figures stand near the left, facing right. "
                 "Aspect ratio 9:2, action along the lower third with a wide empty band above.",
                 ratio="9/2")
    return h.replace("</p></div>", f'</p><div class="Limpfig">{fig}</div></div>', 1)


# ══ 장별 후보 ═══════════════════════════════════════════════════════
# (장 번호, [(표시, 재료, 함수, 설명)…]). 설명은 후보목록_시각안.md에서 가져왔다.
ALL = {
    1: [("A", "그림 없이 판만", s01_a, "제목 한 줄과 부제만 두고 나머지는 비웁니다. 첫 화면이 조용해집니다."),
        ("B", "생성 이미지", s01_b, "사람과 화면이 마주 본 넓은 그림을 뒤에 깔고 제목을 얹습니다. 16:9 구획 하나입니다."),
        ("C", "실제 수치", s01_c, "13개월 세션 흐름을 아주 옅은 선으로 뒤에 깔고 제목을 얹습니다. 재단의 실제 기록으로 시작한다는 신호가 됩니다.")],
    2: [("A", "그림 없이 판만", s02_a, "세 항목을 가로 세 칸으로 나누고 칸마다 큰 번호를 붙입니다."),
        ("B", "그림 없이 판만", s02_b, "오늘과 끝난 뒤를 가로 축으로 두고, 세 항목을 그 축 위 세 지점에 놓습니다. 목표가 시간의 앞뒤로 읽힙니다."),
        ("C", "손그림", s02_c, "확인란이 있는 종이 한 장에 세 줄을 적은 모습으로 그립니다.")],
    3: [("A", "손그림", s03_a, "가로 띠 하나를 네 구간으로 나누고, 구간마다 사람 몫과 AI 몫의 면적을 다르게 칠합니다. 메시지가 몫의 크기라서 면적이 가장 정확합니다."),
        ("B", "실제 화면", s03_b, "같은 일을 대화로 시킨 화면과 위임으로 시킨 화면을 갈무리해 두 장으로 견줍니다. 22:9 구획 두 개입니다."),
        ("C", "그림 없이 판만", s03_c, "네 단계를 가로 축 위에 놓고 각 단계 아래에 사람이 하는 일을 한 줄씩 답니다.")],
    4: [("A", "생성 이미지", s04_a, "질문이 되돌아올수록 굵어지는 고리를 그림으로 뽑고, 오른쪽에 이유 셋을 둡니다. 세 마디를 오른쪽으로 밀어 계단으로 만든 탓에 글의 시작점이 줄마다 다릅니다."),
        ("B", "실제 화면", s04_b, "확신을 담아 물은 화면과 의심하게 물은 화면을 실제로 갈무리해 나란히 놓습니다. 두 화면은 같은 높이로 맞추고, 아래 이유 셋은 세 칸으로 균등하게 나눕니다."),
        ("C", "그림 없이 판만", s04_c, "동의가 쌓인 만큼 길어지는 막대를 왼쪽에 두고 이유 셋을 행으로 쌓습니다. 막대, 제목, 설명이 각각 같은 열에 섭니다.")],
    5: [("A", "그림 없이 판만", s05_a, "두 목록의 항목을 한 줄씩 좌우로 짝지어 같은 높이에 놓습니다. 지금은 각자 나열이라 대응이 보이지 않습니다."),
        ("B", "손그림", s05_b, "같은 문서를 두 사람이 볼 때 한쪽에는 채워져 보이고 다른 쪽에는 빈 곳이 보이는 그림입니다."),
        ("C", "실제 자료", s05_c, "실제로 만든 산출물 하나를 놓고 만든 사람의 표시와 받은 사람의 표시를 겹칩니다. 16:9 구획 하나입니다.")],
    6: [("A", "그림 없이 판만", s06_a, "다섯 단계를 오르는 계단으로 두고 재단이 서 있는 단을 표시합니다. 손을 들게 하는 장이라 서 있는 단이 한눈에 보여야 합니다."),
        ("B", "실제 수치 그림", s06_b, "단계마다 머무는 조직의 비율을 막대 높이로 보이고 재단 위치를 겹칩니다."),
        ("C", "손그림", s06_c, "단계마다 조직이 어떻게 달라지는지 작은 그림 다섯 개로 그립니다.")],
    7: [("A", "그림 없이 판만", s07_a, "업무와 AI 사이를 가로 축 하나로 그리고, 막히는 곳에 끊긴 표시를 둡니다. 거리가 멀다는 말이 축 위에서 바로 읽힙니다."),
        ("B", "손그림", s07_b, "두 곳이 끊긴 다리를 그립니다."),
        ("C", "실제 화면", s07_c, "실제로 막혔던 화면 두 장을 갈무리해 넣습니다. 22:9 구획 두 개입니다.")],
    8: [("A", "지금 판 그대로", s08_a, "곡선 하나가 이 장의 전부라 판을 바꾸지 않습니다. 이미 전달이 되는 장입니다."),
        ("B", "손그림", s08_b, "곡선을 둘로 늘려 도구만 들인 조직과 일하는 방식을 바꾼 조직을 겹칩니다."),
        ("C", "그림 없이 판만", s08_c, "곡선을 걷고 느려지는 기간과 빨라지는 기간을 가로 길이로만 견줍니다.")],
    9: [("A", "실제 화면", s09_a, "맥락 없이 물은 화면과 자료를 읽힌 뒤 물은 화면을 실제로 갈무리해 넣습니다. 지금은 답을 글로 옮겨 적어 두었는데, 실제 화면이면 설명이 필요 없습니다."),
        ("B", "그림 없이 판만", s09_b, "두 답을 나란히 두고 달라진 대목을 같은 줄에서 견줍니다."),
        ("C", "손그림", s09_c, "자료 더미가 들어가고 답이 달라져 나오는 흐름을 그립니다.")],
    10: [("A", "실제 화면", s10_a, "뒤에 나올 네 화면의 작은 갈무리 네 장을 나란히 놓습니다. 예고편이 되어 뒤 네 장을 기다리게 합니다. 4:3 구획 네 개입니다."),
         ("B", "그림 없이 판만", s10_b, "질문 하나를 더 던지는 비용이 줄어드는 축 위에 네 방식을 놓습니다."),
         ("C", "손그림", s10_c, "같은 자료 한 묶음에서 네 방향으로 뻗는 그림입니다.")],
    11: [("A", "지금 판 그대로", s11_a, "시연물이 이 장의 주인공이라 판을 바꾸지 않습니다. 시연이 있는 장은 화면을 비워 두는 편이 낫습니다."),
         ("B", "실제 자료", s11_b, "표 전체를 한 화면에 아주 작게 축소해 넣고, 읽어야 할 양을 면적으로 보입니다. 16:9 구획 하나입니다."),
         ("C", "그림 없이 판만", s11_c, "시연물은 화면 밖에서 크게 띄우고, 화면에는 1,598이라는 숫자 하나만 크게 둡니다.")],
    12: [("A", "그림 없이 판만", s12_a, "질문을 카드에서 목록으로 바꾸고 왼쪽 표시 하나로 통과와 막힘을 나눕니다. 이 틀은 14장과 17장에도 나와서 셋을 서로 다르게 만들어야 합니다."),
         ("B", "실제 화면", s12_b, "각 질문을 실제로 돌린 결과를 작은 갈무리로 붙입니다. 4:3 구획 네 개입니다."),
         ("C", "손그림", s12_c, "질문이 표를 통과하거나 튕겨 나오는 그림입니다.")],
    13: [("A", "지금 판 그대로", s13_a, "시연물이 주인공이라 판을 바꾸지 않습니다. 화면을 크게 보여야 다음 장의 한계가 살아납니다."),
         ("B", "실제 화면", s13_b, "시연물 대신 재단이 아침마다 여는 화면을 갈무리해 넣습니다. 16:9 구획 하나입니다."),
         ("C", "그림 없이 판만", s13_c, "화면을 왼쪽에 두고 오른쪽에 이 화면이 답하는 질문을 목록으로 답니다. 14장의 예고가 됩니다.")],
    14: [("A", "실제 화면", s14_a, "대시보드 화면을 가운데 놓고, 답할 수 있는 질문과 없는 질문을 옆에 붙입니다. 화면 밖이라는 말이 실제 화면 위에서 가장 잘 보입니다."),
         ("B", "그림 없이 판만", s14_b, "화면 테두리만 그리고 안과 밖으로 질문을 나눕니다."),
         ("C", "손그림", s14_c, "미리 골라 둔 화면 밖으로 질문이 밀려나는 그림입니다.")],
    15: [("A", "지금 판 그대로", s15_a, "시연물이 주인공이라 판을 바꾸지 않습니다. 근거를 손으로 가리키는 장이라 화면이 커야 합니다."),
         ("B", "실제 화면", s15_b, "실제 도구에 재단 자료를 읽히고 물은 화면을 갈무리해 넣습니다. 22:9 구획 하나입니다."),
         ("C", "그림 없이 판만", s15_c, "답과 근거 표를 위아래로 나눠 근거가 함께 남는다는 것만 크게 보입니다.")],
    16: [("A", "그림 없이 판만", s16_a, "두 방식이 걸리는 시간을 가로 막대 두 개로 견줍니다. 비용이 줄어든다는 말은 길이로 보이는 편이 빠릅니다."),
         ("B", "실제 화면", s16_b, "질문을 이어 던진 대화 한 판을 갈무리로 넣습니다. 22:9 구획 하나입니다."),
         ("C", "손그림", s16_c, "화면을 짓는 길과 질문을 잇는 길 두 가지를 그립니다.")],
    17: [("A", "실제 화면", s17_a, "근거 표가 붙은 답 화면을 넣고, 사람이 확인해야 할 곳에 표시를 겹칩니다. 15장에서 본 화면을 다시 쓰면 이어집니다."),
         ("B", "그림 없이 판만", s17_b, "답 하나를 놓고 AI가 한 부분과 사람이 할 부분을 두 색으로 나눕니다."),
         ("C", "손그림", s17_c, "답까지는 이어지고 결정 앞에서 멈추는 선입니다.")],
    18: [("A", "지금 판 그대로", s18_a, "시연물이 주인공이라 판을 바꾸지 않습니다. 지도를 움직여 보이는 장이라 화면을 비워 둡니다."),
         ("B", "실제 화면", s18_b, "지도에서 점 하나를 눌러 나온 상세를 옆에 함께 둡니다. 16:9 구획 하나입니다."),
         ("C", "그림 없이 판만", s18_c, "왼쪽 설명을 걷고 화면 전체를 지도로 채웁니다.")],
    19: [("A", "지금 판 그대로", s19_a, "시연물이 주인공이라 판을 바꾸지 않습니다. 시간이 흐르는 것을 보여야 하는 장이라 재생 화면이 필요합니다."),
         ("B", "실제 수치 그림", s19_b, "레이스가 끝난 순간의 순위를 멈춘 화면으로 옆에 함께 둡니다. 16:9 구획 하나입니다."),
         ("C", "그림 없이 판만", s19_c, "가로선 하나에 13개월을 찍고 그 위에 실제 후원 건수를 겹칩니다.")],
    20: [("A", "실제 화면", s20_a, "18장의 구조 지도를 가운데 두고 사람의 질문과 AI의 답을 양쪽에 붙입니다. 18장과 19장의 시연물을 회수하는 장입니다."),
         ("B", "손그림", s20_b, "같은 그림을 사이에 두고 사람과 AI가 마주 보는 모습입니다."),
         ("C", "그림 없이 판만", s20_c, "같은 기준을 가리키는 두 화살표입니다.")],
    21: [("A", "그림 없이 판만", s21_a, "머릿속과 문서와 다른 담당자, 세 지점을 축 하나에 놓습니다. 다른 조직 사례라 실제 자료를 쓰기 어렵습니다."),
         ("B", "실제 자료", s21_b, "실제로 남긴 문서를 갈무리해 넣습니다. 조직 이름은 가립니다. 16:9 구획 하나입니다."),
         ("C", "손그림", s21_c, "한 사람 머리에서 나온 것이 여러 사람에게 닿는 그림입니다.")],
    22: [("A", "실제 수치 그림", s22_a, "13개월 후원 건수 막대에 4월의 123건을 함께 그리고, 세상 평균선과 재단 기준선을 겹칩니다. 재단 자료가 이미 있어 근거까지 함께 보입니다."),
         ("B", "실제 화면", s22_b, "AI가 평균으로 판단한 답 화면을 갈무리해 넣습니다. 22:9 구획 하나입니다."),
         ("C", "그림 없이 판만", s22_c, "같은 숫자를 두 기준으로 읽은 결과를 좌우로 견줍니다.")],
    23: [("A", "손그림", s23_a, "만든 양과 읽은 양 두 곡선이 시간이 갈수록 벌어지는 그래프 하나입니다. 벌어진다는 말이 곡선에서 바로 읽힙니다."),
         ("B", "그림 없이 판만", s23_b, "만든 분량과 읽은 분량을 두 개의 길이로 견줍니다."),
         ("C", "생성 이미지", s23_c, "쌓이는 종이와 줄어드는 읽는 시간입니다. 22:9 구획 하나입니다.")],
    24: [("A", "그림 없이 판만", s24_a, "여섯을 두 줄로 접어 글자 크기를 되찾습니다. 여섯 단계를 읽히게 하는 것이 먼저입니다."),
         ("B", "손그림", s24_b, "결론에서 원본까지 거슬러 올라가는 선 하나입니다."),
         ("C", "실제 화면", s24_c, "실제로 되짚은 화면 두 장입니다. 근거 표에서 원본으로 갑니다. 22:9 구획 두 개입니다.")],
    25: [("A", "실제 화면", s25_a, "같은 결과를 두 도구에 검수시킨 화면 둘을 나란히 놓습니다. 시연으로 바로 이어집니다. 22:9 구획 두 개입니다."),
         ("B", "그림 없이 판만", s25_b, "만드는 쪽과 의심하는 쪽 사이에 결과물 하나를 두고 양쪽에서 화살표를 겁니다."),
         ("C", "손그림", s25_c, "자기 글을 자기가 읽을 때 보이지 않는 곳입니다.")],
    26: [("A", "실제 자료", s26_a, "실제 규칙 파일을 갈무리해 넣습니다. 진행노트에 예시 문안을 재단과 정한 뒤 고친다고 적어 두었으니, 그때 실제 파일로 바꿉니다. 22:9 구획 하나입니다."),
         ("B", "그림 없이 판만", s26_b, "매번 하던 지시 문장과 규칙 파일의 항목을 한 줄씩 마주 놓습니다."),
         ("C", "손그림", s26_c, "말로 하던 것이 글로 굳는 그림입니다.")],
    27: [("A", "그림 없이 판만", s27_a, "기록 더미에서 몇 줄만 남는 걸러짐을 길이 차이로 보입니다. 26장이 실제 자료라면 이 장은 판만으로 두어 번갈아 가게 합니다."),
         ("B", "손그림", s27_b, "체 하나를 지나 남는 것입니다."),
         ("C", "실제 자료", s27_c, "실제로 모은 기록과 그중 남긴 것입니다. 22:9 구획 하나입니다.")],
    28: [("A", "실제 자료", s28_a, "규칙 파일 안에서 여섯 항목이 각각 어디에 적히는지 표시를 겹칩니다. 26장의 실제 파일을 그대로 이어 씁니다. 16:9 구획 하나입니다."),
         ("B", "그림 없이 판만", s28_b, "여섯을 두 줄 세 칸으로 두고 항목마다 무엇을 적는지 한 줄씩 답니다."),
         ("C", "손그림", s28_c, "문장 하나만 복사했을 때 빠지는 것들입니다.")],
    29: [("A", "실제 화면", s29_a, "시연 전에 한 번 돌려 보기로 한 그 대화를 갈무리해 넣습니다. 진행노트에 실제로 돌려 보고 쓴다고 적혀 있습니다. 22:9 구획 하나입니다."),
         ("B", "그림 없이 판만", s29_b, "지시문 한 덩이와 그 결과로 나온 질문 목록을 위아래로 놓습니다."),
         ("C", "손그림", s29_c, "묻는 쪽과 답하는 쪽이 뒤바뀌는 그림입니다.")],
    30: [("A", "그림 없이 판만", s30_a, "한 사람이 걸은 길과 다음 사람이 시작하는 지점을 위아래 두 줄로 놓습니다. 다시 겪지 않는다는 말이 두 줄의 시작점 차이로 보입니다."),
         ("B", "손그림", s30_b, "같은 곳에서 두 번 넘어지지 않는 그림입니다."),
         ("C", "실제 자료", s30_c, "실제로 남긴 시행착오 기록입니다. 16:9 구획 하나입니다.")],
    31: [("A", "그림 없이 판만", s31_a, "위아래 단계를 같은 줄에 마주 놓아 무엇이 줄었는지 보입니다. 지금은 어긋나 있어 견주기 어렵습니다."),
         ("B", "실제 자료", s31_b, "재단의 실제 발송 절차 문서를 확인한 뒤 그 순서로 바꿉니다. 16:9 구획 하나입니다."),
         ("C", "손그림", s31_c, "사람이 서 있던 지점이 앞뒤 두 곳으로 옮겨 가는 그림입니다.")],
    32: [("A", "그림 없이 판만", s32_a, "업무 흐름 하나를 그리고 세 능력이 필요한 지점 셋을 그 위에 찍습니다. 능력을 나열하지 않고 언제 쓰는지가 보입니다."),
         ("B", "손그림", s32_b, "실행이 넘어간 뒤 남는 세 가지입니다."),
         ("C", "생성 이미지", s32_c, "나누고 바로잡고 잇는 세 동작입니다. 2:1 구획 하나입니다.")],
    33: [("A", "손그림", s33_a, "도구를 하나 더 얹은 그림과 일을 다시 그린 그림을 좌우로 놓습니다. 34장과 39장에도 같은 대비표가 나와서 셋 가운데 하나는 그림으로 빠져야 합니다."),
         ("B", "그림 없이 판만", s33_b, "대비표를 유지하되 행을 줄이고 글자를 키웁니다."),
         ("C", "실제 자료", s33_c, "재단 업무 하나를 골라 지금 흐름과 다시 그린 흐름을 나란히 놓습니다. 16:9 구획 하나입니다.")],
    34: [("A", "실제 자료", s34_a, "재단이 쓰는 도구를 실제로 적고 그 사이를 잇는 선을 그립니다. 재단이 쓰는 도구를 화면에 올리면 남의 이야기가 아니게 됩니다. 16:9 구획 하나입니다."),
         ("B", "손그림", s34_b, "따로 떨어진 섬 하나와 이어 붙인 다리입니다."),
         ("C", "그림 없이 판만", s34_c, "대비표를 유지하되 행을 줄이고 글자를 키웁니다.")],
    35: [("A", "그림 없이 판만", s35_a, "달라도 되는 것과 같아야 하는 것을 한 판에 두 색으로 나눕니다. 종이 두 장 틀이 이 부에만 다섯 번 나옵니다."),
         ("B", "손그림", s35_b, "서로 다른 길이 한 지점에서 만나는 그림입니다."),
         ("C", "실제 자료", s35_c, "재단 안에서 실제로 달라도 됐던 것과 같아야 했던 것입니다. 16:9 구획 하나입니다.")],
    36: [("A", "그림 없이 판만", s36_a, "만들 수 있는 것 전부와 그중 만들 것을 길이 차이로 보입니다. 덜 만든다는 말은 면적으로 보는 편이 빠릅니다."),
         ("B", "손그림", s36_b, "넘치게 쌓인 것에서 몇 개만 골라 내는 그림입니다."),
         ("C", "생성 이미지", s36_c, "비용이 사라진 자리에 남는 선택입니다. 2:1 구획 하나입니다.")],
    37: [("A", "실제 자료", s37_a, "재단 업무 몇 개를 네 조건에 하나씩 대어 본 표를 놓습니다. 시연에 올릴 업무를 재단과 정할 때 그대로 쓰는 표가 됩니다."),
         ("B", "그림 없이 판만", s37_b, "네 조건이 모두 겹치는 영역을 그리고 그 안에 후보 업무를 둡니다."),
         ("C", "손그림", s37_c, "조건을 하나씩 통과하며 좁아지는 통로입니다.")],
    38: [("A", "그림 없이 판만", s38_a, "결과물 하나를 놓고 세 방식이 어디를 보는지 표시를 겹칩니다. 40장이 그림이라서 이 장은 판만으로 두는 편이 낫습니다."),
         ("B", "실제 화면", s38_b, "실제 결과물에 세 방식의 검수 표시를 얹은 화면입니다. 16:9 구획 하나입니다."),
         ("C", "손그림", s38_c, "같은 것을 다르게 자르는 세 가지입니다.")],
    39: [("A", "손그림", s39_a, "답은 한 곳으로 모이고 결정은 여러 곳으로 뻗는 그림입니다. 33장과 34장에서 이미 대비표를 썼습니다."),
         ("B", "그림 없이 판만", s39_b, "대비표를 유지하되 행을 줄이고 글자를 키웁니다."),
         ("C", "생성 이미지", s39_c, "빠른 답과 느린 결정입니다. 2:1 구획 하나입니다.")],
    40: [("A", "생성 이미지", s40_a, "종이 한 장이 번져 화면이 꺼지는 장면을 가로로 긴 그림으로 뽑습니다. 아래 네 마디를 조금씩 내려 앉혀 윗변이 줄마다 어긋납니다."),
         ("B", "직접 그린 그림", s40_b, "네 단계를 기울기가 커지는 판 네 개로 직접 그립니다. 바닥선 하나가 네 칸을 가로지르고, 판과 글이 모두 같은 줄에서 시작합니다."),
         ("C", "시간 축", s40_c, "사건 셋은 촘촘히 붙고 마지막 사건 뒤로 멈춰 선 구간이 길게 남습니다. 손해가 사고 자체보다 그 뒤에 온다는 말을 길이로 보입니다.")],
    41: [("A", "그림 없이 판만", s41_a, "일곱을 크기 차이 없이 두 줄로 균등하게 놓습니다. 일곱을 다 읽히게 하는 것이 먼저입니다."),
         ("B", "손그림", s41_b, "숫자 뒤에 사람이 있는 그림 하나를 왼쪽에 두고 일곱을 오른쪽에 놓습니다."),
         ("C", "실제 자료", s41_c, "재단의 실제 개인정보 처리 문구를 한 줄 인용합니다. 22:9 구획 하나입니다.")],
    42: [("A", "그림 없이 판만", s42_a, "일곱에서 셋으로 줄어드는 것을 두 목록의 길이 차이로 보입니다. 지금 판이 이미 이 뜻에 가까워서 길이만 맞추면 됩니다."),
         ("B", "실제 자료", s42_b, "매일 확인하는 실제 확인표를 갈무리로 넣습니다. 22:9 구획 하나입니다."),
         ("C", "손그림", s42_c, "일곱 개가 셋으로 접히는 그림입니다.")],
    43: [("A", "그림 없이 판만", s43_a, "기술 쪽과 현장 쪽을 좌우 끝에 두고 그 사이에 다섯을 놓습니다. 사이를 잇는다는 말이 좌우 배치에서 바로 읽힙니다."),
         ("B", "손그림", s43_b, "두 세계 사이에서 말을 옮기는 사람입니다."),
         ("C", "실제 자료", s43_c, "재단 안에서 그 역할에 가까운 담당자의 일을 한 줄로 적습니다. 16:9 구획 하나입니다.")],
    44: [("A", "그림 없이 판만", s44_a, "세 칸을 가로 시간 축 위에 놓고 칸의 길이를 실제 기간에 맞춥니다. 90일이라는 말이 길이로 보입니다."),
         ("B", "실제 자료", s44_b, "재단 일정에 맞춘 실제 날짜를 넣습니다. 22:9 구획 하나입니다."),
         ("C", "손그림", s44_c, "한 업무가 관찰에서 기준으로 옮겨 가는 흐름입니다.")],
    45: [("A", "그림 없이 판만", s45_a, "하기 싫은 이유와 그 이유를 없애는 방법을 한 줄씩 마주 놓습니다. 짝을 지어야 설득이 되는 장입니다."),
         ("B", "실제 화면", s45_b, "실제로 줄어든 시간을 보이는 화면입니다. 22:9 구획 하나입니다."),
         ("C", "손그림", s45_c, "밀어내는 손과 당기는 손입니다.")],
    46: [("A", "그림 없이 판만", s46_a, "다섯을 두 줄로 접어 글자 크기를 되찾습니다. 리더가 있는 자리에서만 쓰는 장이라 판을 단순하게 둡니다."),
         ("B", "손그림", s46_b, "빨라진 실행 뒤에 좁아지는 곳입니다."),
         ("C", "실제 자료", s46_c, "재단의 실제 결재 흐름에서 좁아지는 곳입니다. 16:9 구획 하나입니다.")],
    47: [("A", "그림 없이 판만", s47_a, "사라지는 일과 남는 일을 가로선 하나의 양 끝에 두고 세 가지를 남는 쪽에 모읍니다. 줄어들지만 사라지지 않는다는 말이 축에서 보입니다."),
         ("B", "손그림", s47_b, "줄어드는 것과 또렷해지는 것입니다."),
         ("C", "실제 자료", s47_c, "재단 담당자의 하루에서 실제로 줄어든 일입니다. 16:9 구획 하나입니다.")],
    48: [("A", "실제 수치 그림", s48_a, "지금 하루와 바뀐 하루를 같은 길이의 막대 두 개로 두고 안쪽 색을 다르게 합니다. 총량은 같고 안이 달라진다는 것이 핵심입니다."),
         ("B", "지금 판 그대로", s48_b, "지금도 막대 두 줄이라 판을 바꾸지 않습니다."),
         ("C", "손그림", s48_c, "같은 8시간 안에서 밀도가 달라지는 그림입니다.")],
    49: [("A", "실제 화면", s49_a, "그럴듯하지만 틀린 답 화면을 넣고 틀린 곳에 표시를 겹칩니다. 틀린 것을 실제로 보여 주어야 무게가 생깁니다. 22:9 구획 하나입니다."),
         ("B", "그림 없이 판만", s49_b, "그럴듯함과 맞음을 가로와 세로로 놓고 네 구역을 만듭니다."),
         ("C", "손그림", s49_c, "매끄러운 겉과 틀린 속입니다.")],
    50: [("A", "그림 없이 판만", s50_a, "카드를 걷고 다섯 낱말을 크게 한 줄로 두고 설명은 아래에 작게 답니다. 마무리 부에서는 화면이 조용한 편이 낫습니다."),
         ("B", "손그림", s50_b, "실행이 빠져나간 뒤 남는 다섯입니다."),
         ("C", "생성 이미지", s50_c, "남는 것들입니다. 9:2 구획 하나입니다.")],
    51: [("A", "그림 없이 판만", s51_a, "쉬운 결정과 어려운 결정을 가로선 하나 위에서 나누고 AI가 가져가는 구간을 표시합니다. 쉬운 것부터 가져간다는 말이 축에서 읽힙니다."),
         ("B", "손그림", s51_b, "답이 하나인 문제와 답이 여럿인 문제입니다."),
         ("C", "생성 이미지", s51_c, "남은 결정 앞에 선 사람입니다. 2:1 구획 하나입니다.")],
    52: [("A", "그림 없이 판만", s52_a, "지금 판을 유지하고 질문만 더 키웁니다."),
         ("B", "실제 수치 그림", s52_b, "13개월 세션 흐름의 옅은 선을 뒤에 깔고 질문을 얹습니다. 01장과 짝이 됩니다."),
         ("C", "생성 이미지", s52_c, "다음으로 이어지는 길입니다. 9:2 구획 하나입니다.")],
}
# 32장(콘텐츠 갈무리)과 33장(지휘실)이 끼면서 그 뒤 장 번호가 둘씩 밀렸다.
# 후보는 예전 번호로 적어 두고 여기서 옮긴다. 새 두 장은 후보 없이 지금 판을 그대로 둔다.
ALL = {(k + 2 if k >= 32 else k): v for k, v in ALL.items()}

# 표지와 마무리 장은 감싸개가 달라 그림 구획을 따로 앉힌다.
COVER_CSS = """
.Lcovfig{position:absolute;right:6%;top:13%;bottom:30%;width:42%;display:flex;
  flex-direction:column;min-height:0;z-index:0}
/* 그림을 오른쪽에 두는 안에서는 제목이 그림을 침범하지 않게 폭을 줄인다 */
.ax-cover:has(.Lcovfig) h1{max-width:900px}
.ax-cover:has(.Lcovfig) .sub{max-width:820px}
.Lcovfig>.imgslot{flex:1;min-height:0}
.Lcovfig .imgbox{flex:1 1 auto !important;min-height:0;height:auto;width:auto !important;
  max-width:100%;align-self:center;margin:0 auto}
.ax-cover .fg,.ax-imp .fg{position:relative;z-index:1}

/* 마무리 장은 겹치지 않고 질문 아래에 넣는다. 질문이 주인공이라 그림은 낮게 깐다 */
.Limpfig{display:flex;flex-direction:column;width:100%;max-width:1280px;margin-top:6px;flex:none}
.Limpfig>.imgslot{flex:none;min-height:0}
.Limpfig .imgbox{flex:none !important;max-height:270px;height:auto;align-self:center}
.Limpfig .imgcap{margin-top:12px}
.Limpfig .imgcap p{font-size:17px}
.ax-imp:has(.Limpfig) .fg{gap:26px}
.ax-imp:has(.Limpfig) h2.big{font-size:74px}
.ax-imp:has(.Limpfig) .impband{font-size:22px;padding:24px 34px}
.ax-imp h2.big.Lbigq{font-size:116px;max-width:1620px}

/* 52장을 한 쪽에 놓으니 차례가 있어야 찾아갑니다 */
.cmpnav{position:sticky;top:0;z-index:40;background:rgba(242,243,247,.94);
  backdrop-filter:saturate(1.4) blur(8px);border-bottom:1.5px solid #E4E7EF;
  padding:14px 40px;margin-bottom:8px}
.cmpnav .in{max-width:1880px;margin:0 auto;display:flex;flex-wrap:wrap;gap:7px}
.cmpnav a{display:inline-block;min-width:38px;text-align:center;padding:6px 8px;border-radius:9px;
  font-family:var(--fm);font-size:14px;font-weight:700;color:var(--faint);text-decoration:none;
  background:#fff;border:1.5px solid #E4E7EF}
.cmpnav a:hover{color:var(--ink);border-color:#C6CBDA}
.grp{scroll-margin-top:82px}
.cmptot{margin-top:16px;font-family:var(--fm);font-size:15px;font-weight:700;
  letter-spacing:.14em;color:var(--faint)}
"""


KEEP_KIND = "지금 판 그대로"
KEEP_NOTE = ("지금 덱에 들어 있는 판을 그대로 둡니다. 손대지 않기로 정하는 것도 하나의 선택입니다.")


def compare_all_body(slides):
    """52장 전부의 후보를 한 줄에 놓은 비교 화면. 장마다 고르고 기록할 수 있다."""
    nav = "".join(f'<a href="#s{n:02d}">{n:02d}</a>' for n in sorted(ALL))
    grp = []
    for n in sorted(ALL):
        src = slides[n - 1]
        cards_ = []
        for label, kind, fn, note in ALL[n]:
            name = f"{n:02d}장 후보 {label} {kind}"
            try:
                made = fn(src)
            except Exception as err:                      # 한 장이 막혀도 나머지는 나오게 둔다
                made = src
                note = f"{note} (판을 만들지 못했습니다: {type(err).__name__})"
            cards_.append(_card(n, label, kind, name, made, note))
        # 지금 판을 그대로 두는 안이 후보에 없으면 넷째 자리에 따로 놓는다
        if not any(kind == KEEP_KIND for _, kind, _, _ in ALL[n]):
            cards_.append(_card(n, "그대로", KEEP_KIND, f"{n:02d}장 현재 상태 유지",
                                src, KEEP_NOTE, keep=True))
        four = " four" if len(cards_) == 4 else ""
        grp.append(f'<section class="grp" id="s{n:02d}">'
                   f'<h2><em>{n:02d}</em>{_head(src)}<span class="grpick"></span></h2>'
                   f'<p class="cmpsub">재료가 다른 안입니다. 화면을 누르면 크게 봅니다. '
                   f'좌우 방향키로 후보를 옮기고 ESC로 닫습니다.</p>'
                   f'<div class="row{four}">{"".join(cards_)}</div>'
                   f'{pick_memo(n)}</section>')
    return (f'<div class="cmpnav"><div class="in"><div class="navnums">{nav}</div>'
            f'{pick_bar()}</div></div>'
            '<div class="cmp">'
            '<div class="cmphd"><h1>52장 시각 안 후보</h1>'
            '<p>장마다 안 하나를 내밀지 않고, 재료가 다른 안을 셋씩 놓았습니다. '
            '여기에 지금 판을 그대로 두는 안을 하나 더해 넷씩입니다. '
            '글은 원본 그대로이고 판만 다릅니다.</p>'
            '<p>재료는 다섯 가지입니다. 실제 화면, 실제 자료와 수치, 손그림, 생성 이미지, '
            '그림 없이 판만입니다. 그림이나 화면이 필요한 안은 구획과 안내문만 넣어 두었고, '
            '단추를 누르면 프롬프트나 갈무리 안내가 복사됩니다.</p>'
            '<p>카드 아래의 정하기 단추로 장마다 안을 하나 고릅니다. 고른 기록은 이 브라우저에 '
            '남고, 위쪽 막대에서 파일로 내려받거나 다시 불러올 수 있습니다.</p>'
            f'<p class="cmptot">{len(ALL)}장, 장마다 안 3개와 현재 상태 유지</p></div>'
            + "".join(grp) + '</div>'
            + '<div class="zoom"><div class="zst"></div></div>'
            + '<div class="znow"></div>'
            + pick_panel())


def _card(n, label, kind, name, made, note, keep=False):
    """후보 카드 하나. 화면과 설명과 고르기 단추가 함께 붙는다."""
    head = "현재" if keep else f"후보 {label}"
    return (f'<figure class="cmpcard{" keep" if keep else ""}">'
            f'<div class="stage" data-name="{name}">{made}</div>'
            f'<figcaption><div class="cl"><b>{head}</b><span>{kind}</span></div>'
            f'<p>{note}</p>{pick_button(n, label, kind)}</figcaption></figure>')


def _head(html):
    """장 제목을 글자만 남겨 뽑는다. 줄바꿈 자리만 빈칸으로 남기고 나머지 태그는 그냥 지운다."""
    for pat in (r'<h2 class="head">(.*?)</h2>', r'<h[12] class="big">(.*?)</h[12]>',
                r"<h1[^>]*>(.*?)</h1>"):
        m = re.search(pat, html, re.S)
        if m:
            s = re.sub(r"<br\s*/?>", " ", m.group(1), flags=re.I)
            return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
    return ""
