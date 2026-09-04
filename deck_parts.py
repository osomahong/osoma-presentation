#!/usr/bin/env python3
"""장을 짜는 데 쓰는 조각들. 카드, 계단, 마주 놓기, 목록판, 아이콘, 일러스트 칸.

여기에는 화면에 보이는 글을 두지 않는다. 조각의 모양과 CSS만 담는다.
장 구성과 문장은 build_deck.py 에 있다.
"""

# 덱을 다섯 부로 나눈다. 장마다 머리말에 이 이름이 붙는다
P1, P2, P3, P4, P5 = ("1부 무엇을 하는 회사인가", "2부 일하는 방식",
                      "3부 스물네 곳을 동시에", "4부 AI를 얹은 자리", "5부 쌓인 것과 앞으로")


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
.resultbar i{width:10px;height:10px;border-radius:50%;background:#3395DA;box-shadow:18px 0 #6FD3C7,36px 0 #65C78A;margin-right:36px}
.resultbody{padding:28px 30px;font-family:var(--fm);font-size:17px;line-height:1.7}
.resultbody .rlabel{display:block;color:#8B93A6;font-size:11px;letter-spacing:.14em;margin-bottom:11px}
.resultbody .rbubble{padding:16px 18px;border-radius:14px;background:#303645;color:#fff;font-weight:600}
.resultbody .rmissing{margin-top:24px;padding-top:18px;border-top:1px solid rgba(255,255,255,.1);color:#AEB6CA;font-size:14px;line-height:1.7}
.resultbody .rmissing strong{display:block;margin-bottom:7px;color:#7CC0EA;font-size:13px}
.rulefile{background:#fff;border:1.5px solid var(--line);padding:22px 28px;box-shadow:0 16px 44px rgba(40,50,80,.08)}
.rfhead{display:flex;align-items:center;justify-content:space-between;padding-bottom:14px;border-bottom:1.5px solid var(--line)}
.rfhead b{font-family:var(--fm);font-size:14px;letter-spacing:.06em;color:var(--ink)}
.rfhead span{font-family:var(--fm);font-size:11px;color:#5BBA82;background:#E9F8EF;border-radius:999px;padding:5px 9px}
.rflist{display:flex;flex-direction:column;margin-top:4px}
.rfrow{display:grid;grid-template-columns:104px minmax(0,1fr);gap:18px;align-items:baseline;padding:11px 0;border-bottom:1px solid #EEF0F5}
.rfrow:last-child{border-bottom:none}
.rfrow b{font-family:var(--fm);font-size:12px;letter-spacing:.08em;color:#2F86C4}
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
  background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box;box-shadow:0 16px 38px rgba(40,120,180,.14)}
.cjob{font-family:var(--f);font-size:15px;font-weight:700;letter-spacing:.02em;color:var(--faint);margin-bottom:7px}
.crow h4{font-size:22px;font-weight:800;line-height:1.4}
.crow p{margin-top:8px;font-size:17.5px;line-height:1.55;color:var(--dim)}
/* 왼쪽에 그림이나 도식, 오른쪽에 번호가 붙은 줄 목록을 놓는다. 줄이 다섯쯤 될 때 쓴다 */
.dkwrap{display:grid;grid-template-columns:1fr 1.04fr;gap:44px;flex:1;min-height:0;
  align-items:center;margin-top:26px}
.dkrows{display:flex;flex-direction:column;justify-content:center;gap:14px;min-height:0}
.dkrow{display:grid;grid-template-columns:50px 1fr;gap:20px;align-items:center;
  background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:16px 26px;
  box-shadow:0 8px 22px rgba(40,50,80,.05)}
.dkrow b{display:grid;place-items:center;width:50px;height:50px;border-radius:50%;
  font-family:var(--fm);font-size:17px;font-weight:700;color:#fff;background:var(--grad);
  box-shadow:0 8px 20px rgba(40,120,180,.22)}
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
.hbar span.judge{background:linear-gradient(120deg,#E4F2FB,#DFF3F0);color:var(--ink)}
.hrow.after .hbar span.judge{background:var(--grad);color:#fff}
/* 지시문 상자 */
.promptbox .tbody{font-size:19px;line-height:1.85;white-space:normal}
/* 규칙 파일. 터미널 판을 그대로 쓰되 안은 해야 할 것과 하지 않을 것 두 묶음이다 */
.rulebox .tbody{padding:26px 30px 28px;font-family:var(--f);white-space:normal;line-height:1.6}
.rgrp + .rgrp{margin-top:24px;padding-top:22px;border-top:1px solid rgba(255,255,255,.10)}
.rhead{font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.12em;margin-bottom:14px}
.rhead.ok{color:#6EE7A0}
.rhead.no{color:#4E9BC9}
.rgrp ul{list-style:none;display:flex;flex-direction:column;gap:11px}
.rgrp li{position:relative;padding-left:26px;font-size:18.5px;color:#D6DBE7;word-break:keep-all}
.rgrp li::before{position:absolute;left:0;top:0;font-family:var(--fm);font-weight:700}
.rgrp.y li::before{content:"+";color:#6EE7A0}
.rgrp.n li::before{content:"-";color:#4E9BC9}

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
  display:grid;place-items:center;cursor:pointer;box-shadow:0 8px 20px rgba(40,120,180,.34);transition:transform .16s}
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
.simcand.pick{color:#fff;border-color:#3395DA;background:linear-gradient(120deg,#1B6FA8,#35B4C7);font-weight:700;transform:translateY(-2px)}
.simstatus{display:flex;align-items:center;gap:8px;margin-top:15px;min-height:18px;font-size:12px;color:#AEB6CA}
.simstatus i{width:7px;height:7px;flex:none;border-radius:50%;background:#3395DA;box-shadow:0 0 0 4px rgba(51,149,218,.12);animation:simlive 1.15s ease-in-out infinite}
.simstatus span{font-family:var(--fm);letter-spacing:.04em;color:#D9DEEA}
.simstatus b{margin-left:auto;color:#fff;font-weight:600}
.simprogress{display:flex;align-items:center;margin-top:14px}
.simprogress i{height:4px;flex:1;border-radius:4px;background:linear-gradient(90deg,#3395DA 0 0%,#343D53 0% 100%);transition:background .45s ease}
.simoutput strong::after{content:"▌";display:inline-block;margin-left:3px;color:#3395DA;animation:simcursor .85s steps(1) infinite}
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
.sowfig{background:linear-gradient(150deg,#EEF6FC,#E9F4FA 45%,#E9F6F6 75%,#EDF8F5);
  border:1.5px solid #DFEAF2;border-radius:26px;padding:22px 30px 32px;
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
.bub.narr{max-width:66%;font-weight:600;background:#EEF6FC;border-radius:8px;box-shadow:0 8px 20px rgba(20,45,70,.16)}
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
