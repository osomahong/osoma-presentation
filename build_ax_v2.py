"""쇼케이스_AX60_v2 전용 레이아웃 층.

원본 덱(쇼케이스_AX60.html)의 글과 구성은 그대로 두고, 장마다 겹치거나 남아 도는 자리만
다시 잡는다. 여기 있는 것은 두 가지다.

- V2_CSS: 원본 CSS 뒤에 덧붙는 규칙. 원본 파일에는 들어가지 않는다.
- v2_patch(slides, REF): 글줄을 건드리지 않고 클래스나 감싸개만 바꾸는 손질.

빌드: python3 build_ax.py --v2
출력: 쇼케이스_AX60_v2.html
"""
import re
from html import escape as html_escape

V2_CSS = """
/* ══ v2 레이아웃 ══════════════════════════════════════════════════
   원칙 세 가지.
   1. 본문 블록이 제목 아래 남는 높이를 실제로 채운다. 가운데 띠처럼 뜨지 않게 한다.
   2. 결론 띠는 늘 화면 아래쪽 같은 자리에 붙는다.
   3. 칸을 나눈 자리에서는 글이 옆 칸을 침범하지 않는다.
   ═══════════════════════════════════════════════════════════════ */

/* ── 1. 본문 블록이 높이를 채운다 ── */
.ax .vcen{gap:34px}
.ax .vcen > .vs,
.ax .vcen > .ba,
.ax .vcen > .hfacts,
.ax .vcen > .tools,
.ax .vcen > .toc{flex:1 1 auto;min-height:0}

/* ── 2. 카드: 아이콘과 글을 한 덩이로 묶어 칸 가운데에 둔다 ── */
.ax .axstep{display:flex;flex-direction:column;justify-content:center;padding:52px 38px}
.ax .axstep .ci{width:52px;height:52px;margin-bottom:26px}
.ax .axstep h4{font-size:29px;margin:14px 0 12px}
.ax .axstep p{font-size:21px;line-height:1.6}
.ax .axlad.five .axstep{padding:44px 30px}
.ax .axlad.five .axstep .ci{width:44px;height:44px;margin-bottom:20px}
.ax .axlad.five .axstep h4{font-size:25px;margin:10px 0 9px}
.ax .axlad.five .axstep p{font-size:19px}

/* 카드 라벨 자리에 긴 문장이 들어간 장은 제목을 먼저 보이고 문장을 아래에 붙인다 */
.ax .axstep.wordy{justify-content:flex-start}
.ax .axstep.wordy .ci{margin-bottom:18px}
.ax .axstep.wordy h4{order:1;margin:0 0 8px}
.ax .axstep.wordy p{order:2}
.ax .axstep.wordy b{order:3;margin-top:auto;padding-top:18px;border-top:1.5px solid rgba(120,110,150,.16);
  font-family:var(--f);font-size:19px;font-weight:500;line-height:1.5;letter-spacing:0;
  background:none;-webkit-text-fill-color:currentColor;color:var(--dim)}
.ax .axstep.wordy b strong{font-weight:800;color:var(--ink)}

/* ── 3. 가로 단계: 칸을 균등하게 나누고 글을 칸 안에 가둔다 ── */
.ax .steps{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);align-items:start;align-content:center}
.ax .stepn{min-width:0;padding:0 14px}
.ax .stepn h4,.ax .stepn p{overflow-wrap:break-word}
.ax .steps:has(> .stepn:nth-child(5)) .stepn{padding:0 10px}
.ax .steps:has(> .stepn:nth-child(5)) .stepn h4{font-size:22px}
.ax .steps:has(> .stepn:nth-child(5)) .stepn p{font-size:17.5px}
.ax .steps:has(> .stepn:nth-child(6)) .stepn h4{font-size:21px;margin-top:16px}
.ax .steps:has(> .stepn:nth-child(6)) .stepn p{font-size:17px;line-height:1.5}

/* ── 4. 종이 두 장 비교: 목록을 종이 가운데에 두고 넘치지 않게 ── */
.ax .balist{align-items:stretch}
.ax .balist .paper{justify-content:center;min-height:0;padding:30px 40px}
.ax .balist .paper .plist{gap:9px}
.ax .balist .paper .prole{margin-top:14px;padding-top:12px}
/* 제목이 두 줄인 장은 아래 내용이 쓸 높이가 줄어드니 목록을 한 단계 좁힌다 */
.ax.tallhead .balist .paper{padding:26px 38px}
.ax.tallhead .balist .paper .plist{gap:7px}
.ax.tallhead .balist .paper .plist li{font-size:21px;line-height:1.45}
.ax .ba .paper{min-height:0}

/* ── 5. 단계가 넷 이하면 동그라미와 글자를 키운다 ── */
.ax .steps:not(:has(> .stepn:nth-child(5))) .stepn b{width:76px;height:76px;font-size:27px}
.ax .steps:not(:has(> .stepn:nth-child(5))) .stepn::before{top:38px;left:calc(50% + 50px);right:calc(-50% + 50px)}
.ax .steps:not(:has(> .stepn:nth-child(5))) .stepn h4{font-size:26px;margin-top:22px}
.ax .steps:not(:has(> .stepn:nth-child(5))) .stepn p{font-size:19.5px}

/* 단계 줄만 있는 장은 줄 뒤에 옅은 판을 깔아 화면을 채운다 */
.ax .vcen > .steps{background:linear-gradient(150deg,#FFF7EF,#FBF2F8 45%,#F4F2FD 75%,#EFF5FE);
  border:1.5px solid #EDEAF2;border-radius:28px;padding:62px 44px}
.ax .vcen > .steps .stepn b{box-shadow:0 10px 26px rgba(200,90,120,.22)}

/* 비포 애프터 두 줄에서는 위아래 단계 크기를 같게 둔다 */
.ax .baflow .steps .stepn b{width:62px;height:62px;font-size:23px}
.ax .baflow .steps .stepn::before{top:31px;left:calc(50% + 42px);right:calc(-50% + 42px)}
.ax .baflow .steps .stepn h4{font-size:22px;margin-top:16px}
.ax .baflow .steps .stepn p{font-size:17.5px;line-height:1.5}

/* ── 6. 사실 카드도 칸을 채우고 글을 가운데에 둔다 ── */
.ax .hfacts{gap:22px}
.ax .hf{display:flex;flex-direction:column;justify-content:center;padding:30px 34px}
.ax .hfacts.four{align-content:stretch;gap:22px}
.ax .hfacts.four .hf{padding:26px 30px}

/* 목록만 있는 장은 줄을 화면 높이에 고르게 편다 */
.ax .vcen > .points{flex:1;justify-content:space-evenly;margin-top:0}

/* 세 칸 계획표는 글을 칸 가운데에 둔다 */
.ax .toc .tocol{display:flex;flex-direction:column;justify-content:center}

/* 오늘 다루는 칸 표시는 카드 안쪽에 붙인다 */
.ax .axstep.today::after{top:20px;right:20px}

/* ── 7. 시간 막대는 화면 폭에 맞춰 크게 ── */
.ax .hours{gap:38px}
.ax .hbar{height:120px}
.ax .hbar span{font-size:24px}
.ax .hrow .hl{font-size:25px}

/* ── 8. 마지막 장은 질문 하나만 크게 ── */
.ax-imp .fg{gap:52px}
.ax-imp h2.big{font-size:96px;max-width:1500px}
.ax-imp .impband{font-size:27px;padding:34px 46px;max-width:1280px;line-height:1.72}

/* ══ 그림을 앞세운 장 ══════════════════════════════════════════════
   장마다 그 장에서만 쓰는 그림을 화면 가운데에 두고, 글은 옆에서 거든다.
   그림이 아직 없는 동안에는 넣을 곳을 비워 두고 캡션과 프롬프트를 함께 둔다.
   ═══════════════════════════════════════════════════════════════ */

/* 그림 넣을 곳 */
.imgslot{display:flex;flex-direction:column;min-height:0}
.imgbox{flex:1;min-height:0;position:relative;border-radius:26px;border:2px dashed #D9DDE8;
  background:linear-gradient(150deg,#FFF7EF,#FBF2F8 45%,#F4F2FD 75%,#EFF5FE);
  display:grid;place-items:center;overflow:hidden}
.imgbox::before{content:"";position:absolute;inset:0;
  background-image:repeating-linear-gradient(45deg,rgba(120,110,150,.055) 0 12px,transparent 12px 24px)}
.imgbox .imark{position:relative;text-align:center;color:var(--faint);
  font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.2em}
.imgbox .imark svg{display:block;margin:0 auto 14px;width:56px;height:56px;
  stroke:#C6CBDA;fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.imgcap{margin-top:18px;display:flex;gap:20px;align-items:flex-start}
.imgcap p{flex:1;font-size:18.5px;line-height:1.55;color:var(--dim)}
.imgcap p b{display:block;font-family:var(--fm);font-size:14px;font-weight:700;
  letter-spacing:.18em;color:var(--faint);margin-bottom:7px}
.pbtn{flex:none;display:inline-flex;align-items:center;gap:9px;padding:11px 20px;border:none;border-radius:999px;
  background:var(--grad);color:#fff;font-family:var(--f);font-size:16px;font-weight:700;cursor:pointer;
  box-shadow:0 8px 22px rgba(168,85,247,.26);transition:transform .12s}
.pbtn:active{transform:translateY(1px)}
.pbtn svg{width:16px;height:16px;stroke:#fff;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.pbtn.done{background:#2FB37A;box-shadow:none}

/* 틀 1. 세로 그림 한 장과 점점 세지는 세 마디 */
.figsplit{display:grid;grid-template-columns:.82fr 1fr;gap:60px;flex:1;min-height:0;margin-top:26px}
.stack{display:flex;flex-direction:column;justify-content:center;gap:16px}
.stk{position:relative;border-radius:20px;padding:24px 32px;background:#fff;
  border:1.5px solid var(--line);box-shadow:0 10px 30px rgba(40,50,80,.06)}
.stk:nth-child(2){margin-left:38px}
.stk:nth-child(3){margin-left:76px;border:2px solid transparent;
  background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box;box-shadow:0 16px 40px rgba(200,90,120,.16)}
.stk .slab{font-family:var(--fm);font-size:13.5px;font-weight:700;letter-spacing:.16em;color:var(--faint);margin-bottom:6px}
.stk h4{font-size:25px;font-weight:800;line-height:1.35;margin-bottom:8px}
.stk p{font-size:19px;line-height:1.55;color:var(--dim)}

/* 틀 2. 가로로 긴 그림 아래로 내려앉는 네 마디 */
.figwide{display:flex;flex-direction:column;flex:1;min-height:0;margin-top:22px;gap:24px}
.figwide .imgslot{flex:1;min-height:0}
.fall{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;align-items:start;flex:none}
.fal{position:relative;border-radius:18px;padding:18px 24px;background:#fff;border:1.5px solid var(--line)}
.fal:nth-child(2){margin-top:12px}
.fal:nth-child(3){margin-top:24px}
.fal:nth-child(4){margin-top:36px;border:2px solid transparent;
  background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}
.fal::after{content:"";position:absolute;right:-22px;top:30px;width:22px;height:2px;background:#E7DCEC}
.fal:last-child::after{display:none}
.fal .fn{font-family:var(--fm);font-size:14.5px;font-weight:700;letter-spacing:.12em;color:var(--faint)}
.fal h4{font-size:22px;font-weight:800;margin:7px 0 6px}
.fal p{font-size:17.5px;line-height:1.5;color:var(--dim)}
.fal:nth-child(4) h4{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.figsplit + .axband,.figwide + .axband{margin-top:20px}
.figsplit .imgbox{flex:none;aspect-ratio:2/1;height:auto;width:100%;margin:auto 0}
.figwide .imgbox{aspect-ratio:9/2;height:100%;width:auto;max-width:100%;margin:0 auto}
.imgslot.pinned{position:relative}
.imgcap.pin{position:absolute;left:26px;right:26px;bottom:24px;margin:0;align-items:center;
  background:rgba(255,255,255,.93);border-radius:18px;padding:16px 22px;box-shadow:0 10px 28px rgba(40,50,80,.12)}

/* ── 9. 화면 비율에 맞춘 본문 크기 ──
   제목을 줄이는 대신 줄바꿈과 칸 폭을 먼저 지킨다. 긴 제목은 tallhead가 처리한다. */
.ax h2.head{font-size:48px}
.ax .lead{font-size:18px}
.ax .kicker{font-size:16px}
.ax .pt h4,.ax .points .pt h4{font-size:20px}
.ax .pt p,.ax .points .pt p{font-size:15px}
.ax .goals .pt h4{font-size:23px}
.ax .goals .pt p{font-size:16px}
.ax .axband{font-size:17px}
.ax.ax-cover h1{font-size:96px}
.ax.ax-cover .sub{font-size:22px}
.ax.ax-imp h2.big{font-size:78px}
.ax.ax-imp .impband{font-size:20px}
.ax .axstep h4{font-size:20px}
.ax .axstep p{font-size:15px}
.ax .axlad.five .axstep h4{font-size:20px}
.ax .axlad.five .axstep p{font-size:15px}
.ax .steps:has(> .stepn:nth-child(5)) .stepn h4{font-size:18px}
.ax .steps:has(> .stepn:nth-child(5)) .stepn p{font-size:14px}
.ax .steps:has(> .stepn:nth-child(6)) .stepn h4{font-size:17px}
.ax .steps:has(> .stepn:nth-child(6)) .stepn p{font-size:14px}
.ax .steps:not(:has(> .stepn:nth-child(5))) .stepn h4{font-size:22px}
.ax .steps:not(:has(> .stepn:nth-child(5))) .stepn p{font-size:15px}
.ax .baflow .steps .stepn h4{font-size:18px}
.ax .baflow .steps .stepn p{font-size:14px}
.ax .hbar span{font-size:20px}
.ax .hrow .hl{font-size:21px}
.ax .tool h4{font-size:19px}
.ax .tool p{font-size:15px}
.ax .vcard h4{font-size:21px}
.ax .vcard p{font-size:16px}
.ax .aq h4{font-size:18px}
.ax .aq p{font-size:15px}
.ax .paper .plist li{font-size:18px}
.ax .paper .ptxt{font-size:20px}
.ax .qacard .qq{font-size:20px}
.ax .qacard .qa{font-size:17px}
.ax .figrow span{font-size:17px}
.ax .embnote{font-size:17px}
/* 갈무리 장의 머리말 축소는 원본 덱에서만 쓴다. v2는 이미 그만큼 작다 */
.ax:has(.hypewrap) h2.head{font-size:48px}
.ax:has(.hypewrap) .lead{font-size:18px}
.ax .stk h4{font-size:21px}
.ax .stk p{font-size:16px}
.ax .fal h4{font-size:18px}
.ax .fal p{font-size:15px}
.ax .hf b{font-size:23px}
.ax .hf p{font-size:16px}
.ax .hstep h4{font-size:21px}
.ax .hstep p{font-size:16px}
"""


# ── 그림 프롬프트 ────────────────────────────────────────────────
# 덱의 톤과 매너를 프롬프트 끝에 늘 같은 문장으로 붙인다. 그래야 장마다 뽑은 그림이
# 한 벌로 보인다. 흰 바탕, 얇은 둥근 선, 네 가지 브랜드 색, 글자 없음이 뼈대다.
STYLE = (
    "Style: clean editorial vector illustration, flat and minimal, thin rounded strokes about 2px, "
    "drawn on a pure white background with generous negative space. "
    "Palette strictly limited to warm orange #FF7A1A, coral pink #FF4D6D, violet #A855F7 and blue #3B82F6, "
    "used as soft linear gradients, with ink #1F2430 for line work and pale grey #E9EBF1 for secondary lines. "
    "Very soft, wide drop shadows. Calm and professional tone suited to a non-profit foundation, "
    "not playful, not corporate stock photography, no 3D render, no gloss. "
    "Human figures are simple and abstract with no facial features. "
    "Absolutely no text, no letters, no numbers, no logos, no watermarks, no UI labels. "
    "Balanced composition with clear empty margins so that captions can sit beside the artwork."
)

PROMPTS = {
    "a4": (
        "A quiet study of a question coming back stronger than it left. "
        "On the left, a small abstract figure seen from behind sits at a desk and sends one thin grey arrow "
        "toward a large rounded screen panel on the right. "
        "From the screen, the same arrow returns three times along a curving path back to the figure, "
        "each return thicker and more saturated than the one before, so the three returning strokes "
        "form a closing loop between the person and the screen. "
        "The returning arrows carry a warm orange to coral pink to violet gradient; the outgoing arrow stays thin and grey. "
        "The loop should read as amplification and agreement building on itself, not as a friendly conversation. "
        "Horizontal composition, aspect ratio 2:1, subject centred with wide empty margins. " + STYLE
    ),
    "a40": (
        "An ultra wide panoramic scene that reads from left to right in one continuous movement. "
        "Far left: a single sheet of paper glides forward, untouched and slightly tilted, carrying a warm orange gradient. "
        "Centre: the sheet tips the first of a row of upright rounded panels, and the panels fall in sequence like dominoes, "
        "losing colour as they go until they are pale grey. "
        "Far right: two small abstract human figures stand still, arms down, in front of a large dark rounded screen that is switched off. "
        "A single thin coral pink line traces the whole path of the fall from the sheet to the dark screen. "
        "The scene should read as one unchecked document spreading into a stopped organisation. "
        "Extremely wide cinematic banner, aspect ratio 9:2 (about 4.5:1), with the action along the lower two thirds "
        "and wide empty sky above. " + STYLE
    ),
}

CAPS = {
    "a4": ("넣을 그림", "질문 하나가 되돌아올 때마다 굵어지는 고리입니다. 사람과 화면 사이에서 확신이 커지는 모습을 보입니다."),
    "a40": ("넣을 그림", "검토 없이 넘어간 종이 한 장이 옆으로 번져 화면이 꺼지는 장면입니다. 왼쪽에서 오른쪽으로 읽습니다."),
}


# ── 실제 화면을 넣는 자리 ─────────────────────────────────────────
# 그림을 뽑는 대신 쓰던 화면을 그대로 갈무리해 넣는 안이다. 프롬프트 자리에는
# 무엇을 어떻게 갈무리할지 적어 두고, 같은 단추로 복사한다.
SHOT_TAIL = (
    "갈무리할 때 지킬 것. 계정 이름과 사진, 후원자 이름, 전화번호, 이메일은 가립니다. "
    "화면 배율을 키워 글자가 작지 않게 하고, 대화는 두 번까지만 보이게 자릅니다. "
    "가로로 긴 직사각형(약 22:9)으로 잘라 두 화면의 크기를 같게 맞춥니다."
)

SLOTS = {
    "a4": dict(tag=CAPS["a4"][0], desc=CAPS["a4"][1], prompt=PROMPTS["a4"],
               btn="프롬프트 복사", mark="IMAGE"),
    "a40": dict(tag=CAPS["a40"][0], desc=CAPS["a40"][1], prompt=PROMPTS["a40"],
                btn="프롬프트 복사", mark="IMAGE"),
    "s4sure": dict(
        tag="넣을 화면 1",
        desc="확신을 담아 물었더니 그대로 거들어 준 대화입니다.",
        btn="갈무리 안내 복사",
        mark="SCREEN",
        prompt=("실제로 쓰는 AI 대화 화면을 그대로 갈무리합니다. "
                "재단 업무에서 최근에 내린 판단 하나를 고릅니다. "
                "그 판단을 이미 정답처럼 담아 묻습니다. 예를 들면 이렇게 묻습니다. "
                "\"이번 연말 캠페인은 인스타그램에 집중하는 쪽이 맞겠지?\" "
                "AI가 그 전제를 받아들이고 근거를 보태 준 답이 돌아오면 그 화면을 씁니다. "
                + SHOT_TAIL)),
    "s4doubt": dict(
        tag="넣을 화면 2",
        desc="같은 판단을 의심하게 물었더니 돌아온 대화입니다.",
        btn="갈무리 안내 복사",
        mark="SCREEN",
        prompt=("앞 화면과 같은 판단을 같은 도구에 다시 묻습니다. 이번에는 결론을 빼고 반대로 묻습니다. "
                "예를 들면 이렇게 묻습니다. "
                "\"이번 연말 캠페인을 인스타그램에 집중하면 실패할 이유를 세 가지 찾아 줘.\" "
                "AI가 앞 화면과 다른 방향을 말한 답이 돌아오면 그 화면을 씁니다. "
                "두 화면은 같은 날 같은 도구에서 뽑아 조건을 맞춥니다. "
                + SHOT_TAIL)),
}

_IMARK = ('<div class="imark"><svg viewBox="0 0 24 24" aria-hidden="true">'
          '<rect x="3" y="5" width="18" height="14" rx="2.5"/>'
          '<circle cx="8.5" cy="10" r="1.6"/><path d="M4 17l5-5 4 4 3-2.5 4 3.5"/></svg>IMAGE</div>')

_COPY = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2"/>'
         '<path d="M5 15V6a2 2 0 0 1 2-2h9"/></svg><span>프롬프트 복사</span>')


def _slot(key, pinned=False):
    """그림이나 화면을 넣을 곳 하나. 캡션과 복사 단추가 함께 붙는다."""
    sl = SLOTS[key]
    prompt = html_escape(sl["prompt"])
    btn = _COPY.replace("프롬프트 복사", sl["btn"])
    mark = _IMARK.replace(">IMAGE<", f'>{sl["mark"]}<')
    cap = (f'<div class="imgcap{" pin" if pinned else ""}"><p><b>{sl["tag"]}</b>{sl["desc"]}</p>'
           f'<button class="pbtn" type="button" data-prompt="{prompt}">{btn}</button></div>')
    box = f'<div class="imgbox">{mark}{cap if pinned else ""}</div>'
    return (f'<div class="imgslot{" pinned" if pinned else ""}">{box}{"" if pinned else cap}</div>')


def _grab(html, pat, flags=re.S):
    m = re.search(pat, html, flags)
    return m.group(0) if m else ""


def _cells(html, cls):
    """axstep 또는 stepn 안의 라벨, 제목, 설명을 순서대로 뽑는다."""
    out = []
    for blk in re.findall(rf'<div class="{cls}[^"]*">(.*?)</div>', html, re.S):
        lab = re.search(r"<b>(.*?)</b>", blk, re.S)
        h4 = re.search(r"<h4>(.*?)</h4>", blk, re.S)
        pp = re.search(r"<p>(.*?)</p>", blk, re.S)
        out.append((lab.group(1) if lab else "", h4.group(1) if h4 else "", pp.group(1) if pp else ""))
    return out


def _reframe(html, body):
    """머리말과 제목과 리드는 그대로 두고, 그 아래를 새 판으로 갈아 끼운다."""
    lead = re.search(r'<p class="lead">.*?</p>', html, re.S)
    brand = html.find('<div class="brandbar">')
    if not lead or brand < 0:
        return html
    return html[:lead.end()] + body + "</div>" + html[brand:]


def _fig_stack(html, key):
    """틀 1. 세로 그림 한 장과 점점 세지는 세 마디."""
    cells = _cells(html, "axstep")
    if len(cells) != 3:
        return html
    stk = "".join(f'<div class="stk"><div class="slab">{lab}</div><h4>{h4}</h4><p>{pp}</p></div>'
                  for lab, h4, pp in cells)
    body = (f'<div class="figsplit">{_slot(key)}<div class="stack">{stk}</div></div>'
            f'{_grab(html, r"<div class=\"axband\"[^>]*>.*?</div>")}')
    return _reframe(html, body)


def _fig_fall(html, key):
    """틀 2. 가로로 긴 그림과 아래로 내려앉는 네 마디."""
    cells = _cells(html, "stepn")
    if len(cells) != 4:
        return html
    fal = "".join(f'<div class="fal"><div class="fn">{lab}</div><h4>{h4}</h4><p>{pp}</p></div>'
                  for lab, h4, pp in cells)
    body = (f'<div class="figwide">{_slot(key, pinned=True)}<div class="fall">{fal}</div></div>'
            f'{_grab(html, r"<div class=\"axband\"[^>]*>.*?</div>")}')
    return _reframe(html, body)


# 샘플로 만든 장. 열쇠는 장 번호다.
# So What 장을 후반부로 옮기고 장이 드나들면서 사고 이후의 추락 장은 41장이 된다.
SAMPLES = {42: ("a40", _fig_fall)}

V2_JS = """
<script>
/* 그림 프롬프트 복사 */
document.addEventListener('click',function(e){
  var b=e.target.closest('.pbtn'); if(!b) return;
  var t=b.getAttribute('data-prompt')||'', s=b.querySelector('span'), old=s.textContent;
  var done=function(){b.classList.add('done');s.textContent='복사했습니다';
    setTimeout(function(){b.classList.remove('done');s.textContent=old},1600)};
  var fallback=function(){var a=document.createElement('textarea');a.value=t;a.style.position='fixed';
    a.style.top='0';a.style.opacity=0;document.body.appendChild(a);a.focus();a.select();
    try{document.execCommand('copy')}catch(err){}a.remove();done()};
  if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(t).then(done,fallback)}
  else{fallback()}
});

/* LLM 답변 생성 원리 시뮬레이션 */
(function(){
  var root=document.querySelector('[data-llm-sim]'); if(!root)return;
  var data={
    base:{
      steps:[
        {pick:'재단의',cands:[['재단의',72],['지난달',12],['이번',9]]},
        {pick:'4월',cands:[['4월',78],['후원',15],['해당',8]]},
        {pick:'후원',cands:[['후원',68],['모금',18],['신청',8]]},
        {pick:'건수는',cands:[['건수는',62],['금액은',19],['참여자는',9]]},
        {pick:'전월보다',cands:[['전월보다',58],['이틀 만에',21],['평소보다',11]]},
        {pick:'늘었습니다.',cands:[['늘었습니다.',61],['증가했습니다.',23],['의미 있습니다.',8]]}
      ]
    },
    strong:{
      steps:[
        {pick:'재단의',cands:[['재단의',82],['지난달',9],['이번',6]]},
        {pick:'4월',cands:[['4월',86],['후원',9],['해당',4]]},
        {pick:'후원',cands:[['후원',81],['모금',12],['신청',4]]},
        {pick:'건수는',cands:[['건수는',84],['금액은',10],['참여자는',4]]},
        {pick:'이틀 만에',cands:[['이틀 만에',54],['전월보다',20],['평소보다',15]]},
        {pick:'69건으로',cands:[['69건으로',57],['크게',18],['증가해',13]]},
        {pick:'평소보다',cands:[['평소보다',61],['지난달보다',18],['평균적으로',8]]},
        {pick:'크게',cands:[['크게',55],['조금',12],['빠르게',9]]},
        {pick:'늘어난 변화입니다.',cands:[['늘어난 변화입니다.',58],['증가한 사례입니다.',16],['커진 수치입니다.',9]]}
      ]
    }
  };
  var mode='base', step=0, candidateIndex=0, currentText='';
  var questionText='4월 후원 건수를 어떻게 해석해야 할까요?';
  var question=root.querySelector('[data-sim-question]');
  var output=root.querySelector('[data-sim-output]');
  var cands=root.querySelector('[data-sim-cands]');
  var progress=root.querySelector('[data-sim-progress]');
  var modeLabel=root.querySelector('[data-sim-mode-label]');
  var stepLabel=root.querySelector('[data-sim-step-label]');
  var live=root.querySelector('[data-sim-live]');
  var timer=null, typingTimer=null, scanTimer=null;
  function renderCandidates(phase){
    var d=data[mode], current=d.steps[step];
    if(phase==='question'){
      cands.innerHTML='';
      return;
    }
    if(!current){
      cands.innerHTML='<span class="simcand pick">문장 완성</span>';
      return;
    }
    cands.innerHTML=current.cands.map(function(c,i){
      var cls='simcand'+((phase==='pick'||phase==='type')&&c[0]===current.pick?' pick':'')+(phase==='scan'&&i===candidateIndex?' focus':'');
      return '<span class="'+cls+'">'+c[0]+' <small>'+c[1]+'%</small></span>';
    }).join('');
  }
  function render(phase){
    var d=data[mode], current=d.steps[step];
    output.textContent=currentText;
    renderCandidates(phase||'scan');
    modeLabel.textContent=mode==='base'?'기본 모델':'좋아진 추론';
    var pct=Math.round(step/d.steps.length*100);
    progress.style.background='linear-gradient(90deg,#FF6A76 0 '+pct+'%,#343D53 '+pct+'% 100%)';
    if(!current){
      stepLabel.textContent='문장 완성';
      live.classList.remove('is-typing');
    }else if(phase==='question'){
      stepLabel.textContent='질문 읽는 중';
      live.classList.remove('is-typing');
    }else if(phase==='type'){
      stepLabel.textContent='선택한 토큰을 연결하는 중';
      live.classList.add('is-typing');
    }else if(phase==='pick'){
      stepLabel.textContent='다음 토큰 선택';
      live.classList.remove('is-typing');
    }else{
      stepLabel.textContent='후보 비교 중';
      live.classList.remove('is-typing');
    }
  }
  function typeToken(token, done){
    var addition=(currentText?' ':'')+token, i=0;
    render('type');
    function add(){
      if(i<addition.length){
        currentText+=addition.charAt(i++);
        output.textContent=currentText;
        typingTimer=window.setTimeout(add,38);
      }else{
        typingTimer=null; done();
      }
    }
    add();
  }
  function playStep(){
    var d=data[mode], current=d.steps[step];
    if(!current){
      render();
      timer=window.setTimeout(function(){
        mode=mode==='base'?'strong':'base'; step=0; candidateIndex=0; currentText='';
        render('scan'); timer=window.setTimeout(playStep,700);
      },2200);
      return;
    }
    candidateIndex=0; render('scan');
    var scanCount=0;
    scanTimer=window.setInterval(function(){
      scanCount++;
      candidateIndex=(candidateIndex+1)%current.cands.length;
      render('scan');
      if(scanCount>=4){
        window.clearInterval(scanTimer); scanTimer=null;
        render('pick');
        timer=window.setTimeout(function(){
          typeToken(current.pick,function(){
            step++;
            timer=window.setTimeout(playStep,520);
          });
        },420);
      }
    },260);
  }
  function typeQuestion(done){
    var i=0;
    question.textContent='';
    function add(){
      if(i<questionText.length){
        question.textContent+=questionText.charAt(i++);
        typingTimer=window.setTimeout(add,42);
      }else{
        typingTimer=null; timer=window.setTimeout(done,520);
      }
    }
    add();
  }
  /* 켜자마자 돌지 않는다. 단추를 누르면 시작하고, 돌아가는 중에 누르면 멈춘다.
     멈춘 자리에서 다시 누르면 그 단계부터 이어 돈다 */
  function stopTimers(){
    window.clearTimeout(timer); window.clearTimeout(typingTimer);
    if(scanTimer){window.clearInterval(scanTimer); scanTimer=null;}
  }
  function start(){
    stopTimers();
    mode='base'; step=0; candidateIndex=0; currentText='';
    render('question');
    timer=window.setTimeout(function(){
      typeQuestion(function(){
        step=0; candidateIndex=0; currentText=''; render('scan');
        timer=window.setTimeout(playStep,450);
      });
    },350);
  }
  render('question');
  var playBtn=root.querySelector('[data-sim-play]'), simState='idle';
  if(playBtn) playBtn.addEventListener('click',function(){
    if(simState==='idle'){ start(); }
    else if(simState==='playing'){ stopTimers(); }
    else { stopTimers();
           /* 질문을 치던 중에 멈췄으면 남은 글자를 채우고 이어 간다 */
           if(question.textContent!==questionText) question.textContent=questionText;
           render('scan'); timer=window.setTimeout(playStep,300); }
    simState=simState==='playing'?'paused':'playing';
    playBtn.classList.toggle('is-playing',simState==='playing');
    playBtn.setAttribute('aria-label',simState==='playing'?'일시정지':'이어 보기');
  });
})();
</script>
"""


def _wordy(html):
    """카드 라벨(b) 자리에 문장이 들어간 카드에 표를 붙인다. 글은 건드리지 않는다."""
    out, pos = [], 0
    key = '<div class="axstep'
    while True:
        i = html.find(key, pos)
        if i < 0:
            out.append(html[pos:])
            break
        j = html.index('>', i)
        nxt = html.find(key, j)
        chunk = html[j:nxt if nxt > 0 else len(html)]
        label = re.search(r"<b>(.*?)</b>", chunk, re.S)
        plain = re.sub(r"<[^>]+>", "", label.group(1)) if label else ""
        tag = html[i:j + 1]
        if len(plain) >= 26:
            tag = tag.replace('class="axstep', 'class="axstep wordy', 1)
        out.append(html[pos:i])
        out.append(tag)
        pos = j + 1
    return "".join(out)


def _tallhead(html):
    """제목이 두 줄인 장에 표를 붙인다. 아래 내용이 쓸 높이가 그만큼 줄어든다."""
    m = re.search(r'<h2 class="head">(.*?)</h2>', html, re.S)
    if not m or "<br>" not in m.group(1):
        return html
    return html.replace('<section class="slide ax ', '<section class="slide ax tallhead ', 1)


def v2_patch(slides, REF):
    """장별 구조 손질. 글줄 수와 순서는 건드리지 않는다."""
    out = []
    for i, html in enumerate(slides, 1):
        if i in SAMPLES:
            key, fn = SAMPLES[i]
            out.append(fn(html, key))
        else:
            out.append(_tallhead(_wordy(html)))
    return out
