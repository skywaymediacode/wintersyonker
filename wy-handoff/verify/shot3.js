const { chromium } = require('playwright');
(async()=>{
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium',args:['--no-sandbox','--font-render-hinting=none']});
  const KILL='.rv{animation:none!important;opacity:1!important;transform:none!important}.marq-in{animation:none!important}';
  const f='Winters-Yonker-Homepage.html';
  for(const [w,h,n] of [[1440,1000,'desk'],[390,844,'mob']]){
    const ctx=await b.newContext({viewport:{width:w,height:h},isMobile:n==='mob',hasTouch:n==='mob'});
    const p=await ctx.newPage(); const e=[]; p.on('pageerror',x=>e.push(String(x)));
    await p.goto('file://'+process.cwd()+'/'+f,{waitUntil:'load'});
    await p.waitForTimeout(1800);
    await p.screenshot({path:`g-${n}-fold.png`});
    await p.addStyleTag({content:KILL}); await p.waitForTimeout(500);
    await p.screenshot({path:`g-${n}-full.png`,fullPage:true});
    const d=await p.evaluate(()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,sh:document.documentElement.scrollHeight}));
    console.log(n,'overflowX:',d.sw>d.cw+1?'YES '+d.sw+'>'+d.cw:'no','| h',d.sh,'| err',e.length?e:'none');
    await ctx.close();
  }
  await b.close();
})();
