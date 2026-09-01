#!/usr/bin/env python3
"""덱에 임베드되는 시연물 네 편의 화면 문구를 대본 파일 하나와 맞춘다.

화면에 뜨는 글이 네 곳에 흩어져 있다. 지휘실은 data/orchestra.json 에, 웹 구조 지도는
graph_template.html 의 SCENES 에, 캠페인 레이스는 build_race.py 의 주석 목록에, 표와
대시보드와 질의는 analog_template.html 의 대화 블록에 있다. 문구만 고치려고 네 파일을
따로 여는 일을 없애려고, 화면에 보이는 글만 시연물_대본.md 한 장으로 모은다.

본문_AX60.md 와 같은 원칙이다. 한 줄이 화면의 글 한 덩이이고, 줄 순서와 줄 수는 그대로
두고 글만 고친다. 줄을 더하거나 지우면 어느 마당에서 어긋났는지 알려 주고 멈춘다.

    python3 sync_script.py           대본 파일을 읽어 시연물 네 편을 다시 만든다
    python3 sync_script.py --export  코드 쪽 글로 대본 파일을 다시 뽑는다
    python3 sync_script.py --check   되박지 않고 어긋난 곳만 알려 준다

굵게는 `**굵게**` 로 적는다. 숫자가 자동으로 들어가는 자리는 `{페이지수}` 처럼 중괄호로
남겨 두고, 그 자리는 지우지 않는다.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEMO = ROOT / "시연물"
SCRIPT = ROOT / "시연물_대본.md"

HEAD = """# 시연물 대본 (직접 고쳐도 됩니다)
#
# 덱에 임베드되는 시연물 네 편에서 화면에 뜨는 글만 모았습니다.
# 한 줄이 화면의 글 한 덩이입니다. 줄 순서와 줄 수는 그대로 두고 글만 바꿉니다.
# `**굵게**` 는 굵은 글씨가 되고, `{페이지수}` 처럼 중괄호로 묶인 자리에는 숫자가 자동으로 들어갑니다.
# 그 자리는 지우지 않습니다. 마당(##)을 더하거나 줄을 더하고 지우면 되박기가 멈춥니다.
#
# 고친 뒤 반영: python3 sync_script.py
# 코드 쪽 글로 이 파일을 다시 뽑을 때: python3 sync_script.py --export (파일의 수정이 지워집니다)
#
# 숫자와 표는 GA4 자료에서 나오므로 여기에 없습니다. 그쪽은 시연물/extract.py 와 각 빌더가 만듭니다.
"""


# ══ 지휘실 ═════════════════════════════════════════════════════════
ORCH = DEMO / "data" / "orchestra.json"


def orch_load():
    return json.loads(ORCH.read_text(encoding="utf-8"))


def orch_read():
    d = orch_load()
    out = {}
    m = d["meta"]
    out["지휘실 / 머리말"] = [m["title"], m["sub"], m["note"]]

    scenes = []
    for s in d["scenes"]:
        scenes += [s["name"], s["cap"]]
    out["지휘실 / 장면 자막"] = scenes

    for j in d["jobs"]:
        rows = [j["kind"], j["ask"], j["head"], j["notice"], j["result"]]
        for a in j["agents"]:
            rows += [a["name"], a["run"], a["done"]]
        out[f"지휘실 / 작업 {j['kind']}"] = rows

    out["지휘실 / 마무리"] = ([d["wrap"]["text"]]
                          + [e["label"] for e in d["timeline"]["events"]]
                          + [d["closing"]["l1"], d["closing"]["l2"], d["closing"]["sub"]])
    return out


def _block(src, key):
    """최상위 키 하나가 감싸는 범위를 돌려준다. 문자열 안의 괄호는 세지 않는다."""
    i = src.index(f'"{key}":') + len(key) + 4
    while src[i] in " \n":
        i += 1
    op = src[i]
    cl = "]" if op == "[" else "}"
    depth, k, quoted = 0, i, False
    while True:
        c = src[k]
        if quoted:
            if c == "\\":
                k += 1
            elif c == '"':
                quoted = False
        elif c == '"':
            quoted = True
        elif c == op:
            depth += 1
        elif c == cl:
            depth -= 1
            if depth == 0:
                return i, k + 1
        k += 1


def _swap(block, field, values):
    """블록 안의 "field": "..." 를 앞에서부터 차례로 갈아 끼운다."""
    it = iter(values)
    pat = re.compile(rf'("{field}": )"(?:[^"\\]|\\.)*"')
    return pat.sub(lambda m: m.group(1) + json.dumps(next(it), ensure_ascii=False), block)


def orch_write(secs):
    """손으로 정리해 둔 JSON 모양을 흩뜨리지 않으려고 값 자리만 갈아 끼운다."""
    src = ORCH.read_text(encoding="utf-8")
    jobs = orch_load()["jobs"]

    def patch(key, fields):
        nonlocal src
        i, j = _block(src, key)
        block = src[i:j]
        for field, values in fields:
            block = _swap(block, field, values)
        src = src[:i] + block + src[j:]

    head = secs["지휘실 / 머리말"]
    patch("meta", [("title", head[:1]), ("sub", head[1:2]), ("note", head[2:3])])

    sc = secs["지휘실 / 장면 자막"]
    patch("scenes", [("name", sc[0::2]), ("cap", sc[1::2])])

    rows = [secs[f"지휘실 / 작업 {j['kind']}"] for j in jobs]
    agents = [r[5:] for r in rows]
    patch("jobs", [("kind", [r[0] for r in rows]), ("ask", [r[1] for r in rows]),
                   ("head", [r[2] for r in rows]), ("notice", [r[3] for r in rows]),
                   ("result", [r[4] for r in rows]),
                   ("name", [a[i] for a in agents for i in range(0, len(a), 3)]),
                   ("run", [a[i] for a in agents for i in range(1, len(a), 3)]),
                   ("done", [a[i] for a in agents for i in range(2, len(a), 3)])])

    tail = secs["지휘실 / 마무리"]
    ev = len(orch_load()["timeline"]["events"])
    patch("wrap", [("text", tail[:1])])
    patch("timeline", [("label", tail[1:1 + ev])])
    patch("closing", [("l1", tail[1 + ev:2 + ev]), ("l2", tail[2 + ev:3 + ev]),
                      ("sub", tail[3 + ev:4 + ev])])
    ORCH.write_text(src, encoding="utf-8")


# ══ 웹 구조 지도 ═══════════════════════════════════════════════════
GRAPH = DEMO / "graph_template.html"
GRAPH_SCENES = re.compile(r"(const SCENES = \[\n)(.*?)(\];)", re.S)
GRAPH_CAP = re.compile(r'cap: (.+?) \}')
# 자동으로 채워지는 숫자를 대본에서는 이름으로 보여 준다
GRAPH_SLOTS = [
    ("{페이지수}", '" + G.meta.pages.toLocaleString("ko-KR") + "'),
    ("{이동수}", '" + G.meta.edges.toLocaleString("ko-KR") + "'),
]


def _graph_lines():
    body = GRAPH_SCENES.search(GRAPH.read_text(encoding="utf-8")).group(2)
    return [ln for ln in body.split("\n") if ln.strip()]


def graph_read():
    caps = []
    for ln in _graph_lines():
        raw = GRAPH_CAP.search(ln).group(1).strip()
        for name, expr in GRAPH_SLOTS:
            raw = raw.replace(expr, name)
        caps.append(raw.strip('"'))
    # 빈 자막(둘러보기 장면)은 대본에서 자리만 지킨다
    return {"웹 구조 지도 / 장면 자막": [c if c else "(자막 없음)" for c in caps]}


def graph_write(secs):
    caps = secs["웹 구조 지도 / 장면 자막"]
    src = GRAPH.read_text(encoding="utf-8")
    lines = _graph_lines()
    out = []
    for ln, cap in zip(lines, caps):
        text = "" if cap == "(자막 없음)" else cap
        for name, expr in GRAPH_SLOTS:
            text = text.replace(name, expr)
        out.append(GRAPH_CAP.sub(lambda m: f'cap: "{text}" }}', ln, count=1))
    body = "\n".join(out) + "\n"
    GRAPH.write_text(GRAPH_SCENES.sub(lambda m: m.group(1) + body + m.group(3), src, count=1),
                     encoding="utf-8")


def graph_build():
    """자막만 바꿨으니 자리 계산은 건너뛴다.

    build_graph.py 를 다시 돌리면 배치가 미세하게 달라져 지도 전체가 바뀐다. 문구만 고친
    자리에서 지도가 흔들리지 않도록, 만들어 둔 graph.json 을 템플릿에 다시 박기만 한다.
    """
    data = (DEMO / "data" / "graph.json").read_text(encoding="utf-8")
    html = GRAPH.read_text(encoding="utf-8").replace("/*__GRAPH_DATA__*/null", data, 1)
    dest = ROOT / "웹구조그래프.html"
    dest.write_text(html, encoding="utf-8")
    return f"저장: {dest.name} {dest.stat().st_size / 1024:.0f}KB"


# ══ 캠페인 레이스 ══════════════════════════════════════════════════
RACE = DEMO / "build_race.py"
RACE_NOTES = re.compile(r'(ANNOTATIONS = \[\n)(.*?)(\]\n)', re.S)
RACE_NOTE = re.compile(r'\("(\d{8})", "(.*?)"\)')
RACE_LABELS = [("label_cum", '"label_cum": "', '"'),
               ("label_roll", '"label_roll": f"', '"'),
               ("foot_cum", '"foot_cum": "', '"'),
               ("foot_roll", '"foot_roll": f"', '"')]


def _race_note_pairs():
    body = RACE_NOTES.search(RACE.read_text(encoding="utf-8")).group(2)
    return RACE_NOTE.findall(body)


def _race_label(src, head, tail):
    i = src.index(head) + len(head)
    return src[i:src.index(tail, i)]


def race_read():
    src = RACE.read_text(encoding="utf-8")
    notes = [f"{d} {t}" for d, t in _race_note_pairs()]
    labels = [_race_label(src, h, t) for _, h, t in RACE_LABELS]
    return {"캠페인 레이스 / 날짜 주석": notes,
            "캠페인 레이스 / 막대 기준 문구": labels}


def race_write(secs):
    src = RACE.read_text(encoding="utf-8")
    rows = []
    for ln in secs["캠페인 레이스 / 날짜 주석"]:
        day, _, text = ln.partition(" ")
        rows.append(f'    ("{day}", "{text.strip()}"),')
    src = RACE_NOTES.sub(lambda m: m.group(1) + "\n".join(rows) + "\n" + m.group(3), src, count=1)

    for text, (_, head, tail) in zip(secs["캠페인 레이스 / 막대 기준 문구"], RACE_LABELS):
        i = src.index(head) + len(head)
        src = src[:i] + text + src[src.index(tail, i):]
    RACE.write_text(src, encoding="utf-8")


# ══ 표와 대시보드와 질의 ═══════════════════════════════════════════
ANALOG = DEMO / "analog_template.html"
ANALOG_BLOCK = re.compile(r'(<div class="thread">\n)(.*?)(\s*</div>\n\s*<div class="box">)', re.S)
ANALOG_ME = re.compile(r'<div class="me">(.*?)</div>')
ANALOG_P = re.compile(r'<p>(.*?)</p>', re.S)
ANALOG_EH = re.compile(r'<div class="eh">(.*?)</div>')


def _analog_body():
    return ANALOG_BLOCK.search(ANALOG.read_text(encoding="utf-8")).group(2)


def _bold_out(s):
    return re.sub(r"<strong>(.*?)</strong>", r"**\1**", s).strip()


def _bold_in(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


def analog_read():
    body = _analog_body()
    rows = []
    for m in re.finditer(r'<div class="me">(.*?)</div>|<p>(.*?)</p>|<div class="eh">(.*?)</div>',
                         body, re.S):
        rows.append(_bold_out(next(g for g in m.groups() if g is not None)))
    return {"표와 대시보드와 질의 / 질의 화면 대화": rows}


def analog_write(secs):
    rows = list(secs["표와 대시보드와 질의 / 질의 화면 대화"])
    src = ANALOG.read_text(encoding="utf-8")
    body = _analog_body()
    it = iter(rows)

    def swap(m):
        text = _bold_in(next(it))
        if m.group(1) is not None:
            return f'<div class="me">{text}</div>'
        if m.group(2) is not None:
            return f'<p>{text}</p>'
        return f'<div class="eh">{text}</div>'

    new = re.sub(r'<div class="me">(.*?)</div>|<p>(.*?)</p>|<div class="eh">(.*?)</div>',
                 swap, body, flags=re.S)
    ANALOG.write_text(src.replace(body, new, 1), encoding="utf-8")


# ══ 대본 파일 ══════════════════════════════════════════════════════
READERS = [orch_read, graph_read, race_read, analog_read]
# 빌더마다 파일을 떨구는 방법이 다르다. 레이스만 --write 를 받아야 완성본을 쓰고,
# 지도는 자리 계산을 건너뛰려고 빌더 대신 여기서 직접 박는다.
WRITERS = [(orch_write, ["build_orchestra.py"]), (graph_write, graph_build),
           (race_write, ["build_race.py", "--write"]), (analog_write, ["build_analog.py"])]


def collect():
    out = {}
    for fn in READERS:
        out.update(fn())
    return out


def dump(secs):
    parts = [HEAD]
    for name, rows in secs.items():
        parts.append(f"\n## {name}\n" + "\n".join(rows) + "\n")
    SCRIPT.write_text("".join(parts), encoding="utf-8")
    print(f"✓ {SCRIPT.name} 생성 (마당 {len(secs)}개, 줄 {sum(len(v) for v in secs.values())}개)")


def parse():
    secs, name = {}, None
    for raw in SCRIPT.read_text(encoding="utf-8").split("\n"):
        line = raw.rstrip()
        if line.startswith("## "):
            name = line[3:].strip()
            secs[name] = []
        elif line.startswith("#"):
            continue
        elif line and name:
            secs[name].append(line)
    return secs


def compare(code, file):
    bad = []
    for name, rows in code.items():
        got = file.get(name)
        if got is None:
            bad.append(f"  마당이 없습니다: {name}")
        elif len(got) != len(rows):
            bad.append(f"  {name}: 파일 {len(got)}줄, 코드 {len(rows)}줄")
    for name in file:
        if name not in code:
            bad.append(f"  코드에 없는 마당입니다: {name}")
    return bad


def main():
    code = collect()
    if "--export" in sys.argv or not SCRIPT.exists():
        dump(code)
        return
    file = parse()
    bad = compare(code, file)
    if bad:
        print("✗ 대본 파일과 코드 구조가 다릅니다. 줄이나 마당을 더하거나 지웠습니다.")
        print("\n".join(bad))
        print("  코드 쪽 글로 다시 뽑으려면 python3 sync_script.py --export")
        raise SystemExit(1)
    if "--check" in sys.argv:
        print("✓ 대본 파일과 코드 구조가 같습니다")
        return
    for write, cmd in WRITERS:
        write(file)
        if callable(cmd):
            print(f"✓ 웹 구조 지도  {cmd()}")
            continue
        r = subprocess.run([sys.executable, *cmd], cwd=DEMO, capture_output=True, text=True)
        if r.returncode:
            print(f"✗ {cmd[0]} 실패\n{r.stdout}{r.stderr}")
            raise SystemExit(1)
        tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
        print(f"✓ {cmd[0]}  {tail}")


if __name__ == "__main__":
    main()
