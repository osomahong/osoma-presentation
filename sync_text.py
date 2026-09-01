"""덱 본문을 슬라이드별 텍스트 파일과 맞춘다.

본문_AX60.md 는 화면에 보이는 글을 장 순서대로 적은 파일이다. 한 줄이 화면의 글 한 덩이(제목, 설명, 카드 제목,
목록 한 줄)다. 빈 줄로 나눈 문단은 한 덩이로 읽어 줄바꿈으로 잇고(제목을 두 줄로 쓸 때), 목록 항목이 줄 수만큼
이어지는 자리에서는 줄마다 한 항목으로 본다. `**굵게**` 는 굵은 글씨가 된다. 사용자가 이 파일을 고치면 다음 빌드가 그 글을 같은 위치에 되박는다. 줄 수와 순서는 코드가 만든
구조를 따르므로, 줄을 더하거나 지우면 빌드가 멈추고 새 추출본을 옆에 써 준다.

제목 안의 강조 색(span.gt)이나 굵은 글씨는 한 줄로 합쳐서 낸다. 그 줄을 고쳤을 때 강조하던 낱말이 새 글에도
있으면 색을 그대로 두고, 없으면 줄 전체를 첫 조각에 넣는다.

sync(slides, path, export=False):
  파일이 없거나 export 가 참이면 코드 텍스트로 파일을 쓴다.
  파일이 있으면 파일 텍스트로 슬라이드 HTML 을 바꿔 돌려준다.
"""
import html as H
import re
import sys

SKIP_CLASSES = {"brandbar", "pgno", "credit", "credit2", "clock"}
SKIP_TAGS = {"style", "script", "title", "svg"}  # svg 는 아래 text 만 따로 살린다
VOID = {"br", "img", "hr", "input", "meta", "link", "stop", "path", "circle", "rect", "line", "use",
        "polyline", "polygon", "ellipse"}
BLOCK = {"h1", "h2", "h3", "h4", "h5", "p", "li", "div", "td", "th", "section", "header", "footer",
         "ul", "ol", "label", "dt", "dd", "figcaption", "text"}
TOKEN = re.compile(r"(<[^>]+>)")
TAG = re.compile(r"<\s*(/?)([a-zA-Z0-9]+)([^>]*)>")
BR = re.compile(r"<br\s*/?>", re.I)
CLASS = re.compile(r'class="([^"]*)"')
INDEX = re.compile(r"0\d")  # 카드 번호 01~09 는 코드가 매기므로 파일에 내지 않는다
LETTERS = re.compile(r"[가-힣A-Za-z0-9]")
ZW = re.compile(r"[\u200b\u200c\u200d\ufeff]")
BOLD = re.compile(r"\*\*(.+?)\*\*")
HEAD = "\n".join([
    "# 쇼케이스 본문 (직접 고쳐도 됩니다)",
    "#",
    "# 한 줄이 화면의 글 한 덩이입니다. 줄 순서와 줄 수는 그대로 두고 글만 바꿉니다.",
    "# 한 덩이를 두 줄로 쓰려면 그 덩이를 빈 줄로 감싸고 안에서 줄을 나눕니다. `**굵게**` 는 굵은 글씨가 됩니다.",
    "# 덩이를 더하거나 지우면 빌드가 멈춥니다. 장을 더하거나 빼는 일은 빌더에서 합니다.",
    "# 고친 뒤 빌드: python3 build_ax.py --approve",
    "# 코드 쪽 글로 이 파일을 다시 뽑을 때: python3 build_ax.py --export (파일의 수정이 지워집니다)",
    "", ""])


def _pieces(html):
    """슬라이드 HTML 을 토큰으로 나누고, 글 조각을 (토큰 번호, 블록 번호, 인라인 여부, 글) 로 모은다."""
    tokens = TOKEN.split(html)
    stack = []  # (tag, skip, elem_id, block_id)
    found = []
    for i, tok in enumerate(tokens):
        if tok.startswith("<"):
            m = TAG.match(tok)
            if not m:
                continue
            closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
            if closing:
                while stack:
                    t = stack.pop()
                    if t[0] == tag:
                        break
                continue
            if tok.endswith("/>") or tag in VOID:
                continue
            cm = CLASS.search(attrs)
            classes = set(cm.group(1).split()) if cm else set()
            parent_skip = stack[-1][1] if stack else False
            skip = (parent_skip and tag != "text") or tag in SKIP_TAGS or bool(classes & SKIP_CLASSES)
            block_id = i if tag in BLOCK else (stack[-1][3] if stack else i)
            stack.append((tag, skip, i, block_id))
            continue
        text = tok.strip()
        if not text or not LETTERS.search(text) or INDEX.fullmatch(text):
            continue
        if not stack or stack[-1][1]:
            continue
        tag, _, _, block_id = stack[-1]
        found.append((i, block_id, tag not in BLOCK, H.unescape(text)))
    return tokens, found


def _groups(tokens, found):
    """같은 블록의 조각을 한 줄로 묶는다. 조각 사이에 <br> 이나 새 여는 태그가 있으면 띄어 잇고, 닫는 태그만 있으면 붙여 잇는다."""
    groups = []
    for piece in found:
        if groups and groups[-1][0][1] == piece[1]:
            groups[-1].append(piece)
        else:
            groups.append([piece])
    lines = []
    for g in groups:
        s = ""
        for k, (i, _, _, _) in enumerate(g):
            raw = H.unescape(tokens[i])
            if k:
                between = "".join(tokens[g[k - 1][0] + 1:i])
                opens = BR.search(between) or re.search(r"<[a-zA-Z]", between)
                if opens and not raw.startswith((" ", "\n")) and not s.endswith(" "):
                    s += " "
            s += raw
        lines.append(re.sub(r"\s+", " ", s).strip())
    return groups, lines


def export(slides, path):
    out = [HEAD]
    for n, html in enumerate(slides, 1):
        tokens, found = _pieces(html)
        _, lines = _groups(tokens, found)
        out.append(f"## {n:02d}\n")
        out.extend(f"{line}\n" for line in lines)
        out.append("\n")
    path.write_text("".join(out), encoding="utf-8")


def _read(path):
    """파일을 {장 번호: [문단]} 으로 읽는다. 문단은 빈 줄로 나뉘고, 줄은 (글, 끝에 공백 두 칸이 있었는지) 로 둔다."""
    data, cur = {}, None
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = ZW.sub("", raw)
        line = raw.strip()
        hard = raw.rstrip("\r\n").endswith("  ")
        if line.startswith("## "):
            cur = int(line[3:].strip()); data[cur] = [[]]
        elif cur is None or line.startswith("#"):
            continue
        elif not line:
            if data[cur][-1]:
                data[cur].append([])
        else:
            data[cur][-1].append((line, hard))
    for n in data:
        data[n] = [p for p in data[n] if p]
    return data


def _align(paras, groups, tokens):
    """문단을 코드 블록에 맞춘다. 세 가지 읽기를 차례로 시도해 블록 수와 맞는 것을 쓴다.
    1) 한 줄이 한 블록  2) 끝 공백 두 칸이 있는 줄은 다음 줄과 한 블록, 줄 수만큼 li 가 이어지면 줄마다 한 항목
    3) 문단 하나가 한 블록(줄 수만큼 li 가 이어지는 문단만 줄마다 한 항목)"""
    tags = [TAG.match(tokens[g[0][1]]).group(2).lower() for g in groups]
    want = len(groups)

    def li_run(at, k):
        return k > 1 and at + k <= len(tags) and all(t == "li" for t in tags[at:at + k])

    flat = [t for p in paras for t, _ in p]
    if len(flat) == want:
        return flat

    out = []
    for p in paras:
        if li_run(len(out), len(p)):
            out.extend(t for t, _ in p); continue
        buf = []
        for t, hard in p:
            buf.append(t)
            if not hard:
                out.append("<br>".join(buf)); buf = []
        if buf:
            out.append("<br>".join(buf))
    if len(out) == want:
        return out

    out = []
    for p in paras:
        if li_run(len(out), len(p)):
            out.extend(t for t, _ in p)
        else:
            out.append("<br>".join(t for t, _ in p))
    return out if len(out) == want else None


def _put(tokens, i, text):
    """글 조각을 되박는다. `**굵게**` 는 strong 으로, `<br>` 은 줄바꿈으로 살린다."""
    tok = tokens[i]
    lead = tok[:len(tok) - len(tok.lstrip())]
    trail = tok[len(tok.rstrip()):]
    body = H.escape(text, quote=False).replace("&lt;br&gt;", "<br>")
    body = BOLD.sub(r"<strong>\1</strong>", body)
    tokens[i] = lead + body + trail


def _rewrite(tokens, group, new):
    """한 블록의 조각들에 새 글을 나눠 넣는다. 강조 조각이 새 글에 남아 있으면 그 자리를 지킨다."""
    hl = [(k, text) for k, (_, _, inline, text) in enumerate(group) if inline]
    if hl:
        pos, segs, ok = 0, [], True
        for _, t in hl:
            at = new.find(t, pos)
            if at < 0:
                ok = False
                break
            segs.append(new[pos:at]); pos = at + len(t)
        segs.append(new[pos:])
        if ok:
            gaps = [[] for _ in range(len(hl) + 1)]
            gi = 0
            for k, (_, _, inline, _) in enumerate(group):
                if inline:
                    gi += 1
                else:
                    gaps[gi].append(k)
            if all(not seg.strip() or gap for seg, gap in zip(segs, gaps)):
                for k, (i, _, inline, text) in enumerate(group):
                    if not inline:
                        _put(tokens, i, "")
                for seg, gap in zip(segs, gaps):
                    if gap:
                        _put(tokens, group[gap[0]][0], seg.strip())
                return
    first, last = group[0][0], group[-1][0]
    _put(tokens, first, new)
    for i, _, _, _ in group[1:]:
        _put(tokens, i, "")
    for i in range(first, last):
        if BR.fullmatch(tokens[i].strip()):
            tokens[i] = ""


def apply(slides, path):
    data = _read(path)
    out, changed, bad = [], 0, []
    for n, html in enumerate(slides, 1):
        tokens, found = _pieces(html)
        groups, lines = _groups(tokens, found)
        paras = data.get(n)
        want = _align(paras, groups, tokens) if paras is not None else None
        if want is None:
            got = 0 if paras is None else sum(len(p) for p in paras)
            bad.append(f"{n:02d}장: 파일 {got}줄, 코드 {len(lines)}줄")
            out.append(html)
            continue
        for group, old, new in zip(groups, lines, want):
            if new == old:
                continue
            changed += 1
            _rewrite(tokens, group, new)
        out.append("".join(tokens))
    if bad:
        fresh = path.with_name(path.stem + ".새로추출.md")
        export(slides, fresh)
        print("✗ 본문 파일과 코드 구조가 다릅니다. 줄을 더하거나 지웠거나, 코드에서 장이 바뀌었습니다.")
        for b in bad:
            print("  " + b)
        print(f"  코드 기준 새 추출본을 {fresh.name} 에 썼습니다. 고친 글을 옮긴 뒤 {path.name} 으로 바꿔 두거나,")
        print("  코드 글을 그대로 쓰려면 python3 build_ax.py --export 로 파일을 다시 뽑습니다.")
        sys.exit(1)
    print(f"✓ 본문 파일 적용 ({path.name}, 코드와 다른 줄 {changed}개)")
    return out


def sync(slides, path, export=False):
    if export or not path.exists():
        globals()["export"](slides, path)
        print(f"✓ 본문 파일 {'다시 씀' if export else '새로 씀'} ({path.name})")
        return slides
    return apply(slides, path)
