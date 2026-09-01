#!/usr/bin/env python3
# 열매나눔재단 AI 온보딩 빌드 스크립트 (지침_열매나눔재단_AI온보딩.md가 단일 기준)
# 사용법: python3 build_slides.py  →  index.html 생성
# HTML을 직접 고치지 말 것. 이 스크립트를 고쳐 재빌드한다.
import base64, re, sys, pathlib, hashlib, json

ROOT = pathlib.Path(__file__).parent
TOTAL = 29  # 구성표 기준 총 장수 (현재 빌드는 s1~s10)

def img64(path):
    data = (ROOT / path).read_bytes()
    ext = pathlib.Path(path).suffix.lstrip(".")
    mime = "image/svg+xml" if ext == "svg" else f"image/{ext}"
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"

LOGO = img64("assets/merryyear.png")
OSOMA = img64("assets/osoma.svg")
AVATAR = img64("assets/ai_avatar.png")

# ── 덱 CSS: 프리뷰_디자인시안_v3.html 승계 + 본제작 컴포넌트 ──
CSS = """
:root{
  --s:1;
  --bg:#FFFFFF; --card:#FFFFFF;
  --ink:#1F2430; --dim:#6A7180; --faint:#9BA1AE;
  --line:#E9EBF1; --line2:#F1F3F7;
  --c1:#FF7A1A; --c2:#FF4D6D; --c3:#A855F7; --c4:#3B82F6;
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
.aur.a1{width:920px;height:920px;right:-260px;top:-330px;background:radial-gradient(circle,rgba(255,122,26,.15),transparent 62%)}
.aur.a2{width:820px;height:820px;right:180px;top:60px;background:radial-gradient(circle,rgba(168,85,247,.12),transparent 62%)}
.aur.a3{width:760px;height:760px;left:-240px;bottom:-300px;background:radial-gradient(circle,rgba(59,130,246,.11),transparent 62%)}
.aur.a4{width:640px;height:640px;left:340px;bottom:-260px;background:radial-gradient(circle,rgba(255,77,109,.09),transparent 62%)}

/* 공통 가구 */
.brandbar{position:absolute;top:56px;right:72px;display:flex;align-items:center;gap:22px;z-index:5}
.brandbar img{height:40px}
.brandbar .div{width:1px;height:26px;background:var(--line)}
/* 열매나눔재단 PNG는 안쪽 여백이 있어, 글자 높이가 서로 맞게 OSOMA는 조금 작게 둔다 */
.brandbar img.osoma{height:26px;width:auto}
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
.tocol{background:linear-gradient(150deg,#FFF7EF 0%,#FBF2F8 45%,#F4F2FD 75%,#EFF5FE 100%);border:1.5px solid #EDEAF2;border-radius:24px;padding:36px 38px;box-shadow:0 16px 44px rgba(40,50,80,.07)}
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
.mchat{background:linear-gradient(160deg,#FDF4EC,#F5F1FB 55%,#EEF4FD);border:1.5px solid #EDEAF2;border-radius:26px;padding:28px;box-shadow:0 20px 56px rgba(40,50,80,.08)}
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
.mrow.user .mbub{background:linear-gradient(120deg,#FFE7D2,#FFDDE7);border-radius:18px 4px 18px 18px;font-weight:600;max-width:80%}
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
  background:linear-gradient(160deg,#FDF4EC,#F5F1FB 55%,#EEF4FD) padding-box,var(--grad) border-box}
.mchat.hot .wtag{color:#C2452D;border-color:#F2D3C4}
.cmpwrap.on .mchat.cold{opacity:.35;transform:scale(.97)}
.cmpwrap.on .mchat.hot{transform:scale(1.03)}

/* s7 읽기/그리기 패널 */
.duo{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.dpanel{background:linear-gradient(150deg,#FFF7EF 0%,#FBF2F8 45%,#F4F2FD 75%,#EFF5FE 100%);border:1.5px solid #EDEAF2;border-radius:24px;padding:28px;box-shadow:0 16px 44px rgba(40,50,80,.07)}
.dpanel .dt{font-family:var(--fm);font-size:15px;font-weight:700;letter-spacing:.2em;margin:0 0 18px;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.scene{height:190px;border-radius:16px;position:relative;overflow:hidden;background:linear-gradient(180deg,#DCEFFB 0%,#F6EFE2 70%)}
.scene .sun{position:absolute;right:34px;top:26px;width:54px;height:54px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#FFC46B,#FF8A3D)}
.scene .hill1{position:absolute;left:-40px;bottom:-64px;width:280px;height:160px;border-radius:50%;background:#7FB98A}
.scene .hill2{position:absolute;right:-60px;bottom:-84px;width:340px;height:180px;border-radius:50%;background:#5E9E6E}
.scene .box{position:absolute;left:120px;bottom:26px;width:120px;height:64px;border-radius:10px;background:#fff;border:2px solid #E3E7DD}
.scene .box::before{content:"";position:absolute;left:12px;top:12px;right:12px;height:10px;border-radius:5px;background:#FF8A3D}
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
.desk .doc .hlt{background:#FDF1EA;border-bottom:2px solid var(--c1);color:var(--ink);padding:1px 4px;border-radius:4px}
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
  background:linear-gradient(150deg,#FFF7EF,#FBF2F8 45%,#F4F2FD 75%,#EFF5FE);border:1.5px solid #EDEAF2}
.trio .thead small{display:block;font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.14em;margin-bottom:8px;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.trio .tlabel{display:flex;align-items:center;justify-content:flex-end;padding-right:12px;font-size:19.5px;font-weight:700;color:var(--dim);text-align:right}
.trio .tcell{background:#fff;border:1.5px solid var(--line);border-radius:18px;padding:24px 28px;font-size:21px;line-height:1.5;
  display:flex;align-items:center;justify-content:center;text-align:center;box-shadow:0 10px 30px rgba(40,50,80,.05)}

/* s13 타임라인 (텍스트 위아래 교차) */
.tl{display:grid;grid-template-columns:repeat(9,1fr);gap:14px}
.tm{position:relative;height:400px;transition:opacity .3s,transform .3s}
.tm::before{content:"";position:absolute;top:calc(50% - 1.5px);left:calc(50% + 34px);right:calc(-50% + 34px);height:3px;background:linear-gradient(90deg,#F3B08C,#C9A6F0)}
.tm:last-child::before{display:none}
.tm .mo{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:54px;height:54px;border-radius:50%;display:grid;place-items:center;
  background:#fff;border:2.5px solid #E5CBE9;font-family:var(--fm);font-size:19px;font-weight:700;color:var(--dim);transition:all .3s}
.tm .tick{position:absolute;left:calc(50% - 1px);width:2px;height:18px;background:#DCC7E4}
.tm.up .tick{bottom:calc(50% + 28px)}
.tm.dn .tick{top:calc(50% + 28px)}
.tm p{position:absolute;left:-16px;right:-16px;text-align:center;font-size:19px;line-height:1.5;color:var(--dim);word-break:keep-all}
.tm.up p{bottom:calc(50% + 54px)}
.tm.dn p{top:calc(50% + 54px)}
.tm .pbadge{position:absolute;top:calc(50% - 13px);left:calc(50% + 36px);font-family:var(--fm);font-size:13px;font-weight:700;letter-spacing:.1em;
  color:#C2452D;background:#FDEDE6;border:1.5px solid #F2D3C4;border-radius:999px;padding:4px 11px;white-space:nowrap}
.tl.focus .tm{opacity:.28}
.tl.focus .tm.on{opacity:1;transform:translateY(-6px)}
.tl.focus .tm.on .mo{background:var(--grad);color:#fff;border-color:transparent;box-shadow:0 10px 26px rgba(200,90,120,.32)}
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
.vcard{border-radius:24px;padding:38px 40px;background:linear-gradient(150deg,#FFF7EF,#FBF2F8 45%,#F4F2FD 75%,#EFF5FE);
  border:1.5px solid #EDEAF2;box-shadow:0 16px 44px rgba(40,50,80,.07)}
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
  background:linear-gradient(150deg,#FFF7EF,#F4F2FD 70%,#EFF5FE);border:1.5px solid #EDEAF2}
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
.stepn::before{content:"";position:absolute;top:33px;left:calc(50% + 44px);right:calc(-50% + 44px);height:3px;background:linear-gradient(90deg,#F3B08C,#C9A6F0)}
.stepn:last-child::before{display:none}
.stepn b{display:grid;place-items:center;width:66px;height:66px;margin:0 auto;border-radius:50%;background:var(--grad);color:#fff;
  font-family:var(--fm);font-size:24px;font-weight:700;box-shadow:0 10px 26px rgba(200,90,120,.3)}
.stepn h4{margin-top:20px;text-align:center;font-size:24px;font-weight:800}
.stepn p{margin-top:10px;text-align:center;font-size:18.5px;line-height:1.55;color:var(--dim)}
.stepband{margin-top:64px;border-radius:20px;padding:26px 34px;font-size:21px;color:var(--dim);line-height:1.6;
  background:linear-gradient(150deg,#FFF7EF,#F4F2FD 70%,#EFF5FE);border:1.5px solid #EDEAF2}
.stepband strong{color:var(--ink)}
/* 문서 대비 */
.ba{display:grid;grid-template-columns:1fr 90px 1fr;align-items:center}
.paper{background:#fff;border:1.5px solid var(--line);border-radius:22px;padding:40px 44px;box-shadow:0 16px 44px rgba(40,50,80,.08);min-height:300px}
.paper .ptag{font-family:var(--fm);font-size:14.5px;font-weight:700;letter-spacing:.16em;color:var(--faint);margin-bottom:20px}
.paper.after .ptag{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.paper .ptxt{font-size:24px;line-height:1.85;color:var(--dim)}
.paper.after{border:2px solid transparent;background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}
.paper.after .ptxt{color:var(--ink)}
.paper .ptxt em{font-style:normal;background:linear-gradient(120deg,#FFE7D2,#FFDDE7);border-radius:6px;padding:1px 6px;font-weight:700}
.baarrow{display:grid;place-items:center}
.baarrow span{width:58px;height:58px;border-radius:50%;background:var(--grad);display:grid;place-items:center;box-shadow:0 10px 26px rgba(200,90,120,.32)}
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
    background:none !important;-webkit-text-fill-color:#FF4D6D !important;color:#FF4D6D !important}
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
    return (f'<div class="brandbar"><img src="{LOGO}" alt="열매나눔재단">'
            f'<span class="div"></span><img class="osoma" src="{OSOMA}" alt="OSOMA"></div>')

def furniture(n, credit=True):
    c = '<div class="credit">MERRY YEAR FOUNDATION × OSOMA</div>' if credit else ''
    num = f'{n:02d} / {TOTAL}' if isinstance(n, int) else n
    return f'{c}<div class="pgno">{num}</div>'

def kicker(k1, k2):
    return f'<div class="kicker"><span class="k1">{k1}</span> <span class="k2">/ {k2}</span></div>'

def slide(n, cls, body, credit=True):
    return f'<div class="vp"><section class="slide {cls}" id="s{n}">{body}{furniture(n, credit)}</section></div>'

# ── 장별 정의: (헤더 텍스트는 lint 헤더 검사 대상) ──
HEADERS = {}

def s1():
    HEADERS[1] = "일은 AI에게, 마음은 사람에게"
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
    body = (f'<i class="aur a1"></i><i class="aur a3"></i>{sig}'
            '<div class="meta-tl">MERRY YEAR FOUNDATION / AI ONBOARDING</div>'
            f'{brandbar()}<div class="fg">'
            '<h1 style="font-size:128px;font-weight:800;letter-spacing:-.04em;line-height:1.16">'
            '일은 <span class="gt">AI에게</span>,<br>마음은 사람에게</h1>'
            '<p class="sub">열매나눔재단 임직원을 위한 AI 온보딩</p>'
            '<div class="mchips"><span><b>60</b> MIN</span><span>NO CODE</span><span>NO INSTALL</span></div>'
            '</div>')
    return slide(1, "cover", body, credit=False)

def s2():
    HEADERS[2] = "오늘의 목차"
    def col(no, title, items):
        lis = "".join(f'<li><b>{i:02d}</b>{t}</li>' for i, t in items)
        return f'<div class="tocol"><h3><b>{no}</b>{title}</h3><ul>{lis}</ul></div>'
    c1 = col("PART 01", "AI의 비밀", [(1, "답변이 생성되는 원리"), (2, "그럴듯함과 사실의 거리"),
                                     (3, "좋은 답변을 얻는 법"), (4, "이미지와 영상을 다루는 방식")])
    c2 = col("PART 02", "AI와 일하는 세 가지 방식", [(5, "묻고 답하기, 함께 편집하기, 업무 위임하기"),
                                                  (6, "2026년의 변화 타임라인"), (7, "내년의 가능성과 사람의 역할"),
                                                  (8, "조직 AX 전환에서 중요한 것")])
    c3 = col("PART 03", "열매나눔재단의 가능성", [(9, "재단에서 가능한 작업들"), (10, "한 가지 일, 세 가지 방식의 워크플로우")])
    body = (f'<i class="aur a2" style="right:-200px;top:-260px"></i>{brandbar()}<div class="fg">'
            '<h2 class="head">오늘의 <span class="gt">목차</span></h2>'
            f'<div class="vcen"><div class="toc">{c1}{c2}{c3}</div></div>'
            '</div>')
    return slide(2, "split", body)

def pdiv(n, num, title, items, rail_on):
    HEADERS[n] = title
    lis = "".join(f'<li><b>{i:02d}</b>{t}</li>' for i, t in items)
    rails = ["AI의 비밀", "일하는 방식", "재단의 가능성", "마무리"]
    rail = "".join(f'<div class="{"on" if i == rail_on else ""}"><i></i><span>{r}</span></div>'
                   for i, r in enumerate(rails))
    body = (f'<i class="aur a2" style="right:-160px;top:auto;bottom:-200px"></i>'
            f'<div class="bignum">{num}</div>{brandbar()}<div class="fg">'
            f'<div class="pno">PART {num}</div><h2>{title}</h2><ul>{lis}</ul></div>'
            f'<div class="rail">{rail}</div>')
    return slide(n, "pdiv", body, credit=False)

def s3():
    return pdiv(3, "01", "AI의 비밀",
                [(1, "답변이 생성되는 원리"), (2, "그럴듯함과 사실의 거리"),
                 (3, "좋은 답변을 얻는 법"), (4, "이미지와 영상을 다루는 방식")], 0)

def part_of(n):
    return "01" if n <= 7 else ("02" if n <= 15 else "03")

def split_slide(n, k2, head_html, header_text, lead, points, right, extra_aur="", kick1=None):
    HEADERS[n] = header_text
    pts = "".join(f'<div class="pt"><b>{i:02d}</b><div><h4>{t}</h4><p>{d}</p></div></div>'
                  for i, (t, d) in enumerate(points, 1))
    body = (f'{extra_aur}{brandbar()}<div class="fg">'
            f'{kicker(kick1 or f"PART {part_of(n)}", k2)}'
            f'<h2 class="head">{head_html}</h2>'
            f'<p class="lead">{lead}</p>'
            f'<div class="cols"><div class="points">{pts}</div><div class="rcol">{right}</div></div>'
            '</div>')
    return slide(n, "split", body)

def s4():
    # 이어쓰기 시뮬레이션: 초기 DOM = 완성 문장 + 후보 1세트 (PDF 박제 상태)
    right = ('<div class="simbox">'
             '<div class="simlabel">NEXT WORD</div>'
             '<div class="simsent" id="simsent">후원자님께 감사의 마음을 전합니다<span class="cursor"></span></div>'
             '<div class="cands" id="simcands"><div class="ct">CANDIDATES</div>'
             '<div class="cand top"><span class="w">마음을</span><span class="track"><span class="fill" style="width:62%"></span></span><span class="pc">62%</span></div>'
             '<div class="cand"><span class="w">인사를</span><span class="track"><span class="fill" style="width:24%"></span></span><span class="pc">24%</span></div>'
             '<div class="cand"><span class="w">열매를</span><span class="track"><span class="fill" style="width:9%"></span></span><span class="pc">9%</span></div>'
             '</div>'
             '<button class="ictl" id="simbtn" onclick="simStep()">처음부터 한 어절씩 이어 보기</button>'
             '</div>'
             '<p class="rcap">예시: 감사 인사의 첫 문장이 만들어지는 과정입니다. 후보와 확률은 가상 수치입니다.</p>')
    sim_js = """
<script>
(function(){
  const steps=[
    {sent:"후원자님께", cands:[["감사의",58],["안부를",21],["소식을",12]]},
    {sent:"후원자님께 감사의", cands:[["마음을",62],["인사를",24],["열매를",9]]},
    {sent:"후원자님께 감사의 마음을", cands:[["전합니다",71],["보냅니다",18],["담습니다",6]]},
    {sent:"후원자님께 감사의 마음을 전합니다", cands:[["마음을",62],["인사를",24],["열매를",9]]}
  ];
  let st=-1;
  window.simStep=function(){
    st=(st+1)%(steps.length+1);
    const idx=(st===steps.length)?steps.length-1:st;
    const s=steps[(st===steps.length)?3:st];
    const sent=document.getElementById('simsent');
    const box=document.getElementById('simcands');
    const btn=document.getElementById('simbtn');
    if(st===steps.length){st=-1;}
    sent.innerHTML=s.sent+'<span class="cursor"></span>';
    let html='<div class="ct">CANDIDATES</div>';
    s.cands.forEach((c,i)=>{
      html+='<div class="cand'+(i===0?' top':'')+'"><span class="w">'+c[0]+'</span>'
        +'<span class="track"><span class="fill" style="width:'+c[1]+'%"></span></span>'
        +'<span class="pc">'+c[1]+'%</span></div>';
    });
    box.innerHTML=html;
    btn.textContent=(st===-1)?'처음부터 한 어절씩 이어 보기':'다음 어절 고르기';
  };
})();
</script>"""
    html = split_slide(4, "AI의 비밀",
        '답변이 생성되는 <span class="gt">원리</span>', "답변이 생성되는 원리",
        "AI는 문장을 한 번에 만들지 않고, 추론에 따라 다음 글자를 하나씩 고르는 일을 반복해 답을 만듭니다.",
        [("다음 글자를 확률로 고릅니다", "지금까지 쓴 글을 보고, 다음에 올 후보마다 그럴듯한 정도를 매깁니다."),
         ("고른 글자가 다시 재료가 됩니다", "방금 붙인 글자까지 읽고 그다음 글자를 또 고릅니다."),
         ("1등만 고르지는 않습니다", "가끔 2등과 3등도 뽑기 때문에 같은 질문에도 답이 조금씩 달라집니다.")],
        right, '<i class="aur a1" style="width:700px;height:700px;right:-200px;top:-260px"></i>')
    return html + sim_js

def s5():
    right = ('<div class="mchat">'
             f'<div class="mhead"><span class="mava"><img src="{AVATAR}" alt="AI"></span><b>AI</b></div>'
             '<div class="mrow user"><div class="mbub">작년 우리 재단 지원 성과를 요약해 줘</div></div>'
             f'<div class="mrow"><span class="mava"><img src="{AVATAR}" alt="AI"></span>'
             '<div class="mcol"><span class="mname">AI</span>'
             '<div class="mbub">작년 한 해 가게 132곳을 지원했고, 후원금은 평균 27% 늘었습니다.</div></div></div>'
             '<div class="mnote">자료를 줬음에도 수치가 맞는지 알 수 없는 상태입니다.</div>'
             '</div>'
             '<div class="warncard"><div class="wt">CHECK BEFORE SEND</div><ul>'
             '<li><b>01</b>이름, 날짜, 금액은 원문 자료와 대조합니다</li>'
             '<li><b>02</b>출처가 없는 수치는 지웠다가 확인 후 되살립니다</li>'
             '<li><b>03</b>원문 자료를 함께 주면 지어내기가 크게 줄어듭니다</li>'
             '</ul></div>'
             '')
    return split_slide(5, "AI의 비밀",
        '그럴듯함과 사실의 거리 - <span class="gt">할루시네이션</span>', "그럴듯함과 사실의 거리 - 할루시네이션",
        "이렇게 그럴듯한 글자를 고르는 원리 그대로, 그럴듯한 내용을 지어내기도 합니다.",
        [("사실을 찾아보고 답하는 것이 아닙니다", "쌓인 글의 패턴으로 문장을 만드는 것이 기본 동작이라, 모르는 것도 그럴듯하게 채웁니다."),
         ("자신 있는 말투와 정확성은 별개입니다", "확신에 찬 문장도 확률이 높았던 표현일 뿐입니다."),
         ("그래서 검토는 늘 사람의 몫입니다", "이름, 날짜, 금액, 근거 데이터는 사람이 확인해야 합니다.")],
        right, '<i class="aur a4"></i>')

def s6():
    ava = f'<span class="mava"><img src="{AVATAR}" alt="AI"></span>'
    right = ('<div class="cmpwrap" id="cmp">'
             '<div class="mchat cold"><span class="wtag">그냥 물었을 때</span>'
             '<div class="mrow user"><div class="mbub">후원 감사 편지 써 줘</div></div>'
             f'<div class="mrow">{ava}<div class="mcol"><span class="mname">AI</span>'
             '<div class="mbub">안녕하세요. 늘 따뜻한 후원에 감사드립니다. 앞으로도 변함없는 관심을 부탁드립니다.</div></div></div></div>'
             '<div class="mchat hot"><span class="wtag">사정을 먼저 알렸을 때</span>'
             '<div class="mrow user"><div class="mbub">여성가장의 자립을 돕는 첫 정기후원을 시작하신 열매나눔재단 후원자님께 보낼 감사 편지를 따뜻한 존댓말로 써 주세요.</div></div>'
             f'<div class="mrow">{ava}<div class="mcol"><span class="mname">AI</span>'
             '<div class="mbub">후원자님의 첫걸음이 한 가정의 자립으로 이어집니다. 보내 주신 마음이 어떻게 열매 맺는지 소식으로 전해 드리겠습니다.</div></div></div></div>'
             '<button class="ictl" onclick="document.getElementById(\'cmp\').classList.toggle(\'on\')">재단의 답 크게 보기</button>'
             '</div>'
             '<p class="rcap">예시: 같은 AI여도 우리 사정을 먼저 알리면 우리의 목소리로 답합니다.</p>')
    return split_slide(6, "AI의 비밀",
        '좋은 답변을 얻는 법 - <span class="gt">프롬프트 엔지니어링</span>', "좋은 답변을 얻는 법 - 프롬프트 엔지니어링",
        "일 잘하는 부하에게 알려주듯, 재단 사정을 먼저 알려 주면 퀄리티가 달라집니다.",
        [("처음 온 인턴은 유능해도 재단 히스토리를 모릅니다", "우리 사업과 후원자 이야기를 먼저 알려줘야 일을 시작할 수 있습니다."),
         ("AI도 같습니다", "요청 앞에 우리 상황을 알려주면 답이 재단의 목소리와 가까워집니다."),
         ("반복되는 정보는 한 번만 쓰면 됩니다", "자주 쓰는 정보는 저장해 두고 매번 불러서 참고하도록 합니다.")],
        right, '<i class="aur a1" style="width:700px;height:700px;right:-200px;top:-260px"></i>')

def s7():
    scene = ('<div class="scene"><i class="sun"></i><i class="hill1"></i><i class="hill2"></i><i class="box"></i></div>')
    right = (f'<div class="duo">'
             f'<div class="dpanel"><div class="dt">READ</div>{scene}'
             '<div class="darrow">사진을 글로</div>'
             '<div class="dtxt">"해 질 녘 언덕 앞에 주황 리본을 두른 흰 상자가 놓여 있습니다."</div></div>'
             f'<div class="dpanel"><div class="dt">DRAW</div>'
             '<div class="dtxt" style="margin-top:0;margin-bottom:16px">"해 질 녘 언덕 앞에 주황 리본을 두른 흰 상자를 그려 주세요."</div>'
             f'<div class="darrow">글을 사진으로</div>{scene}</div>'
             '</div>'
             '<p class="rcap">예시: 같은 능력이 양방향으로 쓰입니다. 왼쪽은 사진을 글로 읽고, 오른쪽은 글을 그림으로 그립니다.</p>')
    return split_slide(7, "AI의 비밀",
        'AI가 <span class="gt">이미지와 영상</span>을 다루는 방식', "AI가 이미지와 영상을 다루는 방식",
        "그림을 언어처럼 읽고, 설명을 받아 그림으로 다시 그립니다.",
        [("읽기: AI는 그림도 글처럼 읽습니다", "사진을 분석해, 글로 묘사하는 것과 같은 방식으로 이해합니다."),
         ("그리기: 설명을 그림으로 다시 그립니다", "글로 쓴 설명을 받아 그 장면을 새로 그려 냅니다."),
         ("실력 차이는 설명 프롬프트에서 드러납니다", "얼마나 자세하게 요청했는지가 결과물의 수준을 정합니다.")],
        right, '<i class="aur a3"></i>')

def s8():
    return pdiv(8, "02", "AI와 일하는 세 가지 방식",
                [(1, "묻고 답하기, 함께 편집하기, 업무 위임하기"), (2, "2026년의 변화 타임라인"),
                 (3, "내년의 가능성과 사람의 역할"), (4, "조직 AX 전환에서 중요한 것")], 1)

def s9():
    right = ('<div class="mchat">'
             f'<div class="mhead"><span class="mava"><img src="{AVATAR}" alt="AI"></span><b>AI</b></div>'
             '<div class="mrow user"><div class="mbub">9월 소식지에 넣을 김장 나눔 행사 안내문 초안을 다섯 줄로 써 주세요.</div></div>'
             f'<div class="mrow"><span class="mava"><img src="{AVATAR}" alt="AI"></span>'
             '<div class="mcol"><span class="mname">AI</span>'
             '<div class="mbub">11월 셋째 주, 후원자님과 함께 담근 김장 김치가 취약계층 가정에 전해집니다. 함께해 주실 봉사자를 모십니다.</div></div></div>'
             '<div class="mrow user"><div class="mbub">둘째 줄을 더 따뜻한 말투로 바꿔 주세요.</div></div>'
             '</div>'
             '')
    return split_slide(9, "세 가지 방식",
        '방식 1. <span class="gt">묻고 답하기</span>', "방식 1. 묻고 답하기",
        "브라우저에서 채팅으로 묻고 답을 받는, 가장 익숙한 방식입니다.",
        [("결과는 화면 속 글로 남습니다", "답을 복사해서 내 문서에 옮겨 붙이는 것까지가 한 번의 작업입니다."),
         ("준비가 필요 없습니다", "브라우저만 열면 바로 시작할 수 있습니다."),
         ("어울리는 일", "짧은 글 초안, 요약, 아이디어 얻기입니다.")],
        right, '<i class="aur a1" style="width:700px;height:700px;right:-200px;top:-260px"></i>')

def s10():
    right = ('<div class="deskwrap"><div class="desk">'
             '<div class="bar"><i></i><i></i><i></i><span>DESKTOP APP</span></div>'
             '<div class="body"><div class="side">'
             '<div class="fi on">사업보고서_초안.docx</div><div class="fi">소식지_9월.docx</div>'
             '<div class="fi">캠페인_기획메모.md</div><div class="fi">행사사진_10월</div></div>'
             '<div class="doc">메자닌아이팩은 지난해 <span class="hlt">북한이탈주민 12명을 신규 채용</span>하여 안정적인 일자리를 이어 갔습니다. 포장박스 생산량은 전년 수준을 유지했고, 신규 거래처 발굴로 매출 기반을 넓혔습니다.'
             '<div class="aiedit"><span class="tag">EDIT</span>문단의 순서를 성과, 과정, 계획 순으로 바꾸고 어투를 보고서체로 통일했습니다. 파일에 바로 저장되었습니다.</div>'
             '</div></div></div></div>'
             '<p class="rcap">문안과 수치는 가상 예시입니다.</p>')
    return split_slide(10, "세 가지 방식",
        '방식 2. <span class="gt">함께 편집하기</span>', "방식 2. 함께 편집하기",
        "데스크톱 앱이 내 문서와 파일을 직접 열어 나란히 작업합니다.",
        [("결과는 내 파일에 남습니다", "복사해 옮길 필요 없이 문서가 바로 고쳐집니다."),
         ("보여 줄 폴더를 사람이 정합니다", "파일을 읽고 고칠 권한은 사람이 허락한 범위 안에서만 씁니다."),
         ("어울리는 일", "보고서 다듬기, 긴 문서 정리, 여러 파일에 걸친 작업입니다.")],
        right, '<i class="aur a2" style="right:-200px;top:-260px"></i>')

def wide(n, k2, head_html, header_text, lead, inner, extra_aur="", cls="split", kick1=None):
    HEADERS[n] = header_text
    body = (f'{extra_aur}{brandbar()}<div class="fg">'
            f'{kicker(kick1 or f"PART {part_of(n)}", k2)}'
            f'<h2 class="head">{head_html}</h2>'
            f'<p class="lead">{lead}</p>'
            f'{inner}</div>')
    return slide(n, cls, body)

def s11():
    right = ('<div class="termwrap"><div class="term">'
             '<div class="bar"><i></i><i></i><i></i><span>자율 실행(CLI)</span></div>'
             '<div class="tbody">'
             '<div class="cmd"><b>&rsaquo;</b>결과보고서 12건을 읽고 사업별 핵심 성과를 한 장으로 정리해 줘</div>'
             '<div class="ok"><i>&check;</i>보고서 폴더에서 파일 12건 확인</div>'
             '<div class="ok"><i>&check;</i>파일마다 핵심 성과 추출</div>'
             '<div class="ok"><i>&check;</i>사업별 표로 정리</div>'
             '<div class="ok"><i>&check;</i>핵심성과_요약.docx 저장</div>'
             '<div class="fin"><i>&#9679;</i>완료: 결과를 확인해 주세요</div>'
             '</div></div></div>'
             '<p class="rcap">지시문과 파일명은 가상 예시입니다.</p>')
    return split_slide(11, "세 가지 방식",
        '방식 3. <span class="gt">업무 위임하기</span>', "방식 3. 업무 위임하기",
        "AI에게 일의 목표를 알려 주면, 과정은 AI가 알아서 진행하고 사람은 결과를 확인합니다.",
        [("중간 과정은 AI가 진행합니다", "자료를 찾고, 정리하고, 파일로 만드는 단계를 사람 없이 이어 갑니다."),
         ("사람은 결과를 검수합니다", "AI가 다 만든 결과물을 받아서 확인하고, 고칠 곳만 다시 알려 줍니다."),
         ("어울리는 일", "순서가 정해진 반복 업무, 여러 파일을 오가는 큰 작업입니다.")],
        right, '<i class="aur a3"></i>')

def s12():
    heads = [("방식 1", "묻고 답하기"), ("방식 2", "함께 편집하기"), ("방식 3", "업무 위임하기")]
    rows = [("결과가 남는 자리", ["화면 속 글", "내 파일", "완성된 결과물"]),
            ("사람의 개입", ["질문마다 답을 주고받기", "고쳐지는 과정을 지켜보며 확인", "끝난 뒤 결과만 검수"]),
            ("적합한 일", ["짧은 초안, 요약, 아이디어", "보고서 다듬기, 긴 문서 정리", "순서가 정해진 반복 업무"])]
    cells = '<div></div>' + "".join(f'<div class="thead"><small>{a}</small>{b}</div>' for a, b in heads)
    for label, vals in rows:
        cells += f'<div class="tlabel">{label}</div>' + "".join(f'<div class="tcell">{v}</div>' for v in vals)
    inner = (f'<div class="vcen"><div class="trio">{cells}</div>'
             '<p class="lcap">어느 방식을 쓸지 고민될 때는 방식 1로 시작하고, 익숙해지면 방식 2와 3까지 써 보면 됩니다.</p></div>')
    return wide(12, "세 가지 방식", '세 방식의 <span class="gt">구분 기준</span>', "세 방식의 구분 기준",
                "결과가 어디에 남는지, 사람이 얼마나 개입하는지, 이 두 가지가 기준입니다.", inner,
                '<i class="aur a2" style="right:-200px;top:-260px"></i>')

def s13():
    # 월별 사건은 지식 기준일(2026-01) 이후가 포함되어 사용자 검수 전 가안이다. 확정 전 검수 필수.
    months = [("1", "새 세대 AI 모델<br>연이어 공개"), ("2", "실사 수준<br>영상 생성 대중화"),
              ("3", "문서 도구에<br>AI 편집 기본 탑재"), ("4", "자율 실행 방식<br>확산 시작"),
              ("5", "음성 AI<br>상담 업무 적용"), ("6", "국내 기관<br>AI 도입 지원 확대"),
              ("7", "비영리 대상<br>지원 프로그램 등장"), ("8", "기획부터 제작까지<br>한 흐름 정착"),
              ("9", "차세대 모델<br>공개 예고")]
    tms = "".join(
        f'<div class="tm {"up" if i % 2 == 1 else "dn"}">'
        f'{"<span class=\"pbadge\">예정</span>" if m == "9" else ""}'
        f'<span class="mo">{m}월</span><i class="tick"></i><p>{ev}</p></div>'
        for i, (m, ev) in enumerate(months, 1))
    inner = (f'<div class="vcen"><div class="tl" id="tl13">{tms}</div>'
             '<button class="ictl" id="tlbtn" onclick="tlStep()" style="align-self:center;margin-top:60px">1월부터 짚어 보기</button>'
             '</div>')
    js = """
<script>
(function(){
  let st=-1;
  window.tlStep=function(){
    const tl=document.getElementById('tl13');
    const btn=document.getElementById('tlbtn');
    const items=tl.querySelectorAll('.tm');
    st++;
    if(st>=items.length){st=-1;}
    items.forEach((el,i)=>el.classList.toggle('on',i===st));
    tl.classList.toggle('focus',st>=0);
    btn.textContent = st===-1 ? '1월부터 짚어 보기' : (st===items.length-1 ? '전체 보기' : '다음 달 보기');
  };
})();
</script>"""
    return wide(13, "변화의 속도", '2026년의 변화 <span class="gt">타임라인</span>', "2026년의 변화 타임라인",
                "올해 들어 여덟 달 사이에도 일하는 방식이 계속 바뀌었습니다.", inner,
                '<i class="aur a1" style="width:700px;height:700px;right:-200px;top:-260px"></i>') + js

def s14():
    right = ('<div class="pstack">'
             '<div class="paper"><div class="ptag">AI에게 맡기는 일</div><ul class="plist">'
             '<li><b>01</b>초안 작성</li><li><b>02</b>자료 정리와 요약</li>'
             '<li><b>03</b>형식 맞추기</li><li><b>04</b>반복 작업</li></ul></div>'
             '<div class="paper after"><div class="ptag">사람에게 남는 일</div><ul class="plist">'
             '<li><b>01</b>방향 결정</li><li><b>02</b>최종 검토와 책임</li>'
             '<li><b>03</b>후원자와의 관계</li><li><b>04</b>현장의 마음</li></ul></div>'
             '</div>'
             '<p class="rcap">표지의 문장 그대로입니다. 일은 AI에게, 마음은 사람에게.</p>')
    return split_slide(14, "내년의 전망",
        '내년의 가능성과 <span class="gt">사람의 역할</span>', "내년의 가능성과 사람의 역할",
        "내년에는 더 오래 걸리는 일을 통째로 맡길 수 있게 된다는 전망이 나옵니다. 그래도 마지막 확인은 사람이 합니다.",
        [("맡기는 단위가 커질 수 있습니다", "한 번의 지시로 처리되는 일의 범위가 계속 넓어지고 있습니다."),
         ("판단과 책임은 사람의 몫입니다", "무엇을 맡길지, 결과를 내보낼지는 사람이 정합니다."),
         ("관계는 사람만 맺을 수 있습니다", "후원자와 수혜자를 마주하는 일은 AI가 대신하지 못합니다.")],
        right, '<i class="aur a4"></i>')

AX_BEFORE = img64("assets/gen_ax_before.jpg")
AX_AFTER = img64("assets/gen_ax_after.jpg")

def s15():
    right = ('<div class="pstack">'
             '<div class="photocard">'
             f'<img src="{AX_BEFORE}" alt="도구만 들어온 조직 연출 예시"><i class="scrim"></i>'
             '<div class="ptext"><div class="ptag2">도구만 들어온 조직</div>'
             '<p>AI 계정은 있지만 들어가 보는 사람이 드뭅니다. 일하는 순서는 예전 그대로입니다.</p></div></div>'
             '<div class="photocard hot">'
             f'<img src="{AX_AFTER}" alt="일하는 방식이 바뀐 조직 연출 예시"><i class="scrim"></i>'
             '<div class="ptext"><div class="ptag2">일하는 방식이 바뀐 조직</div>'
             '<p>감사 편지 초안은 AI가 먼저 쓰고, 사람은 다듬어 보냅니다. 반복 업무마다 AI 단계가 들어가 있습니다.</p></div></div>'
             '</div>'
             '<p class="rcap">사진은 AI로 만든 연출 예시입니다.</p>')
    return split_slide(15, "조직의 준비",
        '조직 <span class="gt">AX 전환</span>에서 중요한 것', "조직 AX 전환에서 중요한 것",
        "AI 전환(AX)에서 바뀌어야 하는 것은 도구가 아니라 일하는 방식입니다.",
        [("계정만 만들고 끝나면 전환이 멈춥니다", "도구만 들어온 조직에서는 익숙한 사람만 쓰고 끝난 사례가 있습니다."),
         ("반복 업무부터 한 단계씩", "자주 하는 일 하나에 AI 단계를 끼워 넣는 것이 시작입니다."),
         ("각자의 자리에서 시작합니다", "전담 부서가 생기기를 기다릴 필요가 없습니다. 먼저 시도한 사람의 방식이 조직의 기준이 될 수 있습니다.")],
        right, '<i class="aur a2" style="right:-200px;top:-260px"></i>')

def s16():
    return pdiv(16, "03", "열매나눔재단의 가능성",
                [(1, "남들보다 앞선 출발선"), (2, "재단에서 가능한 작업들"),
                 (3, "한 가지 일, 세 가지 방식의 워크플로우"), (4, "안전하게 사용하는 규칙")], 2)

def s17():
    cards = [("DATA", "GA4", "홈페이지 방문과 후원 흐름이 데이터로 쌓이고 있습니다."),
             ("WAREHOUSE", "빅쿼리", "쌓인 데이터를 언제든 꺼내 쓸 수 있는 창고입니다."),
             ("DASHBOARD", "루커 스튜디오", "숫자를 한눈에 확인하는 대시보드입니다.")]
    grid = "".join(f'<div class="acard on"><div class="atag">{t}</div><h3>{n}</h3><p>{d}</p></div>'
                   for t, n, d in cards)
    inner = (f'<div class="vcen"><div class="assets" id="assets17">{grid}</div>'
             '<div class="impband"><strong>재단이 2025년에 갖춘 데이터 기반입니다.</strong> '
             '데이터가 준비된 조직에서는 AI에게 시킬 수 있는 일의 폭이 넓어집니다.</div>'
             '<button class="ictl" id="asbtn" onclick="assetStep()">자산 하나씩 켜 보기</button>'
             '</div>')
    js = """
<script>
(function(){
  let lit=3;
  window.assetStep=function(){
    const cards=document.querySelectorAll('#assets17 .acard');
    const btn=document.getElementById('asbtn');
    lit=(lit+1)%4;
    cards.forEach((el,i)=>el.classList.toggle('on',i<lit));
    btn.textContent = lit===3 ? '자산 하나씩 켜 보기' : '다음 자산 켜기';
  };
})();
</script>"""
    return wide(17, "재단의 자산", '남들보다 <span class="gt">앞선 출발선</span>', "남들보다 앞선 출발선",
                "AI 전환(AX)에는 디지털 전환(DX)이라는 기반이 먼저 필요합니다. 재단은 그 기반을 이미 갖추고 있습니다.",
                inner, '<i class="aur a1"></i><i class="aur a3"></i>', cls="split imp") + js

def s18():
    jobs = [("감사 편지", "후원자 상황에 맞춘 초안 작성"),
            ("결과보고서 요약", "긴 보고서를 한 장으로 압축"),
            ("신청서 초안", "지원사업 신청서의 뼈대 잡기"),
            ("보도자료", "행사 소식을 기사 형식으로 작성"),
            ("카드뉴스 문안", "핵심 메시지를 장별 문구로 나누기"),
            ("번역", "해외 협력 문서를 우리말로 옮기기"),
            ("회의록 정리", "녹취록을 결정 사항 중심으로 정리"),
            ("문의 응대", "자주 오는 질문의 답변 초안 만들기"),
            ("데이터 질문", "후원 데이터를 말로 묻고 답 받기")]
    grid = "".join(f'<div class="job"><b>{i:02d}</b><h4>{t}</h4><p>{d}</p></div>'
                   for i, (t, d) in enumerate(jobs, 1))
    inner = (f'<div class="vcen"><div class="jobs">{grid}</div>'
             '<p class="lcap">이어지는 시나리오에서는 모금 캠페인 하나를 처음부터 끝까지 진행해 봅니다.</p></div>')
    return wide(18, "가능한 작업", '열매나눔재단에서 <span class="gt">가능한 작업들</span>', "열매나눔재단에서 가능한 작업들",
                "오늘 배운 세 방식으로 바로 시작할 수 있는 일들입니다.", inner,
                '<i class="aur a2" style="right:-200px;top:-260px"></i>')

CAP_CAMP = img64("assets/cap_mob_camp.png")

def s19():
    right = ('<div class="scen">'
             f'<div class="phone"><div class="bezel"><img src="{CAP_CAMP}" alt="재단 캠페인 페이지"></div>'
             '<div class="plabel">참고 자료: 재단 캠페인 페이지</div></div>'
             '<div class="paper"><div class="ptag">AI가 만든 기획 초안</div><ul class="plist">'
             '<li><b>제목</b>"가게의 불이 다시 켜질 때" 포함 후보 3안</li>'
             '<li><b>구성</b>현장 이야기, 문제, 재단의 방법, 후원금 사용처, 참여 방법</li>'
             '<li><b>톤</b>현장 인용을 앞세운 담담한 존댓말</li>'
             '</ul></div></div>'
             '<p class="rcap">왼쪽은 재단의 실제 캠페인 페이지이고, 오른쪽 기획 초안은 가상 예시입니다.</p>')
    return split_slide(19, "시나리오",
        '시나리오 1. <span class="gt">캠페인 상세페이지</span> 기획', "시나리오 1. 캠페인 상세페이지 기획",
        "재단의 기존 캠페인 페이지를 AI에게 참고 자료로 주고, 새 캠페인의 기획 초안을 받아 봅니다.",
        [("참고 자료 전달", "기존 상세페이지 링크와 이번 캠페인의 사정을 함께 알려 줍니다."),
         ("구성안 받기", "제목 후보, 스토리 순서, 문단별 내용이 담긴 초안이 나옵니다."),
         ("사람이 고르고 다듬기", "후보 중에서 재단의 목소리에 맞는 안을 골라 다듬습니다.")],
        right, '<i class="aur a1" style="width:700px;height:700px;right:-200px;top:-260px"></i>')

def s20():
    steps = [("기획", "목표와 대상을 한 문단으로 정리"),
             ("문구", "제목과 본문 카피를 여러 안으로 작성"),
             ("상세페이지", "구성안과 문단별 원고 작성"),
             ("소재", "카드뉴스와 배너 시안 제작")]
    nodes = "".join(f'<div class="stepn"><b>{i}</b><h4>{t}</h4><p>{d}</p></div>'
                    for i, (t, d) in enumerate(steps, 1))
    inner = ('<div class="vcen">'
             f'<div class="steps">{nodes}</div>'
             '<div class="stepband"><strong>다음 장부터 이 흐름을 세 방식으로 각각 진행합니다.</strong> '
             '같은 일을 어느 방식으로 하느냐에 따라 무엇이 달라지는지 비교해 봅니다.</div>'
             '</div>')
    return wide(20, "시나리오", '시나리오 2. <span class="gt">새 모금 캠페인</span>, 기획부터 제작까지',
                "시나리오 2. 새 모금 캠페인, 기획부터 제작까지",
                "기획부터 소재까지 네 단계가 한 흐름으로 이어집니다.", inner,
                '<i class="aur a3"></i>')

def s21():
    cards = [("방식 1", "묻고 답하기", "단계마다 사람이 AI에게 묻고, 받은 글을 직접 문서로 옮깁니다."),
             ("방식 2", "함께 편집하기", "캠페인 폴더 안에서 작업이 이어지고, 결과가 파일로 쌓입니다."),
             ("방식 3", "업무 위임하기", "지시 한 번으로 작업이 소재 시안까지 진행되고, 사람은 마지막에 검수합니다.")]
    grid = "".join(f'<div class="vcard"><small>{a}</small><h4>{b}</h4><p>{c}</p></div>'
                   for a, b, c in cards)
    inner = (f'<div class="vcen"><div class="vers">{grid}</div>'
             '<p class="lcap">다음 세 장에서 한 방식씩 봅니다.</p></div>')
    return wide(21, "워크플로우", 'AI를 활용한 <span class="gt">세 가지 방식</span>으로 본 우리의 업무',
                "AI를 활용한 세 가지 방식으로 본 우리의 업무",
                "방금 본 캠페인 흐름을 세 가지 방식으로 각각 진행해 보고, 차이를 비교합니다.", inner,
                '<i class="aur a2" style="right:-200px;top:-260px"></i>')

def s22():
    steps = [("기획 묻기", "캠페인 개요를 질문하고 답을 문서에 복사"),
             ("문구 묻기", "기획을 붙여 넣고 카피 요청"),
             ("구성 묻기", "카피를 붙여 넣고 상세페이지 구성 요청"),
             ("소재 요청", "확정한 문구로 이미지 시안 요청")]
    nodes = "".join(f'<div class="stepn"><b>{i}</b><h4>{t}</h4><p>{d}</p></div>'
                    for i, (t, d) in enumerate(steps, 1))
    inner = ('<div class="vcen">'
             f'<div class="steps">{nodes}</div>'
             '<div class="stepband"><strong>손이 많이 가는 대신, 준비 없이 바로 시작할 수 있습니다.</strong></div>'
             '</div>')
    return wide(22, "워크플로우", '버전 1. <span class="gt">묻고 답하기</span>', "버전 1. 묻고 답하기",
                "브라우저 채팅으로 단계마다 AI에게 묻고, 받은 답은 사람이 문서로 옮깁니다.", inner,
                '<i class="aur a1" style="width:700px;height:700px;right:-200px;top:-260px"></i>')

def s23():
    right = ('<div class="deskwrap"><div class="desk">'
             '<div class="bar"><i></i><i></i><i></i><span>DESKTOP APP</span></div>'
             '<div class="body"><div class="side">'
             '<div class="fi on">캠페인_기획.docx</div><div class="fi">카피_3안.docx</div>'
             '<div class="fi">상세페이지_구성.docx</div><div class="fi">배너_시안</div></div>'
             '<div class="doc">겨울 자립 캠페인은 <span class="hlt">가게를 다시 여는 사장님들</span>의 이야기를 중심에 두고, 첫 정기후원자 모집을 목표로 합니다.'
             '<div class="aiedit"><span class="tag">EDIT</span>기획 문서를 바탕으로 카피 3안을 카피_3안.docx에 저장했습니다. 다음으로 상세페이지 구성을 잡겠습니다.</div>'
             '</div></div></div></div>'
             '<p class="rcap">문안과 파일명은 가상 예시입니다.</p>')
    return split_slide(23, "워크플로우",
        '버전 2. <span class="gt">함께 편집하기</span>', "버전 2. 함께 편집하기",
        "캠페인 폴더를 열어 두면, 네 단계 작업이 파일에서 바로 이어집니다.",
        [("폴더 하나로 묶입니다", "AI가 기획 문서를 읽은 채로 문구와 구성 작업을 진행합니다."),
         ("결과가 파일로 쌓입니다", "단계마다 산출물이 문서로 저장되어 히스토리가 남습니다."),
         ("사람은 파일을 검토합니다", "저장된 파일을 확인하고 방향을 조정합니다.")],
        right, '<i class="aur a2" style="right:-200px;top:-260px"></i>')

def s24():
    right = ('<div class="termwrap"><div class="term">'
             '<div class="bar"><i></i><i></i><i></i><span>자율 실행(CLI)</span></div>'
             '<div class="tbody">'
             '<div class="cmd"><b>&rsaquo;</b>겨울 자립 캠페인을 기획부터 배너 시안까지 진행해 줘</div>'
             '<div class="ok"><i>&check;</i>캠페인_기획.docx 작성</div>'
             '<div class="ok"><i>&check;</i>카피 3안 작성</div>'
             '<div class="ok"><i>&check;</i>상세페이지 구성 작성</div>'
             '<div class="ok"><i>&check;</i>배너 시안 4장 생성</div>'
             '<div class="fin"><i>&#9679;</i>완료: 결과를 확인해 주세요</div>'
             '</div></div></div>'
             '<p class="rcap">지시문과 파일명은 가상 예시입니다.</p>')
    return split_slide(24, "워크플로우",
        '버전 3. <span class="gt">업무 위임하기</span>', "버전 3. 업무 위임하기",
        "흐름 전체를 AI에게 맡기는 방식입니다.",
        [("지시는 한 번입니다", "캠페인 목표와 참고 자료를 처음에 전달합니다."),
         ("중간 산출물도 남습니다", "기획, 카피, 구성, 시안이 각각 파일로 저장됩니다."),
         ("사람은 마지막에 검수합니다", "완성된 묶음을 보고 고칠 곳만 AI에게 알려 줍니다.")],
        right, '<i class="aur a3"></i>')

def s25():
    def col(no, title, items):
        lis = "".join(f'<li><b>{i:02d}</b>{t}</li>' for i, t in enumerate(items, 1))
        return f'<div class="tocol"><h3><b>{no}</b>{title}</h3><ul>{lis}</ul></div>'
    c1 = col("STEP 1", "지금 바로", ["소식지와 카드뉴스 제작 시간 단축", "후원자 유형별 감사 메시지 변형", "행사 안내문과 보도자료 초안"])
    c2 = col("STEP 2", "다음 단계", ["월간 모금 성과 리포트 정리", "자주 오는 문의 답변 정리", "캠페인 문구 A안 B안 비교"])
    c3 = col("STEP 3", "내년", ["후원 데이터로 캠페인 시점 잡기", "내부 문서를 찾아 주는 검색 비서", "신규 후원자 환영 여정 설계"])
    inner = (f'<div class="vcen"><div class="toc">{c1}{c2}{c3}</div>'
             '<p class="lcap">전부 할 필요는 없습니다. 우리 일에 맞는 것부터 고르면 됩니다.</p></div>')
    return wide(25, "로드맵", '모금 재단의 더 많은 <span class="gt">활용 예시 로드맵</span>',
                "모금 재단의 더 많은 활용 예시 로드맵",
                "모금 재단이 더 시도해 볼 수 있는 활용 예시를 세 단계 로드맵으로 정리했습니다.", inner,
                '<i class="aur a1" style="width:700px;height:700px;right:-200px;top:-260px"></i>')

def s26():
    rules = [("개인정보는 넣지 않습니다", "후원자 실명과 연락처, 수혜자 사연 원문이 여기에 해당합니다. 이름을 빼고 요약해서 넣습니다."),
             ("내보내기 전에 대조합니다", "이름, 날짜, 금액을 원문 자료와 하나씩 맞춰 봅니다."),
             ("책임은 사람에게 있습니다", "AI가 쓴 초안도 보내는 순간 우리 글이 됩니다. 마지막 판단은 사람이 합니다.")]
    grid = "".join(f'<div class="tool"><span class="tno">{i:02d}</span><div><h4>{t}</h4><p>{d}</p></div></div>'
                   for i, (t, d) in enumerate(rules, 1))
    inner = (f'<div class="vcen"><div class="tools">{grid}</div>'
             '<p class="lcap">이 장은 출력해서 책상 앞에 붙여 두어도 좋습니다.</p></div>')
    return wide(26, "안전 수칙", 'AI를 안전하게 사용하기 위한 <span class="gt">세 가지 규칙</span>',
                "AI를 안전하게 사용하기 위한 세 가지 규칙",
                "후원자와 수혜자의 정보를 다루는 조직이므로, 이 세 가지는 꼭 지킵니다.", inner,
                '<i class="aur a4"></i>')

def s27():
    jobs = [("감사 편지 초안", "최근 후원 1건에 보낼 감사 편지 초안 요청"),
            ("보고서 요약", "최근 결과보고서 하나를 한 장으로 요약"),
            ("소식지 제목", "다음 소식지 제목 후보 5안 받기"),
            ("회의록 정리", "이번 주 회의 메모를 결정 사항 중심으로 정리"),
            ("안내문 다듬기", "쓰다 만 안내문을 따뜻한 존댓말로 다듬기"),
            ("아이디어 얻기", "다음 캠페인 아이디어 10개 받아 보기")]
    grid = "".join(f'<div class="job"><b>{i:02d}</b><h4>{t}</h4><p>{d}</p></div>'
                   for i, (t, d) in enumerate(jobs, 1))
    inner = (f'<div class="vcen"><div class="jobs">{grid}</div>'
             '<p class="lcap">잘 쓰려고 준비부터 할 필요는 없습니다. 지금 하던 일의 문장 하나면 충분합니다.</p></div>')
    return wide(27, "이번 주", '바로 <span class="gt">해볼 수 있는 것</span>', "바로 해볼 수 있는 것",
                "이 중 하나를 골라 이번 주에 한 번 써 보는 것이 시작입니다.", inner,
                '<i class="aur a2" style="right:-200px;top:-260px"></i>', kick1="NEXT")

def s28():
    HEADERS[28] = "일은 AI에게, 마음은 사람에게"
    body = ('<i class="aur a1"></i><i class="aur a3"></i>'
            f'{brandbar()}<div class="fg"><div class="vcen" style="align-items:center">'
            f'{kicker("OUTRO", "오늘의 결론")}'
            '<h2 style="font-size:104px;font-weight:800;letter-spacing:-.035em;line-height:1.2;text-align:center">'
            '일은 <span class="gt">AI에게</span>,<br>마음은 사람에게</h2>'
            '<p class="lead" style="text-align:center;max-width:1100px">반복되는 일은 AI에게 맡기고, 아낀 시간은 후원자와 수혜자를 마주하는 데 씁니다.</p>'
            '</div></div>')
    return slide(28, "split imp", body)

def s29():
    HEADERS[29] = "마무리"
    body = ('<i class="aur a2" style="right:-200px;top:-260px"></i><i class="aur a4"></i>'
            f'{brandbar()}<div class="fg"><div class="vcen" style="align-items:center">'
            f'{kicker("THANK YOU", "열매나눔재단 AI 온보딩")}'
            '<h2 style="font-size:120px;font-weight:800;letter-spacing:-.035em;text-align:center">감사합니다</h2>'
            '<p class="lead" style="text-align:center">오늘 고른 한 가지부터, 이번 주에 시작해 보시기를 바랍니다.</p>'
            '</div></div>')
    return slide(29, "split imp", body, credit=False)

# ── 보강 장 (추가 설명 슬라이드, 번호는 "본편-차수" 표기) ──
GEN = {k: img64(f"assets/{k}") for k in
       ["gen_kimchi.jpg", "gen_owner.jpg", "gen_sprout.jpg", "gen_office.jpg", "gen_boxes.jpg"]}

def supp(n, name, head_html, header_text, lead, inner, kick2="보강"):
    HEADERS[n] = header_text
    body = (f'{brandbar()}<div class="fg">'
            f'<div class="kicker"><span class="k1">PLUS</span> <span class="k2">/ {kick2}</span></div>'
            f'<h2 class="head">{head_html}</h2>'
            f'<p class="lead">{lead}</p>'
            f'{inner}</div>')
    return slide(n, "split", body)

def s2_1():
    inner = ('<div class="vcen"><div class="mosaic">'
             f'<div class="mo tall"><img src="{GEN["gen_sprout.jpg"]}" alt="캠페인 이미지 예시"></div>'
             f'<div class="mo"><img src="{GEN["gen_office.jpg"]}" alt="소식지 작업 예시"></div>'
             f'<div class="mo"><img src="{GEN["gen_boxes.jpg"]}" alt="현장 기록 예시"></div>'
             f'<div class="mo"><img src="{GEN["gen_kimchi.jpg"]}" alt="행사 콘텐츠 예시"></div>'
             f'<div class="mo"><img src="{GEN["gen_owner.jpg"]}" alt="인터뷰 콘텐츠 예시"></div>'
             '</div>'
             '<div class="mocap">'
             '<span><b>캠페인 이미지와 카드뉴스</b>: 이미 만들고 계신 결과물입니다.</span>'
             '<span><b>소식지와 현장 기록</b>: 오늘은 만드는 시간이 달라집니다.</span>'
             '<span><b>인터뷰와 사례 콘텐츠</b>: 오늘은 다루는 방식이 달라집니다.</span>'
             '</div>'
             '<p class="lcap">이미지는 AI로 만든 예시입니다. 실제 재단 산출물로 교체합니다.</p></div>')
    return supp("02-1", "갤러리", '<span class="gt">이미 만들고 있는</span> 것들', "이미 만들고 있는 것들",
                "이런 결과물은 재단에서 이미 만들고 있습니다. 오늘 달라지는 것은 만드는 속도와 다루는 방식입니다.",
                inner, "목차 보강")

def s4_1():
    steps = [("읽기", "지금까지 쓴 글 확인"),
             ("후보 나열", "다음에 올 글자 후보 추론"),
             ("확률 재기", "후보마다 점수 책정"),
             ("하나 선택", "1등만 고르지 않고 하나 뽑기"),
             ("반복", "문장이 끝날 때까지 반복")]
    nodes = "".join(f'<div class="stepn"><b>{i}</b><h4>{t}</h4><p>{d}</p></div>'
                    for i, (t, d) in enumerate(steps, 1))
    inner = ('<div class="vcen">'
             f'<div class="steps">{nodes}</div>'
             '<div class="stepband"><strong>앞 장의 시뮬레이션에서 본 것이 이 다섯 단계입니다.</strong> 이 과정이 눈 깜짝할 사이에 반복되면서 답변이 완성됩니다.</div>'
             '</div>')
    return supp("04-1", "플로우", '한 문장이 <span class="gt">완성되는 과정</span>', "한 문장이 완성되는 과정",
                "다섯 단계가 글자마다 반복됩니다.", inner, "원리 보강")

def s4_2():
    inner = ('<div class="vcen"><div class="ba">'
             '<div class="paper"><div class="ptag">첫 번째 대답</div>'
             '<div class="ptxt">"후원자님과 함께하는 김장 나눔의 계절이 돌아왔습니다."</div></div>'
             '<div class="baarrow"><span><i class="qb">Q</i></span></div>'
             '<div class="paper"><div class="ptag">두 번째 대답</div>'
             '<div class="ptxt">"올겨울, 김치 한 포기에 마음을 담아 이웃에게 전합니다."</div></div>'
             '</div>'
             '<p class="lcap">같은 질문 "김장 행사 안내문 첫 문장 써 줘"에 나온 두 답입니다. 둘 다 자연스럽고, 추론하여 나온 글자가 달라졌을 뿐입니다. 마음에 들 때까지 다시 요청해도 됩니다.</p></div>')
    return supp("04-2", "대비", '동일한 질문, <span class="gt">여러 가지 대답</span>', "동일한 질문, 여러 가지 대답",
                "1등만 고르지 않기 때문에 같은 질문에도 답이 달라집니다.", inner, "원리 보강")

def s5_1():
    steps = [("원문과 대조", "이름, 날짜, 금액을 재단 자료와 맞춰보기"),
             ("수치 검증", "출처 없는 수치는 직접 확인하기"),
             ("자료 전달", "원문 자료를 전달하면 지어내기가 크게 줄어듦")]
    nodes = "".join(f'<div class="stepn"><b>{i}</b><h4>{t}</h4><p>{d}</p></div>'
                    for i, (t, d) in enumerate(steps, 1))
    inner = ('<div class="vcen">'
             f'<div class="steps">{nodes}</div>'
             '<div class="stepband"><strong>중요한 글일수록 이 순서를 지킵니다.</strong></div>'
             '</div>')
    return supp("05-1", "플로우", '내보내기 전 <span class="gt">확인 세 가지</span>', "내보내기 전 확인 세 가지",
                "앞 장에서 본 확인 세 가지를 일하는 순서로 펼쳐 봅니다.", inner, "검토 보강")

def s6_1():
    inner = ('<div class="vcen"><div class="ba">'
             '<div class="paper"><div class="ptag">BEFORE</div>'
             '<div class="ptxt">감사 편지 써 줘</div></div>'
             '<div class="baarrow"><span><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span></div>'
             '<div class="paper after"><div class="ptag">AFTER (앞 장의 요청문)</div>'
             '<div class="ptxt"><em>여성가장의 자립을 돕는</em> <em>첫 정기후원을 시작하신 열매나눔재단 후원자님께</em> 보낼 감사 편지를 <em>따뜻한 존댓말로</em> 써 주세요.</div></div>'
             '</div>'
             '<p class="lcap">하이라이트한 부분이 앞 장에서 말한 우리의 사정입니다. 우리가 누구인지, 누구에게 보내는지, 어떤 말투로 쓸지, 이 세 정보를 알려 주는 것이 중요합니다.</p></div>')
    return supp("06-1", "대비", '프롬프트 내용 <span class="gt">상세 분석</span>', "프롬프트 내용 상세 분석",
                "앞 장의 요청문을 세 파트로 나눠 봅니다.", inner, "프롬프트 보강")

def s6_2():
    cards = [("무엇을 물을지", "업무를 아는 사람은 질문부터 구체적입니다"),
             ("무엇을 알려 줄지", "어떤 사정이 답을 바꾸는지 골라낼 수 있습니다"),
             ("무엇이 틀렸는지", "결과의 어색한 부분을 바로 알아봅니다")]
    grid = "".join(f'<div class="tool"><span class="tno">{i:02d}</span><div><h4>{t}</h4><p>{d}</p></div></div>'
                   for i, (t, d) in enumerate(cards, 1))
    inner = (f'<div class="vcen"><div class="tools">{grid}</div>'
             '<p class="lcap">프롬프트 기술보다 재단 일의 경험이 먼저입니다. 여러분이 쌓아 온 도메인 지식이 곧 AI를 다루는 능력입니다.</p></div>')
    return supp("06-2", "카드", 'AI를 다루는 능력의 차이 - <span class="gt">도메인 지식</span>',
                "AI를 다루는 능력의 차이 - 도메인 지식",
                "같은 AI를 써도 우리 일을 잘 아는 사람이 더 좋은 답을 얻습니다.", inner, "프롬프트 보강")

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

# ── 조립 ──
def build():
    # s2_1은 범위 규칙(보강 장은 본편 내용 확장 전용)에 따라 도입부에서 제외, s18 보강으로 이월 예정
    slides = [s1(), s2(), s3(), s4(), s4_1(), s4_2(), s5(), s5_1(),
              s6(), s6_1(), s6_2(), s7(), s8(), s9(), s10(),
              s11(), s12(), s13(), s14(), s15(), s16(), s17(), s18(), s19(), s20(),
              s21(), s22(), s23(), s24(), s25(), s26(), s27(), s28(), s29()]
    lint(slides)
    prose_gate(slides, "본덱", "--approve" in sys.argv)
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>열매나눔재단 AI 온보딩 / OSOMA</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
{"".join(slides)}
<script>
const fit=()=>document.documentElement.style.setProperty('--s',Math.min(innerWidth/1920,innerHeight/1080));
addEventListener('resize',fit);fit();
</script>
</body>
</html>"""
    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"✓ index.html 생성 ({len(html)//1024}KB, 슬라이드 {len(slides)}장 / 전체 {TOTAL}장 계획)")

if __name__ == "__main__":
    build()
