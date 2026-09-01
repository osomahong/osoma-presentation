"""AX 쇼케이스 덱을 만든다.

기획 원칙은 하나다. AI의 기능을 보여주지 않고, 일을 AI로 설계하는 방식을 보여준다.
재단의 389일 데이터는 주제가 아니라 증거물로 쓴다.

59장이다. 원래 장들(이 파일), 2026-08-27 오전에 더한 장(build_ax_deep.py), 오후에 더한 장(build_ax_add.py).
본문은 본문_AX60.md 와 맞춘다. 파일이 있으면 그 텍스트로 빌드하고, --export 를 주면 코드 텍스트로 파일을 다시 쓴다.
시간 제한을 없앤 뒤로 머리말은 시간 대신 부와 소주제를 적는다. 장 번호는 조립 순서대로 매겨지므로 각 장
함수는 번호를 받고, 다른 장을 가리킬 때는 REF 사전을 쓴다.

문장 원칙: 제목은 질문이나 실제 상황으로, 설명은 말로 채우니 장표 문장은 짧게, 주어는 담당자.

빌드: python3 build_ax.py [--approve] [--export] [--v2] [--compare] [--all]
출력: 쇼케이스_AX60.html (--v2를 주면 쇼케이스_AX60_v2.html)
"""
import sys
from pathlib import Path
from sync_text import sync
from toolbar import TOOLBAR_HTML
from build_slides import CSS, LOGO, lint, HEADERS, prose_gate, kicker, brandbar
from build_ax_deep import DEEP_CSS, REF, icon, make as make_deep, P1, P2, P3, P4, P5
from build_ax_add import ADD_CSS, make as make_add
from build_ax_v2 import V2_CSS, V2_JS, v2_patch
from build_v2_variants import VARIANT_CSS, COMPARE_CSS, COMPARE_JS, compare_body, compare_controls
from v2_layouts import LAYOUT_CSS
from v2_sketch import SKETCH_CSS
from v2_pick import PICK_CSS, PICK_JS
from build_v2_all import COVER_CSS, compare_all_body

TOTAL = 53
ROOT = Path(__file__).resolve().parent

EXTRA_CSS = """
/* ── AX 쇼케이스 공통 ── */
.ax .credit2{position:absolute;left:120px;bottom:52px;font-family:var(--fm);font-size:15px;letter-spacing:.14em;color:var(--faint);z-index:6}
.ax .clock{position:absolute;top:64px;left:120px;font-family:var(--fm);font-size:17px;letter-spacing:.24em;color:var(--faint);z-index:5}
.vcen{flex:1;display:flex;flex-direction:column;justify-content:center;gap:40px;min-height:0}
.axcols{display:grid;grid-template-columns:1fr 1.05fr;gap:72px;margin-top:44px;flex:1;align-items:center;min-height:0}
.points .pt h4{font-size:26px}
.points .pt p{font-size:21px;line-height:1.55}
.rcap{font-size:18px;color:var(--faint);margin-top:18px;line-height:1.5}

/* 표지 */
.ax-cover .fg{justify-content:flex-end;padding-bottom:150px;gap:44px}
.ax-cover h1{font-size:116px;font-weight:800;letter-spacing:-.04em;line-height:1.16}
.ax-cover .sub{font-size:30px;color:var(--dim);font-weight:500;max-width:1250px}
.ax-cover .mchips{display:flex;font-family:var(--fm);font-size:18px;letter-spacing:.18em;color:var(--dim)}
.ax-cover .mchips span{padding:0 34px;border-left:1px solid var(--line)}
.ax-cover .mchips span:first-child{padding-left:0;border-left:none}
.ax-cover .mchips b{font-weight:700;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}

/* 네 칸 사다리 */
.axlad{display:grid;grid-template-columns:repeat(4,1fr);gap:24px}
.axstep{background:linear-gradient(150deg,#FFF7EF,#FBF2F8 45%,#F4F2FD 75%,#EFF5FE);border:1.5px solid #EDEAF2;border-radius:24px;padding:34px 32px 30px}
.axstep b{font-family:var(--fm);font-size:19px;font-weight:700;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.axstep h4{font-size:27px;font-weight:800;margin:12px 0 10px}
.axstep p{font-size:20px;line-height:1.5;color:var(--dim)}
.axstep.today{position:relative;box-shadow:0 18px 46px rgba(40,50,80,.10)}
.axstep.today::after{content:"TODAY";position:absolute;top:-16px;right:22px;font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.16em;color:#fff;background:var(--grad);padding:6px 16px;border-radius:999px}
.axband{background:linear-gradient(90deg,#FFF3E6,#F3EFFD);border:1.5px solid #EDEAF2;border-radius:18px;padding:24px 36px;font-size:23px;line-height:1.6;color:var(--dim)}
.axband strong{font-weight:800;color:var(--ink)}

/* 시연물 삽입 틀 */
.emb h2.head{font-size:58px}
.emb .lead{font-size:26px;margin-top:16px}
.embwrap{display:flex;gap:48px;align-items:stretch;flex:1;min-height:0;margin-top:34px}
/* 화면 하나만 놓는 장. 옆의 숫자와 메모를 걷어내고 화면을 남은 높이만큼 키운다 */
.embwrap.solo{justify-content:center}
.embbox{height:100%;aspect-ratio:16/9;border-radius:22px;overflow:hidden;border:1.5px solid var(--line);box-shadow:0 20px 54px rgba(30,40,60,.16);background:#04060d;flex:none}
.embbox{position:relative}
.embbox iframe{width:100%;height:100%;border:0;display:block}
/* 시연 시작 단추. 켜자마자 돌지 않고 눌러야 시작한다. 시작한 뒤에 다시 누르면 처음부터 돈다 */
.embbox.waiting iframe{visibility:hidden}
.embbox.waiting::before{content:"단추를 누르면 시연이 시작됩니다";position:absolute;inset:0;
  display:grid;place-items:center;font-family:var(--fm);font-size:17px;letter-spacing:.06em;color:#7A879F}
/* 시연을 켜기 전에는 검은 판 대신 그 시연의 한 장면을 세워 둔다.
   그림은 assets/illus/ 안의 갈무리이고, 단추를 누르면 iframe 이 그 위를 덮는다 */
.embbox.poster{background-size:cover;background-position:center;background-repeat:no-repeat}
.embbox.poster.waiting::before{place-items:end start;padding:0 0 22px 28px;color:#D6DEEE;
  background:linear-gradient(rgba(4,6,13,.1) 60%,rgba(4,6,13,.66))}
/* 판 안에 두면 돌아가는 화면을 가려서 판 오른쪽 바깥 여백에 세운다 */
.embwrap{position:relative}
.embplay{position:absolute;top:0;right:0;z-index:4;width:54px;height:54px;padding:0;border:0;
  border-radius:50%;background:var(--grad);display:grid;place-items:center;cursor:pointer;
  box-shadow:0 12px 28px rgba(200,90,120,.36);transition:transform .16s}
.embplay svg{width:20px;height:20px;fill:#fff;margin-left:3px}
.embplay .pa{display:none}
.embplay.is-playing .pi{display:none}
.embplay.is-playing .pa{display:block;margin-left:-3px}
.embplay:hover{transform:scale(1.07)}
.embside{flex:1;display:flex;flex-direction:column;justify-content:center;gap:26px;min-width:0}
.figrow{display:flex;align-items:baseline;gap:18px;padding:18px 0;border-top:1px solid var(--line)}
.figrow:first-child{border-top:none}
.figrow b{font-family:var(--fm);font-size:34px;font-weight:700;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;flex:none}
.figrow span{font-size:21px;color:var(--dim);line-height:1.45}
.embnote{font-size:20px;line-height:1.6;color:var(--dim);background:linear-gradient(150deg,#FFF7EF,#F4F2FD 70%,#EFF5FE);border:1.5px solid #EDEAF2;border-radius:18px;padding:22px 26px}
.embnote strong{color:var(--ink);font-weight:800}

/* 갈무리가 여덟 장이라 머리말이 크면 판이 낮아진다. 이 장에서만 제목과 리드를 한 단계 줄인다 */
.slide:has(.hypewrap) h2.head{font-size:56px}
.slide:has(.hypewrap) .lead{font-size:23px;margin-top:18px}

/* 콘텐츠 갈무리 판. 판이 세로를 끝까지 쓰고, 카드는 남은 높이에 맞춰 커진다.
   카드 크기를 픽셀로 박으면 덱마다 머리말 높이가 달라 위아래가 남는다. */
.hypewrap{display:grid;grid-template-columns:.62fr 1.38fr;gap:44px;align-items:stretch;flex:1;min-height:0;margin-top:30px}
.hypetxt{display:flex;flex-direction:column;justify-content:center;padding:0 8px;min-width:0}
.hypetxt .hk{font-family:var(--fm);font-size:24px;font-weight:700;letter-spacing:.2em;color:#A855F7;margin-bottom:26px}
.hypetxt h3{font-size:36px;line-height:1.35;margin:0 0 22px;color:var(--ink)}
.hypetxt p{font-size:21px;line-height:1.65;color:var(--dim);margin:0 0 18px}
.hypetxt p:last-child{font-size:20px;margin:0}
.hypebox{background:#111522;border-radius:28px;padding:24px 26px 22px;min-width:0;min-height:0;
  box-shadow:0 18px 42px rgba(15,23,42,.18);display:flex;flex-direction:column;gap:14px}
.hypebox .hlabel{flex:none;font-family:var(--fm);font-size:14px;letter-spacing:.18em;color:#AEB6CA;text-align:right}
.hyperow{display:flex;justify-content:center;align-items:center;gap:12px;min-height:0}
/* 두 줄의 높이 비율은 카드가 칸 폭을 꽉 쓰는 지점에서 나온 값이다.
   판이 작아지면 카드도 같이 작아지고, 폭이 모자라면 max-width가 먼저 걸려 넘치지 않는다. */
.hyperow.r1{flex:148 1 0}
.hyperow.r2{flex:322 1 0}
.hyperow > div{height:100%;max-width:calc((100% - 36px) / 4);border-radius:10px;overflow:hidden;
  background:#fff;border:1px solid rgba(30,42,80,.22);box-shadow:0 3px 9px rgba(15,23,42,.16)}
.hyperow.r1 > div{aspect-ratio:16/9}
/* 세로 카드는 갈무리 원본이 0.82라 그 비율로 둔다. 2대 3으로 자르면 좌우가 잘린다 */
.hyperow.r2 > div{aspect-ratio:41/50}
.hyperow img{width:100%;height:100%;object-fit:cover;display:block}

/* 관제실 4분할 */
.quad{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:40px}
.qcell{background:#232732;border-radius:22px;overflow:hidden;box-shadow:0 18px 46px rgba(20,25,40,.22)}
.qcell .qbar{display:flex;align-items:center;justify-content:space-between;padding:14px 22px;border-bottom:1px solid rgba(255,255,255,.08)}
.qcell .qbar b{font-size:19px;font-weight:800;color:#fff}
.qcell .qbar span{font-family:var(--fm);font-size:14px;letter-spacing:.08em;color:#8B93A6}
.qcell .qbar span em{font-style:normal;font-weight:700;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.qcell .qbody{padding:18px 24px;font-family:var(--fm);font-size:16.5px;line-height:1.95;color:#C6CCDA;min-height:146px}
.qcell .qbody .qok i{font-style:normal;color:#6EE7A0;margin-right:10px}
.qcell .qbody .qrun i{font-style:normal;margin-right:10px;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.qcell .qbody .qwait i{font-style:normal;color:#8B93A6;margin-right:10px}

/* 질문 카드 두 장 */
.qacard{background:#fff;border:1.5px solid var(--line);border-radius:24px;padding:32px 36px;box-shadow:0 14px 40px rgba(40,50,80,.07)}
.qacard + .qacard{margin-top:26px;border:2px solid transparent;background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}
.qacard .qlabel{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.16em;color:var(--faint);margin-bottom:18px}
.qacard + .qacard .qlabel{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.qacard .qq{font-size:24px;font-weight:700;line-height:1.5}
.qacard .qa{margin-top:16px;padding-top:16px;border-top:1.5px solid var(--line2);font-size:20.5px;line-height:1.6;color:var(--dim)}
.qaimg{display:flex;align-items:center;justify-content:center;min-height:0}
.qaimg img{max-width:100%;max-height:560px;width:auto;height:auto;display:block;border-radius:24px;
  background:#fff;box-shadow:0 18px 44px rgba(20,25,40,.12)}

/* 종이 대비 목록 */
.balist{display:grid;grid-template-columns:1fr 90px 1fr;align-items:stretch;margin-top:40px;flex:1;min-height:0}
.balist .paper{display:flex;flex-direction:column;justify-content:center}
.paper .plist{list-style:none;display:flex;flex-direction:column;gap:14px;margin-top:6px}
.paper .plist.two{display:grid;grid-template-columns:1fr 1fr;gap:14px 22px}
.paper .plist li{font-size:23px;line-height:1.5;color:var(--dim);padding-left:26px;position:relative}
.paper .plist li::before{content:"";position:absolute;left:0;top:13px;width:10px;height:10px;border-radius:50%;background:#DDE1EA}
.paper.after .plist li{color:var(--ink);font-weight:600}
.paper.after .plist li::before{background:var(--grad)}
.paper .prole{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.14em;color:var(--faint);margin-top:22px;padding-top:18px;border-top:1.5px solid var(--line2)}
.paper.after .prole{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}

/* 10장. 왼쪽에 GA4 실제 화면, 오른쪽에 네 가지 방식을 두 줄 두 칸으로.
   그림은 assets/illus/s10.png 를 갈아 끼우면 바뀐다. 가로로 긴 판이라 권장 비율은 2.11:1 */
.waywrap{display:grid;grid-template-columns:auto 1fr;gap:44px;flex:1;min-height:0;
  align-items:stretch;margin-top:24px}
.wayart{align-self:center;width:780px;aspect-ratio:1400/664;border-radius:20px;overflow:hidden;
  background:#fff;border:1.5px solid var(--line);box-shadow:0 18px 44px rgba(20,25,40,.16)}
.wayart img{width:100%;height:100%;object-fit:cover;display:block}
.waywrap .axlad.ways{grid-template-columns:1fr 1fr;gap:20px;min-height:0;align-content:center}
.waywrap .axlad.ways .axstep{padding:26px 28px}
.waywrap .axlad.ways .axstep h4{font-size:23px}
.waywrap .axlad.ways .axstep p{font-size:17.5px;line-height:1.5}

/* 03장. 쏟아지는 AI 서비스 로고 벽. 다섯 칸 네 줄, 줄마다 성격이 같다 */
.logowall{display:grid;grid-template-columns:repeat(5,1fr);gap:16px;flex:1;min-height:0;
  align-content:center;margin-top:28px}
.logocell{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:13px;
  background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:20px 10px 16px;
  box-shadow:0 10px 26px rgba(40,50,80,.05)}
.logocell img{width:54px;height:54px;object-fit:contain;border-radius:12px}
.logocell span{font-size:17px;font-weight:700;color:var(--ink);letter-spacing:-.01em}

/* 네 칸 정리 */
.tools.four{grid-template-columns:repeat(2,1fr);gap:28px}
.tools.four .tool{min-height:170px}


/* 쓰는 법: 왼쪽 절차, 오른쪽 사실 */
.howto{display:grid;grid-template-columns:.95fr 1fr;gap:44px;margin-top:34px;flex:1;align-items:center;min-height:0}
.hflow{display:flex;flex-direction:column}
.hstep{display:flex;gap:24px;align-items:flex-start;padding:13px 0;position:relative}
.hstep b{flex:none;width:46px;height:46px;border-radius:50%;display:grid;place-items:center;
         background:var(--grad);color:#fff;font-family:var(--fm);font-size:19px;font-weight:700}
.hstep::before{content:"";position:absolute;left:23px;top:59px;bottom:-3px;width:2px;background:#E9E5EF}
.hstep:last-child::before{display:none}
.hstep h4{font-size:25px;font-weight:800;margin-top:8px}
.hstep p{font-size:20px;line-height:1.55;color:var(--dim);margin-top:7px}
.hfacts{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.hf{background:linear-gradient(150deg,#FFF7EF,#F4F2FD 70%,#EFF5FE);border:1.5px solid #EDEAF2;
    border-radius:20px;padding:26px 28px}
.hf span{font-family:var(--fm);font-size:14.5px;font-weight:700;letter-spacing:.16em;color:var(--faint)}
.hf b{display:block;font-size:26px;font-weight:800;margin:11px 0 9px;letter-spacing:-.02em;line-height:1.25}
.hf p{font-size:18.5px;line-height:1.5;color:var(--dim)}

/* 활용 예시: 답이 나오는 질문과 막히는 질문 */
.asks{display:grid;grid-template-columns:1fr 1fr;gap:34px;margin-top:34px;flex:1;align-content:center}
.askcol{display:flex;flex-direction:column;gap:15px}
.askcol .ah{display:flex;align-items:center;gap:13px;font-size:22px;font-weight:800;padding-bottom:15px;
            border-bottom:1.5px solid var(--line2);color:var(--faint)}
.askcol .ah i{font-style:normal;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;
              font-size:15px;color:#fff;background:#C9CEDA;flex:none}
.askcol.yes .ah{color:var(--ink)}
.askcol.yes .ah i{background:var(--grad)}
.aq{background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:21px 25px}
.askcol.yes .aq{border:2px solid transparent;
                background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}
.aq h4{font-size:22px;font-weight:700;line-height:1.45}
.aq p{font-size:19px;line-height:1.5;color:var(--dim);margin-top:8px}

/* 마무리 */
.ax-imp .fg{justify-content:center;align-items:center;text-align:center;gap:38px}
.ax-imp h2.big{font-size:88px;font-weight:800;letter-spacing:-.04em;line-height:1.22}
.ax-imp .impband{font-size:26px;color:var(--dim);max-width:1180px;line-height:1.7}
.ax-imp .impsmall{font-size:22px;color:var(--faint);line-height:1.7}

/* RAG 장. 08장의 좌우 판(.cwrap)을 그대로 쓴다. 오른쪽은 진단이 아니라 순서라
   첫 칸만 강조하던 규칙을 끄고, 라벨 자리에 단계 이름을 넣는다 */
.ragslide .crow:first-child{border:1.5px solid var(--line);background:#fff;
  box-shadow:0 10px 28px rgba(40,50,80,.05)}
.ragslide .cjob{font-family:var(--fm);letter-spacing:.13em}
/* 그림이 정사각이라 칸도 정사각으로 잡는다. 너비는 높이에서 받아 가므로 판이 커지면 함께 넓어진다 */
.ragslide .cwrap{grid-template-columns:auto 1fr}
.ragslide .cshot{height:100%;aspect-ratio:1;background:#EDF0F6;
  box-shadow:0 18px 44px rgba(40,50,80,.12)}
"""


PLAY_JS = """
/* 시연 단추는 세 단계로 돈다. 처음에는 시작(누를 때 iframe 을 붙이므로 켜자마자 돌지 않는다),
   돌아가는 중에는 일시정지, 멈춘 뒤에는 이어 보기. 시연물 쪽은 postMessage 로 받는다 */
document.addEventListener('click',function(e){
  var b=e.target.closest('[data-embplay]'); if(!b) return;
  var box=b.closest('.embwrap').querySelector('.embbox'), f=box.querySelector('iframe');
  var st=b.getAttribute('data-state')||'idle';
  if(st==='idle'){
    if(f&&f.dataset.src) f.src=f.dataset.src;
    box.classList.remove('waiting');
  }else{
    try{f.contentWindow.postMessage({ax:st==='playing'?'pause':'play'},'*')}catch(err){}
  }
  var next=st==='playing'?'paused':'playing';
  b.setAttribute('data-state',next);
  b.classList.toggle('is-playing',next==='playing');
  b.setAttribute('aria-label',next==='playing'?'일시정지':'이어 보기');
});
"""


def furniture(n, clock):
    tl = f'<div class="clock">{clock}</div>' if clock else ''
    return (f'{brandbar()}{tl}'
            f'<div class="credit2">MERRY YEAR FOUNDATION × OSOMA</div>'
            f'<div class="pgno">{n:02d} / {TOTAL}</div>')


def ax(n, cls, body, clock):
    return (f'<div class="vp"><section class="slide ax {cls}" id="a{n}">{body}'
            f'{furniture(n, clock)}</section></div>')


def head_block(k1, k2, head_html, lead):
    return (f'{kicker(k1, k2)}'
            f'<h2 class="head">{head_html}</h2>'
            f'<p class="lead">{lead}</p>')


def pts_html(points):
    return "".join(f'<div class="pt"><b>{i:02d}</b><div><h4>{t}</h4><p>{d}</p></div></div>'
                   for i, (t, d) in enumerate(points, 1))


def howto(flow, facts):
    """쓰는 법 장표. 왼쪽에 지나야 하는 절차, 오른쪽에 누가 얼마나 걸리는지."""
    steps = "".join(f'<div class="hstep"><b>{i}</b><div><h4>{t}</h4><p>{d}</p></div></div>'
                    for i, (t, d) in enumerate(flow, 1))
    cards = "".join(f'<div class="hf"><span>{k}</span><b>{v}</b><p>{d}</p></div>'
                    for k, v, d in facts)
    return f'<div class="howto"><div class="hflow">{steps}</div><div class="hfacts">{cards}</div></div>'


def asks(yes, no):
    """활용 예시 장표. 답이 나오는 질문과 막히는 질문을 나란히 둔다."""
    def col(cls, mark, title, items):
        body = "".join(f'<div class="aq"><h4>{q}</h4><p>{a}</p></div>' for q, a in items)
        return f'<div class="askcol {cls}"><div class="ah"><i>{mark}</i>{title}</div>{body}</div>'
    return ('<div class="asks">'
            + col("yes", "&check;", "이렇게 물으면 답이 나옵니다", yes)
            + col("no", "&times;", "여기서 막힙니다", no)
            + '</div>')


def split(n, k1, k2, head_html, header_text, lead, points, right, clock, cls=""):
    HEADERS[n] = header_text
    body = ('<div class="fg">'
            + head_block(k1, k2, head_html, lead)
            + f'<div class="axcols"><div class="points">{pts_html(points)}</div>'
              f'<div class="rcol">{right}</div></div></div>')
    return ax(n, cls, body, clock)


def wide(n, k1, k2, head_html, header_text, lead, inner, clock, cls=""):
    HEADERS[n] = header_text
    body = ('<div class="fg">'
            + head_block(k1, k2, head_html, lead)
            + inner + '</div>')
    return ax(n, cls, body, clock)


def band(html, top=0):
    style = f' style="margin-top:{top}px"' if top else ''
    return f'<div class="axband"{style}>{html}</div>'


# ── 01 표지 ──────────────────────────────────────────────────────────
def a1(n):
    HEADERS[n] = "AI와 함께하는 미래, 일의 의미는 어떻게 달라질까요"
    aur = '<i class="aur a1"></i><i class="aur a2"></i><i class="aur a3"></i><i class="aur a4"></i>'
    sig = ('<svg class="signal" viewBox="0 0 660 660">'
           '<defs><linearGradient id="sg" x1="0" y1="0" x2="1" y2="1">'
           '<stop offset="0" stop-color="#FF7A1A"/><stop offset=".34" stop-color="#FF4D6D"/>'
           '<stop offset=".68" stop-color="#A855F7"/><stop offset="1" stop-color="#3B82F6"/>'
           '</linearGradient></defs>'
           '<circle class="ring" cx="330" cy="330" r="80" fill="none" stroke="url(#sg)" stroke-width="2.5" opacity=".95"/>'
           '<circle class="ring" cx="330" cy="330" r="160" fill="none" stroke="url(#sg)" stroke-width="2.5" opacity=".62"/>'
           '<circle class="ring" cx="330" cy="330" r="240" fill="none" stroke="url(#sg)" stroke-width="2.5" opacity=".4"/>'
           '<circle class="ring" cx="330" cy="330" r="320" fill="none" stroke="url(#sg)" stroke-width="2.5" opacity=".22"/>'
           '<circle class="rip" cx="330" cy="330" r="300" fill="none" stroke="url(#sg)" stroke-width="3"/>'
           '<circle class="rip r2" cx="330" cy="330" r="300" fill="none" stroke="url(#sg)" stroke-width="3"/>'
           '<circle cx="330" cy="330" r="14" fill="url(#sg)"/></svg>')
    body = (f'{aur}{sig}<div class="fg">'
            '<h1>AI와 함께하는 미래,<br><span class="gt">일의 의미는 어떻게 달라질까요</span></h1>'
            '<p class="sub">AI가 나의 일을 대신할 때, 일의 본질과 우리의 역할을 함께 생각해봅니다.</p>'
            '<div class="mchips"><span><b>5</b> PARTS</span><span><b>REAL</b> DATA</span></div>'
            '</div>')
    return ax(n, "ax-cover", body, "MERRY YEAR FOUNDATION / AX SHOWCASE")


# ── 04 맡기는 방식 ───────────────────────────────────────────────────
# ── 03 쏟아지는 AI 서비스 ────────────────────────────────────────────
def a_flood(n):
    """많이 언급되는 모델과 서비스 스무 개를 로고로 늘어놓는다.

    줄마다 성격이 같다. 첫 줄 대화형, 둘째 줄 검색과 모델, 셋째 줄 미디어 생성, 넷째 줄 업무 도구.
    로고는 assets/logos 아래에 있고 각 서비스의 파비콘을 받아 두었다.
    """
    rows = [("chatgpt", "ChatGPT"), ("claude", "Claude"), ("gemini", "Gemini"),
            ("copilot", "Copilot"), ("grok", "Grok"),
            ("perplexity", "Perplexity"), ("deepseek", "DeepSeek"), ("glm", "GLM"),
            ("mistral", "Mistral"), ("qwen", "Qwen"),
            ("midjourney", "Midjourney"), ("higgsfield", "Higgsfield"), ("runway", "Runway"),
            ("elevenlabs", "ElevenLabs"), ("suno", "Suno"),
            ("cursor", "Cursor"), ("replit", "Replit"), ("orca", "Orca"),
            ("paseo", "Paseo"), ("obsidian", "Obsidian")]
    cells = "".join(f'<div class="logocell"><img src="assets/logos/{f}.png" alt="{name} 로고">'
                    f'<span>{name}</span></div>' for f, name in rows)
    inner = (f'<div class="logowall">{cells}</div>'
             + band('<strong>다 따라잡을 수는 없습니다.</strong> '
                    '오늘 이야기는 도구 목록이 아니라, 무엇이 새로 나와도 흔들리지 않는 일하는 방식입니다.', 26))
    return wide(n, P1, "따라잡기의 불안", '이렇게 많은 AI 서비스가 <span class="gt">쏟아지고 있습니다</span>',
                "쏟아지는 AI 모델과 서비스 스무 개",
                "많이 언급되는 AI 모델과 서비스만 추려도 스무 개가 넘습니다. 대화형 AI와 모델, 미디어 생성, 업무 도구까지 다달이 새 이름이 나옵니다.",
                inner, "")


def a3(n):
    steps = [("묻기", "채팅으로 묻고 답을 받습니다. 결과는 대화창에 남습니다.", "", "message"),
             ("같이 고치기", "내 문서를 열어 놓고 같이 고칩니다. 결과는 문서에 남습니다.", "", "editdoc"),
             ("통째로 맡기기", "목표만 정해 주면 과정은 AI가 진행합니다. 결과는 파일과 기록으로 남습니다.", "today", "bolt"),
             ("팀으로 시키기", "역할이 다른 AI 여럿이 동시에 일합니다. 결과는 업무 흐름으로 남습니다.", "today", "users")]
    nodes = "".join(f'<div class="axstep {c}">{icon(ic)}<b>STEP {i}</b><h4>{t}</h4><p>{d}</p></div>'
                    for i, (t, d, c, ic) in enumerate(steps, 1))
    inner = ('<div class="vcen">'
             f'<div class="axlad">{nodes}</div>'
             + band('앞의 두 단계는 이미 하고 계실 겁니다. <strong>오늘 보시는 것은 셋째와 넷째 단계입니다.</strong>')
             + '</div>')
    return wide(n, P1, "AI 활용의 핵심", '중요한 것은<br><span class="gt">무엇을 어떻게 시킬지</span>입니다',
                "무엇을 물을지, 어디까지 맡길지 정하는 네 단계",
                "최신 AI의 이름을 따라잡는 것보다 먼저 해야 할 일은, 지금 내 업무에서 무엇을 물을 수 있는지와 어떤 방향으로 물을지를 정하는 것입니다.",
                inner, "")


# ── 08 조직을 모르는 AI ──────────────────────────────────────────────
def a4(n):
    # 오른쪽은 글 대신 그림 한 장으로 둔다. 위는 자료 없이 물었을 때, 아래는 자료를 읽힌 뒤.
    # 그림은 assets/illus/s10_ctx.png 를 갈아 끼우면 바뀐다. 세로로 긴 판이라 권장 비율은 0.8:1
    right = ('<div class="qaimg"><img src="assets/illus/s10_ctx.png" '
             'alt="자료 없이 물었을 때와 재단 자료를 읽힌 뒤의 결과 대비"></div>')
    points = [("질문을 아무리 다듬어도 한계가 있습니다",
               "재단을 모르는 상대에게는 일반론이 돌아옵니다."),
              ("맥락은 자료로 줍니다",
               "웹 구조, 캠페인 기록, 후원 흐름을 한 번 읽히면 다음 질문부터 답이 달라집니다."),
              ("이 자료는 오늘 만든 것이 아닙니다",
               "재단이 2025년부터 쌓아 온 기록 그대로입니다.")]
    return split(n, P2, "재단 자료 읽히기", 'AI는 열매나눔재단을<br><span class="gt">얼마나</span> 알까요?',
                 "AI가 열매나눔재단을 아는 만큼",
                 "우리가 준 자료만큼만 압니다. 질문을 다듬는 것보다 재단이 어떻게 일하는지 읽히는 쪽이 결과를 더 크게 바꿉니다.",
                 points, right, "")


# ── 09 같은 자료를 보는 네 가지 방식 ─────────────────────────────────
def a5(n):
    steps = [("표로 확인", "내려받아 정렬하고 피벗을 돌립니다. 숫자는 다 있지만 사람이 다 읽어야 합니다.", "", "table"),
             ("대시보드", "전문가가 볼 지표를 골라 화면에 걸어 둡니다. 물을 수 있는 것은 걸어 둔 만큼입니다.", "", "chart"),
             ("자연어 질의", "말로 묻고 근거와 함께 답을 받습니다. 질문을 바꾸는 데 비용이 들지 않습니다.", "", "message"),
             ("구조로 남기기", "표를 점과 선으로 바꿔 두면 사람도 보고 AI도 읽습니다.", "", "network")]
    nodes = "".join(f'<div class="axstep {c}">{icon(ic)}<b>방식 {i}</b><h4>{t}</h4><p>{d}</p></div>'
                    for i, (t, d, c, ic) in enumerate(steps, 1))
    shot = ('<div class="wayart"><img src="assets/illus/s10.png" '
            'alt="열매나눔재단 GA4 트래픽 획득 보고서 화면"></div>')
    inner = ('<div class="vcen">'
             f'<div class="waywrap">{shot}<div class="axlad ways">{nodes}</div></div>'
             + band('네 방식 모두 지금도 쓰입니다. '
                    '<strong>뒤로 갈수록 질문 하나를 더 던지는 비용이 줄어듭니다.</strong>')
             + '</div>')
    return wide(n, P2, "네 가지 방식", '같은 GA4를 보는 <span class="gt">네 가지 방식</span>',
                "같은 GA4를 보는 네 가지 방식",
                "지금부터 보실 네 화면은 전부 같은 기록에서 나왔습니다. 자료는 같고 담는 방식만 다릅니다.",
                inner, "")


# ── 10 방식 1. 표 화면 ───────────────────────────────────────────────
def a6(n):
    inner = ('<div class="embwrap solo">'
             '<div class="embbox"><iframe src="아날로그대비.html?view=table" loading="lazy" '
             'allow="fullscreen" title="GA4 원본을 내려받은 표"></iframe></div>'
             '</div>')
    return wide(n, P2, "방식 1 표", '<span class="gt">1,598줄</span>짜리 엑셀, 어디까지 읽어 보셨나요?',
                "1,598줄짜리 엑셀",
                "GA4에서 페이지 보고서를 내려받으면 이 파일이 나옵니다. 2025년 8월부터 389일이 다 들어 있습니다.",
                inner, "", cls="emb")


# ── 11 방식 1. 쓰는 법 ───────────────────────────────────────────────
def a7(n):
    flow = [("내려받기", "보고서를 고르고 기간을 잡아 파일로 받습니다."),
            ("열 정리", "쓸 열만 남기고 표기를 맞춥니다. 한글이 깨지면 다시 받습니다."),
            ("정렬과 필터", "조회수 순으로 세우고 필요 없는 도메인을 걸러 냅니다."),
            ("피벗", "월별이나 채널별로 묶으려면 피벗 테이블을 새로 만듭니다."),
            ("옮겨 적기", "나온 숫자를 보고서 문서에 직접 옮깁니다.")]
    facts = [("WHO", "담당자 한 사람", "엑셀을 다룰 줄 아는 사람에게 몰립니다."),
             ("TIME", "반나절", "익숙해져도 서너 시간이 듭니다."),
             ("AGAIN", "처음부터 다시", "질문이 하나 늘면 첫 단계로 돌아갑니다."),
             ("LEFT", "숫자 몇 개", "과정은 사라지고 결과 숫자만 문서에 남습니다.")]
    return wide(n, P2, "방식 1 표", '숫자 하나 보고서에 넣는 데 <span class="gt">반나절</span>',
                "숫자 하나에 반나절",
                "표로 볼 때는 이 순서를 지나야 숫자 하나가 보고서에 들어갑니다. 지금도 이렇게 하고 계신가요?",
                howto(flow, facts), "")


# ── 12 방식 1. 활용 예시 ─────────────────────────────────────────────
def a8(n):
    yes = [("조회수가 가장 많은 페이지는 어디일까요", "조회수 열을 내림차순으로 세우면 바로 나옵니다."),
           ("지난달 후원은 몇 건일까요", "일자별 시트에서 기간을 잘라 더합니다."),
           ("어느 채널이 세션을 가장 많이 보냈을까요", "채널 시트를 정렬하면 됩니다.")]
    no = [("사람들이 어떤 길로 후원까지 갔을까요", "페이지 사이의 이동은 어느 열에도 없습니다."),
          ("이 캠페인은 왜 반응이 좋았을까요", "표는 무엇이 일어났는지만 적고 이유는 적지 않습니다."),
          ("지금 고칠 만한 페이지는 어디일까요", "표는 순서대로 세워 줄 뿐, 어디를 고칠지는 알려 주지 않습니다.")]
    inner = (asks(yes, no)
             + band('<strong>표에 애초에 없는 정보가 있습니다.</strong> '
                    '페이지 사이를 오간 기록은 내려받는 순간 사라집니다.', 30))
    return wide(n, P2, "방식 1 표", '표로 답이 나오는 질문, <span class="gt">나오지 않는 질문</span>',
                "표로 답이 나오는 질문과 나오지 않는 질문",
                "표로도 답이 나오는 질문이 있고, 표로는 시작도 못 하는 질문이 있습니다.",
                inner, "")


# ── 13 방식 2. 대시보드 화면 ─────────────────────────────────────────
def a9(n):
    inner = ('<div class="embwrap solo">'
             '<div class="embbox"><iframe src="아날로그대비.html?view=dash" loading="lazy" '
             'allow="fullscreen" title="같은 자료를 옮겨 담은 대시보드"></iframe></div>'
             '</div>')
    return wide(n, P2, "방식 2 대시보드", '대시보드: 전문가가 <span class="gt">중요한 지표를 골라</span> 만든 보고서',
                "전문가가 미리 골라 둔 대시보드",
                "같은 자료를 대시보드로 옮기면 이렇게 보입니다. 아침마다 여는 화면이 됩니다.",
                inner, "", cls="emb")


# ── 14 방식 2. 쓰는 법 ───────────────────────────────────────────────
def a10(n):
    flow = [("볼 것 정하기", "무엇을 매일 볼지 담당자와 정합니다. 이 단계가 가장 오래 걸립니다."),
            ("자료 연결", "GA4나 데이터베이스를 도구에 붙입니다."),
            ("지표와 기준", "세션, 후원, 수익처럼 볼 값과 나눌 기준을 고릅니다."),
            ("화면 배치", "카드와 차트를 놓고 색과 순서를 맞춥니다."),
            ("공유", "주소를 나누면 그때부터 누구나 열어 봅니다.")]
    facts = [("WHO", "만드는 사람 따로", "대개 외부 도움이나 데이터 담당이 맡습니다."),
             ("TIME", "며칠에서 몇 주", "무엇을 볼지 고르는 데 걸리고 만드는 데 또 걸립니다."),
             ("AGAIN", "다시 만들기", "화면에 없는 지표는 요청하고 기다려야 합니다."),
             ("LEFT", "매일 여는 화면", "한 번 만들면 오래 씁니다. 이것이 대시보드의 값어치입니다.")]
    return wide(n, P2, "방식 2 대시보드", '만드는 데 <span class="gt">며칠</span>, 여는 데 <span class="gt">몇 초</span>',
                "대시보드를 만들고 여는 일",
                "대시보드는 만드는 사람과 쓰는 사람이 다릅니다. 그래서 만들 때 대개 외부 도움이 들어갑니다.",
                howto(flow, facts), "")


# ── 15 방식 2. 활용 예시 ─────────────────────────────────────────────
def a11(n):
    yes = [("이번 주 세션이 지난주보다 늘었을까요", "카드에 붙은 화살표가 바로 답합니다."),
           ("어느 채널이 후원을 가장 많이 만들었을까요", "표 위젯을 후원 열로 세우면 나옵니다."),
           ("작년 8월에 무슨 일이 있었을까요", "꺾은선의 봉우리가 날짜를 알려 줍니다.")]
    no = [("이 캠페인은 왜 지난달보다 잘됐을까요", "두 숫자를 나란히 놓을 뿐 이유를 잇지 않습니다."),
          ("이 캠페인 페이지 다음으로 어디를 봤을까요", "화면에 없는 질문이라 다시 만들어야 합니다."),
          ("다음 캠페인은 무엇을 닮게 만들까요", "판단은 화면 밖에 남습니다.")]
    inner = (asks(yes, no)
             + band('<strong>대시보드는 질문을 미리 정해 둔 화면입니다.</strong> '
                    '정해 둔 질문에는 빠르고, 새 질문이 생기면 화면을 다시 만들어야 합니다.', 30))
    return wide(n, P2, "방식 2 대시보드", '대시보드로 답이 나오는 질문, <span class="gt">나오지 않는 질문</span>',
                "대시보드로 답이 나오는 질문과 나오지 않는 질문",
                "미리 걸어 둔 질문에는 아주 빠르게 답합니다. 걸어 두지 않은 질문 앞에서는 멈춥니다.",
                inner, "")


# ── 16 방식 3. 자연어 질의 화면 ──────────────────────────────────────
def a12(n):
    inner = ('<div class="embwrap solo">'
             '<div class="embbox"><iframe src="아날로그대비.html?view=ai" loading="lazy" '
             'allow="fullscreen" title="같은 자료를 놓고 말로 묻기"></iframe></div>'
             '</div>')
    return wide(n, P2, "방식 3 자연어 질의", '<span class="gt">말로 묻고</span> 근거까지 받기',
                "말로 묻고 근거까지 받기",
                "같은 자료를 AI에게 읽히고 말로 물었습니다. 답에 어느 줄을 봤는지 근거 표가 같이 붙습니다.",
                inner, "", cls="emb")


# ── 16 자연어 질의의 속. RAG ─────────────────────────────────────────
def a_rag(n):
    """방금 본 답이 어디서 나왔는지 푸는 장.

    왼쪽은 그림 한 장, 오른쪽은 단계 셋이다. 그림은 assets/illus/rag.png 를 갈아 끼우면 바뀐다.
    판은 08장의 좌우 구도(.cwrap)를 그대로 쓴다.
    """
    steps = [("찾기", "질문과 관련 있는 대목만 골라냅니다",
              "넘긴 자료를 통째로 읽지 않습니다. 질문과 가까운 몇 줄을 먼저 찾습니다."),
             ("붙이기", "찾은 대목을 질문과 함께 넘깁니다",
              "AI는 이 대목을 읽고 답합니다. 답에 어느 줄을 봤는지 근거가 함께 붙는 이유입니다."),
             ("답하기", "찾은 범위 안에서만 답합니다",
              "자료에 없는 것은 답하지 못합니다. 자료를 고치면 다음 답이 바로 달라집니다.")]
    rows = "".join(f'<div class="crow"><div class="cjob">{lab}</div><h4>{t}</h4><p>{d}</p></div>'
                   for lab, t, d in steps)
    shot = ('<div class="cshot"><img src="assets/illus/rag.png" '
            'alt="질문에서 시작해 자료를 찾고, 찾은 문서 몇 개를 AI에게 넘겨 답을 만드는 흐름"></div>')
    inner = (f'<div class="cwrap">{shot}<div class="creply">{rows}</div></div>'
             + band('<strong>RAG는 AI를 다시 학습시키는 방식이 아닙니다.</strong> '
                    '물을 때마다 우리 자료를 찾아 읽게 하는 방식이라, 넘기지 않은 것은 답에 나오지 않습니다.', 26))
    return wide(n, P2, "방식 3 자연어 질의", 'AI는 우리 자료를 <span class="gt">어떻게 찾아 읽을까요?</span>',
                "AI가 우리 자료를 찾아 읽는 방식",
                "방금 본 답은 AI가 원래 알던 내용이 아닙니다. 물을 때마다 우리가 넘긴 자료에서 관련된 대목을 찾아 그 부분만 읽고 답합니다. 이 방식을 RAG라고 부릅니다.",
                inner, "", cls="ragslide")


# ── 17 방식 3. 쓰는 법 ───────────────────────────────────────────────
def a13(n):
    flow = [("자료 읽히기", "내려받은 원본을 그대로 넘깁니다. 미리 손질하지 않아도 됩니다."),
            ("말로 묻기", "지표 이름을 모르는 채 궁금한 대로 적습니다."),
            ("근거 확인", "어느 줄을 보고 답했는지 같이 옵니다. 숫자는 담당자가 대조합니다."),
            ("되묻기", "답을 보고 다시 물으면 바로 더 파고듭니다.")]
    facts = [("WHO", "궁금한 사람이 직접", "엑셀을 다룰 줄 몰라도 물을 수 있습니다."),
             ("TIME", "몇 분", "자료를 읽히는 데 한 번, 그다음은 물을 때마다 몇 분입니다."),
             ("AGAIN", "한 번 더 묻기", "질문을 하나 더 던지는 데 시간이 거의 들지 않습니다."),
             ("LEFT", "대화 기록", "답이 글이라 다음 사람은 처음부터 다시 읽어야 합니다.")]
    return wide(n, P2, "방식 3 자연어 질의", '한 번 정보를 주면 계속 <span class="gt">되물을 수 있습니다</span>',
                "한 번 정보를 주면 계속 되묻기",
                "만드는 단계가 없어지고 묻는 단계만 남습니다. 대신 확인하는 단계가 새로 생깁니다.",
                howto(flow, facts), "")


# ── 18 방식 3. 활용 예시 ─────────────────────────────────────────────
def a14(n):
    yes = [("어느 채널이 후원까지 가장 잘 이어졌을까요", "채널별 기록을 비교해 어디가 앞서는지 답합니다."),
           ("이 캠페인은 다른 캠페인과 무엇이 다를까요", "시트 여러 개를 한 번에 놓고 비교합니다."),
           ("보고서에 넣을 문장으로 정리해 주세요", "숫자와 문장을 한 번에 받습니다.")]
    no = [("전체가 어떻게 생겼는지 한눈에 보여 주세요", "답이 글이라 그림이 머릿속에 그려지지 않습니다."),
          ("이 숫자가 맞는지 확인해 주세요", "근거는 붙지만 맞고 틀림은 담당자가 봐야 합니다."),
          ("다음 사람도 이 맥락을 이어받게 해 주세요", "대화는 흩어집니다. 남기려면 따로 정리해야 합니다.")]
    inner = (asks(yes, no)
             + band('<strong>물을 수 있는 폭은 넓어졌지만 답은 여전히 글입니다.</strong> '
                    '전체를 한눈에 보는 일과 다음 사람에게 넘기는 일이 남습니다.', 30))
    return wide(n, P2, "방식 3 자연어 질의", '자연어 질의로 답이 나오는 질문, <span class="gt">나오지 않는 질문</span>',
                "자연어 질의로 답이 나오는 질문과 나오지 않는 질문",
                "앞의 두 화면에서 막혔던 질문에 여기서 답이 나옵니다. 그래도 남는 것이 있습니다.",
                inner, "")


# ── 19 방식 4. 조직 기억 (웹구조그래프) ──────────────────────────────
def a15(n):
    inner = ('<div class="embwrap solo">'
             '<div class="embbox waiting poster" style="background-image:url(assets/illus/emb_graph.png)">'
             '<iframe data-src="웹구조그래프.html" loading="lazy" '
             'allow="fullscreen" title="열매나눔재단 웹 구조 지도"></iframe></div>'
             '<button class="embplay" type="button" aria-label="시연 시작" data-embplay><svg viewBox="0 0 24 24" aria-hidden="true"><path class="pi" d="M8 5l11 7-11 7z"/><path class="pa" d="M7 5h3.4v14H7zM13.6 5H17v14h-3.4z"/></svg></button>'
             '</div>')
    return wide(n, P2, "방식 4 구조",
                'AI의 눈으로 보는 열매나눔재단<br><span class="gt">웹사이트 데이터 구조</span>',
                "AI의 눈으로 보는 열매나눔재단 웹사이트 데이터 구조",
                "앞의 세 화면과 같은 자료입니다. 표도 대시보드도 담지 못한 페이지 사이 이동을 그렸습니다.",
                inner, "", cls="emb")


# ── 20 방식 4. 시간 축 (캠페인레이스) ────────────────────────────────
def a16(n):
    inner = ('<div class="embwrap solo">'
             '<div class="embbox waiting"><iframe data-src="캠페인레이스.html" loading="lazy" '
             'allow="fullscreen" title="열매나눔재단 캠페인 모금 레이스"></iframe></div>'
             '<button class="embplay" type="button" aria-label="시연 시작" data-embplay><svg viewBox="0 0 24 24" aria-hidden="true"><path class="pi" d="M8 5l11 7-11 7z"/><path class="pa" d="M7 5h3.4v14H7zM13.6 5H17v14h-3.4z"/></svg></button>'
             '</div>')
    return wide(n, P2, "방식 4 구조", '389일 동안 쌓인 <span class="gt">후원금액</span>',
                "389일 동안 쌓인 후원금액",
                "재단의 시간도 자료입니다. 어떤 캠페인이 언제 앞섰는지가 그대로 남아 있습니다.",
                inner, "", cls="emb")


# ── 21 방식 4. 쓰는 법 ───────────────────────────────────────────────
def a17(n):
    flow = [("원본 넘기기", "표로 내려받던 그 파일을 그대로 씁니다."),
            ("점과 선 정하기", "무엇을 점으로 두고 무엇을 선으로 이을지 담당자가 정합니다."),
            ("위치 계산", "점 1,151개의 위치를 미리 계산해 고정해 둡니다."),
            ("화면 만들기", "사람이 보는 화면과 AI가 읽을 자료가 같은 파일에서 나옵니다.")]
    facts = [("WHO", "담당자가 정하고 AI가 만들기", "무엇을 이을지는 담당자가 정합니다."),
             ("TIME", "처음 한 번", "만드는 일은 한 번뿐이고 그다음부터는 자료만 바꿔 넣으면 됩니다."),
             ("AGAIN", "화면에서 바로", "찾아서 눌러 봅니다. 다시 만들지 않습니다."),
             ("LEFT", "파일 하나", "사람도 열어 보고 AI도 읽습니다.")]
    return wide(n, P2, "방식 4 구조", '한 번 만들어 두고 <span class="gt">자료만 바꿔</span> 넣기',
                "한 번 만들어 두고 자료만 바꿔 넣는 일",
                "앞의 셋과 달리 자료를 점과 선으로 바꾸는 단계가 먼저 있습니다. 그 단계를 담당자가 AI에게 맡깁니다.",
                howto(flow, facts), "")


# ── 22 방식 4. 활용 예시 ─────────────────────────────────────────────
def a18(n):
    yes = [("전체가 어떻게 생겼을까요", "한 화면에 다 들어옵니다. 설명할 말이 필요 없습니다."),
           ("이 페이지가 후원과 어떻게 이어질까요", "눌러서 이어진 선을 따라가면 됩니다."),
           ("AI에게 재단을 어떻게 설명할까요", "이 파일을 넘깁니다. 매번 다시 적지 않아도 됩니다.")]
    no = [("무엇을 이을지 누가 정할까요", "무엇을 잇는지 정하는 일은 여전히 담당자 몫입니다."),
          ("이 그림이 맞는지 누가 볼까요", "자료가 틀리면 그림도 같이 틀립니다."),
          ("그래서 무엇을 할지 누가 정할까요", "보이는 것과 정하는 것은 다른 일입니다.")]
    inner = (asks(yes, no)
             + band('<strong>네 방식을 지나오며 줄어든 것은 매번 다시 설명해야 하는 말입니다.</strong> 담당자의 일은 그대로입니다.', 30))
    return wide(n, P2, "방식 4 구조", '구조로 남기면 <span class="gt">사람도 보고 AI도 읽습니다</span>',
                "사람이 보는 화면과 AI가 읽는 자료가 하나인 방식",
                "네 번째 방식에서 달라지는 것은 답이 어디에 어떻게 남는지입니다.",
                inner, "")


# ── 27 한 업무를 네 역할로 ───────────────────────────────────────────
def a19(n):
    cells = [("조사", "3단계 중 3단계",
              '<div class="qok"><i>&check;</i>지난 캠페인과 반응 정리</div>'
              '<div class="qok"><i>&check;</i>후원 유입 경로 확인</div>'
              '<div class="qok"><i>&check;</i>반복해서 쓰인 문구 추출</div>'),
             ("전략", "3단계 중 2단계",
              '<div class="qok"><i>&check;</i>보낼 대상 후보 정리</div>'
              '<div class="qrun"><i>&#9654;</i>메시지 방향 3안 작성 중</div>'),
             ("제작", "3단계 중 2단계",
              '<div class="qok"><i>&check;</i>메일 초안 작성</div>'
              '<div class="qrun"><i>&#9654;</i>배너 문구 배치 중</div>'),
             ("검수", "3단계 중 1단계",
              '<div class="qrun"><i>&#9654;</i>당사자를 존중하는 표현인지 점검</div>'
              '<div class="qwait"><i>&#9675;</i>숫자 근거 대조 대기</div>'
              '<div class="qwait"><i>&#9675;</i>지난 캠페인 중복 확인 대기</div>')]
    quad = "".join(f'<div class="qcell"><div class="qbar"><b>{t}</b><span><em>{s}</em></span></div>'
                   f'<div class="qbody">{b}</div></div>' for t, s, b in cells)
    inner = (f'<div class="quad">{quad}</div>'
             + band('<strong>담당자가 하던 업무 순서를 그대로 AI 역할로 옮긴 것입니다.</strong> '
                    '여기까지가 초안이고, 어느 안을 내보낼지는 담당자가 고릅니다.', 26))
    return wide(n, P4, "업무 쪼개기", '연말 캠페인 기획을 <span class="gt">네 역할</span>로 나눠 시킵니다',
                "연말 캠페인 기획을 네 역할로",
                "한 번에 시키지 않습니다. 조사, 전략, 제작, 검수로 나누고 각각 맡깁니다.",
                inner, "")


# ── 32 쏟아지는 에이전트 콘텐츠 ──────────────────────────────────────
def a_hype(n):
    yt = [("yt_claudecode", "-1.2"), ("yt_gemini", "0.9"), ("yt_claude30", "-0.7"), ("yt_agent", "1.1")]
    card = [("card_team4", "0.8"), ("card_lessons", "-1.0"), ("card_cardnews", "1.2"), ("card_insta", "-0.8")]
    row1 = "".join(f'<div style="transform:rotate({r}deg)"><img src="assets/refs/{f}.jpg" alt=""></div>'
                   for f, r in yt)
    row2 = "".join(f'<div style="transform:rotate({r}deg)"><img src="assets/refs/{f}.jpg" alt=""></div>'
                   for f, r in card)
    inner = ('<div class="hypewrap">'
             '<div class="hypetxt">'
             '<div class="hk">FOMO</div>'
             '<h3>놓치면 뒤처질 것 같은 마음을<br><span class="gt">자극하는 장면들</span></h3>'
             '<p>새로운 기능과 도구를 지금 당장 따라잡아야 한다는 메시지는 빠르게 늘고 있습니다.</p>'
             '<p>하지만 모델이 발전할수록 기능과 개념은 서로 합쳐집니다. 오늘은 유행어보다 질문의 방향을 봅니다.</p>'
             '</div>'
             '<div class="hypebox">'
             '<div class="hlabel">AI 강의와 비법 콘텐츠</div>'
             f'<div class="hyperow r1">{row1}</div>'
             f'<div class="hyperow r2">{row2}</div>'
             '</div>'
             '</div>'
             + band('<strong>기능과 개념은 모델의 발전으로 빠르게 합쳐집니다.</strong> 따라잡을 것은 유행어가 아니라, 지금 AI에게 무엇을 물을지 정하는 능력입니다.', 22))
    return wide(n, P1, "따라잡기의 불안", '여러분도 이런 AI 강의 썸네일,<br><span class="gt">보신 적 있죠?</span>',
                "AI를 놓치면 뒤처질 것 같은 마음",
                "AI를 검색하면 상위에 노출되는 준이아빠블로그를 운영하는 저도 최신 기술을 계속 찾아 정리합니다. 하지만 매번 새 도구를 외우지 않으면 안 된다는 불안까지 따라갈 필요는 없습니다.",
                inner, "")


# ── 33 원격 지휘 (지휘실) ────────────────────────────────────────────
def a_orc(n):
    # 오른쪽 설명을 걷어내고 연출만 남긴다. 연출이라는 것과 세는 방식은 리드에서 말한다.
    inner = ('<div class="embwrap solo">'
             '<div class="embbox waiting"><iframe data-src="지휘실.html" loading="lazy" '
             'allow="fullscreen" title="한 사람이 여러 기기를 지휘하는 방식"></iframe></div>'
             '<button class="embplay" type="button" aria-label="시연 시작" data-embplay>'
             '<svg viewBox="0 0 24 24" aria-hidden="true">'
             '<path class="pi" d="M8 5l11 7-11 7z"/>'
             '<path class="pa" d="M7 5h3.4v14H7zM13.6 5H17v14h-3.4z"/></svg></button>'
             '</div>')
    return wide(n, P4, "여러 기기 지휘", '한 사람이 <span class="gt">여러 기기</span>를 동시에 지휘할 수도 있습니다',
                "한 사람이 여러 기기를 동시에 지휘하는 방식",
                "기기마다 에이전트와 터미널을 따로 열어 두면 서로 다른 업무를 동시에 지시할 수 있습니다. "
                "아래는 실제 화면이 아니라 그렇게 일하는 하루를 1분으로 압축한 연출입니다.",
                inner, "", cls="emb")


# ── 25 개인기에서 조직 규칙으로 ──────────────────────────────────────
def a20(n):
    before = ('<div class="paper"><div class="ptag">지금 / 매번 붙이던 말</div>'
              '<ul class="plist">'
              '<li>우리 재단 문체는 이렇습니다</li>'
              '<li>이런 표현은 피해 주세요</li>'
              '<li>숫자는 이 방식으로 적습니다</li>'
              '<li>보고서 순서는 이렇습니다</li>'
              '</ul>'
              '<div class="prole">잘 쓰는 한 사람의 요령으로 남습니다</div></div>')
    arrow = ('<div class="baarrow"><span><svg viewBox="0 0 24 24">'
             '<path d="M4 12h15M13 6l6 6-6 6"/></svg></span></div>')
    after = ('<div class="paper after"><div class="ptag">파일로 만든 뒤</div>'
             '<ul class="plist">'
             '<li>캠페인 문안 검토 규칙 파일 하나</li>'
             '<li>같은 폴더에 두고 팀이 같이 씁니다</li>'
             '<li>다음 업무부터 설명 없이 적용됩니다</li>'
             '<li>규칙이 바뀌면 파일만 고칩니다</li>'
             '</ul>'
             '<div class="prole">재단이 다시 쓰는 자산이 됩니다</div></div>')
    inner = (f'<div class="balist">{before}{arrow}{after}</div>'
             + band('여기서부터 AI 활용이 개인기를 벗어납니다. '
                    '<strong>한 사람이 잘 쓰던 방법을 팀이 다시 쓰게 만드는 일, 이것을 AX의 출발점으로 봅니다.</strong>', 34))
    return wide(n, P3, "규칙 파일", '매번 붙이던 설명을 <span class="gt">파일로</span> 만들면',
                "매번 붙이던 설명을 파일로 만들기",
                "재단 문체는 이렇다, 이런 표현은 피해 달라, 숫자는 이렇게 적는다. "
                "매번 붙이던 이 설명을 규칙 파일로 만들어 두면 다음 사람은 같은 말을 다시 하지 않아도 됩니다.",
                inner, "")


# ── 34 실습 ─────────────────────────────────────────────────────────
def a21(n):
    steps = [("나에게 맞는 결과 만들기",
              "업무 하나를 고르고 시작과 결과물을 정합니다. 반복, 탐색, 정리, 초안, 검토, 결정으로 단계를 나눕니다."),
             ("동료가 이해할 수 있는 결과로 바꾸기",
              "AI가 맡을 단계와 담당자가 맡을 단계를 나누고, 필요한 자료와 전제와 금지선을 적습니다."),
             ("재단 기준으로 검토하기",
              "무엇으로 검토하고 누가 책임질지 정합니다. 만든 사람이 아닌 동료가 봅니다."),
             ("누구나 다시 쓸 수 있는 자산으로 남기기",
              "설명서와 예시와 검수 기준을 결과물과 같이 남깁니다.")]
    nodes = "".join(f'<div class="stepn"><b>{i:02d}</b><h4>{t}</h4><p>{d}</p></div>'
                    for i, (t, d) in enumerate(steps, 1))
    inner = ('<div class="vcen">'
             f'<div class="steps">{nodes}</div>'
             + band('참석자 한 분의 업무를 지금 이 네 단계로 나눠 봅니다. '
                    '<strong>첫 단계는 혼자 해도 됩니다. 둘째 단계부터는 그 업무를 모르는 동료가 옆에 있어야 합니다.</strong>')
             + '</div>')
    return wide(n, P5, "실습", '실습: 내 업무 하나를 <span class="gt">네 단계</span>로',
                "실습. 내 업무 하나를 네 단계로",
                "프롬프트 실습이 아닙니다. 내 일 하나를 골라, 나에게 맞는 결과에서 동료도 쓸 수 있는 자산까지 네 단계로 나눠 봅니다.",
                inner, "")


# ── 36 사람과 AI의 몫 ────────────────────────────────────────────────
def a22(n):
    before = ('<div class="paper"><div class="ptag">지금 / 한 사람이 이어서</div>'
              '<ul class="plist two">'
              '<li>자료 찾기</li><li>옮겨 적기</li><li>정리하기</li><li>분석하기</li>'
              '<li>초안 쓰기</li><li>검수하기</li><li>다시 고치기</li>'
              '</ul>'
              '<div class="prole">일곱 가지가 모두 한 사람 몫입니다</div></div>')
    arrow = ('<div class="baarrow"><span><svg viewBox="0 0 24 24">'
             '<path d="M4 12h15M13 6l6 6-6 6"/></svg></span></div>')
    after = ('<div class="paper after"><div class="ptag">역할을 나눈 뒤</div>'
             '<ul class="plist">'
             '<li>담당자가 목표를 정합니다</li>'
             '<li>AI가 조사하고 정리하고 분석합니다</li>'
             '<li>AI가 초안을 쓰고 기준과 대조합니다</li>'
             '<li>담당자가 검토하고 결정합니다</li>'
             '</ul>'
             '<div class="prole">담당자 몫은 세 가지로 또렷해집니다</div></div>')
    inner = (f'<div class="balist">{before}{arrow}{after}</div>'
             + band('<strong>AI가 맡는 일이 늘수록 담당자가 할 일은 더 분명해집니다.</strong>', 34))
    return wide(n, P5, "마무리", 'AI에게 맡기고 나면<br>담당자 일이 <span class="gt">줄어들까요?</span>',
                "AI에게 맡긴 뒤 담당자 몫",
                "줄어드는 것이 아니라 또렷해집니다. 목표를 정하고, 검토하고, 결정하는 세 가지가 담당자 몫으로 남습니다.",
                inner, "")


# ── 37 담당자가 하는 다섯 가지 ───────────────────────────────────────
def a23(n):
    roles = [("목표를 정합니다", "무엇을 왜 하는지는 AI에게 시키기 전에 담당자가 적습니다.", "target"),
             ("맥락을 읽습니다", "무엇을 이을지, 어느 기록이 중요한지 담당자가 고릅니다.", "pin"),
             ("존엄과 공익을 지킵니다", "반응이 좋은 문구와 당사자를 존중하는 문구 사이에서 담당자가 고릅니다.", "heart"),
             ("AI의 결과를 검토합니다", "근거 표의 숫자를 원본과 대조하는 일은 담당자 몫입니다.", "check"),
             ("결정하고 책임집니다", "어느 안을 내보낼지 정하고 그 아래 이름을 적습니다.", "stamp")]
    nodes = "".join(f'<div class="axstep">{icon(ic)}<b>담당자 {i}</b><h4>{t}</h4><p>{d}</p></div>'
                    for i, (t, d, ic) in enumerate(roles, 1))
    inner = ('<div class="vcen">'
             f'<div class="axlad five">{nodes}</div>'
             + band('<strong>다섯 가지 모두 AI가 대신할 수 없는 일입니다.</strong> '
                    '결과를 읽고 무엇을 쓸지 정하는 일은 여전히 이 방 안의 사람이 합니다.')
             + '</div>')
    return wide(n, P5, "마무리", 'AX 뒤에도 담당자가 하는 <span class="gt">다섯 가지</span>',
                "AX 뒤에도 담당자가 하는 다섯 가지",
                "오늘 본 화면들에서 AI가 맡은 일이 늘수록 또렷해진 것은 담당자가 하는 다섯 가지입니다.",
                inner, "")


# ── 38 마무리 ────────────────────────────────────────────────────────
def a24(n):
    HEADERS[n] = "열매나눔재단은 어떤 조직으로 일하고 싶은지"
    aur = '<i class="aur a1"></i><i class="aur a3"></i>'
    body = (f'{aur}<div class="fg">'
            + kicker(P5, "마무리")
            + '<h2 class="big">열매나눔재단은<br><span class="gt">어떤 조직</span>으로 일하고 싶을까요?</h2>'
              '<p class="impband"><strong>AX의 목표는 한 사람이 AI를 잘 쓰게 만드는 것이 아닙니다.</strong> '
              '한 사람에게 맞춰진 결과를 재단이 이해하고, 검토하고, 다시 쓸 수 있게 만드는 것입니다.</p>'
              '</div>')
    return ax(n, "ax-imp", body, "")


def _compare_page(title, body, extra_css="", extra_js=""):
    """비교 화면 한 쪽. 덱과 같은 CSS 위에 비교용 층만 더 얹는다."""
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">
<style>{CSS}{EXTRA_CSS}{DEEP_CSS}{ADD_CSS}{V2_CSS}{VARIANT_CSS}{LAYOUT_CSS}{SKETCH_CSS}{COVER_CSS}{COMPARE_CSS}{extra_css}</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="ig" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF7A1A"/><stop offset=".5" stop-color="#A855F7"/><stop offset="1" stop-color="#3B82F6"/></linearGradient></defs></svg>
{body}
{compare_controls()}
{V2_JS}
{COMPARE_JS}
{extra_js}
</body>
</html>"""


def write_compare(slides):
    """4장과 40장 후보를 나란히 놓은 비교 화면. 덱 파일은 건드리지 않는다."""
    html = _compare_page("4장과 40장 후보 비교", compare_body(slides))
    out = "후보비교_04_40.html"
    open(out, "w", encoding="utf-8").write(html)
    print(f"✓ {out} 생성 ({len(html)//1024}KB)")


def write_compare_all(slides):
    """52장 전부의 후보를 나란히 놓은 비교 화면. 고르고 기록하는 층이 함께 들어간다."""
    html = _compare_page("52장 시각 안 후보", compare_all_body(slides),
                         extra_css=PICK_CSS, extra_js=PICK_JS)
    out = "후보비교_전장.html"
    open(out, "w", encoding="utf-8").write(html)
    print(f"✓ {out} 생성 ({len(html)//1024}KB)")


PRINT_SIM_DONE = (
    '<strong data-sim-output>재단의 4월 후원 건수는 이틀 만에 69건으로 평소보다 크게 늘어난 변화입니다.</strong>')
PRINT_SIM_CANDS = ('<div data-sim-cands>'
                   '<span class="simcand pick">늘어난 변화입니다. <small>58%</small></span>'
                   '<span class="simcand">증가한 사례입니다. <small>16%</small></span>'
                   '<span class="simcand">커진 수치입니다. <small>9%</small></span></div>')


def print_freeze(html):
    """인쇄용 변환. 시연물을 내용이 가장 많은 장면에 멈춘 채 박아 넣는다.

    각 시연물이 검수용으로 가진 멈춤 매개변수를 그대로 쓴다.
    웹 구조 지도는 두 사이트를 잇는 장면(stage=7), 캠페인 레이스는 마지막 직전(at=0.97),
    지휘실은 세 기기와 대화가 모두 찬 오후(at=0.88)다. 문장 생성 시뮬레이션은 좋아진 추론의 완성 문장을 박는다.
    """
    subs = [
        ('data-src="웹구조그래프.html" loading="lazy" ', 'src="웹구조그래프.html?stage=7" '),
        ('data-src="캠페인레이스.html" loading="lazy" ', 'src="캠페인레이스.html?at=0.97" '),
        ('data-src="지휘실.html" loading="lazy" ', 'src="지휘실.html?at=0.88" '),
        ('loading="lazy" ', ''),           # 나머지도 인쇄에서는 바로 불러온다
        ('embbox waiting', 'embbox'),      # 대기 안내를 걷는다
        # 문장 생성 시뮬레이션. data-llm-sim 을 지워 대본 스크립트가 초기화하지 않게 한다
        ('<div class="llmsim" data-llm-sim>', '<div class="llmsim">'),
        ('data-sim-mode-label>기본 모델</span>', 'data-sim-mode-label>좋아진 추론</span>'),
        ('<strong data-sim-output></strong>', PRINT_SIM_DONE),
        ('<div data-sim-cands></div>', PRINT_SIM_CANDS),
        ('data-sim-step-label>질문 입력 중</b>', 'data-sim-step-label>문장 완성</b>'),
        ('<i data-sim-progress></i>', '<i data-sim-progress style="background:#FF6A76"></i>'),
    ]
    for a, b in subs:
        html = html.replace(a, b)
    import re as _re
    html = _re.sub(r'<button class="(?:embplay|simplay)".*?</button>', '', html, flags=_re.S)
    return html


def build():
    HEADERS.clear()
    deep = make_deep(wide, split)
    add = make_add(wide, split)
    d = {k: v[0] for k, v in deep.items() if len(v) == 1}
    d_dir = dict(zip(["d_unit", "d_share", "d_check", "d_speed", "d_rules", "d_plan"], deep["direction"]))
    s1, s2, s3 = deep["trait"]
    # (열쇠, 장 함수). 열쇠는 다른 장에서 REF로 번호를 가리킬 때 쓴다.
    order = [("a1", a1), ("hype", a_hype), ("flood", a_flood), ("s1", s1), ("a3", a3), ("s2", s2),
             ("stages", add["stages"]), ("stuck", add["stuck"]), ("jcurve", add["jcurve"]),
             ("a4", a4), ("a5", a5), ("a6", a6), ("a8", a8), ("a9", a9), ("a11", a11),
             ("a12", a12), ("rag", a_rag), ("a13", a13), ("a14", a14), ("a15", a15), ("a16", a16), ("a18", a18),
             ("average", add["average"]),
             ("share_q", add["share_q"]),
             ("toon_tech", add["toon_tech"]), ("toon_cog", add["toon_cog"]), ("toon_intent", add["toon_intent"]),
             ("d_trust", d["trust"]),
             ("review_other", add["review_other"]), ("a20", a20), ("d_reuse", d["reuse"]), ("grill", add["grill"]),
             ("shared_memory", add["shared_memory"]),
             ("orchestra", a_orc),
             ("d_unit", d_dir["d_unit"]), ("buy_vs_connect", add["buy_vs_connect"]), ("d_share", d_dir["d_share"]),
             ("less", add["less"]), ("d_check", d_dir["d_check"]),
             ("d_speed", d_dir["d_speed"]), ("d_rules", d_dir["d_rules"]),
             ("simple_rules", add["simple_rules"]), ("translator", add["translator"]), ("d_plan", d_dir["d_plan"]),
             ("relief", add["relief"]), ("leaders", add["leaders"]),
             ("a22", a22), ("hours", add["hours"]),
             ("gellmann", add["gellmann"]), ("a23", a23), ("hard_calls", add["hard_calls"]),
             ("boss_skills", add["boss_skills"]), ("a24", a24)]
    assert len(order) == TOTAL, f"장 수 {len(order)}가 TOTAL {TOTAL}과 다르다"
    REF.clear(); REF.update({k: i for i, (k, _) in enumerate(order, 1)})
    slides = [fn(i) for i, (_, fn) in enumerate(order, 1)]
    slides = sync(slides, ROOT / "본문_AX60.md", export="--export" in sys.argv)
    # 문장 검사와 승인은 본문 기준으로만 한다. v2의 캡션은 판을 바꾸는 층이라
    # 승인 파일을 흔들지 않도록 검사를 마친 뒤에 끼운다.
    lint(slides)
    prose_gate(slides, "AX60", "--approve" in sys.argv)
    if "--all" in sys.argv:
        write_compare_all(slides)
        return
    cmp_mode = "--compare" in sys.argv
    if cmp_mode:
        write_compare(slides)
        return
    prn = "--print" in sys.argv
    v2 = "--v2" in sys.argv or prn   # 인쇄본은 발표에 쓰는 v2 판을 기준으로 찍는다
    if v2:
        slides = v2_patch(slides, REF)
        lint(slides)
    slides[-1] = slides[-1].replace('<div class="vp">', '<div class="vp last">', 1)
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>열매나눔재단 / 일하는 방식을 다시 설계하기</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">
<style>{CSS}{EXTRA_CSS}{DEEP_CSS}{ADD_CSS}{V2_CSS if v2 else ""}</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="ig" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF7A1A"/><stop offset=".5" stop-color="#A855F7"/><stop offset="1" stop-color="#3B82F6"/></linearGradient></defs></svg>
{"".join(slides)}
<script>
const fit=()=>document.documentElement.style.setProperty('--s',Math.min(innerWidth/1920,innerHeight/1080));
addEventListener('resize',fit);fit();
{PLAY_JS}
</script>
{V2_JS if v2 else ""}
{TOOLBAR_HTML}
</body>
</html>"""
    out = "쇼케이스_AX60_v2.html" if v2 else "쇼케이스_AX60.html"
    if prn:
        html = print_freeze(html)
        out = "쇼케이스_AX60_인쇄.html"
    open(out, "w", encoding="utf-8").write(html)
    print(f"✓ {out} 생성 ({len(html)//1024}KB, {len(slides)}장)")


if __name__ == "__main__":
    build()
