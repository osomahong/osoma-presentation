#!/usr/bin/env python3
"""오픈소스마케팅 회사 소개 덱 30장.

전 직원이 함께 보는 자리에서 쓴다. 무엇을 파는지가 아니라 무엇을 만드는지를 설명한다.
장 구성과 문장이 여기 있고, 색과 CSS는 deck_theme.py, 조각은 deck_parts.py 에 있다.

빌드: python3 build_deck.py [--approve] [--export] [--print]
  화면 문장이 바뀌면 교정대기_소개.txt 가 생기고 빌드가 멈춘다. 검수한 뒤 --approve 로 승인한다.
  화면에 보이는 글은 본문_소개.md 에 장별로 한 줄에 한 덩이씩 들어 있다.
"""
import sys
from pathlib import Path

from sync_text import sync
from toolbar import TOOLBAR_HTML
from deck_theme import CSS, TOTAL, HEADERS, lint, prose_gate, kicker, brandbar, grad_svg
from deck_parts import (P1, P2, P3, P4, P5, DEEP_CSS, ADD_CSS, ARROW,
                        icon, vs, stepflow, cards, paper, illus, toon, band)

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
.axstep{background:linear-gradient(150deg,#FFF7EF,#FBF2F8 45%,#F4F2FD 75%,#EFF5FE);border:1.5px solid #DFEAF2;border-radius:24px;padding:34px 32px 30px}
.axstep b{font-family:var(--fm);font-size:19px;font-weight:700;background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.axstep h4{font-size:27px;font-weight:800;margin:12px 0 10px}
.axstep p{font-size:20px;line-height:1.5;color:var(--dim)}
.axstep.today{position:relative;box-shadow:0 18px 46px rgba(40,50,80,.10)}
.axstep.today::after{content:"TODAY";position:absolute;top:-16px;right:22px;font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.16em;color:#fff;background:var(--grad);padding:6px 16px;border-radius:999px}
.axband{background:linear-gradient(90deg,#EAF4FC,#E8F6F3);border:1.5px solid #DFEAF2;border-radius:18px;padding:24px 36px;font-size:23px;line-height:1.6;color:var(--dim)}
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
.embnote{font-size:20px;line-height:1.6;color:var(--dim);background:linear-gradient(150deg,#FFF7EF,#F4F2FD 70%,#EFF5FE);border:1.5px solid #DFEAF2;border-radius:18px;padding:22px 26px}
.embnote strong{color:var(--ink);font-weight:800}

/* 갈무리가 여덟 장이라 머리말이 크면 판이 낮아진다. 이 장에서만 제목과 리드를 한 단계 줄인다 */
.slide:has(.hypewrap) h2.head{font-size:56px}
.slide:has(.hypewrap) .lead{font-size:23px;margin-top:18px}

/* 콘텐츠 갈무리 판. 판이 세로를 끝까지 쓰고, 카드는 남은 높이에 맞춰 커진다.
   카드 크기를 픽셀로 박으면 덱마다 머리말 높이가 달라 위아래가 남는다. */
.hypewrap{display:grid;grid-template-columns:.62fr 1.38fr;gap:44px;align-items:stretch;flex:1;min-height:0;margin-top:30px}
.hypetxt{display:flex;flex-direction:column;justify-content:center;padding:0 8px;min-width:0}
.hypetxt .hk{font-family:var(--fm);font-size:24px;font-weight:700;letter-spacing:.2em;color:#35B4C7;margin-bottom:26px}
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
.hf{background:linear-gradient(150deg,#FFF7EF,#F4F2FD 70%,#EFF5FE);border:1.5px solid #DFEAF2;
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


def furniture(n, clock):
    tl = f'<div class="clock">{clock}</div>' if clock else ''
    return (f'{brandbar()}{tl}'
            f'<div class="credit2">OPEN SOURCE MARKETING</div>'
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



DECK_CSS = """
/* 목차를 다섯 칸으로. 부가 다섯이라 세 칸 판으로는 자리가 모자란다 */
.toc.five{grid-template-columns:repeat(5,1fr);gap:18px;margin-top:44px;flex:1;align-content:center}
.toc.five .tocol{padding:28px 26px}
.toc.five .tocol h3{font-size:21px;margin-bottom:14px}
.toc.five .tocol h3 b{font-size:16px;margin-right:10px}
.toc.five .tocol li{font-size:18px;padding:8px 0;gap:12px}
.toc.five .tocol li b{font-size:14px}

/* 왼쪽에 이름표, 오른쪽에 사실을 줄로 세운다 */
.infolist{background:#fff;border:1.5px solid var(--line);border-radius:24px;padding:14px 34px;
  box-shadow:0 14px 40px rgba(40,50,80,.07)}
.inforow{display:grid;grid-template-columns:150px minmax(0,1fr);gap:20px;align-items:baseline;
  padding:17px 0;border-top:1px solid var(--line2)}
.inforow:first-child{border-top:none}
.inforow b{font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.1em;color:var(--faint)}
.inforow span{font-size:20px;line-height:1.5;color:var(--ink);font-weight:600}

/* 숫자 판. 넷이나 셋을 나란히 놓는다 */
.facts{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;flex:1;align-content:center;margin-top:40px}
.facts.three{grid-template-columns:repeat(3,1fr)}
.fact{background:#fff;border:1.5px solid var(--line);border-radius:26px;padding:44px 38px;
  box-shadow:0 16px 44px rgba(40,50,80,.06)}
.fact b{display:block;font-family:var(--fm);font-size:76px;font-weight:700;line-height:1;letter-spacing:-.03em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.fact h4{margin-top:24px;font-size:24px;font-weight:800}
.fact p{margin-top:10px;font-size:18px;line-height:1.5;color:var(--dim)}

/* 연혁. 왼쪽에 연도, 오른쪽에 그 해에 한 일 */
.hist{display:flex;flex-direction:column;gap:26px;flex:1;justify-content:center;margin-top:34px}
.histrow{display:grid;grid-template-columns:200px minmax(0,1fr);gap:36px;align-items:start}
.histyear{font-family:var(--fm);font-size:52px;font-weight:700;line-height:1;letter-spacing:-.02em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.histyear em{display:block;margin-top:12px;font-family:var(--f);font-style:normal;font-size:17px;
  font-weight:600;color:var(--faint);letter-spacing:0}
.histitems{display:flex;flex-wrap:wrap;gap:10px 12px;padding-top:6px;border-top:1.5px solid var(--line)}
.histitems span{font-size:19px;line-height:1.4;color:var(--dim);background:#fff;border:1.5px solid var(--line);
  border-radius:999px;padding:9px 18px}
.histitems span.on{border:1.5px solid transparent;font-weight:700;color:var(--ink);
  background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}

/* 산업군 묶음. 연혁과 같은 판이되 왼쪽 이름표가 한글이라 크기를 줄인다 */
.hist.grp .histyear{font-family:var(--f);font-size:29px;font-weight:800;line-height:1.3;letter-spacing:-.01em}
.hist.grp .histyear em{margin-top:9px;font-family:var(--fm);font-size:15px;letter-spacing:.08em}
.hist.grp .histitems span{font-size:18px;padding:8px 16px}

/* 조직도. 위에 대표, 아래에 본부와 팀 */
.org{display:flex;flex-direction:column;align-items:center;gap:0;flex:1;justify-content:center;margin-top:26px}
.orgtop{padding:18px 54px;border-radius:999px;font-size:24px;font-weight:800;color:#fff;background:var(--grad);
  box-shadow:0 14px 34px rgba(40,120,180,.28)}
.orgline{width:2px;height:34px;background:var(--line)}
.orgmid{display:flex;gap:26px}
.orgmid div{padding:14px 38px;border-radius:999px;font-size:20px;font-weight:700;color:var(--ink);
  background:#fff;border:1.5px solid var(--line)}
.orgcols{display:grid;grid-template-columns:1fr 1fr;gap:32px;width:100%;max-width:1300px;margin-top:34px}
.orgcol{background:#fff;border:1.5px solid var(--line);border-radius:24px;padding:32px 36px;
  box-shadow:0 14px 40px rgba(40,50,80,.06)}
.orgcol h4{font-size:26px;font-weight:800}
.orgcol ul{list-style:none;margin-top:18px;display:flex;flex-direction:column;gap:11px}
.orgcol li{font-size:19.5px;line-height:1.45;color:var(--dim);padding-left:22px;position:relative}
.orgcol li::before{content:"";position:absolute;left:0;top:11px;width:8px;height:8px;border-radius:50%;background:var(--grad)}

/* 단계가 여섯이면 판이 넘친다. 그 장에서만 글자와 여백을 한 단계 줄인다 */
.hflow:has(.hstep:nth-child(6)) .hstep{padding:9px 0;gap:20px}
.hflow:has(.hstep:nth-child(6)) .hstep b{width:40px;height:40px;font-size:16px}
.hflow:has(.hstep:nth-child(6)) .hstep::before{left:20px;top:51px}
.hflow:has(.hstep:nth-child(6)) .hstep h4{font-size:22.5px;margin-top:6px}
.hflow:has(.hstep:nth-child(6)) .hstep p{font-size:17.5px;line-height:1.5}
.howto:has(.hstep:nth-child(6)) .hf{padding:26px 30px}
.howto:has(.hstep:nth-child(6)) .hf b{font-size:30px}

/* 마무리 */
.ax-end .fg{justify-content:center;gap:38px;align-items:flex-start}
.ax-end h2{font-size:84px;font-weight:800;letter-spacing:-.035em;line-height:1.2}
.ax-end .endsub{font-size:27px;color:var(--dim);line-height:1.6;max-width:1180px}
.ax-end .endcontact{display:flex;gap:16px;margin-top:14px}
.ax-end .endcontact span{font-family:var(--fm);font-size:20px;letter-spacing:.04em;color:var(--dim);
  border:1.5px solid var(--line);border-radius:999px;padding:13px 28px;background:#fff}
"""


def _tools(items, cls=""):
    body = "".join(f'<div class="tool"><span class="tno">{i:02d}</span><div><h4>{t}</h4><p>{d}</p></div></div>'
                   for i, (t, d) in enumerate(items, 1))
    return f'<div class="tools {cls}">{body}</div>'


def _facts(items, cls=""):
    body = "".join(f'<div class="fact"><b>{b}</b><h4>{t}</h4><p>{d}</p></div>' for b, t, d in items)
    return f'<div class="facts {cls}">{body}</div>'


def _info(rows):
    return ('<div class="infolist">'
            + "".join(f'<div class="inforow"><b>{k}</b><span>{v}</span></div>' for k, v in rows)
            + '</div>')


def _rows(rows, cls=""):
    """왼쪽 이름표, 오른쪽 칩 목록. 연혁과 산업군이 같은 판을 쓴다."""
    out = []
    for label, note, items in rows:
        chips = "".join(f'<span class="{c}">{t}</span>' for t, c in items)
        out.append(f'<div class="histrow"><div class="histyear">{label}<em>{note}</em></div>'
                   f'<div class="histitems">{chips}</div></div>')
    return f'<div class="hist {cls}">{"".join(out)}</div>'


# ══ 표지와 차례 ════════════════════════════════════════════════════════

def s_cover(n):
    HEADERS[n] = "다섯 명이 네 해 동안 한 일"
    aur = '<i class="aur a1"></i><i class="aur a2"></i><i class="aur a3"></i><i class="aur a4"></i>'
    sig = ('<svg class="signal" viewBox="0 0 660 660">'
           f'<defs>{grad_svg("sg")}</defs>'
           '<circle class="ring" cx="330" cy="330" r="80" fill="none" stroke="url(#sg)" stroke-width="2.5" opacity=".95"/>'
           '<circle class="ring" cx="330" cy="330" r="160" fill="none" stroke="url(#sg)" stroke-width="2.5" opacity=".62"/>'
           '<circle class="ring" cx="330" cy="330" r="240" fill="none" stroke="url(#sg)" stroke-width="2.5" opacity=".4"/>'
           '<circle class="ring" cx="330" cy="330" r="320" fill="none" stroke="url(#sg)" stroke-width="2.5" opacity=".22"/>'
           '<circle class="rip" cx="330" cy="330" r="300" fill="none" stroke="url(#sg)" stroke-width="3"/>'
           '<circle class="rip r2" cx="330" cy="330" r="300" fill="none" stroke="url(#sg)" stroke-width="3"/>'
           '<circle cx="330" cy="330" r="14" fill="url(#sg)"/></svg>')
    body = (f'{aur}{sig}<div class="fg">'
            '<h1>다섯 명이 네 해 동안<br><span class="gt">53건을 했습니다</span></h1>'
            '<p class="sub">무엇을 했고, 누구와 했고, 국가 지원사업을 어떻게 굴리고 있고, '
            'AI를 어디까지 쓰고 있고, 어디로 가는지 순서대로 봅니다.</p>'
            '<div class="mchips"><span><b>53</b> 프로젝트</span><span><b>24</b> 개사 동시 운영</span>'
            '<span><b>3</b> 년 연속 국가사업</span></div>'
            '</div>')
    return ax(n, "ax-cover", body, "OPEN SOURCE MARKETING / COMPANY DECK")


def s_toc(n):
    HEADERS[n] = "오늘 다룰 다섯 가지"
    cols = [("PART 1", "그동안 한 일",
             ["회사 개요", "네 갈래의 일", "남기는 결과물", "구축 여섯 단계", "그로스가 푸는 문제", "연혁"]),
            ("PART 2", "고객사와 산업군",
             ["53건을 넷으로", "유통과 커머스", "IT와 금융", "교육과 공공", "제조와 서비스"]),
            ("PART 3", "지원사업 운영",
             ["3년째 맡은 사업", "판을 까는 법", "일정이 안 엉키는 이유", "주간 운영",
              "진행률 기준표", "공사 보고 세 층", "3년치 운영"]),
            ("PART 4", "AI를 쓰는 수준",
             ["일의 성격이 바뀜", "AI를 심는 순서", "실제로 까는 것", "기업이 쓰는 도구",
              "구독 설계", "우리 일에도"]),
            ("PART 5", "앞으로",
             ["두 갈래", "AX를 주력으로", "도구를 제품으로", "마무리"])]
    html = "".join(
        f'<div class="tocol"><h3><b>{no}</b>{title}</h3><ul>'
        + "".join(f'<li><b>{i:02d}</b>{x}</li>' for i, x in enumerate(items, 1))
        + '</ul></div>' for no, title, items in cols)
    inner = f'<div class="toc five">{html}</div>'
    return wide(n, P1, "오늘의 차례", '<span class="gt">다섯 가지</span>를 순서대로 봅니다',
                "오늘 다룰 다섯 가지",
                "한 일과 고객사를 먼저 놓고, 국가 지원사업 운영과 AI 활용을 자세히 본 뒤, 앞으로로 마칩니다.",
                inner, "")


# ══ 1부 그동안 한 일 ═══════════════════════════════════════════════════

def s_intro(n):
    rows = [("회사명", "주식회사 오픈소스마케팅"),
            ("설립일", "2020년 12월 14일"),
            ("대표이사", "오승종"),
            ("업종", "경영 컨설팅업, 광고 대행업, 마케팅 교육업, 응용 소프트웨어 개발 및 공급"),
            ("소재지", "서울특별시 강남구 봉은사로37길 5, 4층"),
            ("연락", "contact@osoma.kr / osoma.kr")]
    points = [("컨설팅 회사이면서 개발 회사입니다",
               "응용 소프트웨어 개발과 공급이 업종에 들어 있습니다. 자체 분석 도구를 직접 만듭니다."),
              ("교육이 부업이 아닙니다",
               "마케팅 교육업이 별도 업종으로 등록되어 있습니다. 넘기는 일까지가 사업입니다."),
              ("2020년 12월에 시작했습니다",
               "본격적인 프로젝트는 2022년부터 연혁에 쌓였습니다.")]
    return split(n, P1, "회사", '등본에 적힌 <span class="gt">오픈소스마케팅</span>',
                 "등본에 적힌 오픈소스마케팅",
                 "업종 네 가지가 회사의 성격을 그대로 보여 줍니다. 컨설팅과 광고, 교육, 그리고 소프트웨어입니다.",
                 points, _info(rows), "")


def s_did_what(n):
    HEADERS[n] = "우리가 실제로 한 네 갈래의 일"
    items = [("분석 환경 구축", "웹과 앱에서 무엇을 셀지 정하고, 태깅을 걸고, 대시보드까지 놓습니다. 53건 가운데 가장 많습니다."),
             ("그로스 마케팅", "매체와 자사몰을 진단하고 가설을 세워 실험을 돌립니다. 실행까지 함께 붙습니다."),
             ("교육과 지원사업 운영", "기업 출강과 온라인 강의를 하고, 국가 지원사업의 운영사를 맡습니다."),
             ("AX 컨설팅", "2025년 말부터 들어온 일입니다. AI를 업무 순서 안에 넣고 도구를 붙입니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "갈래", "", icons=["chart", "target", "book", "bolt"])
             + band('네 갈래는 따로 팔린 적이 거의 없습니다. '
                    '<strong>분석을 깔고, 그 위에서 마케팅을 돌리고, 마지막에 교육으로 넘기는 한 덩어리였습니다.</strong>')
             + '</div>')
    return wide(n, P1, "한 일의 갈래", '네 갈래로 <span class="gt">53건</span>을 했습니다',
                "우리가 실제로 한 네 갈래의 일",
                "2022년부터 2025년까지 회사소개서 연혁에 적힌 프로젝트를 성격으로 묶었습니다.",
                inner, "")


def s_did_data(n):
    HEADERS[n] = "분석 환경 구축에서 남기는 여섯 가지"
    items = [("이벤트 정의서", "웹과 앱에서 무엇을 언제 세는지 적은 문서입니다. 뒤의 모든 것이 이 문서를 따릅니다."),
             ("스크립트 가이드", "개발자가 그대로 붙일 수 있게 쓴 dataLayer 코드 안내입니다."),
             ("GTM 태깅", "정의서대로 걸어 둔 태그와 트리거, 변수입니다."),
             ("디버깅 기록", "미리보기와 DebugView로 이벤트가 제대로 들어오는지 확인한 결과입니다."),
             ("Looker Studio 대시보드", "담당자가 매일 여는 화면입니다. 항목을 직접 더할 수 있게 만듭니다."),
             ("온보딩 교육", "직접 묻고 고치는 법을 익히는 자리입니다.")]
    inner = ('<div class="vcen">' + _tools(items)
             + band('교보문고도 신세계면세점도 안랩도 이 여섯 가지를 받고 끝났습니다. '
                    '<strong>업종이 달라도 넘기는 것의 목록은 같습니다.</strong>')
             + '</div>')
    return wide(n, P1, "결과물", '매번 <span class="gt">같은 여섯 가지</span>를 남깁니다',
                "분석 환경 구축에서 남기는 여섯 가지",
                "53건에서 가장 많이 반복된 일이고, 표준화의 뿌리입니다.",
                inner, "")


def s_did_steps(n):
    HEADERS[n] = "구축이 지나는 여섯 단계"
    flow = [("무엇을 셀지 정합니다",
             "화면을 함께 보며 성과로 셀 행동을 고릅니다. 여기서 고르지 않은 것은 나중에 볼 수 없습니다."),
            ("정의서로 적습니다",
             "이벤트 이름과 매개변수, 발생 조건을 표로 적습니다. 개발과 마케팅이 같은 문서를 봅니다."),
            ("스크립트와 태깅을 겁니다",
             "개발이 dataLayer를 심고, 우리가 GTM에서 태그와 트리거를 붙입니다."),
            ("검수합니다",
             "미리보기와 DebugView로 누락과 중복을 잡습니다. 여기서 걸러야 대시보드가 거짓말을 하지 않습니다."),
            ("대시보드를 만듭니다",
             "Looker Studio에 지표를 배치합니다. 담당자가 항목을 더할 수 있는 구조로 둡니다."),
            ("넘깁니다",
             "정의서 읽는 법과 태그 고치는 법을 온보딩으로 옮깁니다.")]
    facts = [("고정", "6단계", "업종이 달라도 순서가 바뀌지 않습니다"),
             ("핵심", "정의서", "네 번째 단계까지가 정의서를 지키는 일입니다"),
             ("끝", "온보딩", "고치는 법을 넘기지 못하면 반년 뒤 다시 깨집니다")]
    inner = ('<div class="vcen">' + howto(flow, facts)
             + band('순서를 지키는 것이 원리입니다. '
                    '<strong>무엇을 셀지 먼저 정하지 않으면 태깅은 매번 다시 하게 됩니다.</strong>')
             + '</div>')
    return wide(n, P1, "일하는 순서", '정하고, 적고, 걸고, <span class="gt">검수하고</span>, 넘깁니다',
                "구축이 지나는 여섯 단계",
                "여섯 결과물이 이 순서에서 하나씩 나옵니다.",
                inner, "")


def s_did_growth(n):
    HEADERS[n] = "그로스 마케팅에서 푸는 문제"
    items = [("전환이 안 나옵니다", "자사몰 고객 행동을 보고 매체 운영과 CRM을 함께 손봅니다. 안국건강과 이너시아가 그랬습니다."),
             ("무엇을 KPI로 둘지 모릅니다", "현황을 훑어 지표 한두 개로 좁히고 가설을 세웁니다. 커버링이 그랬습니다."),
             ("자연 유입이 줄었습니다", "CMS 이관에 맞춰 테크니컬 SEO를 점검하고 가이드를 만듭니다. 서울관광재단이 그랬습니다."),
             ("조직이 못 따라옵니다", "채널 운영 가이드를 만들고 마인드셋 내재화까지 갑니다. KOTRA가 그랬습니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "문제", "", icons=["alert", "flag", "search", "users"])
             + band('전략 문서만 넘기고 끝난 건은 드뭅니다. '
                    '<strong>매체를 함께 돌리고 결과를 읽는 데까지 붙어 있습니다.</strong>')
             + '</div>')
    return wide(n, P1, "그로스 마케팅", '풀어 달라고 <span class="gt">불려 온 자리</span>들입니다',
                "그로스 마케팅에서 푸는 문제",
                "회사소개서 레퍼런스에 적힌 과제를 문제 유형으로 묶었습니다.",
                inner, "")


def s_hist(n):
    HEADERS[n] = "2020년부터 2025년까지"
    rows = [("2020", "12월 14일 설립", [("주식회사 오픈소스마케팅 설립", "on")]),
            ("2022", "프로젝트 9건", [("KOTRA", "on"), ("서울관광재단 SEO", ""), ("신한S브릿지 8기와 9기", ""),
                                  ("인프런 강의 2종", "on"), ("브랜든", ""), ("마켓올슨", ""),
                                  ("로위", ""), ("메디트리", "")]),
            ("2023", "프로젝트 14건", [("교보문고", "on"), ("신세계면세점", "on"), ("KT 알파", ""),
                                   ("동원디어푸드", ""), ("더플라자 호텔", ""), ("ABC마트", ""),
                                   ("대림 e편한세상", ""), ("키플링, 이스트팩", ""), ("위닉스", ""),
                                   ("지란지교소프트", ""), ("신세계사이먼", ""), ("씨티닷츠", "")]),
            ("2024", "프로젝트 14건", [("한국관광공사 지원사업", "on"), ("안랩", "on"), ("반다이남코코리아", "on"),
                                   ("경동나비엔", ""), ("스케쳐스코리아", ""), ("오픈서베이", ""),
                                   ("파크시스템스", ""), ("고려대학교", ""), ("이투스에듀", ""),
                                   ("신한퓨처스랩", ""), ("풀무원녹즙", ""), ("원밀리언", "")]),
            ("2025", "프로젝트 16건", [("한국관광공사 지원사업", "on"), ("LG CNS", "on"),
                                   ("베스핀글로벌 AI 리드 스코어링", "on"), ("남유 FNC AI 광고 대시보드", "on"),
                                   ("뤼튼테크놀로지", ""), ("열매나눔재단", ""), ("푸르메재단", ""),
                                   ("연세대학교", ""), ("한림대학교", ""), ("소브린", "")])]
    return wide(n, P1, "연혁", '네 해 동안 <span class="gt">53건</span>이 쌓였습니다',
                "2020년부터 2025년까지",
                "2026년 2월 회사소개서 연혁을 연도로 묶었습니다. 칸에 다 담기지 않은 건은 생략했습니다.",
                _rows(rows), "")


# ══ 2부 고객사와 산업군 ════════════════════════════════════════════════

def s_ind_overview(n):
    HEADERS[n] = "고객사를 네 갈래로 묶으면"
    items = [("53", "프로젝트", "2022년부터 2025년까지 연혁에 적힌 건수입니다."),
             ("4", "산업군", "유통, IT와 금융, 교육과 공공, 제조와 서비스입니다."),
             ("18", "가장 넓은 갈래", "제조와 서비스, 비영리를 합한 수입니다."),
             ("3", "연속 재의뢰", "한국관광공사 지원사업을 세 해 연속 맡고 있습니다.")]
    inner = _facts(items)
    return wide(n, P2, "산업군 개요", '한 업종에 <span class="gt">묶이지 않았습니다</span>',
                "고객사를 네 갈래로 묶으면",
                "대기업 유통부터 대학, 정부기관, 스타트업까지 섞여 있습니다.",
                inner, "")


def s_ind_retail(n):
    HEADERS[n] = "유통과 커머스 열두 곳"
    rows = [("종합 플랫폼", "도서, 면세, 완구", [("교보문고", "on"), ("신세계면세점", "on"),
                                          ("반다이남코코리아", "on"), ("신세계사이먼", "")]),
            ("패션과 리테일", "매장과 자사몰", [("ABC마트", ""), ("스케쳐스코리아", ""),
                                        ("키플링, 이스트팩", ""), ("씨티닷츠, 던스트", ""), ("마켓올슨", "")]),
            ("식품과 리빙", "정기 배송과 구독", [("동원디어푸드", ""), ("레시피그룹, 세터", ""), ("메터그룹, 몽디에스", "")])]
    inner = (_rows(rows, "grp")
             + band('공통점은 웹과 앱을 함께 쓰고 구매가 성과라는 것입니다. '
                    '<strong>이벤트 정의서의 뼈대가 서로 크게 다르지 않습니다.</strong>'))
    return wide(n, P2, "산업군", '<span class="gt">유통과 커머스</span>가 가장 익숙합니다',
                "유통과 커머스 열두 곳", "53건 가운데 12건이 여기에 들어갑니다.", inner, "")


def s_ind_it(n):
    HEADERS[n] = "IT와 금융 열세 곳"
    rows = [("보안과 클라우드", "B2B 리드가 성과", [("안랩", "on"), ("LG CNS", "on"),
                                            ("베스핀글로벌", "on"), ("지란지교소프트", "")]),
            ("SaaS와 스타트업", "제품 안의 행동", [("뤼튼테크놀로지", ""), ("오픈서베이", ""),
                                          ("유니드컴즈, 킵그로우", ""), ("소브린, DBPR", "")]),
            ("금융과 액셀러레이팅", "포트폴리오 지원", [("신한퓨처스랩", ""), ("신한 글로벌 슛업", ""),
                                              ("신한S브릿지 8기와 9기", ""), ("KT 알파", "")])]
    inner = (_rows(rows, "grp")
             + band('B2B가 많아 성과가 구매가 아니라 문의와 상담입니다. '
                    '<strong>무엇을 전환으로 볼지 정하는 일부터 시작합니다.</strong>'))
    return wide(n, P2, "산업군", '<span class="gt">IT와 금융</span>이 가장 많습니다',
                "IT와 금융 열세 곳", "53건 가운데 13건이 여기에 들어갑니다.", inner, "")


def s_ind_public(n):
    HEADERS[n] = "교육과 공공 열 곳"
    rows = [("정부기관과 공공", "지원사업 운영 포함", [("한국관광공사", "on"), ("KOTRA", "on"),
                                            ("서울관광재단", "")]),
            ("대학", "입학과 홍보", [("고려대학교", ""), ("연세대학교", ""), ("한림대학교", "")]),
            ("교육 서비스", "온라인 강의 포함", [("이투스에듀", ""), ("인프런 강의 2종", "on")])]
    inner = (_rows(rows, "grp")
             + band('한국관광공사 지원사업은 2024년, 2025년, 2026년 세 해를 이어서 맡고 있습니다. '
                    '<strong>3부가 이 사업 이야기입니다.</strong>'))
    return wide(n, P2, "산업군", '<span class="gt">공공과 대학</span>도 함께 합니다',
                "교육과 공공 열 곳", "53건 가운데 10건이 여기에 들어갑니다.", inner, "")


def s_ind_rest(n):
    HEADERS[n] = "제조와 서비스, 비영리 열여덟 곳"
    rows = [("제조와 건설", "오프라인이 본업", [("경동나비엔", "on"), ("위닉스", ""),
                                       ("파크시스템스", ""), ("대림 e편한세상", ""), ("풀무원녹즙", "")]),
            ("서비스와 문화", "예약과 멤버십", [("더플라자 호텔", ""), ("원밀리언", ""),
                                       ("라그나로크 라틴아메리카", ""), ("로위", ""), ("메디트리", "")]),
            ("비영리", "후원이 성과", [("열매나눔재단", "on"), ("푸르메재단", "on")]),
            ("그 밖", "초기 단계와 광고", [("남유 FNC", ""), ("빅픽처팀", ""), ("티니어", ""),
                                    ("뭉클랩", ""), ("에프엠커뮤니케이션", ""), ("비플레인", "")])]
    inner = _rows(rows, "grp")
    return wide(n, P2, "산업군", '나머지 <span class="gt">열여덟 곳</span>이 가장 넓습니다',
                "제조와 서비스, 비영리 열여덟 곳",
                "53건 가운데 18건이 여기에 들어갑니다. 성과로 세는 것이 저마다 다릅니다.",
                inner, "")


# ══ 3부 지원사업을 운영하는 방식 ═══════════════════════════════════════

def s_kto_what(n):
    HEADERS[n] = "3년째 맡고 있는 국가 지원사업"
    items = [("24", "참여 기업", "2026년 사업 기준으로 동시에 굴러가는 기업 수입니다."),
             ("11", "컨설턴트", "우리 다섯 명에 파트너사 컨설턴트를 붙여 편성합니다."),
             ("4", "개월", "6월에 열어 9월과 10월에 닫습니다.")]
    inner = (_facts(items, "three")
             + band('개별 컨설팅과 하는 일은 크게 다르지 않습니다. '
                    '<strong>다른 것은 스물네 곳을 동시에 굴리면서 공사에 한 목소리로 보고하는 일입니다.</strong>'))
    return wide(n, P3, "사업 개요", '한국관광공사 <span class="gt">데이터와 AI 활용 지원사업</span>',
                "3년째 맡고 있는 국가 지원사업",
                "2024년, 2025년, 2026년 세 해 연속으로 운영사를 맡고 있습니다.",
                inner, "")


def s_kto_setup(n):
    points = [("기업 하나에 채널 하나를 엽니다",
               "채널 이름을 유형과 조와 기업명으로 통일합니다. 기업 담당자와 컨설턴트, 운영진이 한자리에 들어갑니다."),
              ("유형을 둘로 나눕니다",
               "유형 1은 분석 환경 구축, 유형 2는 광고 캠페인까지 갑니다. 유형별로 산출물과 회차가 다릅니다."),
              ("컨설턴트를 조로 묶습니다",
               "우리 인원만으로는 스물네 곳을 못 맡습니다. 파트너사 컨설턴트를 같은 규칙 아래 편성합니다.")]
    rows = [("운영 주관", "오픈소스마케팅"),
            ("PM과 운영", "CMO 1명, 운영 담당 2명"),
            ("컨설턴트", "오픈소스마케팅 4명, 파트너사 6명"),
            ("발주처", "한국관광공사 담당자 3명"),
            ("소통 자리", "기업별 채널 24개, 컨설턴트 공용 채널 1개"),
            ("기록 자리", "유형별 마스터 시트 2개, 기업별 구글 문서")]
    return split(n, P3, "판 깔기", '먼저 <span class="gt">자리를 정합니다</span>',
                 "사업을 여는 순간 정하는 것",
                 "사업이 열리면 가장 먼저 하는 일은 컨설팅이 아니라 자리를 정하는 일입니다.",
                 points, _info(rows), "")


def s_kto_sched(n):
    HEADERS[n] = "스물네 곳 일정이 엉키지 않는 이유"
    flow = [("컨설턴트가 미팅을 잡습니다",
             "기업 채널에서 담당자와 날짜를 정합니다. 여기까지는 각자 합니다."),
            ("공용 채널에 한 줄로 올립니다",
             "회차, 기업명, 날짜, 온라인인지 오프라인인지를 같은 형식으로 남깁니다."),
            ("전체 일정이 한자리에 쌓입니다",
             "스물네 곳의 회차 진도가 채널 하나를 훑으면 보입니다. 따로 취합하지 않습니다."),
            ("운영진이 빈 곳만 봅니다",
             "회차가 밀린 기업이 눈에 띄면 그 채널만 들어가 확인합니다.")]
    facts = [("형식", "한 줄", "회차와 기업명과 일시만 적습니다"),
             ("취합", "없음", "올리는 순간 취합이 끝납니다"),
             ("확인", "빈 곳", "전체를 보지 않고 밀린 곳만 봅니다")]
    inner = ('<div class="vcen">' + howto(flow, facts)
             + band('일정을 모으는 사람을 두지 않습니다. '
                    '<strong>올리는 형식을 통일해 두면 채널 하나가 곧 전체 일정표가 됩니다.</strong>')
             + '</div>')
    return wide(n, P3, "일정 관리", '모으지 않고 <span class="gt">쌓이게</span> 둡니다',
                "스물네 곳 일정이 엉키지 않는 이유",
                "회차 관리가 사업 운영에서 가장 자주 깨지는 자리입니다.",
                inner, "")


def s_kto_weekly(n):
    HEADERS[n] = "한 주가 도는 방식"
    flow = [("금요일 15시, 봇이 알립니다",
             "주간 이슈 기입 리마인드가 공용 채널에 자동으로 올라옵니다. 사람이 챙기지 않습니다."),
            ("월요일 11시까지 두세 줄을 씁니다",
             "기업별 구글 문서의 주간 요약 탭에 그 주에 한 일과 진행률을 적습니다."),
            ("운영진이 빈칸만 확인합니다",
             "월요일 오전에 안 채워진 곳에만 다시 알립니다."),
            ("월간 보고 자료로 바로 쌓입니다",
             "주간 요약이 모여 월간 이슈 공유 문서가 됩니다. 따로 만들지 않습니다.")]
    facts = [("주기", "주 1회", "금요일에 알리고 월요일에 마감합니다"),
             ("분량", "2~3줄", "길게 쓰라고 하면 아무도 안 씁니다"),
             ("함께", "진행률", "숫자 하나를 같이 적습니다")]
    inner = ('<div class="vcen">' + howto(flow, facts)
             + band('주간 보고를 짧게 자른 것이 핵심입니다. '
                    '<strong>두세 줄이라 매주 채워지고, 매주 채워지니 월간 보고가 저절로 만들어집니다.</strong>')
             + '</div>')
    return wide(n, P3, "주간 운영", '금요일에 알리고 <span class="gt">월요일에 닫습니다</span>',
                "한 주가 도는 방식",
                "스물네 곳의 진행 상황이 매주 같은 자리에 같은 모양으로 쌓입니다.",
                inner, "")


def s_kto_rate(n):
    rows = [("60%", "이벤트 정의서 확정, 수집 구조 설계 완료"),
            ("70%", "스크립트 설치와 이벤트 세팅, 검수 진행"),
            ("80%", "분석 도구와 AI 자연어 분석 환경 설정 완료"),
            ("90%", "시각화 대시보드 제작, AI 자동 리포트 워크플로우 구축"),
            ("100%", "내재화 교육 완료, 산출물 인계")]
    points = [("숫자를 감으로 적지 않습니다",
               "진행률 기준표를 만들어 두고 그 단계에 닿았을 때만 숫자를 올립니다."),
              ("컨설턴트가 달라도 같은 값이 나옵니다",
               "파트너사 컨설턴트가 섞여 있어도 70퍼센트의 뜻이 같습니다."),
              ("멈춘 자리가 드러납니다",
               "여러 주 같은 숫자에 머물면 어느 단계에서 막혔는지 바로 보입니다.")]
    return split(n, P3, "진행률", '<span class="gt">70퍼센트</span>가 무엇인지 정해 둡니다',
                 "진행률을 숫자로 맞추는 법",
                 "진행률은 적는 사람마다 다르게 씁니다. 그래서 단계마다 뜻을 적어 둡니다.",
                 points, _info(rows), "")


def s_kto_report(n):
    HEADERS[n] = "공사에 보고하는 세 층"
    items = [("주간", "기업별 구글 문서의 주간 요약 탭. 두세 줄과 진행률입니다. 컨설턴트가 직접 씁니다."),
             ("월간", "한국관광공사 서울센터에서 대면 보고. 유형별 마스터 시트가 자료입니다. 참석 인원과 차량까지 미리 취합합니다."),
             ("차수별", "유형 2는 캠페인 계획서를 먼저 내고 집행 뒤 결과보고서를 냅니다. 봇이 D-7과 D-2에 알립니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "층", "three", icons=["clock", "flag", "file"])
             + band('세 층이 같은 자료를 쓴다는 것이 중요합니다. '
                    '<strong>주간 요약이 월간 보고가 되고, 차수별 결과보고서가 최종 성과가 됩니다.</strong>')
             + '</div>')
    return wide(n, P3, "성과 보고", '주간, 월간, <span class="gt">차수별</span>로 나눕니다',
                "공사에 보고하는 세 층",
                "보고 주기마다 문서를 새로 만들면 스물네 곳을 감당할 수 없습니다.",
                inner, "")


def s_kto_change(n):
    HEADERS[n] = "바뀌는 것을 다루는 방식"
    rows = [(("바뀌면 메일이나 전화로 알립니다", "누가 언제 무엇을 바꿨는지 흩어집니다"),
             ("스레드 하나에 모읍니다", "기업명과 바뀐 내용, 사유를 같은 형식으로 답니다")),
            (("KPI를 컨설턴트가 판단합니다", "기업 사정이 바뀌면 지표가 조용히 달라집니다"),
             ("KPI 변경은 사유를 적어 올립니다", "제외하거나 추가하는 이유를 적고 공사가 확인합니다")),
            (("계획서는 처음 한 번만 씁니다", "실제 진행과 문서가 어긋난 채로 끝납니다"),
             ("계획서를 시점마다 갱신합니다", "AI 컨설팅 수행계획서와 프로젝트 계획서를 함께 고칩니다"))]
    inner = ('<div class="vcen">' + vs("흔한 방식", "이 사업에서 하는 방식", rows)
             + band('사업이 넉 달이면 계획이 반드시 바뀝니다. '
                    '<strong>바뀌는 것을 막는 대신 바뀐 자리를 한곳에 남깁니다.</strong>')
             + '</div>')
    return wide(n, P3, "변경 관리", '계획은 <span class="gt">바뀝니다</span>',
                "바뀌는 것을 다루는 방식",
                "지표와 계획이 바뀌는 것 자체는 문제가 아닙니다. 흔적이 남지 않는 것이 문제입니다.",
                inner, "")


def s_kto_years(n):
    HEADERS[n] = "세 해를 이어서 맡은 사업"
    rows = [("2024", "첫 운영", [("한국관광공사 데이터 마케팅 지원사업 운영", "on")]),
            ("2025", "두 번째", [("한국관광공사 데이터 마케팅 지원사업 운영", "on")]),
            ("2026", "세 번째, 진행 중", [("관광기업 데이터와 AI 활용 지원사업", "on"), ("참여 기업 24곳", ""),
                                   ("컨설턴트 11명", ""), ("유형 2 캠페인 집행", ""), ("AI 구독 지원", "")])]
    inner = (_rows(rows, "grp")
             + band('세 해 연속 같은 발주처가 다시 맡겼다는 것이 운영 성적입니다. '
                    '<strong>연도별 성과 수치는 사업 종료 보고서에 있으니 그 값을 받아 이 자리에 채웁니다.</strong>'))
    return wide(n, P3, "운영 이력", '<span class="gt">세 해</span> 연속 운영사입니다',
                "세 해를 이어서 맡은 사업",
                "회사소개서 연혁과 2026년 사업 기록에서 확인한 내용입니다.",
                inner, "")


# ══ 4부 지금 AI를 쓰는 수준 ════════════════════════════════════════════

def s_ai_shift(n):
    HEADERS[n] = "일의 성격이 바뀐 자리"
    rows = [(("분석 환경을 세워 주고 나옵니다", "무엇을 셀지 정하고 태깅을 걸어 두는 일이었습니다"),
             ("모아 둔 데이터로 판단까지 갑니다", "AI 리드 스코어링처럼 무엇이 유망한지 매기는 일이 들어왔습니다")),
            (("대시보드를 만들어 줍니다", "사람이 열어 보고 해석하는 화면이었습니다"),
             ("AI가 먼저 읽고 짚어 줍니다", "AI 광고 분석 대시보드처럼 어디를 볼지 도구가 먼저 말합니다")),
            (("도구 활용법을 가르칩니다", "GA4와 Looker Studio를 다루는 법이었습니다"),
             ("일하는 순서를 다시 짭니다", "AI를 어느 단계에 넣을지가 교육 주제가 되었습니다"))]
    inner = ('<div class="vcen">' + vs("2024년까지", "2025년 말부터", rows)
             + band('2025년 12월 연혁에 <strong>AI 리드 스코어링</strong>과 '
                    '<strong>AI 광고 분석 대시보드</strong>가 처음 들어왔습니다.')
             + '</div>')
    return wide(n, P4, "달라진 것", '맡는 일이 <span class="gt">판단 쪽으로</span> 옮겨 왔습니다',
                "일의 성격이 바뀐 자리",
                "같은 데이터를 다루지만 어디까지 맡는지가 달라졌습니다.",
                inner, "")


def s_ai_flow(n):
    HEADERS[n] = "고객사에 AI를 심는 다섯 단계"
    steps = [("현황 진단", "지금 누가 무엇에 쓰고 있는지 봅니다. 대개 개인이 챗봇 하나를 쓰는 상태입니다."),
             ("구독 설계", "어떤 도구를 몇 계정, 어느 요금제로 쓸지 정합니다. 예산과 정산 방식까지 함께 봅니다."),
             ("환경 구성", "실제 노트북에 도구를 깔고 데이터에 연결합니다. 이 단계를 대면으로 합니다."),
             ("스킬과 자동화", "반복 업무 하나를 골라 자동화합니다. 손을 움직이는 실습으로 넘깁니다."),
             ("내재화", "담당자가 새 업무에 스스로 붙일 수 있게 두고 나옵니다.")]
    inner = ('<div class="vcen">' + stepflow(steps, hot=(3,))
             + band('두 번째와 세 번째 단계가 다른 회사와 갈리는 자리입니다. '
                    '<strong>구독을 대신 설계하고 노트북 앞에 같이 앉습니다.</strong>')
             + '</div>')
    return wide(n, P4, "AI 컨설팅", '도구를 <span class="gt">깔아 주는 데까지</span> 갑니다',
                "고객사에 AI를 심는 다섯 단계",
                "쓰라고 말하는 것과 쓰게 만드는 것 사이에 이 다섯 단계가 있습니다.",
                inner, "")


def s_ai_install(n):
    HEADERS[n] = "현장에서 실제로 까는 것"
    items = [("Codex와 Claude Code", "터미널에서 도는 코딩 에이전트입니다. 기업 담당자 노트북에 함께 설치합니다."),
             ("GA4 연동", "GCP 서비스 계정 키를 만들어 붙입니다. 이걸 해야 AI가 실제 자료를 읽습니다."),
             ("GA4 자연어 분석 스킬", "말로 물으면 GA4를 조회해 답하는 스킬을 깝니다. 실데이터로 바로 시연합니다."),
             ("MCP 연결", "Claude에 영상 생성 도구 같은 외부 서비스를 붙여 한자리에서 돌게 합니다."),
             ("반복 업무 자동화", "그 회사가 매주 손으로 하던 일을 하나 골라 스크립트로 만듭니다."),
             ("대시보드와 자동 리포트", "Looker Studio 화면을 만들고 AI가 요약을 붙이는 흐름까지 잇습니다.")]
    inner = ('<div class="vcen">' + _tools(items)
             + band('설치가 곧 컨설팅입니다. '
                    '<strong>깔아 주지 않으면 GCP 키 발급에서 대부분 멈춥니다.</strong>')
             + '</div>')
    return wide(n, P4, "설치물", '말로 끝내지 않고 <span class="gt">깔아 놓고</span> 나옵니다',
                "현장에서 실제로 까는 것",
                "2026년 지원사업에서 기업마다 반복하고 있는 목록입니다.",
                inner, "")


def s_ai_stack(n):
    HEADERS[n] = "기업이 실제로 쓰는 도구"
    rows = [("대화형과 코딩", "가장 먼저 붙는 자리", [("Claude Max", "on"), ("ChatGPT Pro", "on"),
                                            ("Codex", "on"), ("Claude Code", "on")]),
            ("미디어 생성", "콘텐츠를 만드는 자리", [("Higgsfield", ""), ("Claude Design", ""),
                                          ("Canva", ""), ("캡컷", "")]),
            ("분석과 데이터", "숫자를 보는 자리", [("GA4", "on"), ("Google Tag Manager", ""),
                                        ("BigQuery", ""), ("Looker Studio", ""), ("Amplitude", "")])]
    inner = (_rows(rows, "grp")
             + band('도구를 정해 놓고 기업을 맞추지 않습니다. '
                    '<strong>무슨 일을 자동화할지 먼저 정하고 그 일에 맞는 요금제를 고릅니다.</strong>'))
    return wide(n, P4, "도구", '기업마다 <span class="gt">쓰는 것이 다릅니다</span>',
                "기업이 실제로 쓰는 도구",
                "2026년 지원사업 참여 기업이 고른 도구를 성격으로 묶었습니다.",
                inner, "")


def s_ai_sub(n):
    points = [("한도 안에서 조합을 짭니다",
               "기업당 지원 한도가 정해져 있습니다. 무엇을 몇 개월 쓸지 계산해 조합을 제안합니다."),
              ("쓰임에 맞춰 요금제를 고릅니다",
               "개발 목적이면 상위 요금제를, 가벼운 작업이면 기본 요금제 계정을 여러 개 붙입니다."),
              ("정산까지 같이 봅니다",
               "선불 충전이나 토큰 과금은 정산 절차에 맞지 않습니다. 플랜 단위 결제를 권합니다.")]
    rows = [("한도", "기업당 지원 금액이 정해져 있습니다"),
            ("기간", "사업 기간 안에 다 쓰도록 나눕니다"),
            ("방식", "플랜 단위 월 구독을 권합니다"),
            ("증빙", "영수증을 모아 사업 종료 때 냅니다"),
            ("바뀔 때", "도구를 바꾸면 사유를 적어 공사에 올립니다")]
    return split(n, P4, "구독 설계", '<span class="gt">무엇을 구독할지</span>도 컨설팅입니다',
                 "구독을 설계하는 일",
                 "AI 도입에서 예산을 어디에 쓸지 정하는 일이 생각보다 큰 자리입니다.",
                 points, _info(rows), "")


def s_ai_us(n):
    HEADERS[n] = "우리 일에도 AI를 씁니다"
    items = [("미팅 브리핑", "지난 기록과 시트를 읽혀 아젠다와 빈칸, 확인할 근거를 미리 뽑습니다."),
             ("미팅록 초안", "대화 기록에서 초안을 만들어 두고 사람이 빈칸을 채웁니다."),
             ("주간 요약 문안", "시트에 그대로 붙일 수 있는 문안을 만들어 둡니다."),
             ("자료 제작", "교육 덱과 시연물을 코드로 만들어 문장만 고치면 다시 빌드되게 둡니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "자리", "", icons=["eye", "editdoc", "pen", "toolbox"])
             + band('스물네 곳을 열한 명이 감당하는 힘이 여기서 나옵니다. '
                    '<strong>쓰라고 권하기 전에 우리 업무 순서 안에 먼저 넣었습니다.</strong>')
             + '</div>')
    return wide(n, P4, "내부 활용", '고객사에 권하기 전에 <span class="gt">먼저 씁니다</span>',
                "우리 일에도 AI를 씁니다",
                "AI를 파는 회사가 안에서 안 쓰면 컨설팅 자리에서 바로 드러납니다.",
                inner, "")


# ══ 5부 앞으로 ═════════════════════════════════════════════════════════

def s_next_two(n):
    HEADERS[n] = "앞으로 갈 두 갈래"
    items = [("AX를 주력으로", "분석과 마케팅 위에 AI를 얹는 일을 사업의 가운데로 옮깁니다."),
             ("도구를 제품으로", "안에서 쓰던 도구를 고객사가 직접 쓰는 물건으로 키웁니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "갈래", "three", icons=["bolt", "toolbox"])
             + band('둘은 따로 가는 길이 아닙니다. '
                    '<strong>AX 컨설팅에서 반복되는 일이 다음 제품의 재료가 됩니다.</strong>')
             + '</div>')
    return wide(n, P5, "방향", '두 갈래로 <span class="gt">함께</span> 갑니다',
                "앞으로 갈 두 갈래",
                "3부와 4부에서 안에서 했던 방식을 그대로 밖으로 넓히는 일입니다.",
                inner, "")


def s_next_ax(n):
    HEADERS[n] = "AX를 주력으로 옮기는 일"
    steps = [("분석은 바닥으로", "수집 구조를 세우는 일은 계속하되 그 위에 얹을 것을 봅니다."),
             ("업무 순서를 다시 짜기", "도구를 파는 대신 일하는 순서 안에 AI를 넣습니다."),
             ("전용 도구를 함께", "고객사 상황에 맞는 도구를 만들어 붙입니다."),
             ("역량을 넘기기", "담당자가 스스로 늘려 갈 수 있게 하고 손을 뗍니다.")]
    inner = ('<div class="vcen">' + stepflow(steps, hot=(2,))
             + band('AI를 도입했는지가 아니라 업무 시간과 결과물이 달라졌는지로 봅니다. '
                    '<strong>도입이 아니라 성과가 기준입니다.</strong>')
             + '</div>')
    return wide(n, P5, "갈래 하나", 'AI를 <span class="gt">업무 순서</span>에 넣는 일을 가운데로',
                "AX를 주력으로 옮기는 일",
                "우리가 안에서 먼저 해 본 순서를 고객사 안에서 다시 만듭니다.",
                inner, "")


def s_next_product(n):
    HEADERS[n] = "도구를 제품으로 키우는 일"
    rows = [(("컨설팅에 딸린 부속입니다", "우리가 프로젝트를 맡을 때만 돌아갑니다"),
             ("따로 서는 물건입니다", "고객사가 직접 열고 쓰는 화면이 됩니다")),
            (("쓰는 사람이 우리뿐입니다", "만든 사람만 아는 자리가 남아 있습니다"),
             ("모르는 사람이 씁니다", "설명 없이도 읽히도록 다듬어야 합니다")),
            (("프로젝트가 끝나면 멈춥니다", "매출이 사람 수에 묶여 있습니다"),
             ("일이 없어도 돌아갑니다", "사람을 늘리지 않고 닿는 곳을 넓힙니다"))]
    inner = ('<div class="vcen">' + vs("지금의 자체 도구", "제품이 되면", rows)
             + band('다섯 명이라는 조건이 바뀌지 않으니, '
                    '<strong>사람이 붙지 않아도 값을 내는 것을 늘리는 쪽으로 갑니다.</strong>')
             + '</div>')
    return wide(n, P5, "갈래 둘", '안에서 쓰던 것을 <span class="gt">밖으로</span> 냅니다',
                "도구를 제품으로 키우는 일",
                "OSOMA INSIGHT와 AD INSIGHT가 지금과 어떻게 달라져야 하는지 적었습니다.",
                inner, "")


def s_end(n):
    HEADERS[n] = "마무리"
    aur = '<i class="aur a2"></i><i class="aur a3"></i>'
    body = (f'{aur}<div class="fg">'
            '<h2>다섯 명이 스물네 곳을 굴리는 힘은<br><span class="gt">순서를 정해 둔 데서</span> 나옵니다</h2>'
            '<p class="endsub">결과물을 고정했고, 고정된 일을 도구로 만들었고, 그 위에 AI를 붙였습니다. '
            '앞으로도 사람을 늘리는 대신 남길 것을 늘리는 쪽으로 갑니다.</p>'
            '<div class="endcontact"><span>contact@osoma.kr</span><span>osoma.kr</span></div>'
            '</div>')
    return ax(n, "ax-end", body, "OPEN SOURCE MARKETING")


# ══ 조립 ═══════════════════════════════════════════════════════════════

ORDER = [s_cover, s_toc,
         s_intro, s_did_what, s_did_data, s_did_steps, s_did_growth, s_hist,
         s_ind_overview, s_ind_retail, s_ind_it, s_ind_public, s_ind_rest,
         s_kto_what, s_kto_setup, s_kto_sched, s_kto_weekly, s_kto_rate,
         s_kto_report, s_kto_change, s_kto_years,
         s_ai_shift, s_ai_flow, s_ai_install, s_ai_stack, s_ai_sub, s_ai_us,
         s_next_two, s_next_ax, s_next_product, s_end]


def print_freeze(html):
    """인쇄용 변환. 움직이는 것을 세워 둔다."""
    return html


def build():
    HEADERS.clear()
    assert len(ORDER) == TOTAL, f"장 수 {len(ORDER)}가 TOTAL {TOTAL}과 다르다"
    slides = [fn(i) for i, fn in enumerate(ORDER, 1)]
    slides = sync(slides, ROOT / "본문_소개.md", export="--export" in sys.argv)
    lint(slides)
    prose_gate(slides, "소개", "--approve" in sys.argv)
    prn = "--print" in sys.argv
    slides[-1] = slides[-1].replace('<div class="vp">', '<div class="vp last">', 1)
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>오픈소스마케팅 / 다섯 명이 네 해 동안 한 일</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap">
<style>{CSS}{EXTRA_CSS}{DEEP_CSS}{ADD_CSS}{DECK_CSS}</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{grad_svg("ig")}</defs></svg>
{"".join(slides)}
<script>
const fit=()=>document.documentElement.style.setProperty('--s',Math.min(innerWidth/1920,innerHeight/1080));
addEventListener('resize',fit);fit();
</script>
{TOOLBAR_HTML}
</body>
</html>"""
    out = "오픈소스마케팅_소개.html"
    if prn:
        html = print_freeze(html)
        out = "오픈소스마케팅_소개_인쇄.html"
    open(out, "w", encoding="utf-8").write(html)
    print(f"✓ {out} 생성 ({len(html)//1024}KB, {len(slides)}장)")


if __name__ == "__main__":
    build()
