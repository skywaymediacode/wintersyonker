const { chromium } = require('playwright');
function lum(c){const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)};return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])}
function cr(a,b){const l1=lum(a),l2=lum(b);const [h,lo]=l1>l2?[l1,l2]:[l2,l1];return (h+0.05)/(lo+0.05)}
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox']});
  const ctx=await b.newContext({viewport:{width:1440,height:1000}});
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file://'+process.cwd()+'/Winters-Yonker-Homepage.html',{waitUntil:'load'});
  await p.addStyleTag({content:'.rv{animation:none!important;opacity:1!important;transform:none!important}'});
  await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
  await p.waitForTimeout(900);
  const data=await p.evaluate(()=>{
    const parse=s=>{const m=s.match(/[\d.]+/g);return m?m.slice(0,4).map(Number):null};
    function bgOf(el){let e=el;while(e){const cs=getComputedStyle(e);const c=parse(cs.backgroundColor);
      if(c&&(c[3]===undefined||c[3]>0.6))return{c:c.slice(0,3),img:cs.backgroundImage!=='none'};e=e.parentElement}return null}
    const res=[];
    document.querySelectorAll('p,span,a,b,li,h1,h2,h3,h4,button,em,div,blockquote,small,label,summary,strong,q').forEach(el=>{
      const txt=Array.from(el.childNodes).filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join('');
      if(txt.length<3)return;
      const r=el.getBoundingClientRect(); if(!r.width||!r.height)return;
      const cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none'||+cs.opacity<0.35)return;
      if(el.closest('[aria-hidden="true"]'))return;
      const fg=parse(cs.color); const bg=bgOf(el); if(!fg||!bg)return;
      res.push({txt:txt.slice(0,44),fg:fg.slice(0,3),bg:bg.c,fs:parseFloat(cs.fontSize),bold:+cs.fontWeight>=700,over:bg.img,
        sel:el.tagName+'.'+((el.className||'').toString()).slice(0,24)});
    });
    return res;
  });
  const fails=[];
  for(const d of data){const ratio=cr(d.fg,d.bg);const large=d.fs>=24||(d.fs>=18.66&&d.bold);const need=large?3:4.5;
    if(ratio<need&&!d.over)fails.push({...d,ratio:+ratio.toFixed(2),need})}
  console.log('CONTRAST — checked',data.length,'| fails',fails.length);
  const seen=new Set();
  fails.forEach(x=>{const k=x.sel+x.ratio;if(seen.has(k))return;seen.add(k);
    console.log(`  ${x.ratio} (need ${x.need}) ${x.fs}px ${x.sel} "${x.txt}" fg rgb(${x.fg}) bg rgb(${x.bg})`)});

  // functional
  await p.click('#sendBtn'); await p.waitForTimeout(200);
  console.log('FUNC — form button:', (await p.textContent('#sendBtn')).trim());
  console.log('FUNC — tel links:', await p.$$eval('a[href^="tel:"]',a=>a.length),
              '| details:', await p.$$eval('details',d=>d.length),
              '| errors:', errs.length?errs:'none');
  await b.close();
})();
