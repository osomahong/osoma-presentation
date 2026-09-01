"""2026-08-27에 더한 장 23개.

조직이 AX에서 막히는 단계, 읽지 않고 넘기는 문제, 기록을 모으는 일, 검증 기준의 모양, 머릿속 기준을 꺼내는
역할 바꾸기, 변화관리와 리더의 몫, 전문성이 더 중요해지는 이유를 다룬다. 다른 조직의 사례는 조직
이름 없이 내용만 쓴다. 조립 순서는 build_ax.py가 정하고, 다른 장의 번호는 REF로 받는다.
"""
from build_ax_deep import (P1, P2, P3, P4, P5, ARROW, REF, vs, stepflow, cards, paper, band)

ADD_CSS = """
/* 왼쪽 그림 한 장과 오른쪽 진단 넷.
   카드가 넷이라 원본 덱의 큰 제목으로는 높이가 모자란다. 이 장에서만 제목과 리드를 한 단계 줄인다 */
.slide:has(.cwrap) h2.head{font-size:56px}
.slide:has(.cwrap) .lead{font-size:23px;margin-top:18px}
.cwrap{display:grid;grid-template-columns:.88fr 1.12fr;gap:48px;flex:1;min-height:0;margin-top:30px;align-items:stretch}
/* 그림 자리. assets/illus/s08.png 를 갈아 끼우면 바뀐다. 권장 비율은 5:4 */
.cshot{min-height:0;border-radius:26px;overflow:hidden;background:#0B1224;
  box-shadow:0 20px 50px rgba(20,25,40,.22)}
.cshot img{width:100%;height:100%;object-fit:cover;display:block}
.creply{display:flex;flex-direction:column;justify-content:center;gap:14px}
.crow{background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:20px 30px;
  box-shadow:0 10px 28px rgba(40,50,80,.05)}
.crow:first-child{border:2px solid transparent;
  background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box;box-shadow:0 16px 38px rgba(200,90,120,.14)}
.cjob{font-family:var(--f);font-size:15px;font-weight:700;letter-spacing:.02em;color:var(--faint);margin-bottom:7px}
.crow h4{font-size:22px;font-weight:800;line-height:1.4}
.crow p{margin-top:8px;font-size:17.5px;line-height:1.55;color:var(--dim)}
/* 더닝크루거 곡선과 다섯 단계를 좌우로 놓는다. 곡선 위 번호가 오른쪽 줄의 번호와 같다.
   원 도식은 Kruger와 Dunning의 1999년 연구에서 이름을 딴 것이고, 구간 이름은 널리 쓰이는 표기를 따랐다. */
.dkwrap{display:grid;grid-template-columns:1fr 1.04fr;gap:44px;flex:1;min-height:0;
  align-items:center;margin-top:26px}
.dkcurve{display:block;width:100%;height:auto;max-height:100%}
.dknum{font-family:var(--fm);font-size:19px;font-weight:700;fill:var(--dim);text-anchor:middle}
.dkz{font-size:17px;fill:var(--faint);text-anchor:middle;font-family:var(--f)}
.dkax{font-family:var(--fm);font-size:15px;letter-spacing:.12em;fill:var(--faint)}
.dkax.r{text-anchor:end}
.dkrows{display:flex;flex-direction:column;justify-content:center;gap:14px;min-height:0}
.dkrow{display:grid;grid-template-columns:50px 1fr;gap:20px;align-items:center;
  background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:16px 26px;
  box-shadow:0 8px 22px rgba(40,50,80,.05)}
.dkrow b{display:grid;place-items:center;width:50px;height:50px;border-radius:50%;
  font-family:var(--fm);font-size:17px;font-weight:700;color:#fff;background:var(--grad);
  box-shadow:0 8px 20px rgba(200,90,120,.22)}
.dkrow h4{font-size:23px;font-weight:800;line-height:1.35}
.dkrow p{margin-top:6px;font-size:17.5px;line-height:1.5;color:var(--dim)}

/* 37장. 왼쪽에 그림 한 장, 오른쪽에 만들 수 있는 것과 내보낼 것.
   그림은 assets/illus/s37.png 를 갈아 끼우면 바뀐다. 가로로 긴 판이라 권장 비율은 1.94:1.
   비율을 바꾸려면 .lessart 의 aspect-ratio 만 그림에 맞춘다 */
.lesswrap{display:grid;grid-template-columns:auto 1fr;gap:44px;flex:1;min-height:0;
  align-items:stretch;margin-top:24px}
.lessart{align-self:center;width:820px;aspect-ratio:1400/723;border-radius:22px;overflow:hidden;
  background:#EDF0F6;box-shadow:0 18px 44px rgba(20,25,40,.18)}
.lessart img{width:100%;height:100%;object-fit:cover;display:block}
.lesswrap .balist{margin-top:0;min-height:0}

/* 고리 그래프 */
.jcurve{width:100%;max-width:720px;display:block}
/* 문자 발송의 지금과 뒤 */
.bawrap{display:flex;flex-direction:column;gap:26px;flex:1;justify-content:center;min-height:0}
.baflow{display:grid;grid-template-columns:150px 1fr;align-items:center;gap:20px}
.baflow .bfl{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.16em;color:var(--faint);line-height:1.6}
.baflow.after .bfl{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.baflow .stepn b{width:54px;height:54px;font-size:17px}
.baflow .stepn::before{top:27px}
.baflow .stepn h4{font-size:21px;margin-top:14px}
.baflow .stepn p{font-size:17px;margin-top:8px}
.baflow:not(.after) .stepn b{background:#DDE1EA;color:var(--dim)}
.baflow:not(.after) .stepn::before{background:#E5E8EF}
/* 하루 8시간 막대 */
.hours{display:flex;flex-direction:column;gap:30px;margin-top:40px;flex:1;justify-content:center}
.hrow{display:grid;grid-template-columns:150px 1fr;align-items:center;gap:28px}
.hrow .hl{font-size:22px;font-weight:800;color:var(--dim)}
.hrow.after .hl{color:var(--ink)}
.hbar{display:flex;height:96px;border-radius:20px;overflow:hidden;border:1.5px solid var(--line)}
.hbar span{display:grid;place-items:center;font-size:22px;font-weight:700;color:var(--dim);background:#F1F3F7}
.hbar span.judge{background:linear-gradient(120deg,#FFE7D2,#FFDDE7);color:var(--ink)}
.hrow.after .hbar span.judge{background:var(--grad);color:#fff}
/* 지시문 상자 */
.promptbox .tbody{font-size:19px;line-height:1.85;white-space:normal}
/* 규칙 파일. 터미널 판을 그대로 쓰되 안은 해야 할 것과 하지 않을 것 두 묶음이다 */
.rulebox .tbody{padding:26px 30px 28px;font-family:var(--f);white-space:normal;line-height:1.6}
.rgrp + .rgrp{margin-top:24px;padding-top:22px;border-top:1px solid rgba(255,255,255,.10)}
.rhead{font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.12em;margin-bottom:14px}
.rhead.ok{color:#6EE7A0}
.rhead.no{color:#FF8A9B}
.rgrp ul{list-style:none;display:flex;flex-direction:column;gap:11px}
.rgrp li{position:relative;padding-left:26px;font-size:18.5px;color:#D6DBE7;word-break:keep-all}
.rgrp li::before{position:absolute;left:0;top:0;font-family:var(--fm);font-weight:700}
.rgrp.y li::before{content:"+";color:#6EE7A0}
.rgrp.n li::before{content:"-";color:#FF8A9B}

/* LLM이 다음 말을 고르며 문장을 만드는 원리 */
.axcols:has(.llmsim){grid-template-columns:.84fr 1.16fr;gap:48px}
.llmsim{background:#111522;color:#F5F7FB;border-radius:24px;padding:24px 26px 20px;
  box-shadow:0 18px 46px rgba(15,23,42,.18);min-width:0}
.simhead{display:flex;align-items:center;justify-content:space-between;font-family:var(--fm);
  font-size:14px;letter-spacing:.08em;color:#F5F7FB}
.simtag{font-size:11px;color:#AEB6CA;border:1px solid #3B4357;border-radius:999px;padding:5px 9px}
/* 시연 시작 단추. 켜자마자 돌지 않고 눌러야 시작한다 */
.simwing{display:flex;align-items:center;gap:12px}
.simplay{width:38px;height:38px;padding:0;border:0;border-radius:50%;background:var(--grad);
  display:grid;place-items:center;cursor:pointer;box-shadow:0 8px 20px rgba(200,90,120,.34);transition:transform .16s}
.simplay svg{width:15px;height:15px;fill:#fff;margin-left:2px}
.simplay .pa{display:none}
.simplay.is-playing .pi{display:none}
.simplay.is-playing .pa{display:block;margin-left:-2px}
.simplay:hover{transform:scale(1.08)}
.simquestion{display:flex;gap:10px;align-items:baseline;margin-top:20px;padding:13px 14px;
  border-radius:11px;background:#1B2232}
.simquestion span{flex:none;font-family:var(--fm);font-size:10px;letter-spacing:.12em;color:#98A3BB}
.simquestion b{min-height:22px;font-size:15px;color:#fff;font-weight:600;word-break:keep-all}
.simoutput{margin-top:22px;padding:18px 18px 16px;border:1px solid #3A4358;border-radius:14px;background:#151B2A}
.simoutput>span,.simcands>span{flex:none;font-family:var(--fm);font-size:11px;
  letter-spacing:.12em;color:#98A3BB}
.simoutput>span{display:block;margin-bottom:9px}
.simoutput strong{display:block;min-height:54px;font-size:22px;line-height:1.45;color:#fff;font-weight:700;word-break:keep-all}
.simcands{margin-top:18px}
.simcands>span{display:block;margin-bottom:8px}
.simcands>div{display:flex;gap:7px;flex-wrap:wrap;min-height:34px}
.simcand{font-family:var(--fm);font-size:12px;color:#CDD5E5;border:1px solid #46516A;border-radius:9px;padding:7px 9px;background:#1A2130}
.simcand{transition:color .25s ease,border-color .25s ease,background .25s ease,transform .25s ease}
.simcand.focus{color:#fff;border-color:#7F8BFF;background:#272D47;transform:translateY(-2px)}
.simcand.pick{color:#fff;border-color:#FF6A76;background:linear-gradient(120deg,#C84C71,#6B4ACB);font-weight:700;transform:translateY(-2px)}
.simstatus{display:flex;align-items:center;gap:8px;margin-top:15px;min-height:18px;font-size:12px;color:#AEB6CA}
.simstatus i{width:7px;height:7px;flex:none;border-radius:50%;background:#FF6A76;box-shadow:0 0 0 4px rgba(255,106,118,.12);animation:simlive 1.15s ease-in-out infinite}
.simstatus span{font-family:var(--fm);letter-spacing:.04em;color:#D9DEEA}
.simstatus b{margin-left:auto;color:#fff;font-weight:600}
.simprogress{display:flex;align-items:center;margin-top:14px}
.simprogress i{height:4px;flex:1;border-radius:4px;background:linear-gradient(90deg,#FF6A76 0 0%,#343D53 0% 100%);transition:background .45s ease}
.simoutput strong::after{content:"▌";display:inline-block;margin-left:3px;color:#FF6A76;animation:simcursor .85s steps(1) infinite}
@keyframes simlive{0%,100%{opacity:.45;transform:scale(.85)}50%{opacity:1;transform:scale(1.1)}}
@keyframes simcursor{0%,45%{opacity:1}46%,100%{opacity:0}}

/* 후반부 핵심 질문 */
.ax.so-what-slide h2.head{font-size:116px;line-height:.92;letter-spacing:-.055em}
.so-what-slide .sowhat-word{display:block;font-family:var(--fm);font-weight:800;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.so-what-slide .sowhat-question{display:block;margin-top:18px;font-family:var(--f);font-size:31px;
  line-height:1.32;letter-spacing:-.025em;color:var(--ink)}
.so-what-slide .lead{margin-top:14px;max-width:1420px}
.so-what-slide .vcen{gap:24px}

/* 설명 문단 대신 일러스트를 세우는 장. 24장, 44장, 53장이 같은 판을 쓴다.
   그림 배경은 순백이라 multiply로 얹으면 카드 그라데이션이 그대로 비친다. */
.sowgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;flex:1 1 auto;min-height:0}
.sowfig{background:linear-gradient(150deg,#FFF7EF,#FBF2F8 45%,#F4F2FD 75%,#EFF5FE);
  border:1.5px solid #EDEAF2;border-radius:26px;padding:22px 30px 32px;
  display:flex;flex-direction:column;min-height:0}
.sowart{flex:1 1 auto;min-height:0;display:flex;align-items:center;justify-content:center}
.sowart img{max-width:100%;max-height:100%;object-fit:contain;mix-blend-mode:multiply}
.sowcap{flex:none;text-align:center}
.sowcap b{font-family:var(--fm);font-size:18px;font-weight:700;letter-spacing:.12em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.sowcap h4{margin-top:12px;font-size:30px;font-weight:800;letter-spacing:-.03em;line-height:1.34;color:var(--ink)}
.sowcap p{margin-top:12px;font-size:19.5px;line-height:1.5;color:var(--dim)}
/* 다섯 칸으로 서면 칸 폭이 절반 가까이 줄어 글자와 여백을 함께 줄인다.
   칸이 남는 높이를 다 먹으면 홀쭉해져서, 여기서는 그림 크기에 맞춰 칸 높이를 정하고 가운데에 둔다. */
/* 어두운 그림을 세울 때. 곱하기로 얹지 않고 제 배경째 액자에 넣는다 */
.sowgrid.shot .sowart{border-radius:18px;overflow:hidden;background:#06080E}
.sowgrid.shot .sowart img{width:100%;height:100%;max-width:none;max-height:none;
  object-fit:contain;mix-blend-mode:normal}
.sowgrid.five{grid-template-columns:repeat(5,1fr);gap:18px;flex:0 0 auto}
.sowgrid.five .sowfig{padding:14px 14px 24px;border-radius:22px;min-height:430px}
.sowgrid.five .sowcap b{font-size:16px}
.sowgrid.five .sowcap h4{margin-top:10px;font-size:25px;line-height:1.32}

/* ── 부채 세 가지를 각각 네 컷으로 푸는 장 ──────────────────────────
   왼쪽에 제목과 마무리, 오른쪽에 2×2 만화를 둔다. 네 컷을 가로로 한 줄에 늘어놓으면
   컷이 납작해져서 장면이 읽히지 않는다. 말풍선은 그림에 그리지 않고 여기서 얹는다.
   한글을 그림 생성에 맡기면 글자가 깨지고, 문안을 고칠 때마다 그림을 다시 뽑아야 해서다. */
.toon-slide .fg{display:grid;grid-template-columns:560px 1fr;column-gap:64px;
  grid-template-rows:auto auto auto 1fr;align-content:start}
.toon-slide .fg > .kicker{grid-area:1/1}
.toon-slide .fg > .head{grid-area:2/1;font-size:56px;line-height:1.16}
.toon-slide .fg > .lead{grid-area:3/1;max-width:none}
.toon-slide .fg > .axband{grid-area:4/1;align-self:start;margin-top:38px;font-size:21px}
.toon-slide .fg > .toonwrap, .toon-slide .fg > .toonpage{grid-area:1/2/5/3;align-self:center}

/* 네 컷이 한 장에 들어간 판. 말풍선은 그림 전체를 기준으로 %로 앉힌다 */
.toonpage{position:relative;border-radius:20px;overflow:hidden;
  border:1.5px solid #E4E1EA;box-shadow:0 14px 34px rgba(30,40,60,.12)}
.toonpage img{width:100%;height:auto;display:block}
/* 여기서는 --x, --y가 그림 전체에서 말풍선 왼쪽 위 모서리 자리다.
   t와 b는 꼬리가 아래를 향하는지 위를 향하는지만 정한다 */
.toonpage .bub{left:var(--x);top:var(--y);right:auto;bottom:auto}

.toonwrap{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.toonpanel{position:relative;aspect-ratio:4/3;border-radius:20px;overflow:hidden;
  border:1.5px solid #E4E1EA;background:#fff;box-shadow:0 14px 34px rgba(30,40,60,.12)}
.toonpanel img{width:100%;height:100%;object-fit:cover;display:block}
.cutno{position:absolute;left:14px;top:13px;z-index:2;font-family:var(--fm);font-size:15px;font-weight:700;
  letter-spacing:.08em;color:#fff;background:rgba(20,24,36,.6);padding:5px 11px;border-radius:999px}

/* 말풍선. 자리는 컷마다 정하고, 꼬리는 위아래 방향만 바꾼다 */
/* 자리와 크기는 컷마다 --x, --y, --w로 조정한다. 값이 없으면 아래 기본값을 쓴다 */
.bub{position:absolute;z-index:3;max-width:var(--w,78%);font-size:20px;line-height:1.4;font-weight:700;
  color:#1F2430;background:#fff;padding:12px 16px;border-radius:20px;
  box-shadow:0 8px 22px rgba(20,30,50,.18)}
/* 꼬리는 두 겹으로 그린다. 아래가 테두리색, 위가 말풍선 바탕색이다.
   --tail은 말풍선 가로 폭에서 꼬리가 붙는 자리다. 화자 쪽으로 옮겨 누가 말하는지 가리킨다. */
.bub::before,.bub::after{content:"";position:absolute;width:0;height:0;border-style:solid;
  border-color:transparent;left:var(--tail,24%);transform:translateX(-50%)}
.bub::before{display:none;border-width:14px}
.bub::after{border-width:11px}
.bub.t{top:var(--y,54px)}
.bub.b{bottom:var(--y,18px)}
.bub.l{left:var(--x,16px)}
.bub.r{right:var(--x,16px)}
.bub.t::after{top:100%;border-bottom-width:0;border-top-color:#fff}
.bub.b::after{bottom:100%;border-top-width:0;border-bottom-color:#fff}
.bub.t::before{top:100%;border-bottom-width:0}
.bub.b::before{bottom:100%;border-top-width:0}
/* 사람이 없는 컷에는 말풍선 대신 네모 자막을 둔다 */
.bub.narr{max-width:66%;font-weight:600;background:#FFF6E8;border-radius:8px;box-shadow:0 8px 20px rgba(60,45,20,.16)}
.bub.narr::before,.bub.narr::after{display:none}

/* 그림체마다 말풍선 모양을 달리해 세 편이 서로 다른 판으로 읽히게 한다 */
.toonwrap.comic .bub{border:2.5px solid #17171C;border-radius:12px;box-shadow:4px 4px 0 rgba(23,23,28,.9)}
.toonwrap.comic .bub::before{display:block}
.toonwrap.comic .bub.t::before{border-top-color:#17171C}
.toonwrap.comic .bub.b::before{border-bottom-color:#17171C}
.toonwrap.webtoon .bub{border-radius:24px}
.toonwrap.novel .bub{border:1.8px solid #2C3A42;border-radius:6px;box-shadow:0 6px 16px rgba(44,58,66,.18)}
.toonwrap.novel .bub::before{display:block}
.toonwrap.novel .bub.t::before{border-top-color:#2C3A42}
.toonwrap.novel .bub.b::before{border-bottom-color:#2C3A42}
"""


def illus(items, label, cls=""):
    """설명 문단 대신 일러스트를 세운 칸을 만든다.

    items는 (파일 이름, 대체 텍스트, 헤더, 헤더 아래 한 줄) 순서다. 마지막 항목은 비워도 된다.
    파일은 assets/illus 아래에 있고, prep_illus.py가 배경을 순백으로 맞춰 둔 것을 쓴다.
    """
    cells = []
    for i, item in enumerate(items, 1):
        f, alt, head = item[:3]
        sub = item[3] if len(item) > 3 else ""
        cells.append(f'<div class="sowfig">'
                     f'<div class="sowart"><img src="assets/illus/{f}.png" alt="{alt}"></div>'
                     f'<div class="sowcap"><b>{label} {i}</b><h4>{head}</h4>'
                     + (f'<p>{sub}</p>' if sub else '')
                     + '</div></div>')
    return f'<div class="sowgrid {cls}">' + "".join(cells) + '</div>'


def toon(name, style, cuts):
    """부채 하나를 네 컷 만화로 푼다.

    cuts는 (대체 텍스트, 말풍선 문안, 말풍선 자리, 미세 조정) 순서다. 마지막은 없어도 된다.
    자리는 t와 b로 위아래를, l과 r로 좌우를 정한다. 사람이 없는 컷은 narr를 더해 네모 자막이 된다.
    미세 조정은 {"tail": "70%", "x": "12%", "y": "8%", "w": "52%"} 꼴로 준다.
    tail은 말풍선 폭에서 꼬리가 붙는 자리라, 화자 쪽으로 옮겨 누가 말하는지 가리킨다.
    """
    panels = []
    for i, cut in enumerate(cuts, 1):
        alt, line, pos = cut[:3]
        tune = cut[3] if len(cut) > 3 else {}
        css = "".join(f'--{k}:{v};' for k, v in tune.items())
        panels.append(f'<div class="toonpanel"><span class="cutno">{i:02d}</span>'
                      f'<img src="assets/toon/{name}_{i}.jpg" alt="{alt}">'
                      f'<span class="bub {pos}"{f" style=\'{css}\'" if css else ""}>{line}</span></div>')
    return f'<div class="toonwrap {style}">' + "".join(panels) + '</div>'


# 더닝크루거 곡선. 좌우로 놓는 판이라 폭이 좁아, 굴곡이 눌리지 않게 세로를 키워 그렸다.
DK_CURVE = '<svg class="dkcurve" viewBox="0 0 800 470" role="img"><defs><linearGradient id="dkg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FF7A1A"/><stop offset=".4" stop-color="#FF4D6D"/><stop offset=".72" stop-color="#A855F7"/><stop offset="1" stop-color="#3B82F6"/></linearGradient></defs><line x1="58" y1="388" x2="772" y2="388" stroke="#E9EBF1" stroke-width="2"/><line x1="58" y1="24" x2="58" y2="388" stroke="#E9EBF1" stroke-width="2"/><path d="M58.0 372.0 L61.0 355.1 L64.0 338.7 L66.9 322.8 L69.9 307.2 L72.9 292.1 L75.8 277.5 L78.8 263.3 L81.8 249.6 L84.8 236.3 L87.8 223.4 L90.7 211.0 L93.7 199.0 L96.7 187.5 L99.7 176.4 L102.6 165.8 L105.6 155.6 L108.6 145.9 L111.5 136.6 L114.5 127.7 L117.5 119.3 L120.5 111.3 L123.4 103.8 L126.4 96.8 L129.4 90.1 L132.4 83.9 L135.4 78.2 L138.3 72.9 L141.3 68.1 L144.3 63.7 L147.2 59.7 L150.2 56.2 L153.2 53.1 L156.2 50.5 L159.1 48.3 L162.1 46.6 L165.1 45.3 L168.1 44.4 L171.1 44.0 L174.0 44.1 L177.0 44.8 L180.0 46.1 L182.9 48.1 L185.9 50.6 L188.9 53.8 L191.9 57.6 L194.9 61.9 L197.8 66.8 L200.8 72.2 L203.8 78.1 L206.8 84.5 L209.7 91.4 L212.7 98.7 L215.7 106.4 L218.7 114.5 L221.6 122.9 L224.6 131.6 L227.6 140.5 L230.6 149.7 L233.5 159.0 L236.5 168.5 L239.5 178.1 L242.5 187.7 L245.4 197.4 L248.4 207.0 L251.4 216.6 L254.4 226.1 L257.3 235.4 L260.3 244.5 L263.3 253.4 L266.2 262.0 L269.2 270.4 L272.2 278.4 L275.2 286.0 L278.1 293.2 L281.1 300.0 L284.1 306.3 L287.1 312.1 L290.1 317.4 L293.0 322.2 L296.0 326.4 L299.0 330.1 L302.0 333.1 L304.9 335.6 L307.9 337.4 L310.9 338.6 L313.9 339.1 L316.8 339.2 L319.8 338.9 L322.8 338.5 L325.8 337.9 L328.7 337.1 L331.7 336.0 L334.7 334.8 L337.6 333.4 L340.6 331.8 L343.6 330.1 L346.6 328.2 L349.6 326.1 L352.5 323.8 L355.5 321.4 L358.5 318.9 L361.4 316.2 L364.4 313.4 L367.4 310.5 L370.4 307.5 L373.3 304.4 L376.3 301.2 L379.3 298.0 L382.3 294.7 L385.2 291.3 L388.2 287.9 L391.2 284.5 L394.2 281.1 L397.1 277.7 L400.1 274.3 L403.1 270.9 L406.1 267.6 L409.0 264.3 L412.0 261.1 L415.0 258.0 L418.0 254.9 L420.9 251.9 L423.9 249.1 L426.9 246.3 L429.9 243.7 L432.9 241.2 L435.8 238.9 L438.8 236.7 L441.8 234.7 L444.8 232.8 L447.7 231.1 L450.7 229.6 L453.7 228.3 L456.7 227.1 L459.6 226.2 L462.6 225.4 L465.6 224.9 L468.5 224.5 L471.5 224.4 L474.5 224.5 L477.5 224.9 L480.4 225.6 L483.4 226.6 L486.4 227.8 L489.4 229.4 L492.3 231.1 L495.3 233.0 L498.3 235.1 L501.3 237.3 L504.2 239.6 L507.2 242.0 L510.2 244.3 L513.2 246.7 L516.2 248.9 L519.1 251.0 L522.1 253.0 L525.1 254.9 L528.0 256.5 L531.0 257.8 L534.0 258.9 L537.0 259.7 L540.0 260.3 L542.9 260.5 L545.9 260.4 L548.9 260.3 L551.8 259.9 L554.8 259.5 L557.8 258.9 L560.8 258.1 L563.8 257.3 L566.7 256.3 L569.7 255.1 L572.7 253.8 L575.6 252.4 L578.6 250.9 L581.6 249.3 L584.6 247.5 L587.6 245.6 L590.5 243.6 L593.5 241.5 L596.5 239.3 L599.4 236.9 L602.4 234.5 L605.4 232.0 L608.4 229.4 L611.4 226.7 L614.3 223.9 L617.3 221.0 L620.3 218.1 L623.2 215.1 L626.2 212.0 L629.2 208.8 L632.2 205.7 L635.1 202.4 L638.1 199.1 L641.1 195.8 L644.1 192.5 L647.0 189.1 L650.0 185.7 L653.0 182.3 L656.0 178.9 L659.0 175.5 L661.9 172.1 L664.9 168.6 L667.9 165.2 L670.8 161.9 L673.8 158.5 L676.8 155.2 L679.8 151.9 L682.8 148.7 L685.7 145.5 L688.7 142.3 L691.7 139.2 L694.7 136.2 L697.6 133.3 L700.6 130.4 L703.6 127.6 L706.5 124.8 L709.5 122.2 L712.5 119.7 L715.5 117.2 L718.5 114.9 L721.4 112.6 L724.4 110.5 L727.4 108.5 L730.4 106.5 L733.3 104.8 L736.3 103.1 L739.3 101.5 L742.2 100.1 L745.2 98.8 L748.2 97.6 L751.2 96.6 L754.1 95.7 L757.1 94.9 L760.1 94.3 L763.1 93.8 L766.1 93.5 L769.0 93.3 L772.0 93.2" fill="none" stroke="url(#dkg)" stroke-width="4.6" stroke-linecap="round"/><circle cx="172.2" cy="44.0" r="19" fill="#fff" stroke="url(#dkg)" stroke-width="3.4"/><text x="172.2" y="51.0" class="dknum">1</text><circle cx="315.0" cy="339.2" r="19" fill="#fff" stroke="url(#dkg)" stroke-width="3.4"/><text x="315.0" y="346.2" class="dknum">2</text><circle cx="472.1" cy="224.4" r="19" fill="#fff" stroke="url(#dkg)" stroke-width="3.4"/><text x="472.1" y="231.4" class="dknum">3</text><circle cx="543.5" cy="260.5" r="19" fill="#fff" stroke="url(#dkg)" stroke-width="3.4"/><text x="543.5" y="267.5" class="dknum">4</text><circle cx="686.3" cy="144.8" r="19" fill="#fff" stroke="url(#dkg)" stroke-width="3.4"/><text x="686.3" y="151.8" class="dknum">5</text><text x="143.7" y="414" class="dkz">우매함의 봉우리</text><text x="322.2" y="414" class="dkz">절망의 골짜기</text><text x="507.8" y="414" class="dkz">깨달음의 비탈</text><text x="700.6" y="414" class="dkz">지속의 고원</text><text x="46" y="16" class="dkax">자신감</text><text x="772" y="456" class="dkax r">겪은 시간</text></svg>'


def make(wide, split):
    """build_ax의 조립 함수를 받아 장 함수를 돌려준다."""

    # ── 1부. 조직의 단계 ──────────────────────────────────────────────
    def stages(n):
        steps = [("환호", "계정을 구독하고, 교육을 하고, AX 팀을 만듭니다."),
                 ("정체", "계정을 줬는데 잘 쓰는 팀만 쓰고 나머지는 열어 보지도 않습니다."),
                 ("확산", "재단 자료와 시스템이 AI에 연결되면 개발자가 아닌 사람도 쓰기 시작합니다."),
                 ("의구심", "결과물은 넘치는데 체감이 없고, 검토하지 않은 결과로 사고가 납니다."),
                 ("마지막 고비", "도구를 바꾸는 대신 일하는 순서를 다시 짭니다. 여기를 넘으면 정착합니다.")]
        rows = "".join(f'<div class="dkrow"><b>{i:02d}</b><div><h4>{t}</h4><p>{d}</p></div></div>'
                       for i, (t, d) in enumerate(steps, 1))
        inner = (f'<div class="dkwrap">{DK_CURVE}<div class="dkrows">{rows}</div></div>'
                 + band('더닝크루거 곡선을 조직의 AI 도입에 맞춰 그렸습니다. '
                        '<strong>오늘 이야기는 2단계에서 5단계로 가는 길입니다.</strong>', 24))
        return wide(n, P1, "조직의 단계", '열매나눔재단은 조직적 AX 다섯 단계 중<br><span class="gt">어디</span>일까요?',
                    "열매나눔재단이 있는 AX 단계",
                    "AI를 들여온 조직들은 대개 이 순서를 겪습니다. 손을 들어 보면 재단이 지금 어디쯤인지 나옵니다.",
                    inner, "")

    def stuck(n):
        """계정을 다 줬는데도 정체하는 이유를, 다른 회사가 같은 자리에서 주고받은 말로 본다.

        왼쪽은 그림 한 장이고 오른쪽은 진단 넷이다. 상황은 그림과 말로 전하고, 글로는 진단만 남긴다.
        진단은 직장인 커뮤니티 글에 달린 댓글에서 추렸고, 공감을 많이 받은 순서로 놓았다.
        닉네임과 공감 수 같은 커뮤니티 표시는 옮기지 않고 직군만 남긴다.
        그림은 assets/illus/s08.png 를 갈아 끼우면 바뀐다.
        """
        replies = [("소프트웨어아키텍트", "도구를 준 것과 쓰게 만든 것은 다릅니다",
                    "잘 쓰는 방법을 찾아 전파하고 실제 업무에 정착시키는 데까지가 관리자의 일이라고 답했습니다."),
                   ("기술영업", "기준이 없으면 제각각 만듭니다",
                    "토큰은 쓰는데 결과물이 없다면 기준이 없어 저마다 다른 것을 만들고 있거나, 개인 성과물을 만들고 있다고 봤습니다."),
                   ("임베디드", "지표가 그대로면 향상은 보이지 않습니다",
                    "빨라진 만큼을 예전과 같은 성과로 보고하면 조직에는 달라진 것이 없어 보입니다."),
                   ("교육 강사", "도구가 아니라 업무 순서와 평가의 문제입니다",
                    "AI를 쓰라고 말하는 대신 업무 순서 안에 AI를 넣자고 했습니다.")]
        rows = "".join(f'<div class="crow"><div class="cjob">{job}</div><h4>{t}</h4><p>{d}</p></div>'
                       for job, t, d in replies)
        shot = ('<div class="cshot"><img src="assets/illus/s08.png" '
                'alt="좋은 도구를 손에 쥐고도 어디로 갈지 정하지 못한 사람들"></div>')
        inner = (f'<div class="cwrap">{shot}<div class="creply">{rows}</div></div>'
                 + band('재단도 계정과 교육까지는 마련했습니다. <strong>남은 일은 잘 쓰는 방법을 찾아 실제 업무에 정착시키는 것입니다.</strong> '
                        '그 방법을 2부와 4부에서 봅니다.', 26))
        return wide(n, P1, "조직의 단계", '도구를 무제한으로 줬는데, <span class="gt">왜 생산성은 그대로일까요?</span>',
                    "계정을 다 줬는데도 정체하는 이유",
                    "많은 기업이 규모도 업종도 무관하게 계정을 다 쥐어 주고도 몇 달째 달라지지 않는 상황은 비슷합니다.",
                    inner, "")

    def jcurve(n):
        f = 'font-family="Pretendard Variable,sans-serif" font-weight="700" font-size="21" fill="#1E2130"'
        svg = ('<svg class="jcurve" viewBox="0 0 760 470">'
               '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
               '<path d="M0 0L10 5L0 10z" fill="#FF4D6D"/></marker></defs>'
               '<path d="M30 420 C 150 400, 290 300, 430 180 C 530 100, 690 120, 670 230 C 650 340, 500 380, 430 320 '
               'C 380 280, 380 220, 430 180 C 510 110, 620 60, 720 25" fill="none" stroke="#1E2130" stroke-width="5" stroke-linecap="round"/>'
               '<g fill="none" stroke="#FF4D6D" stroke-width="3" stroke-linecap="round" marker-end="url(#ah)">'
               '<path d="M100 445 C 180 418, 240 375, 290 325"/>'
               '<path d="M700 150 C 740 200, 740 270, 700 320"/>'
               '<path d="M590 400 C 530 440, 460 440, 410 400"/>'
               '<path d="M380 345 C 345 300, 350 250, 388 212"/>'
               '<path d="M540 65 C 610 32, 660 12, 710 2"/>'
               '</g>'
               f'<text x="245" y="448" {f} text-anchor="middle">AI 도입</text>'
               f'<text x="712" y="356" {f} text-anchor="middle">느려짐</text>'
               f'<text x="540" y="466" {f} text-anchor="middle">기준 배우기</text>'
               f'<text x="345" y="200" {f} text-anchor="end">순서 바꾸기</text>'
               f'<text x="640" y="115" {f} text-anchor="middle">더 빨라짐</text>'
               '</svg>'
               '<p class="rcap">고리를 한 번 돌아야 처음보다 높이 올라갑니다.</p>')
        points = [("처음에는 배우는 시간이 듭니다", "무엇을 시킬 수 있는지 익히는 데 몇 주가 갑니다."),
                  ("그다음에는 검증하는 시간이 듭니다", "버튼 한 번이면 끝날 줄 알았는데, AI가 제대로 했는지 읽는 시간이 더 듭니다."),
                  ("기준을 배우고 순서를 바꾼 팀만 다시 올라갑니다", "도구만 바꾼 팀은 고리 안을 돕니다.")]
        return split(n, P1, "조직의 단계", 'AI를 쓰면 시간이 줄까요?<br><span class="gt">처음에는 분명 줄어드는 것처럼 보입니다</span>',
                     "AI를 쓰면 처음에는 시간이 늘어나는 이유",
                     "도입 직후에는 배우는 시간과 검증하는 시간이 더 들어 오히려 느려집니다. 오늘 이야기의 나머지는 이 고리를 지나는 방법입니다.",
                     points, svg, "")

    # ── 2부. 방식 4와 숫자 읽기 ───────────────────────────────────────
    def dash_anyone(n):
        steps = [("연동 가이드를 문서 한 장으로", "자료가 어디에 있고 어떻게 잇는지 담당자가 적습니다."),
                 ("AI에게 읽히기", "그 문서를 AI가 먼저 읽습니다."),
                 ("담당자가 말로 요청", "데이터 담당이 아니어도 보고 싶은 것을 말로 요청합니다."),
                 ("대시보드가 나옵니다", "지표 화면이 바로 만들어집니다.")]
        inner = ('<div class="vcen">' + stepflow(steps)
                 + band(f'재단도 GA4 연동 설명을 문서 한 장으로 남기면 같은 방식으로 할 수 있습니다. '
                        f'<strong>{REF["a18"]}장의 네 번째 방식이 실제 조직에서 굴러가는 모습입니다.</strong>')
                 + '</div>')
        return wide(n, P2, "방식 4 구조", '다른 조직은 이렇게 했습니다:<br>대시보드를 <span class="gt">누구나</span>',
                    "다른 조직의 사례. 대시보드를 누구나",
                    "데이터 담당이 없는 조직이 연동 가이드를 문서로 정리해 AI에게 읽히고, 담당자가 직접 대시보드를 만들게 했습니다.",
                    inner, "")

    def average(n):
        right = ('<div class="llmsim" data-llm-sim>'
                 '<div class="simhead"><span>문장 생성</span>'
                 '<span class="simwing"><span class="simtag" data-sim-mode-label>기본 모델</span>'
                 '<button class="simplay" type="button" aria-label="시연 시작" data-sim-play>'
                 '<svg viewBox="0 0 24 24" aria-hidden="true">'
                 '<path class="pi" d="M8 5l11 7-11 7z"/>'
                 '<path class="pa" d="M7 5h3.4v14H7zM13.6 5H17v14h-3.4z"/></svg></button></span></div>'
                 '<div class="simquestion"><span>사용자</span><b data-sim-question>4월 후원 건수를 어떻게 해석해야 할까요?</b></div>'
                 '<div class="simoutput"><span>답변 생성</span><strong data-sim-output></strong></div>'
                 '<div class="simcands"><span>다음 후보</span><div data-sim-cands></div></div>'
                 '<div class="simstatus"><i data-sim-live></i><b data-sim-step-label>질문 입력 중</b></div>'
                 '<div class="simprogress"><i data-sim-progress></i></div>'
                 '</div>')
        points = [("LLM은 정답을 꺼내기보다 다음 말을 고릅니다",
                   "앞 문맥에서 다음에 올 가능성이 높은 단어를 하나 고릅니다."),
                  ("선택을 이어 문장을 만듭니다",
                   "고른 단어를 다시 문맥에 넣고, 다음 후보를 비교합니다."),
                  ("모델이 좋아질수록 보는 범위가 넓어집니다",
                   "긴 문맥과 자료, 질문의 목적과 재단 기준까지 함께 반영해 평균적인 말에서 벗어납니다.")]
        return split(n, P2, "LLM의 생성 구조", 'AI는 정답을 꺼내기보다<br><span class="gt">다음 말을 고르며</span> 답을 만듭니다',
                     "LLM이 답변을 생성하는 방식",
                     "LLM은 앞 문맥에서 다음에 올 가능성이 높은 단어를 고르고, 그 선택을 이어 문장을 만듭니다. 모델이 좋아질수록 더 긴 맥락과 목적, 기준을 함께 반영합니다.",
                     points, right, "")

    # ── 3부. 읽지 않고 넘기는 문제 ───────────────────────────────────
    def cog_debt(n):
        items = [("결론만 읽습니다", "결과물이 많아 마지막 줄만 봅니다."),
                 ("남의 AI 결과를 내 AI에 넣어 돌려보냅니다", "아무도 읽지 않은 문서가 사람 손을 거치지 않고 오갑니다."),
                 ("확신 없는 결과물이 돌아다닙니다", "생산량은 늘었는데 내가 만든 것에 내가 확신이 없습니다.")]
        inner = ('<div class="vcen">' + cards(items, "단계", "three", ["list", "refresh", "alert"])
                 + band('<strong>이것이 인지부채입니다.</strong> 생각은 AI에게 맡겨도 이해는 맡길 수 없습니다. '
                        'AI가 쓴 사업 보고서를 읽지 않고 이사회에 올리는 순간, 재단은 자기 보고서를 모르는 조직이 됩니다.')
                 + '</div>')
        return wide(n, P3, "인지부채", 'AI 결과가 많아질수록,<br><span class="gt">인지부채</span>가 쌓일 수 있습니다',
                    "결과는 늘었는데 조직의 이해는 줄어드는 일",
                    "AI 결과물이 넘치면 전체 읽기를 포기하고 결론만 봅니다. 그다음 사람도 마찬가지로 넘기면서, 생산량과 이해 사이에 부채가 생깁니다.",
                    inner, "")

    def review_other(n):
        same = paper("같은 대화에서 \"검토도 해 봐\"",
                     ["자기가 한 말을 옹호합니다", "일부만 잡아냅니다", "고친 척만 하고 넘어갑니다"],
                     "만든 AI는 자기 결과를 봐줍니다")
        other = paper("새 대화나 다른 역할의 AI에게",
                      ["만든 맥락을 모른 채 봅니다", "관점이 다른 검토자를 여럿 둡니다", "타당한 지적만 원래 대화로 가져옵니다"],
                      "검수는 남이 해야 검수입니다", after=True)
        inner = (f'<div class="balist">{same}{ARROW}{other}</div>'
                 + band('실제로 쓰는 지시는 단순합니다. <strong>역할이 다른 검토자 셋을 두고 초안을 비판하게 한 뒤, '
                        '타당한 지적만 받아들이는 순서를 두 번 반복합니다.</strong>', 34))
        return wide(n, P3, "읽지 않고 넘기는 문제", '검수는 만든 AI와 <span class="gt">다른 AI</span>에게',
                    "검수는 만든 AI와 다른 AI에게",
                    "AI는 자기가 한 말을 옹호하는 성질이 있습니다. 문안을 쓴 대화와 검수하는 대화를 나눕니다.",
                    inner, "")

    # ── 3부. 규칙 파일 ────────────────────────────────────────────────
    def share_q(n):
        # 부채 이름 셋을 각인시키는 장이다. 25장부터 각 부채를 따로 푸니 설명은 한 줄로 줄이고 그림에 맡긴다.
        figs = [("debt_1", "반듯한 사무실 아래로 임시 배관과 얽힌 선이 받치고 있는 그림",
                 "기술부채", "도구만 얹어 두고 업무와 권한을 임시로 둡니다"),
                ("debt_2", "기계가 쏟아내는 것을 사람들이 확인 표시만 찍고 지나가는 그림",
                 "인지부채", "읽고 판단하지 않은 채 다음으로 넘깁니다"),
                ("debt_3", "쌓인 문서 앞에서 사람들이 물음표를 띄우고 서 있는 그림",
                 "의도부채", "결과는 남고 왜 만들었는지는 사라집니다")]
        inner = ('<div class="vcen">' + illus(figs, "부채", "shot")
                 + band('<strong>AX는 자동화를 더하는 일이 아닙니다.</strong> 세 부채가 쌓이지 않도록 기준과 맥락, 책임을 함께 남기는 일입니다. '
                        '중요한 정보를 구독형 AI에 묶어 두면 중장기에는 로컬 LLM까지 다시 설계해야 합니다.', 22)
                 + '</div>')
        return wide(n, P3, "조직의 AX와 세 가지 부채", 'AI를 붙일수록 조직에<br><span class="gt">무엇이 쌓일까요?</span>',
                    "조직의 AX에서 함께 관리해야 할 세 가지 부채",
                    "부채는 돈을 빌리는 일과 같습니다. 지금 당장은 빠르게 갈 수 있지만, 미뤄 둔 몫이 이자처럼 불어나 나중에 훨씬 큰 일이 되어 돌아옵니다.",
                    inner, "")

    # ── 3부. 부채 세 가지를 네 컷으로 ────────────────────────────────
    # 세 편을 서로 다른 그림체로 그린다. 같은 이야기라도 원하는 그림체로 뽑을 수 있다는 것을
    # 자료 자체로 보이려는 뜻이다. 순서는 24장에서 부채를 늘어놓은 순서를 그대로 따른다.
    def toon_tech(n):
        cuts = [("급한 일에 도구 하나를 기계 옆에 붙이는 장면", "일단 이거 하나만 붙이면 됩니다", "t l"),
                ("도구가 늘고 케이블이 얽히기 시작하는 장면", "선은 나중에 정리하죠", "t l"),
                ("얽힌 케이블을 두고 자리를 뜨는 장면", "잘 돌아가니까 그냥 둡시다", "b l"),
                ("기계가 멈추고 얽힌 선 앞에 서 있는 장면", "어디서 멈춘 건지 모르겠습니다", "t l")]
        inner = toon("tech", "comic", cuts) + band(
            '<strong>기술부채는 도구가 많아서 생기지 않습니다.</strong> 무엇을 어떻게 이었는지 남기지 않아서 생깁니다.')
        return wide(n, P3, "기술부채", '급할 때 붙인 것은<br><span class="gt">나중에 고칠 수 없습니다</span>',
                    "기술부채가 쌓이는 네 컷",
                    "도구를 하나씩 붙이는 동안에는 아무 문제가 없습니다. 잇는 방식과 권한, 검수를 적어 두지 않으면 멈춘 뒤에 고칠 수 없습니다.",
                    inner, "", cls="toon-slide")

    def toon_cog(n):
        cuts = [("인쇄된 문서를 받아 드는 장면", "보고서가 나왔습니다", "t r"),
                ("맨 아랫줄만 보고 옆으로 넘기는 장면", "결론만 보면 되겠네요", "t l"),
                ("문서가 사람 셋을 그대로 지나가는 장면", "저도 그대로 넘기겠습니다", "b r"),
                ("쌓인 문서 앞에서 서로를 바라보는 장면", "이거 무슨 내용이었죠", "b l")]
        inner = toon("cog", "webtoon", cuts) + band(
            '<strong>아무도 설명하지 못하는 문서는 만든 만큼 남지 않습니다.</strong> 읽는 시간을 따로 잡아야 이 부채가 멈춥니다.')
        return wide(n, P3, "인지부채", '읽지 않은 문서는<br><span class="gt">사람을 그냥 지나갑니다</span>',
                    "인지부채가 쌓이는 네 컷",
                    "AI가 만든 것이 늘수록 전체를 읽지 않고 결론만 봅니다. 다음 사람도 그렇게 넘기면 조직의 이해가 줄어듭니다.",
                    inner, "", cls="toon-slide")

    def toon_intent(n):
        # 네 컷과 말풍선이 한 장에 다 들어 있는 그림이라 덧붙이는 말풍선 없이 그림만 건다.
        alt = ("의도부채 네 컷 만화. 목적과 지킬 것을 공책에 적어 두고, 결과물만 서랍에 넣고, "
               "몇 달 뒤 왜 그렇게 했는지 기억하지 못하고, 다음 사람은 물어볼 사람이 없습니다")
        inner = (f'<div class="toonpage novel"><img src="assets/toon/intent.jpg" alt="{alt}"></div>') + band(
            '<strong>다음 사람이 처음부터 다시 정해야 하는 것이 의도부채입니다.</strong> 목적과 지킬 것, 책임자를 결과 옆에 같이 적어 둡니다.')
        return wide(n, P3, "의도부채", '결과만 남기면<br><span class="gt">이유가 사라집니다</span>',
                    "의도부채가 쌓이는 네 컷",
                    "목적과 지킬 것을 분명히 적어 두고도 결과물만 저장하면, 몇 달 뒤의 나도 다음 사람도 그 기준을 처음부터 다시 만들어야 합니다.",
                    inner, "", cls="toon-slide")

    def grill(n):
        # 만들어진 규칙 파일이 어떻게 생겼는지 그대로 보인다. 해야 할 것과 하지 않을 것을 나란히 적는다.
        do = ["숫자는 GA4 원본에서 가져오고, 어느 데이터를 봤는지 함께 적습니다",
              "사연이 담긴 문장은 내보내기 전에 담당자가 직접 읽습니다",
              "결과물은 파일로 남기고, 어디에 두었는지 적습니다"]
        dont = ["후원자 이름과 연락처는 넘기지 않습니다",
                "확인하지 않은 숫자는 보고서에 넣지 않습니다",
                "모르는 것을 아는 것처럼 쓰지 않습니다"]
        def grp(cls, head_cls, head, items):
            lis = "".join(f'<li>{x}</li>' for x in items)
            return (f'<div class="rgrp {cls}"><div class="rhead {head_cls}">{head}</div>'
                    f'<ul>{lis}</ul></div>')
        right = ('<div class="termwrap rulebox"><div class="term">'
                 '<div class="bar"><i></i><i></i><i></i><span>MERRYYEAR.md</span></div>'
                 '<div class="tbody">'
                 + grp("y", "ok", "지켜야 할 것", do) + grp("n", "no", "하지 말아야 할 것", dont)
                 + '</div></div></div>'
                 '<p class="rcap">AI가 일을 시작하기 전에 먼저 읽는 파일입니다. 새로 온 사람에게 건네는 안내문과 같습니다.</p>')
        points = [("역할을 바꿉니다", "내가 AI에게 묻는 대신 AI가 나에게 집요하게 묻게 합니다."),
                  ("질문은 한 번에 하나, 추천 답을 같이", "답하기 쉬워야 끝까지 갑니다."),
                  ("결과를 파일로 남깁니다", "대화가 닫혀도 기준은 남습니다. 다음 사람은 이 파일부터 읽습니다.")]
        return split(n, P3, "규칙 파일", '규칙 파일은 AI가 <span class="gt">물어보게</span> 해서 만듭니다',
                     "규칙 파일을 AI가 물어보게 해서 만들기",
                     "머릿속에만 있는 기준은 내가 알고 있다는 사실조차 모릅니다. 누가 물어봐야 나오고, 적어야 남습니다.",
                     points, right, "")

    def shared_memory(n):
        steps = [("팀마다 AI와 주고받은 기록", "후원팀도 홍보팀도 각자 시행착오를 겪습니다."),
                 ("배운 것 골라내기", "기록에서 재단 규칙과 예외를 뽑아냅니다."),
                 ("재단 공용 기억에 올리기", "한 파일 묶음에 모으고 주기적으로 갱신합니다."),
                 ("새 사람과 새 AI도 같은 맥락에서 시작", "처음 온 사람도 첫날부터 재단 기준으로 일합니다.")]
        inner = ('<div class="vcen">' + stepflow(steps)
                 + band('<strong>후원팀이 찾아낸 표기 규칙을 홍보팀이 다시 찾아낼 이유가 없습니다.</strong> 시행착오 비용은 한 번만 냅니다.')
                 + '</div>')
        return wide(n, P3, "규칙 파일", '한 팀의 시행착오를<br>재단 전체의 <span class="gt">기억</span>으로',
                    "한 팀의 시행착오를 재단 전체의 기억으로",
                    "모은 기록이 도움이 되려면 누군가 골라내어 한곳에 두어야 합니다. 부서마다 같은 시행착오를 반복할 이유가 없습니다.",
                    inner, "")

    # ── 4부. 업무 쪼개기 ──────────────────────────────────────────────
    def sms_case(n):
        before = [("대상 추리기", "후원 기록에서 보낼 사람을 골라 엑셀로 뽑습니다."),
                  ("문안 쓰기", "지난 문자를 찾아 이름과 금액을 바꿉니다."),
                  ("번호 맞추기", "이름과 번호를 한 줄씩 대조합니다."),
                  ("발송 시스템 입력", "문안과 번호를 옮겨 붙입니다."),
                  ("상급자 확인", "메신저로 갈무리를 보내고 답을 기다립니다."),
                  ("발송", "확인이 오면 버튼을 누릅니다.")]
        after = [("기준 정하기", "어떤 문자가 누구에게 언제 가는지 담당자가 규칙 파일에 적습니다."),
                 ("AI가 대상과 초안", "후원 기록을 읽고 보낼 사람과 문안을 만듭니다."),
                 ("규칙으로 점검", "이름, 금액, 금지 표현, 발송 시점을 정한 규칙으로 대조합니다."),
                 ("담당자 승인", "걸린 것만 읽고 발송 버튼을 누릅니다.")]
        inner = ('<div class="bawrap">'
                 f'<div class="baflow"><div class="bfl">지금<br>담당자 손으로</div>{stepflow(before)}</div>'
                 f'<div class="baflow after"><div class="bfl">AI 에이전트를<br>끼운 뒤</div>{stepflow(after, hot=(1, 4))}</div>'
                 + band('<strong>AI가 한 일보다 담당자가 먼저 적은 기준과 마지막 승인이 이 흐름을 만듭니다.</strong> '
                        '손으로 하던 여섯 단계 가운데 넷이 AI 몫이 되고, 담당자는 처음과 끝에 섭니다.')
                 + '</div>')
        return wide(n, P4, "업무 쪼개기", '안내 문자 한 통이 나가기까지,<br>지금과 <span class="gt">AI 에이전트를 끼운 뒤</span>',
                    "안내 문자 발송의 지금과 AI 에이전트를 끼운 뒤",
                    "감사 문자와 정기후원 안내를 예로 듭니다. 지금은 여섯 단계를 담당자가 손으로 지나고, 바꾼 뒤에는 담당자가 두 곳에만 섭니다.",
                    inner, "")

    def boss_skills(n):
        # 세 칸을 글로 설명하지 않고 소프트 3D 일러스트로 대신한다. 헤더 한 줄만 남긴다.
        figs = [("sowhat_1", "모래시계에서 흘러나온 시간이 과녁으로 이어지는 그림",
                 "더 중요한 문제에<br>시간을 씁니다"),
                ("sowhat_2", "판단 기준이 적힌 문서가 조직의 서랍에 쌓이는 그림",
                 "판단 기준을<br>조직의 자산으로 남깁니다"),
                ("sowhat_3", "막대 세 개가 높아지고 화살표가 위로 향하는 그림",
                 "내년의 성과를<br>바꿉니다")]
        inner = ('<div class="vcen">' + illus(figs, "기여")
                 + band('<strong>AI 사용량과 자동화 개수는 중간 지표입니다.</strong> 조직이 새로 잘하게 된 일이 최종 성과입니다.')
                 + '</div>')
        return wide(n, P5, "So What", '<span class="sowhat-word">So What?</span><span class="sowhat-question">AI를 잘 쓰고 자동화까지 했습니다. 그래서 조직에 무엇이 남았나요?</span>',
                    "AI 활용과 자동화 다음에 답해야 할 질문",
                    "자동화는 출발점입니다. 줄어든 시간과 쌓인 기준이 조직의 성과로 이어져야 AX입니다.",
                    inner, "", cls="so-what-slide")

    # ── 4부. 기준 세우기 ──────────────────────────────────────────────
    def buy_vs_connect(n):
        # 앞 장과 같은 좌우 표를 쓴다. 네 줄은 출발, 목표, 자산, 책임 순서로 읽는다.
        rows = [(("새 도구를 하나 더 구독합니다", "계정과 교육까지 마련하면 도입이 끝난 것처럼 보입니다."),
                 ("쓰던 시스템에 AI를 연결합니다", "지금 있는 자료와 절차를 그대로 두고 그 위에서 AI가 일하게 만듭니다.")),
                (("기능이 많은 것을 고릅니다", "고를 때는 좋아 보이지만, 실제로 쓰는 기능은 몇 개뿐입니다."),
                 ("매일 하는 일 하나를 고칩니다", "단순한 것이 오래 남습니다. 담당자가 바뀌어도 그대로 돌아갑니다.")),
                (("잘 쓰는 사람 머릿속에 남습니다", "그 사람이 없으면 일도 같이 멈춥니다."),
                 ("문서와 파일로 남습니다", "다음 사람이 열어 보고 이어서 씁니다.")),
                (("AI에게 끝까지 맡깁니다", "일이 잘못돼도 누가 확인했어야 하는지 남지 않습니다."),
                 ("AI가 만들고 사람이 확인합니다", "규칙으로 한 번 거르고, 마지막 책임은 담당자가 집니다."))]
        inner = (vs("새로 구독하는 쪽", "쓰던 것에 연결하는 쪽", rows)
                 + band('<strong>우리가 이미 쓰는 GA4와 후원 시스템, 문서 폴더가 그대로 출발점입니다.</strong> '
                        '새로 구독할 것을 고르기 전에, 지금 쓰는 것에 무엇을 연결할 수 있는지부터 봅니다.', 30))
        return wide(n, P4, "기준 세우기", 'AX는 새 도구를 구독하는 일이 아니라<br>이미 쓰는 것에 <span class="gt">연결하는 일</span>입니다',
                    "AX는 구독하는 일이 아니라 연결하는 일",
                    "AI를 도입한다고 하면 어떤 도구를 구독할지부터 정하기 쉽습니다. 그런데 오래 남는 것은 새로 들여온 도구가 아니라, 이미 쓰던 시스템에 AI를 연결해 바꾼 업무 순서입니다.",
                    inner, "")

    def less(n):
        can = paper("만들 수 있는 것",
                    ["카드뉴스 100장", "사연별 문안 20안", "보고서 버전 10개", "후원자 유형별 메일 30통"],
                    "만드는 비용은 0에 가깝습니다")
        will = paper("재단이 실제로 내보낼 것",
                     ["후원자에게 갈 3장", "담당자가 고른 1안", "이사회에 갈 1부", "이번 달에 보낼 2통"],
                     "고르는 비용은 그대로입니다", after=True)
        shot = ('<div class="lessart"><img src="assets/illus/s37.png" '
                'alt="공짜로 쏟아져 나온 결과물 더미와, 그 가운데 내보낼 몇 개만 골라 든 모습"></div>')
        inner = (f'<div class="lesswrap">{shot}<div class="balist">{can}{ARROW}{will}</div></div>'
                 + band(f'<strong>무엇을 만들지 않을지는 사람마다 다릅니다.</strong> 그 취향을 맞추는 회의가 병목이 되지 않게, '
                        f'{REF["d_share"]}장의 기준을 문서로 먼저 정합니다.', 34))
        return wide(n, P4, "기준 세우기", '뭐든 만들 수 있다면<br><span class="gt">무엇을 만들지 않을지</span>가 실력입니다',
                    "뭐든 만들 수 있을 때 필요한 것",
                    "빨리 만들 수 있으니 다 만들자는 것이 흔한 실수입니다. 숟가락이 공짜라도 100개를 쓰지는 않습니다.",
                    inner, "")

    def check_shapes(n):
        items = [("통과와 실패", "금지 표현이 있는지, 이름을 지웠는지. 만들기 쉬워서 검수 목록의 대부분이 이 모양입니다."),
                 ("숫자로 재기", "근거 숫자가 원본과 맞는지, 발송까지 며칠 걸렸는지."),
                 ("점수로 매기기", "당사자를 존중하는 문장인지 5점으로 매깁니다. AI에게 전문가 역할을 주고 채점하게 합니다.")]
        inner = ('<div class="vcen">' + cards(items, "모양", "three", ["checkx", "ruler", "star"])
                 + band(f'<strong>{REF["d_rules"]}장의 원칙 일곱 개를 이 세 모양으로 옮겨 적으면 검수 목록이 됩니다.</strong> '
                        '전부 사람이 볼 필요는 없습니다. 통과와 실패는 자동으로, 점수는 AI가, 마지막 판단만 담당자가.')
                 + '</div>')
        return wide(n, P4, "기준 세우기", '검수 기준은 <span class="gt">세 가지 모양</span>입니다',
                    "검수 기준의 세 가지 모양",
                    "AI가 쏟아내는 것을 전부 읽으려 하면 지칩니다. 기준을 세 가지 모양으로 적어 두면 사람이 볼 것만 남습니다.",
                    inner, "")

    def rollback(n):
        steps = [("검토하지 않은 보고서", "AI가 쓴 보고서를 읽지 않고 올립니다."),
                 ("그 보고서로 결정", "리더가 그 보고서를 믿고 결정합니다."),
                 ("나중에 드러납니다", "숫자가 틀렸거나 있어야 할 것이 빠져 있었습니다."),
                 ("AI 사용을 막습니다", "놀란 조직이 AI를 통째로 막습니다. 그 뒤 반년은 아무것도 못 합니다.")]
        inner = ('<div class="vcen">' + stepflow(steps, hot=(4,))
                 + band('<strong>검토 기준을 먼저 세우는 이유입니다.</strong> 다음 장의 원칙 일곱 개가 그 기준입니다.')
                 + '</div>')
        return wide(n, P4, "기준 세우기", '한 번 사고가 나면 <span class="gt">6개월</span>이 날아갑니다',
                    "한 번 사고가 나면 6개월이 날아가는 이유",
                    "AI를 쓰다 사고가 나면 손해는 사고 자체보다 그 뒤에 옵니다. 조직이 AI를 통째로 막는 반년입니다.",
                    inner, "")

    def simple_rules(n):
        seven = paper("원칙 일곱 개",
                      ["사람을 데이터로만 보지 않기", "개인정보는 빼고 읽히기", "동의한 목적 안에서만",
                       "AI가 만든 부분 밝히기", "편향 점검하기", "책임자를 사람으로", "자동화하지 않을 권리"],
                      "앞 장의 원칙입니다. 다 맞지만 매일 확인하기에는 많습니다", two=True)
        three = paper("매일 확인하는 규칙 세 개",
                      ["이름을 지웠는지", "숫자를 원본과 대조했는지", "승인자 이름을 적었는지"],
                      "이 셋만 지켜도 일곱 개의 대부분이 지켜집니다", after=True)
        inner = (f'<div class="balist">{seven}{ARROW}{three}</div>'
                 + band('<strong>AI의 속도, 담당자의 판단과 책임, 그리고 단순한 규칙 세 개.</strong> 이 셋이 같이 가야 규칙이 살아남습니다.', 34))
        return wide(n, P4, "기준 세우기", '규칙은 <span class="gt">단순해야</span> 지켜집니다',
                    "규칙이 단순해야 지켜지는 이유",
                    "규칙은 적어 두어야 지켜지고, 그 수가 적어야 매일 확인합니다. 일곱 개를 매일 셀 수는 없습니다.",
                    inner, "")

    # ── 4부. 조직 움직이기 ────────────────────────────────────────────
    def translator(n):
        # 다섯 가지 모두 추상 명사라 선 아이콘으로는 잡히지 않는다. 설명 한 줄씩을 그림으로 바꾼다.
        figs = [("force_1", "돋보기가 비스듬히 서 있는 그림", "상황을<br>읽는 힘"),
                ("force_2", "뚜껑이 열린 공구 상자 그림", "도구를<br>아는 힘"),
                ("force_3", "땅에 박힌 지도 핀 그림", "현장을<br>아는 힘"),
                ("force_4", "펼쳐진 책에서 종이가 날아오르는 그림", "남기고<br>알려 주는 힘"),
                ("force_5", "받침 위에 놓인 승인 도장 그림", "믿음을<br>만드는 힘")]
        inner = ('<div class="vcen">' + illus(figs, "힘", "five")
                 + band('기술팀이 없는 재단에서는 담당자 한 사람이 이 역할을 맡게 됩니다. '
                        '<strong>다섯 가지를 다 갖춘 사람을 찾기보다, 현장을 아는 사람이 나머지를 배우는 편이 빠릅니다.</strong>')
                 + '</div>')
        return wide(n, P4, "조직 움직이기", '재단 안에서 <span class="gt">누가</span> 끌고 갈까요?',
                    "재단 안에서 끌고 갈 사람",
                    "업무와 기술 사이를 잇는 사람이 있어야 굴러갑니다. 그 사람에게 필요한 힘은 다섯 가지입니다.",
                    inner, "")

    def relief(n):
        person = paper("개인에게는",
                       ["귀찮아하는 업무부터 고릅니다", "첫 시도에서 바로 성공 경험을 줍니다",
                        "AI의 한계를 숨기지 않습니다", "일을 덜어 준다는 말로 설명합니다"],
                       "쓰게 만드는 쪽")
        org = paper("재단에는",
                    ["누구나 쓰는 공용 자료와 규칙을 둡니다", "성과와 실패를 투명하게 공유합니다",
                     "전 직원이 사례를 보는 시간을 정해 둡니다", "잘된 사례는 만든 사람이 직접 보여 줍니다"],
                    "퍼지게 만드는 쪽", after=True)
        inner = (f'<div class="balist">{person}{ARROW}{org}</div>'
                 + band('<strong>60일째 시험 운영 결과를 전 직원 앞에서 여는 시간이 양쪽을 한꺼번에 채웁니다.</strong> '
                        '사람은 따라 하면서 배웁니다.', 34))
        return wide(n, P4, "조직 움직이기", '일을 뺏는 것이 아니라<br>귀찮은 일을 <span class="gt">덜어 줍니다</span>',
                    "일을 뺏는 게 아니라 귀찮은 일을 덜어 준다는 설득",
                    "시스템을 만든 뒤 진짜 걸림돌은 사람의 거부감과 관성입니다. AI 도입은 기술 문제보다 사람을 움직이는 문제입니다.",
                    inner, "")

    def leaders(n):
        items = [("읽는 시간을 줍니다", "결과물이 한꺼번에 나오니 읽는 시간을 따로 잡아야 합니다."),
                 ("사용량 대신 결과물로 봅니다", "얼마나 썼는지보다 무엇이 재단에 남았는지를 봅니다."),
                 ("검토가 한 사람에게 몰리지 않게 합니다", "승인이 밀리면 그 사람이 병목이 되고 먼저 지칩니다."),
                 ("경영진이 나섭니다", "일하는 순서를 바꾸는 일이라 담당자 혼자서는 못 합니다."),
                 ("지치는 속도를 봅니다", "같은 사람이 더 많은 판단을 하게 되니, 지치지 않게 하는 것도 일입니다.")]
        inner = ('<div class="vcen">' + cards(items, "리더", "five", ["clock", "file", "users", "flag", "battery"])
                 + band('<strong>재단 리더가 참석하는 자리에서 쓰는 장입니다.</strong> 담당자에게 시키기 전에 리더가 먼저 마련해야 하는 것들입니다.')
                 + '</div>')
        return wide(n, P4, "조직 움직이기", '리더가 <span class="gt">마련해 줘야</span> 하는 것',
                    "리더가 마련해 줘야 하는 것",
                    "담당자가 아무리 잘해도 리더가 마련해 주지 않으면 막히는 다섯 가지입니다.",
                    inner, "")

    # ── 5부. 마무리 ───────────────────────────────────────────────────
    def hours(n):
        inner = ('<div class="hours">'
                 '<div class="hrow"><div class="hl">지금</div><div class="hbar">'
                 '<span style="flex:6">직접 만드는 일 6시간</span><span class="judge" style="flex:2">판단 2시간</span></div></div>'
                 '<div class="hrow after"><div class="hl">바꾼 뒤</div><div class="hbar">'
                 '<span style="flex:2">AI에게 시키기 2시간</span><span class="judge" style="flex:6">판단 6시간</span></div></div>'
                 '</div>'
                 + band(f'<strong>아직 직접 만드는 시간이 6시간이면 옛 방식으로 일하는 것입니다.</strong> '
                        f'{REF["a22"]}장의 담당자 몫 세 가지가 늘어난 판단 시간에 들어갑니다.', 30))
        return wide(n, P5, "마무리", '만드는 시간을 줄이고,<br>생각하는 시간을 <span class="gt">늘립니다</span>',
                    "하루 8시간의 구성이 바뀌는 방향",
                    "하루 8시간의 구성이 바뀝니다. 만드는 시간이 줄고 판단하는 시간이 늘어납니다.",
                    inner, "")

    def gellmann(n):
        right = ('<div class="qacard"><div class="qlabel">내 분야 기사를 읽을 때</div>'
                 '<div class="qq">틀린 곳이 바로 보입니다</div>'
                 '<div class="qa">재단 담당자는 AI가 쓴 사연 요약에서 빠진 것을 알아챕니다.</div></div>'
                 '<div class="qacard"><div class="qlabel">남의 분야 기사를 읽을 때</div>'
                 '<div class="qq">그럴듯하면 믿습니다</div>'
                 '<div class="qa">AI 결과가 그럴듯해 보였다면, 그 가운데 일부는 우리가 그 분야를 몰라서 그렇게 보인 것입니다.</div></div>')
        points = [("그럴듯한 것과 맞는 것은 다릅니다", "AI는 뻔한 실수는 하지 않습니다. 그래서 더 그럴듯합니다."),
                  ("가짜를 거르는 눈은 그 일을 아는 사람에게 있습니다", "믿을 만한 검수 기준은 재단 일을 아는 사람이 만듭니다."),
                  ("검수 기준을 쌓을수록 더 전문가가 됩니다", "무엇이 좋은 결과인지 정하는 사람이 전문가입니다.")]
        return split(n, P5, "마무리", '그럴듯한 가짜를 거르는 것은<br>재단 일을 <span class="gt">아는 사람</span>입니다',
                     "그럴듯한 가짜를 거르는 사람",
                     "내 분야 기사는 오류가 보이는데 남의 분야 기사는 믿습니다. AI 결과를 읽을 때도 같은 일이 일어납니다.",
                     points, right, "")

    def hard_calls(n):
        items = [("옳은 가치와 옳은 가치 사이", "후원 전환율과 당사자 존엄 사이의 선택처럼, 둘 다 맞는데 하나를 골라야 합니다."),
                 ("있어야 할 것이 빠진 것을 알아채기", "AI는 있는 것을 다루지, 빠진 것은 눈치채지 못합니다. 빠진 것은 그 일을 아는 사람만 봅니다."),
                 ("책임이 딸린 결정", "틀리면 무슨 일이 생기는지 알고, 수습할 수 있고, 남이 납득하는 사람이 도장을 찍습니다.")]
        inner = ('<div class="vcen">' + cards(items, "결정", "three", ["scale", "missing", "stamp"])
                 + band(f'<strong>쉬운 결정을 AI가 다 하고 나면 사람에게는 어려운 결정만 옵니다.</strong> '
                        f'{REF["d_speed"]}장의 선택이 그 예이고, 지금의 AI는 책임을 질 수 있는 주체가 아닙니다.')
                 + '</div>')
        return wide(n, P5, "마무리", 'AI가 사람에게 넘기는 결정은<br><span class="gt">어떤 것</span>일까요?',
                    "AI가 사람에게 넘기는 결정",
                    "AI가 하지 못하고 사람에게 넘기는 것은 대개 어려운 결정입니다. 세 종류입니다.",
                    inner, "")

    return {"stages": stages, "stuck": stuck, "jcurve": jcurve, "dash_anyone": dash_anyone, "average": average,
            "cog_debt": cog_debt, "review_other": review_other, "share_q": share_q, "grill": grill,
            "toon_tech": toon_tech, "toon_cog": toon_cog, "toon_intent": toon_intent,
            "shared_memory": shared_memory, "sms_case": sms_case, "boss_skills": boss_skills,
            "buy_vs_connect": buy_vs_connect, "less": less, "check_shapes": check_shapes, "rollback": rollback,
            "simple_rules": simple_rules, "translator": translator, "relief": relief, "leaders": leaders,
            "hours": hours, "gellmann": gellmann, "hard_calls": hard_calls}
