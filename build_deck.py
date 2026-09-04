#!/usr/bin/env python3
"""오픈소스마케팅 회사 소개 덱 28장.

모회사 대표와 임원에게 회사의 가치를 설명하는 자리에서 쓴다.
무슨 문제를 푸는 회사인지를 먼저 세우고, 실제 산출물 캡처와 재현 화면으로 일하는 방식을 증명한다.
캡처마다 어떤 화면인지, 어떤 작업인지, 어디로 이어져 어떤 가치를 주는지 세 칸을 붙인다.
실물의 출처와 민감정보 처리 기준은 README 의 실물의 출처 표를 따른다.
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


# ── 실물 캡처와 재현 화면용 CSS ──
SHOT_CSS = """
/* 실물 캡처 장. 왼쪽에 화면, 오른쪽에 설명 세 칸 */
.shotwrap{display:grid;grid-template-columns:1.35fr 1fr;gap:52px;flex:1;min-height:0;margin-top:30px;align-items:center}
.shotwrap.rev{grid-template-columns:1fr 1.35fr}
.shotbox{min-width:0;display:flex;align-items:center;justify-content:center;min-height:0;height:100%}
.shotbox img{max-width:100%;max-height:640px;width:auto;height:auto;display:block;border-radius:18px;
  border:1.5px solid var(--line);box-shadow:0 20px 52px rgba(20,25,40,.16);background:#fff}
.shotside{display:flex;flex-direction:column;gap:20px;min-width:0}
.shotmeta{border:1.5px solid var(--line);border-radius:18px;padding:20px 24px;background:#fff}
.shotmeta b{font-family:var(--fm);font-size:13.5px;font-weight:700;letter-spacing:.16em;
  background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.shotmeta h4{font-size:22px;font-weight:800;margin:8px 0 7px;letter-spacing:-.01em}
.shotmeta p{font-size:18.5px;line-height:1.55;color:var(--dim)}
.srcnote{font-size:16px;color:var(--faint);line-height:1.5}

/* 구글 시트 재현. 실데이터를 시트 화면 모양으로 놓는다 */
.gsheet{background:#fff;border:1.5px solid var(--line);border-radius:16px;overflow:hidden;
  box-shadow:0 18px 44px rgba(20,25,40,.12);min-width:0}
.gsheet .gbar{display:flex;align-items:center;gap:12px;padding:12px 18px;border-bottom:1px solid #E4E7EE;background:#F8F9FC}
.gsheet .gbar i{width:26px;height:26px;border-radius:6px;background:#0F9D58;display:grid;place-items:center;flex:none}
.gsheet .gbar i svg{width:15px;height:15px;fill:#fff}
.gsheet .gbar b{font-size:16.5px;font-weight:700;color:#3C4043}
.gsheet .gbar span{font-size:13.5px;color:#80868B}
.gsheet table{width:100%;border-collapse:collapse;table-layout:fixed}
.gsheet th{background:#F1F3F6;color:#5F6368;font-size:14px;font-weight:700;padding:9px 12px;
  border:1px solid #E4E7EE;text-align:left}
.gsheet td{font-size:14.5px;padding:8px 12px;border:1px solid #EDF0F5;color:#3C4043;line-height:1.4;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.gsheet td.mono{font-family:var(--fm);font-size:13px;color:#1A73E8}
.gsheet td.grp{font-weight:700;color:#202124}
.gsheet .gtabs{display:flex;gap:2px;padding:8px 14px 10px;background:#F8F9FC;border-top:1px solid #E4E7EE}
.gsheet .gtabs span{font-size:13px;padding:5px 16px;border-radius:6px 6px 0 0;color:#5F6368}
.gsheet .gtabs span.on{background:#fff;color:#1A73E8;font-weight:700;border:1px solid #E4E7EE;border-bottom:none}

/* 슬랙 채널 재현. 실제 메시지를 이름만 가리고 옮긴다 */
.slackui{background:#fff;border:1.5px solid var(--line);border-radius:16px;overflow:hidden;
  box-shadow:0 18px 44px rgba(20,25,40,.12);display:flex;flex-direction:column;min-width:0}
.slackui .shead{display:flex;align-items:center;gap:10px;padding:13px 20px;border-bottom:1px solid #E8E8E8}
.slackui .shead b{font-size:17px;font-weight:800;color:#1D1C1D}
.slackui .shead b::before{content:"# ";color:#616061;font-weight:400}
.slackui .shead span{font-size:13.5px;color:#616061}
.smsg{display:flex;gap:12px;padding:11px 20px}
.smsg + .smsg{border-top:1px solid #F4F4F4}
.smsg .sava{flex:none;width:38px;height:38px;border-radius:9px;display:grid;place-items:center;
  color:#fff;font-size:15px;font-weight:800}
.smsg .sbody{min-width:0;flex:1}
.smsg .sname{font-size:15.5px;font-weight:800;color:#1D1C1D}
.smsg .sname span{font-weight:400;font-size:12.5px;color:#616061;margin-left:8px}
.smsg .stext{font-size:15.5px;line-height:1.5;color:#1D1C1D;margin-top:3px}
.smsg .stext em{font-style:normal;font-weight:700}
.smsg .stext .schip{display:inline-block;background:#F8F0DC;color:#A05A00;border-radius:3px;
  padding:0 4px;font-size:14.5px}
.smsg.bot .sava{background:linear-gradient(135deg,#4A154B,#7C3085)}
.sdivider{display:flex;align-items:center;gap:14px;padding:6px 20px}
.sdivider i{flex:1;height:1px;background:#E8E8E8}
.sdivider span{font-size:12.5px;font-weight:700;color:#616061;border:1px solid #E8E8E8;border-radius:999px;padding:3px 12px}

/* AI 자연어 분석 대화 재현 */
.aichat{background:#fff;border:1.5px solid var(--line);border-radius:16px;overflow:hidden;
  box-shadow:0 18px 44px rgba(20,25,40,.12);display:flex;flex-direction:column;min-width:0}
.aichat .ahead{display:flex;align-items:center;gap:10px;padding:12px 20px;border-bottom:1px solid #ECECF1;background:#FAFAFC}
.aichat .ahead i{width:24px;height:24px;border-radius:50%;background:var(--grad);flex:none}
.aichat .ahead b{font-size:15.5px;font-weight:700;color:#3C4043}
.amsg{padding:14px 22px;display:flex;flex-direction:column;gap:8px}
.amsg.user{align-items:flex-end}
.amsg.user .abub{background:#F0F4F9;border-radius:16px 16px 4px 16px;padding:13px 20px;
  font-size:17.5px;font-weight:600;color:#1F1F1F;max-width:82%}
.amsg .arun{font-family:var(--fm);font-size:13px;color:#7A879F;display:flex;align-items:center;gap:8px}
.amsg .arun i{width:7px;height:7px;border-radius:50%;background:var(--grad);flex:none}
.amsg .atable{width:100%;border-collapse:collapse;margin:4px 0}
.amsg .atable th{font-size:13.5px;color:#5F6368;font-weight:700;text-align:left;padding:7px 12px;
  border-bottom:2px solid #E4E7EE}
.amsg .atable td{font-size:15px;padding:7px 12px;border-bottom:1px solid #F0F2F6;color:#3C4043}
.amsg .atable td.num{font-family:var(--fm);font-size:14px;text-align:right}
.amsg .atable tr.hot td{font-weight:700;color:#1A73E8;background:#F5F9FF}
.amsg .asum{font-size:16.5px;line-height:1.6;color:#3C4043;background:#F8FAF8;border-left:3px solid #35B4C7;
  border-radius:0 10px 10px 0;padding:12px 18px}

/* 자동 리포트 파이프라인 도해 */
.pipe{display:grid;grid-template-columns:1fr 64px 1fr 64px 1fr 64px 1fr;align-items:stretch;gap:0;margin-top:8px}
.pipenode{background:#fff;border:1.5px solid var(--line);border-radius:20px;padding:26px 26px 22px;
  display:flex;flex-direction:column;gap:10px;box-shadow:0 12px 32px rgba(40,50,80,.06)}
.pipenode.hot{border:2px solid transparent;background:linear-gradient(#fff,#fff) padding-box,var(--grad) border-box}
.pipenode b{font-family:var(--fm);font-size:13.5px;font-weight:700;letter-spacing:.14em;color:var(--faint)}
.pipenode.hot b{background:var(--grad);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.pipenode h4{font-size:23px;font-weight:800;letter-spacing:-.01em}
.pipenode p{font-size:17.5px;line-height:1.5;color:var(--dim)}
.pipearrow{display:grid;place-items:center}
.pipearrow svg{width:30px;height:30px;stroke:#C9CEDA;stroke-width:2.4;fill:none}
.pipecap{margin-top:26px}

/* 노션 인계 문서 트리 재현 */
.notionui{background:#fff;border:1.5px solid var(--line);border-radius:16px;overflow:hidden;
  box-shadow:0 18px 44px rgba(20,25,40,.12);display:grid;grid-template-columns:250px 1fr;min-width:0}
.notionui .nside{background:#F7F6F3;border-right:1px solid #EDECE9;padding:16px 10px;font-size:14px;color:#5F5E5B}
.notionui .nside .nrow{display:flex;align-items:center;gap:7px;padding:5px 10px;border-radius:6px;line-height:1.35}
.notionui .nside .nrow.on{background:#EFEEEB;font-weight:700;color:#37352F}
.notionui .nside .nrow.d1{padding-left:26px}.notionui .nside .nrow.d2{padding-left:42px}
.notionui .nmain{padding:30px 40px}
.notionui .nmain h3{font-size:26px;font-weight:800;color:#37352F;margin-bottom:16px}
.notionui .nmain .nitem{display:flex;align-items:center;gap:10px;padding:8px 4px;border-bottom:1px solid #F1F0EE;
  font-size:16.5px;color:#37352F}
.notionui .nmain .nitem i{font-style:normal;flex:none}
.notionui .nmain .nitem span{color:#9B9A97;font-size:14px;margin-left:auto;flex:none}

/* 스크립트 가이드: 모바일 캡처 옆 실제 코드 */
.codebox{background:#0F172A;border-radius:16px;padding:22px 26px;overflow:hidden;
  box-shadow:0 18px 44px rgba(15,23,42,.28)}
.codebox .cfile{font-family:var(--fm);font-size:12.5px;letter-spacing:.1em;color:#64748B;margin-bottom:12px}
.codebox pre{font-family:var(--fm);font-size:14.5px;line-height:1.66;color:#CBD5E1;white-space:pre;overflow:hidden}
.codebox .ck{color:#7DD3FC}.codebox .cs{color:#FCA5A5}.codebox .cc{color:#64748B}

/* 실물 캡처 장의 머리말을 한 단계 줄여 판을 키운다 */
.slide:has(.shotwrap) h2.head,.slide:has(.gsheet) h2.head{font-size:54px}
.slide:has(.shotwrap) .lead,.slide:has(.gsheet) .lead{font-size:23px;margin-top:14px}
"""


def shot(img, alt, metas, note, rev=False, inner_html=None):
    """실물 캡처 한 장. 왼쪽에 화면(또는 재현 HTML), 오른쪽에 설명 세 칸과 출처."""
    metas_html = "".join(f'<div class="shotmeta"><b>{k}</b><h4>{t}</h4><p>{d}</p></div>'
                         for k, t, d in metas)
    left = inner_html if inner_html else f'<img src="{img}" alt="{alt}">'
    return (f'<div class="shotwrap{" rev" if rev else ""}">'
            f'<div class="shotbox">{left}</div>'
            f'<div class="shotside">{metas_html}<p class="srcnote">{note}</p></div>'
            '</div>')


# ══ 표지와 차례 ════════════════════════════════════════════════════════

def s_cover(n):
    HEADERS[n] = "오픈소스마케팅이 하는 일"
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
            '<h1>고객이 무엇을 하는지<br><span class="gt">숫자로 보이게</span> 만듭니다</h1>'
            '<p class="sub">웹과 앱에서 벌어지는 행동을 세어 두고, '
            '그 숫자 위에서 광고와 자사몰을 고쳐 성과를 끌어올립니다. '
            '오늘은 이 일을 실제 산출물 화면으로 보여 드립니다.</p>'
            '<div class="mchips"><span><b>53</b> 프로젝트</span><span><b>24</b> 개사 동시 운영</span>'
            '<span><b>3</b> 년 연속 국가사업</span></div>'
            '</div>')
    return ax(n, "ax-cover", body, "OPEN SOURCE MARKETING / COMPANY DECK")


def s_toc(n):
    HEADERS[n] = "오늘 다룰 다섯 부"
    cols = [("PART 1", "무엇을 하는 회사인가",
             ["회사 개요", "고객사가 겪는 문제", "분석 환경의 뜻", "일의 네 갈래", "맡긴 뒤 달라지는 것"]),
            ("PART 2", "일하는 방식, 실물로",
             ["구축 여섯 단계", "이벤트 정의서", "스크립트 가이드", "검수 화면", "대시보드",
              "빅쿼리 연결", "인계 문서", "그로스 마케팅"]),
            ("PART 3", "스물네 곳을 동시에",
             ["사업 개요", "회차 등록 채널", "봇 리마인드", "진행률 기준", "보고 세 층"]),
            ("PART 4", "AI를 얹은 자리",
             ["달라진 일", "심는 다섯 단계", "자연어 분석", "자동 리포트", "구독 설계"]),
            ("PART 5", "쌓인 것과 앞으로",
             ["고객사", "연혁과 방향", "마무리"])]
    html = "".join(
        f'<div class="tocol"><h3><b>{no}</b>{title}</h3><ul>'
        + "".join(f'<li><b>{i:02d}</b>{x}</li>' for i, x in enumerate(items, 1))
        + '</ul></div>' for no, title, items in cols)
    inner = f'<div class="toc five">{html}</div>'
    return wide(n, P1, "오늘의 차례", '일한 <span class="gt">실물</span>을 순서대로 봅니다',
                "오늘 다룰 다섯 부",
                "무엇을 하는 회사인지 먼저 세우고, 실제 산출물 화면으로 일하는 방식을 본 뒤, 운영 규모와 AI, 앞으로로 마칩니다.",
                inner, "")


# ══ 1부 무엇을 하는 회사인가 ═══════════════════════════════════════════

def s_intro(n):
    rows = [("회사명", "주식회사 오픈소스마케팅"),
            ("설립일", "2020년 12월 14일"),
            ("대표이사", "오승종"),
            ("업종", "경영 컨설팅업, 광고 대행업, 마케팅 교육업, 응용 소프트웨어 개발 및 공급"),
            ("소재지", "서울특별시 강남구 봉은사로37길 5, 4층"),
            ("연락", "contact@osoma.kr / osoma.kr")]
    points = [("컨설팅과 개발을 함께 합니다",
               "응용 소프트웨어 개발이 업종에 들어 있습니다. 분석 도구를 직접 만들어 프로젝트에 씁니다."),
              ("교육이 사업의 한 축입니다",
               "마케팅 교육업이 별도 업종입니다. 고객사 담당자가 스스로 다루게 만드는 데까지가 사업 범위입니다."),
              ("2020년 12월에 시작했습니다",
               "프로젝트는 2022년부터 본격적으로 쌓였습니다.")]
    return split(n, P1, "회사", '<span class="gt">업종 넷</span>이 회사의 성격을 그대로 보여 줍니다',
                 "등록된 업종 네 가지",
                 "경영 컨설팅과 광고 대행, 마케팅 교육, 그리고 응용 소프트웨어 개발입니다. "
                 "네 해 동안 한 일이 이 넷을 벗어나지 않았습니다.",
                 points, _info(rows), "")


def s_problem(n):
    HEADERS[n] = "고객사가 들고 오는 문제 넷"
    items = [("광고비를 쓰는데 무엇이 통했는지 모릅니다",
              "매체가 보내 주는 숫자와 실제 매출이 맞지 않습니다. 어느 광고를 끄고 어느 광고를 늘릴지 정할 근거가 없습니다."),
             ("화면 안에서 고객이 무엇을 하는지 안 보입니다",
              "방문자 수는 알지만 어디서 이탈하는지는 모릅니다. 고칠 자리를 짚지 못합니다."),
             ("무엇을 성과로 셀지부터 정해지지 않았습니다",
              "구매가 없는 회사일수록 심합니다. 부서마다 다른 숫자를 성과라고 부릅니다."),
             ("데이터를 쌓아 두었는데 읽는 사람이 없습니다",
              "도구는 도입했지만 담당자가 다루지 못해 화면이 방치됩니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "문제", "", icons=["scale", "eye", "missing", "search"])
             + band('네 문제는 따로 오지 않습니다. 무엇을 셀지 정하지 않은 채로 광고비만 커지면 넷이 함께 나타납니다. '
                    '<strong>그래서 우리는 세는 일부터 다시 만듭니다.</strong>')
             + '</div>')
    return wide(n, P1, "출발점", '고객사는 <span class="gt">같은 자리</span>에서 막혀 있습니다',
                "고객사가 들고 오는 문제 넷",
                "네 해 동안 만난 회사들이 처음에 꺼내는 말은 크게 넷입니다. 업종이 달라도 반복됩니다.",
                inner, "")


def s_ground(n):
    HEADERS[n] = "분석 환경이라는 말의 뜻"
    yes = [("지난달 광고 가운데 매출로 이어진 것은 어느 것입니까",
            "매체별로 유입부터 구매까지 한 줄로 이어 볼 수 있습니다."),
           ("장바구니에서 결제로 넘어가는 비율은 얼마입니까",
            "단계마다 이탈을 세어 두었기 때문에 바로 나옵니다."),
           ("첫 구매 고객과 재구매 고객은 어떻게 다르게 움직입니까",
            "행동마다 고객 구분을 함께 남겨 두었기 때문입니다.")]
    no = [("방문자가 늘었는데 매출은 왜 그대로입니까",
           "무엇을 보고 왔는지 기록이 없어 원인을 좁히지 못합니다."),
          ("어느 화면에서 이탈이 가장 큽니까",
           "화면 이동을 세지 않으면 지나온 순서를 되돌릴 수 없습니다."),
          ("이번 캠페인은 성공입니까",
           "기준을 미리 정해 두지 않아 판단이 사람마다 갈립니다.")]
    inner = ('<div class="vcen">' + asks(yes, no)
             + band('질문이 어려워서 답이 안 나오는 것이 아닙니다. '
                    '<strong>무엇을 셀지 미리 정해 두지 않으면 지나간 행동은 되돌려 셀 수 없습니다.</strong>')
             + '</div>')
    return wide(n, P1, "분석 환경", '<span class="gt">분석 환경</span>은 질문에 답할 수 있는 상태입니다',
                "분석 환경이라는 말의 뜻",
                "웹과 앱에서 벌어지는 행동을 정해 둔 이름으로 기록해 두는 일입니다. "
                "이것이 되어 있는지에 따라 답할 수 있는 질문이 갈립니다.",
                inner, "")


def s_did_what(n):
    HEADERS[n] = "우리가 하는 네 갈래의 일"
    items = [("분석 환경 구축", "무엇을 셀지 정하고, 기록이 남게 심고, 담당자가 보는 화면까지 놓습니다. 네 해 동안 가장 많이 한 일입니다."),
             ("그로스 마케팅", "쌓인 숫자로 가설을 세우고 매체와 자사몰에서 실험을 돌립니다. 집행까지 함께 붙습니다."),
             ("교육과 지원사업 운영", "고객사 담당자를 가르치고, 국가 지원사업의 운영사를 맡습니다."),
             ("AX 컨설팅", "2025년 말부터 들어온 일입니다. 업무 순서 안에 AI를 넣고 도구를 붙입니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "갈래", "", icons=["chart", "target", "book", "bolt"])
             + band('네 갈래가 따로 팔린 적은 거의 없습니다. '
                    '<strong>분석 환경을 깔고 그 위에서 마케팅을 돌리는 한 덩어리였습니다.</strong>')
             + '</div>')
    return wide(n, P1, "한 일의 갈래", '일로 보면 <span class="gt">네 갈래</span>입니다',
                "우리가 하는 네 갈래의 일",
                "분석 환경을 가운데 두면 일이 넷으로 갈라집니다. 2022년부터 2025년까지 한 프로젝트를 성격으로 묶었습니다.",
                inner, "")


def s_value(n):
    HEADERS[n] = "맡기기 전과 맡긴 뒤"
    rows = [(("숫자를 대행사가 들고 있습니다", "계약이 끝나면 판단 근거도 함께 나갑니다"),
             ("숫자가 회사 안에 쌓입니다", "우리가 빠져도 기록은 남아 계속 쌓입니다")),
            (("성과 기준이 부서마다 다릅니다", "같은 캠페인을 두고 평가가 갈립니다"),
             ("성과 기준이 문서 하나로 고정됩니다", "이벤트 정의서에 적힌 대로 셉니다")),
            (("담당자가 바뀌면 처음부터 다시 합니다", "설정을 아는 사람이 없어 화면이 멈춥니다"),
             ("담당자가 직접 고칩니다", "고치는 법까지 넘기고 나옵니다"))]
    inner = ('<div class="vcen">' + vs("맡기기 전", "맡긴 뒤", rows)
             + band('우리가 남기는 것은 보고서가 아니라 <strong>회사가 계속 쓰는 기록 체계입니다.</strong> '
                    '다음 부에서 그 체계를 이루는 실물을 하나씩 봅니다.')
             + '</div>')
    return wide(n, P1, "가치", '판단의 <span class="gt">근거</span>가 회사 안에 남습니다',
                "맡기기 전과 맡긴 뒤",
                "일이 끝난 뒤 고객사에 무엇이 남는지로 우리 일을 설명합니다.",
                inner, "")


# ══ 2부 일하는 방식, 실물로 ════════════════════════════════════════════

def s_did_steps(n):
    HEADERS[n] = "구축이 지나는 여섯 단계"
    flow = [("무엇을 셀지 정합니다",
             "화면을 함께 보며 성과로 셀 행동을 고릅니다. 여기서 고르지 않은 행동은 나중에 되돌려 볼 수 없습니다."),
            ("이벤트 정의서로 적습니다",
             "행동의 이름과 발생 조건, 함께 남길 정보를 표로 적습니다. 개발과 마케팅이 같은 문서를 봅니다."),
            ("기록이 남도록 심습니다",
             "개발이 코드를 심고, 우리가 태그를 붙여 행동마다 기록이 남게 합니다."),
            ("검수합니다",
             "빠진 기록과 두 번 세어진 기록을 잡습니다. 여기서 걸러야 화면의 숫자를 믿을 수 있습니다."),
            ("보는 화면을 만듭니다",
             "담당자가 매일 여는 대시보드에 지표를 배치합니다. 항목을 직접 더할 수 있는 구조로 둡니다."),
            ("넘깁니다",
             "정의서 읽는 법과 태그 고치는 법을 교육으로 옮깁니다.")]
    facts = [("고정", "여섯 단계", "업종이 달라도 순서가 바뀌지 않습니다"),
             ("중심", "정의서", "네 번째 단계까지가 정의서를 지키는 일입니다"),
             ("증거", "실물 여섯 장", "단계마다 남는 산출물을 다음 장부터 실제 화면으로 봅니다")]
    inner = ('<div class="vcen">' + howto(flow, facts)
             + band('말로 하면 여섯 줄이지만, 단계마다 실물이 남습니다. '
                    '<strong>다음 여섯 장이 그 실물입니다.</strong>')
             + '</div>')
    return wide(n, P2, "일하는 순서", '정하고, 적고, 심고, <span class="gt">검수하고</span>, 넘깁니다',
                "구축이 지나는 여섯 단계",
                "분석 환경 구축은 업종이 달라도 이 순서를 지납니다.",
                inner, "")


def s_shot_spec(n):
    HEADERS[n] = "실물 하나, 이벤트 정의서"
    gicon = '<svg viewBox="0 0 24 24"><path d="M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zm-9 14H7v-2h3zm0-4H7v-2h3zm0-4H7V7h3zm7 8h-5v-2h5zm0-4h-5v-2h5zm0-4h-5V7h5z"/></svg>'
    rows = [("견적 및 도입문의", "견적 문의 1단계", "add_to_cart", "step", "견적 문의 순서", "고정: 1"),
            ("", "", "", "item_type", "1단계 검색 유형", "제품별 또는 플랫폼별"),
            ("", "견적 문의 2단계", "begin_checkout", "items.item_name", "제품 이름", "지능형 위협 대응"),
            ("", "", "", "items.item_variant", "재계약 여부", "y/n"),
            ("", "견적 문의 3단계, 완료", "purchase", "company_type", "회사 유형", "공공/교육/기업/금융"),
            ("회원가입", "회원가입 완료", "sign_up_3_complete", "account_type", "회원 구분", "기업회원/개인회원"),
            ("", "", "", "mkt_agreement", "마케팅 수신 동의", "y/n")]
    trs = "".join(
        f'<tr><td class="grp">{g}</td><td>{e}</td><td class="mono">{ev}</td>'
        f'<td class="mono">{p}</td><td>{d}</td><td>{x}</td></tr>'
        for g, e, ev, p, d, x in rows)
    sheet = (f'<div class="gsheet"><div class="gbar"><i>{gicon}</i>'
             '<b>안랩 한국어 웹사이트 GA4 이벤트 정의서</b><span>실제 문서에서 견적 문의 부분을 옮겼습니다</span></div>'
             '<table><colgroup><col style="width:12%"><col style="width:17%"><col style="width:17%">'
             '<col style="width:17%"><col style="width:18%"><col style="width:19%"></colgroup>'
             '<tr><th>구분</th><th>이벤트</th><th>이벤트명</th><th>매개변수</th><th>뜻</th><th>값 예시</th></tr>'
             f'{trs}</table>'
             '<div class="gtabs"><span class="on">PC</span><span>MO</span></div></div>')
    metas = [("어떤 화면", "구축 2단계의 산출물, 이벤트 정의서입니다",
              "안랩 웹사이트에서 무엇을 언제 세는지 적은 실제 문서입니다. 견적 문의가 세 단계로 나뉘어 있습니다."),
             ("어떤 작업", "성과로 셀 행동에 이름을 붙입니다",
              "구매가 없는 B2B 사이트라 견적 문의 완료를 구매처럼 세도록 정했습니다. 부서마다 다르던 성과 기준이 이 표 하나로 고정됩니다."),
             ("어디로 이어지나", "뒤의 모든 작업이 이 문서를 따릅니다",
              "개발이 이 표를 보고 코드를 심고, 우리가 이 표대로 검수하고, 대시보드도 이 이름으로 집계합니다.")]
    inner = shot("", "", metas, "2024년 안랩 프로젝트에서 실제로 쓴 정의서입니다. 문서 원본은 구글 시트로 고객사에 남아 있습니다.",
                 inner_html=sheet)
    return wide(n, P2, "실물 1", '무엇을 셀지 <span class="gt">문서 하나</span>에 고정합니다',
                "실물 하나, 이벤트 정의서", "", inner, "")


def s_shot_guide(n):
    HEADERS[n] = "실물 둘, 스크립트 가이드"
    code = ('<div class="codebox"><div class="cfile">장바구니 페이지 / 신세계면세점 스크립트 삽입 가이드</div>'
            '<pre><span class="cc">// 장바구니 페이지 진입 시 아래 스크립트를 실행합니다</span>\n'
            'dataLayer.push({\n'
            '  <span class="ck">event</span>: <span class="cs">\'view_cart\'</span>,\n'
            '  <span class="ck">items</span>: [{\n'
            '    <span class="ck">item_id</span>:       <span class="cs">\'{상품 ID}\'</span>,\n'
            '    <span class="ck">item_name</span>:     <span class="cs">\'{상품 이름}\'</span>,\n'
            '    <span class="ck">item_brand</span>:    <span class="cs">\'{브랜드 이름}\'</span>,\n'
            '    <span class="ck">item_category</span>: <span class="cs">\'{카테고리 이름}\'</span>,\n'
            '    <span class="ck">price</span>:         <span class="cs">\'{상품 판매가}\'</span>,\n'
            '    <span class="ck">quantity</span>:      <span class="cs">\'{상품 수량}\'</span>\n'
            '  }]\n'
            '});</pre></div>')
    combo = ('<div style="display:grid;grid-template-columns:auto 1fr;gap:26px;align-items:center;min-width:0">'
             '<img src="assets/capture/guide_mobile.png" alt="신세계면세점 모바일 화면에 표시 위치를 붉은 상자로 표시한 가이드"'
             ' style="max-height:600px;width:auto;border-radius:16px;border:1.5px solid var(--line);'
             'box-shadow:0 16px 40px rgba(20,25,40,.14)">'
             f'{code}</div>')
    metas = [("어떤 화면", "구축 3단계의 산출물, 스크립트 가이드입니다",
              "왼쪽은 신세계면세점 모바일 화면에 표시 위치를 붉은 상자로 짚은 가이드이고, 오른쪽은 그 자리에 심는 실제 코드입니다."),
             ("어떤 작업", "개발자가 그대로 붙이게 만듭니다",
              "화면마다 어느 자리에서 어떤 코드를 실행할지 적어 넘깁니다. 개발이 해석할 여지를 없애는 것이 이 문서의 목적입니다."),
             ("어디로 이어지나", "정의서의 이름이 코드가 됩니다",
              "정의서에 적은 view_cart라는 이름이 이 코드로 심어지고, 심어진 그대로 다음 단계의 검수 대상이 됩니다.")]
    inner = shot("", "", metas, "2023년 신세계면세점 프로젝트에서 실제로 넘긴 가이드입니다.", rev=True, inner_html=combo)
    return wide(n, P2, "실물 2", '개발자가 <span class="gt">그대로 붙일 수 있게</span> 적습니다',
                "실물 둘, 스크립트 가이드", "", inner, "")


def s_shot_debug(n):
    HEADERS[n] = "실물 셋, 검수 화면"
    metas = [("어떤 화면", "구축 4단계, 검수 작업의 실제 화면입니다",
              "왼쪽은 신세계면세점 상품 화면이고 오른쪽 콘솔에 방금 심은 기록이 실시간으로 찍히고 있습니다. 붉은 상자 안이 잘못 들어온 값입니다."),
             ("어떤 작업", "빠진 기록과 틀린 값을 잡습니다",
              "화면을 하나하나 눌러 보며 정의서와 다르게 들어오는 값을 찾습니다. 이 화면에서는 카테고리 값이 비어 들어와 수정 대상으로 기록했습니다."),
             ("어디로 이어지나", "대시보드의 숫자를 믿게 만듭니다",
              "여기서 거르지 않으면 틀린 숫자가 그대로 집계됩니다. 검수를 통과한 데이터만 다음 장의 대시보드에 오릅니다.")]
    inner = shot("assets/capture/debug_console.jpg",
                 "신세계면세점 상품 화면과 개발자 도구 콘솔로 수집 값을 검수하는 실제 화면",
                 metas, "2023년 신세계면세점 디버깅 방문 기록에 남은 실제 검수 화면입니다.")
    return wide(n, P2, "실물 3", '숫자를 <span class="gt">믿게 만드는</span> 단계입니다',
                "실물 셋, 검수 화면", "", inner, "")


def s_shot_dash(n):
    HEADERS[n] = "실물 넷, 대시보드"
    metas = [("어떤 화면", "구축 5단계의 산출물, 루커 스튜디오 대시보드입니다",
              "베스핀글로벌 프로젝트에서 만든 GA4 대시보드의 콘텐츠 분석 탭입니다. 문의까지 가는 길목이 한 화면에 모여 있습니다."),
             ("어떤 작업", "쌓인 기록을 판단할 수 있는 모양으로 놓습니다",
              "서비스 조회, 문의 단계별 이탈, 콘텐츠별 읽힘 깊이까지 정의서에서 정한 이름 그대로 집계됩니다."),
             ("어디로 이어지나", "회의가 이 화면에서 시작됩니다",
              "어느 콘텐츠가 문의로 이어졌는지가 바로 보이므로, 감이 아니라 이 화면을 근거로 다음 콘텐츠를 정하게 됩니다.")]
    inner = shot("assets/capture/looker_dashboard.png",
                 "베스핀글로벌 GA4 대시보드의 콘텐츠 및 웹사이트 분석 화면",
                 metas, "2026년 베스핀글로벌 프로젝트에서 실제로 운영 중인 대시보드입니다.")
    return wide(n, P2, "실물 4", '담당자가 <span class="gt">매일 여는 화면</span>을 만듭니다',
                "실물 넷, 대시보드", "", inner, "")


def s_shot_bq(n):
    HEADERS[n] = "실물 다섯, 빅쿼리 연결"
    metas = [("어떤 화면", "GA4 관리 화면에서 빅쿼리를 연결하는 자리입니다",
              "신세계면세점에 넘긴 연결 가이드의 한 장면입니다. 붉은 상자 안이 눌러야 할 메뉴입니다."),
             ("어떤 작업", "기록의 원본을 회사 창고에 쌓습니다",
              "GA4 화면은 요약만 보여 주고 원본은 일정 기간 뒤 지워집니다. 빅쿼리에 연결해 두면 행동 하나하나가 회사 소유의 창고에 그대로 쌓입니다."),
             ("어디로 이어지나", "뒤에 나올 AI 분석의 재료가 됩니다",
              "AI에게 데이터를 읽혀 분석하는 일도, 몇 년치 행동을 되짚는 일도 이 창고가 있어야 가능합니다.")]
    inner = shot("assets/capture/ga4_bigquery.png",
                 "GA4 관리 화면에서 빅쿼리 링크 메뉴를 붉은 상자로 표시한 가이드",
                 metas, "신세계면세점에 넘긴 GA4 빅쿼리 연결 가이드의 실제 화면입니다. 시연용 테스트 계정으로 만들었습니다.")
    return wide(n, P2, "실물 5", '데이터가 <span class="gt">회사의 자산</span>으로 쌓입니다',
                "실물 다섯, 빅쿼리 연결", "", inner, "")


def s_shot_handover(n):
    HEADERS[n] = "실물 여섯, 인계 문서"
    nside = ('<div class="nside">'
             '<div class="nrow">&#128193; 태깅 컨설팅</div>'
             '<div class="nrow d1 on">&#128218; 교보문고</div>'
             '<div class="nrow d2">회의록</div>'
             '<div class="nrow d2 on">결과 산출물</div>'
             '<div class="nrow d1">&#128218; 신세계 면세점</div>'
             '<div class="nrow d1">&#128218; 안랩</div>'
             '<div class="nrow d1">&#128218; 소브린</div>'
             '<div class="nrow d1">&#128218; 하우스버디</div>'
             '<div class="nrow d1">&#128218; 나비엔하우스</div>'
             '</div>')
    nmain = ('<div class="nmain"><h3>&#128218; 결과 산출물</h3>'
             '<div class="nitem"><i>&#128196;</i>이벤트 정의서 공유 문서<span>시트 8개 연결</span></div>'
             '<div class="nitem"><i>&#128196;</i>스크립트 삽입 가이드<span>화면별 코드</span></div>'
             '<div class="nitem"><i>&#128196;</i>GA4 빅쿼리 연결 가이드<span>단계별 캡처</span></div>'
             '<div class="nitem"><i>&#128196;</i>루커 스튜디오 생성 가이드<span>대시보드 만들기</span></div>'
             '<div class="nitem"><i>&#128196;</i>디버깅 방문 기록<span>검수 결과</span></div>'
             '<div class="nitem"><i>&#128196;</i>온보딩에서 다룰 것<span>인계 교육 자료</span></div>'
             '</div>')
    notion = f'<div class="notionui">{nside}{nmain}</div>'
    metas = [("어떤 화면", "고객사별 인계 문서를 모아 둔 노션입니다",
              "고객사마다 방 하나씩을 두고 회의록과 결과 산출물을 모두 남깁니다. 교보문고 방의 실제 구성을 옮겼습니다."),
             ("어떤 작업", "여섯 단계의 산출물을 한자리에 모읍니다",
              "앞에서 본 정의서, 가이드, 검수 기록이 전부 이 방에 들어갑니다. 프로젝트가 끝나면 방을 통째로 고객사에 넘깁니다."),
             ("어디로 이어지나", "담당자가 바뀌어도 일이 이어집니다",
              "새 담당자가 이 방만 읽으면 무엇을 어떻게 세고 있는지 파악할 수 있습니다. 우리가 빠져도 남는 가치가 여기 있습니다.")]
    inner = shot("", "", metas, "실제 노션 워크스페이스의 교보문고 문서방 구성을 이름 그대로 옮겼습니다.",
                 inner_html=notion)
    return wide(n, P2, "실물 6", '우리가 빠져도 <span class="gt">기록은 남습니다</span>',
                "실물 여섯, 인계 문서", "", inner, "")


def s_growth(n):
    HEADERS[n] = "쌓인 숫자로 하는 그로스 마케팅"
    metas = [("어떤 화면", "사이버한국외대 광고 성과 대시보드입니다",
              "검색광고 키워드별, 배너 캠페인별로 방문과 상담 신청이 몇 건씩 나왔는지 집계한 실제 화면입니다."),
             ("어떤 작업", "광고비의 성적표를 만들고 실험을 돌립니다",
              "전환이 없는 키워드와 상담으로 이어지는 키워드가 한눈에 갈립니다. 못 하는 광고를 끄고 잘하는 광고에 예산을 옮깁니다."),
             ("어디로 이어지나", "광고비 결정이 감에서 숫자로 바뀝니다",
              "분석 환경이 있어야 이 성적표가 나옵니다. 구축과 그로스가 한 덩어리로 팔리는 이유입니다.")]
    inner = shot("assets/capture/looker_ads.png",
                 "사이버한국외대 검색광고 키워드 성과와 배너 캠페인 성과 대시보드",
                 metas, "2026년 사이버한국외대 입학 홍보 프로젝트의 실제 광고 성과 화면입니다.")
    return wide(n, P2, "그로스 마케팅", '분석 다음은 <span class="gt">실험</span>입니다',
                "쌓인 숫자로 하는 그로스 마케팅", "", inner, "")


# ══ 3부 스물네 곳을 동시에 ═════════════════════════════════════════════

def s_kto_what(n):
    HEADERS[n] = "세 해째 맡고 있는 국가 지원사업"
    items = [("24", "참여 기업", "2026년 사업에서 동시에 진행하는 기업 수입니다."),
             ("11", "컨설턴트", "우리 다섯 명에 파트너사 인력을 붙여 편성합니다."),
             ("4", "개월", "6월에 열어 9월과 10월에 닫습니다.")]
    inner = (_facts(items, "three")
             + band('기업 한 곳에서 하는 일은 앞에서 본 컨설팅과 같습니다. '
                    '다른 것은 스물네 곳을 동시에 진행하면서 공사에 한 목소리로 보고하는 일이고, '
                    '<strong>그 운영의 실물이 다음 두 장입니다.</strong>'))
    return wide(n, P3, "사업 개요", '한국관광공사 <span class="gt">데이터와 AI 활용 지원사업</span>',
                "세 해째 맡고 있는 국가 지원사업",
                "2024년부터 세 해 연속으로 운영사를 맡았고, 세 번째 사업이 진행 중입니다.",
                inner, "")


def _slack_msgs(head_note, msgs):
    colors = {"김": "#4A90D9", "박": "#E8912D", "이": "#7C5CBF", "홍": "#3AA675", "조": "#D95970", "유": "#5B8A72"}
    out = [f'<div class="shead"><b>kto_전체_컨설턴트</b><span>{head_note}</span></div>']
    for who, when, html, bot in msgs:
        if bot:
            ava = '<div class="sava bot-i" style="background:linear-gradient(135deg,#4A154B,#7C3085)">&#129302;</div>'
            name = f'<div class="sname">{who}<span>앱 / {when}</span></div>'
        else:
            c = colors.get(who[5] if len(who) > 5 else "김", "#4A90D9")
            ava = f'<div class="sava" style="background:{c}">{who[5] if len(who) > 5 else ""}</div>'
            name = f'<div class="sname">{who}<span>{when}</span></div>'
        out.append(f'<div class="smsg{" bot" if bot else ""}">{ava}'
                   f'<div class="sbody">{name}<div class="stext">{html}</div></div></div>')
    return f'<div class="slackui">{"".join(out)}</div>'


def s_shot_slack(n):
    HEADERS[n] = "실물, 회차 등록 채널"
    msgs = [
        ("컨설턴트_박OO", "9월 2일 19:04",
         '&#9654; <em>8회차 미팅 확정</em><br>호퍼스: 9월 3일(목) 오전 10시 - 온라인', False),
        ("컨설턴트_이OO", "9월 2일 17:38",
         '&#9654; <em>8회차 미팅 확정</em><br>세상에없는세상: 9월 9일(수) 오전 11시 - 온라인', False),
        ("컨설턴트_김OO", "9월 2일 15:06",
         '&#9654; <em>8회차 미팅 확정</em><br>레프트아이템딜리버리: 9월 14일(월) 오후 3시 - 온라인', False),
        ("컨설턴트_홍OO", "8월 26일 10:45",
         '&#9654; <em>7회차 미팅 확정</em><br>그리니어: 8월 31일(월) 오전 10시 30분 - 오프라인', False),
        ("컨설턴트_조OO", "8월 26일 10:57",
         '&#9654; <em>8회차 미팅 확정</em><br>한국드림관광: 9월 2일(수) 오전 11시 - 오프라인', False),
    ]
    pane = _slack_msgs("컨설턴트 11명이 함께 쓰는 공용 채널", msgs)
    metas = [("어떤 화면", "컨설턴트 공용 슬랙 채널입니다",
              "2026년 사업의 실제 채널 기록을 옮겼고 컨설턴트 이름만 가렸습니다. 미팅이 잡힐 때마다 같은 형식 한 줄이 쌓입니다."),
             ("어떤 작업", "일정을 모으지 않고 쌓이게 둡니다",
              "회차, 기업명, 일시, 온오프라인만 적는 형식을 정해 두었습니다. 취합 담당자가 없어도 채널 하나가 전체 일정표가 됩니다."),
             ("어디로 이어지나", "운영진은 빈 곳만 봅니다",
              "스물네 곳의 회차 진도가 채널을 훑으면 보이므로, 밀린 기업의 채널만 골라 들어가 확인합니다.")]
    inner = shot("", "", metas, "2026년 9월 첫 주의 실제 채널 기록입니다. 컨설턴트 이름은 가렸습니다.",
                 inner_html=pane)
    return wide(n, P3, "실물, 회차 등록", '모으지 않고 <span class="gt">쌓이게</span> 둡니다',
                "실물, 회차 등록 채널", "", inner, "")


def s_shot_bot(n):
    HEADERS[n] = "실물, 봇이 대신 챙기는 마감"
    msgs = [
        ("알림이", "금요일 15:00",
         '<span class="schip">@channel</span> &#9989; <em>주간 이슈 기입 리마인드</em><br>'
         '금요일입니다. 주간 성과와 진행 상황, 미팅록 작성 부탁드립니다.<br>'
         '- 차주 월요일 11:00까지<br>- 각 기업별 [컨설팅 진행 노트] 문서 내 [주간 요약] 탭', True),
        ("알림이", "8월 24일 11:00",
         '&#9989; <em>[유형2] 3차(9월) 캠페인 계획서 리마인드</em><br>'
         '계획서 제출까지 D-1 남았습니다. 각 기업별 구글 문서 내 계획서 작성을 부탁드립니다.<br>'
         '- 제출 기한: 8월 25일(화) 15:00까지', True),
        ("알림이", "9월 2일 11:00",
         '<span class="schip">@channel</span> &#9989; <em>월간보고 & 캠페인 결과보고서 리마인드</em><br>'
         '제출까지 D-1 남았습니다. 수치는 8월 최종 데이터 기준으로 작성 부탁드립니다.<br>'
         '&#128204; 제출 기한: 9월 3일(목) 15:00까지', True),
    ]
    pane = _slack_msgs("마감을 챙기는 자동 알림", msgs)
    metas = [("어떤 화면", "마감을 알리는 봇의 실제 메시지입니다",
              "주간 기입은 매주 금요일 15시, 계획서와 보고서는 D-7, D-2, D-1에 자동으로 올라옵니다."),
             ("어떤 작업", "사람이 챙기던 독촉을 봇에 맡겼습니다",
              "스물네 곳의 마감을 사람이 챙기면 챙기는 일만으로 하루가 찹니다. 알림은 봇이 하고, 운영진은 안 채워진 곳에만 답을 답니다."),
             ("어디로 이어지나", "주간 두세 줄이 월간 보고가 됩니다",
              "이렇게 모인 주간 기록이 그대로 월간 이슈 공유 문서가 되어, 공사 보고 자료를 따로 만들지 않습니다.")]
    inner = shot("", "", metas, "2026년 사업 채널에 실제로 올라온 봇 메시지입니다.", rev=True, inner_html=pane)
    return wide(n, P3, "실물, 봇 리마인드", '사람이 아니라 <span class="gt">봇이 챙깁니다</span>',
                "실물, 봇이 대신 챙기는 마감", "", inner, "")


def s_kto_rate(n):
    rows = [("60%", "이벤트 정의서 확정, 수집 구조 설계 완료"),
            ("70%", "스크립트 설치와 이벤트 세팅, 검수 진행"),
            ("80%", "분석 도구와 AI 자연어 분석 환경 설정 완료"),
            ("90%", "시각화 대시보드 제작, AI 자동 리포트 구축"),
            ("100%", "내재화 교육 완료, 산출물 인계")]
    points = [("숫자를 감으로 적지 않습니다",
               "기준표를 만들어 두고 그 단계에 닿았을 때만 숫자를 올립니다."),
              ("컨설턴트가 달라도 같은 값이 나옵니다",
               "파트너사 인력이 섞여 있어도 70퍼센트의 뜻이 같습니다."),
              ("멈춘 자리가 드러납니다",
               "여러 주 같은 숫자에 머물면 어느 단계에서 막혔는지 보입니다.")]
    return split(n, P3, "진행률", '<span class="gt">70퍼센트</span>가 무엇인지 정해 둡니다',
                 "진행률을 맞추는 기준표",
                 "주간 보고에 함께 적는 숫자입니다. 적는 사람마다 뜻이 달라지므로 단계마다 기준을 정해 둡니다. 오른쪽이 실제 기준표입니다.",
                 points, _info(rows), "")


def s_kto_report(n):
    HEADERS[n] = "공사에 보고하는 세 층"
    items = [("주간", "기업별 구글 문서의 주간 요약 탭입니다. 두세 줄과 진행률을 컨설턴트가 직접 씁니다."),
             ("월간", "한국관광공사 서울센터에서 대면으로 보고합니다. 주간 기록이 모인 유형별 마스터 시트가 자료입니다."),
             ("차수별", "유형 2는 캠페인 계획서를 먼저 내고 집행 뒤 결과보고서를 냅니다. 앞 장의 봇이 D-7과 D-2에 알립니다.")]
    inner = ('<div class="vcen">'
             + cards(items, "층", "three", icons=["clock", "flag", "file"])
             + band('주간 요약이 월간 보고가 되고, 차수별 결과보고서가 최종 성과가 됩니다. '
                    '세 층이 같은 자료를 쓰기 때문에 옮겨 적는 일이 없고, '
                    '<strong>지표나 계획이 바뀌면 사유를 적어 스레드 한곳에 남깁니다.</strong>')
             + '</div>')
    return wide(n, P3, "성과 보고", '주간, 월간, <span class="gt">차수별</span>로 나눕니다',
                "공사에 보고하는 세 층",
                "주간에 쌓인 것이 위로 어떻게 올라가는지 봅니다. 주기마다 문서를 새로 만들면 스물네 곳을 감당하지 못합니다.",
                inner, "")


# ══ 4부 AI를 얹은 자리 ═════════════════════════════════════════════════

def s_ai_shift(n):
    HEADERS[n] = "일의 성격이 바뀐 자리"
    rows = [(("분석 환경을 세워 주고 나옵니다", "무엇을 셀지 정하고 기록을 심어 두는 일이었습니다"),
             ("쌓인 데이터로 판단까지 갑니다", "베스핀글로벌 리드 스코어링처럼 무엇이 유망한지 매기는 일이 들어왔습니다")),
            (("대시보드를 만들어 줍니다", "사람이 열어 보고 해석하는 화면이었습니다"),
             ("AI가 먼저 읽고 짚어 줍니다", "남유 FNC 광고 분석처럼 어디를 볼지 도구가 먼저 말합니다")),
            (("도구 다루는 법을 가르칩니다", "분석 도구를 쓰는 방법이었습니다"),
             ("업무 순서를 다시 짭니다", "AI를 어느 단계에 넣을지가 교육 주제가 되었습니다"))]
    inner = ('<div class="vcen">' + vs("2024년까지", "2025년 말부터", rows)
             + band('2025년 12월에 <strong>AI 리드 스코어링</strong>과 '
                    '<strong>AI 광고 분석 대시보드</strong>가 처음 들어왔습니다. '
                    '그 뒤로 AI를 심는 순서가 자리를 잡았습니다.')
             + '</div>')
    return wide(n, P4, "달라진 것", '맡는 일이 <span class="gt">판단 쪽으로</span> 옮겨 왔습니다',
                "일의 성격이 바뀐 자리",
                "다루는 데이터는 같지만 어디까지 맡는지가 달라졌습니다.",
                inner, "")


def s_ai_flow(n):
    HEADERS[n] = "고객사에 AI를 심는 다섯 단계"
    steps = [("현황 진단", "지금 누가 무엇에 쓰고 있는지 봅니다. 개인이 챗봇 하나를 쓰는 상태가 대부분입니다."),
             ("구독 설계", "어떤 도구를 몇 계정, 어느 요금제로 쓸지 정합니다. 예산과 정산 방식까지 함께 봅니다."),
             ("환경 구성", "담당자 노트북에 도구를 설치하고 회사 데이터에 연결합니다. 이 단계를 대면으로 합니다."),
             ("스킬과 자동화", "반복 업무 하나를 골라 자동화합니다. 담당자가 직접 손을 움직이는 실습으로 넘깁니다."),
             ("내재화", "새 업무에 스스로 붙일 수 있게 두고 나옵니다.")]
    inner = ('<div class="vcen">' + stepflow(steps, hot=(3,))
             + band('요리책을 주는 회사는 많지만 부엌에 같이 서는 회사는 드뭅니다. '
                    '우리는 세 번째 단계에서 담당자 노트북을 함께 열고, '
                    '<strong>회사 데이터에 연결된 상태로 만들어 놓고 나옵니다. 그 결과가 다음 두 장입니다.</strong>')
             + '</div>')
    return wide(n, P4, "AI 컨설팅", '쓰라고 말하는 대신 <span class="gt">쓰게 만듭니다</span>',
                "고객사에 AI를 심는 다섯 단계",
                "도구를 소개하는 일과 실제로 쓰게 만드는 일 사이에 이 다섯 단계가 있습니다.",
                inner, "")


def s_ai_chat(n):
    HEADERS[n] = "설치 결과 하나, 말로 묻는 분석"
    chat = ('<div class="aichat">'
            '<div class="ahead"><i></i><b>GA4 자연어 분석 / 담당자 노트북에 설치한 화면</b></div>'
            '<div class="amsg user"><div class="abub">지난주 어느 채널에서 온 방문이 문의로 가장 많이 이어졌어?</div></div>'
            '<div class="amsg"><div class="arun"><i></i>GA4에서 지난주 채널별 방문과 문의 완료를 조회하고 있습니다</div>'
            '<table class="atable"><tr><th>유입 채널</th><th style="text-align:right">방문</th>'
            '<th style="text-align:right">문의 완료</th><th style="text-align:right">전환율</th></tr>'
            '<tr class="hot"><td>네이버 검색광고</td><td class="num">4,120</td><td class="num">86</td><td class="num">2.09%</td></tr>'
            '<tr><td>구글 검색</td><td class="num">2,860</td><td class="num">41</td><td class="num">1.43%</td></tr>'
            '<tr><td>인스타그램 광고</td><td class="num">5,340</td><td class="num">37</td><td class="num">0.69%</td></tr>'
            '<tr><td>직접 방문</td><td class="num">1,980</td><td class="num">22</td><td class="num">1.11%</td></tr></table>'
            '<div class="asum">문의로 가장 많이 이어진 채널은 네이버 검색광고입니다. 인스타그램은 방문이 가장 많지만 '
            '전환율이 3분의 1 수준이라, 예산 재배분을 검토할 자리입니다.</div></div></div>')
    metas = [("어떤 화면", "말로 물으면 GA4를 조회해 답합니다",
              "담당자가 보고서 화면을 다루는 법을 몰라도, 평소 말로 묻던 질문을 그대로 던지면 됩니다."),
             ("비유하면", "데이터 창고에 창고지기를 앉힌 셈입니다",
              "지금까지는 창고에서 물건을 찾으려면 정리법을 배워야 했습니다. 이제는 창고지기에게 무엇이 필요한지 말하면 찾아다 줍니다."),
             ("어디로 이어지나", "질문의 횟수가 늘어납니다",
              "묻는 비용이 낮아지면 담당자가 더 자주 묻게 되고, 자주 물을수록 판단이 숫자에 가까워집니다.")]
    inner = shot("", "", metas,
                 "2026년 지원사업 참여 기업의 노트북마다 실제로 설치하는 기능입니다. 화면의 수치는 시연용 예시입니다.",
                 inner_html=chat)
    return wide(n, P4, "설치 결과 1", '보고서 대신 <span class="gt">질문</span>을 가르칩니다',
                "설치 결과 하나, 말로 묻는 분석", "", inner, "")


def s_ai_pipe(n):
    HEADERS[n] = "설치 결과 둘, 아침에 도착하는 리포트"
    arrow = '<div class="pipearrow"><svg viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6"/></svg></div>'
    pipe = ('<div class="pipe">'
            '<div class="pipenode"><b>재료</b><h4>GA4와 빅쿼리</h4><p>2부에서 심어 둔 기록이 매일 쌓입니다.</p></div>'
            + arrow +
            '<div class="pipenode"><b>매주 자동</b><h4>스크립트가 조회</h4><p>사람이 열던 화면을 정해진 시각에 코드가 대신 엽니다.</p></div>'
            + arrow +
            '<div class="pipenode hot"><b>AI</b><h4>읽고 요약</h4><p>지난주와 달라진 자리를 짚어 두세 문단으로 씁니다.</p></div>'
            + arrow +
            '<div class="pipenode"><b>도착</b><h4>슬랙과 문서로</h4><p>월요일 아침, 담당자 채널에 요약이 먼저 와 있습니다.</p></div>'
            '</div>')
    rows2 = [(("담당자가 화면을 엽니다", "매주 월요일 한 시간을 복사와 붙여넣기에 씁니다"),
              ("요약이 먼저 와 있습니다", "그 한 시간을 요약을 읽고 판단하는 데 씁니다"))]
    inner = ('<div class="vcen">' + pipe
             + '<div class="pipecap">' + vs("자동화 전", "자동화 뒤", rows2) + '</div>'
             + band('매주 자료를 오려 붙여 보고서를 만들던 사람에게, 아침마다 완성된 스크랩이 배달되는 것과 같습니다. '
                    '<strong>참여 기업마다 그 회사가 매주 손으로 하던 일 하나를 골라 이 흐름으로 바꿉니다.</strong>')
             + '</div>')
    return wide(n, P4, "설치 결과 2", '리포트가 <span class="gt">아침에 도착</span>합니다',
                "설치 결과 둘, 아침에 도착하는 리포트",
                "매주 반복되던 보고 작업 하나가 어떻게 바뀌는지 흐름으로 봅니다.",
                inner, "")


def s_ai_sub(n):
    points = [("한도 안에서 조합을 짭니다",
               "기업당 지원 한도가 정해져 있습니다. 무엇을 몇 개월 쓸지 계산해 조합을 제안합니다."),
              ("쓰임에 맞춰 요금제를 고릅니다",
               "개발 목적이면 상위 요금제를, 가벼운 작업이면 기본 요금제 계정을 여러 개 붙입니다."),
              ("정산까지 함께 봅니다",
               "선불 충전이나 사용량 과금은 정산 절차에 맞지 않습니다. 플랜 단위 결제를 권합니다.")]
    rows = [("한도", "기업당 지원 금액이 정해져 있습니다"),
            ("기간", "사업 기간 안에 다 쓰도록 나눕니다"),
            ("방식", "플랜 단위 월 구독을 권합니다"),
            ("증빙", "영수증을 모아 사업 종료 때 냅니다"),
            ("바뀔 때", "도구를 바꾸면 사유를 적어 공사에 올립니다")]
    return split(n, P4, "구독 설계", '<span class="gt">무엇을 구독할지</span>도 컨설팅입니다',
                 "구독을 설계하는 일",
                 "한도 안에서 도구를 어떻게 조합할지 정하는 일입니다. 예산을 어디에 쓰는지에 따라 성과가 달라집니다.",
                 points, _info(rows), "")


# ══ 5부 쌓인 것과 앞으로 ═══════════════════════════════════════════════

def s_clients(n):
    HEADERS[n] = "네 해 동안 만난 고객사"
    rows = [("유통과 커머스", "12건", [("교보문고", "on"), ("신세계면세점", "on"), ("반다이남코코리아", "on"),
                                  ("ABC마트", ""), ("스케쳐스코리아", ""), ("동원디어푸드", ""),
                                  ("신세계사이먼", ""), ("키플링, 이스트팩", ""), ("씨티닷츠, 던스트", ""),
                                  ("마켓올슨", ""), ("레시피그룹, 세터", ""), ("메터그룹, 몽디에스", "")]),
            ("IT와 금융", "13건", [("안랩", "on"), ("LG CNS", "on"), ("베스핀글로벌", "on"),
                                ("뤼튼테크놀로지", ""), ("오픈서베이", ""), ("지란지교소프트", ""),
                                ("신한퓨처스랩", ""), ("신한 글로벌 슛업", ""), ("신한S브릿지 8기와 9기", ""),
                                ("KT 알파", ""), ("유니드컴즈, 킵그로우", ""), ("소브린, DBPR", "")]),
            ("교육과 공공", "10건", [("한국관광공사", "on"), ("KOTRA", "on"), ("서울관광재단", ""),
                                 ("고려대학교", ""), ("연세대학교", ""), ("한림대학교", ""),
                                 ("이투스에듀", ""), ("인프런 강의 2종", "")]),
            ("제조와 서비스", "18건", [("경동나비엔", "on"), ("위닉스", ""), ("파크시스템스", ""),
                                  ("대림 e편한세상", ""), ("풀무원녹즙", ""), ("더플라자 호텔", ""),
                                  ("원밀리언", ""), ("열매나눔재단", ""), ("푸르메재단", ""),
                                  ("라그나로크 라틴아메리카", ""), ("로위", ""), ("메디트리", ""),
                                  ("남유 FNC", ""), ("빅픽처팀", ""), ("에프엠커뮤니케이션", "")])]
    inner = (_rows(rows, "grp")
             + band('성과의 정의는 업종마다 달랐습니다. 구매가 없는 회사에서는 문의와 상담을 성과로 잡았습니다. '
                    '<strong>정의가 달라져도 오늘 본 실물의 순서는 같았습니다.</strong>'))
    return wide(n, P5, "고객사", '한 업종에 <span class="gt">묶이지 않았습니다</span>',
                "네 해 동안 만난 고객사",
                "2022년부터 2025년까지 53건을 고객사 성격으로 묶으면 네 갈래입니다. 칸에 다 담기지 않은 곳은 생략했습니다.",
                inner, "")


def s_hist_next(n):
    HEADERS[n] = "쌓인 네 해와 앞으로 갈 두 갈래"
    rows = [("2022", "9건", [("KOTRA", "on"), ("서울관광재단 SEO", ""), ("신한S브릿지", ""), ("인프런 강의 2종", "on")]),
            ("2023", "14건", [("교보문고", "on"), ("신세계면세점", "on"), ("ABC마트", ""), ("더플라자 호텔", "")]),
            ("2024", "14건", [("한국관광공사 지원사업", "on"), ("안랩", "on"), ("반다이남코코리아", ""), ("고려대학교", "")]),
            ("2025", "16건", [("한국관광공사 지원사업", "on"), ("LG CNS", "on"),
                            ("베스핀글로벌 AI 리드 스코어링", "on"), ("남유 FNC AI 광고 대시보드", "on")])]
    items = [("AX를 주력으로",
              "분석과 마케팅 위에 AI를 얹는 일을 사업의 가운데로 옮깁니다. 도구를 파는 대신 업무 순서 안에 넣습니다."),
             ("도구를 제품으로",
              "안에서 쓰던 도구를 고객사가 직접 여는 물건으로 키웁니다. 사람을 늘리지 않고 닿는 곳을 넓히는 길입니다.")]
    inner = (_rows(rows, "grp")
             + '<div style="margin-top:26px">' + cards(items, "갈래", "three", icons=["bolt", "toolbox"]) + '</div>'
             + band('2025년에 AI를 다루는 프로젝트가 처음 들어왔고, 다음 걸음도 그 연장선에 있습니다. '
                    '<strong>AX 컨설팅에서 반복되는 일이 다음 제품의 재료가 됩니다.</strong>', top=26))
    return wide(n, P5, "연혁과 방향", '네 해가 쌓여 <span class="gt">다음 두 갈래</span>가 나왔습니다',
                "쌓인 네 해와 앞으로 갈 두 갈래",
                "연혁의 굵은 항목을 따라가면 흐름이 보입니다. 2025년의 AI 프로젝트 둘이 앞으로 갈 방향을 정했습니다.",
                inner, "")


def s_end(n):
    HEADERS[n] = "마무리"
    aur = '<i class="aur a2"></i><i class="aur a3"></i>'
    body = (f'{aur}<div class="fg">'
            '<h2>오픈소스마케팅이 남기는 것은<br><span class="gt">회사 안에 쌓이는 판단 근거</span>입니다</h2>'
            '<p class="endsub">오늘 본 정의서와 가이드, 검수 화면, 대시보드가 그 증거입니다. '
            '무엇을 셀지 정하고, 기록이 남게 만들고, 그 숫자로 마케팅을 고치는 일을 네 해 동안 반복했습니다.</p>'
            '<div class="endcontact"><span>contact@osoma.kr</span><span>osoma.kr</span></div>'
            '</div>')
    return ax(n, "ax-end", body, "OPEN SOURCE MARKETING")


# ══ 조립 ═══════════════════════════════════════════════════════════════

ORDER = [s_cover, s_toc,
         s_intro, s_problem, s_ground, s_did_what, s_value,
         s_did_steps, s_shot_spec, s_shot_guide, s_shot_debug, s_shot_dash,
         s_shot_bq, s_shot_handover, s_growth,
         s_kto_what, s_shot_slack, s_shot_bot, s_kto_rate, s_kto_report,
         s_ai_shift, s_ai_flow, s_ai_chat, s_ai_pipe, s_ai_sub,
         s_clients, s_hist_next, s_end]


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
<style>{CSS}{EXTRA_CSS}{SHOT_CSS}{DEEP_CSS}{ADD_CSS}{DECK_CSS}</style>
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
