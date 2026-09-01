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
from deck_parts import (P1, P2, P3, P4, DEEP_CSS, ADD_CSS, ARROW,
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
/* 목차를 네 칸으로. 부가 넷이라 세 칸 판으로는 한 칸이 남는다 */
.toc.four{grid-template-columns:repeat(4,1fr);gap:22px;margin-top:48px;flex:1;align-content:center}
.toc.four .tocol{padding:30px 30px}
.toc.four .tocol h3{font-size:22px;margin-bottom:16px}
.toc.four .tocol li{font-size:19px;padding:9px 0}

/* 기업 개요. 왼쪽에 요점 셋, 오른쪽에 등본에 적힌 사실을 줄로 세운다 */
.infolist{background:#fff;border:1.5px solid var(--line);border-radius:24px;padding:14px 34px;
  box-shadow:0 14px 40px rgba(40,50,80,.07)}
.inforow{display:grid;grid-template-columns:150px minmax(0,1fr);gap:20px;align-items:baseline;
  padding:17px 0;border-top:1px solid var(--line2)}
.inforow:first-child{border-top:none}
.inforow b{font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.1em;color:var(--faint)}
.inforow span{font-size:20px;line-height:1.5;color:var(--ink);font-weight:600}

/* 숫자 넉 장 */
.facts{display:grid;grid-template-columns:repeat(4,1fr);gap:28px;flex:1;align-content:center;margin-top:40px}
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

/* 마무리 */
.ax-end .fg{justify-content:center;gap:38px;align-items:flex-start}
.ax-end h2{font-size:84px;font-weight:800;letter-spacing:-.035em;line-height:1.2}
.ax-end .endsub{font-size:27px;color:var(--dim);line-height:1.6;max-width:1180px}
.ax-end .endcontact{display:flex;gap:16px;margin-top:14px}
.ax-end .endcontact span{font-family:var(--fm);font-size:20px;letter-spacing:.04em;color:var(--dim);
  border:1.5px solid var(--line);border-radius:999px;padding:13px 28px;background:#fff}
"""


# ══ 1부 우리는 어떤 회사인가 ═══════════════════════════════════════════

def s_cover(n):
    HEADERS[n] = "우리가 하는 일은 고객사의 홀로 서기"
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
            '<h1>우리가 하는 일은<br><span class="gt">고객사의 홀로 서기</span>입니다</h1>'
            '<p class="sub">오픈소스마케팅이 무엇을 하는 회사이고 어떤 가치를 만드는지 한 벌로 정리했습니다.</p>'
            '<div class="mchips"><span><b>2020</b> 설립</span><span><b>4</b> 사업 영역</span>'
            '<span><b>53</b> 프로젝트</span></div>'
            '</div>')
    return ax(n, "ax-cover", body, "OPEN SOURCE MARKETING / COMPANY DECK")


def s_toc(n):
    HEADERS[n] = "오늘 다룰 네 가지"
    cols = [("PART 1", "우리는 어떤 회사인가",
             ["한 문장 정의", "기업 개요", "목표는 홀로 서기", "핵심 가치 셋", "내재화의 뜻"]),
            ("PART 2", "우리가 하는 일",
             ["사업 영역 넷", "데이터 분석 컨설팅", "그로스 마케팅 컨설팅", "AX 컨설팅", "마케팅 및 분석 교육"]),
            ("PART 3", "일하는 방식과 결과물",
             ["남기는 결과물", "공통 진행 순서", "쓰는 도구", "고객을 읽는 세 축", "레퍼런스"]),
            ("PART 4", "지나온 자리와 사람",
             ["연혁", "숫자로 보기", "조직 구성", "우리가 만드는 가치", "마무리"])]
    html = "".join(
        f'<div class="tocol"><h3><b>{no}</b>{title}</h3><ul>'
        + "".join(f'<li><b>{i:02d}</b>{x}</li>' for i, x in enumerate(items, 1))
        + '</ul></div>' for no, title, items in cols)
    inner = f'<div class="toc four">{html}</div>'
    return wide(n, P1, "오늘의 차례", '오늘 <span class="gt">네 가지</span>를 봅니다',
                "오늘 다룰 네 가지",
                "회사를 한 문장으로 정의하고, 하는 일과 일하는 방식을 본 뒤, 지나온 자리와 사람으로 마칩니다.",
                inner, "")


def s_oneline(n):
    HEADERS[n] = "고객이 스스로 성장하는 구조 만들기"
    items = [("지식을 나눕니다", "우리가 아는 것을 감추지 않습니다. 컨설팅 자리에서 방법과 근거를 함께 꺼내 놓습니다."),
             ("구조를 만듭니다", "한 번의 성과가 아니라, 다음에도 같은 판단을 내릴 수 있는 순서와 기준을 남깁니다."),
             ("손을 뗍니다", "우리가 빠진 뒤에도 고객사가 스스로 굴릴 수 있을 때 일이 끝났다고 봅니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "원칙", "three", icons=["message", "network", "flag"])
             + band('오픈소스마케팅이 만드는 마케팅의 목표는 <strong>독립</strong>입니다. '
                    '단기 성과보다 지속 가능한 성장의 구조를 만드는 일에 집중합니다.')
             + '</div>')
    return wide(n, P1, "한 문장 정의", '우리는 <span class="gt">고객이 스스로 성장하는</span> 구조를 만듭니다',
                "고객이 스스로 성장하는 구조 만들기",
                "오픈소스마케팅은 고객이 스스로 성장할 수 있도록 곁에 서는 마케팅 파트너입니다.",
                inner, "")


def s_profile(n):
    rows = [("회사명", "주식회사 오픈소스마케팅"),
            ("설립일", "2020년 12월 14일"),
            ("대표이사", "오승종"),
            ("사업자번호", "697-81-02005"),
            ("업종", "경영 컨설팅업, 광고 대행업, 마케팅 교육업, 응용 소프트웨어 개발 및 공급"),
            ("소재지", "서울특별시 강남구 봉은사로37길 5, 4층"),
            ("연락", "contact@osoma.kr / osoma.kr")]
    right = ('<div class="infolist">'
             + "".join(f'<div class="inforow"><b>{k}</b><span>{v}</span></div>' for k, v in rows)
             + '</div>')
    points = [("컨설팅 회사이면서 개발 회사입니다",
               "응용 소프트웨어 개발과 공급이 업종에 함께 들어 있습니다. 자체 분석 도구를 직접 만듭니다."),
              ("교육이 부업이 아닙니다",
               "마케팅 교육업이 별도 업종으로 등록되어 있습니다. 내재화 교육은 사업의 한 축입니다."),
              ("서울 강남에 한 곳입니다",
               "사무실은 봉은사로37길 5, 4층 한 곳이고 컨설턴트가 고객사로 나갑니다.")]
    return split(n, P1, "기업 개요", '등본에 적힌 <span class="gt">오픈소스마케팅</span>',
                 "등본에 적힌 오픈소스마케팅",
                 "업종 네 가지가 회사의 성격을 그대로 보여 줍니다. 컨설팅과 광고, 교육, 그리고 소프트웨어입니다.",
                 points, right, "")


def s_independence(n):
    rows = [(("일이 끝나면 자료도 함께 떠납니다", "다음 과제가 오면 다시 밖에서 사람을 불러야 합니다"),
             ("일이 끝나면 방법이 남습니다", "정의서와 가이드, 대시보드가 고객사 안에 그대로 놓입니다")),
            (("무엇을 왜 그렇게 했는지는 컨설턴트만 압니다", "결과는 받았지만 판단의 근거는 넘어오지 않습니다"),
             ("판단의 근거를 함께 적어 둡니다", "같은 상황이 오면 담당자가 스스로 고를 수 있습니다")),
            (("성과가 좋으면 계약이 길어집니다", "의존이 깊어질수록 컨설팅 회사에 유리합니다"),
             ("역량이 붙으면 손을 뗍니다", "고객사가 홀로 설 수 있을 때를 끝으로 봅니다"))]
    inner = ('<div class="vcen">' + vs("흔히 보는 컨설팅", "오픈소스마케팅", rows)
             + band('우리의 컨설팅이 단기 성과에 그치지 않도록, '
                    '<strong>고객사가 스스로 이어 갈 수 있는 형태로</strong> 노하우를 넘깁니다.')
             + '</div>')
    return wide(n, P1, "기업 이념", '궁극적인 목표는 <span class="gt">고객사의 홀로 서기</span>',
                "궁극적인 목표는 고객사의 홀로 서기",
                "컨설팅이 끝난 날 무엇이 남는지가 두 방식을 가릅니다.",
                inner, "")


def s_values(n):
    HEADERS[n] = "우리를 움직이는 세 가지"
    items = [("나눔 Share", "각 분야 전문가가 모여 서로의 지식을 공유합니다. 안에서 나눈 것을 고객사에도 그대로 나눕니다."),
             ("연구 Study", "빠르게 바뀌는 디지털 시장을 끊임없이 살핍니다. 새 도구가 나오면 먼저 써 보고 판단합니다."),
             ("소통 Communication", "상황과 서비스에 맞는 방향을 함께 정합니다. 정답을 통보하지 않고 근거를 놓고 이야기합니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "가치", "three", icons=["users", "search", "message"])
             + band('디지털 시장이 어디로 가는지 한 발 앞서 살피고, '
                    '<strong>그 회사의 상황과 서비스에 맞는 방향</strong>을 제시합니다.')
             + '</div>')
    return wide(n, P1, "핵심 가치", '나눔, 연구, <span class="gt">소통</span>',
                "우리를 움직이는 세 가지",
                "회사 안에서 지키는 세 가지가 고객사 앞에서도 그대로 나옵니다.",
                inner, "")


def s_internalize(n):
    HEADERS[n] = "내재화가 끝났다고 말할 수 있는 상태"
    left = paper("컨설팅이 끝난 날, 이것만 남으면",
                 ["결과 보고서 한 부", "설정이 끝난 분석 도구", "우리가 만든 대시보드",
                  "다음 과제가 오면 다시 문의"], "그때뿐인 성과")
    right = paper("이렇게 남아야 내재화입니다",
                  ["무엇을 왜 세는지 적힌 정의서", "담당자가 고칠 수 있는 태깅 가이드",
                   "직접 항목을 더하는 대시보드", "새 과제를 스스로 설계"], "이어지는 역량", after=True)
    inner = ('<div class="vcen"><div class="balist">'
             + left + ARROW + right + '</div>'
             + band('일회성 결과가 아니라 지속적인 성과로 이어지도록, '
                    '<strong>내재화를 목표로 모든 컨설팅을 진행합니다.</strong>')
             + '</div>')
    return wide(n, P1, "내재화", '내재화는 <span class="gt">무엇이 남는가</span>로 판단합니다',
                "내재화가 끝났다고 말할 수 있는 상태",
                "역량이 붙었는지는 말로 확인하기 어렵습니다. 손에 남은 것으로 봅니다.",
                inner, "")


# ══ 2부 우리가 하는 일 ═════════════════════════════════════════════════

def s_areas(n):
    HEADERS[n] = "사업 영역 네 가지"
    items = [("데이터 분석 컨설팅", "웹과 앱의 이벤트 수집 구조를 설계하고, 분석 도구 세팅과 시각화 보고서까지 놓습니다."),
             ("그로스 마케팅 컨설팅", "디지털 마케팅 운영 현황을 진단하고, 최우선 과제와 실행 전략을 함께 정합니다."),
             ("AX 컨설팅", "막연한 AI 도입이 아니라 실제 성과로 이어지는 AI 전환 전략을 설계합니다."),
             ("마케팅 및 분석 교육", "고객사가 스스로 분석 방향을 찾고 마케팅을 최적화하도록 실습형 교육을 진행합니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "영역", "", icons=["chart", "target", "bolt", "book"])
             + band('네 영역은 따로 팔지 않습니다. '
                    '<strong>분석으로 목표를 수치화하고, 그 위에서 마케팅을 돌리고, AI로 속도를 올린 뒤, 교육으로 넘깁니다.</strong>')
             + '</div>')
    return wide(n, P2, "개요", '우리가 하는 일 <span class="gt">네 가지</span>',
                "사업 영역 네 가지",
                "데이터 수집부터 마케팅 전략 도출까지, 근거에 기반한 성장 경험을 제공합니다.",
                inner, "")


def _service(n, kicker2, head, header, lead, points, why_title, why_items):
    right = ('<div class="infolist">'
             f'<div class="inforow"><b>WHY OSOMA</b><span>{why_title}</span></div>'
             + "".join(f'<div class="inforow"><b>{i:02d}</b><span>{x}</span></div>'
                       for i, x in enumerate(why_items, 1))
             + '</div>')
    return split(n, P2, kicker2, head, header, lead, points, right, "")


def s_data(n):
    points = [("분석 도구를 고르는 일부터 시작합니다",
               "서비스 형태와 분석 목적에 맞는 도구를 먼저 정합니다. 도구가 정해져야 수집 구조가 정해집니다."),
              ("무엇을 셀지 문서로 남깁니다",
               "웹과 앱의 맞춤 이벤트 정의서를 씁니다. 이 문서가 있어야 개편 때 수집이 깨지지 않습니다."),
              ("보는 화면까지 만들어 둡니다",
               "시각화 대시보드를 만들어 담당자가 바로 열 수 있게 합니다.")]
    why = ["서비스 분석에 필요한 데이터 수집 구조 설계",
           "서비스 구조에 맞는 이벤트 세팅 가이드 작성",
           "분석 도구 활용법 온보딩 진행",
           "즉시 쓸 수 있는 시각화 보고서 대시보드 제공"]
    return _service(n, "데이터 분석 컨설팅",
                    '사용자 행동을 <span class="gt">읽을 수 있는 상태</span>로 만듭니다',
                    "사용자 행동을 읽을 수 있는 상태로 만들기",
                    "마케팅 성과 분석과 서비스 기획에 필요한 사용자 행동 분석 환경을 구축합니다.",
                    points, "이런 점이 다릅니다", why)


def s_data_flow(n):
    HEADERS[n] = "데이터 분석 컨설팅 다섯 단계"
    steps = [("데이터 수집 현황 점검", "지금 무엇이 어떻게 쌓이고 있는지 먼저 봅니다."),
             ("분석 구조 설계", "서비스 구조에 맞는 이벤트와 매개변수를 정의합니다."),
             ("분석 세팅", "GTM 태깅과 스크립트로 정의한 대로 수집을 겁니다."),
             ("시각화 대시보드 제작", "담당자가 매일 여는 화면을 만듭니다."),
             ("데이터 분석 활용 교육", "직접 묻고 고칠 수 있도록 온보딩을 진행합니다.")]
    inner = ('<div class="vcen">' + stepflow(steps, hot=(5,))
             + band('마지막 단계가 교육인 것이 이 순서의 핵심입니다. '
                    '<strong>수집을 걸어 놓고 손을 떼면 여섯 달 뒤에 다시 깨집니다.</strong>')
             + '</div>')
    return wide(n, P2, "데이터 분석 컨설팅", '점검에서 <span class="gt">교육</span>까지 다섯 단계',
                "데이터 분석 컨설팅 다섯 단계",
                "데이터 수집 구조 설계부터 활용 교육까지, 데이터 활용의 전 과정을 함께합니다.",
                inner, "")


def s_growth(n):
    points = [("문제를 먼저 좁힙니다",
               "기업 현황을 살펴 최우선으로 풀 과제를 정합니다. 채널을 늘리는 일은 그다음입니다."),
              ("목표를 숫자로 바꿉니다",
               "달성하려는 상태를 지표로 적습니다. 무엇이 좋아지면 성공인지 먼저 합의합니다."),
              ("실행까지 같이 갑니다",
               "전략만 넘기지 않고 매체 운영과 성과 분석, 최적화까지 함께 돌립니다.")]
    why = ["기업 맞춤형 문제 진단 및 목표 설정",
           "디지털 매체 전반을 아우르는 마케팅 전략 제시",
           "각 분야별 전문 컨설턴트의 전담 배치",
           "즉시 실행 가능한 실무 전략 제시"]
    return _service(n, "그로스 마케팅 컨설팅",
                    '지금 <span class="gt">가장 필요한 한 가지</span>를 찾습니다',
                    "지금 가장 필요한 한 가지 찾기",
                    "디지털 마케팅 채널 전반에 걸쳐 문제 상황을 진단하고 실행 가이드를 제공합니다.",
                    points, "이런 점이 다릅니다", why)


def s_growth_flow(n):
    HEADERS[n] = "그로스 마케팅 컨설팅 다섯 단계"
    steps = [("현황 분석과 문제 진단", "매체와 자사몰, 고객 행동을 한 번에 훑습니다."),
             ("목표 설정", "풀어야 할 문제를 지표 한두 개로 좁힙니다."),
             ("마케팅 액션 플랜 제시", "가설을 세우고 검증할 순서를 짭니다."),
             ("마케팅 운영 지원", "실제 매체 운영과 소재 테스트를 함께 돌립니다."),
             ("성과 분석 및 최적화", "결과를 읽고 다음 실험으로 넘깁니다.")]
    inner = ('<div class="vcen">' + stepflow(steps, hot=(3,))
             + band('다각적인 접근과 실험으로 목표에 다다르도록, '
                    '<strong>실무자가 그대로 쓸 수 있는 전략을 제시합니다.</strong>')
             + '</div>')
    return wide(n, P2, "그로스 마케팅 컨설팅", '진단에서 <span class="gt">최적화</span>까지 다섯 단계',
                "그로스 마케팅 컨설팅 다섯 단계",
                "문제 현황 분석으로 구체적 목표를 세운 뒤, 실험을 거쳐 목표에 다다릅니다.",
                inner, "")


def s_ax(n):
    points = [("도입이 아니라 성과로 봅니다",
               "AI를 켰는지가 아니라 업무 시간과 결과물이 달라졌는지로 판단합니다."),
              ("분석 구축 위에서 설계합니다",
               "데이터가 쌓이는 구조를 먼저 만들고, 그 위에 AI를 얹습니다."),
              ("쓰던 사람이 이어 갑니다",
               "AI 활용 역량을 내재화해 담당자가 스스로 굴릴 수 있게 합니다.")]
    why = ["분석 구축 기반의 실전형 전략 설계",
           "비즈니스 상황에 맞춘 AX 전략 커스터마이징",
           "즉시 사용 가능한 전용 도구 제공",
           "실무자의 현안을 푸는 기술 지원과 가이드"]
    return _service(n, "AX 컨설팅",
                    '데이터가 <span class="gt">실제로 일하게</span> 만듭니다',
                    "데이터가 실제로 일하게 만들기",
                    "AX는 인공지능 전환을 말합니다. 수집을 넘어 AI가 그 데이터로 일하도록 설계합니다.",
                    points, "이런 점이 다릅니다", why)


def s_ax_flow(n):
    HEADERS[n] = "AX 컨설팅 다섯 단계"
    steps = [("AI 활용 현황 진단", "지금 누가 무엇에 쓰고 있는지 먼저 봅니다."),
             ("도입 목표와 계획 수립", "어느 업무를 어디까지 맡길지 정합니다."),
             ("AX 전략 실행", "업무 순서 안에 AI를 넣고 도구를 붙입니다."),
             ("진행 상태 점검과 최적화", "실제로 쓰이는지 보고 막힌 자리를 풉니다."),
             ("AI 활용 역량 내재화", "담당자가 스스로 늘려 갈 수 있게 넘깁니다.")]
    inner = ('<div class="vcen">' + stepflow(steps, hot=(3,))
             + band('AI 전환의 비전을 세우고 최신 기술을 들여, '
                    '<strong>고객사의 마케팅과 서비스 분석 역량이 스스로 자라게 합니다.</strong>')
             + '</div>')
    return wide(n, P2, "AX 컨설팅", '진단에서 <span class="gt">내재화</span>까지 다섯 단계',
                "AX 컨설팅 다섯 단계",
                "막연한 AI 도입이 아니라, 실제 성과를 만드는 순서로 진행합니다.",
                inner, "")


def s_tools_own(n):
    HEADERS[n] = "직접 만든 분석 도구 두 가지"
    items = [("OSOMA INSIGHT", "서비스 분석 도구입니다. 쌓인 행동 데이터를 AI가 읽고, 무엇이 달라졌는지 말로 돌려줍니다."),
             ("OSOMA AD INSIGHT", "광고 효율 분석 도구입니다. 매체별 성과를 한자리에 모아 어디를 줄이고 늘릴지 짚습니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "도구", "three", icons=["chart", "target"])
             + band('업종에 응용 소프트웨어 개발이 들어 있는 이유입니다. '
                    '<strong>컨설팅에서 반복되는 일을 도구로 만들어 고객사에 함께 넘깁니다.</strong>')
             + '</div>')
    return wide(n, P2, "자체 도구", '컨설팅 노하우를 <span class="gt">도구로</span> 만듭니다',
                "직접 만든 분석 도구 두 가지",
                "자체 개발한 분석 솔루션과 컨설팅 노하우를 함께 씁니다.",
                inner, "")


def s_edu(n):
    points = [("대상을 먼저 봅니다",
               "누가 듣는지와 무엇을 할 수 있게 되어야 하는지를 정하고 커리큘럼을 짭니다."),
              ("분야별 강사가 들어갑니다",
               "매체 운영과 분석은 다른 사람이 맡습니다. 실무를 하는 컨설턴트가 그대로 강사입니다."),
              ("실습으로 끝냅니다",
               "듣고 끝나지 않도록 자기 계정과 자기 자료로 손을 움직이게 합니다.")]
    why = ["수강 대상과 목적에 맞는 커리큘럼 구성",
           "분야별 전문 강사 배치",
           "실무에 바로 쓰는 실습형 진행",
           "운영부터 분석까지 아우르는 교육 범위"]
    return _service(n, "마케팅 및 분석 교육",
                    '노하우를 <span class="gt">사람에게</span> 옮깁니다',
                    "노하우를 사람에게 옮기기",
                    "기업 내부에서 분석과 마케팅 운영 역량을 내재화하는 맞춤 교육 프로그램입니다.",
                    points, "이런 점이 다릅니다", why)


def s_edu_flow(n):
    HEADERS[n] = "마케팅 및 분석 교육 다섯 단계"
    steps = [("교육 목적과 타겟 파악", "누가 듣고 무엇을 할 수 있게 되어야 하는지 정합니다."),
             ("분야별 맞춤 강사 매칭", "주제에 맞는 실무 컨설턴트를 배치합니다."),
             ("맞춤 커리큘럼 기획", "회차와 난이도를 대상에 맞춰 짭니다."),
             ("교육 자료 제작", "고객사의 실제 화면과 자료로 예시를 만듭니다."),
             ("강의 및 실습 진행", "손을 움직이는 실습으로 마칩니다.")]
    inner = ('<div class="vcen">' + stepflow(steps, hot=(4,))
             + band('교육 자료를 고객사의 실제 화면으로 만드는 것이 다릅니다. '
                    '<strong>남의 사례가 아니라 자기 자료로 배웁니다.</strong>')
             + '</div>')
    return wide(n, P2, "마케팅 및 분석 교육", '파악에서 <span class="gt">실습</span>까지 다섯 단계',
                "마케팅 및 분석 교육 다섯 단계",
                "실무 기반의 노하우를 그대로 옮기는 순서입니다.",
                inner, "")


def s_chain(n):
    HEADERS[n] = "네 영역이 이어지는 하나의 흐름"
    steps = [("분석 컨설팅", "목표를 수치화할 기반을 만듭니다."),
             ("그로스 마케팅", "그 숫자 위에서 실험하고 최적화합니다."),
             ("AX 컨설팅", "AI를 얹어 업무 효율을 끌어올립니다."),
             ("내재화 교육", "고객사가 스스로 운영하게 넘깁니다.")]
    inner = ('<div class="vcen">' + stepflow(steps, hot=(4,))
             + band('네 영역을 따로 파는 회사는 많습니다. '
                    '<strong>우리는 앞 단계의 결과가 다음 단계의 입력이 되도록 이어 붙입니다.</strong>')
             + '</div>')
    return wide(n, P2, "네 영역의 관계", '따로가 아니라 <span class="gt">한 줄</span>입니다',
                "네 영역이 이어지는 하나의 흐름",
                "데이터 분석 컨설팅으로 목표를 수치화하고, 그 위에서 그로스 마케팅을 돌린 뒤, AI로 효율을 올리고 내재화 교육으로 넘깁니다.",
                inner, "")


# ══ 3부 일하는 방식과 결과물 ═══════════════════════════════════════════

def s_deliver(n):
    HEADERS[n] = "일이 끝나면 손에 남는 것"
    items = [("이벤트 정의서", "웹과 앱에서 무엇을 언제 세는지 적은 문서입니다."),
             ("스크립트 가이드", "개발자가 그대로 붙일 수 있는 수집 코드 안내입니다."),
             ("GTM 태깅", "정의서대로 걸어 둔 태그와 트리거입니다."),
             ("디버깅 기록", "수집이 제대로 되는지 확인한 점검 결과입니다."),
             ("시각화 대시보드", "담당자가 매일 여는 Looker Studio 화면입니다."),
             ("온보딩 교육", "직접 묻고 고치는 법을 익히는 자리입니다.")]
    grid = "".join(f'<div class="tool"><span class="tno">{i:02d}</span><div><h4>{t}</h4><p>{d}</p></div></div>'
                   for i, (t, d) in enumerate(items, 1))
    inner = (f'<div class="vcen"><div class="tools">{grid}</div>'
             + band('여섯 가지는 프로젝트마다 이름만 조금 다를 뿐 거의 그대로 나옵니다. '
                    '<strong>결과물의 목록이 곧 우리가 약속하는 범위입니다.</strong>')
             + '</div>')
    return wide(n, P3, "결과물", '보고서 한 부가 아니라 <span class="gt">여섯 가지</span>를 남깁니다',
                "일이 끝나면 손에 남는 것",
                "데이터 분석 컨설팅에서 고객사에 넘기는 것들입니다.",
                inner, "")


def s_common_flow(n):
    HEADERS[n] = "어느 일이든 지나는 공통 순서"
    flow = [("진단", "지금 상태를 먼저 봅니다. 무엇이 없는지부터 적습니다."),
            ("설계", "목표를 정하고 그에 맞는 구조와 순서를 짭니다."),
            ("실행", "설계한 대로 걸고 돌립니다. 컨설턴트가 함께 붙습니다."),
            ("내재화", "담당자가 스스로 이어 갈 수 있게 넘깁니다.")]
    facts = [("영역", "4", "분석, 그로스, AX, 교육 어느 쪽이든 이 순서를 지납니다"),
             ("고정", "진단", "진단 없이 바로 실행으로 들어가지 않습니다"),
             ("끝", "내재화", "넘기지 못하면 끝난 것으로 보지 않습니다")]
    inner = ('<div class="vcen">' + howto(flow, facts)
             + band('네 영역의 다섯 단계는 서로 다르게 적혀 있지만, '
                    '<strong>큰 순서는 진단, 설계, 실행, 내재화로 같습니다.</strong>')
             + '</div>')
    return wide(n, P3, "일하는 순서", '진단, 설계, 실행, <span class="gt">내재화</span>',
                "어느 일이든 지나는 공통 순서",
                "사업 영역이 달라도 일을 여는 방식과 닫는 방식은 같습니다.",
                inner, "")


def s_stack(n):
    HEADERS[n] = "우리가 손에 쥐는 도구"
    items = [("GA4", "웹과 앱의 사용자 행동을 모으는 기본 분석 도구입니다."),
             ("Google Tag Manager", "코드를 다시 배포하지 않고 수집을 걸고 고치는 자리입니다."),
             ("BigQuery", "원자료를 그대로 쌓아 두고 자유롭게 물어보는 창고입니다."),
             ("Looker Studio", "쌓인 자료를 담당자가 매일 여는 화면으로 만듭니다."),
             ("Amplitude", "제품 안에서 사용자가 어떻게 움직이는지 깊게 보는 도구입니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "도구", "five", icons=["chart", "form", "table", "eye", "network"])
             + band('도구를 정해 놓고 고객사를 맞추지 않습니다. '
                    '<strong>서비스 형태와 분석 목적을 먼저 보고 도구를 고릅니다.</strong>')
             + '</div>')
    return wide(n, P3, "쓰는 도구", '도구는 <span class="gt">목적에 맞춰</span> 고릅니다',
                "우리가 손에 쥐는 도구",
                "레퍼런스에 반복해서 나오는 다섯 가지입니다.",
                inner, "")


def s_axes(n):
    HEADERS[n] = "고객사를 읽는 세 축"
    items = [("TYPE", "B2B인지 B2C인지 봅니다. 사는 사람과 결정하는 사람이 같은지가 갈립니다."),
             ("CATEGORY", "Web인지 App인지 봅니다. 수집을 거는 방식과 도구가 달라집니다."),
             ("KPI", "Traffic인지 Lead인지 Purchase인지 봅니다. 성과로 셀 것을 먼저 정합니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "축", "three", icons=["users", "form", "flag"])
             + band('세 축을 먼저 적어 두면 그다음이 빨라집니다. '
                    '<strong>어떤 이벤트를 정의할지, 어떤 화면을 만들지가 여기서 정해집니다.</strong>')
             + '</div>')
    return wide(n, P3, "고객사 읽기", '<span class="gt">세 축</span>으로 먼저 자리를 잡습니다',
                "고객사를 읽는 세 축",
                "레퍼런스마다 맨 위에 이 세 가지를 적어 두는 이유입니다.",
                inner, "")


def s_ref_data(n):
    HEADERS[n] = "데이터 분석 컨설팅 레퍼런스"
    items = [("교보문고", "도서와 전자책, 기프트를 함께 파는 종합 콘텐츠 플랫폼입니다. 웹과 앱, GA4와 BigQuery를 함께 다뤘습니다."),
             ("신세계면세점", "온라인 면세 상품 구매 플랫폼입니다. 웹과 앱의 구매 흐름을 GA4로 잇고 대시보드까지 만들었습니다."),
             ("반다이남코코리아", "프라모델과 피규어를 파는 온라인 쇼핑 플랫폼입니다. 웹과 앱 이벤트를 함께 정의했습니다."),
             ("안랩", "기업과 개인 보안 서비스를 소개하는 웹사이트입니다. 문의로 이어지는 길을 지표로 세웠습니다.")]
    grid = "".join(f'<div class="tool"><span class="tno">{i:02d}</span><div><h4>{t}</h4><p>{d}</p></div></div>'
                   for i, (t, d) in enumerate(items, 1))
    inner = (f'<div class="vcen"><div class="tools">{grid}</div>'
             + band('네 곳 모두 같은 여섯 가지를 남기고 나왔습니다. '
                    '<strong>정의서, 스크립트 가이드, 태깅, 디버깅, 대시보드, 온보딩 교육입니다.</strong>')
             + '</div>')
    return wide(n, P3, "레퍼런스", '분석 환경을 세운 <span class="gt">네 곳</span>',
                "데이터 분석 컨설팅 레퍼런스",
                "규모와 업종이 다르지만 일의 모양은 같았습니다.",
                inner, "")


def s_ref_growth(n):
    HEADERS[n] = "그로스 마케팅 컨설팅 레퍼런스"
    items = [("KOTRA", "해외 무역관을 위한 디지털 마케팅 채널 운영 가이드를 만들고 마인드셋 내재화까지 진행했습니다."),
             ("안국건강", "자사몰 고객 행동을 분석하고 매체 운영 점검과 CRM 전략까지 함께 세웠습니다."),
             ("스테이폴리오", "숙박 큐레이션 플랫폼입니다. 그로스해킹 내재화 프로그램을 설계하고 전환 테스트를 돌렸습니다."),
             ("서울관광재단 Visit Seoul", "CMS 이관에 맞춰 테크니컬 SEO를 점검하고 자연 유입 활성화 가이드를 만들었습니다.")]
    grid = "".join(f'<div class="tool"><span class="tno">{i:02d}</span><div><h4>{t}</h4><p>{d}</p></div></div>'
                   for i, (t, d) in enumerate(items, 1))
    inner = (f'<div class="vcen"><div class="tools">{grid}</div>'
             + band('공공기관과 제조, 플랫폼이 섞여 있습니다. '
                    '<strong>업종이 달라도 현황 파악과 목표 설정으로 여는 것은 같습니다.</strong>')
             + '</div>')
    return wide(n, P3, "레퍼런스", '실행까지 함께 간 <span class="gt">네 곳</span>',
                "그로스 마케팅 컨설팅 레퍼런스",
                "전략만 넘기지 않고 운영과 최적화까지 붙어 있었습니다.",
                inner, "")


# ══ 4부 지나온 자리와 사람 ═════════════════════════════════════════════

def _hist(rows):
    out = []
    for year, note, items in rows:
        chips = "".join(f'<span class="{c}">{t}</span>' for t, c in items)
        out.append(f'<div class="histrow"><div class="histyear">{year}<em>{note}</em></div>'
                   f'<div class="histitems">{chips}</div></div>')
    return f'<div class="hist">{"".join(out)}</div>'


def s_hist1(n):
    HEADERS[n] = "설립부터 2023년까지"
    rows = [("2020", "12월 14일 설립", [("주식회사 오픈소스마케팅 설립", "on")]),
            ("2022", "프로젝트 9건", [("신한S브릿지 8기와 9기", ""), ("KOTRA", "on"), ("서울관광재단 SEO", ""),
                                  ("브랜든", ""), ("마켓올슨", ""), ("로위", ""), ("메디트리", ""),
                                  ("인프런 강의 2종", "on")]),
            ("2023", "프로젝트 14건", [("교보문고", "on"), ("신세계면세점", "on"), ("KT 알파", ""),
                                   ("동원디어푸드", ""), ("더플라자 호텔", ""), ("ABC마트", ""),
                                   ("대림 e편한세상", ""), ("키플링, 이스트팩", ""), ("위닉스", ""),
                                   ("지란지교소프트", ""), ("신세계사이먼", ""), ("씨티닷츠", "")])]
    inner = _hist(rows)
    return wide(n, P4, "연혁", '2020년에 <span class="gt">시작했습니다</span>',
                "설립부터 2023년까지",
                "회사소개서 연혁에 적힌 프로젝트를 연도로 묶었습니다.",
                inner, "")


def s_hist2(n):
    HEADERS[n] = "2024년과 2025년"
    rows = [("2024", "프로젝트 14건", [("안랩", "on"), ("한국관광공사", "on"), ("경동나비엔", ""),
                                   ("반다이남코코리아", "on"), ("스케쳐스코리아", ""), ("오픈서베이", ""),
                                   ("파크시스템스", ""), ("고려대학교", ""), ("이투스에듀", ""),
                                   ("신한퓨처스랩", ""), ("풀무원녹즙", ""), ("원밀리언", "")]),
            ("2025", "프로젝트 16건", [("LG CNS", "on"), ("베스핀글로벌 AI 리드 스코어링", "on"),
                                   ("뤼튼테크놀로지", ""), ("열매나눔재단", ""), ("푸르메재단", ""),
                                   ("연세대학교", ""), ("한림대학교", ""), ("한국관광공사", ""),
                                   ("라그나로크 라틴아메리카", ""), ("남유 FNC AI 광고 대시보드", "on"),
                                   ("소브린", ""), ("메터그룹", "")])]
    inner = _hist(rows)
    return wide(n, P4, "연혁", '분석에서 <span class="gt">AI</span>로 넓어졌습니다',
                "2024년과 2025년",
                "2025년 말부터 AI 리드 스코어링과 AI 광고 분석이 연혁에 들어옵니다.",
                inner, "")


def s_numbers(n):
    HEADERS[n] = "숫자로 보는 오픈소스마케팅"
    items = [("2020", "설립", "12월 14일에 문을 열었습니다."),
             ("53", "프로젝트", "회사소개서 연혁에 적힌 2022년부터 2025년까지의 건수입니다."),
             ("4", "사업 영역", "분석, 그로스, AX, 교육입니다."),
             ("2", "자체 도구", "OSOMA INSIGHT와 OSOMA AD INSIGHT입니다.")]
    grid = "".join(f'<div class="fact"><b>{b}</b><h4>{t}</h4><p>{d}</p></div>' for b, t, d in items)
    inner = f'<div class="facts">{grid}</div>'
    return wide(n, P4, "숫자", '지나온 자리를 <span class="gt">숫자로</span> 봅니다',
                "숫자로 보는 오픈소스마케팅",
                "2026년 2월 회사소개서에 적힌 값을 그대로 옮겼습니다.",
                inner, "")


def s_org(n):
    HEADERS[n] = "일을 나누는 방식"
    inner = ('<div class="org">'
             '<div class="orgtop">대표이사</div>'
             '<div class="orgline"></div>'
             '<div class="orgmid"><div>CMO</div><div>컨설팅 본부</div><div>AX 전략실</div></div>'
             '<div class="orgcols">'
             '<div class="orgcol"><h4>마케팅 컨설팅팀</h4><ul>'
             '<li>마케팅 운영 현황 진단</li><li>데이터 기반 그로스 마케팅 컨설팅</li>'
             '<li>마케팅 AI 도입 및 활용 컨설팅</li><li>마케팅 운영 역량 내재화 교육</li></ul></div>'
             '<div class="orgcol"><h4>분석 컨설팅팀</h4><ul>'
             '<li>데이터 분석 환경 진단 및 점검</li><li>데이터 분석 환경 구축 및 시각화 컨설팅</li>'
             '<li>분석 AI 도입 및 활용 컨설팅</li><li>데이터 분석 역량 내재화 교육</li></ul></div>'
             '</div></div>')
    return wide(n, P4, "조직", '두 팀이 <span class="gt">같은 순서</span>로 일합니다',
                "일을 나누는 방식",
                "마케팅과 분석으로 팀이 갈리지만, 진단하고 구축하고 넘기는 순서는 두 팀이 같습니다.",
                inner, "")


def s_value(n):
    HEADERS[n] = "우리가 만드는 가치"
    items = [("근거를 남깁니다", "감이 아니라 숫자로 판단하도록 수집 구조와 정의서를 세워 둡니다."),
             ("속도를 올립니다", "매체 운영과 분석에 AI를 넣어 같은 시간에 더 많이 시험하게 합니다."),
             ("사람을 남깁니다", "우리가 빠져도 굴러가도록 방법을 담당자에게 옮깁니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "가치", "three", icons=["ruler", "bolt", "users"])
             + band('오픈소스마케팅은 지식과 실행을 나누며, '
                    '<strong>고객이 스스로 성장할 수 있는 마케팅 환경을 만듭니다.</strong>')
             + '</div>')
    return wide(n, P4, "정리", '우리가 파는 것은 <span class="gt">결과가 아니라 역량</span>입니다',
                "우리가 만드는 가치",
                "세 가지가 남으면 우리가 한 일이 제 몫을 한 것입니다.",
                inner, "")


def s_end(n):
    HEADERS[n] = "마무리"
    aur = '<i class="aur a2"></i><i class="aur a3"></i>'
    body = (f'{aur}<div class="fg">'
            '<h2>지속 가능한 성장을 설계하는<br><span class="gt">마케팅 컨설팅 기업</span></h2>'
            '<p class="endsub">데이터와 전략, 그리고 사람의 연결로 브랜드가 스스로 성장하는 순간을 만듭니다. '
            '우리가 만드는 마케팅의 목표는 독립입니다.</p>'
            '<div class="endcontact"><span>contact@osoma.kr</span><span>osoma.kr</span></div>'
            '</div>')
    return ax(n, "ax-end", body, "OPEN SOURCE MARKETING")


# ══ 조립 ═══════════════════════════════════════════════════════════════

ORDER = [s_cover, s_toc, s_oneline, s_profile, s_independence, s_values, s_internalize,
         s_areas, s_data, s_data_flow, s_growth, s_growth_flow, s_ax, s_ax_flow,
         s_tools_own, s_edu, s_edu_flow, s_chain,
         s_deliver, s_common_flow, s_stack, s_axes, s_ref_data, s_ref_growth,
         s_hist1, s_hist2, s_numbers, s_org, s_value, s_end]


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
<title>오픈소스마케팅 / 우리는 어떤 회사인가</title>
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
