#!/usr/bin/env node
/* Revisa todas las rutinas de rutinas/*.json: formato completo (validar-rutina.js)
   y que cada foto exista. Uso: node scripts/validar-rutinas.js
   Sale con error si encuentra algún problema (así lo marca GitHub). */
"use strict";
const fs=require("fs"),path=require("path");
const raiz=path.join(__dirname,"..");
const validarRutina=require(path.join(raiz,"validar-rutina.js"));
const dir=path.join(raiz,"rutinas");
let total=0;
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith(".json")).sort()){
 let r,problemas=[];
 try{r=JSON.parse(fs.readFileSync(path.join(dir,f),"utf8"))}
 catch(e){problemas.push("No es un JSON válido: "+e.message)}
 if(r){
  problemas=validarRutina(r);
  if(r.id&&r.id+".json"!==f)problemas.push("El \"id\" ("+r.id+") no coincide con el nombre del archivo.");
  (r.dias||[]).forEach((d,di)=>(d.exercises||[]).forEach((x,ei)=>(Array.isArray(x.img)?x.img:[]).concat(x.video?[x.video]:[],ei===0&&d.cooldownVideo?[d.cooldownVideo]:[]).forEach(p=>{
   if(typeof p==="string"&&!/^https?:/.test(p)&&!fs.existsSync(path.join(raiz,p.split("?")[0])))problemas.push("Día "+(di+1)+", ejercicio "+(ei+1)+": no existe el archivo "+p);
  })));
 }
 console.log((problemas.length?"✗ ":"✓ ")+f);
 problemas.forEach(p=>console.log("   - "+p));
 total+=problemas.length;
}
if(total){console.log("\n"+total+" problema(s). Corregir antes de publicar.");process.exit(1)}
console.log("\nTodas las rutinas están bien.");
