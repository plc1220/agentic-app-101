from html.parser import HTMLParser
from pathlib import Path
import json
class Parser(HTMLParser):
 def __init__(self):
  super().__init__();self.root={'tag':'root','attrs':{},'children':[]};self.stack=[self.root]
 def handle_starttag(self,t,a):
  n={'tag':t,'attrs':dict(a),'children':[]};self.stack[-1]['children'].append(n)
  if t not in ['br','img','hr','input','meta','link']: self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i]['tag']==t:self.stack=self.stack[:i];break
 def handle_data(self,d): self.stack[-1]['children'].append(d)
s=json.loads(Path('.pptx-build/source.json').read_text())
for x in s['slides']:
 p=Parser();p.feed(x['staticHtml']);x['tree']=p.root
Path('.pptx-build/source.json').write_text(json.dumps(s,ensure_ascii=False))
