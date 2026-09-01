"""덱 오른쪽 위 도구 모음. 유진투자증권 온보딩 덱(홈미니)의 도구를 이 덱 구조(section#a{n}, 1920×1080)에 맞춰 옮겼다.

- 발표자 보기: 보조 모니터용 창에 현재 장, 다음 장 미리보기, 시계와 경과 시간을 띄운다.
- 번호 이동: 장 번호를 넣고 Enter.
- PDF 내려받기: export_pdf.py 가 만든 파일을 받는다. 파일 이름은 PDF_NAME 하나로 맞춘다.
- 전체보기: 브라우저 전체 화면. 해제는 ESC. 전체 화면에서는 단추 다섯 개가 모두 사라진다.
- 편집: 화면 글을 그 자리에서 고치고 브라우저 저장소에 저장한다. 빌드로 구조가 바뀐 장은 복원하지 않는다.

도구를 빼려면 build_ax.py 에서 TOOLBAR_HTML 을 빈 문자열로 바꾼다.
"""

PDF_NAME = "쇼케이스_AX60.pdf"

TOOLBAR_HTML = r'''<!-- ============================================================
     TOOLBAR BLOCK — 도구 모음. 빼려면 build_ax.py 에서 TOOLBAR_HTML = '' 로 비운다.
============================================================ -->
<style id="ed-css">
#pv-btn,#pdf-btn,#fs-btn,#ed-btn,#go-box{position:fixed;top:18px;z-index:9999;font-family:inherit;
  font-size:15px;font-weight:700;letter-spacing:.04em;border-radius:6px;cursor:pointer;
  opacity:.85;transition:opacity .15s;box-shadow:0 2px 8px rgba(0,0,0,.12)}
#pv-btn:hover,#pdf-btn:hover,#fs-btn:hover,#ed-btn:hover,#go-box:hover,#go-box:focus-within{opacity:1}
#ed-btn{right:24px;background:#2B3040;color:#fff;border:none;padding:9px 20px;opacity:.8}
#fs-btn{right:112px;background:#368ECD;color:#fff;border:none;padding:9px 20px;opacity:.8}
#pdf-btn{right:216px;background:#fff;color:#2B3040;border:1.5px solid #C9D6E6;padding:8px 18px;text-decoration:none}
#go-box{right:360px;display:flex;align-items:center;gap:2px;background:#fff;border:1.5px solid #C9D6E6;padding:6px 12px;cursor:default}
#go-box input{width:40px;border:none;outline:none;font-family:inherit;font-size:15px;font-weight:700;color:#2B3040;
  text-align:right;font-variant-numeric:tabular-nums;-moz-appearance:textfield}
#go-box input::-webkit-outer-spin-button,#go-box input::-webkit-inner-spin-button{-webkit-appearance:none;margin:0}
#go-box .gt{font-size:15px;font-weight:700;color:#8C94A8;white-space:nowrap}
#pv-btn{right:478px;background:#fff;color:#2B3040;border:1.5px solid #C9D6E6;padding:8px 18px}
#ed-bar{position:fixed;top:14px;right:24px;z-index:9999;background:#1E2436;border-radius:8px;padding:7px 10px;
  display:none;gap:6px;align-items:center;box-shadow:0 4px 20px rgba(0,0,0,.22)}
#ed-bar button{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);color:#fff;border-radius:5px;
  padding:6px 13px;font-size:14px;font-weight:700;cursor:pointer;font-family:inherit;transition:background .12s;white-space:nowrap}
#ed-bar button:hover{background:rgba(255,255,255,.22)}
#ed-bar .ed-save{background:#368ECD;border-color:#2B7AB5}
#ed-bar .ed-save:hover{background:#2B7AB5}
#ed-bar .ed-sep{width:1px;height:22px;background:rgba(255,255,255,.18);margin:0 2px;flex-shrink:0}
[contenteditable="true"]{outline:none;cursor:text;border-radius:3px;transition:box-shadow .12s}
[contenteditable="true"]:hover{box-shadow:0 0 0 1.5px rgba(54,142,205,.4)}
[contenteditable="true"]:focus{box-shadow:0 0 0 2px #368ECD}
#ed-toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%);background:#1E2436;color:#fff;
  padding:9px 22px;border-radius:6px;font-size:15px;font-weight:700;opacity:0;transition:opacity .2s;
  pointer-events:none;z-index:9999;white-space:nowrap}
@media print{#pv-btn,#pdf-btn,#fs-btn,#ed-btn,#go-box,#ed-bar,#ed-toast{display:none !important}}
</style>
<button id="pv-btn" onclick="pvOpen()">발표자 보기</button>
<div id="go-box" title="슬라이드 번호를 입력하고 Enter">
  <input id="go-in" type="number" min="1" placeholder="번호" aria-label="슬라이드 번호로 이동">
  <span class="gt" id="go-total"></span>
</div>
<a id="pdf-btn" href="__PDF_NAME__" download>PDF 내려받기</a>
<button id="fs-btn" onclick="fsEnter()">전체보기</button>
<button id="ed-btn" onclick="edToggle()">편집</button>
<div id="ed-bar">
  <button onmousedown="event.preventDefault()" onclick="edSize(-2)">A−</button>
  <button onmousedown="event.preventDefault()" onclick="edSize(+2)">A+</button>
  <div class="ed-sep"></div>
  <button class="ed-save" onclick="edSave()">저장</button>
  <button onclick="edExport()">내보내기</button>
  <button onclick="edRestore()">되돌리기</button>
  <button onclick="edClear()">저장 비우기</button>
  <button onclick="edToggle()">닫기</button>
</div>
<div id="ed-toast"></div>
<script id="ed-js">
(function(){
  // 저장 키에 장 수를 넣어, 장 수가 다른 빌드의 저장본이 엉뚱한 자리에 들어가지 않게 한다.
  // 구성과 본문이 크게 바뀐 빌드는 이전 장의 저장본을 복원하지 않는다.
  var STORE='osoma-slide-edits:v1:'+document.querySelectorAll('section.slide').length;
  var SEL='.kicker,h1,h2.head,h2.big,.lead,.sub,.mchips span'
    +',.pt h4,.pt p,.axstep b,.axstep h4,.axstep p'
    +',.paper .ptag,.paper li,.paper .prole,.axband,.rcap'
    +',.hf span,.hf b,.hf p,.vs .vh,.vc h4,.vc p'
    +',.qlabel,.qq,.qa,.figrow b,.figrow span,.embnote'
    +',.stepn h4,.stepn p,.bfl,.tool h4,.tool p,.dkrow h4,.dkrow p,.crow h4,.crow p'
    +',.askcol h4,.aq h4,.aq p,.impband,.tbody,.hbar span,.hrow .hl'
    +',.tocol h3,.tocol li,.qcell .qh,.qcell .qs,.qcell div';

  function restore(){
    try{
      var d=JSON.parse(localStorage.getItem(STORE)||'null');
      if(!d) return false;
      document.querySelectorAll('section.slide').forEach(function(sec){
        var els=sec.querySelectorAll(SEL);
        // 저장 시점과 편집 대상 개수가 다르면 그 장은 건너뛴다. 빌드로 구조가 바뀌면 자리가 밀린다.
        if(d[sec.id+':n']!==els.length) return;
        els.forEach(function(el,i){
          var v=d[sec.id+':'+i];
          if(v){el.innerHTML=v.h; if(v.f) el.style.fontSize=v.f;}
        });
      });
      return true;
    }catch(e){return false;}
  }
  // 복원하기 전에 빌드가 만든 원본을 담아 둔다. 내보내기가 이 값과 견줘 고친 곳만 추린다.
  var ORIG={};
  document.querySelectorAll('section.slide').forEach(function(sec){
    sec.querySelectorAll(SEL).forEach(function(el,i){ ORIG[sec.id+':'+i]=el.innerHTML; });
  });
  restore();

  var on=false;
  function syncFsBtn(){
    // 편집 바가 열려 있거나 전체보기 중이면 버튼을 숨긴다. 전체보기 해제는 ESC로만.
    var hide=(on||document.fullscreenElement)?'none':'';
    document.getElementById('ed-btn').style.display=hide;
    document.getElementById('fs-btn').style.display=hide;
    document.getElementById('pdf-btn').style.display=hide;
    document.getElementById('go-box').style.display=hide?'none':'flex';
    document.getElementById('pv-btn').style.display=hide;
  }

  // 번호로 이동
  (function(){
    var total=document.querySelectorAll('section.slide').length;
    var inp=document.getElementById('go-in');
    document.getElementById('go-total').textContent='/ '+total;
    inp.setAttribute('max',total);
    inp.addEventListener('keydown',function(e){
      if(e.key!=='Enter') return;
      var n=parseInt(inp.value,10);
      if(!n) return;
      n=Math.max(1,Math.min(total,n));
      var t=document.getElementById('a'+n);
      if(t){t.scrollIntoView();inp.value='';inp.blur();}
    });
  })();

  // 발표자 보기. 미리보기는 덱 CSS와 해당 장만 담은 1920×1080 iframe(srcdoc)이다.
  (function(){
    var pvWin=null,pvCur=1,pvTimer=null,pvT0=null;
    var secs=document.querySelectorAll('section.slide');
    var total=secs.length;
    var FONTS='';
    document.querySelectorAll('head link[rel="stylesheet"]').forEach(function(l){FONTS+=l.outerHTML;});
    var DEFS=(function(){var d=document.querySelector('body > svg[aria-hidden]');return d?d.outerHTML:'';})();
    var deckCSS=null;
    function css(){
      if(deckCSS===null){
        var st=document.querySelector('head style:not(#ed-css)');
        deckCSS=st?st.textContent:'';
      }
      return deckCSS;
    }
    function srcdoc(n){
      var sec=document.getElementById('a'+n);
      if(!sec)return '<!doctype html><body style="background:#1E2436">';
      return '<!doctype html><html lang="ko"><head><meta charset="utf-8">'+FONTS
        +'<style>'+css()
        +' html,body{overflow:hidden;scroll-snap-type:none;background:#fff}'
        +' section.slide{transform:none}'
        +' #ed-btn,#fs-btn,#pdf-btn,#go-box,#pv-btn{display:none}'
        +'</style></head><body>'+DEFS+sec.outerHTML+'</body></html>';
    }
    function fit(){
      if(!pvWin||pvWin.closed)return;
      try{
        ['cur','nxt'].forEach(function(k){
          var box=pvWin.document.getElementById('pv-'+k+'-box');
          var fr=pvWin.document.getElementById('pv-'+k);
          if(!box||!fr)return;
          var sc=Math.min(box.clientWidth/1920,box.clientHeight/1080);
          fr.style.transform='scale('+sc+')';
          fr.style.left=((box.clientWidth-1920*sc)/2)+'px';
          fr.style.top=((box.clientHeight-1080*sc)/2)+'px';
        });
      }catch(e){}
    }
    function sync(){
      if(!pvWin||pvWin.closed)return;
      try{
        var d=pvWin.document;
        d.getElementById('pv-cur').srcdoc=srcdoc(pvCur);
        var last=(pvCur>=total);
        d.getElementById('pv-nxt').srcdoc=last
          ?'<!doctype html><body style="background:#12152C;color:#5E6890;display:flex;align-items:center;justify-content:center;font-family:sans-serif;font-size:40px;margin:0">마지막 장입니다</body>'
          :srcdoc(pvCur+1);
        d.getElementById('pv-no').textContent=pvCur+' / '+total;
        d.getElementById('pv-nxno').textContent=last?'끝':'다음: '+(pvCur+1)+'장';
        fit();
      }catch(e){}
    }
    function tick(){
      if(!pvWin||pvWin.closed){clearInterval(pvTimer);pvTimer=null;return;}
      try{
        var d=pvWin.document,now=new Date();
        d.getElementById('pv-clock').textContent=
          ('0'+now.getHours()).slice(-2)+':'+('0'+now.getMinutes()).slice(-2)+':'+('0'+now.getSeconds()).slice(-2);
        var el=Math.floor((now-pvT0)/1000);
        d.getElementById('pv-elapsed').textContent=Math.floor(el/60)+'분 '+('0'+el%60).slice(-2)+'초';
      }catch(e){}
    }
    window.pvNav=function(d){
      var n=Math.max(1,Math.min(total,pvCur+d));
      var t=document.getElementById('a'+n);
      if(t)t.scrollIntoView();
    };
    window.pvOpen=function(){
      if(pvWin&&!pvWin.closed){pvWin.focus();return;}
      pvWin=window.open('','axpv','width=1280,height=780');
      if(!pvWin){alert('팝업이 차단되었습니다. 이 사이트의 팝업을 허용해 주세요.');return;}
      pvT0=new Date();
      var d=pvWin.document;
      d.open();
      d.write('<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>발표자 보기 : AX 쇼케이스</title>'+FONTS
        +'<style>'
        +'*{box-sizing:border-box}body{margin:0;background:#1E2436;color:#E8ECF4;'
        +'font-family:"Pretendard Variable",Pretendard,sans-serif;height:100vh;display:flex;flex-direction:column;overflow:hidden}'
        +'.top{flex:0 0 auto;display:flex;align-items:center;gap:14px;padding:10px 18px;border-bottom:1px solid rgba(255,255,255,.1)}'
        +'.top .tt{font-size:14px;font-weight:800;letter-spacing:.06em;color:#AFB8CC}'
        +'.top .hint{font-size:12.5px;color:#5E6890}'
        +'.top .sp{flex:1}'
        +'.top button{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.22);color:#fff;'
        +'border-radius:6px;padding:6px 16px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit}'
        +'.main{flex:1;display:flex;gap:14px;padding:14px;min-height:0}'
        +'.cur{flex:1.6;display:flex;flex-direction:column;min-width:0}'
        +'.side{flex:1;display:flex;flex-direction:column;gap:14px;min-width:0}'
        +'.lab{font-size:13px;font-weight:800;color:#8C97AF;letter-spacing:.06em;margin-bottom:6px}'
        +'.box{position:relative;flex:1;background:#12152C;border-radius:10px;overflow:hidden;min-height:0}'
        +'.box iframe{position:absolute;width:1920px;height:1080px;border:none;transform-origin:top left;background:#fff;pointer-events:none}'
        +'.meta{flex:0 0 auto;display:flex;gap:22px;background:#12152C;border-radius:10px;padding:14px 20px;align-items:center}'
        +'.meta .k{font-size:11.5px;font-weight:800;color:#5E6890;letter-spacing:.06em}'
        +'.meta .v{font-size:26px;font-weight:900;font-variant-numeric:tabular-nums;margin-top:2px}'
        +'.meta .v.small{font-size:19px}'
        +'</style></head><body>'
        +'<div class="top"><span class="tt">발표자 보기</span>'
        +'<span class="hint">이 창을 보조 모니터로 옮기세요. ←/→ 키로 장을 넘길 수 있습니다.</span>'
        +'<span class="sp"></span><button id="pv-prev">← 이전</button><button id="pv-next">다음 →</button></div>'
        +'<div class="main">'
        +'<div class="cur"><div class="lab" id="pv-no">1 / '+total+'</div><div class="box" id="pv-cur-box"><iframe id="pv-cur"></iframe></div></div>'
        +'<div class="side">'
        +'<div style="flex:1.2;display:flex;flex-direction:column;min-height:0"><div class="lab" id="pv-nxno">다음: 2장</div>'
        +'<div class="box" id="pv-nxt-box"><iframe id="pv-nxt"></iframe></div></div>'
        +'<div class="meta"><span><span class="k">현재 시각</span><div class="v" id="pv-clock">--:--:--</div></span>'
        +'<span><span class="k">경과</span><div class="v small" id="pv-elapsed">0분 00초</div></span></div>'
        +'</div></div></body></html>');
      d.close();
      d.getElementById('pv-prev').addEventListener('click',function(){window.pvNav(-1);});
      d.getElementById('pv-next').addEventListener('click',function(){window.pvNav(1);});
      d.addEventListener('keydown',function(e){
        if(e.key==='ArrowRight'||e.key===' '||e.key==='PageDown')window.pvNav(1);
        if(e.key==='ArrowLeft'||e.key==='PageUp')window.pvNav(-1);
      });
      pvWin.addEventListener('resize',fit);
      if(pvTimer)clearInterval(pvTimer);
      pvTimer=setInterval(tick,500);
      sync();
    };
    // 화면의 60% 이상을 차지한 장을 현재 장으로 본다
    var io=new IntersectionObserver(function(es){
      es.forEach(function(en){
        if(en.intersectionRatio>=.6){
          var n=parseInt(en.target.id.slice(1),10);
          if(n&&n!==pvCur){pvCur=n;sync();}
        }
      });
    },{threshold:[.6]});
    secs.forEach(function(sec){io.observe(sec);});
    window.addEventListener('beforeunload',function(){
      if(pvWin&&!pvWin.closed)pvWin.close();
    });
  })();

  window.edToggle=function(){
    on=!on;
    document.getElementById('ed-btn').style.display=on?'none':'';
    document.getElementById('ed-bar').style.display=on?'flex':'none';
    syncFsBtn();
    document.querySelectorAll(SEL).forEach(function(el){
      el.contentEditable=on?'true':'false';
    });
  };

  window.fsEnter=function(){
    var el=document.documentElement;
    var req=el.requestFullscreen||el.webkitRequestFullscreen;
    if(!req) return;
    var p=req.call(el,{navigationUI:'hide'});
    if(p&&p.catch) p.catch(function(){});
  };
  ['fullscreenchange','webkitfullscreenchange'].forEach(function(ev){
    document.addEventListener(ev,syncFsBtn);
  });

  window.edSize=function(delta){
    var sel=window.getSelection();
    if(!sel||!sel.rangeCount) return;
    if(!sel.isCollapsed){
      var range=sel.getRangeAt(0);
      var anc=range.commonAncestorContainer;
      var refEl=anc.nodeType===3?anc.parentElement:anc;
      var existingSpan=null;
      if(refEl.tagName==='SPAN'&&refEl.style.fontSize) existingSpan=refEl;
      else if(refEl.childNodes.length===1&&refEl.firstChild.nodeType!==3
              &&refEl.firstChild.tagName==='SPAN'&&refEl.firstChild.style.fontSize)
        existingSpan=refEl.firstChild;
      if(existingSpan){
        var ec=parseFloat(existingSpan.style.fontSize)||parseFloat(getComputedStyle(existingSpan).fontSize)||24;
        existingSpan.style.fontSize=Math.max(10,ec+delta)+'px';
        var nr=document.createRange();
        nr.selectNodeContents(existingSpan);
        sel.removeAllRanges(); sel.addRange(nr);
        return;
      }
      var cur=parseFloat(getComputedStyle(refEl).fontSize)||24;
      var sp=document.createElement('span');
      sp.style.fontSize=Math.max(10,cur+delta)+'px';
      try{
        sp.appendChild(range.extractContents());
        range.insertNode(sp);
        var nr2=document.createRange();
        nr2.selectNodeContents(sp);
        sel.removeAllRanges(); sel.addRange(nr2);
      }catch(e){}
    }else{
      var node=sel.anchorNode;
      var el=node&&(node.nodeType===3?node.parentElement:node);
      var target=el&&el.closest('[contenteditable="true"]');
      if(target){
        var c=parseFloat(target.style.fontSize)||parseFloat(getComputedStyle(target).fontSize)||24;
        target.style.fontSize=Math.max(10,c+delta)+'px';
      }
    }
  };

  window.edSave=function(){
    var out={};
    document.querySelectorAll('section.slide').forEach(function(sec){
      var els=sec.querySelectorAll(SEL);
      out[sec.id+':n']=els.length;
      els.forEach(function(el,i){
        out[sec.id+':'+i]={h:el.innerHTML,f:el.style.fontSize||''};
      });
    });
    localStorage.setItem(STORE,JSON.stringify(out));
    toast('저장됨 ✓');
  };

  window.edExport=function(){
    // 빌드 원본과 다른 곳만 모은다. 이 파일을 apply_edits.py 가 본문_AX60.md 에 되박는다.
    var txt=function(h){var d=document.createElement('div');d.innerHTML=h;
      return (d.textContent||'').replace(/\u00a0/g,' ').replace(/\s+/g,' ').trim()};
    var rows=[];
    document.querySelectorAll('section.slide').forEach(function(sec){
      sec.querySelectorAll(SEL).forEach(function(el,i){
        var a=txt(ORIG[sec.id+':'+i]||''), b=txt(el.innerHTML);
        if(a!==b&&b) rows.push({slide:sec.id,i:i,from:a,to:b});
      });
    });
    if(!rows.length){toast('고친 곳이 없습니다');return;}
    var blob=new Blob([JSON.stringify(rows,null,1)],{type:'application/json'});
    var a=document.createElement('a');
    a.href=URL.createObjectURL(blob); a.download='편집본_소개.json';
    document.body.appendChild(a); a.click(); a.remove();
    toast(rows.length+'곳 내보냈습니다');
  };

  window.edClear=function(){
    // 고친 글을 본문 파일로 옮긴 뒤에는 저장본을 비워야 새 빌드가 그대로 보인다.
    if(!confirm('브라우저에 저장된 편집을 지우고 빌드한 글로 되돌립니다. 계속할까요?')) return;
    localStorage.removeItem(STORE); location.reload();
  };

  window.edRestore=function(){
    if(restore()) toast('복원됨');
    else toast('저장된 내용이 없습니다');
  };

  function toast(msg){
    var t=document.getElementById('ed-toast');
    t.textContent=msg; t.style.opacity='1';
    clearTimeout(t._t);
    t._t=setTimeout(function(){t.style.opacity='0';},1600);
  }
})();
</script>
<!-- ============================================================ /TOOLBAR -->'''.replace("__PDF_NAME__", PDF_NAME)
