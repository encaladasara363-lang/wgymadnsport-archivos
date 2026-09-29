const {chromium}=require('playwright');require('fs').mkdirSync(__dirname+'/salida',{recursive:true});
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:794,height:1123},deviceScaleFactor:2});
await p.goto('file://'+__dirname+'/carteles-avisos.html',{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:__dirname+'/salida/carteles-avisos.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
const hs=await p.$$('.hoja');for(let i=0;i<hs.length;i++)await hs[i].screenshot({path:`${__dirname}/salida/carteles-avisos-${i+1}.png`});
await b.close();console.log('ok')})();
