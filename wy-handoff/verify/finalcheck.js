const { chromium } = require('playwright');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});
  const ctx=await b.newContext({viewport:{width:1440,height:1000}});
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file://'+process.cwd()+'/Winters-Yonker-Homepage.html',{waitUntil:'load'});
  await p.waitForTimeout(2500);

  // hero video
  const v=await p.evaluate(()=>{const el=document.getElementById('heroVid');
    return el?{paused:el.paused,muted:el.muted,loop:el.loop,t:+el.currentTime.toFixed(2),dur:+(el.duration||0).toFixed(1),w:el.videoWidth,h:el.videoHeight}:null});
  console.log('HERO VIDEO:', JSON.stringify(v));
  await p.click('#heroPP'); await p.waitForTimeout(400);
  console.log('  after pause click -> paused =', await p.evaluate(()=>document.getElementById('heroVid').paused),
              '| label =', await p.getAttribute('#heroPP','aria-label'));
  await p.click('#heroPP'); await p.waitForTimeout(300);
  console.log('  after play click  -> paused =', await p.evaluate(()=>document.getElementById('heroVid').paused));

  // attorney slider
  await p.evaluate(()=>document.getElementById('team').scrollIntoView());
  await p.waitForTimeout(600);
  const names=()=>p.evaluate(()=>{
    const t=document.getElementById('attTrack');
    const i=Math.round(Math.abs(parseFloat((t.style.transform.match(/-?[\d.]+/)||[0])[0]))/100);
    return Array.from(t.children[i].querySelectorAll('b')).map(x=>x.textContent);
  });
  console.log('\nSLIDER slide 1:', (await names()).join(' | '));
  await p.click('#attNext'); await p.waitForTimeout(900);
  console.log('SLIDER slide 2:', (await names()).join(' | '));
  console.log('  counter =', await p.textContent('#attNow'),
              '| rail fill =', await p.evaluate(()=>document.getElementById('attFill').style.height));
  await p.click('#attPrev'); await p.waitForTimeout(900);
  console.log('  back to slide', await p.textContent('#attNow'));
  await p.click('#attPP'); await p.waitForTimeout(300);
  console.log('  pause label =', await p.getAttribute('#attPP','aria-label'));
  console.log('  dots =', await p.$$eval('#attDots button',d=>d.length),
              '| current dot =', await p.$$eval('#attDots button',d=>d.findIndex(x=>x.getAttribute('aria-current')==='true')));

  const d=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth}));
  console.log('\nOverflow-X:', d.sw>d.cw+1?'YES':'no', '| JS errors:', errs.length?errs:'none');
  await b.close();
})();
