"""후보 B와 C, 그리고 셋을 나란히 놓고 보는 비교 페이지.

한 장에 하나의 답만 내밀지 않으려고 만든 층이다. 후보 A는 build_ax_v2에 있고,
여기에는 재료가 다른 후보 둘과 비교 화면이 들어간다.

- 후보 A: 생성 이미지를 넣는 안
- 후보 B: 실제 화면이나 직접 그린 그림을 쓰는 안
- 후보 C: 그림 없이 판만으로 푸는 안

빌드: python3 build_ax.py --compare
출력: 후보비교_04_40.html
"""
import re

from functools import partial

from build_ax_v2 import _cells, _grab, _reframe, _slot, _fig_stack, _fig_fall, SLOTS

VARIANT_CSS = """
/* ══ 후보 B와 C의 판 ═══════════════════════════════════════════════
   여기 있는 판은 모두 열과 행을 맞춘다. 칸의 위와 아래, 글의 시작점이
   옆 칸과 같은 줄에 놓이게 하고, 어긋나게 미는 배치는 쓰지 않는다.
   ═══════════════════════════════════════════════════════════════ */

/* ── 4장 B. 실제 대화 화면 두 장 ── */
.shots{display:grid;grid-template-columns:1fr 1fr;gap:46px;flex:none;margin-top:14px}
.shots .imgslot{min-height:0}
.shots .imgbox{flex:none;aspect-ratio:26/9;width:100%}
.shots .imgcap{margin-top:12px}
.shots .imgcap p{font-size:17px;line-height:1.5}
.rsn{display:grid;grid-template-columns:repeat(3,1fr);flex:1;min-height:0;margin-top:26px}
.rsn>div{padding:4px 36px;display:flex;flex-direction:column;justify-content:center;
  border-left:1.5px solid var(--line)}
.rsn>div:first-child{padding-left:0;border-left:none}
.rsn>div:last-child{padding-right:0}
.rsn b{font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.16em;color:var(--faint)}
.rsn h4{font-size:23px;font-weight:800;line-height:1.35;margin:9px 0 8px}
.rsn p{font-size:18px;line-height:1.55;color:var(--dim)}

/* ── 4장 C. 동의가 쌓이는 만큼 길어지는 막대 ── */
.ampg{display:grid;grid-template-columns:288px 500px minmax(0,1fr);column-gap:0;
  flex:1;min-height:0;margin-top:22px}
.ampg>*{align-self:center;padding:32px 0;border-top:1.5px solid var(--line)}
.ampg>*:nth-child(-n+3){border-top:none;padding-top:8px}
.ampb{display:flex;flex-direction:column;gap:12px;padding-right:52px}
.ampb i{display:block;height:16px;border-radius:8px;background:#ECEEF4}
.ampb i:nth-child(1){width:40%}
.ampb i:nth-child(2){width:68%}
.ampb i:nth-child(3){width:100%}
.ampb i.on{background:var(--grad);box-shadow:0 6px 16px rgba(200,90,120,.18)}
.ampl b{font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.16em;color:var(--faint)}
.ampl{padding-right:52px}
.ampl h4{font-size:28px;font-weight:800;line-height:1.35;margin-top:10px}
.ampd{font-size:22px;line-height:1.62;color:var(--dim);max-width:880px}

/* ── 40장 B. 차례로 넘어지는 판 ── */
.domi{display:grid;grid-template-rows:1fr auto;grid-auto-flow:column;
  grid-auto-columns:minmax(0,1fr);flex:1;min-height:0;margin-top:20px}
.dfig{position:relative;border-bottom:2px solid var(--line)}
.dfig i{position:absolute;left:14px;bottom:0;width:94px;height:272px;border-radius:14px;
  border:2px solid rgba(0,0,0,.06);transform-origin:bottom right;transform:rotate(var(--r))}
.dfig.d1 i{background:linear-gradient(165deg,#FFCFA6,#F9AEC6)}
.dfig.d2 i{background:linear-gradient(165deg,#FFE0C6,#FBC8DA)}
.dfig.d3 i{background:linear-gradient(165deg,#F3EDE6,#EFDDE6)}
.dfig.d4 i{background:#EFF0F5}
.dtx{padding:26px 44px 0 0}
.dtx b{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.12em;color:var(--faint)}
.dtx h4{font-size:24px;font-weight:800;line-height:1.35;margin:9px 0 9px}
.dtx p{font-size:18.5px;line-height:1.55;color:var(--dim)}
.dtx.out h4{color:#FF4D6D}

/* ── 40장 C. 사고 뒤에 붙는 정지 구간 ── */
.tline{display:grid;grid-template-columns:1fr 1fr 1fr 2.05fr;flex:1;min-height:0;margin-top:22px}
.tstop{position:relative;display:grid;grid-template-rows:1fr 52px 1fr;min-width:0;padding-right:40px}
.tstop:last-child{padding-right:0}
.tstop::before{content:"";position:absolute;left:25px;top:6px;bottom:6px;width:2px;
  background:repeating-linear-gradient(180deg,#EDEFF5 0 7px,transparent 7px 14px)}
.tstop h4{position:relative;align-self:end;font-size:27px;font-weight:800;line-height:1.35;padding-bottom:24px}
.tstop p{position:relative;align-self:start;font-size:19.5px;line-height:1.58;color:var(--dim);padding-top:24px}
.trk{position:relative;display:flex;align-items:center;gap:0}
.trk b{flex:none;width:52px;height:52px;border-radius:50%;background:var(--grad);color:#fff;
  display:grid;place-items:center;font-family:var(--fm);font-size:19px;font-weight:700;
  box-shadow:0 10px 24px rgba(200,90,120,.26)}
.trk s{flex:1;height:3px;background:linear-gradient(90deg,#F3B08C,#C9A6F0);text-decoration:none}
.tstop.dead{border-radius:22px;
  background:linear-gradient(180deg,rgba(233,236,243,0) 4%,rgba(226,230,239,.85) 96%)}
.tstop.dead::before{display:none}
.tstop.dead h4{color:#FF4D6D;padding-left:26px}
.tstop.dead p{padding-left:26px}
.tstop.dead .trk{padding-left:26px}
.tstop.dead .trk s{height:14px;border-radius:7px;margin-right:26px;
  background:repeating-linear-gradient(120deg,#CFD4E0 0 9px,#E8EBF2 9px 18px)}
"""


def _v4_shots(html):
    """4장 B. 실제 대화 화면 두 장을 위에 나란히 두고 이유 셋을 아래 세 칸에 맞춘다."""
    cells = _cells(html, "axstep")
    if len(cells) != 3:
        return html
    rsn = "".join(f'<div><b>{lab}</b><h4>{h4}</h4><p>{pp}</p></div>' for lab, h4, pp in cells)
    body = (f'<div class="shots">{_slot("s4sure")}{_slot("s4doubt")}</div>'
            f'<div class="rsn">{rsn}</div>'
            f'{_grab(html, r"<div class=\"axband\"[^>]*>.*?</div>")}')
    return _reframe(html, body)


def _v4_amp(html):
    """4장 C. 그림 없이, 동의가 쌓인 만큼 길어지는 막대로 증폭을 보인다."""
    cells = _cells(html, "axstep")
    if len(cells) != 3:
        return html
    rows = []
    for i, (lab, h4, pp) in enumerate(cells, 1):
        bars = "".join(f'<i class="{"on" if k <= i else ""}"></i>' for k in (1, 2, 3))
        rows.append(f'<div class="ampb">{bars}</div>'
                    f'<div class="ampl"><b>{lab}</b><h4>{h4}</h4></div>'
                    f'<div class="ampd">{pp}</div>')
    body = (f'<div class="ampg">{"".join(rows)}</div>'
            f'{_grab(html, r"<div class=\"axband\"[^>]*>.*?</div>")}')
    return _reframe(html, body)


def _v40_domino(html):
    """40장 B. 네 단계를 차례로 넘어지는 판으로 직접 그린다. 그림 생성이 필요 없다."""
    cells = _cells(html, "stepn")
    if len(cells) != 4:
        return html
    tilt = ("0deg", "16deg", "46deg", "90deg")
    out = []
    for i, ((lab, h4, pp), r) in enumerate(zip(cells, tilt), 1):
        cls = " out" if i == 4 else ""
        out.append(f'<div class="dfig d{i}"><i style="--r:{r}"></i></div>'
                   f'<div class="dtx{cls}"><b>{lab}</b><h4>{h4}</h4><p>{pp}</p></div>')
    body = (f'<div class="domi">{"".join(out)}</div>'
            f'{_grab(html, r"<div class=\"axband\"[^>]*>.*?</div>")}')
    return _reframe(html, body)


def _v40_axis(html):
    """40장 C. 사건 셋은 촘촘하고 그 뒤 정지 구간만 길게 남는 시간 축."""
    cells = _cells(html, "stepn")
    if len(cells) != 4:
        return html
    out = []
    for i, (lab, h4, pp) in enumerate(cells, 1):
        cls = " dead" if i == 4 else ""
        out.append(f'<div class="tstop{cls}"><h4>{h4}</h4>'
                   f'<div class="trk"><b>{lab}</b><s></s></div><p>{pp}</p></div>')
    body = (f'<div class="tline">{"".join(out)}</div>'
            f'{_grab(html, r"<div class=\"axband\"[^>]*>.*?</div>")}')
    return _reframe(html, body)


# 장 번호별 후보. 첫 항목이 지금 v2에 들어가 있는 안이다.
VARIANTS = {
    4: [("A", "생성 이미지", partial(_fig_stack, key="a4"),
         "질문이 되돌아올수록 굵어지는 고리를 그림으로 뽑고, 오른쪽에 이유 셋을 둡니다. "
         "세 마디를 오른쪽으로 밀어 계단으로 만든 탓에 글의 시작점이 줄마다 다릅니다."),
        ("B", "실제 대화 화면", _v4_shots,
         "확신을 담아 물은 화면과 의심하게 물은 화면을 실제로 갈무리해 나란히 놓습니다. "
         "두 화면은 같은 높이로 맞추고, 아래 이유 셋은 세 칸으로 균등하게 나눕니다."),
        ("C", "그림 없이 판만", _v4_amp,
         "동의가 쌓인 만큼 길어지는 막대를 왼쪽에 두고 이유 셋을 행으로 쌓습니다. "
         "막대, 제목, 설명이 각각 같은 열에 서고 행 사이는 선 하나로 나눕니다.")],
    40: [("A", "생성 이미지", partial(_fig_fall, key="a40"),
          "종이 한 장이 번져 화면이 꺼지는 장면을 가로로 긴 그림으로 뽑습니다. "
          "아래 네 마디를 조금씩 내려 앉혀 윗변이 줄마다 어긋납니다."),
         ("B", "직접 그린 그림", _v40_domino,
          "네 단계를 기울기가 커지는 판 네 개로 직접 그립니다. 바닥선 하나가 네 칸을 가로지르고, "
          "판과 글이 모두 같은 줄에서 시작합니다. 그림을 따로 뽑지 않아도 됩니다."),
         ("C", "시간 축", _v40_axis,
          "사건 셋은 촘촘히 붙고 마지막 사건 뒤로 멈춰 선 구간이 길게 남습니다. "
          "손해가 사고 자체보다 그 뒤에 온다는 말을 길이로 보입니다.")],
}
# 32장(콘텐츠 갈무리)과 33장(지휘실)이 끼면서 그 뒤 장 번호가 둘씩 밀렸다.
# 후보는 예전 번호로 적어 두고 여기서 옮긴다.
VARIANTS = {(k + 2 if k >= 32 else k): v for k, v in VARIANTS.items()}

COMPARE_CSS = """
html{scroll-snap-type:none !important}
body{background:#F2F3F7;display:block;padding:0 0 90px}
.cmp{max-width:1880px;margin:0 auto;padding:0 40px}
.cmphd{padding:64px 0 10px}
.cmphd h1{font-family:var(--f);font-size:38px;font-weight:800;letter-spacing:-.02em}
.cmphd p{margin-top:14px;font-size:19px;line-height:1.65;color:var(--dim);max-width:1080px}
.cmphd p+p{margin-top:8px}
.grp{margin-top:52px}
.grp>h2{font-size:24px;font-weight:800;margin-bottom:6px}
.grp>h2 em{font-style:normal;font-family:var(--fm);font-size:15px;font-weight:700;
  letter-spacing:.14em;color:var(--faint);margin-right:14px}
.grp>.cmpsub{font-size:18px;color:var(--dim);margin-bottom:24px}
.row{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;align-items:start}
.cmpcard{background:#fff;border:1.5px solid #E4E7EF;border-radius:20px;overflow:hidden;
  box-shadow:0 12px 34px rgba(40,50,80,.07)}
.cmpcard .stage{position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;cursor:zoom-in;
  border-bottom:1.5px solid #ECEEF4;background:#fff}
.cmpcard .vp{position:absolute;top:0;left:0;width:1920px;height:1080px;display:block;overflow:hidden;
  transform:scale(var(--t));transform-origin:0 0}
.cmpcard .slide{transform:none;box-shadow:none;margin:0}
.cmpcard figcaption{padding:22px 26px 26px}
.cmpcard .cl{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.cmpcard .cl b{font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.16em;color:var(--faint)}
.cmpcard .cl span{font-size:17px;font-weight:800;padding:5px 14px;border-radius:999px;
  background:linear-gradient(135deg,#FFF1E6,#F6ECFD);color:#7A4FBE}
.cmpcard figcaption p{font-size:17px;line-height:1.6;color:var(--dim)}
.zoom{position:fixed;inset:0;z-index:90;background:rgba(24,28,40,.88);display:none;
  align-items:center;justify-content:center}
.zoom.on{display:flex}
.zoom .zst{position:relative;width:1920px;height:1080px;transform:scale(var(--z));
  transform-origin:center center;background:#fff;box-shadow:0 30px 90px rgba(0,0,0,.4)}
.zoom .zst .vp{position:absolute;top:0;left:0;width:1920px;height:1080px;display:block;transform:none}
.zbar{position:fixed;left:0;right:0;bottom:26px;display:none;justify-content:center;gap:14px;z-index:92}
.zoom.on~.zbar{display:flex}
.zbar button{border:none;border-radius:999px;padding:12px 22px;font-family:var(--f);font-size:16px;
  font-weight:700;cursor:pointer;background:rgba(255,255,255,.94);color:var(--ink)}
.znow{position:fixed;top:26px;left:0;right:0;text-align:center;z-index:92;color:#fff;
  font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.16em}
"""

COMPARE_JS = """
<script>
(function(){
  var stages=[].slice.call(document.querySelectorAll('.cmpcard .stage'));
  var fitThumbs=function(){stages.forEach(function(s){
    s.style.setProperty('--t', s.clientWidth/1920)})};
  addEventListener('resize',fitThumbs);fitThumbs();

  var zoom=document.querySelector('.zoom'), zst=zoom.querySelector('.zst');
  var znow=document.querySelector('.znow'), home=null, cur=-1;
  var fitZoom=function(){zoom.style.setProperty('--z',
    Math.min((innerWidth-80)/1920,(innerHeight-160)/1080))};
  addEventListener('resize',fitZoom);fitZoom();

  var close=function(){ if(!home) return;
    home.appendChild(zst.firstElementChild); home=null; cur=-1; zoom.classList.remove('on')};
  var open=function(i){ if(i<0||i>=stages.length) return; close();
    var s=stages[i]; home=s; cur=i;
    zst.appendChild(s.firstElementChild);
    znow.textContent=s.getAttribute('data-name')||'';
    zoom.classList.add('on'); fitZoom()};

  stages.forEach(function(s,i){s.addEventListener('click',function(){open(i)})});
  zoom.addEventListener('click',function(e){if(e.target===zoom) close()});
  document.querySelector('[data-go="prev"]').addEventListener('click',function(){open((cur+stages.length-1)%stages.length)});
  document.querySelector('[data-go="next"]').addEventListener('click',function(){open((cur+1)%stages.length)});
  document.querySelector('[data-go="close"]').addEventListener('click',close);
  addEventListener('keydown',function(e){
    if(!zoom.classList.contains('on')) return;
    if(e.key==='Escape') close();
    if(e.key==='ArrowRight') open((cur+1)%stages.length);
    if(e.key==='ArrowLeft') open((cur+stages.length-1)%stages.length)});
})();
</script>
"""


def _title(html):
    m = re.search(r'<h2 class="head">(.*?)</h2>', html, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""


def compare_body(slides):
    """장별 후보를 한 줄에 셋씩 놓은 비교 화면의 안쪽을 만든다."""
    grp = []
    for n in sorted(VARIANTS):
        src = slides[n - 1]
        cards = []
        for label, kind, fn, note in VARIANTS[n]:
            name = f"{n:02d}장 후보 {label} {kind}"
            cards.append(
                f'<figure class="cmpcard"><div class="stage" data-name="{name}">{fn(src)}</div>'
                f'<figcaption><div class="cl"><b>후보 {label}</b><span>{kind}</span></div>'
                f'<p>{note}</p></figcaption></figure>')
        grp.append(f'<section class="grp"><h2><em>{n:02d}</em>{_title(src)}</h2>'
                   f'<p class="cmpsub">재료가 다른 세 안입니다. 화면을 누르면 크게 봅니다. '
                   f'좌우 방향키로 후보를 옮기고 ESC로 닫습니다.</p>'
                   f'<div class="row">{"".join(cards)}</div></section>')
    return ('<div class="cmp">'
            '<div class="cmphd"><h1>4장과 40장 후보 비교</h1>'
            '<p>한 장에 안 하나를 내밀지 않고, 재료가 다른 안을 셋씩 놓았습니다. '
            '글은 원본 그대로이고 판만 다릅니다.</p>'
            '<p>후보 A는 지금 v2 파일에 들어가 있는 안입니다. 어긋나게 민 배치를 그대로 두어 '
            '나머지 둘과 견주어 보게 했습니다.</p></div>'
            + "".join(grp) + '</div>'
            + '<div class="zoom"><div class="zst"></div></div>'
            + '<div class="znow"></div>')


def compare_controls():
    return ('<div class="zbar"><button type="button" data-go="prev">이전 후보</button>'
            '<button type="button" data-go="next">다음 후보</button>'
            '<button type="button" data-go="close">닫기</button></div>')
