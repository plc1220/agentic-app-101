import fs from 'node:fs';
import vm from 'node:vm';
const html=fs.readFileSync('docker-ai-cicd-workshop.html','utf8');
const slides=JSON.parse(html.match(/const SLIDES=(.*?);\n/)[1]);
const assets=JSON.parse(html.match(/const ASSETS=(.*?);\n/)[1]);
const refs=JSON.parse(html.match(/const REFS=(.*?);\n/)[1]);
const scope={}; vm.createContext(scope);
vm.runInContext(html.slice(html.indexOf('const esc='),html.indexOf('function initRefined'))+'\nthis.custom=CUSTOM_KINDS;this.render=renderRefined;',scope);
for(const s of slides){if(scope.custom.includes(s.kind))s.staticHtml=scope.render(s); else if(['containers','pipeline','rollback','finalquiz'].includes(s.kind))s.staticHtml=scope[s.kind]();else s.staticHtml=s.body;}
fs.writeFileSync('.pptx-build/source.json',JSON.stringify({slides,assets,refs}));
