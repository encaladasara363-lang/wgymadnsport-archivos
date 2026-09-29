const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:794,height:1123},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/plantilla-carteles-avisos.html',{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:'carteles-avisos.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
const hs=await p.$$('.hoja');for(let i=0;i<hs.length;i++)await hs[i].screenshot({path:`carteles-avisos-${i+1}.png`});
await b.close();console.log('ok')})();
