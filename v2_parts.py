"""후보 판을 짜는 데 쓰는 공용 부품.

원본 장에서 글을 뽑아내는 추출기와, 그림이나 화면을 넣을 구획 하나를 만드는 함수가 들어 있다.
글은 원본 그대로 옮기고 감싸개만 바꾼다. 여기서 새 문장을 지어내지 않는다.

- 추출기: 원본 장의 틀별로 라벨, 제목, 설명을 순서대로 꺼낸다
- slot: 그림이나 화면을 넣을 곳 하나. 비율과 안내문과 복사 단추가 붙는다
"""
import re
from html import escape as html_escape

from build_ax_v2 import STYLE, SHOT_TAIL

# ── 자료 갈무리 안내의 공통 꼬리 ────────────────────────────────────
DATA_TAIL = (
    "실제 파일을 쓰되 조직 이름과 담당자 이름, 후원자 정보는 가립니다. "
    "글자가 읽히도록 화면 배율을 키우고, 보여 줄 부분만 남기고 잘라 냅니다."
)


# ══ 구획 ═══════════════════════════════════════════════════════════
_KINDS = {
    "IMAGE": ("프롬프트 복사", "IMAGE"),
    "SCREEN": ("갈무리 안내 복사", "SCREEN"),
    "DATA": ("자료 안내 복사", "DATA"),
    "CHART": ("그림 안내 복사", "CHART"),
}

_MARK = ('<div class="imark"><svg viewBox="0 0 24 24" aria-hidden="true">'
         '<rect x="3" y="5" width="18" height="14" rx="2.5"/>'
         '<circle cx="8.5" cy="10" r="1.6"/><path d="M4 17l5-5 4 4 3-2.5 4 3.5"/></svg>{}</div>')

_ICO = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/>'
        '<path d="M5 15V6a2 2 0 0 1 2-2h9"/></svg><span>{}</span>')


def slot(tag, desc, prompt, kind="IMAGE", ratio=None, pinned=False, cls=""):
    """그림이나 화면을 넣을 곳 하나.

    ratio를 주면 그 비율로 칸을 못 박는다. 주지 않으면 남는 높이를 채운다.
    pinned를 주면 캡션이 칸 안쪽 아래에 얹힌다.
    """
    btn, mark = _KINDS[kind]
    style = f' style="aspect-ratio:{ratio};flex:none;width:100%"' if ratio else ""
    cap = (f'<div class="imgcap{" pin" if pinned else ""}"><p><b>{tag}</b>{desc}</p>'
           f'<button class="pbtn" type="button" data-prompt="{html_escape(prompt)}">'
           f'{_ICO.format(btn)}</button></div>')
    box = f'<div class="imgbox"{style}>{_MARK.format(mark)}{cap if pinned else ""}</div>'
    return (f'<div class="imgslot{" pinned" if pinned else ""}{(" " + cls) if cls else ""}">'
            f'{box}{"" if pinned else cap}</div>')


def img_prompt(scene):
    """생성 이미지 프롬프트. 덱의 톤과 매너를 늘 같은 문장으로 뒤에 붙인다."""
    return scene.rstrip() + " " + STYLE


def shot_guide(what):
    """갈무리 안내. 가릴 것과 자를 크기를 늘 같은 문장으로 뒤에 붙인다."""
    return what.rstrip() + " " + SHOT_TAIL


def data_guide(what):
    """실제 자료를 넣을 때의 안내."""
    return what.rstrip() + " " + DATA_TAIL


# ══ 추출기 ═════════════════════════════════════════════════════════
def band(html):
    """결론 띠를 그대로 가져온다. 없으면 빈 문자열."""
    m = re.search(r'<div class="axband"[^>]*>.*?</div>', html, re.S)
    return m.group(0) if m else ""


def head_text(html):
    m = re.search(r'<h2 class="head">(.*?)</h2>', html, re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(1))).strip() if m else ""


def cards(html):
    """카드 줄(axstep). (라벨, 제목, 설명) 목록."""
    out = []
    for blk in re.findall(r'<div class="axstep[^"]*">(.*?)</div>', html, re.S):
        out.append((_one(blk, "b"), _one(blk, "h4"), _one(blk, "p")))
    return out


def steps(html):
    """가로 단계(stepn). (번호, 제목, 설명) 목록."""
    out = []
    for blk in re.findall(r'<div class="stepn[^"]*">(.*?)</div>', html, re.S):
        out.append((_one(blk, "b"), _one(blk, "h4"), _one(blk, "p")))
    return out


def step_rows(html):
    """비포 애프터 두 줄(baflow). [(줄이름, [(번호, 제목, 설명)…])…]"""
    rows = []
    for m in re.finditer(r'<div class="baflow[^"]*">(.*?)(?=<div class="baflow|<div class="axband|$)',
                         html, re.S):
        chunk = m.group(1)
        lab = _one(chunk, "div", cls="bfl")
        rows.append((lab, steps(chunk)))
    return rows


def papers(html):
    """종이 두 장(paper). [(윗말, [줄…], 아랫말)…]"""
    tags = re.findall(r'<div class="ptag">(.*?)</div>', html, re.S)
    lists = [re.findall(r"<li>(.*?)</li>", u, re.S)
             for u in re.findall(r'<ul class="plist[^"]*">(.*?)</ul>', html, re.S)]
    roles = re.findall(r'<div class="prole">(.*?)</div>', html, re.S)
    n = min(len(tags), len(lists), len(roles))
    return list(zip(tags[:n], lists[:n], roles[:n]))


def points(html):
    """왼쪽 번호 목록(pt). (번호, 제목, 설명) 목록."""
    out = []
    for blk in re.findall(r'<div class="pt">(.*?)</div></div>', html, re.S):
        out.append((_one(blk, "b"), _one(blk, "h4"), _one(blk, "p")))
    return out


def asks(html):
    """두 칸 질문(askcol). [(칸이름, 머리말, [(질문, 설명)…])…]"""
    out = []
    parts = re.split(r'<div class="askcol ', html)[1:]
    for p in parts:
        kind = p[:p.index('"')]
        head = re.sub(r"<i>.*?</i>", "", _one(p, "div", cls="ah"), flags=re.S)
        qs = [(_one(b, "h4"), _one(b, "p"))
              for b in re.findall(r'<div class="aq">(.*?)</div>', p, re.S)]
        out.append((kind, head.strip(), qs))
    return out


def versus(html):
    """좌우 대비표(vs). (왼쪽 머리말, 오른쪽 머리말, [(왼 제목, 왼 설명, 오른 제목, 오른 설명)…])"""
    heads = re.findall(r'<div class="vh[^"]*">(.*?)</div>', html, re.S)
    cells = re.findall(r'<div class="vc( r)?"><h4>(.*?)</h4><p>(.*?)</p></div>', html, re.S)
    left = [(h, p) for r, h, p in cells if not r]
    right = [(h, p) for r, h, p in cells if r]
    rows = [(lh, lp, rh, rp) for (lh, lp), (rh, rp) in zip(left, right)]
    return (heads[0] if heads else "", heads[1] if len(heads) > 1 else "", rows)


def facts(html):
    """사실 카드(hf). [(라벨, 제목, 설명)…]. 마지막 한 줄 카드는 제목 자리가 빈다."""
    out = []
    for blk in re.findall(r'<div class="hf(?: [^"]*)?">(.*?)</div>', html, re.S):
        out.append((_one(blk, "span"), _one(blk, "b"), _one(blk, "p")))
    return out


def flow(html):
    """절차 줄(hstep). (번호, 제목, 설명) 목록."""
    out = []
    for blk in re.findall(r'<div class="hstep[^"]*">(.*?)</div></div>', html, re.S):
        out.append((_one(blk, "b"), _one(blk, "h4"), _one(blk, "p")))
    return out


def tools(html):
    """여섯 도구(tool). (번호, 제목, 설명) 목록."""
    out = []
    for blk in re.findall(r'<div class="tool">(.*?)</div></div>', html, re.S):
        out.append((_one(blk, "span", cls="tno"), _one(blk, "h4"), _one(blk, "p")))
    return out


def columns(html):
    """세 칸 계획표(tocol). [(굵은 머리, 나머지 머리, [(번호, 줄)…])…]"""
    out = []
    for blk in re.findall(r'<div class="tocol">(.*?)</ul>', html, re.S):
        h3 = _one(blk, "h3")
        b = re.search(r"<b>(.*?)</b>", h3, re.S)
        rest = re.sub(r"<b>.*?</b>", "", h3, flags=re.S).lstrip("/ ").strip()
        items = [(re.search(r"<b>(.*?)</b>", li, re.S).group(1) if "<b>" in li else "",
                  re.sub(r"<b>.*?</b>", "", li, flags=re.S).strip())
                 for li in re.findall(r"<li>(.*?)</li>", blk, re.S)]
        out.append((b.group(1) if b else "", rest, items))
    return out


def hours(html):
    """시간 막대(hrow). [(줄이름, [(몫, 글, 판단인가)…])…]"""
    out = []
    for m in re.finditer(r'<div class="hrow[^"]*">(.*?)</div></div>', html, re.S):
        chunk = m.group(1)
        lab = _one(chunk, "div", cls="hl")
        segs = [(int(f), t, bool(j))
                for j, f, t in re.findall(r'<span(?: class="(judge)")? style="flex:(\d+)">(.*?)</span>',
                                          chunk, re.S)]
        out.append((lab, segs))
    return out


def qacards(html):
    """오른쪽 대화 상자(qacard). [(라벨, 질문, 답)…]

    상자 안에 div가 셋이라 닫는 태그로 자르면 마지막 칸이 잘린다. 여는 태그를 기준으로 쪼갠다.
    """
    out = []
    for chunk in html.split('<div class="qacard">')[1:]:
        out.append((_one(chunk, "div", cls="qlabel"),
                    _one(chunk, "div", cls="qq"),
                    _one(chunk, "div", cls="qa")))
    return out


def embed(html):
    """시연물 임베드(embwrap). (iframe 전체, [(숫자, 설명)…], 아래 한 줄)"""
    ifr = re.search(r"<iframe[^>]*></iframe>", html, re.S)
    rows = re.findall(r'<div class="figrow"><b>(.*?)</b><span>(.*?)</span></div>', html, re.S)
    note = _one(html, "div", cls="embnote")
    return (ifr.group(0) if ifr else "", rows, note)


def _one(blk, tag, cls=None):
    pat = rf'<{tag} class="{cls}">(.*?)</{tag}>' if cls else rf"<{tag}>(.*?)</{tag}>"
    m = re.search(pat, blk, re.S)
    return m.group(1) if m else ""


def plain(s):
    """태그를 걷어 낸 글자만. 줄바꿈 자리는 빈칸 하나로 남긴다."""
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
