"""손으로 그린 그림 묶음.

생성 이미지를 뽑지 않고 개념만 선과 면으로 보이는 안에 쓴다. 그림에는 글자를 넣지 않는다.
글은 그림 옆이나 아래에 원본 그대로 놓고, 그림은 뜻만 나른다.

모든 그림은 SVG 하나이고 부모 칸을 가득 채운다. 색은 덱의 네 가지를 그대로 쓴다.
"""

# 붓 색. 원본 덱의 네 가지에서 가져왔다.
O, K, V, B = "#FF7A1A", "#FF4D6D", "#A855F7", "#3B82F6"
INK, PALE, MUTE = "#1F2430", "#E9EBF1", "#C6CBDA"

SKETCH_CSS = """
/* ══ 손그림 ═══════════════════════════════════════════════════════
   글자를 넣지 않고 선과 면으로만 뜻을 나른다. 칸을 가득 채우고 비율만 지킨다.
   ═══════════════════════════════════════════════════════════════ */
.skwrap{display:flex;align-items:center;justify-content:center;min-height:0;
  border-radius:26px;padding:22px;
  background:linear-gradient(150deg,#FFF9F3,#FDF5FA 45%,#F6F4FE 75%,#F1F7FF);
  border:1.5px solid #EDEAF2}
.skwrap svg{display:block;width:100%;height:100%;max-height:100%;overflow:visible}
.skwrap svg *{vector-effect:non-scaling-stroke}
.skcap{margin-top:16px;font-size:18.5px;line-height:1.55;color:var(--dim)}
.skcap b{display:block;font-family:var(--fm);font-size:14px;font-weight:700;
  letter-spacing:.18em;color:var(--faint);margin-bottom:7px}
"""

_DEFS = f"""<defs>
<linearGradient id="v2sg" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{O}"/><stop offset=".45" stop-color="{K}"/>
  <stop offset=".8" stop-color="{V}"/><stop offset="1" stop-color="{B}"/></linearGradient>
<linearGradient id="v2sv" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{V}"/><stop offset="1" stop-color="{B}"/></linearGradient>
</defs>"""


def _svg(vb, inner, ratio=None):
    st = f' style="aspect-ratio:{ratio}"' if ratio else ""
    return (f'<svg viewBox="{vb}" preserveAspectRatio="xMidYMid meet" aria-hidden="true"{st}>'
            f'{_DEFS}<g fill="none" stroke-linecap="round" stroke-linejoin="round">{inner}</g></svg>')


def wrap(name, cap=None, tag="넣을 그림", ratio=None):
    """그림 하나를 칸에 담는다. 캡션은 주면 아래에 붙는다."""
    body = f'<div class="skwrap">{SKETCHES[name](ratio)}</div>'
    if cap:
        body += f'<div class="skcap"><b>{tag}</b>{cap}</div>'
    return f'<div class="imgslot">{body}</div>'


# ══ 그림 ═══════════════════════════════════════════════════════════
def band4(r=None):
    """03 가로 띠 하나를 네 구간으로 나누고 사람 몫과 AI 몫의 면적을 다르게 칠한다."""
    seg, out = [(0.80, O), (0.58, K), (0.34, V), (0.14, B)], []
    for i, (h, c) in enumerate(seg):
        x = 24 + i * 92
        top = 30 + (1 - h) * 110
        out.append(f'<rect x="{x}" y="{top:.0f}" width="80" height="{h*110:.0f}" rx="10" '
                   f'fill="{c}" opacity=".9"/>')
        out.append(f'<rect x="{x}" y="30" width="80" height="{(1-h)*110:.0f}" rx="10" '
                   f'fill="{PALE}"/>')
        out.append(f'<line x1="{x}" y1="152" x2="{x+80}" y2="152" stroke="{MUTE}" stroke-width="2"/>')
    return _svg("0 0 400 180", "".join(out), r)


def checkpaper(r=None):
    """02 확인란이 있는 종이 한 장에 세 줄."""
    out = ['<rect x="96" y="16" width="208" height="188" rx="14" fill="#fff" stroke="' + PALE + '" stroke-width="2"/>']
    for i, c in enumerate((O, K, V)):
        y = 62 + i * 48
        out.append(f'<rect x="120" y="{y-16}" width="30" height="30" rx="8" stroke="{c}" stroke-width="2.4"/>')
        out.append(f'<path d="M127 {y-2}l6 7 11-14" stroke="{c}" stroke-width="2.8"/>')
        out.append(f'<line x1="164" y1="{y-6}" x2="{276 - i*18}" y2="{y-6}" stroke="{PALE}" stroke-width="6"/>')
        out.append(f'<line x1="164" y1="{y+8}" x2="{242 - i*14}" y2="{y+8}" stroke="{PALE}" stroke-width="6"/>')
    return _svg("0 0 400 220", "".join(out), r)


def five(r=None):
    """06 단계마다 조직이 어떻게 달라지는지 다섯 무리로."""
    rows = [(4, 0), (4, 1), (4, 2), (5, 3), (4, 4)]
    out, cols = [], (MUTE, O, K, V, B)
    for i, (n, spread) in enumerate(rows):
        cx = 46 + i * 78
        out.append(f'<circle cx="{cx}" cy="150" r="30" stroke="{PALE}" stroke-width="2"/>')
        for k in range(n):
            a = k * 90 + spread * 14
            import math
            rad = 13 + (4 - spread) * 3
            x = cx + rad * math.cos(math.radians(a))
            y = 150 + rad * math.sin(math.radians(a))
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="{cols[i]}" opacity=".9"/>')
        if i < 4:
            out.append(f'<path d="M{cx+34} 150h10" stroke="{MUTE}" stroke-width="2"/>')
        out.append(f'<line x1="{cx-26}" y1="196" x2="{cx+26}" y2="196" '
                   f'stroke="{cols[i]}" stroke-width="{3 + i}"/>')
    return _svg("0 0 400 220", "".join(out), r)


def bridge(r=None):
    """07 두 곳이 끊긴 다리."""
    out = [f'<rect x="6" y="120" width="70" height="56" rx="10" fill="{PALE}"/>',
           f'<rect x="324" y="120" width="70" height="56" rx="10" fill="{PALE}"/>',
           f'<path d="M76 120h58" stroke="url(#v2sg)" stroke-width="9"/>',
           f'<path d="M176 120h58" stroke="url(#v2sg)" stroke-width="9"/>',
           f'<path d="M276 120h48" stroke="url(#v2sg)" stroke-width="9"/>']
    for x in (134, 234):
        out.append(f'<path d="M{x} 112l0 16M{x+42} 112l0 16" stroke="{K}" stroke-width="3"/>')
        out.append(f'<path d="M{x+4} 132l34 34M{x+38} 132l-34 34" stroke="{K}" stroke-width="3" opacity=".55"/>')
    for x in (76, 134, 176, 234, 276, 324):
        out.append(f'<line x1="{x}" y1="126" x2="{x}" y2="176" stroke="{MUTE}" stroke-width="2.5"/>')
    out.append(f'<line x1="6" y1="178" x2="394" y2="178" stroke="{PALE}" stroke-width="4"/>')
    return _svg("0 0 400 200", "".join(out), r)


def readflow(r=None):
    """09 자료 더미가 들어가고 답이 달라져 나오는 흐름."""
    out = []
    for i in range(4):
        out.append(f'<rect x="{16 + i*7}" y="{62 + i*17}" width="86" height="15" rx="6" '
                   f'fill="{PALE}"/>')
    out.append(f'<path d="M118 108h40" stroke="{MUTE}" stroke-width="3"/>')
    out.append(f'<path d="M150 100l10 8-10 8" stroke="{MUTE}" stroke-width="3"/>')
    out.append(f'<rect x="166" y="60" width="76" height="96" rx="18" stroke="url(#v2sv)" stroke-width="3"/>')
    out.append(f'<circle cx="204" cy="108" r="18" stroke="{V}" stroke-width="3"/>')
    out.append(f'<path d="M258 108h40" stroke="url(#v2sg)" stroke-width="3"/>')
    out.append(f'<path d="M290 100l10 8-10 8" stroke="{B}" stroke-width="3"/>')
    for i, w in enumerate((104, 88, 116)):
        out.append(f'<rect x="306" y="{72 + i*30}" width="{w*0.7:.0f}" height="15" rx="6" '
                   f'fill="url(#v2sg)" opacity="{.9 - i*.22:.2f}"/>')
    return _svg("0 0 400 200", "".join(out), r)


def fan4(r=None):
    """10 같은 자료 한 묶음에서 네 방향으로 뻗는다."""
    out = [f'<rect x="26" y="82" width="66" height="46" rx="12" fill="{PALE}"/>',
           f'<rect x="34" y="74" width="66" height="46" rx="12" fill="#fff" stroke="{MUTE}" stroke-width="2"/>']
    ends = [(360, 34), (368, 84), (368, 132), (360, 180)]
    for (x, y), c in zip(ends, (O, K, V, B)):
        out.append(f'<path d="M104 100C190 100 220 {y} {x-34} {y}" stroke="{c}" stroke-width="3"/>')
        out.append(f'<circle cx="{x-24}" cy="{y}" r="11" fill="{c}" opacity=".92"/>')
    return _svg("0 0 400 210", "".join(out), r)


def sieve(r=None):
    """12과 27 체 하나를 지나 남는 것."""
    out = []
    for i in range(9):
        out.append(f'<circle cx="{40 + i*36}" cy="{28 + (i % 3)*16}" r="9" fill="{PALE}"/>')
    out.append(f'<path d="M28 108h344" stroke="url(#v2sg)" stroke-width="5"/>')
    for i in range(12):
        out.append(f'<line x1="{40 + i*28}" y1="100" x2="{40 + i*28}" y2="116" '
                   f'stroke="{MUTE}" stroke-width="2.5"/>')
    for i, c in enumerate((O, K, V)):
        out.append(f'<circle cx="{132 + i*68}" cy="{168 + (i % 2)*14}" r="12" fill="{c}" opacity=".9"/>')
    return _svg("0 0 400 200", "".join(out), r)


def pushout(r=None):
    """14 미리 골라 둔 화면 밖으로 질문이 밀려난다."""
    out = [f'<rect x="70" y="34" width="200" height="140" rx="16" stroke="{MUTE}" stroke-width="2.5" fill="#fff"/>']
    for i in range(3):
        out.append(f'<rect x="92" y="{58 + i*40}" width="{150 - i*22}" height="20" rx="8" fill="{PALE}"/>')
    for i, c in enumerate((O, K, V)):
        y = 52 + i * 50
        out.append(f'<path d="M276 {y+10}h58" stroke="{c}" stroke-width="3"/>')
        out.append(f'<path d="M326 {y+2}l10 8-10 8" stroke="{c}" stroke-width="3"/>')
        out.append(f'<circle cx="{352}" cy="{y+10}" r="11" stroke="{c}" stroke-width="3"/>')
    return _svg("0 0 400 210", "".join(out), r)


def twopath(r=None):
    """16 화면을 짓는 길과 질문을 잇는 길."""
    out = [f'<circle cx="34" cy="106" r="12" fill="{INK}"/>']
    out.append(f'<path d="M50 100C120 40 150 40 200 40" stroke="{MUTE}" stroke-width="3" stroke-dasharray="9 8"/>')
    for i in range(3):
        out.append(f'<rect x="{206 + i*54}" y="24" width="42" height="32" rx="8" '
                   f'fill="{PALE}" stroke="{MUTE}" stroke-width="2"/>')
    out.append(f'<path d="M50 114C120 176 150 176 340 176" stroke="url(#v2sg)" stroke-width="4"/>')
    for i, c in enumerate((O, K, V, B)):
        out.append(f'<circle cx="{120 + i*74}" cy="{"176" if i else "150"}" r="9" fill="{c}"/>')
    return _svg("0 0 400 210", "".join(out), r)


def stopline(r=None):
    """17 답까지는 이어지고 결정 앞에서 멈추는 선."""
    out = [f'<path d="M20 110h236" stroke="url(#v2sg)" stroke-width="6"/>']
    for i, c in enumerate((O, K, V)):
        out.append(f'<circle cx="{40 + i*76}" cy="110" r="13" fill="{c}"/>')
    out.append(f'<path d="M268 110h18" stroke="{MUTE}" stroke-width="6" stroke-dasharray="4 10"/>')
    out.append(f'<line x1="300" y1="52" x2="300" y2="168" stroke="{K}" stroke-width="4"/>')
    out.append(f'<circle cx="352" cy="110" r="26" stroke="{MUTE}" stroke-width="3" stroke-dasharray="8 8"/>')
    return _svg("0 0 400 210", "".join(out), r)


def faceoff(r=None):
    """20 같은 그림을 사이에 두고 사람과 AI가 마주 본다."""
    out = [f'<rect x="146" y="52" width="108" height="106" rx="16" stroke="url(#v2sv)" stroke-width="3" fill="#fff"/>']
    for i in range(3):
        out.append(f'<line x1="168" y1="{78 + i*26}" x2="{232 - i*12}" y2="{78 + i*26}" stroke="{PALE}" stroke-width="7"/>')
    out.append(f'<circle cx="62" cy="86" r="20" stroke="{INK}" stroke-width="3"/>')
    out.append(f'<path d="M28 158c0-22 16-36 34-36s34 14 34 36" stroke="{INK}" stroke-width="3"/>')
    out.append(f'<rect x="306" y="62" width="60" height="56" rx="14" stroke="{V}" stroke-width="3"/>')
    out.append(f'<path d="M320 152h32M336 118v34" stroke="{V}" stroke-width="3"/>')
    out.append(f'<path d="M104 100h34M262 100h34" stroke="{MUTE}" stroke-width="3"/>')
    return _svg("0 0 400 200", "".join(out), r)


def spread(r=None):
    """21 한 사람 머리에서 나온 것이 여러 사람에게 닿는다."""
    out = [f'<circle cx="56" cy="104" r="24" stroke="{INK}" stroke-width="3"/>',
           f'<rect x="168" y="76" width="60" height="56" rx="12" fill="#fff" stroke="url(#v2sv)" stroke-width="3"/>',
           f'<path d="M84 104h74" stroke="{MUTE}" stroke-width="3"/>']
    for i, c in enumerate((O, K, V, B)):
        y = 34 + i * 48
        out.append(f'<path d="M232 104C280 104 288 {y} 322 {y}" stroke="{c}" stroke-width="2.6"/>')
        out.append(f'<circle cx="342" cy="{y}" r="13" stroke="{c}" stroke-width="2.6"/>')
    return _svg("0 0 400 210", "".join(out), r)


def gapcurve(r=None):
    """23 만든 양과 읽은 양 두 곡선이 갈수록 벌어진다."""
    out = [f'<line x1="30" y1="180" x2="380" y2="180" stroke="{MUTE}" stroke-width="2"/>',
           f'<line x1="30" y1="20" x2="30" y2="180" stroke="{MUTE}" stroke-width="2"/>',
           f'<path d="M30 172C130 158 220 88 380 26" stroke="url(#v2sg)" stroke-width="4.5"/>',
           f'<path d="M30 174C140 168 250 154 380 142" stroke="{MUTE}" stroke-width="4.5"/>']
    for x in (200, 270, 340):
        import math
        t = (x - 30) / 350
        y1 = 172 - (146 * t ** 1.7)
        y2 = 174 - (32 * t)
        out.append(f'<line x1="{x}" y1="{y1:.0f}" x2="{x}" y2="{y2:.0f}" stroke="{K}" '
                   f'stroke-width="2.5" stroke-dasharray="6 6"/>')
    return _svg("0 0 400 200", "".join(out), r)


def climbback(r=None):
    """24 결론에서 원본까지 거슬러 올라가는 선 하나."""
    out, xs = [], [352, 288, 224, 160, 96, 34]
    ys = [42, 68, 94, 120, 146, 172]
    d = " ".join(f"{'M' if i == 0 else 'L'}{x} {y}" for i, (x, y) in enumerate(zip(xs, ys)))
    out.append(f'<path d="{d}" stroke="url(#v2sg)" stroke-width="4"/>')
    for i, (x, y) in enumerate(zip(xs, ys)):
        c = (O, K, V, B, V, MUTE)[i]
        out.append(f'<circle cx="{x}" cy="{y}" r="{13 if i in (0, 5) else 9}" fill="{c}"/>')
    out.append(f'<path d="M50 166l-12 8 12 8" stroke="{MUTE}" stroke-width="3"/>')
    return _svg("0 0 400 210", "".join(out), r)


def blindspot(r=None):
    """25 자기 글을 자기가 읽을 때 보이지 않는 곳."""
    out = [f'<rect x="118" y="26" width="164" height="158" rx="14" fill="#fff" stroke="{PALE}" stroke-width="2"/>']
    for i in range(5):
        out.append(f'<line x1="140" y1="{56 + i*26}" x2="{260 - (i % 3)*20}" y2="{56 + i*26}" '
                   f'stroke="{PALE}" stroke-width="7"/>')
    out.append(f'<circle cx="200" cy="108" r="40" fill="{MUTE}" opacity=".5"/>')
    out.append(f'<circle cx="52" cy="104" r="19" stroke="{INK}" stroke-width="3"/>')
    out.append(f'<path d="M74 104h34" stroke="{MUTE}" stroke-width="3" stroke-dasharray="7 7"/>')
    out.append(f'<circle cx="348" cy="104" r="19" stroke="{V}" stroke-width="3"/>')
    out.append(f'<path d="M326 104h-34" stroke="{V}" stroke-width="3"/>')
    return _svg("0 0 400 210", "".join(out), r)


def harden(r=None):
    """26 말로 하던 것이 글로 굳는다."""
    out = []
    for i in range(3):
        out.append(f'<path d="M{30 + i*16} {56 + i*38}c22-18 60-18 78 0c18 18 4 34-18 34h-40z" '
                   f'stroke="{MUTE}" stroke-width="2.4" stroke-dasharray="7 6"/>')
    out.append(f'<path d="M186 108h44" stroke="url(#v2sg)" stroke-width="3.5"/>')
    out.append(f'<path d="M222 100l10 8-10 8" stroke="{V}" stroke-width="3.5"/>')
    out.append(f'<rect x="248" y="34" width="130" height="150" rx="14" fill="#fff" '
               f'stroke="url(#v2sv)" stroke-width="3"/>')
    for i in range(5):
        out.append(f'<line x1="272" y1="{66 + i*26}" x2="{354 - (i % 2)*22}" y2="{66 + i*26}" '
                   f'stroke="{PALE}" stroke-width="7"/>')
    return _svg("0 0 400 210", "".join(out), r)


def island(r=None):
    """34 따로 떨어진 섬 하나와 이어 붙인 다리."""
    out = [f'<ellipse cx="86" cy="150" rx="66" ry="26" fill="{PALE}"/>',
           f'<ellipse cx="304" cy="150" rx="62" ry="24" fill="{PALE}"/>',
           f'<rect x="56" y="86" width="60" height="46" rx="12" stroke="{MUTE}" stroke-width="2.6"/>',
           f'<rect x="276" y="88" width="56" height="44" rx="12" stroke="url(#v2sv)" stroke-width="3"/>',
           f'<path d="M152 132h96" stroke="url(#v2sg)" stroke-width="7"/>']
    for x in (152, 200, 248):
        out.append(f'<line x1="{x}" y1="132" x2="{x}" y2="158" stroke="{MUTE}" stroke-width="2.5"/>')
    out.append(f'<path d="M16 176h368" stroke="{MUTE}" stroke-width="2" stroke-dasharray="5 8"/>')
    return _svg("0 0 400 200", "".join(out), r)


def meet(r=None):
    """35 서로 다른 길이 한 지점에서 만난다."""
    out = []
    for i, c in enumerate((O, K, V, B)):
        y0 = 26 + i * 44
        out.append(f'<path d="M22 {y0}C130 {y0} 180 106 288 106" stroke="{c}" stroke-width="3.2"/>')
        out.append(f'<circle cx="22" cy="{y0}" r="9" fill="{c}"/>')
    out.append(f'<circle cx="300" cy="106" r="24" fill="#fff" stroke="url(#v2sv)" stroke-width="4"/>')
    out.append(f'<path d="M324 106h48" stroke="url(#v2sv)" stroke-width="4"/>')
    return _svg("0 0 400 200", "".join(out), r)


def pick(r=None):
    """36 넘치게 쌓인 것에서 몇 개만 골라 낸다."""
    out = []
    import math
    for i in range(14):
        a = i * 47
        x = 92 + 62 * math.cos(math.radians(a))
        y = 104 + 56 * math.sin(math.radians(a * 1.6))
        out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="26" height="20" rx="6" fill="{PALE}"/>')
    out.append(f'<path d="M208 106h44" stroke="{MUTE}" stroke-width="3"/>')
    out.append(f'<path d="M244 98l10 8-10 8" stroke="{MUTE}" stroke-width="3"/>')
    for i, c in enumerate((O, K, V)):
        out.append(f'<rect x="286" y="{50 + i*46}" width="72" height="32" rx="9" fill="{c}" opacity=".9"/>')
    return _svg("0 0 400 210", "".join(out), r)


def funnel(r=None):
    """37 조건을 하나씩 통과하며 좁아지는 통로."""
    out, w = [], [140, 106, 74, 44]
    for i, (ww, c) in enumerate(zip(w, (O, K, V, B))):
        x = 40 + i * 84
        out.append(f'<path d="M{x} {106-ww/2:.0f}h56v{ww}h-56z" fill="{c}" opacity="{.18 + i*.06:.2f}"/>')
        out.append(f'<path d="M{x+56} {106-ww/2:.0f}L{x+84} {106-w[min(i+1,3)]/2:.0f}'
                   f'M{x+56} {106+ww/2:.0f}L{x+84} {106+w[min(i+1,3)]/2:.0f}" '
                   f'stroke="{c}" stroke-width="2.6"/>')
    out.append(f'<circle cx="368" cy="106" r="16" fill="{B}"/>')
    return _svg("0 0 400 210", "".join(out), r)


def cut3(r=None):
    """38 같은 것을 다르게 자르는 세 가지."""
    out = []
    for i, (c, d) in enumerate(((O, "M46 30v148"), (K, "M20 104h152"), (V, "M28 42l136 124"))):
        x = i * 128
        out.append(f'<rect x="{20 + x}" y="30" width="152" height="148" rx="16" '
                   f'fill="#fff" stroke="{PALE}" stroke-width="2.4"/>')
        shifted = d.replace("M46", f"M{46+x}").replace("M20", f"M{20+x}").replace("M28", f"M{28+x}")
        shifted = shifted.replace("h152", "h152").replace("l136", "l136")
        out.append(f'<path d="{shifted}" stroke="{c}" stroke-width="4" stroke-dasharray="10 7"/>')
    return _svg("0 0 400 208", "".join(out), r)


def converge(r=None):
    """39 답은 한 곳으로 모이고 결정은 여러 곳으로 뻗는다."""
    out = []
    for i, c in enumerate((O, K, V, B)):
        y = 32 + i * 46
        out.append(f'<path d="M20 {y}C86 {y} 108 106 158 106" stroke="{c}" stroke-width="3"/>')
    out.append(f'<circle cx="170" cy="106" r="14" fill="{INK}"/>')
    out.append(f'<line x1="200" y1="34" x2="200" y2="178" stroke="{PALE}" stroke-width="3"/>')
    out.append(f'<circle cx="232" cy="106" r="14" fill="#fff" stroke="{V}" stroke-width="4"/>')
    for i, c in enumerate((O, K, V, B)):
        y = 32 + i * 46
        out.append(f'<path d="M246 106C296 106 318 {y} 380 {y}" stroke="{c}" stroke-width="3" '
                   f'stroke-dasharray="9 7"/>')
    return _svg("0 0 400 208", "".join(out), r)


def fold7(r=None):
    """42 일곱 개가 셋으로 접힌다."""
    out = []
    for i in range(7):
        out.append(f'<rect x="24" y="{16 + i*26}" width="112" height="18" rx="7" fill="{PALE}"/>')
    out.append(f'<path d="M152 104h48" stroke="url(#v2sg)" stroke-width="3.5"/>')
    out.append(f'<path d="M192 96l10 8-10 8" stroke="{V}" stroke-width="3.5"/>')
    for i, c in enumerate((O, K, V)):
        out.append(f'<rect x="230" y="{40 + i*50}" width="146" height="34" rx="11" fill="{c}" opacity=".88"/>')
    return _svg("0 0 400 208", "".join(out), r)


def carry(r=None):
    """43 두 세계 사이에서 말을 옮기는 사람."""
    out = [f'<rect x="14" y="40" width="112" height="128" rx="16" fill="{PALE}"/>',
           f'<rect x="274" y="40" width="112" height="128" rx="16" fill="{PALE}"/>']
    for i in range(3):
        out.append(f'<rect x="34" y="{62 + i*34}" width="{72 - i*10}" height="16" rx="6" fill="{MUTE}" opacity=".6"/>')
        out.append(f'<circle cx="{306 + i*26}" cy="{78 + i*32}" r="11" stroke="{V}" stroke-width="2.6"/>')
    out.append(f'<circle cx="200" cy="76" r="21" stroke="{INK}" stroke-width="3"/>')
    out.append(f'<path d="M168 152c0-24 14-40 32-40s32 16 32 40" stroke="{INK}" stroke-width="3"/>')
    out.append(f'<path d="M134 104h34M232 104h34" stroke="url(#v2sg)" stroke-width="3.4"/>')
    return _svg("0 0 400 208", "".join(out), r)


def narrow(r=None):
    """46 빨라진 실행 뒤에 좁아지는 곳."""
    out = [f'<path d="M16 60h190v92H16z" fill="{PALE}"/>',
           f'<path d="M206 60L262 96v20l-56 36z" fill="{MUTE}" opacity=".55"/>',
           f'<path d="M262 96h122v20H262z" fill="url(#v2sg)" opacity=".85"/>']
    for i in range(5):
        out.append(f'<circle cx="{40 + i*38}" cy="106" r="12" fill="#fff" opacity=".9"/>')
    out.append(f'<path d="M206 44v124M262 80v52" stroke="{K}" stroke-width="3"/>')
    return _svg("0 0 400 208", "".join(out), r)


def density(r=None):
    """48 같은 길이 안에서 밀도가 달라진다."""
    out = [f'<rect x="24" y="40" width="352" height="52" rx="14" stroke="{MUTE}" stroke-width="2.4"/>',
           f'<rect x="24" y="128" width="352" height="52" rx="14" stroke="{MUTE}" stroke-width="2.4"/>']
    for i in range(6):
        out.append(f'<rect x="{40 + i*58}" y="54" width="34" height="24" rx="7" fill="{PALE}"/>')
    for i in range(14):
        out.append(f'<rect x="{34 + i*25}" y="142" width="16" height="24" rx="5" '
                   f'fill="url(#v2sg)" opacity="{.55 + (i % 3)*.15:.2f}"/>')
    return _svg("0 0 400 208", "".join(out), r)


def surface(r=None):
    """49 매끄러운 겉과 틀린 속."""
    out = [f'<rect x="34" y="28" width="332" height="72" rx="16" fill="#fff" stroke="{PALE}" stroke-width="2.4"/>']
    for i in range(3):
        out.append(f'<line x1="58" y1="{50 + i*18}" x2="{338 - i*44}" y2="{50 + i*18}" stroke="{PALE}" stroke-width="7"/>')
    out.append(f'<path d="M34 116h332" stroke="{MUTE}" stroke-width="2" stroke-dasharray="7 7"/>')
    out.append(f'<rect x="34" y="130" width="332" height="62" rx="16" fill="#fff" stroke="{PALE}" stroke-width="2.4"/>')
    for i, x in enumerate((84, 186, 292)):
        out.append(f'<line x1="{x-26}" y1="161" x2="{x+26}" y2="161" stroke="{PALE}" stroke-width="7"/>')
        out.append(f'<path d="M{x-11} 150l22 22M{x+11} 150l-22 22" stroke="{K}" stroke-width="3.4"/>')
    return _svg("0 0 400 208", "".join(out), r)


def remain5(r=None):
    """50 실행이 빠져나간 뒤 남는 다섯."""
    out = [f'<rect x="20" y="34" width="160" height="140" rx="18" fill="{PALE}" opacity=".7"/>']
    for i in range(6):
        out.append(f'<rect x="{38 + (i % 2)*66}" y="{56 + (i//2)*40}" width="52" height="26" rx="8" '
                   f'fill="#fff" opacity=".8"/>')
    out.append(f'<path d="M196 104h34" stroke="{MUTE}" stroke-width="3" stroke-dasharray="7 7"/>')
    for i, c in enumerate((O, K, V, B, V)):
        out.append(f'<circle cx="{258 + (i % 3)*54}" cy="{72 + (i//3)*64}" r="21" '
                   f'fill="{c}" opacity=".9"/>')
    return _svg("0 0 400 208", "".join(out), r)


def onemany(r=None):
    """51 답이 하나인 문제와 답이 여럿인 문제."""
    out = [f'<circle cx="60" cy="104" r="13" fill="{INK}"/>',
           f'<path d="M76 104h74" stroke="url(#v2sg)" stroke-width="4"/>',
           f'<circle cx="166" cy="104" r="17" fill="{O}"/>',
           f'<line x1="200" y1="30" x2="200" y2="180" stroke="{PALE}" stroke-width="3"/>',
           f'<circle cx="246" cy="104" r="13" fill="{INK}"/>']
    for i, c in enumerate((O, K, V, B)):
        y = 40 + i * 44
        out.append(f'<path d="M262 104C310 104 322 {y} 356 {y}" stroke="{c}" stroke-width="3" stroke-dasharray="9 7"/>')
        out.append(f'<circle cx="374" cy="{y}" r="11" stroke="{c}" stroke-width="3"/>')
    return _svg("0 0 400 208", "".join(out), r)


def hands(r=None):
    """45 밀어내는 손과 당기는 손."""
    out = [f'<rect x="158" y="66" width="84" height="76" rx="16" fill="url(#v2sg)" opacity=".85"/>',
           f'<path d="M28 104h96" stroke="{MUTE}" stroke-width="4"/>',
           f'<path d="M104 88l20 16-20 16" stroke="{MUTE}" stroke-width="4"/>',
           f'<path d="M372 104h-96" stroke="{V}" stroke-width="4"/>',
           f'<path d="M296 88l-20 16 20 16" stroke="{V}" stroke-width="4"/>']
    for i in range(3):
        out.append(f'<path d="M{34 + i*10} {74 - i*0}c8-10 22-10 30 0" stroke="{MUTE}" stroke-width="2.4"/>')
        out.append(f'<path d="M{336 - i*10} 134c-8 10-22 10-30 0" stroke="{V}" stroke-width="2.4" opacity=".8"/>')
    return _svg("0 0 400 208", "".join(out), r)


def shrinkclear(r=None):
    """47 줄어드는 것과 또렷해지는 것."""
    out = []
    for i in range(5):
        out.append(f'<rect x="24" y="{26 + i*34}" width="{150 - i*24}" height="22" rx="8" '
                   f'fill="{PALE}" opacity="{.9 - i*.14:.2f}"/>')
    out.append(f'<path d="M196 104h40" stroke="{MUTE}" stroke-width="3"/>')
    out.append(f'<path d="M228 96l10 8-10 8" stroke="{MUTE}" stroke-width="3"/>')
    for i, c in enumerate((O, K, V)):
        out.append(f'<rect x="256" y="{44 + i*46}" width="122" height="34" rx="11" fill="{c}" opacity=".9"/>')
    return _svg("0 0 400 208", "".join(out), r)


def pairview(r=None):
    """05 같은 문서를 두 사람이 볼 때 한쪽은 채워져 보이고 한쪽은 빈 곳이 보인다."""
    out = []
    for j in range(2):
        x = 24 + j * 200
        out.append(f'<rect x="{x}" y="34" width="152" height="146" rx="14" fill="#fff" '
                   f'stroke="{PALE}" stroke-width="2.4"/>')
        for i in range(5):
            y = 62 + i * 24
            if j == 0 or i % 2 == 0:
                out.append(f'<line x1="{x+22}" y1="{y}" x2="{x + 130 - (i % 3)*18}" y2="{y}" '
                           f'stroke="{PALE if j else MUTE}" stroke-width="7" opacity="{1 if j == 0 else .5}"/>')
            else:
                out.append(f'<rect x="{x+22}" y="{y-8}" width="{100 - i*8}" height="16" rx="6" '
                           f'stroke="{K}" stroke-width="2.2" stroke-dasharray="6 6"/>')
    out.append(f'<circle cx="100" cy="196" r="12" stroke="{INK}" stroke-width="2.6"/>')
    out.append(f'<circle cx="300" cy="196" r="12" stroke="{V}" stroke-width="2.6"/>')
    return _svg("0 0 400 218", "".join(out), r)


def twocurve(r=None):
    """08 도구만 들인 조직과 일하는 방식을 바꾼 조직의 두 곡선."""
    out = [f'<line x1="28" y1="180" x2="380" y2="180" stroke="{MUTE}" stroke-width="2"/>',
           f'<line x1="28" y1="20" x2="28" y2="180" stroke="{MUTE}" stroke-width="2"/>',
           f'<path d="M28 120C90 172 150 176 220 150C288 124 330 118 380 116" '
           f'stroke="{MUTE}" stroke-width="4.5"/>',
           f'<path d="M28 120C92 176 148 172 216 132C284 92 330 56 380 30" '
           f'stroke="url(#v2sg)" stroke-width="4.5"/>',
           f'<circle cx="28" cy="120" r="9" fill="{INK}"/>']
    return _svg("0 0 400 200", "".join(out), r)


def flow4(r=None):
    """44 한 업무가 관찰에서 기준으로 옮겨 간다."""
    out = []
    for i, c in enumerate((O, K, V)):
        x = 34 + i * 124
        out.append(f'<rect x="{x}" y="{72 - i*8}" width="94" height="{68 + i*16}" rx="14" '
                   f'fill="{c}" opacity="{.28 + i*.24:.2f}"/>')
        if i < 2:
            out.append(f'<path d="M{x+100} 106h16" stroke="{MUTE}" stroke-width="3"/>')
            out.append(f'<path d="M{x+110} 98l10 8-10 8" stroke="{MUTE}" stroke-width="3"/>')
    out.append(f'<line x1="34" y1="182" x2="378" y2="182" stroke="{PALE}" stroke-width="5"/>')
    return _svg("0 0 400 208", "".join(out), r)


def standshift(r=None):
    """31 사람이 서 있던 지점이 앞뒤 두 곳으로 옮겨 간다."""
    out = [f'<line x1="24" y1="70" x2="376" y2="70" stroke="{PALE}" stroke-width="6"/>',
           f'<line x1="24" y1="160" x2="376" y2="160" stroke="{PALE}" stroke-width="6"/>']
    for i in range(6):
        out.append(f'<circle cx="{48 + i*62}" cy="70" r="11" fill="{MUTE}"/>')
    out.append(f'<circle cx="172" cy="70" r="17" fill="{INK}"/>')
    for i, c in enumerate((O, K, V, B)):
        out.append(f'<circle cx="{62 + i*88}" cy="160" r="11" fill="{c}" opacity=".85"/>')
    out.append(f'<circle cx="62" cy="160" r="18" fill="{INK}"/>')
    out.append(f'<circle cx="326" cy="160" r="18" fill="{INK}"/>')
    out.append(f'<path d="M172 88C130 118 96 128 66 140M172 88C230 118 292 130 322 140" '
               f'stroke="{K}" stroke-width="2.6" stroke-dasharray="7 6"/>')
    return _svg("0 0 400 200", "".join(out), r)


def three_act(r=None):
    """32 실행이 넘어간 뒤 남는 세 가지."""
    out = [f'<rect x="20" y="52" width="118" height="104" rx="16" fill="{PALE}" opacity=".8"/>',
           f'<path d="M154 104h34" stroke="{MUTE}" stroke-width="3" stroke-dasharray="7 7"/>']
    for i, c in enumerate((O, K, V)):
        x = 208 + i * 62
        out.append(f'<circle cx="{x}" cy="104" r="26" stroke="{c}" stroke-width="3.4"/>')
        out.append(f'<circle cx="{x}" cy="104" r="9" fill="{c}"/>')
        if i < 2:
            out.append(f'<path d="M{x+28} 104h6" stroke="{MUTE}" stroke-width="2.4"/>')
    return _svg("0 0 400 208", "".join(out), r)


def sevenman(r=None):
    """41 숫자 뒤에 사람이 있다."""
    out = []
    for i in range(7):
        out.append(f'<rect x="{28 + i*50}" y="{160 - (i % 4)*26}" width="30" height="{20 + (i % 4)*26}" '
                   f'rx="7" fill="{PALE}"/>')
    out.append(f'<circle cx="212" cy="72" r="30" stroke="url(#v2sv)" stroke-width="3.4"/>')
    out.append(f'<path d="M164 168c0-32 22-54 48-54s48 22 48 54" stroke="url(#v2sv)" stroke-width="3.4"/>')
    return _svg("0 0 400 200", "".join(out), r)


def twinframe(r=None):
    """33 도구를 하나 더 얹은 그림과 일을 다시 그린 그림."""
    out = [f'<rect x="18" y="52" width="152" height="106" rx="16" fill="{PALE}"/>']
    for i in range(3):
        out.append(f'<rect x="{36 + i*44}" y="76" width="32" height="58" rx="8" fill="#fff" opacity=".9"/>')
    out.append(f'<rect x="120" y="34" width="60" height="52" rx="12" fill="{O}" opacity=".9"/>')
    out.append(f'<line x1="200" y1="30" x2="200" y2="180" stroke="{PALE}" stroke-width="3"/>')
    for i, c in enumerate((O, K, V, B)):
        out.append(f'<rect x="{232 + (i % 2)*84}" y="{52 + (i//2)*58}" width="70" height="44" rx="12" '
                   f'fill="{c}" opacity=".82"/>')
    out.append(f'<path d="M302 74h30M267 96v14M351 96v14M302 132h30" stroke="{MUTE}" stroke-width="2.6"/>')
    return _svg("0 0 400 208", "".join(out), r)


SKETCHES = {
    "band4": band4, "checkpaper": checkpaper, "five": five, "bridge": bridge,
    "readflow": readflow, "fan4": fan4, "sieve": sieve, "pushout": pushout,
    "twopath": twopath, "stopline": stopline, "faceoff": faceoff, "spread": spread,
    "gapcurve": gapcurve, "climbback": climbback, "blindspot": blindspot, "harden": harden,
    "island": island, "meet": meet, "pick": pick, "funnel": funnel, "cut3": cut3,
    "converge": converge, "fold7": fold7, "carry": carry, "narrow": narrow,
    "density": density, "surface": surface, "remain5": remain5, "onemany": onemany,
    "hands": hands, "shrinkclear": shrinkclear, "pairview": pairview, "twocurve": twocurve,
    "flow4": flow4, "standshift": standshift, "three_act": three_act, "sevenman": sevenman,
    "twinframe": twinframe,
}
