"""후보 판 묶음.

원본 장에서 뽑은 글을 다른 판에 다시 앉힌다. 글은 그대로 두고 자리만 바꾼다.
판을 짤 때 지키는 것은 넷이다.

- 칸은 균등하게 나눈다. 세 칸이면 세 칸 모두 폭이 같다.
- 같은 종류의 글은 같은 줄에서 시작한다. 라벨끼리, 제목끼리, 설명끼리 윗변을 맞춘다.
- 어긋나게 미는 계단 배치는 그 어긋남 자체가 뜻일 때만 쓴다.
- 그림 넣을 곳은 비율을 못 박고 캡션과 복사 단추를 함께 붙인다.
"""
from build_ax_v2 import _reframe
from v2_parts import band

LAYOUT_CSS = """
/* ══ 후보 판 ═══════════════════════════════════════════════════════
   여기 있는 판은 모두 열과 행을 맞춘다. 칸의 윗변과 글의 시작점이 옆 칸과 같은 줄에 선다.
   ═══════════════════════════════════════════════════════════════ */
.Lc{display:flex;flex-direction:column;flex:1;min-height:0;margin-top:24px;gap:24px}
.Lc>.axband{flex:none;margin-top:0}
/* 덩이를 둘 이상 쌓은 판. 높이를 나눠 쓰므로 글자와 여백을 한 단계 줄인다 */
.Lc.dense{margin-top:18px;gap:18px}
.Lc.dense .Lrow{padding:11px 0}
.Lc.dense .Lrow h4{font-size:21px;margin-bottom:5px}
.Lc.dense .Lrow p{font-size:17px;line-height:1.48}
.Lc.dense .Lsub{font-size:14.5px;margin-top:5px}
.Lc.dense .Lpl,.Lc.dense .Lpr{padding:11px 0;font-size:18px;line-height:1.45}
.Lc.dense .Lpe{padding-top:12px;font-size:17.5px}
.Lc.dense .Lmk{padding:12px 0}
.Lc.dense .Lmk h4{font-size:20px}
.Lc.dense .Lmk p{font-size:16.5px}
.Lc.dense .Lcell{padding:20px 22px}
.Lc.dense .Lcell h4{font-size:21px;margin-bottom:7px}
.Lc.dense .Lcell p{font-size:17px;line-height:1.48}
.Lc.dense .Laxpt{padding-top:30px}
.Lc.dense .Laxpt h4{font-size:21px}
.Lc.dense .Laxpt p{font-size:17px;line-height:1.48}
.Lc.dense .Lqc{padding:20px 24px}
.Lc.dense .Lqc h4{font-size:20px}
.Lc.dense .Lqc p{font-size:16.5px}

/* 두 칸: 왼쪽 그림, 오른쪽 글 */
.L2{display:grid;grid-template-columns:.92fr 1fr;gap:56px;flex:1;min-height:0;align-items:stretch}
.L2.wide{grid-template-columns:1.15fr 1fr}
.L2.narrow{grid-template-columns:.62fr 1fr}
.L2>.imgslot{min-height:0}
.Lside{display:flex;flex-direction:column;justify-content:center;gap:18px;min-height:0}

/* 위아래: 그림 위, 글 아래.
   가로로 긴 구획은 폭에 맞추면 화면을 넘긴다. 남은 높이에 맞추고 폭은 비율이 정하게 둔다 */
.Ltop{display:flex;flex-direction:column;flex:1;min-height:0;gap:26px}
.Ltop>.imgslot{flex:1.5 1 0;min-height:0}
.Ltop>.imgslot>.imgbox{flex:1 1 auto !important;min-height:0;height:auto;
  width:auto !important;max-width:100%;align-self:center;margin:0 auto}
.Ltop>.imgslot>.imgcap{margin-top:14px}
/* 구획이 자리를 먹으니 아래 글은 한 단계 촘촘하게 */
.Ltop>.Lrows{flex:1 1 0}
.Ltop .Lrow{padding:12px 0}
.Ltop .Lrow h4{font-size:22px;margin-bottom:5px}
.Ltop .Lrow p{font-size:17.5px;line-height:1.5}
.Ltop .Lsub{font-size:15px;margin-top:6px}

/* 구획 여럿을 한 줄에 */
.Lgrid{display:grid;gap:34px;flex:none}
.Lgrid.g2{grid-template-columns:1fr 1fr}
.Lgrid.g4{grid-template-columns:repeat(4,1fr);gap:24px}
.Lgrid .imgcap p{font-size:16.5px;line-height:1.5}
.Lgrid.g4 .imgcap{flex-direction:column;gap:12px}
.Lgrid.g4 .imgcap p{font-size:15.5px}
.Lgrid.g4 .pbtn{font-size:14px;padding:9px 15px}

/* 행으로 쌓는 글. 라벨, 제목, 설명이 각각 같은 열에 선다 */
.Lrows{display:grid;flex:1;min-height:0;align-content:stretch}
.Lrow{display:grid;grid-template-columns:132px minmax(0,1fr);column-gap:32px;align-items:center;
  padding:20px 0;border-top:1.5px solid var(--line)}
.Lrow:first-child{border-top:none}
.Lrow>b{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.16em;color:var(--faint)}
.Lrow h4{font-size:25px;font-weight:800;line-height:1.34;margin-bottom:7px}
.Lrow p{font-size:19px;line-height:1.56;color:var(--dim)}
/* 줄이 늘면 그만큼 촘촘하게. 넘쳐서 결론 띠를 덮지 않게 한다 */
.Lrows.t4 .Lrow{padding:14px 0}
.Lrows.t4 .Lrow h4{font-size:23px;margin-bottom:6px}
.Lrows.t4 .Lrow p{font-size:18px;line-height:1.5}
.Lrows.t4 .Lsub{font-size:15.5px;margin-top:6px}
.Lrows.t5 .Lrow{padding:11px 0;grid-template-columns:108px minmax(0,1fr);column-gap:24px}
.Lrows.t5 .Lrow h4{font-size:21px;margin-bottom:5px}
.Lrows.t5 .Lrow p{font-size:17px;line-height:1.48}
.Lrows.t5 .Lsub{font-size:15px;margin-top:5px}
.Lrows.t6 .Lrow{padding:8px 0;grid-template-columns:96px minmax(0,1fr);column-gap:20px}
.Lrows.t6 .Lrow h4{font-size:19.5px;margin-bottom:4px}
.Lrows.t6 .Lrow p{font-size:16px;line-height:1.45}
.Lrows.t6 .Lsub{font-size:14.5px;margin-top:4px}

/* 세 칸, 네 칸, 다섯 칸으로 균등하게 */
.Lcols{display:grid;gap:34px;flex:1;min-height:0;align-content:stretch}
.Lcols.c2{grid-template-columns:1fr 1fr}
.Lcols.c3{grid-template-columns:repeat(3,1fr)}
.Lcols.c4{grid-template-columns:repeat(4,1fr);gap:26px}
.Lcols.c5{grid-template-columns:repeat(5,1fr);gap:20px}
.Lcell{display:flex;flex-direction:column;justify-content:flex-start;min-width:0;
  background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:30px 28px}
.Lcell.plain{background:none;border:none;padding:26px 22px 26px 0;border-left:1.5px solid var(--line);
  padding-left:30px}
.Lcell.plain:first-child{border-left:none;padding-left:0}
.Lcell>b{display:block;font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.16em;
  color:var(--faint);margin-bottom:14px}
.Lcell h4{font-size:24px;font-weight:800;line-height:1.34;margin-bottom:10px}
.Lcell p{font-size:18.5px;line-height:1.56;color:var(--dim)}
.Lcols.c5 .Lcell h4{font-size:21px}
.Lcols.c5 .Lcell p{font-size:17px;line-height:1.5}
.Lcols.c4 .Lcell h4{font-size:22px}
.Lcols.c4 .Lcell p{font-size:17.5px}

/* 큰 번호를 앞세운 세 칸 */
.Lbig>b{font-family:var(--fm);font-size:76px;font-weight:800;line-height:1;letter-spacing:-.03em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;margin-bottom:22px}

/* 가로 축 하나 위에 지점을 찍는다 */
.Laxis{display:flex;flex-direction:column;flex:1;min-height:0;justify-content:center;gap:0}
.Laxend{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:26px;
  font-family:var(--fm);font-size:16px;font-weight:700;letter-spacing:.14em;color:var(--faint)}
.Laxend s{height:2px;background:var(--line);text-decoration:none;display:block}
.Laxend span:last-child{text-align:right}
.Laxtrack{position:relative;height:8px;border-radius:4px;background:var(--grad);margin:34px 0 0}
.Laxpts{display:grid;margin-top:0}
.Laxpt{position:relative;padding:34px 26px 0 0;min-width:0}
.Laxpt::before{content:"";position:absolute;left:0;top:-30px;width:22px;height:22px;border-radius:50%;
  background:#fff;border:5px solid var(--v,#A855F7);box-shadow:0 6px 16px rgba(120,80,200,.2)}
.Laxpt b{display:block;font-family:var(--fm);font-size:14.5px;font-weight:700;letter-spacing:.16em;
  color:var(--faint);margin-bottom:9px}
.Laxpt h4{font-size:24px;font-weight:800;line-height:1.34;margin-bottom:8px}
.Laxpt p{font-size:18.5px;line-height:1.55;color:var(--dim)}
.Lsub{display:block;margin-top:9px;font-size:16.5px;line-height:1.5;color:var(--faint)}
.Laxpt.cut::before{border-color:#FF4D6D;background:#FFF1F4}
.Laxpt.cut h4{color:#FF4D6D}
/* 지점이 늘면 칸이 좁아지니 글자도 함께 줄인다 */
.Laxpts.t4 .Laxpt{padding-right:20px}
.Laxpts.t4 .Laxpt h4{font-size:21.5px}
.Laxpts.t4 .Laxpt p{font-size:17px;line-height:1.5}
.Laxpts.t4 .Lsub{font-size:15px;margin-top:7px}
.Laxpts.t5 .Laxpt{padding-right:16px}
.Laxpts.t5 .Laxpt b{font-size:13px;margin-bottom:7px}
.Laxpts.t5 .Laxpt h4{font-size:19.5px;margin-bottom:6px}
.Laxpts.t5 .Laxpt p{font-size:15.5px;line-height:1.45}
.Laxpts.t5 .Lsub{font-size:14px;margin-top:6px}
.Laxpts.t6 .Laxpt{padding-right:14px}
.Laxpts.t6 .Laxpt h4{font-size:18px}
.Laxpts.t6 .Laxpt p{font-size:14.5px;line-height:1.42}

/* 축 아래에 놓는 한 줄 목록. 축이 나른 쪽과 겹치지 않게 낮게 깐다 */
.Lgone{display:flex;flex-wrap:wrap;align-items:baseline;gap:12px 20px;flex:none;
  padding-top:22px;border-top:1.5px solid var(--line)}
.Lgone>b{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.14em;
  color:var(--faint);margin-right:6px}
.Lgone>span{font-size:19px;color:var(--dim)}
.Lgone>span+span::before{content:"";display:inline-block;width:4px;height:4px;border-radius:50%;
  background:var(--line);vertical-align:middle;margin-right:20px}
.Lgone>em{font-style:normal;font-size:18px;font-weight:800;color:var(--ink);margin-left:auto}

/* 계단 */
.Lstair{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;align-items:end;flex:1;min-height:0;gap:20px}
.Lstep{display:flex;flex-direction:column;justify-content:flex-end;min-width:0}
.Lstep .Lbox{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:flex-end;
  border-radius:20px 20px 0 0;padding:24px 24px 26px;border:1.5px solid var(--line);
  border-bottom:none;background:#fff}
.Lstep b{font-family:var(--fm);font-size:14.5px;font-weight:700;letter-spacing:.16em;color:var(--faint)}
.Lstep h4{font-size:24px;font-weight:800;margin:9px 0 8px;line-height:1.32}
.Lstep p{font-size:17.5px;line-height:1.5;color:var(--dim)}
.Lstep.here .Lbox{border:2px solid transparent;border-bottom:none;
  background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box;
  box-shadow:0 -10px 34px rgba(200,90,120,.14)}
.Lstair+.Lfloor{height:6px;border-radius:3px;background:var(--grad);flex:none}

/* 길이와 면적으로 견주기 */
.Lspan{display:flex;flex-direction:column;flex:1;min-height:0;justify-content:center;gap:44px}
.Lsp{display:grid;grid-template-columns:210px minmax(0,1fr);column-gap:34px;align-items:center}
.Lsp>b{font-family:var(--fm);font-size:17px;font-weight:700;letter-spacing:.14em;color:var(--faint)}
.Lsbar{height:74px;border-radius:16px;display:flex;align-items:center;padding:0 30px;
  font-size:22px;font-weight:800;color:#fff}
.Lsbar.a{background:var(--grad)}
.Lsbar.b{background:#E4E7EF;color:var(--dim)}
.Lspn{margin-top:12px;font-size:18.5px;line-height:1.55;color:var(--dim)}
.Lspan.compact{flex:none;gap:28px;justify-content:flex-start}
.Lspan.compact .Lsbar{height:64px}

/* 두 목록을 한 줄씩 마주 놓기 */
.Lpair{display:grid;grid-template-columns:1fr 76px 1fr;flex:1;min-height:0;align-content:stretch;
  column-gap:0}
.Lpair>.Lph{padding-bottom:18px;font-family:var(--fm);font-size:15px;font-weight:700;
  letter-spacing:.14em;color:var(--faint)}
.Lpair>.Lph.r{text-align:right}
.Lpl,.Lpr{display:flex;align-items:center;padding:18px 0;border-top:1.5px solid var(--line);
  font-size:20px;line-height:1.5}
.Lpr{justify-content:flex-end;text-align:right;color:var(--dim)}
.Lpm{display:grid;place-items:center;border-top:1.5px solid var(--line)}
.Lpm i{display:block;width:26px;height:2px;background:var(--line)}
.Lpe{padding-top:18px;font-size:19px;font-weight:800}
.Lpe.r{text-align:right;color:var(--dim)}

/* 위아래 두 줄, 시작점이 다르다 */
.Ltwo{display:flex;flex-direction:column;flex:1;min-height:0;justify-content:center;gap:46px}
.Ltl{display:grid;grid-template-columns:200px minmax(0,1fr);column-gap:30px;align-items:center}
.Ltl>b{font-family:var(--fm);font-size:16px;font-weight:700;letter-spacing:.14em;color:var(--faint)}
.Lttrack{position:relative;display:grid;grid-auto-flow:column;grid-auto-columns:1fr;
  align-items:center;height:64px}
.Lttrack::before{content:"";position:absolute;left:0;right:0;top:31px;height:3px;background:var(--line)}
.Ltnode{position:relative;display:grid;place-items:center}
.Ltnode i{width:24px;height:24px;border-radius:50%;background:#E4E7EF;display:block}
.Ltnode.on i{background:var(--grad);box-shadow:0 6px 16px rgba(200,90,120,.24)}
.Ltnode span{position:absolute;top:38px;font-size:16px;color:var(--dim);white-space:nowrap}
.Ltnote{margin-top:16px;font-size:19px;line-height:1.55;color:var(--dim)}
.Ltnode span:empty{display:none}
.Ltwo.compact{flex:none;gap:24px;justify-content:flex-start}
.Ltwo.compact .Lttrack{height:46px}
.Ltwo.compact .Lttrack::before{top:22px}

/* 네 구역 */
.Lquad{display:grid;grid-template-columns:170px 1fr 1fr;grid-template-rows:auto 1fr 1fr;
  flex:1;min-height:0;gap:0}
.Lqh{display:grid;place-items:center;padding:14px;font-family:var(--fm);font-size:15px;
  font-weight:700;letter-spacing:.14em;color:var(--faint)}
.Lqs{display:grid;place-items:center;text-align:center;padding:14px;font-family:var(--fm);
  font-size:15px;font-weight:700;letter-spacing:.14em;color:var(--faint)}
.Lqc{border:1.5px solid var(--line);margin:-0.75px 0 0 -0.75px;padding:26px 30px;
  display:flex;flex-direction:column;justify-content:center}
.Lqc h4{font-size:22px;font-weight:800;line-height:1.34;margin-bottom:9px}
.Lqc p{font-size:18px;line-height:1.55;color:var(--dim)}
.Lqc.hot{background:linear-gradient(150deg,#FFF3EC,#FBEFF7);border-color:transparent}
.Lqc.hot h4{color:#C2185B}

/* 큰 낱말 한 줄 */
.Lwords{display:grid;grid-auto-flow:column;grid-auto-columns:1fr;flex:1;min-height:0;
  align-items:center;gap:22px}
.Lw{min-width:0;text-align:left}
.Lw h4{font-size:40px;font-weight:800;line-height:1.2;letter-spacing:-.02em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.Lw p{margin-top:16px;font-size:17.5px;line-height:1.55;color:var(--dim)}
.Lwords.five .Lw h4{font-size:33px}

/* 화면 테두리 안과 밖 */
.Lframe{display:grid;grid-template-columns:1.08fr 1fr;gap:44px;flex:1;min-height:0}
.Lscreen{position:relative;border:3px solid var(--line);border-radius:22px;padding:32px 34px;
  display:flex;flex-direction:column;justify-content:center;gap:16px;background:#fff}
.Lscreen::before{content:"";position:absolute;left:24px;right:24px;top:14px;height:5px;border-radius:3px;
  background:var(--line)}
.Loutside{display:flex;flex-direction:column;justify-content:center;gap:16px;padding-left:8px}
.Lq{font-size:21px;line-height:1.45;font-weight:700}
.Lqd{font-size:17.5px;line-height:1.5;color:var(--dim);margin-top:5px}
.Lin{padding-left:26px;position:relative}
.Lin::before{content:"";position:absolute;left:0;top:9px;width:14px;height:14px;border-radius:50%;
  background:var(--grad)}
.Lout{padding-left:26px;position:relative}
.Lout::before{content:"";position:absolute;left:0;top:9px;width:14px;height:14px;border-radius:50%;
  border:3px solid #FF9BB0;background:#fff}
.Loutside .Lq{color:#C2185B}

/* 한 판을 두 색으로 나눈다 */
.Ltone{display:flex;flex-direction:column;flex:1;min-height:0;gap:0}
.Lth{display:grid;grid-template-columns:1fr 1fr;gap:0;flex:none}
.Lth>div{padding:16px 30px;font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.14em}
.Lth>div:first-child{background:linear-gradient(135deg,#FFF1E6,#FDECF3);color:#B4553F;
  border-radius:16px 0 0 0}
.Lth>div:last-child{background:#EEF0F6;color:var(--faint);border-radius:0 16px 0 0}
.Ltb{display:grid;grid-template-columns:1fr 1fr;flex:1;min-height:0}
.Ltb>div{padding:26px 30px;display:flex;flex-direction:column;justify-content:center;gap:14px;
  border-top:1.5px solid var(--line)}
.Ltb>div:first-child{background:linear-gradient(150deg,rgba(255,241,230,.6),rgba(253,236,243,.6))}
.Ltb>div:last-child{background:rgba(238,240,246,.5)}
.Ltb li,.Ltb p{font-size:19.5px;line-height:1.55;list-style:none}
.Ltb li b{display:block;font-weight:800;color:var(--ink)}
.Ltb ul{display:flex;flex-direction:column;gap:20px}

/* 겹치는 영역 */
.Lover{display:grid;grid-template-columns:.9fr 1fr;gap:52px;flex:1;min-height:0;align-items:center}
.Lvenn{position:relative;aspect-ratio:1/.86;width:100%;max-width:430px;margin:0 auto}
.Lvenn i{position:absolute;width:60%;height:60%;border-radius:50%;border:2.5px solid;opacity:.85}
.Lvenn i:nth-child(1){left:0;top:0;border-color:#FF7A1A}
.Lvenn i:nth-child(2){right:0;top:0;border-color:#FF4D6D}
.Lvenn i:nth-child(3){left:0;bottom:0;border-color:#A855F7}
.Lvenn i:nth-child(4){right:0;bottom:0;border-color:#3B82F6}
.Lvenn u{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:26%;height:26%;
  border-radius:50%;background:var(--grad);text-decoration:none;
  box-shadow:0 12px 32px rgba(168,85,247,.28)}

/* 목록에 통과와 막힘 표시 */
.Lmark{display:flex;flex-direction:column;flex:1;min-height:0;justify-content:center;gap:0}
.Lmk{display:grid;grid-template-columns:52px minmax(0,1fr);column-gap:24px;align-items:start;
  padding:19px 0;border-top:1.5px solid var(--line)}
.Lmk:first-of-type{border-top:none}
.Lmk i{width:34px;height:34px;border-radius:50%;display:grid;place-items:center;font-style:normal;
  font-size:17px;font-weight:800;margin-top:2px}
.Lmk.ok i{background:var(--grad);color:#fff}
.Lmk.no i{background:#FFF1F4;color:#FF4D6D;border:2px solid #FFC7D3}
.Lmk h4{font-size:21.5px;font-weight:700;line-height:1.4}
.Lmk p{margin-top:5px;font-size:17.5px;line-height:1.5;color:var(--dim)}
.Lmk.no h4{color:#C2185B}
.Lmark.t5 .Lmk{padding:13px 0}
.Lmark.t5 .Lmk h4{font-size:20px}
.Lmark.t5 .Lmk p{font-size:16.5px;margin-top:4px}
.Lmark.t6 .Lmk{padding:10px 0;grid-template-columns:46px minmax(0,1fr);column-gap:20px}
.Lmark.t6 .Lmk i{width:30px;height:30px;font-size:15px}
.Lmark.t6 .Lmk h4{font-size:19px}
.Lmark.t6 .Lmk p{font-size:16px;margin-top:3px;line-height:1.45}

/* 위와 아래로 나눈다 */
.Lud{display:grid;grid-template-rows:auto 1fr;flex:1;min-height:0;gap:26px}
.Lud.big{grid-template-rows:1fr auto}
.Lud.big>section:first-child{padding:22px 24px}
.Lud .Lfull{flex:1;min-height:0;height:100%}
.Lud>section{background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:26px 32px;
  display:flex;flex-direction:column;justify-content:center;min-height:0}
.Lud>section>b{display:block;font-family:var(--fm);font-size:14.5px;font-weight:700;
  letter-spacing:.16em;color:var(--faint);margin-bottom:12px}
.Lud h4{font-size:23px;font-weight:800;line-height:1.36;margin-bottom:8px}
.Lud p,.Lud li{font-size:19px;line-height:1.58;color:var(--dim);list-style:none}
.Lud ul{display:flex;flex-direction:column;gap:9px}
.Lud>section.hot{border:2px solid transparent;
  background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}

/* 같은 기준을 가리키는 두 화살표 */
.Larr{display:grid;grid-template-columns:1fr .8fr 1fr;align-items:center;gap:34px;flex:1;min-height:0}
.Larrmid{background:#fff;border:2px solid transparent;border-radius:22px;padding:30px 26px;
  background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box;text-align:center}
.Larrmid h4{font-size:24px;font-weight:800;line-height:1.35}
.Larrmid p{margin-top:10px;font-size:18px;line-height:1.55;color:var(--dim)}
.Larrs{display:flex;flex-direction:column;gap:20px}
.Larrs.r{text-align:right}
.Larrs h4{font-size:22px;font-weight:800;line-height:1.35}
.Larrs p{margin-top:10px;font-size:18px;line-height:1.75;color:var(--dim)}
.Larrline{height:3px;background:var(--grad);border-radius:2px;position:relative}
.Larrline::after{content:"";position:absolute;right:-2px;top:-6px;border-left:14px solid #A855F7;
  border-top:7px solid transparent;border-bottom:7px solid transparent}
.Larrs.r .Larrline::after{left:-2px;right:auto;border-left:none;border-right:14px solid #FF7A1A}

/* 가로 막대 견주기 */
.Lbars{display:flex;flex-direction:column;flex:1;min-height:0;justify-content:center;gap:34px}
.Lbr{display:grid;grid-template-columns:190px minmax(0,1fr);column-gap:30px;align-items:center}
.Lbr>b{font-family:var(--fm);font-size:17px;font-weight:700;letter-spacing:.14em;color:var(--faint)}
.Lbrack{display:flex;height:82px;border-radius:16px;overflow:hidden;background:#EEF0F6}
.Lbseg{display:flex;align-items:center;padding:0 26px;font-size:20px;font-weight:800;color:#fff;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.Lbseg.g{background:var(--grad)}
.Lbseg.m{background:#D5D9E4;color:var(--dim)}
.Lbseg.v{background:linear-gradient(135deg,#A855F7,#3B82F6)}
.Lbnote{margin-top:14px;font-size:18.5px;line-height:1.55;color:var(--dim)}
.Lbnote>b{font-weight:800;color:var(--ink)}

/* 실제 수치 막대와 기준선 */
.Lchart{display:grid;grid-template-columns:1.05fr .95fr;gap:52px;flex:1;min-height:0;align-items:center}
.Lplot{position:relative;height:100%;min-height:0;display:flex;align-items:flex-end;gap:12px;
  padding:34px 0 34px}
.Lplot i{flex:1;border-radius:8px 8px 0 0;background:#E4E7EF;display:block}
.Lplot i.hot{background:var(--grad)}
.Lline{position:absolute;left:0;right:0;height:2px}
.Lline span{position:absolute;right:0;top:-26px;font-family:var(--fm);font-size:14px;font-weight:700;
  letter-spacing:.12em}
.Lline.avg{background:repeating-linear-gradient(90deg,#C6CBDA 0 9px,transparent 9px 18px)}
.Lline.avg span{color:var(--faint)}
.Lline.ours{background:repeating-linear-gradient(90deg,#FF4D6D 0 9px,transparent 9px 18px)}
.Lline.ours span{color:#FF4D6D}
.Lplotwrap{display:flex;flex-direction:column;height:100%;min-height:0}
.Lplotx{display:flex;gap:12px;margin-top:10px}
.Lplotx span{flex:1;text-align:center;font-family:var(--fm);font-size:12.5px;font-weight:700;
  letter-spacing:.04em;color:var(--faint)}
.Lplotx span.on{color:#FF4D6D}

/* 표 */
.Ltab{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center}
.Ltab table{width:100%;border-collapse:collapse}
.Ltab th,.Ltab td{padding:16px 18px;text-align:left;border-bottom:1.5px solid var(--line);
  font-size:18.5px;line-height:1.45}
.Ltab th{font-family:var(--fm);font-size:14.5px;font-weight:700;letter-spacing:.14em;color:var(--faint)}
.Ltab td:first-child{font-weight:800;width:34%}
.Ltab .yes{color:#2FB37A;font-weight:800}
.Ltab .no{color:#FF4D6D;font-weight:800}
.Ltab .maybe{color:var(--faint);font-weight:800}
.Ltab th{vertical-align:bottom}
.Ltab th .Lsub{margin-top:7px;font-size:14.5px;letter-spacing:0;font-weight:500;
  font-family:var(--f);text-transform:none}
.Ltab td:not(:first-child){text-align:center;font-size:22px}

/* 시연물을 화면 가득 */
.Lfull{flex:1;min-height:0;border-radius:22px;overflow:hidden;border:1.5px solid var(--line)}
.Lfull iframe{width:100%;height:100%;border:none;display:block}

/* 숫자 하나만 크게 */
.Lone{display:grid;grid-template-columns:1fr 1fr;gap:60px;flex:1;min-height:0;align-items:center}
.Lonenum{font-family:var(--fm);font-size:190px;font-weight:800;line-height:.92;letter-spacing:-.05em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.Lonecap{margin-top:18px;font-size:22px;line-height:1.55;color:var(--dim)}

/* 표지와 마무리 */
.Lcover{position:relative;flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center}
.Lspark{position:absolute;left:0;right:0;bottom:6%;height:44%;opacity:.16;pointer-events:none}
.Lspark svg{width:100%;height:100%;display:block}
.Lbigq{font-size:104px;font-weight:800;line-height:1.22;letter-spacing:-.03em;max-width:1560px}

/* 결과물 하나에 세 가지 표시를 겹친다 */
.Lmarks{display:grid;grid-template-columns:.86fr 1fr;gap:52px;flex:1;min-height:0;align-items:center}
.Ldoc{position:relative;background:#fff;border:1.5px solid var(--line);border-radius:20px;
  padding:30px 32px;display:flex;flex-direction:column;gap:14px}
.Ldoc i{display:block;height:15px;border-radius:7px;background:#EEF0F6}
.Ldoc i:nth-child(3){width:78%}
.Ldoc i:nth-child(6){width:64%}
.Ldoc u{position:absolute;left:20px;right:20px;height:44px;border-radius:12px;text-decoration:none;
  border:2.5px solid}
.Ldoc u:nth-of-type(1){top:20px;border-color:#FF7A1A}
.Ldoc u:nth-of-type(2){top:96px;border-color:#FF4D6D}
.Ldoc u:nth-of-type(3){top:172px;border-color:#A855F7}
.Lmk3{display:flex;flex-direction:column;gap:24px}
.Lmk3 div{padding-left:26px;border-left:4px solid}
.Lmk3 div:nth-child(1){border-color:#FF7A1A}
.Lmk3 div:nth-child(2){border-color:#FF4D6D}
.Lmk3 div:nth-child(3){border-color:#A855F7}
.Lmk3 h4{font-size:24px;font-weight:800;line-height:1.34;margin-bottom:8px}
.Lmk3 p{font-size:18.5px;line-height:1.56;color:var(--dim)}

/* 대비표를 줄이고 글자를 키운다 */
.Lvs{display:grid;grid-template-columns:1fr 92px 1fr;flex:1;min-height:0;align-content:stretch}
.Lvs>.h{padding-bottom:20px;font-family:var(--fm);font-size:16px;font-weight:700;
  letter-spacing:.14em;color:var(--faint)}
.Lvs>.h.r{text-align:right}
.Lvs>.c{padding:26px 0;border-top:1.5px solid var(--line);display:flex;flex-direction:column;
  justify-content:center}
.Lvs>.c.r{text-align:right}
.Lvs>.m{border-top:1.5px solid var(--line);display:grid;place-items:center;
  font-size:24px;color:var(--faint)}
.Lvs h4{font-size:27px;font-weight:800;line-height:1.34;margin-bottom:9px}
.Lvs p{font-size:19.5px;line-height:1.55;color:var(--dim)}
.Lvs>.c.r h4{color:var(--ink)}

/* 두 줄로 접은 격자 */
.Lfold{display:grid;gap:22px;flex:1;min-height:0;align-content:stretch}
.Lfold.f3{grid-template-columns:repeat(3,1fr)}
.Lfold.f4{grid-template-columns:repeat(4,1fr)}
.Lfd{background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:24px 26px;
  display:flex;flex-direction:column;justify-content:center;min-width:0}
.Lfd>b{display:block;font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.16em;
  color:var(--faint);margin-bottom:11px}
.Lfd h4{font-size:22px;font-weight:800;line-height:1.34;margin-bottom:8px}
.Lfd p{font-size:17.5px;line-height:1.52;color:var(--dim)}
.Lfd.hot{border:2px solid transparent;
  background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}
.Lfold.f4 .Lfd h4{font-size:21px}
.Lfold.f4 .Lfd p{font-size:17px}
"""


# ══ 감싸개 ═════════════════════════════════════════════════════════
def frame(html, *blocks, keep_band=True):
    """머리말과 제목과 리드는 그대로 두고 그 아래를 갈아 끼운다.

    덩이를 둘 이상 쌓으면 남는 높이를 나눠 써야 하므로 한 단계 촘촘하게 표를 붙인다.
    """
    body = "".join(blocks)
    if keep_band:
        body += band(html)
    cls = "Lc dense" if len([b for b in blocks if b]) > 1 else "Lc"
    return _reframe(html, f'<div class="{cls}">{body}</div>')


def side(*blocks):
    return f'<div class="Lside">{"".join(blocks)}</div>'


def two(left, right, cls=""):
    return f'<div class="L2{(" " + cls) if cls else ""}">{left}{right}</div>'


def top(fig, below):
    return f'<div class="Ltop">{fig}{below}</div>'


def grid(slots, cls="g2"):
    return f'<div class="Lgrid {cls}">{"".join(slots)}</div>'


# ══ 판 ═════════════════════════════════════════════════════════════
def rows(items):
    """행으로 쌓는다. 라벨과 제목과 설명이 각각 같은 열에 선다."""
    out = "".join(f'<div class="Lrow"><b>{a}</b><div><h4>{b}</h4><p>{c}</p></div></div>'
                  for a, b, c in items)
    lines = len(items) + sum(str(c).count("<br>") for _, _, c in items)
    return f'<div class="Lrows{_density(lines)}">{out}</div>'


def _density(n):
    """줄 수에 맞춰 촘촘함을 한 단계씩 올린다. 설명 안의 줄바꿈도 한 줄로 센다."""
    return "" if n <= 3 else f" t{min(n, 6)}"


def cols(items, n=3, plain=False):
    """칸을 균등하게 나눈다."""
    cl = "plain" if plain else ""
    out = "".join(f'<div class="Lcell {cl}"><b>{a}</b><h4>{b}</h4><p>{c}</p></div>'
                  for a, b, c in items)
    return f'<div class="Lcols c{n}">{out}</div>'


def bignum(items):
    """큰 번호를 앞세운 칸."""
    out = "".join(f'<div class="Lcell plain Lbig"><b>{a}</b><h4>{b}</h4><p>{c}</p></div>'
                  for a, b, c in items)
    return f'<div class="Lcols c{len(items)}">{out}</div>'


def axis(items, left="", right="", cuts=()):
    """가로 축 하나를 긋고 그 위에 지점을 찍는다."""
    ends = (f'<div class="Laxend"><span>{left}</span><s></s><span>{right}</span></div>'
            if left or right else "")
    pts = "".join(f'<div class="Laxpt{" cut" if i in cuts else ""}">'
                  f'<b>{a}</b><h4>{b}</h4><p>{c}</p></div>'
                  for i, (a, b, c) in enumerate(items))
    return (f'<div class="Laxis">{ends}<div class="Laxtrack"></div>'
            f'<div class="Laxpts{_density(len(items))}" '
            f'style="grid-template-columns:repeat({len(items)},1fr)">{pts}</div></div>')


def strip(head, items, tail=""):
    """한 줄로 늘어놓는 목록. 축이 이미 나른 쪽과 견주는 자리에 쓴다."""
    body = "".join(f"<span>{x}</span>" for x in items)
    end = f"<em>{tail}</em>" if tail else ""
    return f'<div class="Lgone"><b>{head}</b>{body}{end}</div>'


def stair(items, here=None):
    """오르는 계단. 서 있는 단을 표시한다."""
    n = len(items)
    out = []
    for i, (a, b, c) in enumerate(items):
        h = 34 + (i + 1) * (100 - 34) / n
        cls = " here" if here == i else ""
        out.append(f'<div class="Lstep{cls}" style="height:{h:.0f}%">'
                   f'<div class="Lbox"><b>{a}</b><h4>{b}</h4><p>{c}</p></div></div>')
    return f'<div class="Lstair">{"".join(out)}</div><div class="Lfloor"></div>'


def spans(rows_, compact=False):
    """길이나 면적으로 두 덩이를 견준다. rows_: [(라벨, 비율, 글, 강조인가, 아래말)]"""
    out = []
    for lab, pct, text, hot, note in rows_:
        out.append(f'<div class="Lsp"><b>{lab}</b><div>'
                   f'<div class="Lsbar {"a" if hot else "b"}" style="width:{pct}%">{text}</div>'
                   f'{f"<div class=Lspn>{note}</div>" if note else ""}</div></div>')
    return f'<div class="Lspan{" compact" if compact else ""}">{"".join(out)}</div>'


def pair(lhead, rhead, pairs, lend="", rend=""):
    """두 목록을 한 줄씩 마주 놓는다. 같은 줄에서 시작한다."""
    head = bool(lhead or rhead)
    out = ([f'<div class="Lph">{lhead}</div><div></div><div class="Lph r">{rhead}</div>']
           if head else [])
    for a, b in pairs:
        out.append(f'<div class="Lpl">{a}</div><div class="Lpm"><i></i></div>'
                   f'<div class="Lpr">{b}</div>')
    if lend or rend:
        out.append(f'<div class="Lpe">{lend}</div><div></div><div class="Lpe r">{rend}</div>')
    return (f'<div class="Lpair" style="grid-template-rows:{"auto " if head else ""}'
            f'repeat({len(pairs)},1fr){" auto" if (lend or rend) else ""}">'
            f'{"".join(out)}</div>')


def twoline(lines, note="", compact=False):
    """위아래 두 줄. 시작점의 차이가 뜻이다. lines: [(라벨, [(글, 켜짐)…])]"""
    out = []
    for lab, nodes in lines:
        nd = "".join(f'<div class="Ltnode{" on" if on else ""}"><i></i><span>{t}</span></div>'
                     for t, on in nodes)
        out.append(f'<div class="Ltl"><b>{lab}</b><div class="Lttrack">{nd}</div></div>')
    tail = f'<div class="Ltnote">{note}</div>' if note else ""
    return f'<div class="Ltwo{" compact" if compact else ""}">{"".join(out)}{tail}</div>'


def quad(xhead, yheads, cells):
    """가로와 세로로 놓아 만든 네 구역. cells: [(제목, 설명, 강조인가)] 네 개."""
    out = [f'<div class="Lqh">{xhead}</div>',
           f'<div class="Lqs">{yheads[0]}</div><div class="Lqs">{yheads[1]}</div>']
    for i, (h, p, hot) in enumerate(cells):
        if i % 2 == 0:
            out.append(f'<div class="Lqs">{yheads[2 + i // 2]}</div>')
        out.append(f'<div class="Lqc{" hot" if hot else ""}"><h4>{h}</h4><p>{p}</p></div>')
    return f'<div class="Lquad">{"".join(out)}</div>'


def words(items):
    """큰 낱말 한 줄과 그 아래 작은 설명."""
    out = "".join(f'<div class="Lw"><h4>{h}</h4><p>{p}</p></div>' for h, p in items)
    cls = " five" if len(items) >= 5 else ""
    return f'<div class="Lwords{cls}">{out}</div>'


def screen_split(inside, outside, ihead="", ohead=""):
    """화면 테두리를 그리고 안과 밖으로 나눈다."""
    ins = "".join(f'<div class="Lin"><div class="Lq">{q}</div><div class="Lqd">{d}</div></div>'
                  for q, d in inside)
    outs = "".join(f'<div class="Lout"><div class="Lq">{q}</div><div class="Lqd">{d}</div></div>'
                   for q, d in outside)
    ih = f'<div class="Lph" style="margin-bottom:6px">{ihead}</div>' if ihead else ""
    oh = f'<div class="Lph" style="margin-bottom:6px">{ohead}</div>' if ohead else ""
    return (f'<div class="Lframe"><div class="Lscreen">{ih}{ins}</div>'
            f'<div class="Loutside">{oh}{outs}</div></div>')


def tone(lhead, rhead, lbody, rbody):
    """한 판을 두 색으로 나눈다."""
    return (f'<div class="Ltone"><div class="Lth"><div>{lhead}</div><div>{rhead}</div></div>'
            f'<div class="Ltb"><div>{lbody}</div><div>{rbody}</div></div></div>')


def overlap(items):
    """네 조건이 모두 겹치는 영역."""
    body = "".join(f'<div class="Lrow"><b>{a}</b><div><h4>{b}</h4><p>{c}</p></div></div>'
                   for a, b, c in items)
    return (f'<div class="Lover"><div class="Lvenn"><i></i><i></i><i></i><i></i><u></u></div>'
            f'<div class="Lrows{_density(len(items))}">{body}</div></div>')


def marks(cols_):
    """목록에 통과와 막힘 표시를 단다. cols_: [(표시, [(질문, 설명)…])]"""
    out = []
    for kind, qs in cols_:
        sym = "&check;" if kind == "ok" else "&times;"
        for q, d in qs:
            out.append(f'<div class="Lmk {kind}"><i>{sym}</i><div><h4>{q}</h4><p>{d}</p></div></div>')
    return f'<div class="Lmark{_density(len(out))}">{"".join(out)}</div>'


def updown(a, b, hot_b=True, big=False):
    """위와 아래로 나눈다. a, b: (라벨, 안쪽 html). big을 주면 위 칸이 높이를 갖는다."""
    return (f'<div class="Lud{" big" if big else ""}">'
            f'<section><b>{a[0]}</b>{a[1]}</section>'
            f'<section{" class=hot" if hot_b else ""}><b>{b[0]}</b>{b[1]}</section></div>')


def arrows(left, mid, right):
    """같은 기준을 가리키는 두 화살표."""
    return (f'<div class="Larr"><div class="Larrs"><h4>{left[0]}</h4><p>{left[1]}</p>'
            f'<div class="Larrline"></div></div>'
            f'<div class="Larrmid"><h4>{mid[0]}</h4><p>{mid[1]}</p></div>'
            f'<div class="Larrs r"><h4>{right[0]}</h4><p>{right[1]}</p>'
            f'<div class="Larrline"></div></div></div>')


def bars(rows_):
    """가로 막대로 견준다. rows_: [(라벨, [(몫, 글, 색)], 아래말)]"""
    out = []
    for lab, segs, note in rows_:
        tr = "".join(f'<div class="Lbseg {c}" style="flex:{f}">{t}</div>' for f, t, c in segs)
        out.append(f'<div class="Lbr"><b>{lab}</b><div><div class="Lbrack">{tr}</div>'
                   f'{f"<div class=Lbnote>{note}</div>" if note else ""}</div></div>')
    return f'<div class="Lbars">{"".join(out)}</div>'


def chart(values, hot, lines, aside, ticks=()):
    """실제 수치 막대와 기준선. values: 높이 비율 목록, lines: [(클래스, 위치%, 이름)]"""
    bs = "".join(f'<i class="{"hot" if i in hot else ""}" style="height:{v}%"></i>'
                 for i, v in enumerate(values))
    ln = "".join(f'<div class="Lline {c}" style="bottom:{p}%"><span>{n}</span></div>'
                 for c, p, n in lines)
    xs = ("".join(f'<span class="{"on" if i in hot else ""}">{t}</span>'
                  for i, t in enumerate(ticks))) if ticks else ""
    plot = (f'<div class="Lplotwrap"><div class="Lplot">{bs}{ln}</div>'
            f'{f"<div class=Lplotx>{xs}</div>" if xs else ""}</div>')
    return f'<div class="Lchart">{plot}{aside}</div>'


def table(head, body):
    """표 하나. head: 열 이름 목록, body: 줄 목록."""
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in body)
    return f'<div class="Ltab"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def full(iframe):
    return f'<div class="Lfull">{iframe}</div>'


def onenum(num, cap, aside):
    return (f'<div class="Lone"><div><div class="Lonenum">{num}</div>'
            f'<div class="Lonecap">{cap}</div></div>{aside}</div>')


def versus_rows(lhead, rhead, rows_):
    """대비표를 줄이고 글자를 키운다."""
    out = [f'<div class="h">{lhead}</div><div></div><div class="h r">{rhead}</div>']
    for lh, lp, rh, rp in rows_:
        out.append(f'<div class="c"><h4>{lh}</h4><p>{lp}</p></div>'
                   f'<div class="m">&ne;</div>'
                   f'<div class="c r"><h4>{rh}</h4><p>{rp}</p></div>')
    return (f'<div class="Lvs" style="grid-template-rows:auto repeat({len(rows_)},1fr)">'
            f'{"".join(out)}</div>')


def fold(items, per=3, hot=None):
    """n개를 여러 줄로 접어 글자 크기를 되찾는다."""
    out = "".join(f'<div class="Lfd{" hot" if hot == i else ""}"><b>{a}</b><h4>{b}</h4><p>{c}</p></div>'
                  for i, (a, b, c) in enumerate(items))
    return f'<div class="Lfold f{per}">{out}</div>'


def doc_marks(items):
    """결과물 하나를 놓고 세 방식이 어디를 보는지 표시를 겹친다."""
    body = "".join(f'<div><h4>{b}</h4><p>{c}</p></div>' for a, b, c in items)
    return ('<div class="Lmarks"><div class="Ldoc">'
            + "<i></i>" * 7 + "<u></u><u></u><u></u></div>"
            + f'<div class="Lmk3">{body}</div></div>')


def spark(values):
    """옅은 선 하나. 표지와 마지막 장의 배경으로 깐다."""
    n = len(values)
    d = " ".join(f'{"M" if i == 0 else "L"}{i * 1000 / (n - 1):.1f} {100 - v:.1f}'
                 for i, v in enumerate(values))
    return ('<div class="Lspark"><svg viewBox="0 0 1000 100" preserveAspectRatio="none">'
            f'<path d="{d}" fill="none" stroke="#A855F7" stroke-width="2"/>'
            f'<path d="{d} L1000 100 L0 100Z" fill="#A855F7" opacity=".18"/></svg></div>')
