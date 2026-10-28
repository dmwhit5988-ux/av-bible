"""The page beside each reference chart: pan, zoom and search, and, for a
chart that writes a sidecar, a card for whatever is tapped.

`page()` returns the whole page as one HTML string. A chart's generator
writes it beside the chart's SVG, so it costs one deploy file and loads
nothing but the SVG and its sidecar. The web app's Reference list opens it
in a frame (web/js/app.js REFERENCES); opened on its own it works the same,
less the way into the app.

- **Moving.** One finger or the mouse pans, two fingers pinch, the wheel
  zooms, and fit / + / - zoom about the middle. The search box is 16 px so
  that iOS doesn't zoom the whole page when it takes focus.
- **Without a sidecar** (the OT timeline), the search steps through the
  sheet's own text (up and down) and zooms each hit to full size.
- **With a sidecar** (`<stem>.json`, family_tree_data.sidecar):
  - a tap on a box selects it and opens its card: a bottom sheet on a
    phone, a side panel when there is room;
  - search lists the matches, each with its relation so namesakes can be
    told apart: whole names first, then the start of a name, then anywhere
    in one, then a name only a box's note carries; a box's other names
    (`a`, "Jacob" for Israel) count as its own;
  - the card's "Line to Adam" outlines every box up the line and frames
    them; a wife's line is her own, from her reference chip in her
    father's family, or isn't offered;
  - a box that a tap selects is brought into view if the card covers it,
    and a tapped reference chip flies to the real box;
  - a verse chip shows the verse, read from /bibles/WEB/, and in the app
    "Open in Theoria" posts {type: "theoria:goto", book, chapter, verse} to
    the app, which goes there;
  - the address remembers the selection (#id=<id>), and the app opens the
    page at #at=<Book>.<chapter>.<verse> so it starts on the names of the
    verse the reader is on.
- **Escape** closes the results, then the card; the page marks the key as
  used (preventDefault) so the app doesn't also close the frame.
"""

import json

_PAGE = r"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>__TITLE__</title>
<style>
  html,body{margin:0;height:100%;background:#0d0d14;color:#d8c68f;
            font-family:Georgia,'Times New Roman',serif;overflow:hidden}
  #stage{position:absolute;inset:0;cursor:grab;touch-action:none}
  #stage.drag{cursor:grabbing}
  #stage svg{position:absolute;top:0;left:0;transform-origin:0 0}
  #bar{position:absolute;top:0;left:0;right:0;z-index:5;display:flex;
       flex-wrap:wrap;gap:8px 10px;align-items:center;padding:10px 14px;
       background:linear-gradient(#0d0d14ee,#0d0d1400)}
  input,button{font:14px Georgia,serif;background:#16161f;color:#d8c68f;
       border:1px solid #4a4658;border-radius:6px;padding:6px 10px}
  #find{position:relative;flex:0 1 330px;min-width:0;display:flex}
  input{font-size:16px;flex:1;min-width:0}
  button{cursor:pointer;min-width:36px}
  #hits{font-size:13px;color:#8a8270;font-style:italic}
  #results{position:absolute;top:100%;left:0;right:0;margin-top:4px;z-index:8;
       max-height:min(52vh,420px);overflow-y:auto;background:#16161f;
       border:1px solid #4a4658;border-radius:8px;box-shadow:0 6px 18px #0009}
  #results button{display:block;width:100%;text-align:left;border:0;
       border-bottom:1px solid #26232f;border-radius:0;padding:8px 10px;
       background:none}
  #results .r-n{color:#e8e0cc;font-size:15px}
  #results .r-s{color:#8a8270;font-size:12px;font-style:italic}
  #banner{position:absolute;left:50%;transform:translateX(-50%);z-index:6;
       bottom:calc(14px + env(safe-area-inset-bottom));display:flex;
       gap:8px;align-items:center;padding:6px 6px 6px 12px;font-size:13px;
       background:#16161fee;border:1px solid #4a4658;border-radius:18px;
       max-width:calc(100% - 28px)}
  #card{position:absolute;z-index:7;background:#14141c;color:#e8e0cc;
       border:1px solid #4a4658;overflow-y:auto;box-sizing:border-box;
       padding:12px 14px calc(14px + env(safe-area-inset-bottom));
       left:0;right:0;bottom:0;max-height:46vh;
       border-radius:12px 12px 0 0;border-bottom:0}
  @media (min-width:700px){
    #card{left:auto;top:58px;width:340px;max-height:none;
          border-radius:10px 0 0 0;border-right:0}
    /* the banner stays clear of the side panel */
    body.carded #banner{left:calc((100% - 340px)/2);max-width:calc(100% - 368px)}
  }
  [hidden]{display:none!important}
  .c-head{display:flex;gap:10px;align-items:flex-start;justify-content:space-between}
  .c-name{font-size:19px;color:#fff4aa}
  .c-sub{font-size:13px;color:#a89f88;font-style:italic;margin-top:2px}
  .c-facts,.c-date{font-size:12px;color:#8a8270;margin-top:6px}
  .c-note{font-size:14px;line-height:1.45;margin:8px 0 0;color:#d8d0bc;font-style:italic}
  .c-row{margin-top:10px;font-size:13px;line-height:1.9}
  .c-lab{display:block;font-size:11px;letter-spacing:1px;text-transform:uppercase;
       color:#8a8270;line-height:1.4}
  .chip{font-size:13px;padding:3px 9px;margin:2px 4px 2px 0;border-radius:14px;
       min-width:0;color:#e8e0cc}
  .chip.house{font-style:italic;color:#a89f88}
  .chip.v{color:#d8c68f}
  .c-book{font-size:12px;color:#a89f88;margin-right:4px}
  #vv{margin-top:8px;padding:8px 10px;border-left:2px solid #d8c68f;background:#1b1b24}
  #vv .vv-ref{font-size:12px;color:#d8c68f;margin-bottom:4px}
  #vv p{margin:0 0 4px;font-size:14px;line-height:1.45}
  #vv .vv-go{margin-top:6px;color:#16130a;background:#d8c68f;border-color:#fff4aa}
  .line{margin-top:6px;line-height:2}
  .line .sep{color:#5a5468;margin-right:4px}
</style>
<div id="bar">
  <div id="find">
    <input id="q" placeholder="__PLACEHOLDER__" size="34" autocomplete="off" spellcheck="false">
    <div id="results" role="listbox" hidden></div>
  </div>
  <button id="prev" aria-label="Previous match">&#8593;</button><button id="next" aria-label="Next match">&#8595;</button>
  <span id="hits"></span>
  <button id="fit">fit</button><button id="in" aria-label="Zoom in">+</button><button id="out" aria-label="Zoom out">&minus;</button>
</div>
<div id="stage"></div>
<div id="banner" hidden><span id="banner-text"></span><button id="banner-x" aria-label="Clear">&#x2715;</button></div>
<aside id="card" aria-label="Details" hidden></aside>
<script>
const W=__W__,H=__H__,DATA=__DATA__,STEM=__STEM__;
const $=id=>document.getElementById(id);
const stage=$('stage'),q=$('q'),hits=$('hits'),results=$('results'),card=$('card');
const NS='http://www.w3.org/2000/svg';
let k=1,tx=0,ty=0,kmin=0.01,svg,anim=0,groups=[],at=-1,matches=[];
let data=null,items=[],state={sel:null,trace:false,at:null};
const layers={};
let framed=false;
try{framed=parent!==window&&parent.location.origin===location.origin}catch(e){}
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

Promise.all([fetch(STEM+'.svg').then(r=>r.text()),
             DATA?fetch(STEM+'.json').then(r=>r.json()):null]).then(([t,d])=>{
  stage.innerHTML=t;data=d;items=d?d.items:[];init()});

function apply(){svg.style.transform=`translate(${tx}px,${ty}px) scale(${k})`;
  for(const[name,px]of[['at',2.5],['trace',2.5],['sel',3.5]])
    if(layers[name])layers[name].setAttribute('stroke-width',(px/k).toFixed(3))}
function fit(){k=Math.min(innerWidth/W,innerHeight/H);
  kmin=Math.min(0.01,k);tx=(innerWidth-W*k)/2;ty=(innerHeight-H*k)/2;apply()}
function init(){svg=stage.querySelector('svg');
  svg.removeAttribute('width');svg.removeAttribute('height');
  svg.setAttribute('width',W);svg.setAttribute('height',H);
  groups=[...svg.querySelectorAll('text')];
  const hl=document.createElementNS(NS,'g');hl.setAttribute('pointer-events','none');
  hl.setAttribute('fill','none');svg.appendChild(hl);
  for(const[name,col,fill]of[['at','#e8e0cc','#e8e0cc14'],['trace','#d8c68f','#d8c68f10'],
                             ['sel','#fff4aa','#fff4aa1c']]){
    const g=document.createElementNS(NS,'g');g.setAttribute('stroke',col);
    g.setAttribute('fill',fill);hl.appendChild(g);layers[name]=g}
  fit();if(DATA)readHash()}

// -- moving ---------------------------------------------------------------
function zoomAt(x,y,f){const nk=Math.min(8,Math.max(kmin,k*f));
  tx=x-(x-tx)*(nk/k);ty=y-(y-ty)*(nk/k);k=nk}
function freeArea(){const top=$('bar').offsetHeight;let w=innerWidth,h=innerHeight-top;
  if(!card.hidden){if(innerWidth>=700)w-=card.offsetWidth;else h-=card.offsetHeight}
  return{x:0,y:top,w:Math.max(w,80),h:Math.max(h,80)}}
// A flight eases there by animation frames, and a timer lands it in case the
// frames stall (a page in the background gets none). A touch, the wheel or a
// zoom button calls halt(), which cancels both.
let flight=0;
function halt(){cancelAnimationFrame(anim);flight++}
function flyTo(cx,cy,nk){halt();const me=flight;
  const fa=freeArea(),fx=fa.x+fa.w/2,fy=fa.y+fa.h/2,k0=k,
        c0x=(fx-tx)/k,c0y=(fy-ty)/k,t0=performance.now(),ms=450;
  const step=now=>{if(me!==flight)return;
    const t=Math.min(1,(now-t0)/ms),e=t<.5?2*t*t:1-Math.pow(2-2*t,2)/2;
    k=k0*Math.pow(nk/k0,e);tx=fx-(c0x+(cx-c0x)*e)*k;ty=fy-(c0y+(cy-c0y)*e)*k;apply();
    if(t<1)anim=requestAnimationFrame(step)};
  anim=requestAnimationFrame(step);
  setTimeout(()=>{if(me!==flight)return;k=nk;tx=fx-cx*nk;ty=fy-cy*nk;apply()},ms+150)}
function frameBoxes(list,kmax){let x0=1e9,y0=1e9,x1=-1e9,y1=-1e9;
  for(const b of list){x0=Math.min(x0,b[0]);y0=Math.min(y0,b[1]);
    x1=Math.max(x1,b[0]+b[2]);y1=Math.max(y1,b[1]+b[3])}
  const fa=freeArea();
  const nk=Math.max(kmin,Math.min((fa.w-48)/(x1-x0),(fa.h-48)/(y1-y0),kmax));
  flyTo((x0+x1)/2,(y0+y1)/2,nk)}
stage.addEventListener('wheel',e=>{e.preventDefault();halt();
  zoomAt(e.clientX,e.clientY,Math.exp(-e.deltaY*0.0015));apply()},{passive:false});
const pts=new Map();let pinch=null,tap=null;
function span(){const[a,b]=[...pts.values()];
  return{x:(a.x+b.x)/2,y:(a.y+b.y)/2,d:Math.hypot(a.x-b.x,a.y-b.y)||1}}
stage.addEventListener('pointerdown',e=>{halt();
  tap=pts.size?null:{x:e.clientX,y:e.clientY,t:performance.now()};
  pts.set(e.pointerId,{x:e.clientX,y:e.clientY});
  stage.classList.add('drag');stage.setPointerCapture(e.pointerId);
  pinch=pts.size===2?span():null});
stage.addEventListener('pointermove',e=>{const p=pts.get(e.pointerId);if(!p)return;
  if(tap&&Math.hypot(e.clientX-tap.x,e.clientY-tap.y)>8)tap=null;
  if(pts.size===1){tx+=e.clientX-p.x;ty+=e.clientY-p.y}
  p.x=e.clientX;p.y=e.clientY;
  if(pts.size===2&&pinch){const s=span();tx+=s.x-pinch.x;ty+=s.y-pinch.y;
    zoomAt(s.x,s.y,s.d/pinch.d);pinch=s}
  apply()});
function lift(e){pts.delete(e.pointerId);pinch=pts.size===2?span():null;
  if(!pts.size){stage.classList.remove('drag');
    if(tap&&performance.now()-tap.t<600)onTap(tap.x,tap.y);tap=null}}
stage.addEventListener('pointerup',lift);
stage.addEventListener('pointercancel',e=>{tap=null;lift(e)});
document.addEventListener('gesturestart',e=>e.preventDefault());
$('fit').onclick=fit;
$('in').onclick=()=>{halt();zoomAt(innerWidth/2,innerHeight/2,1.3);apply()};
$('out').onclick=()=>{halt();zoomAt(innerWidth/2,innerHeight/2,1/1.3);apply()};

// -- search ---------------------------------------------------------------
// A box's names and the other names it goes by ("Israel" is also Jacob) rank
// whole names first, then the start of a name, then anywhere in one; a name
// found only in a box's note comes last.
function rank(s){const out=[];
  items.forEach((it,i)=>{if(it.x!=null)return;let best=4;
    for(const part of it.n.split('·').concat(it.a||[])){const t=part.trim().toLowerCase();
      if(t===s){best=0;break}
      if(t.startsWith(s))best=Math.min(best,1);else if(t.includes(s))best=Math.min(best,2)}
    if(best===4&&(it.note||'').toLowerCase().includes(s))best=3;
    if(best<4)out.push([best,it.g==null?999:it.g,i])});
  out.sort((a,b)=>a[0]-b[0]||a[1]-b[1]||a[2]-b[2]);return out.map(r=>r[2])}
function search(){searchTimer=0;const s=q.value.trim().toLowerCase();at=-1;
  if(!DATA){matches=s?groups.filter(t=>t.textContent.toLowerCase().includes(s)):[];
    hits.textContent=s?`${matches.length} found`:'';if(matches.length)go(0);return}
  matches=s?rank(s):[];
  hits.textContent=s?`${matches.length} found`:'';
  results.innerHTML=matches.slice(0,60).map((i,n)=>`<button data-n="${n}" role="option">`+
    `<div class="r-n">${esc(items[i].n)}</div><div class="r-s">${esc(items[i].s||'')}`+
    `${items[i].g!=null?' · generation '+items[i].g:''}</div></button>`).join('')+
    (matches.length>60?`<div class="r-s" style="padding:8px 10px">and ${matches.length-60} more — type more of the name</div>`:'');
  results.hidden=!s||document.activeElement!==q}
function go(n){if(!matches.length)return;at=(n+matches.length)%matches.length;
  if(DATA){select(matches[at],{fly:true});hits.textContent=`${at+1} / ${matches.length}`;return}
  const t=matches[at];let b=t.getBoundingClientRect();
  if(k<1){zoomAt(b.left+b.width/2,b.top+b.height/2,1/k);apply();
    b=t.getBoundingClientRect()}
  tx-=b.left+b.width/2-innerWidth/2;ty-=b.top+b.height/2-innerHeight/2;apply();
  t.style.fill='#fff4aa';setTimeout(()=>t.style.fill='',2200);
  hits.textContent=`${at+1} / ${matches.length}`}
let searchTimer=0;
q.addEventListener('input',()=>{clearTimeout(searchTimer);searchTimer=setTimeout(search,DATA?90:0)});
q.addEventListener('focus',()=>{if(DATA&&q.value.trim())results.hidden=false});
q.addEventListener('blur',()=>setTimeout(()=>{results.hidden=true},180));
q.addEventListener('keydown',e=>{if(e.key!=='Enter')return;
  // a search still waiting out its pause runs now, so Enter takes this query
  if(searchTimer){clearTimeout(searchTimer);search()}
  if(!matches.length)return;e.preventDefault();go(at<0?0:at);q.blur()});
results.addEventListener('pointerdown',e=>e.preventDefault());
results.addEventListener('click',e=>{const b=e.target.closest('button[data-n]');if(!b)return;
  go(Number(b.dataset.n));results.hidden=true;q.blur()});
$('next').onclick=()=>matches.length&&go(at+1);
$('prev').onclick=()=>matches.length&&go(at-1);

// -- selecting ------------------------------------------------------------
function outline(layer,list){const g=layers[layer];g.textContent='';
  for(const i of list||[]){const b=items[i].b,r=document.createElementNS(NS,'rect'),pad=5;
    r.setAttribute('x',b[0]-pad);r.setAttribute('y',b[1]-pad);
    r.setAttribute('width',b[2]+2*pad);r.setAttribute('height',b[3]+2*pad);
    r.setAttribute('rx',8);g.appendChild(r)}
  apply()}
function onTap(x,y){if(!DATA||!svg)return;const sx=(x-tx)/k,sy=(y-ty)/k,tol=6/k;
  let best=-1,area=Infinity;
  items.forEach((it,i)=>{const b=it.b;
    if(sx>=b[0]-tol&&sx<=b[0]+b[2]+tol&&sy>=b[1]-tol&&sy<=b[1]+b[3]+tol&&b[2]*b[3]<area){
      best=i;area=b[2]*b[3]}});
  if(best>=0)select(best,{fly:k<0.6})}
function ancestors(i){const out=[];for(let j=i;j!=null;j=items[j].p)out.unshift(j);return out}
// Where a box's own line to Adam starts. A wife hangs under her husband, so
// his line isn't hers: hers runs from her reference chip in her father's
// family where she has one (Leah under Laban), and otherwise isn't drawn.
function lineFrom(i){const it=items[i];
  if(it.l!=='wife'&&it.l!=='kin')return i;
  const own=items.findIndex(c=>c.x===i&&c.p!=null&&c.l!=='wife');
  return own>=0?own:null}
function select(i,{fly=false}={}){const via=items[i].x!=null;if(via)i=items[i].x;
  state.sel=i;state.trace=false;outline('sel',[i]);outline('trace',[]);
  renderCard();
  try{history.replaceState(null,'','#id='+encodeURIComponent(items[i].id))}catch(e){}
  // A tap on a reference chip goes to the real box, wherever it is; a box
  // the card now covers, or that is off screen, comes into view.
  const b=items[i].b,fa=freeArea(),x0=b[0]*k+tx,y0=b[1]*k+ty;
  const seen=x0>=fa.x&&y0>=fa.y&&x0+b[2]*k<=fa.x+fa.w&&y0+b[3]*k<=fa.y+fa.h;
  if(fly||via)frameBoxes([b],Math.min(Math.max(k,1.2),2));
  else if(!seen)flyTo(b[0]+b[2]/2,b[1]+b[3]/2,k)}
function deselect(){state.sel=null;state.trace=false;outline('sel',[]);outline('trace',[]);
  card.hidden=true;card.innerHTML='';document.body.classList.remove('carded');
  try{history.replaceState(null,'',location.pathname+location.search)}catch(e){}}

// -- the card -------------------------------------------------------------
const chip=(i,extra='')=>{const it=items[i];
  return `<button class="chip${it.k==='house'?' house':''}" data-go="${i}">${esc(it.n)}${extra}</button>`};
function refLabel(r){const[,c1,v1,c2,v2]=r;
  if(!v1)return c2?`${c1}–${c2}`:`${c1}`;
  if(c2)return `${c1}:${v1}–${c2}:${v2}`;
  return v2?`${c1}:${v1}–${v2}`:`${c1}:${v1}`}
const single=r=>r[2]&&!r[3]&&!r[4];
function merged(rows){const out=[],ranges=rows.filter(r=>!single(r));
  // a verse a range on the same card already covers isn't listed again
  rows=rows.filter(r=>!single(r)||!ranges.some(g=>g[0]===r[0]&&inRange(g,r[1],r[2])));
  for(const r of rows){const p=out[out.length-1];
    if(p&&r[0]===p[0]&&r[1]===p[1]&&!p[3]&&!r[3]&&!r[4]&&r[2]&&p[2]&&r[2]===(p[4]||p[2])+1){
      p[4]=r[2];continue}
    out.push(r.slice())}
  return out}
function renderCard(keep=false){const i=state.sel,it=items[i];if(i==null)return;
  const kind={king:'king',priest:'priest or Levite',house:'a house or company'}[it.k];
  const facts=[it.g!=null?`generation ${it.g} from Adam`:'',kind||''].filter(Boolean).join(' · ');
  let h=`<div class="c-head"><div><div class="c-name">${esc(it.n)}</div>`+
    (it.s?`<div class="c-sub">${esc(it.s)}</div>`:'')+`</div>`+
    `<button id="card-x" aria-label="Close">&#x2715;</button></div>`;
  if(facts)h+=`<div class="c-facts">${esc(facts)}</div>`;
  if(it.d)h+=`<div class="c-date">${esc(it.d)}</div>`;
  if(it.note)h+=`<p class="c-note">${esc(it.note)}</p>`;
  // a cross-reference to this box's own reference chip names the family the
  // chip stands in, which then isn't listed again under "Also in the family of"
  const told=new Set();
  for(const[o,why]of it.xr||[]){const self=items[o].x===i&&items[o].p!=null,to=self?items[o].p:o;
    if(self)told.add(to);
    h+=`<div class="c-row"><span class="c-lab">Also</span>${chip(to)} <span class="c-note" style="font-size:13px">${esc(why)}</span></div>`}
  const p=it.p!=null?items[it.p]:null;
  if(p){if(it.l==='wife')h+=row('Husband',[it.p]);
    else if(it.l==='kin')h+=row('Family',[it.p]);
    else if((p.l==='wife'||p.l==='kin')&&p.p!=null)h+=row('Parents',[p.p,it.p]);
    else h+=row(p.k==='house'?'Among':it.l==='dash'?'Joined under':p.k==='woman'?'Mother':'Father',[it.p])}
  // "kin" is the wife line used for the reckoning only: Tamar, whose sons
  // are reckoned to Judah, her father-in-law
  const kids=it.c||[],wives=kids.filter(j=>items[j].l==='wife'),
        kin=kids.filter(j=>items[j].l==='kin'),
        others=kids.filter(j=>!wives.includes(j)&&!kin.includes(j)),
        // a dashed join is one the text implies (a man hung on his tribe),
        // not a son, except inside a house, whose members all hang that way
        joined=it.k==='house'?[]:others.filter(j=>items[j].l==='dash'),
        rest=others.filter(j=>!joined.includes(j));
  const echoes=[];items.forEach(c=>{if(c.x===i&&c.p!=null&&!told.has(c.p))echoes.push(c.p)});
  if(echoes.length)h+=row('Also in the family of',echoes);
  if(wives.length)h+=row(it.l==='wife'?'Husbands':'Wives',wives);
  if(rest.length)h+=row(it.k==='house'?'Members':'Children',rest);
  if(joined.length)h+=row('Joined under, as the text implies',joined);
  for(const w of wives)if((items[w].c||[]).length)h+=row('With '+items[w].n,items[w].c);
  for(const w of kin)h+=row(`With ${items[w].n}, ${items[w].s}`,[w].concat(items[w].c||[]));
  const from=lineFrom(i);
  if(it.p!=null&&from!=null){const line=ancestors(from);
    h+=`<div class="c-row"><button id="trace" class="chip v">${state.trace?'Hide the line':from===i?'Line to Adam':'Her line to Adam'} (${line.length})</button>`+
      (state.trace?`<div class="line">${line.map(j=>chip(j)).join('<span class="sep">›</span>')}</div>`:'')+`</div>`}
  if(it.r){h+=`<div class="c-row"><span class="c-lab">Verses</span>`;let last=-1;
    for(const r of merged(it.r)){if(r[0]!==last){last=r[0];h+=`<span class="c-book">${esc(data.books[r[0]])}</span>`}
      h+=`<button class="chip v" data-ref="${r.join(',')}">${refLabel(r)}</button>`}
    h+=`</div><div id="vv" hidden></div>`}
  card.innerHTML=h;card.hidden=false;document.body.classList.add('carded');
  if(!keep)card.scrollTop=0}
function row(label,list){const shown=list.slice(0,24);
  return `<div class="c-row"><span class="c-lab">${esc(label)}</span>`+shown.map(j=>chip(j)).join('')+
    (list.length>24?`<span class="c-book">and ${list.length-24} more</span>`:'')+`</div>`}
card.addEventListener('click',async e=>{const t=e.target.closest('button');if(!t)return;
  if(t.id==='card-x'){deselect();return}
  if(t.dataset.go!=null){select(Number(t.dataset.go),{fly:true});return}
  if(t.id==='trace'){state.trace=!state.trace;
    const line=state.trace?ancestors(lineFrom(state.sel)):[],st=card.scrollTop;
    outline('trace',line);renderCard(true);card.scrollTop=st;
    // keep the card where it was, and bring the line it just listed into view
    const ln=card.querySelector('.line');
    if(ln)card.scrollTop=Math.max(st,ln.offsetTop+ln.offsetHeight-card.clientHeight);
    if(state.trace)frameBoxes(line.map(j=>items[j].b),1.2);return}
  if(t.dataset.ref){showVerse(t.dataset.ref.split(',').map(Number));return}
  if(t.dataset.goto){const[b,c,v]=t.dataset.goto.split('|');
    parent.postMessage({type:'theoria:goto',book:b,chapter:Number(c),verse:Number(v)},location.origin)}});
async function showVerse(r){const[b,c1,v1,c2,v2]=r,book=data.books[b],vv=$('vv');
  vv.hidden=false;vv.innerHTML=`<div class="vv-ref">${esc(book)} ${refLabel(r)}</div><p>…</p>`;
  try{const ch=await fetch(`/bibles/WEB/${book.replace(/ /g,'_')}_${c1}.json`).then(x=>x.json());
    const first=v1||ch.verses[0][0],last=c2?Infinity:(v2||(v1?v1:ch.verses[0][0]));
    const vs=ch.verses.filter(([n])=>n>=first&&n<=last);
    const shown=vs.slice(0,4);
    vv.innerHTML=`<div class="vv-ref">${esc(book)} ${refLabel(r)}</div>`+
      shown.map(([n,t])=>`<p><b style="color:#d8c68f;font-size:11px">${n}</b> ${esc(t)}</p>`).join('')+
      (vs.length>shown.length||c2||!v1?'<p style="color:#8a8270">…</p>':'')+
      (framed?`<button class="vv-go" data-goto="${esc(book)}|${c1}|${first}">Open in Theoria ▸</button>`:'')}
  catch(err){vv.innerHTML=`<div class="vv-ref">${esc(book)} ${refLabel(r)}</div><p>The text didn't load.</p>`}
  vv.scrollIntoView({block:'nearest'})}

// -- the address ----------------------------------------------------------
function inRange(r,C,V){const[,c1,v1,c2,v2]=r,ce=c2||c1;
  if(!v1)return C>=c1&&C<=ce;                 // whole chapters
  if(C<c1||C>ce||(C===c1&&V<v1))return false;
  const ve=v2||(c2?Infinity:v1);return !(C===ce&&V>ve)}
function readHash(){const h=new URLSearchParams(location.hash.slice(1));
  const id=h.get('id');
  if(id){const i=items.findIndex(it=>it.id===id);if(i>=0){select(i,{fly:true});return}
    // an id this sheet no longer has: offer its namesakes instead
    q.value=id.split('.')[0].split('~')[0].split('-')[0];search();
    if(matches.length){results.hidden=false;q.focus()}return}
  const a=(h.get('at')||'').split('.');if(a.length!==3)return;
  const book=a[0].replace(/_/g,' '),C=Number(a[1]),V=Number(a[2]),b=data.books.indexOf(book);
  if(b<0)return;
  // the names the verse itself speaks; failing those, the families whose
  // passage it falls in
  const named=test=>{const out=[];items.forEach((it,i)=>{
    if(it.x==null&&(it.r||[]).some(r=>r[0]===b&&test(r)&&inRange(r,C,V)))out.push(i)});return out};
  let hit=named(single);if(!hit.length)hit=named(r=>!single(r));
  if(!hit.length)return;
  state.at=hit;outline('at',hit);
  $('banner-text').textContent=`${hit.length===1?'1 name':hit.length+' names'} in ${book} ${C}:${V}`;
  $('banner').hidden=false;
  if(hit.length===1)select(hit[0]);
  frameBoxes(hit.map(i=>items[i].b),1.2)}
$('banner-x').onclick=()=>{state.at=null;outline('at',[]);$('banner').hidden=true};
document.addEventListener('keydown',e=>{if(e.key!=='Escape')return;
  if(!results.hidden){results.hidden=true;q.blur();e.preventDefault()}
  else if(!card.hidden){deselect();e.preventDefault()}});
addEventListener('resize',()=>{if(svg)apply()});
</script>
"""


def page(stem, w, h, title, data=False,
         placeholder="find a name — Zerubbabel, Jochebed, Achsah…"):
    """The viewer page for `<stem>.svg` (w x h px), as one HTML string.
    With `data`, it also reads `<stem>.json` (family_tree_data.sidecar)."""
    return (_PAGE.replace("__TITLE__", title)
            .replace("__PLACEHOLDER__", placeholder)
            .replace("__W__", w).replace("__H__", h)
            .replace("__DATA__", "true" if data else "false")
            .replace("__STEM__", json.dumps(stem)))
