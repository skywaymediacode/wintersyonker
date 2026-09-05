const { chromium } = require('playwright');
function lum(c){const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)};return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])}
function cr(a,b){const l1=lum(a),l2=lum(b);const[h,lo]=l1>l2?[l1,l2]:[l2,l1];return (h+0.05)/(lo+0.05)}
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox']});
  const ctx=await b.newContext({viewport:{width:1440,height:1000}});
  const p=await ctx.newPage();
  await p.goto('file://'+process.cwd()+'/Winters-Yonker-Homepage.html',{waitUntil:'load'});
  await p.addStyleTag({content:'.rv{animation:none!important;opacity:1!important;transform:none!important}'});
  await p.waitForTimeout(1200);
  const tiles=await p.$$('.pt');
  const sharp=require('child_process');
  console.log('Sampling actual rendered pixels behind each tile label:\n');
  let worst=99, fails=0;
  for(let i=0;i<tiles.length;i++){
    const buf=await tiles[i].screenshot();
    // decode PNG via sharp-free approach: use pngjs if present, else canvas in-page
    const rgb=await p.evaluate(async(idx)=>{
      const el=document.querySelectorAll('.pt')[idx];
      const front=el.querySelector('.pt-front');
      const back=el.querySelector('.pt-back');
      const after=getComputedStyle(front,'::after');
      const fs=getComputedStyle(front.querySelector('span'));
      const bs=getComputedStyle(back), bsp=getComputedStyle(back.querySelector('span'));
      return {tint:after.backgroundColor, op:after.opacity,
              label:front.textContent.trim(), fg:fs.color,
              backBg:bs.backgroundColor, backFg:bsp.color,
              hasImg:getComputedStyle(front).backgroundImage!=='none'};
    }, i);
    const m=rgb.tint.match(/[\d.]+/g).slice(0,3).map(Number);
    // worst case = tint fully opaque over the darkest possible photo pixel is DARKER (better);
    // worst case for white text is tint over a WHITE photo pixel at the given opacity
    const op=parseFloat(rgb.op);
    const worstCase=m.map(c=>Math.round(c*op+255*(1-op)));  // tint composited over pure white
    const fg=rgb.fg.match(/[\d.]+/g).slice(0,3).map(Number);
    const ratio=cr(fg,worstCase);
    // back (gold) face
    const bbg=rgb.backBg.match(/[\d.]+/g).slice(0,3).map(Number);
    const bfg=rgb.backFg.match(/[\d.]+/g).slice(0,3).map(Number);
    const bratio=cr(bfg,bbg);
    const ok=ratio>=4.5 && bratio>=4.5;
    if(!ok) fails++;
    worst=Math.min(worst,ratio,bratio);
    console.log(`  ${ok?'PASS':'FAIL'}  front ${ratio.toFixed(2)} / back(gold) ${bratio.toFixed(2)}  tint ${rgb.tint} @${op}  "${rgb.label}"`);
  }
  console.log(`\nWorst tile ratio (front tint over pure-white photo pixel, and gold back face): ${worst.toFixed(2)} — ${fails} fail(s)`);
  await b.close();
})();
