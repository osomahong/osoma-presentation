"""60분 덱의 본 흐름 사이에 끼우는 장들과 부록.

본 흐름에 들어가는 것: 이걸 할 수 있게 됩니다(3장), 개인 최적화의 함정 세 장(5~7장), 실습 질문. 심화 여덟 장도 여기 있다. 조립 순서는 build_ax.py가 정한다.

문장 원칙: 제목은 질문이나 실제 상황, 설명은 말로 채우니 장표 문장은 짧게, 주어는 담당자.
중심 비유는 레시피 하나만 쓴다(손맛은 달라도 재료와 순서와 위생 기준은 같다).
"""

DEEP_CSS = """
/* ── 머리말을 한글 파트 표기로 ── */
.ax .kicker{font-family:var(--f);font-size:21px;font-weight:700;letter-spacing:.02em}
.ax .kicker .k2{font-weight:500}

/* 카드 아이콘 */
.axstep .ci{width:46px;height:46px;display:block;margin-bottom:16px;stroke:url(#ig);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.axlad.five .axstep .ci{width:40px;height:40px;margin-bottom:12px}

/* ── 심화 장 ── */
.axlad.three{grid-template-columns:repeat(3,1fr)}
.axlad.five{grid-template-columns:repeat(5,1fr);gap:20px}
.axlad.five .axstep{padding:30px 26px 26px}
.axlad.five .axstep h4{font-size:24px}
.axlad.five .axstep p{font-size:18.5px}
.hfacts.four{grid-template-columns:repeat(4,1fr);margin-top:40px;flex:1;align-content:center}
.hf.hot{border:2px solid transparent;background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}
.hf.hot p{color:var(--ink);font-weight:700;font-size:20px;line-height:1.55}
.stepn.hot h4{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}

/* 06장. 왼쪽에 예시 갈무리 두 장을 세우고 대비 목록을 오른쪽으로 민다.
   갈무리는 03장에서 쓴 것을 그대로 쓴다. 같은 화면을 다시 꺼내 예시로 삼는 자리다 */
.minewrap{display:grid;grid-template-columns:280px 1fr;gap:44px;flex:1;min-height:0;align-items:stretch;margin-top:24px}
.mineart{display:flex;flex-direction:column;justify-content:center;gap:18px;min-height:0}
.mineart div{min-height:0;border-radius:12px;overflow:hidden;background:#fff;
  border:1px solid rgba(30,42,80,.18);box-shadow:0 8px 22px rgba(15,23,42,.12)}
.mineart .m1{aspect-ratio:16/9}
.mineart .m2{aspect-ratio:41/50}
.mineart img{width:100%;height:100%;object-fit:cover;display:block}
.minewrap .balist{margin-top:0;min-height:0}

/* 좌우 대비 표 */
.vs{display:grid;grid-template-columns:1fr 84px 1fr;gap:12px 0;align-items:stretch;margin-top:26px;flex:1;align-content:center}
.vs .vh{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.16em;color:var(--faint);padding:0 6px 2px}
.vs .vh.r{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.vs .vc{background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:17px 30px}
.vs .vc.r{border:2px solid transparent;background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}
.vs .vc h4{font-size:24px;font-weight:800;line-height:1.4}
.vs .vc p{font-size:18.5px;color:var(--dim);margin-top:7px;line-height:1.5}
.vs .vne{display:grid;place-items:center;font-family:var(--fm);font-size:28px;font-weight:700;color:var(--faint)}

/* 30 60 90 */
.toc.deep{margin-top:40px;flex:1;align-content:center}
.toc.deep .tocol li{font-size:21px;padding:12px 0}
.toc.deep .tocol h3{font-size:27px}
.toc.deep .tocol h3 b{font-size:21px}

/* 두 줄 제목과 리드가 있는 장에서 대비 목록이 넘치지 않게 */
.balist{margin-top:24px}
.paper .plist li{font-size:22px}
.balist .paper .plist{gap:10px}
.balist .paper .prole{margin-top:16px;padding-top:14px}

/* 대비 목록 오른쪽에 질문 카드 두 장 */
.balist .rcol{gap:0;min-height:0}
.balist .rcol .qacard{padding:20px 30px}
.balist .rcol .qacard + .qacard{margin-top:12px}
.balist .rcol .qacard .qlabel{margin-bottom:12px}
.balist .rcol .qacard .qa{margin-top:12px;padding-top:12px}

/* 결과만 남은 상태와 규칙 파일 예시 */
.rulefile-demo{gap:18px}
.rulecompare{display:grid;grid-template-columns:.72fr 1.28fr;gap:22px;flex:1;min-height:0;align-items:stretch}
.resultonly,.rulefile{min-width:0;border-radius:22px;overflow:hidden}
.resultonly{background:#232732;color:#D9DEEA;box-shadow:0 18px 46px rgba(30,35,50,.14)}
.resultbar{display:flex;align-items:center;gap:8px;padding:15px 20px;border-bottom:1px solid rgba(255,255,255,.1);
  font-family:var(--fm);font-size:12px;letter-spacing:.1em;color:#8B93A6}
.resultbar i{width:10px;height:10px;border-radius:50%;background:#FF6A76;box-shadow:18px 0 #F5B04C,36px 0 #65C78A;margin-right:36px}
.resultbody{padding:28px 30px;font-family:var(--fm);font-size:17px;line-height:1.7}
.resultbody .rlabel{display:block;color:#8B93A6;font-size:11px;letter-spacing:.14em;margin-bottom:11px}
.resultbody .rbubble{padding:16px 18px;border-radius:14px;background:#303645;color:#fff;font-weight:600}
.resultbody .rmissing{margin-top:24px;padding-top:18px;border-top:1px solid rgba(255,255,255,.1);color:#AEB6CA;font-size:14px;line-height:1.7}
.resultbody .rmissing strong{display:block;margin-bottom:7px;color:#FF9A9F;font-size:13px}
.rulefile{background:#fff;border:1.5px solid var(--line);padding:22px 28px;box-shadow:0 16px 44px rgba(40,50,80,.08)}
.rfhead{display:flex;align-items:center;justify-content:space-between;padding-bottom:14px;border-bottom:1.5px solid var(--line)}
.rfhead b{font-family:var(--fm);font-size:14px;letter-spacing:.06em;color:var(--ink)}
.rfhead span{font-family:var(--fm);font-size:11px;color:#5BBA82;background:#E9F8EF;border-radius:999px;padding:5px 9px}
.rflist{display:flex;flex-direction:column;margin-top:4px}
.rfrow{display:grid;grid-template-columns:104px minmax(0,1fr);gap:18px;align-items:baseline;padding:11px 0;border-bottom:1px solid #EEF0F5}
.rfrow:last-child{border-bottom:none}
.rfrow b{font-family:var(--fm);font-size:12px;letter-spacing:.08em;color:#A16BCE}
.rfrow span{font-size:16px;line-height:1.45;color:var(--ink);word-break:keep-all}
.rulefile-demo .axband{margin-top:0}
/* 조건 여섯 장 */
.tools.six .tool{min-height:150px;padding:28px 34px}

/* 실습 질문 두 묶음 */
.asks.qs .aq h4{font-size:21.5px;font-weight:600}
.asks.qs .askcol{gap:12px}
.asks.qs .aq{padding:17px 24px}

/* 이걸 할 수 있게 됩니다 */
.goals{display:flex;flex-direction:column;max-width:1500px}
.goals .pt{padding:34px 0}
.goals .pt h4{font-size:31px}
.goals .pt p{font-size:22px}
"""

REF = {}  # 장 열쇠 → 번호. build_ax.build()가 조립 순서대로 채운다

P1, P2, P3, P4, P5 = ("1부 AI 활용 이해", "2부 같은 자료를 네 가지로", "3부 개인의 요령을 조직의 자산으로",
                          "4부 업무 단위의 AX", "5부 실습과 마무리")

# ── 카드 아이콘. 24×24 선 아이콘, 선 색은 문서 맨 위의 #ig 그라데이션 ──
ICONS = {
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><path d="M12 11.5v1"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-6 7-6s7 2.5 7 6"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14c3 0 5 2 5 5"/>',
    "heart": '<path d="M12 20s-7-4.6-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.4-7 10-7 10z"/>',
    "pen": '<path d="M4 20l4-1L19 8l-3-3L5 16z"/><path d="M14 7l3 3"/>',
    "eye": '<path d="M2 12s3.5-6 10-6 10 6 10 6-3.5 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "refresh": '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 4v5h-5"/>',
    "alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h.01"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M8.5 7.5L20 19M8.5 16.5L20 5"/>',
    "network": '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M12 11.5L6.5 17M12 11.5l5.5 5.5"/>',
    "repeat": '<path d="M17 2l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/>',
    "form": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M9 10v10"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "checkx": '<path d="M3 13l3 3 5-6"/><path d="M14 8l6 6M20 8l-6 6"/>',
    "ruler": '<rect x="2" y="9" width="20" height="6" rx="1"/><path d="M6 9v3M10 9v3M14 9v3M18 9v3"/>',
    "star": '<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
    "search": '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
    "toolbox": '<rect x="3" y="8" width="18" height="12" rx="2"/><path d="M8 8V5h8v3M3 13h18"/>',
    "pin": '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"/><circle cx="12" cy="10" r="2.2"/>',
    "book": '<path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "file": '<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h12l-2 4 2 4H5"/>',
    "battery": '<rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 10v4M6 11v2M10 11v2"/>',
    "scale": '<path d="M12 3v18M6 21h12"/><path d="M4 8h16"/><path d="M7 8l-3 6a3 3 0 0 0 6 0zM17 8l-3 6a3 3 0 0 0 6 0z"/>',
    "missing": '<rect x="4" y="4" width="16" height="16" rx="2" stroke-dasharray="3 3"/><path d="M12 8v8M8 12h8"/>',
    "stamp": '<path d="M8 13V9a4 4 0 0 1 8 0v4"/><rect x="4" y="13" width="16" height="4" rx="1"/><path d="M6 20h12"/>',
    "message": '<path d="M4 5h16v11H9l-5 4z"/>',
    "editdoc": '<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5"/><path d="M9 16l6-6"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "table": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M3 15h18M9 4v16M15 4v16"/>',
    "chart": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 16v-5M12 16V8M17 16v-3"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/>',
}


def icon(name):
    """카드 위에 놓는 선 아이콘. 이름이 없으면 빈 문자열."""
    if not name:
        return ""
    return f'<svg class="ci" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


ARROW = ('<div class="baarrow"><span><svg viewBox="0 0 24 24">'
         '<path d="M4 12h15M13 6l6 6-6 6"/></svg></span></div>')


def vs(left_head, right_head, rows):
    """왼쪽과 오른쪽을 한 줄씩 맞세우는 표. rows는 ((l_h4, l_p), (r_h4, r_p)) 목록."""
    cells = [f'<div class="vh">{left_head}</div><div></div><div class="vh r">{right_head}</div>']
    for (lh, lp), (rh, rp) in rows:
        lp_html = f'<p>{lp}</p>' if lp else ''
        rp_html = f'<p>{rp}</p>' if rp else ''
        cells.append(f'<div class="vc"><h4>{lh}</h4>{lp_html}</div>'
                     '<div class="vne">&ne;</div>'
                     f'<div class="vc r"><h4>{rh}</h4>{rp_html}</div>')
    return f'<div class="vs">{"".join(cells)}</div>'


def stepflow(steps, hot=()):
    nodes = "".join(f'<div class="stepn{" hot" if i in hot else ""}"><b>{i:02d}</b><h4>{t}</h4><p>{d}</p></div>'
                    for i, (t, d) in enumerate(steps, 1))
    return f'<div class="steps">{nodes}</div>'


def cards(items, label, cls="", icons=None):
    icons = icons or [None] * len(items)
    nodes = "".join(f'<div class="axstep">{icon(ic)}<b>{label} {i}</b><h4>{t}</h4><p>{d}</p></div>'
                    for i, ((t, d), ic) in enumerate(zip(items, icons), 1))
    return f'<div class="axlad {cls}">{nodes}</div>'


def paper(tag, items, role, after=False, two=False):
    cls = "paper after" if after else "paper"
    ul = "plist two" if two else "plist"
    lis = "".join(f'<li>{x}</li>' for x in items)
    return f'<div class="{cls}"><div class="ptag">{tag}</div><ul class="{ul}">{lis}</ul><div class="prole">{role}</div></div>'


def band(html, top=0):
    style = f' style="margin-top:{top}px"' if top else ''
    return f'<div class="axband"{style}>{html}</div>'


def make(wide, split):
    """build_ax의 조립 함수를 받아 장 함수를 돌려준다. 순환 참조를 피하려는 구조다."""

    # ── 3장. 이걸 할 수 있게 됩니다 ───────────────────────────────────
    def goals(n):
        items = [("내 업무 하나를 AI가 맡을 단계와 내가 검수할 단계로 나눕니다",
                  "연말 캠페인 기획이든 월간 보고서든, 어디까지 맡기고 어디서부터 직접 볼지 정합니다."),
                 ("내가 만든 AI 결과물을 동료가 그대로 쓸 수 있는지 판단합니다",
                  "나에게만 잘 맞는 결과물과 재단이 다시 쓸 수 있는 결과물을 구별합니다."),
                 ("각자 달라도 되는 취향과 재단이 함께 지켜야 할 기준을 나눕니다",
                  "문체와 배치는 달라도 되고, 정확성과 개인정보와 책임은 같아야 합니다.")]
        html = "".join(f'<div class="pt"><b>{i:02d}</b><div><h4>{t}</h4><p>{d}</p></div></div>'
                       for i, (t, d) in enumerate(items, 1))
        inner = f'<div class="vcen"><div class="points goals">{html}</div></div>'
        return wide(n, P1, "시작", '끝나면 <span class="gt">이걸 할 수 있게</span> 됩니다',
                    "끝나면 할 수 있게 되는 것 세 가지",
                    "AI 사용법 대신 내 업무를 나누는 법을 봅니다. 끝나고 나면 아래 세 가지를 직접 할 수 있습니다.",
                    inner, "")

    # ── 5장. AI는 왜 내 말을 잘 들을까 ────────────────────────────────
    def s1(n):
        items = [("이미 앞선 능력은 많습니다", "읽고, 비교하고, 만들고, 반복하는 일은 AI가 사람보다 빠르고 넓게 처리합니다."),
                 ("하지만 사람은 전부를 끌어내지 못합니다", "무엇을 원하는지, 어디까지 맡길지, 어떤 기준으로 고칠지 충분히 지시하지 못합니다."),
                 ("그래서 아직 추월을 못 느낍니다", "AI의 능력이 낮아서가 아니라, 사람이 꺼내 쓰는 폭이 좁기 때문입니다.")]
        inner = ('<div class="vcen">' + cards(items, "이유", "three", ["user", "pen", "heart"])
                 + band('<strong>AI는 점점 더 쉽게 쓰도록 바뀔 것입니다.</strong> 그때 남는 질문은 이것입니다. 사람이 지시하지 않은 것까지 AI가 더 잘해낼 수 있을까요?')
                 + '</div>')
        return wide(n, P1, "AI 능력과 사람의 지시", 'AI가 사람의 능력을 아득히 추월했다는데,<br>주변을 둘러보면 <span class="gt">왜 아직 와닿지 않을까요?</span>',
                    "이미 앞선 AI가 아직 체감되지 않는 이유",
                    "AI는 이미 많은 작업에서 사람을 앞섰습니다. 다만 사람의 지시가 AI의 능력을 다 끌어내지 못하고 있어, 우리는 그 차이를 아직 일상에서 충분히 보지 못합니다.",
                    inner, "")

    # ── 6장. 내 마음에 든 결과물, 동료도 만족할까 ─────────────────────
    def s2(n):
        me = paper("만든 사람 눈에는",
                   ["왜 이렇게 만들었는지 이미 압니다", "익숙한 용어와 작업 순서를 압니다",
                    "빈 곳을 머릿속으로 채워서 읽습니다", "어디를 고치면 되는지 압니다"],
                   "그래서 만족스럽습니다")
        other = paper("옆자리 동료 눈에는",
                      ["왜 이렇게 만들었는지 알기 어렵습니다", "사용법과 전제를 다시 배워야 합니다",
                       "빈 곳이 그대로 보입니다", "결국 만든 사람에게 다시 물어봅니다"],
                      "그래서 다시 일이 됩니다", after=True)
        shots = ('<div class="mineart">'
                 '<div class="m1"><img src="assets/refs/yt_claudecode.jpg" alt="AI 도구를 소개하는 영상 갈무리"></div>'
                 '<div class="m2"><img src="assets/refs/card_team4.jpg" alt="AI 활용법을 정리한 카드뉴스 갈무리"></div>'
                 '</div>')
        inner = (f'<div class="minewrap">{shots}<div class="balist">{me}{ARROW}{other}</div></div>'
                 + band('<strong>내가 만족했다는 것은 검수의 끝이 아니라 첫 신호입니다.</strong> '
                        '동료가 읽고, 쓰고, 고치고, 다시 쓸 수 있어야 재단의 결과물입니다.', 26))
        return wide(n, P1, "개인 최적화의 함정", '내 마음에 쏙 드는 내손내만 AI 결과물,<br>옆자리 동료도 <span class="gt">만족할까요?</span>',
                    "내 마음에 든 결과물과 동료의 눈",
                    "만든 사람은 빈 곳을 머릿속으로 채워서 읽습니다. 동료에게는 그 빈 곳이 그대로 보입니다.",
                    inner, "")

    # ── 7장. 내 컴퓨터에서는 잘 되던 것 ────────────────────────────────
    def s3(n):
        then = paper("만들 때의 나는",
                     ["어떤 파일을 썼는지 알고 있음", "내가 정한 용어와 규칙을 알고 있음",
                      "작업 순서를 기억하고 있음", "왜 이렇게 만들었는지 알고 있음"],
                     "그래서 바로 이어서 쓸 수 있습니다")
        later = paper("시간이 지난 나는",
                      ["어떤 파일을 썼는지 다시 찾아야 함", "용어와 규칙의 의미를 다시 떠올려야 함",
                       "작업 순서를 다시 복원해야 함", "왜 이렇게 만들었는지 다시 해석해야 함"],
                      "그래서 내가 만든 일도 다시 처음부터 읽게 됩니다", after=True)
        inner = (f'<div class="balist">{then}{ARROW}{later}</div>'
                 + band('<strong>결과만 남기면 기억은 사라집니다.</strong> 다시 쓸 수 있으려면 맥락과 기준까지 함께 남아야 합니다.', 34))
        return wide(n, P1, "개인 최적화의 함정", '내가 만든 결과물,<br>한 달 뒤의 나도 <span class="gt">바로 이해할까요?</span>',
                    "한 달 뒤의 내가 내 결과물을 이해하는지",
                    "결과물에는 내용만 남는 게 아닙니다. 그때의 파일, 용어, 순서, 전제도 함께 들어갑니다.",
                    inner, "")

    # ── 24장. AI 답을 믿어도 될까 ─────────────────────────────────────
    def d_trust(n):
        steps = [("질문", "무엇을 왜 물었는지 적어 둡니다."),
                 ("자료", "어떤 원본을 읽혔는지 남깁니다."),
                 ("AI 처리", "어떤 규칙으로 무엇을 했는지 기록합니다."),
                 ("근거", "답이 어느 줄에서 나왔는지 같이 받습니다."),
                 ("담당자 검토", "누가 무엇을 기준으로 봤는지 남깁니다."),
                 ("승인", "누가 승인했는지 이름이 남습니다.")]
        inner = ('<div class="vcen">' + stepflow(steps, hot=(4, 5))
                 + band(f'{REF["a12"]}장의 자연어 질의 화면에서 답마다 근거 표가 붙어 있던 이유입니다. '
                        '<strong>여섯 가지가 남아 있으면 틀렸을 때 어디서 틀렸는지 찾아 되돌릴 수 있습니다.</strong>')
                 + '</div>')
        return wide(n, P3, "읽지 않고 넘기는 문제", 'AI 답을 <span class="gt">믿어도 될까요?</span>',
                    "AI 답을 믿어도 되는 조건",
                    "AI 답은 그럴듯하지만 항상 맞지는 않습니다. 믿으려면 어디서 나왔는지 따라갈 수 있어야 합니다. "
                    "질문부터 승인까지 여섯 가지가 남아 있는지 확인합니다.",
                    inner, "")

    # ── 26장. 내 규칙 파일을 동료가 쓰려면 ────────────────────────────
    def d_reuse(n):
        rows = [("목적", "후원자에게 월간 캠페인 결과를 알린다"),
                ("사용자와 대상", "홍보팀 작성자 → 후원자"),
                ("자료와 전제", "캠페인 보고서, 후원자 정보, 발송 일정"),
                ("작성 순서", "사실 확인 → 초안 → 금지 표현 검사 → 승인"),
                ("통과와 금지", "수치 근거 필수, 개인정보와 존엄성 훼손 금지"),
                ("수정과 책임", "홍보팀 작성, 담당자 검토, 팀장 승인")]
        file_rows = "".join(f'<div class="rfrow"><b>{label}</b><span>{value}</span></div>'
                            for label, value in rows)
        inner = ('<div class="vcen rulefile-demo"><div class="rulecompare">'
                 '<div class="resultonly"><div class="resultbar"><i></i><span>AI 결과만 남긴 경우</span></div>'
                 '<div class="resultbody"><span class="rlabel">AI OUTPUT</span>'
                 '<div class="rbubble">4월 후원 캠페인 결과를 정리했습니다.</div>'
                 '<div class="rmissing"><strong>빠진 것</strong>왜 만들었는지, 누가 쓰는지, 무엇을 지켜야 하는지 알 수 없습니다.</div>'
                 '</div></div>'
                 '<div class="rulefile"><div class="rfhead"><b>캠페인_문안_검토_규칙.md</b><span>다시 사용 가능</span></div>'
                 f'<div class="rflist">{file_rows}</div></div>'
                 '</div>'
                 + band('<strong>결과는 복사할 수 있지만, 의도는 문서로 남겨야 다음 사람이 이어서 씁니다.</strong>')
                 + '</div>')
        return wide(n, P3, "의도부채를 막는 규칙 파일", '의도부채를 막으려면<br><span class="gt">무엇을 더 적어야 할까요?</span>',
                    "결과와 함께 남겨야 할 여섯 가지",
                    "프롬프트와 결과만 복사해 주는 것으로는 부족합니다. 왜 이렇게 만들었고, 누가 쓰고, 무엇을 지키려 했는지와 통과 기준을 함께 적어야 합니다.",
                    inner, "")

    # ── 28장. 어떤 AI를 구독할지보다 어떤 업무를 바꿀지 ───────────────
    def d_unit(n):
        rows = [(("어떤 AI를 도입할까요", "도구 목록에서 시작합니다."),
                 ("어떤 업무의 병목을 줄일까요", "업무 흐름에서 시작합니다.")),
                (("누가 사용할까요", "교육 대상을 정합니다."),
                 ("누가 검토하고 누가 결정할까요", "역할과 책임을 다시 나눕니다.")),
                (("얼마나 빨라지나요", "속도를 잽니다."),
                 ("무엇이 파일로 남아 다음에도 쓰이나요", "남는 자산을 봅니다."))]
        inner = (vs("도구에서 시작하면", "업무에서 시작하면", rows)
                 + band('<strong>업무 하나를 조사, 전략, 제작, 검수 네 역할로 다시 그리는 것이 그 예입니다.</strong>', 30))
        return wide(n, P4, "기준 세우기", '어떤 AI를 구독할지보다<br><span class="gt">어떤 업무를 바꿀지</span>가 먼저입니다',
                    "어떤 AI보다 어떤 업무",
                    "AX는 ChatGPT나 자동화 도구를 들여오는 일이 아닙니다. 업무 하나가 어떻게 시작되고, "
                    "누가 자료를 모으고, 어디서 검토하고, 누가 결정하는지 다시 그리는 일입니다.",
                    inner, "")

    # ── 29장. 다 똑같이 만들어야 할까 ─────────────────────────────────
    def d_share(n):
        taste = paper("각자 달라도 되는 것",
                      ["표현 방식", "색과 배치", "문장 길이와 어조", "작업 순서", "개인 취향"],
                      "손맛입니다. 표준화하지 않습니다", two=True)
        rule = paper("누가 만들어도 같아야 하는 것",
                     ["업무 목적", "대상과 사용자", "정확성", "존엄성", "개인정보와 보안", "재사용성", "검수와 책임"],
                     "위생 기준입니다. 문서로 남기고 공유합니다", after=True, two=True)
        inner = (f'<div class="balist">{taste}{ARROW}{rule}</div>'
                 + band('<strong>똑같이 만들 필요는 없지만, 무엇을 지켜야 하는지는 함께 알아야 합니다.</strong>', 34))
        return wide(n, P4, "기준 세우기", '다 <span class="gt">똑같이</span> 만들어야 할까요?',
                    "취향과 기준을 나누는 법",
                    "아닙니다. 표현과 배치와 어조는 각자 달라도 됩니다. 다만 목적, 대상, 정확성, 존엄성, 개인정보, "
                    "재사용, 검수와 책임은 누가 만들어도 같아야 합니다.",
                    inner, "")

    # ── 30장. 어떤 일부터 맡길까 ──────────────────────────────────────
    def d_check(n):
        items = [("자주 반복되나요", "매달 매년 돌아오는 일이 먼저입니다. 한 번뿐인 일은 설명하는 시간이 더 듭니다."),
                 ("형식이 분명한가요", "넣는 것과 나오는 것의 형식이 정해진 보고서와 정리표가 여기 해당합니다."),
                 ("결과를 확인할 수 있나요", "맞는지 담당자가 볼 수 있어야 합니다. 볼 수 없는 일은 맡기지 않습니다."),
                 ("틀려도 감당되나요", "지원받는 분에게 닿는 문장은 틀리면 큰일입니다. 마지막까지 담당자가 읽습니다.")]
        inner = ('<div class="vcen">' + cards(items, "질문", "", ["repeat", "form", "check", "shield"])
                 + band('<strong>반복되고 형식이 있고 확인할 수 있는 일부터 맡깁니다.</strong> 틀리면 큰일 나는 판단은 담당자가 끝까지 봅니다.')
                 + '</div>')
        return wide(n, P4, "기준 세우기", '어떤 일부터 <span class="gt">AI에게 맡길까요?</span>',
                    "AI에게 먼저 맡길 일 고르기",
                    "네 가지만 물어보면 됩니다. 자주 반복되는지, 형식이 분명한지, 결과를 확인할 수 있는지, 틀려도 감당되는지.",
                    inner, "")

    # ── 31장. 빠르게 나온 답이 좋은 답일까 ────────────────────────────
    def d_speed(n):
        rows = [(("반응이 좋은 문구", "클릭과 공유가 많이 나오는 표현"),
                 ("당사자를 존중하는 문구", "사연 속 당사자가 읽어도 괜찮은 표현")),
                (("후원 전환율이 높은 사연", "숫자가 잘 나오는 사연"),
                 ("실제로 도움이 급한 사연", "숫자가 잘 나오지 않아도 사정이 급한 사람")),
                (("자동화할 수 있는 일", "기술로 가능한 범위"),
                 ("자동화해도 되는 일", "해도 된다고 재단이 정한 범위"))]
        inner = (vs("빠른 답이 고르는 쪽", "좋은 결정이 보는 쪽", rows)
                 + band('<strong>효율만 좇으면 놓치는 것이 있습니다.</strong> 답이 나온 뒤에 담당자가 읽는 시간까지가 일입니다.', 30))
        return wide(n, P4, "기준 세우기", 'AI가 빠르게 해결해 준 답이<br><span class="gt">좋은 답</span>일까요?',
                    "빠른 답과 좋은 결정의 차이",
                    "AI는 답이 나오기까지 걸리는 시간을 크게 줄입니다. 다만 그 답을 사연 속 당사자가 어떻게 받아들일지는 담당자가 직접 읽어 봐야 압니다.",
                    inner, "")

    # ── 32장. 공익 조직이라서 더 지켜야 할 것 ─────────────────────────
    def d_rules(n):
        rules = [("사람을 데이터로만 보지 않기", "캠페인 레이스의 막대 하나하나가 한 사람의 사연입니다."),
                 ("개인정보와 민감정보는 빼고 읽히기", "캠페인 이름 속 당사자 이름부터 지우고 넘깁니다."),
                 ("동의한 목적 안에서만 쓰기", "받을 때 밝힌 목적을 벗어나지 않습니다."),
                 ("AI가 만든 부분을 밝히기", "어디까지 AI가 썼는지 후원자와 동료에게 알립니다."),
                 ("약한 사람에게 불리한 편향 점검하기", "반응 좋은 사연만 남는지 살핍니다."),
                 ("책임자를 사람으로 정하기", "AI가 만든 결과라도 책임자 이름은 사람입니다."),
                 ("자동화하지 않을 권리 두기", "할 수 있어도 하지 않기로 정할 수 있습니다.")]
        html = "".join(f'<div class="hf"><span>원칙 {i:02d}</span><b>{t}</b><p>{d}</p></div>'
                       for i, (t, d) in enumerate(rules, 1))
        html += ('<div class="hf hot"><span>한 줄로</span>'
                 '<p>효율성은 공익성을 대신할 수 없고, 공익성은 효율성 덕분에 더 넓어질 수 있습니다.</p></div>')
        inner = f'<div class="hfacts four">{html}</div>'
        return wide(n, P4, "기준 세우기", '공익 조직이라서 <span class="gt">더 지켜야 할 것</span>',
                    "공익 조직이 더 지켜야 할 일곱 가지",
                    "재단이 다루는 자료에는 사람의 이름과 사정이 들어 있습니다. 효율보다 앞서는 기준 일곱 가지입니다.",
                    inner, "")

    # ── 33장. 90일이면 업무 하나가 팀 표준이 된다 ─────────────────────
    def d_plan(n):
        cols = [("30일", "관찰하고 적기",
                 ["반복 업무 3개 고르기", "지금 업무 흐름 기록하기", "자료와 규칙 모으기", "개인정보와 위험 요소 확인하기"]),
                ("60일", "나누고 돌려 보기",
                 ["한 업무를 AI 역할과 담당자 역할로 나누기", "작은 시험 운영 돌리기", "검토 기준과 승인 절차 적기", "결과와 실패 사례 기록하기"]),
                ("90일", "표준으로 남기기",
                 ["검증된 업무를 팀 표준으로 바꾸기", "규칙 파일과 서식과 설명서로 저장하기", "담당자와 책임자 정하기", "다음 업무로 넓히기"])]
        html = "".join(f'<div class="tocol"><h3><b>{d}</b>{t}</h3><ul>'
                       + "".join(f'<li><b>{j:02d}</b>{it}</li>' for j, it in enumerate(items, 1))
                       + '</ul></div>' for d, t, items in cols)
        inner = (f'<div class="toc deep">{html}</div>'
                 + band('<strong>AX는 한 번 하고 끝나는 도입 사업이 아니라, 일을 관찰하고 나누고 다시 배우는 운영 방식입니다.</strong>', 30))
        return wide(n, P4, "조직 움직이기", '90일이면 업무 하나가 <span class="gt">팀 표준</span>이 됩니다',
                    "90일 실행 순서",
                    "큰 도입 계획보다 업무 하나를 끝까지 돌려 보는 편이 빠릅니다. 30일 관찰, 60일 시험 운영, 90일 표준입니다.",
                    inner, "")

    # ── 35장. 넘기기 전에 묻는 것 ─────────────────────────────────────
    def practice_q(n):
        def col(cls, mark, title, items):
            body = "".join(f'<div class="aq"><h4>{q}</h4></div>' for q in items)
            return f'<div class="askcol {cls}"><div class="ah"><i>{mark}</i>{title}</div>{body}</div>'
        split_q = ["이 업무의 목적은 무엇일까요",
                   "AI가 반드시 알아야 하는 맥락은 무엇일까요",
                   "AI가 틀렸을 때 가장 위험한 대목은 어디일까요",
                   "담당자가 반드시 직접 판단해야 하는 지점은 어디일까요",
                   "이 업무가 끝난 뒤 무엇이 재단의 자산으로 남아야 할까요"]
        hand_q = ["만든 사람이 없어도 동료가 쓸 수 있을까요",
                  "처음 보는 사람이 목적과 사용법을 이해할 수 있을까요",
                  "만든 사람의 취향과 재단이 지켜야 할 기준이 나뉘어 있을까요",
                  "동료가 평가할 수 있는 품질 기준이 있을까요",
                  "실제 사용자나 동료에게 보여 주고 검증했을까요",
                  "결과물과 함께 어떤 설명서와 예시와 검수 기준을 남겨야 할까요"]
        inner = ('<div class="asks qs">'
                 + col("no", "1", "업무를 나눌 때 묻는 것", split_q)
                 + col("yes", "2", "동료에게 넘길 때 묻는 것", hand_q)
                 + '</div>')
        return wide(n, P5, "실습", '동료에게 넘기기 전에<br>이 <span class="gt">여섯 가지</span>를 물어봅니다',
                    "동료에게 넘기기 전에 묻는 것",
                    "왼쪽은 업무를 나눌 때, 오른쪽은 결과를 동료에게 넘길 때 묻습니다. 오른쪽에 답이 없으면 아직 개인 결과물입니다.",
                    inner, "")

    return {"goals": [goals], "trait": [s1, s2, s3], "trust": [d_trust], "reuse": [d_reuse],
            "direction": [d_unit, d_share, d_check, d_speed, d_rules, d_plan], "practice_q": [practice_q]}
