"""Reading page for a harness: the paper in reading order, large type, comments to the clipboard.

Called by `cards.py read`. One static HTML file; MathJax renders the TeX. The author
selects text, attaches a comment, and copies all comments (with card ids and the
quoted text) to paste back to the agent. Comments live only in this browser tab.
"""
import html as _html
import json
import re

LABELS = {'ja': {'toc': '目次', 'smaller': '文字を小さく', 'larger': '文字を大きく', 'narrower': '行を短く', 'wider': '行を長く', 'theme': '明暗', 'comments': 'コメント', 'copy': 'クリップボードにコピー', 'copied': 'コピーしました', 'add': 'コメントする', 'placeholder': 'コメント', 'save': '追加', 'cancel': '取り消し', 'none': 'コメントはまだありません．本文を選ぶとボタンが出ます．', 'delete': '削除', 'clear': '全部消す', 'close': '閉じる', 'confirm': 'コメントを全部消しますか？', 'nocomment': '(コメントなし)', 'proof': '証明', 'appendix': '付録'},
          'en': {'toc': 'Contents', 'smaller': 'Smaller text', 'larger': 'Larger text', 'narrower': 'Shorter lines', 'wider': 'Longer lines', 'theme': 'Light/dark', 'comments': 'Comments', 'copy': 'Copy to clipboard', 'copied': 'Copied', 'add': 'Comment', 'placeholder': 'Comment', 'save': 'Add', 'cancel': 'Cancel', 'none': 'No comments yet. Select text to add one.', 'delete': 'Delete', 'clear': 'Clear all', 'close': 'Close', 'confirm': 'Delete all comments?', 'nocomment': '(no comment)', 'proof': 'Proof', 'appendix': 'Appendix'}}

KIND_NAMES = {'definition': 'Definition', 'theorem': 'Theorem', 'proposition': 'Proposition',
              'lemma': 'Lemma', 'corollary': 'Corollary'}


def numbering(cards, items, fact_kinds):
    """Paper numbers: section.counter with one shared counter per section, A.n in the appendix."""
    num, sec_no, count, last = {}, 0, 0, object()
    for si, _, cid, _ in items:
        if cid not in cards:
            continue
        if si != last:
            last = si
            count = 0
            if si is not None:
                sec_no = si + 1
        if cards[cid].kind in fact_kinds:
            count += 1
            num[cid] = f'{"A" if si is None else sec_no}.{count}'
    return num


def tex_to_html(text, cards, num, label_to_id, card_label):
    t = _html.escape(text.strip(), quote=False)
    t = re.sub(r'\\paragraph\{([^{}]*)\}', r'<strong class="para">\1</strong>', t)
    t = re.sub(r'\\emph\{([^{}]*)\}', r'<em>\1</em>', t)
    t = re.sub(r'\\textbf\{([^{}]*)\}', r'<strong>\1</strong>', t)

    def ref(m):
        lab = m.group(1)
        cid = label_to_id.get(lab) or (lab if lab in cards else None)
        if cid and cid in num:
            return f'<a class="ref" href="#{cid}">{KIND_NAMES[cards[cid].kind]} {num[cid]}</a>'
        return m.group(0)  # equation labels stay for MathJax

    t = re.sub(r'\\(?:ref|Cref|cref)\{([^}]*)\}', ref, t)
    t = re.sub(r'\\cite\[([^\]]*)\]\{([^}]*)\}', r'<span class="cite">[\2, \1]</span>', t)
    t = re.sub(r'\\cite\{([^}]*)\}', r'<span class="cite">[\1]</span>', t)
    for env, tag in (('enumerate', 'ol'), ('itemize', 'ul')):
        t = re.sub(r'\\begin\{' + env + r'\}(\[[^\]]*\])?', f'<{tag}>', t)
        t = t.replace(r'\end{' + env + '}', f'</li></{tag}>')
    t = re.sub(r'<(ol|ul)>\s*\\item(\[[^\]]*\])?', lambda m: f'<{m.group(1)}><li>' + (f'<b>{m.group(2)[1:-1]}</b> ' if m.group(2) else ''), t)
    t = re.sub(r'\\item(\[[^\]]*\])?', lambda m: '</li><li>' + (f'<b>{m.group(1)[1:-1]}</b> ' if m.group(1) else ''), t)
    t = t.replace('~', ' ')
    for cid in sorted(num, key=len, reverse=True):
        t = re.sub(r'(?<![\w#/-])' + re.escape(cid) + r'(?![\w-])',
                   f'<a class="ref" href="#{cid}">{KIND_NAMES[cards[cid].kind]} {num[cid]}</a>', t)
    # one paragraph per blank line; proof steps "(n) " start their own paragraph
    t = re.sub(r'\n\((\d+)\) ', r'\n\n(\1) ', t)
    return ''.join(f'<p>{x.strip()}</p>' for x in re.split(r'\n\s*\n', t) if x.strip())


def build(h, cards, st, items, card_label, prop_kinds, fact_kinds):
    num = numbering(cards, items, fact_kinds)
    label_to_id = {card_label(c): c.id for c in cards.values() if c.is_fact}
    author_proofs = {x: c for c in cards.values() if c.kind == 'explanation' and c.meta.get('role') == 'proof'
                     for x in c.meta.get('explains') or []}
    conv = lambda s: tex_to_html(s, cards, num, label_to_id, card_label)  # noqa: E731
    out, toc, cur, appendix = [], [], object(), False
    for si, stitle, cid, opt in items:
        if cid not in cards:
            continue
        c = cards[cid]
        if si is None and not appendix:
            appendix = True
            out.append('<h2 id="sec-A">A　{{appendix}}</h2>')
            toc.append(('sec-A', 'A　{{appendix}}'))
        elif si is not None and si != cur:
            cur = si
            out.append(f'<h2 id="sec-{si + 1}">{si + 1}　{_html.escape(stitle)}</h2>')
            toc.append((f'sec-{si + 1}', f'{si + 1}　{_html.escape(stitle)}'))
        if c.kind == 'explanation':
            if c.meta.get('role') == 'proof':
                continue
            out.append(f'<section class="prose" data-card="{cid}"><span class="cid">{cid}</span>{conv(c.body)}</section>')
            continue
        title = f'（{_html.escape(c.meta["title"])}）' if c.meta.get('title') else ''
        head = f'<span class="kname">{KIND_NAMES[c.kind]} {num.get(cid, "")}</span>{title}'
        parts = [f'<div class="stmt">{conv(c.sec("Statement"))}</div>']
        if c.kind in prop_kinds:
            mode = opt.get('proof') or ('author' if cid in author_proofs else 'fact')
            proof = author_proofs[cid].body if mode == 'author' and cid in author_proofs else c.sec('Proof')
            if mode in ('fact', 'author') and proof.strip():
                parts.append(f'<details class="proof"><summary>{{proof}}</summary>{conv(proof)}</details>')
        out.append(f'<article id="{cid}" class="card k-{c.kind}" data-card="{cid}">'
                   f'<header>{head}<span class="cid">{cid}</span></header>{"".join(parts)}</article>')
    nav = ''.join(f'<a href="#{a}">{t}</a>' for a, t in toc)
    title = _html.escape(st.get('title') or h.cfg.get('title') or 'Draft')
    macros = json.dumps(h.cfg.get('mathjax_macros') or {})
    page = (PAGE.replace('%TITLE%', title).replace('%LANG%', _html.escape(h.language))
            .replace('%MATHJAX%', _html.escape(h.cfg.get('mathjax', 'https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-chtml-full.js')))
            .replace('%MACROS%', macros).replace('%NAV%', nav).replace('%BODY%', '\n'.join(out))
            .replace('%SIZE%', str(h.cfg.get('reader_font_px', 21))).replace('%WIDTH%', str(h.cfg.get('reader_width_em', 34))))
    for k, v in LABELS['ja' if h.language == 'ja' else 'en'].items():
        page = page.replace('{{' + k + '}}', _html.escape(v))
    return page


PAGE = r"""<!doctype html><html lang="%LANG%"><head><meta charset="utf-8"><title>%TITLE%</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<script>
MathJax = {tex: {inlineMath: [['$','$'],['\\(','\\)']], displayMath: [['\\[','\\]'],['$$','$$']],
  processEnvironments: true, tags: 'ams', macros: %MACROS%},
  options: {skipHtmlTags: ['script','noscript','style','textarea','code']},
  startup: {pageReady() { return MathJax.startup.defaultPageReady().then(() => {
    for (const it of MathJax.startup.document.math) {
      const m = it.math, root = it.typesetRoot; if (!root) continue;
      root.dataset.tex = !it.display ? '$' + m + '$' : (m.startsWith('\\begin') ? m : '\\[' + m + '\\]');
    }});}}};
</script>
<script defer src="%MATHJAX%"></script>
<style>
:root{--fs:%SIZE%px;--w:%WIDTH%em;--bg:#fbfaf7;--fg:#1d1d1f;--muted:#76736d;--rule:#e2ddd3;--box:#f3f0e8;--accent:#8a5a00;--link:#1f5fa8;--hl:#fff1b8}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#1b1b1d;--fg:#e8e6e1;--muted:#9a968e;--rule:#3a3936;--box:#25242a;--accent:#e0b060;--link:#8ab4f8;--hl:#5a4a10}}
:root[data-theme="dark"]{--bg:#1b1b1d;--fg:#e8e6e1;--muted:#9a968e;--rule:#3a3936;--box:#25242a;--accent:#e0b060;--link:#8ab4f8;--hl:#5a4a10}
html{background:var(--bg)}
body{margin:0;color:var(--fg);background:var(--bg);font-family:"Noto Serif","Source Serif 4","Georgia","Times New Roman","Hiragino Mincho ProN","Yu Mincho","Noto Serif JP","Noto Serif CJK JP",serif;font-size:var(--fs);line-height:1.95}
mjx-container.msel{background:Highlight;color:HighlightText;border-radius:2px}
main{max-width:var(--w);margin:0 auto;padding:4.5em 1em 40vh}
h1{font-size:1.5em;line-height:1.5;margin:.5em 0 1.5em}
h2{font-size:1.2em;margin:2.5em 0 1em;padding-bottom:.2em;border-bottom:1px solid var(--rule)}
p{margin:.55em 0}
a{color:var(--link);text-decoration:none} a:hover{text-decoration:underline}
.card{margin:1.6em 0;padding:.6em 1em;border-left:4px solid var(--rule);background:var(--box);border-radius:4px}
.card:target{outline:2px solid var(--accent)}
.k-theorem,.k-proposition,.k-corollary{border-left-color:var(--accent)}
.card header{font-weight:bold;margin-bottom:.2em}
.kname{margin-right:.3em}
.cid{float:right;font:12px/1.6 ui-monospace,monospace;color:var(--muted);font-weight:normal;user-select:none}
.proof summary{cursor:pointer;color:var(--muted);font-size:.9em}
.proof[open] summary{margin-bottom:.4em}
.proof{margin-top:.5em}
.prose{margin:1.2em 0}
.cite{color:var(--muted);font-size:.9em}
ol,ul{padding-left:1.4em}
mjx-container[display="true"]{overflow-x:auto;overflow-y:hidden}
#bar{position:fixed;top:0;left:0;right:0;z-index:5;display:flex;gap:.4em;align-items:center;padding:.4em .8em;background:var(--bg);border-bottom:1px solid var(--rule);font:14px system-ui,sans-serif}
#bar button,#cbox button{font:13px system-ui,sans-serif;padding:.2em .6em;border:1px solid var(--rule);background:var(--box);color:var(--fg);border-radius:4px;cursor:pointer}
#bar .sp{flex:1}
#toc{display:none;position:fixed;top:2.6em;left:.8em;z-index:6;max-height:70vh;overflow:auto;background:var(--bg);border:1px solid var(--rule);padding:.5em .8em;font:14px/1.8 system-ui,sans-serif}
#toc a{display:block}
#addc{position:absolute;display:none;z-index:7;font:13px system-ui,sans-serif;padding:.25em .7em;border:1px solid var(--accent);background:var(--accent);color:var(--bg);border-radius:4px;cursor:pointer}
#cbox{display:none;position:fixed;right:1em;bottom:1em;z-index:8;width:min(30em,90vw);max-height:60vh;overflow:auto;background:var(--bg);border:1px solid var(--rule);border-radius:6px;padding:.6em .8em;font:14px/1.6 system-ui,sans-serif;box-shadow:0 4px 18px rgba(0,0,0,.18)}
#cbox textarea{width:100%;box-sizing:border-box;min-height:4em;font:14px system-ui,sans-serif;background:var(--bg);color:var(--fg);border:1px solid var(--rule)}
#clist .c{border-top:1px solid var(--rule);padding:.3em 0}
#clist .q{color:var(--muted)}
mark.cm{background:var(--hl);color:inherit}
</style></head><body>
<div id="bar"><button id="btoc">{{toc}}</button><button id="bsm" title="{{smaller}}">A−</button><button id="blg" title="{{larger}}">A＋</button>
<button id="bnr" title="{{narrower}}">⇤⇥−</button><button id="bwd" title="{{wider}}">⇤⇥＋</button><button id="bth">{{theme}}</button>
<span class="sp"></span><button id="bcom">{{comments}} <span id="ccount">0</span></button><button id="bcopy">{{copy}}</button></div>
<nav id="toc">%NAV%</nav>
<main><h1>%TITLE%</h1>
%BODY%
</main>
<button id="addc">{{add}}</button>
<div id="cbox"><div id="cedit" style="display:none"><div class="q" id="cquote"></div><textarea id="ctext" placeholder="{{placeholder}}"></textarea>
<button id="csave">{{save}}</button> <button id="ccancel">{{cancel}}</button></div>
<div id="clist"></div><p><button id="cclear">{{clear}}</button> <button id="cclose">{{close}}</button></p></div>
<script>
(function(){
  const root=document.documentElement, store={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
  const key='reader:'+location.pathname;
  let fs=parseFloat(store.get(key+':fs'))||%SIZE%, w=parseFloat(store.get(key+':w'))||%WIDTH%;
  const th=store.get(key+':theme'); if(th) root.dataset.theme=th;
  function apply(){root.style.setProperty('--fs',fs+'px');root.style.setProperty('--w',w+'em');store.set(key+':fs',fs);store.set(key+':w',w);}
  apply();
  const $=id=>document.getElementById(id);
  $('bsm').onclick=()=>{fs=Math.max(14,fs-1);apply()}; $('blg').onclick=()=>{fs=Math.min(34,fs+1);apply()};
  $('bnr').onclick=()=>{w=Math.max(20,w-2);apply()}; $('bwd').onclick=()=>{w=Math.min(60,w+2);apply()};
  $('bth').onclick=()=>{const d=root.dataset.theme==='dark'||(!root.dataset.theme&&matchMedia('(prefers-color-scheme: dark)').matches);root.dataset.theme=d?'light':'dark';store.set(key+':theme',root.dataset.theme)};
  $('btoc').onclick=()=>{const t=$('toc');t.style.display=t.style.display==='block'?'none':'block'};
  $('toc').onclick=()=>{$('toc').style.display='none'};
  // comments: only in this tab (sessionStorage survives a reload)
  let comments=[]; try{comments=JSON.parse(sessionStorage.getItem(key+':c')||'[]')}catch(e){}
  const save=()=>{try{sessionStorage.setItem(key+':c',JSON.stringify(comments))}catch(e){}};
  let pending=null;
  function cardOf(node){while(node&&node!==document.body){if(node.dataset&&node.dataset.card)return node; node=node.parentNode}return null}
  // Selected text with every formula replaced by its TeX source (data-tex set after typesetting).
  function selText(s){
    if(!s.rangeCount)return '';
    const d=document.createElement('div');
    for(let i=0;i<s.rangeCount;i++)d.appendChild(s.getRangeAt(i).cloneContents());
    if(!d.querySelector('mjx-container'))return s.toString();
    d.querySelectorAll('mjx-container').forEach(m=>m.replaceWith(m.dataset.tex||''));
    return d.textContent;
  }
  // Formulas draw their glyphs outside the text, so mark the ones inside the selection ourselves.
  let marked=[];
  document.addEventListener('selectionchange',()=>{
    marked.forEach(m=>m.classList.remove('msel')); marked=[];
    const s=getSelection(); if(!s.rangeCount||s.isCollapsed)return;
    for(let i=0;i<s.rangeCount;i++){
      let a=s.getRangeAt(i).commonAncestorContainer; if(a.nodeType!==1)a=a.parentNode;
      const own=a.closest('mjx-container');
      for(const m of own?[own]:a.querySelectorAll('mjx-container'))
        if(s.containsNode(m,true)){m.classList.add('msel');marked.push(m)}
    }
  });
  document.addEventListener('copy',e=>{
    const s=getSelection(); if(!s.rangeCount)return;
    const t=selText(s); if(t===s.toString())return;
    e.clipboardData.setData('text/plain',t); e.preventDefault();
  });
  function label(el){const h=el.querySelector('.kname');return (h?h.textContent+' ':'')+'['+el.dataset.card+']'}
  function render(){
    $('ccount').textContent=comments.length;
    $('clist').innerHTML=comments.map((c,i)=>'<div class="c"><b>'+c.where+'</b><div class="q">「'+c.quote.replace(/</g,'&lt;')+'」</div><div>'+c.text.replace(/</g,'&lt;')+'</div><button data-i="'+i+'">{{delete}}</button></div>').join('')||'<p class="q">{{none}}</p>';
    $('clist').querySelectorAll('button').forEach(b=>b.onclick=()=>{comments.splice(+b.dataset.i,1);save();render()});
  }
  document.addEventListener('mouseup',e=>{
    if(e.target.closest('#cbox,#bar,#addc'))return;
    const s=getSelection(); const txt=selText(s).trim(); const b=$('addc');
    if(!txt){b.style.display='none';return}
    const el=cardOf(s.anchorNode); if(!el){b.style.display='none';return}
    pending={where:label(el),quote:txt.replace(/\s+/g,' ')};
    const r=s.getRangeAt(0).getBoundingClientRect();
    b.style.left=(window.scrollX+r.right+6)+'px'; b.style.top=(window.scrollY+r.top-4)+'px'; b.style.display='block';
  });
  $('addc').onclick=()=>{ $('addc').style.display='none'; $('cbox').style.display='block'; $('cedit').style.display='block';
    $('cquote').textContent=pending.where+'「'+pending.quote+'」'; $('ctext').value=''; $('ctext').focus(); };
  $('csave').onclick=()=>{ if(!pending)return; comments.push({...pending,text:$('ctext').value.trim()}); pending=null; save(); $('cedit').style.display='none'; render(); };
  $('ccancel').onclick=()=>{ pending=null; $('cedit').style.display='none'; };
  $('bcom').onclick=()=>{ const b=$('cbox'); b.style.display=b.style.display==='block'?'none':'block'; render(); };
  $('cclose').onclick=()=>{ $('cbox').style.display='none'; };
  $('cclear').onclick=()=>{ if(confirm('{{confirm}}')){comments=[];save();render()} };
  $('bcopy').onclick=async()=>{
    const text=comments.map(c=>c.where+'\n「'+c.quote+'」\n→ '+(c.text||'{{nocomment}}')).join('\n\n');
    try{await navigator.clipboard.writeText(text)}catch(e){const t=document.createElement('textarea');t.value=text;document.body.appendChild(t);t.select();document.execCommand('copy');t.remove()}
    $('bcopy').textContent='{{copied}}'; setTimeout(()=>$('bcopy').textContent='{{copy}}',1500);
  };
  render();
})();
</script></body></html>"""
