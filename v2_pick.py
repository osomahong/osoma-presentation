"""후보를 고르고 그 기록을 남기는 층.

비교 화면에서 장마다 안 하나를 고르면 브라우저에 저장되고, 새로 열어도 그대로 남습니다.
기록은 파일로 내려받아 옮기거나 다시 불러올 수 있고, 표로 복사해 문서에 붙일 수 있습니다.

- 카드마다 고르기 단추가 붙습니다. 한 장에 하나만 고를 수 있고, 다시 누르면 풀립니다
- 고른 장에는 메모 칸이 열립니다. 고른 이유나 준비할 것을 적어 둡니다
- 위쪽 막대에 지금까지 몇 장을 정했는지 나옵니다
- 고른 안 보기를 누르면 52장 전체가 표로 나옵니다

기록은 `merryyear-ax-picks-v1` 열쇠로 브라우저에 담깁니다. 브라우저를 지우면 함께 지워지므로,
정한 뒤에는 파일로 내려받아 둡니다.
"""

PICK_CSS = """
/* ══ 고르고 기록하기 ═══════════════════════════════════════════════
   고른 안은 테두리와 표로 드러내고, 아직 정하지 않은 장은 차례에서 옅게 둔다.
   ═══════════════════════════════════════════════════════════════ */
.cmpnav .in{align-items:center}
.navnums{display:flex;flex-wrap:wrap;gap:7px;flex:1;min-width:0}
.navact{display:flex;align-items:center;gap:10px;flex:none;padding-left:22px}
.navcount{font-family:var(--fm);font-size:14px;font-weight:700;letter-spacing:.1em;color:var(--faint);
  white-space:nowrap}
.navcount b{color:#7A4FBE;font-size:17px}
.navbtn{border:1.5px solid #E4E7EF;background:#fff;border-radius:10px;padding:8px 15px;
  font-family:var(--f);font-size:14.5px;font-weight:700;color:var(--dim);cursor:pointer;white-space:nowrap}
.navbtn:hover{border-color:#C6CBDA;color:var(--ink)}
.navbtn.on{background:var(--grad);border-color:transparent;color:#fff}
.cmpnav a.done{background:linear-gradient(135deg,#FFF1E6,#F6ECFD);border-color:transparent;color:#7A4FBE}
/* 한 문장이라 넓은 자간의 고정폭 글꼴이 읽기 나쁘다 */
.cmptot{font-family:var(--f);letter-spacing:0;font-size:16.5px;font-weight:700}

/* 현재 판을 그대로 두는 안까지 넷이 되면 한 줄에 넷을 놓는다 */
.row.four{grid-template-columns:repeat(4,1fr);gap:22px}
.row.four .cmpcard figcaption{padding:18px 20px 22px}
.row.four .cmpcard .cl{gap:9px;margin-bottom:8px}
.row.four .cmpcard .cl b{font-size:13px;letter-spacing:.12em}
.row.four .cmpcard .cl span{font-size:15px;padding:4px 11px}
.row.four .cmpcard figcaption p{font-size:15.5px;line-height:1.55}
.row.four .pickbtn{padding:11px 12px;font-size:15px}
.cmpcard.keep .cl span{background:#EEF0F6;color:var(--faint)}

/* 카드 높이를 맞춰 정하기 단추가 한 줄에 서게 한다 */
.row{align-items:stretch}
.cmpcard{display:flex;flex-direction:column}
.cmpcard figcaption{flex:1;display:flex;flex-direction:column}
.cmpcard figcaption p{margin-bottom:16px}

/* 고르기 단추 */
.pickbtn{margin-top:auto;width:100%;border:1.5px solid #E4E7EF;background:#fff;border-radius:12px;
  padding:12px 16px;font-family:var(--f);font-size:16px;font-weight:700;color:var(--dim);cursor:pointer;
  display:flex;align-items:center;justify-content:center;gap:9px;transition:border-color .12s}
.pickbtn:hover{border-color:#C6CBDA;color:var(--ink)}
.pickbtn i{display:block;width:18px;height:18px;border-radius:50%;border:2px solid #C6CBDA;flex:none}
.cmpcard.picked{border-color:transparent;box-shadow:0 0 0 2.5px #A855F7,0 16px 40px rgba(120,80,200,.18)}
.cmpcard.picked .pickbtn{background:var(--grad);border-color:transparent;color:#fff}
.cmpcard.picked .pickbtn i{border-color:#fff;background:#fff;position:relative}
.cmpcard.picked .pickbtn i::after{content:"";position:absolute;left:5px;top:2px;width:5px;height:9px;
  border:solid #A855F7;border-width:0 2.5px 2.5px 0;transform:rotate(42deg)}

/* 장 제목 옆의 고른 표시 */
.grpick{display:none;margin-left:14px;font-family:var(--f);font-size:16px;font-weight:800;
  padding:5px 14px;border-radius:999px;background:linear-gradient(135deg,#FFF1E6,#F6ECFD);color:#7A4FBE;
  vertical-align:middle}
.grp.has .grpick{display:inline-block}

/* 메모 칸 */
.memorow{display:none;margin-top:18px}
.grp.has .memorow{display:block}
.memorow input{width:100%;max-width:1080px;border:1.5px solid #E4E7EF;border-radius:12px;
  padding:13px 18px;font-family:var(--f);font-size:16.5px;color:var(--ink);background:#fff}
.memorow input::placeholder{color:#C6CBDA}
.memorow input:focus{outline:none;border-color:#A855F7}

/* 고른 안 보기 */
.sum{position:fixed;inset:0;z-index:95;background:rgba(24,28,40,.6);display:none;
  align-items:center;justify-content:center;padding:44px}
.sum.on{display:flex}
.sumbox{background:#fff;border-radius:22px;width:100%;max-width:1180px;max-height:100%;
  display:flex;flex-direction:column;overflow:hidden;box-shadow:0 30px 90px rgba(0,0,0,.3)}
.sumhd{padding:30px 36px 22px;border-bottom:1.5px solid #ECEEF4;flex:none}
.sumhd h2{font-size:27px;font-weight:800;letter-spacing:-.02em}
.sumhd p{margin-top:9px;font-size:17px;line-height:1.6;color:var(--dim)}
.sumbody{overflow:auto;padding:6px 36px 10px;flex:1;min-height:0}
.sumbody table{width:100%;border-collapse:collapse}
.sumbody th,.sumbody td{padding:12px 10px;text-align:left;border-bottom:1.5px solid #F0F2F7;
  font-size:16px;line-height:1.45;vertical-align:top}
.sumbody th{position:sticky;top:0;background:#fff;font-family:var(--fm);font-size:13.5px;
  font-weight:700;letter-spacing:.12em;color:var(--faint);z-index:1}
.sumbody td.n{font-family:var(--fm);font-weight:700;color:var(--faint);width:52px}
.sumbody td.t{font-weight:700}
.sumbody td.k{width:74px;font-weight:800;color:#7A4FBE}
.sumbody td.m{color:var(--dim);width:28%}
.sumbody tr.none td{color:#C6CBDA}
.sumbody tr.none td.t{font-weight:500}
.sumft{padding:20px 36px 26px;border-top:1.5px solid #ECEEF4;display:flex;gap:10px;flex:none;
  flex-wrap:wrap;align-items:center}
.sumft .grow{flex:1}
.sumft button{border:1.5px solid #E4E7EF;background:#fff;border-radius:11px;padding:11px 18px;
  font-family:var(--f);font-size:15.5px;font-weight:700;color:var(--dim);cursor:pointer}
.sumft button:hover{border-color:#C6CBDA;color:var(--ink)}
.sumft button.pri{background:var(--grad);border-color:transparent;color:#fff}
.sumft button.warn:hover{border-color:#FF9BB0;color:#C2185B}

/* 알림 */
.toast{position:fixed;left:50%;bottom:38px;transform:translateX(-50%) translateY(20px);z-index:99;
  background:rgba(24,28,40,.94);color:#fff;border-radius:999px;padding:14px 26px;
  font-family:var(--f);font-size:16px;font-weight:700;opacity:0;pointer-events:none;
  transition:opacity .18s,transform .18s}
.toast.on{opacity:1;transform:translateX(-50%) translateY(0)}
"""


def pick_bar():
    """위쪽 차례 막대 오른쪽에 붙는 단추와 진행 수."""
    return ('<div class="navact">'
            '<span class="navcount"><b>0</b> / 52 정함</span>'
            '<button class="navbtn" type="button" data-act="summary">고른 안 보기</button>'
            '<button class="navbtn" type="button" data-act="export">내려받기</button>'
            '<button class="navbtn" type="button" data-act="import">불러오기</button>'
            '<input type="file" accept=".json,application/json" hidden data-act="file">'
            '</div>')


def pick_button(n, label, kind):
    """카드 아래에 붙는 고르기 단추."""
    return (f'<button class="pickbtn" type="button" data-n="{n:02d}" data-k="{label}" '
            f'data-kind="{kind}"><i></i><span>이 안으로 정하기</span></button>')


def pick_memo(n):
    """고른 장에만 열리는 메모 칸."""
    return (f'<div class="memorow"><input type="text" data-memo="{n:02d}" '
            f'placeholder="고른 이유나 준비할 것을 적어 둡니다"></div>')


def pick_panel():
    """고른 안을 표로 보여 주는 화면."""
    return ('<div class="sum"><div class="sumbox">'
            '<div class="sumhd"><h2>고른 시각 안</h2>'
            '<p class="sumnote"></p></div>'
            '<div class="sumbody"><table><thead><tr>'
            '<th>장</th><th>제목</th><th>안</th><th>재료</th><th>메모</th>'
            '</tr></thead><tbody></tbody></table></div>'
            '<div class="sumft">'
            '<button class="pri" type="button" data-act="copymd">표로 복사</button>'
            '<button type="button" data-act="export">파일로 내려받기</button>'
            '<button type="button" data-act="import">파일에서 불러오기</button>'
            '<span class="grow"></span>'
            '<button class="warn" type="button" data-act="clear">전부 지우기</button>'
            '<button type="button" data-act="close">닫기</button>'
            '</div></div></div>'
            '<div class="toast"></div>')


PICK_JS = """
<script>
/* 고른 안을 기록한다. 브라우저에 담고, 파일로 옮길 수 있게 한다. */
(function(){
  var KEY = 'merryyear-ax-picks-v1';
  var KEEP = '그대로';          /* 현재 판을 그대로 두는 안의 표시 */
  var state = {};

  var can = (function(){
    try { localStorage.setItem(KEY + '-t', '1'); localStorage.removeItem(KEY + '-t'); return true; }
    catch (e) { return false; }
  })();

  function load(){
    if (!can) return {};
    try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { return {}; }
  }
  function save(){
    if (!can) return;
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
  }

  var toastEl = document.querySelector('.toast'), toastT = null;
  function toast(msg){
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.classList.add('on');
    clearTimeout(toastT); toastT = setTimeout(function(){ toastEl.classList.remove('on'); }, 2200);
  }

  function pad(n){ return ('0' + n).slice(-2); }

  /* 장 번호별 제목. 차례를 만들 때 한 번만 읽는다 */
  var titles = {};
  [].forEach.call(document.querySelectorAll('.grp'), function(g){
    var n = g.id.replace('s', '');
    var h = g.querySelector('h2');
    var em = h.querySelector('em');
    titles[n] = h.textContent.replace(em ? em.textContent : '', '').trim();
  });

  function render(){
    var done = 0;
    [].forEach.call(document.querySelectorAll('.grp'), function(g){
      var n = g.id.replace('s', ''), cur = state[n];
      g.classList.toggle('has', !!cur);
      var badge = g.querySelector('.grpick');
      if (badge) badge.textContent = cur ? (cur.k === KEEP ? '현재 상태 유지'
                                                          : '고른 안 ' + cur.k + ' ' + cur.kind) : '';
      [].forEach.call(g.querySelectorAll('.pickbtn'), function(b){
        var on = !!cur && cur.k === b.getAttribute('data-k');
        b.closest('.cmpcard').classList.toggle('picked', on);
        b.querySelector('span').textContent = on ? '정한 안' : '이 안으로 정하기';
      });
      var memo = g.querySelector('[data-memo]');
      if (memo && document.activeElement !== memo) memo.value = (cur && cur.memo) || '';
      if (cur) done++;
    });
    [].forEach.call(document.querySelectorAll('.cmpnav a'), function(a){
      a.classList.toggle('done', !!state[a.getAttribute('href').replace('#s', '')]);
    });
    var c = document.querySelector('.navcount b');
    if (c) c.textContent = done;
    return done;
  }

  /* 카드의 고르기 단추. 같은 안을 다시 누르면 풀린다 */
  document.addEventListener('click', function(e){
    var b = e.target.closest('.pickbtn');
    if (!b) return;
    var n = b.getAttribute('data-n'), k = b.getAttribute('data-k');
    if (state[n] && state[n].k === k) delete state[n];
    else state[n] = {k: k, kind: b.getAttribute('data-kind'), memo: (state[n] || {}).memo || ''};
    save(); render();
    if (!can) toast('브라우저에 담지 못했습니다. 내려받기로 남겨 두시기 바랍니다');
  });

  document.addEventListener('input', function(e){
    var m = e.target.closest('[data-memo]');
    if (!m) return;
    var n = m.getAttribute('data-memo');
    if (!state[n]) return;
    state[n].memo = m.value; save();
  });

  /* 고른 안 보기 */
  var sum = document.querySelector('.sum');
  function openSum(){
    var body = sum.querySelector('tbody'), rows = [], done = 0;
    Object.keys(titles).sort().forEach(function(n){
      var cur = state[n];
      if (cur) done++;
      rows.push('<tr class="' + (cur ? '' : 'none') + '">' +
        '<td class="n">' + n + '</td>' +
        '<td class="t">' + titles[n] + '</td>' +
        '<td class="k">' + (cur ? (cur.k === KEEP ? '유지' : cur.k) : '') + '</td>' +
        '<td>' + (cur ? (cur.k === KEEP ? '현재 상태 유지' : cur.kind)
                      : '아직 정하지 않았습니다') + '</td>' +
        '<td class="m">' + ((cur && cur.memo) || '') + '</td></tr>');
    });
    body.innerHTML = rows.join('');
    sum.querySelector('.sumnote').textContent =
      Object.keys(titles).length + '장 가운데 ' + done + '장을 정했습니다.' +
      (can ? ' 기록은 이 브라우저에 남습니다.'
           : ' 이 브라우저에는 담기지 않으니 파일로 내려받아 두시기 바랍니다.');
    sum.classList.add('on');
  }

  function markdown(){
    var done = 0, lines = [];
    var keys = Object.keys(titles).sort();
    keys.forEach(function(n){ if (state[n]) done++; });
    lines.push('# 고른 시각 안', '');
    lines.push(keys.length + '장 가운데 ' + done + '장을 정했습니다.', '');
    lines.push('| 장 | 제목 | 안 | 재료 | 메모 |');
    lines.push('|---|---|---|---|---|');
    keys.forEach(function(n){
      var c = state[n];
      if (!c) return;
      lines.push('| ' + n + ' | ' + titles[n] + ' | ' + (c.k === KEEP ? '유지' : c.k) +
                 ' | ' + (c.k === KEEP ? '현재 상태 유지' : c.kind) +
                 ' | ' + (c.memo || '') + ' |');
    });
    var left = keys.filter(function(n){ return !state[n]; });
    if (left.length) {
      lines.push('', '## 아직 정하지 않은 장', '', left.join(', '));
    }
    return lines.join('\\n');
  }

  function copy(text, msg){
    var done = function(){ toast(msg); };
    var fb = function(){
      var a = document.createElement('textarea');
      a.value = text; a.style.position = 'fixed'; a.style.top = '0'; a.style.opacity = 0;
      document.body.appendChild(a); a.focus(); a.select();
      try { document.execCommand('copy'); } catch (err) {}
      a.remove(); done();
    };
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fb);
    else fb();
  }

  function download(){
    var keys = Object.keys(state);
    if (!keys.length) { toast('아직 정한 장이 없습니다'); return; }
    var data = {version: 1, picks: state};
    var blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = '고른시각안.json';
    document.body.appendChild(a); a.click();
    setTimeout(function(){ URL.revokeObjectURL(a.href); a.remove(); }, 500);
    toast(keys.length + '장의 기록을 내려받았습니다');
  }

  var fileIn = document.querySelector('[data-act="file"]');
  fileIn.addEventListener('change', function(){
    var f = fileIn.files && fileIn.files[0];
    if (!f) return;
    var r = new FileReader();
    r.onload = function(){
      try {
        var d = JSON.parse(r.result);
        var picks = d && d.picks ? d.picks : d;
        if (!picks || typeof picks !== 'object') throw 0;
        state = picks; save();
        var n = render();
        if (sum.classList.contains('on')) openSum();
        toast(n + '장의 기록을 불러왔습니다');
      } catch (e) { toast('읽을 수 없는 파일입니다'); }
    };
    r.readAsText(f);
    fileIn.value = '';
  });

  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-act]');
    if (!b || b === fileIn) return;
    var act = b.getAttribute('data-act');
    if (act === 'summary') openSum();
    else if (act === 'close') sum.classList.remove('on');
    else if (act === 'export') download();
    else if (act === 'import') fileIn.click();
    else if (act === 'copymd') copy(markdown(), '표를 복사했습니다');
    else if (act === 'clear') {
      if (!Object.keys(state).length) { toast('아직 정한 장이 없습니다'); return; }
      if (!confirm('정한 안을 전부 지웁니다. 되돌릴 수 없습니다.')) return;
      state = {}; save(); render(); openSum(); toast('기록을 지웠습니다');
    }
  });

  sum.addEventListener('click', function(e){ if (e.target === sum) sum.classList.remove('on'); });
  addEventListener('keydown', function(e){
    if (e.key === 'Escape' && sum.classList.contains('on')) sum.classList.remove('on');
  });

  state = load();
  render();
})();
</script>
"""
