#!/usr/bin/env python3
"""덱의 바탕. 색과 CSS, 공통 가구, 문장 검사기와 교정 게이트를 담는다.

화면에 보이는 글은 여기에 두지 않는다. 장 구성과 문장은 build_deck.py 에 있다.
색을 바꾸려면 아래 :root 의 --c1 부터 --c4 와 오로라 네 개의 rgba 만 고치면 된다.
"""
import base64, re, sys, pathlib, hashlib, json

ROOT = pathlib.Path(__file__).parent
TOTAL = 26

def img64(path):
    data = (ROOT / path).read_bytes()
    ext = pathlib.Path(path).suffix.lstrip(".")
    mime = "image/svg+xml" if ext == "svg" else f"image/{ext}"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"

OSOMA = img64("assets/osoma.svg")

# 제목의 강조 낱말과 카드 테두리에 쓰는 그라데이션. 로고 파랑에서 청록으로 간다
GRAD_STOPS = [("0", "#1B6FA8"), (".34", "#3395DA"), (".68", "#35B4C7"), ("1", "#6FD3C7")]

def grad_svg(gid):
    """SVG 안에서 쓰는 같은 그라데이션. 표지의 신호 그림과 아이콘이 가져다 쓴다."""
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in GRAD_STOPS)
    return f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient>'


# ── 덱 CSS ──
CSS = """
:root{
  --s:1;
  --bg:#FFFFFF; --card:#FFFFFF;
  --ink:#1F2430; --dim:#6A7180; --faint:#9BA1AE;
  --line:#E9EBF1; --line2:#F1F3F7;
  --c1:#1B6FA8; --c2:#3395DA; --c3:#35B4C7; --c4:#6FD3C7;
  --grad:linear-gradient(100deg,var(--c1) 0%,var(--c2) 34%,var(--c3) 68%,var(--c4) 100%);
  --f:'Pretendard Variable',Pretendard,-apple-system,sans-serif;
  --fm:'JetBrains Mono',ui-monospace,monospace;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-snap-type:y mandatory}
body{background:#EDEFF4;font-family:var(--f);color:var(--ink);word-break:keep-all;overflow-wrap:break-word}
.lead,.pt p,.ptxt,.rcap,.lcap,.mbub,.stepband,.impband,.tm p,.tool p,.job p,.mnote{text-wrap:pretty}
.vp{height:100dvh;display:flex;align-items:center;justify-content:center;scroll-snap-align:start;overflow:hidden}
section.slide{width:1920px;height:1080px;position:relative;flex:none;transform:scale(var(--s));background:var(--bg);overflow:hidden;box-shadow:0 24px 80px rgba(30,40,60,.18)}
.fg{position:relative;height:100%;padding:100px 120px;display:flex;flex-direction:column;z-index:2}

/* 오로라 글로우 */
.aur{position:absolute;border-radius:50%;pointer-events:none;z-index:0}
.aur.a1{width:920px;height:920px;right:-260px;top:-330px;background:radial-gradient(circle,rgba(27,111,168,.14),transparent 62%)}
.aur.a2{width:820px;height:820px;right:180px;top:60px;background:radial-gradient(circle,rgba(53,180,199,.13),transparent 62%)}
.aur.a3{width:760px;height:760px;left:-240px;bottom:-300px;background:radial-gradient(circle,rgba(51,149,218,.12),transparent 62%)}
.aur.a4{width:640px;height:640px;left:340px;bottom:-260px;background:radial-gradient(circle,rgba(111,211,199,.10),transparent 62%)}

/* 공통 가구 */
.brandbar{position:absolute;top:56px;right:72px;display:flex;align-items:center;gap:22px;z-index:5}
.brandbar img{height:40px}
.brandbar .div{width:1px;height:26px;background:var(--line)}
.brandbar img.osoma{height:30px;width:auto}
.meta-tl{position:absolute;top:64px;left:120px;font-family:var(--fm);font-size:17px;letter-spacing:.24em;color:var(--faint);z-index:5}
.pgno{position:absolute;right:72px;bottom:52px;font-family:var(--fm);font-size:17px;color:var(--faint);z-index:5}
.credit{position:absolute;left:120px;bottom:52px;font-family:var(--fm);font-size:15px;letter-spacing:.14em;color:var(--faint);z-index:5}

/* 그라데이션 장치 */
.gt{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent}
mark{background:var(--grad);color:#fff;padding:2px 20px;border-radius:12px;font-weight:800;box-decoration-break:clone;-webkit-box-decoration-break:clone}

/* 텍스트 계층 */
.kicker{font-family:var(--fm);font-size:21px;font-weight:600;letter-spacing:.26em;margin-bottom:34px}
.kicker .k1{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.kicker .k2{color:var(--faint)}
h2.head{font-size:68px;font-weight:800;letter-spacing:-.03em;line-height:1.22}
.lead{font-size:29px;line-height:1.6;color:var(--dim);font-weight:400;margin-top:22px}

/* 표지 */
.cover .fg{justify-content:flex-end;padding-bottom:150px;gap:44px}
.cover h1{font-size:128px;font-weight:800;letter-spacing:-.04em;line-height:1.16}
.cover .sub{font-size:30px;color:var(--dim);font-weight:500}
.cover .mchips{display:flex;font-family:var(--fm);font-size:18px;letter-spacing:.18em;color:var(--dim)}
.cover .mchips span{padding:0 34px;border-left:1px solid var(--line)}
.cover .mchips span:first-child{padding-left:0;border-left:none}
.cover .mchips b{font-weight:700;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.signal{position:absolute;right:150px;top:110px;width:660px;height:660px;z-index:1}
.signal .rip{opacity:0}
.signal .ring{transform-origin:330px 330px;animation:pulse 4.2s ease-in-out infinite}
.signal .ring:nth-of-type(2){animation-delay:.6s}
.signal .ring:nth-of-type(3){animation-delay:1.2s}
.signal .ring:nth-of-type(4){animation-delay:1.8s}
.signal .rip{transform-origin:330px 330px;animation:rip 3.6s ease-out infinite}
.signal .rip.r2{animation-delay:1.8s}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.09)}}
@keyframes rip{0%{transform:scale(.24);opacity:0}10%{opacity:.95}100%{transform:scale(1.12);opacity:0}}

/* 목차 */
.toc{display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px;margin-top:56px;align-items:stretch}
.tocol{background:linear-gradient(150deg,#EEF6FC 0%,#E9F4FA 45%,#E9F6F6 75%,#EDF8F5 100%);border:1.5px solid #DFEAF2;border-radius:24px;padding:36px 38px;box-shadow:0 16px 44px rgba(40,50,80,.07)}
.tocol h3{font-size:25px;font-weight:800;margin:0 0 22px}
.tocol h3 b{font-family:var(--fm);font-size:18px;font-weight:700;letter-spacing:.12em;margin-right:14px;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.tocol li{list-style:none;display:flex;gap:16px;align-items:baseline;font-size:21.5px;color:var(--dim);font-weight:500;padding:11px 0;border-top:1px solid var(--line2)}
.tocol li b{font-family:var(--fm);font-size:16px;font-weight:700;color:var(--faint)}
.promise{display:flex;gap:14px;margin-top:auto}
.promise span{padding:12px 28px;border-radius:999px;border:1.5px solid var(--line);font-size:21px;font-weight:700;color:var(--dim)}

/* 파트 표지 */
.pdiv .fg{justify-content:center;gap:44px}
.pdiv .bignum{position:absolute;right:40px;bottom:-70px;font-family:var(--fm);font-size:660px;font-weight:700;line-height:1;letter-spacing:-.05em;z-index:1;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;opacity:.9}
.pdiv .pno{font-family:var(--fm);font-size:22px;font-weight:700;letter-spacing:.3em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.pdiv h2{font-size:112px;font-weight:800;letter-spacing:-.035em;line-height:1.1}
.pdiv ul{list-style:none;display:flex;flex-direction:column;margin-top:16px;max-width:1000px}
.pdiv li{display:flex;align-items:center;gap:32px;font-size:30px;color:var(--dim);font-weight:500;padding:24px 0;border-top:1px solid var(--line)}
.pdiv li:last-child{border-bottom:1px solid var(--line)}
.pdiv li b{font-family:var(--fm);font-size:20px;font-weight:700;letter-spacing:.1em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.rail{position:absolute;left:120px;bottom:110px;display:flex;gap:12px;z-index:5}
.rail div{display:flex;flex-direction:column;gap:12px}
.rail i{display:block;width:180px;height:4px;border-radius:2px;background:var(--line)}
.rail .on i{background:var(--grad)}
.rail span{font-family:var(--fm);font-size:15px;letter-spacing:.06em;color:var(--faint)}
.rail .on span{color:var(--ink);font-weight:600}

/* 설명형 split */
.split .cols{display:grid;grid-template-columns:1fr 760px;gap:84px;flex:1;min-height:0;margin-top:14px}
.points{display:flex;flex-direction:column;margin-top:34px}
.pt{display:flex;gap:30px;padding:28px 0;border-top:1px solid var(--line)}
.pt b{font-family:var(--fm);font-size:19px;font-weight:700;letter-spacing:.1em;padding-top:6px;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.pt h4{font-size:27px;font-weight:700;margin-bottom:9px;letter-spacing:-.01em}
.pt p{font-size:22px;line-height:1.6;color:var(--dim)}
.rcol{display:flex;flex-direction:column;justify-content:center;gap:18px}
.rcap{font-size:19px;line-height:1.55;color:var(--faint);text-align:center;padding:0 10px}

/* 메신저 챗 목업 (카카오톡형: 프로필 아바타 + 말풍선) */
.mchat{background:linear-gradient(160deg,#EFF6FC,#EAF5F8 55%,#ECF7F4);border:1.5px solid #DFEAF2;border-radius:26px;padding:28px;box-shadow:0 20px 56px rgba(40,50,80,.08)}
.mhead{display:flex;align-items:center;gap:12px;margin-bottom:8px;padding-bottom:16px;border-bottom:1.5px solid rgba(110,120,150,.14)}
.mhead .mava{width:44px;height:44px}
.mhead b{font-size:19px;font-weight:800}
.mrow{display:flex;gap:14px;margin-top:18px}
.mrow.user{justify-content:flex-end}
.mava{width:52px;height:52px;border-radius:50%;background:#fff;border:1.5px solid var(--line);overflow:hidden;flex:none;align-self:flex-start}
.mava img{width:100%;height:100%;object-fit:cover;display:block}
.mcol{display:flex;flex-direction:column;gap:7px;max-width:80%}
.mname{font-size:15px;font-weight:700;color:var(--dim)}
.mbub{background:#fff;border-radius:4px 18px 18px 18px;padding:14px 19px;font-size:19px;line-height:1.55;color:var(--ink);box-shadow:0 3px 10px rgba(40,50,80,.07)}
.mrow.user .mbub{background:linear-gradient(120deg,#E4F2FB,#DFF3F0);border-radius:18px 4px 18px 18px;font-weight:600;max-width:80%}
.mnote{margin-top:18px;padding-top:14px;border-top:1.5px dashed rgba(110,120,150,.22);font-size:17.5px;line-height:1.5;color:var(--dim)}

/* s4 이어쓰기 시뮬레이션 */
.simbox{background:var(--card);border:1.5px solid var(--line);border-radius:26px;padding:38px 40px;box-shadow:0 20px 56px rgba(40,50,80,.08)}
.simlabel{font-family:var(--fm);font-size:15px;letter-spacing:.2em;color:var(--faint);margin-bottom:18px}
.simsent{min-height:120px;font-size:34px;font-weight:700;line-height:1.5;letter-spacing:-.01em}
.simsent .cursor{display:inline-block;width:4px;height:34px;background:var(--c3);vertical-align:-4px;margin-left:6px;border-radius:2px}
.cands{margin-top:26px;border-top:1px solid var(--line2);padding-top:24px;min-height:220px}
.cands .ct{font-family:var(--fm);font-size:15px;letter-spacing:.2em;color:var(--faint);margin-bottom:16px}
.cand{display:grid;grid-template-columns:150px 1fr 74px;align-items:center;gap:18px;padding:9px 0}
.cand .w{font-size:23px;font-weight:700}
.cand .track{height:14px;border-radius:7px;background:var(--line2);overflow:hidden}
.cand .fill{display:block;height:100%;border-radius:7px;background:var(--grad)}
.cand .pc{font-family:var(--fm);font-size:17px;color:var(--dim);text-align:right}
.cand.top .w{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}

/* s5 검토 카드 */
.warncard{background:var(--card);border:1.5px solid var(--line);border-radius:24px;padding:30px 34px;box-shadow:0 16px 44px rgba(40,50,80,.07)}
.warncard .wt{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.18em;margin-bottom:14px;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.warncard ul{list-style:none}
.warncard li{display:flex;gap:14px;align-items:baseline;font-size:21px;color:var(--dim);padding:9px 0;border-top:1px solid var(--line2)}
.warncard li b{font-family:var(--fm);font-size:15px;color:var(--faint)}

/* s6 비교 토글 (메신저 카드 2장) */
.cmpwrap{display:flex;flex-direction:column;gap:20px}
.cmpwrap .mchat{padding:22px 26px;transition:transform .35s,opacity .35s}
.cmpwrap .mchat .mrow{margin-top:14px}
.cmpwrap .mbub{font-size:18.5px;padding:12px 17px}
.cmpwrap .mava{width:46px;height:46px}
.wtag{display:inline-flex;font-family:var(--fm);font-size:13.5px;font-weight:700;letter-spacing:.14em;color:var(--dim);
  background:#fff;border:1.5px solid var(--line);border-radius:999px;padding:7px 16px}
.mchat.hot{border:2px solid transparent;
  background:linear-gradient(160deg,#EFF6FC,#EAF5F8 55%,#ECF7F4) padding-box,var(--grad) border-box}
.mchat.hot .wtag{color:#1B6FA8;border-color:#CFE6F5}
.cmpwrap.on .mchat.cold{opacity:.35;transform:scale(.97)}
.cmpwrap.on .mchat.hot{transform:scale(1.03)}

/* s7 읽기/그리기 패널 */
.duo{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.dpanel{background:linear-gradient(150deg,#EEF6FC 0%,#E9F4FA 45%,#E9F6F6 75%,#EDF8F5 100%);border:1.5px solid #DFEAF2;border-radius:24px;padding:28px;box-shadow:0 16px 44px rgba(40,50,80,.07)}
.dpanel .dt{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.2em;margin:0 0 18px;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.scene{height:190px;border-radius:16px;position:relative;overflow:hidden;background:linear-gradient(180deg,#DCEFFB 0%,#E8F2F8 70%)}
.scene .sun{position:absolute;right:34px;top:26px;width:54px;height:54px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#6FD3C7,#3395DA)}
.scene .hill1{position:absolute;left:-40px;bottom:-64px;width:280px;height:160px;border-radius:50%;background:#7FB98A}
.scene .hill2{position:absolute;right:-60px;bottom:-84px;width:340px;height:180px;border-radius:50%;background:#5E9E6E}
.scene .box{position:absolute;left:120px;bottom:26px;width:120px;height:64px;border-radius:10px;background:#fff;border:2px solid #E3E7DD}
.scene .box::before{content:"";position:absolute;left:12px;top:12px;right:12px;height:10px;border-radius:5px;background:#3395DA}
.dpanel .dtxt{margin-top:16px;font-size:19px;line-height:1.6;color:var(--dim);border:1.5px dashed var(--line);border-radius:14px;padding:14px 18px}
.darrow{text-align:center;font-family:var(--fm);font-size:15px;letter-spacing:.16em;color:var(--faint);padding:6px 0}

/* s10 데스크톱 앱 목업 */
.deskwrap{position:relative;width:100%;border-radius:28px;padding:2px;background:var(--grad);box-shadow:0 26px 70px rgba(120,80,220,.14)}
.desk{background:var(--card);border-radius:26px;overflow:hidden}
.desk .bar{display:flex;align-items:center;gap:9px;padding:16px 24px;border-bottom:1px solid var(--line2)}
.desk .bar i{width:12px;height:12px;border-radius:50%;background:#E4E7EE}
.desk .bar span{margin-left:10px;font-family:var(--fm);font-size:14.5px;color:var(--faint);letter-spacing:.1em}
.desk .body{display:grid;grid-template-columns:210px 1fr;min-height:430px}
.desk .side{border-right:1px solid var(--line2);padding:20px 18px;background:#FAFBFD}
.desk .side .fi{font-size:16.5px;color:var(--dim);padding:9px 12px;border-radius:9px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.desk .side .fi.on{background:#F0ECFB;color:var(--ink);font-weight:700}
.desk .doc{padding:26px 30px;font-size:18.5px;line-height:1.75;color:var(--dim)}
.desk .doc .hlt{background:#EAF4FC;border-bottom:2px solid var(--c1);color:var(--ink);padding:1px 4px;border-radius:4px}
.desk .doc .aiedit{margin-top:18px;border-left:3px solid transparent;border-image:linear-gradient(180deg,var(--c1),var(--c3)) 1;padding-left:18px;color:var(--dim)}
.desk .doc .aiedit .tag{display:block;font-family:var(--fm);font-size:13px;letter-spacing:.16em;font-weight:700;margin-bottom:6px;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}

/* s11 자율 실행 로그 창 */
.termwrap{border-radius:28px;padding:2px;background:var(--grad);box-shadow:0 26px 70px rgba(120,80,220,.14)}
.term{background:#232732;border-radius:26px;overflow:hidden}
.term .bar{display:flex;align-items:center;gap:9px;padding:16px 24px;border-bottom:1px solid rgba(255,255,255,.08)}
.term .bar i{width:12px;height:12px;border-radius:50%;background:#3A4050}
.term .bar span{margin-left:10px;font-family:var(--fm);font-size:14.5px;color:#8B93A6;letter-spacing:.1em}
.term .tbody{padding:28px 32px;font-family:var(--fm);font-size:18.5px;line-height:2.1;color:#C6CCDA}
.term .cmd{color:#fff;font-weight:600}
.term .cmd b{font-weight:700;margin-right:12px;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.term .ok i{font-style:normal;color:#6EE7A0;margin-right:12px}
.term .fin{color:#fff;font-weight:600;margin-top:8px}
.term .fin i{font-style:normal;margin-right:12px;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}

/* s12 세 방식 비교 표 */
.trio{display:grid;grid-template-columns:230px repeat(3,1fr);gap:16px;align-items:stretch}
.trio .thead{border-radius:18px;padding:24px 26px;text-align:center;font-size:23.5px;font-weight:800;
  background:linear-gradient(150deg,#EEF6FC,#E9F4FA 45%,#E9F6F6 75%,#EDF8F5);border:1.5px solid #DFEAF2}
.trio .thead small{display:block;font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.14em;margin-bottom:8px;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.trio .tlabel{display:flex;align-items:center;justify-content:flex-end;padding-right:12px;font-size:19.5px;font-weight:700;color:var(--dim);text-align:right}
.trio .tcell{background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:24px 28px;font-size:21px;line-height:1.5;
  display:flex;align-items:center;justify-content:center;text-align:center;box-shadow:0 10px 30px rgba(40,50,80,.05)}

/* s13 타임라인 (텍스트 위아래 교차) */
.tl{display:grid;grid-template-columns:repeat(9,1fr);gap:14px}
.tm{position:relative;height:400px;transition:opacity .3s,transform .3s}
.tm::before{content:"";position:absolute;top:calc(50% - 1.5px);left:calc(50% + 34px);right:calc(-50% + 34px);height:3px;background:linear-gradient(90deg,#7CC0EA,#6FD3C7)}
.tm:last-child::before{display:none}
.tm .mo{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:54px;height:54px;border-radius:50%;display:grid;place-items:center;
  background:#fff;border:2.5px solid #BFE2F2;font-family:var(--fm);font-size:19px;font-weight:700;color:var(--dim);transition:all .3s}
.tm .tick{position:absolute;left:calc(50% - 1px);width:2px;height:18px;background:#CFE6F5}
.tm.up .tick{bottom:calc(50% + 28px)}
.tm.dn .tick{top:calc(50% + 28px)}
.tm p{position:absolute;left:-16px;right:-16px;text-align:center;font-size:19px;line-height:1.5;color:var(--dim);word-break:keep-all}
.tm.up p{bottom:calc(50% + 54px)}
.tm.dn p{top:calc(50% + 54px)}
.tm .pbadge{position:absolute;top:calc(50% - 13px);left:calc(50% + 36px);font-family:var(--fm);font-size:13px;font-weight:700;letter-spacing:.1em;
  color:#1B6FA8;background:#EAF4FC;border:1.5px solid #CFE6F5;border-radius:999px;padding:4px 11px;white-space:nowrap}
.tl.focus .tm{opacity:.28}
.tl.focus .tm.on{opacity:1;transform:translateY(-6px)}
.tl.focus .tm.on .mo{background:var(--grad);color:#fff;border-color:transparent;box-shadow:0 10px 26px rgba(40,120,180,.32)}
.tl.focus .tm.on p{color:var(--ink);font-weight:700}

/* s14, s15 종이 카드 스택과 목록 */
.pstack{display:flex;flex-direction:column;gap:18px}
.pstack .paper{min-height:0;padding:24px 32px}
/* s15 풀블리드 포토 카드 */
.photocard{position:relative;border-radius:22px;overflow:hidden;min-height:308px;display:flex;align-items:flex-end;box-shadow:0 16px 44px rgba(40,50,80,.16)}
.photocard img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.photocard .scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,18,28,0) 30%,rgba(15,18,28,.86))}
.photocard .ptext{position:relative;padding:24px 30px;z-index:2}
.photocard .ptag2{font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.18em;color:rgba(255,255,255,.85)}
.photocard .ptext p{margin-top:9px;font-size:21px;line-height:1.55;color:rgba(255,255,255,.97);text-wrap:pretty}
.photocard.hot::after{content:"";position:absolute;inset:0;border-radius:22px;border:3px solid transparent;
  background:var(--grad) border-box;-webkit-mask:linear-gradient(#fff 0 0) padding-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;z-index:3;pointer-events:none}

/* s21 방식 요약 카드 */
.vers{display:grid;grid-template-columns:repeat(3,1fr);gap:30px;align-items:stretch}
.vcard{border-radius:24px;padding:38px 40px;background:linear-gradient(150deg,#EEF6FC,#E9F4FA 45%,#E9F6F6 75%,#EDF8F5);
  border:1.5px solid #DFEAF2;box-shadow:0 16px 44px rgba(40,50,80,.07)}
.vcard small{display:block;font-family:var(--fm);font-size:14.5px;font-weight:700;letter-spacing:.16em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.vcard h4{margin-top:10px;font-size:27px;font-weight:800}
.vcard p{margin-top:12px;font-size:20px;line-height:1.6;color:var(--dim);text-wrap:pretty}
.paper .plist{list-style:none;margin-top:2px}
.paper .plist li{display:flex;gap:16px;align-items:baseline;font-size:21px;color:var(--dim);padding:9px 0;border-top:1px solid var(--line2)}
.paper .plist li:first-child{border-top:none}
.paper .plist li b{font-family:var(--fm);font-size:15px;color:var(--faint);flex:none}
.paper.after .plist li{color:var(--ink)}

/* s17 자산 카드 (임팩트) */
.imp .fg{align-items:center;text-align:center}
.imp .ictl{align-self:center}
.assets{display:grid;grid-template-columns:repeat(3,1fr);gap:34px;align-items:stretch;width:100%;margin-top:56px}
.acard{background:#fff;border:2px solid var(--line);border-radius:26px;padding:46px 44px;text-align:center;
  box-shadow:0 16px 44px rgba(40,50,80,.07);transition:opacity .35s,transform .35s;opacity:.32}
.acard .atag{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.22em;color:var(--faint)}
.acard h3{margin-top:14px;font-size:46px;font-weight:800;letter-spacing:-.02em}
.acard p{margin-top:14px;font-size:20.5px;line-height:1.55;color:var(--dim)}
.acard.on{opacity:1;transform:translateY(-6px);border-color:transparent;
  background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box;box-shadow:0 24px 60px rgba(120,80,220,.16)}
.acard.on h3{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.impband{width:100%;margin-top:44px;border-radius:20px;padding:24px 34px;font-size:21.5px;color:var(--dim);line-height:1.6;
  background:linear-gradient(150deg,#EEF6FC,#E9F6F6 70%,#EDF8F5);border:1.5px solid #DFEAF2}
.impband strong{color:var(--ink)}

/* s18 작업 후보 그리드 */
.jobs{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;align-items:stretch}
.job{background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:24px 30px;box-shadow:0 10px 30px rgba(40,50,80,.05)}
.job b{font-family:var(--fm);font-size:16px;font-weight:700;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.job h4{margin-top:7px;font-size:23.5px;font-weight:800}
.job p{margin-top:6px;font-size:18px;color:var(--dim);line-height:1.5}

/* s19 폰 캡처와 기획 초안 */
.scen{display:flex;gap:30px;align-items:center}
.scen .phone{width:266px;flex:none}
.scen .bezel{border-radius:38px;border:8px solid #232732;overflow:hidden;height:548px;background:#fff;box-shadow:0 20px 52px rgba(30,40,60,.2)}
.scen .bezel img{width:100%;display:block}
.scen .plabel{margin-top:14px;text-align:center;font-size:17px;font-weight:700;color:var(--dim)}
.scen .paper{flex:1;min-height:0;padding:30px 36px}

/* 인터랙션 버튼 */
.ictl{display:inline-flex;align-items:center;gap:10px;align-self:flex-start;margin-top:18px;padding:13px 30px;border-radius:999px;border:none;cursor:pointer;
  font-family:var(--f);font-size:19px;font-weight:700;color:#fff;background:var(--grad);box-shadow:0 8px 24px rgba(168,85,247,.28)}
.ictl:active{transform:translateY(1px)}

/* ── 보강 장(추가 설명 슬라이드) 컴포넌트: 레이아웃 카탈로그 승계 ── */
.vcen{flex:1;display:flex;flex-direction:column;justify-content:center}
.lcap{font-size:18px;line-height:1.55;color:var(--faint);margin-top:20px}
.suptag{font-family:var(--fm);font-size:15px;letter-spacing:.18em;color:var(--faint);margin-left:18px}
/* 단계 플로우 */
.steps{display:flex;align-items:stretch;gap:0}
.stepn{flex:1;position:relative;padding:0 18px}
.stepn::before{content:"";position:absolute;top:33px;left:calc(50% + 44px);right:calc(-50% + 44px);height:3px;background:linear-gradient(90deg,#7CC0EA,#6FD3C7)}
.stepn:last-child::before{display:none}
.stepn b{display:grid;place-items:center;width:66px;height:66px;margin:0 auto;border-radius:50%;background:var(--grad);color:#fff;
  font-family:var(--fm);font-size:24px;font-weight:700;box-shadow:0 10px 26px rgba(40,120,180,.3)}
.stepn h4{margin-top:20px;text-align:center;font-size:24px;font-weight:800}
.stepn p{margin-top:10px;text-align:center;font-size:18.5px;line-height:1.55;color:var(--dim)}
.stepband{margin-top:64px;border-radius:20px;padding:26px 34px;font-size:21px;color:var(--dim);line-height:1.6;
  background:linear-gradient(150deg,#EEF6FC,#E9F6F6 70%,#EDF8F5);border:1.5px solid #DFEAF2}
.stepband strong{color:var(--ink)}
/* 문서 대비 */
.ba{display:grid;grid-template-columns:1fr 90px 1fr;align-items:center}
.paper{background:#fff;border:1.5px solid var(--line);border-radius:22px;padding:40px 44px;box-shadow:0 16px 44px rgba(40,50,80,.08);min-height:300px}
.paper .ptag{font-family:var(--fm);font-size:14.5px;font-weight:700;letter-spacing:.16em;color:var(--faint);margin-bottom:20px}
.paper.after .ptag{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.paper .ptxt{font-size:24px;line-height:1.85;color:var(--dim)}
.paper.after{border:2px solid transparent;background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}
.paper.after .ptxt{color:var(--ink)}
.paper .ptxt em{font-style:normal;background:linear-gradient(120deg,#E4F2FB,#DFF3F0);border-radius:6px;padding:1px 6px;font-weight:700}
.baarrow{display:grid;place-items:center}
.baarrow span{width:58px;height:58px;border-radius:50%;background:var(--grad);display:grid;place-items:center;box-shadow:0 10px 26px rgba(40,120,180,.32)}
.baarrow svg{width:26px;height:26px;stroke:#fff;stroke-width:2.6;fill:none}
.baarrow .qb{color:#fff;font-family:var(--fm);font-size:23px;font-weight:700}
/* 카드 그리드 */
.tools{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;align-items:stretch}
.tool{display:flex;gap:26px;align-items:center;background:#fff;border:1.5px solid var(--line);border-radius:24px;padding:38px 36px;
  min-height:190px;box-shadow:0 14px 40px rgba(40,50,80,.07)}
.tool .tno{flex:none;font-family:var(--fm);font-size:26px;font-weight:700;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.tool h4{font-size:24.5px;font-weight:800}
.tool p{margin-top:9px;font-size:18.5px;color:var(--dim);line-height:1.5}
/* 갤러리 모자이크 */
.mosaic{display:grid;grid-template-columns:1.5fr 1fr 1fr;grid-template-rows:252px 252px;gap:20px;margin-top:26px}
.mo{border-radius:20px;overflow:hidden;position:relative;box-shadow:0 14px 40px rgba(40,50,80,.12)}
.mo img{width:100%;height:100%;object-fit:cover;display:block}
.mo.tall{grid-row:span 2}
.mocap{display:flex;gap:26px;margin-top:16px}
.mocap span{flex:1;font-size:17.5px;color:var(--dim);line-height:1.5}
.mocap b{font-weight:700;color:var(--ink)}

/* 인쇄 */
@media print{
  html,body{width:1920px;background:#fff}
  *{animation:none !important;transition:none !important}
  body{scroll-snap-type:none !important}
  .vp{height:auto;display:block;overflow:visible;page-break-after:always;break-after:page}
  .vp.last{page-break-after:auto;break-after:auto}
  /* 크롬 인쇄에서 그라데이션 글자(background-clip:text) 둘레에 얇은 테두리가 찍혀, 인쇄에서는 단색으로 바꾼다 */
  .gt,.kicker .k1,.cover .mchips b,.ax-cover .mchips b,.axstep b,.figrow b,.paper.after .prole,.paper.after .ptag,
  .qacard + .qacard .qlabel,.qcell .qbar span em,.qcell .qbody .qrun i,.term .cmd b,.term .fin i,
  .stepn.hot h4,.vs .vh.r,.baflow.after .bfl,.acard.on h3,.cand.top .w{
    background:none !important;-webkit-text-fill-color:#2F86C4 !important;color:#2F86C4 !important}
  section.slide{transform:none;box-shadow:none;margin:0 auto}
  .ictl{display:none!important}
  .signal .ring{animation:none!important}
  .tl .tm,.acard{opacity:1!important;transform:none!important}
  @page{size:1920px 1080px;margin:0}
}
@media (prefers-reduced-motion:reduce){.chat{transition:none}}
"""

# ── 공통 조각 ──
def brandbar():
    return f'<div class="brandbar"><img class="osoma" src="{OSOMA}" alt="오픈소스마케팅"></div>'

def furniture(n, credit=True):
    c = '<div class="credit">OPEN SOURCE MARKETING</div>' if credit else ''
    num = f'{n:02d} / {TOTAL}' if isinstance(n, int) else n
    return f'{c}<div class="pgno">{num}</div>'

def kicker(k1, k2):
    return f'<div class="kicker"><span class="k1">{k1}</span> <span class="k2">/ {k2}</span></div>'

def slide(n, cls, body, credit=True):
    return f'<div class="vp"><section class="slide {cls}" id="s{n}">{body}{furniture(n, credit)}</section></div>'

# 장마다 헤더 문장을 담아 둔다. lint 의 헤더 종결어미 검사가 이 값을 본다
HEADERS = {}

# ── lint: 금지 기호, 번역투, 헤더 종결어미 ──
BANNED_CHARS = {"—": "줄표", "–": "줄표", "·": "가운뎃점", "…": "말줄임표", "!": "느낌표"}
TRANS = [
    (r"중 하나(입니다|였습니다|이다|다\b)", "~중 하나"), (r"에 대(해|한|해서)\s", "~에 대해"),
    (r"[을를] 통해", "~을 통해"), (r"에 있어서?\s", "~에 있어서"),
    (r"되어지|보여집니다|여겨집니다", "이중 피동"), (r"에 의해\s", "~에 의해"),
    (r"라는 사실[을이]", "~라는 사실"), (r"당신", "당신"),
    (r"에도 불구하고", "~에도 불구하고"), (r"하는 것을 돕", "~하는 것을 돕는다"),
]

def strip_tags(html):
    html = re.sub(r"<script.*?</script>", "", html, flags=re.S)
    html = re.sub(r"<style.*?</style>", "", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return html

def lint(slides_html):
    bad = []
    for i, html in enumerate(slides_html, 1):
        text = strip_tags(html)
        for ch, name in BANNED_CHARS.items():
            if ch in text:
                bad.append(f"s{i}: 금지 기호 {name}({ch})")
        for pat, name in TRANS:
            if re.search(pat, text):
                bad.append(f"s{i}: 번역투 {name}")
    for n, h in HEADERS.items():
        if re.search(r"(습니다|합니다|입니다)$", h.strip()):
            bad.append(f"s{n}: 헤더가 서술형 종결({h})")
    if bad:
        print("✗ lint 위반:")
        for b in bad:
            print("  " + b)
        sys.exit(1)
    print("✓ 금지 기호 검사 통과 (기호, 번역투, 헤더 종결어미)")

# ── 교정 게이트: 작성 → 교정 → 승인 루프 강제 ──
# 화면 텍스트가 바뀌면 빌드가 실패하고 교정대기 파일이 생성된다.
# 대기 문장을 hongblog 지침(낭독 여덟 질문)으로 검수(새 문맥의 교정 에이전트 권장)하고,
# 위반을 고친 뒤 --approve 로 승인해야 빌드가 통과된다. 이 게이트를 지우지 말 것.
def extract_sentences(slides_html):
    sents = []
    for html in slides_html:
        text = re.sub(r"\s+", " ", strip_tags(html)).strip()
        for p in re.split(r"(?<=\.)[\s\"]+|(?<=\?)\s+", text):
            p = p.strip().strip('"')
            if len(p) >= 8 and re.search(r"[가-힣]", p):
                sents.append(p)
    return sents

def prose_gate(slides_html, tag, approve):
    approve_file = ROOT / f"교정승인_{tag}.json"
    pending_file = ROOT / f"교정대기_{tag}.txt"
    sents = extract_sentences(slides_html)
    digest = hashlib.sha256("\n".join(sents).encode()).hexdigest()
    prev = json.loads(approve_file.read_text(encoding="utf-8")) if approve_file.exists() else {}
    if prev.get("hash") == digest:
        print(f"✓ 교정 승인 일치 ({tag})")
        pending_file.unlink(missing_ok=True)
        return
    newly = [s for s in sents if s not in set(prev.get("sentences", []))]
    body = ("# 교정 대기 문장 (hongblog 지침 낭독 여덟 질문으로 검수할 것)\n"
            "# 검수와 수정을 마친 뒤: python3 build_slides.py --approve\n\n"
            + "\n".join(f"- {s}" for s in (newly or sents)))
    pending_file.write_text(body, encoding="utf-8")
    if approve:
        approve_file.write_text(json.dumps({"hash": digest, "sentences": sents}, ensure_ascii=False),
                                encoding="utf-8")
        pending_file.unlink(missing_ok=True)
        print(f"✓ 교정 승인 기록 ({tag}, 신규/변경 {len(newly or sents)}문장)")
        return
    print(f"✗ 교정 미승인 ({tag}): 신규/변경 {len(newly or sents)}문장이 {pending_file.name} 에 있다.")
    print("  대기 문장을 검수하고 위반을 고친 뒤 --approve 로 승인해야 빌드된다.")
    sys.exit(1)
