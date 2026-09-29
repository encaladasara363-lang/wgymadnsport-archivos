const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:1123,height:794},deviceScaleFactor:2});
await p.goto('file://'+process.cwd()+'/plantilla-carteles-avisos.html',{waitUntil:'load'});await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:'carteles-avisos.pdf',width:'297mm',height:'210mm',printBackground:true,preferCSSPageSize:true});
await (await p.$('.hoja')).screenshot({path:'carteles-avisos.png'});await b.close();console.log('ok')})();
