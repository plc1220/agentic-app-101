"""Full-day teaching content. Keep slides concise; facilitator detail lives in notes."""
import html
import hashlib
import re
import base64
from pathlib import Path

SOURCES = {
 'sse': ('MDN: server-sent events', 'https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events'),
 'streams': ('MDN: readable streams', 'https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams'),
 'fastapi-responses': ('FastAPI responses', 'https://fastapi.tiangolo.com/advanced/custom-response/'),
 'deep-streaming': ('Deep Agents streaming', 'https://docs.langchain.com/oss/python/deepagents/streaming'),
 'react': ('ReAct paper', 'https://arxiv.org/abs/2210.03629'),
 'patterns': ('Agent workflow patterns', 'https://www.anthropic.com/engineering/building-effective-agents'),
 'ralph': ('Ralph: original description', 'https://ghuntley.com/ralph/'),
 'adk': ('Google ADK', 'https://google.github.io/adk-docs/'),
 'langgraph': ('LangGraph', 'https://docs.langchain.com/oss/python/langgraph/overview'),
 'deepagents': ('Deep Agents', 'https://docs.langchain.com/oss/python/deepagents/overview'),
 'deep-quickstart': ('Deep Agents quickstart', 'https://docs.langchain.com/oss/python/deepagents/quickstart'),
 'deep-backends': ('Deep Agents backends', 'https://docs.langchain.com/oss/python/deepagents/backends'),
 'crewai': ('CrewAI', 'https://docs.crewai.com/en/introduction'),
 'skills': ('Agent Skills', 'https://agentskills.io/what-are-skills'),
 'deep-skills': ('Deep Agents skills', 'https://docs.langchain.com/oss/python/deepagents/skills'),
 'mcp': ('MCP architecture', 'https://modelcontextprotocol.io/docs/learn/architecture'),
 'gemini': ('Gemini pricing', 'https://ai.google.dev/gemini-api/docs/pricing'),
 'genai': ('Google Gen AI SDK', 'https://googleapis.github.io/python-genai/'),
}
MODULES = {
 'A': ('09:00–09:30', 'Agent fundamentals', 30),
 'B': ('09:30–10:30', 'Architecture and data', 60),
 'C': ('10:45–12:00', 'Containers and project structure', 75),
 'D': ('13:00–14:15', 'Agent patterns and frameworks', 75),
 'E': ('14:30–15:10', 'Streaming chat and artifacts', 40),
 'F': ('15:10–15:50', 'Demo stack and walkthrough', 40),
 'G': ('15:50–16:35', 'System design exercise', 45),
 'H': ('16:35–17:00', 'Review and Q&A', 25),
}

def art(name, alt, css):
    data = base64.b64encode((Path(__file__).resolve().parent.parent / 'assets' / name).read_bytes()).decode()
    return f'<img class="{css}" src="data:image/png;base64,{data}" alt="{html.escape(alt, quote=True)}">'

def head(group, title, subtitle=''):
    return f'<div class="lesson-head"><div class="eyebrow"><span class="section-no">{group}</span>{MODULES[group][1]}</div><h2>{title}</h2>{f"<p class=lead>{subtitle}</p>" if subtitle else ""}</div>'
def takeaway(text, tag='Key point'):
    return f'<div class="takeaway"><span>{tag}</span>{text}</div>'
def cards(items):
    count={2:'two',4:'four'}.get(len(items),'')
    return '<div class="lesson-grid '+count+'">'+''.join(f'<article class="lesson-card"><span class="label">{a}</span><h3>{b}</h3><p>{c}</p>{f"<small>{d}</small>" if d else ""}</article>' for a,b,c,d in items)+'</div>'
def table(headers,rows,extra=''):
    return f'<table class="lesson-table {extra}"><thead><tr>'+''.join(f'<th>{x}</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{x}</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table>'
def flow(items):
    return '<div class="horizontal-flow">'+ '<div class="flow-arrow">→</div>'.join(f'<div class="flow-block"><span class="label">{a}</span><h3>{b}</h3><p>{c}</p></div>' for a,b,c in items)+'</div>'
def tasks(items):
    return '<ol class="task-list">'+''.join(f'<li><span>{i:02d}</span>{t}</li>' for i,t in enumerate(items,1))+'</ol>'
def code_pair(code, notes,tree=False):
    return f'<div class="dual-code"><pre class="{"tree" if tree else "codebox"}">{html.escape(code)}</pre><div class="code-notes">'+''.join(f'<div><h3>{a}</h3><p>{b}</p></div>' for a,b in notes)+'</div></div>'
def diagram(nodes,paths,description):
    # Nodes: x,y,w,h,label,sub,fill. Paths: SVG d; coordinates are authored to avoid crossing labels.
    out=f'<svg class="diagram-svg" viewBox="0 0 1144 330" role="img" aria-label="{html.escape(description,quote=True)}"><defs><marker id="arrow-{hashlib.sha256(description.encode()).hexdigest()[:12]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#4f8072"/></marker></defs>'
    for d in paths: out+=f'<path d="{d}" fill="none" stroke="#4f8072" stroke-width="2" marker-end="url(#arrow-{hashlib.sha256(description.encode()).hexdigest()[:12]})"/>'
    for x,y,w,h,label,sub,fill in nodes:
        out+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="#9eb8a9"/><text x="{x+w/2}" y="{y+29}" text-anchor="middle" font-size="22" font-weight="650" fill="#1b3b34">{html.escape(label)}</text><text x="{x+w/2}" y="{y+52}" text-anchor="middle" font-size="15" fill="#57736b">{html.escape(sub)}</text>'
    return out+'</svg>'

def expand(old,icon):
    out=[]
    def add(title,g,mins,body,note,theme='',sources=()):
        citations=''
        if sources:
            citations='<div class="sources-line">Reference: '+''.join(f'<a href="{SOURCES[k][1]}" target="_blank" rel="noreferrer">{SOURCES[k][0]} ↗</a>' for k in sources)+'</div>'
        out.append(dict(title=title,theme=theme,body=body+citations,note=f'{MODULES[g][0]} · {MODULES[g][1]} · {mins} minutes\n\n{note}'+('\n\nReferences: '+'; '.join(SOURCES[k][1] for k in sources) if sources else ''),group=g,minutes=mins))
    def reuse(idx,g,mins,extra=''):
        s=old[idx].copy();s.update(group=g,minutes=mins)
        s['note']=f'{MODULES[g][0]} · {MODULES[g][1]} · {mins} minutes\n\n'+s['note']+ ('\n\n'+extra if extra else '')
        s['body']=re.sub(r'<span class="section-no">\d+</span>',f'<span class="section-no">{g}</span>',s['body'])
        out.append(s)
    def exercise(title,g,mins,prompt,steps,deliver,note):
        add(title,g,mins,head(g,title)+f'<span class="timer">{mins} MIN · DISCUSS</span><p class="exercise-prompt">{prompt}</p>'+tasks(steps)+f'<div class="exercise-output">Output: {deliver}</div>',note,'exercise')
    def pause(title,period,mins,next_topic):
        out.append(dict(title=title,theme='break-card',body=f'<span class="label">BREAK</span><h2>{title}<br><em>{mins} minutes.</em></h2><p class="lead">Up next: {next_topic}</p><div class="break-time">{period}</div>',note=f'{period} · {mins} minutes. Resume on time; no setup tasks for participants.',group='break',minutes=mins))

    # A — 30 minutes
    reuse(0,'A',3,'Today is a full-day workshop. Ask participants to think of one repetitive information task they would like help with.')
    add('Workshop agenda','A',4,head('A','Workshop <em>agenda</em>')+'<div class="agenda">'+''.join(f'<div class="agenda-row"><time>{time}</time><div><strong>{name}</strong><small>{sub}</small></div></div>' for time,name,sub in [
        ('09:00–10:30','Agent fundamentals','The agent idea, architecture and data'),('10:45–12:00','Application architecture','Containers and project structure'),('13:00–14:15','Agent frameworks','Execution patterns, frameworks, skills and MCP'),('14:30–15:10','Streaming UI','Chat, progress and artifacts'),('15:10–15:50','Demo walkthrough','Stack, setup and reliability'),('15:50–16:35','System design','Document assistant architecture'),('16:35–17:00','Review and Q&A','Knowledge check and discussion')])+'</div>'+takeaway('Breaks at 10:30 and 14:15. Lunch from 12:00 to 13:00.','Schedule'),'Explain the rhythm: short talks, examples, pair discussions and a capstone. Nobody needs to install software. Ask participants to return at the listed times. Use the slide overview to jump to a module if discussion runs long.')
    add('Learning objectives','A',5,head('A','Learning <em>objectives</em>')+cards([('01','Application architecture','Show how a question reaches the AI and its tools.',''),('02','Technology selection','Recognize storage, framework and integration choices.',''),('03','Code walkthrough','Know which file to change and which secret to keep private.','')]),'Invite participants to choose the outcome that is least familiar. Define repo as a folder whose changes Git tracks; API as an interface software uses to request a service. Gather two participant use cases for later discussion.')
    add('Chat, workflow or agent','A',7,head('A','Chatbots, workflows<br>and <em>agents</em>')+cards([('CHAT','Generate an answer','“Rewrite this message politely.”','The main result is text.'),('WORKFLOW','Follow known steps','“Validate a form, save it, send a receipt.”','The path is defined in code.'),('AGENT','Choose useful steps','“Find the right session and explain when it starts.”','The model may select a tool.')])+takeaway('Many real apps combine fixed steps with model decisions.'),'Ask the group to classify a receipt email and a research assistant. Explain that an agent still runs inside programmed limits. A workflow can call an LLM, and an agent can follow a mostly fixed workflow. These categories help choose control flow; they are not a ranking.')
    reuse(1,'A',6,'Show the question first. Ask “where should the answer come from?” Then discuss why an approved schedule lookup beats relying on model knowledge for a changing timetable.')
    exercise('Exercise: define a use case','A',5,'Think of one task from your own work.', ['Name the person asking for help.','Describe the useful output in one sentence.','Name one source the assistant should consult.'],'a one-sentence use case.','Allow two minutes alone, two minutes in pairs and one minute for examples. Prefer bounded jobs: find a policy, summarize a document, check a status. If someone proposes running an entire department, narrow it to one useful decision.')

    # B — 60 minutes
    add('Application components','B',7,head('B','Application <em>components</em>')+diagram([
        (10,90,240,100,'Frontend','User input and rendering','#d9e9f0'),(310,90,240,100,'Backend API','Requests and authorization','#d3ead7'),(610,90,240,100,'Agent runtime','Model calls and tool loop','#fbd8c9'),(910,90,230,100,'Tool functions','Execute allowed operations','#f1dfa5')
    ],['M250 122H308','M550 122H608','M850 122H908','M910 161H852','M610 161H552','M310 161H252'],
    'Connected application components. Requests and tool calls move from frontend to API, agent runtime and tools; results return in the other direction.')+
    '<p class="diagram-caption">Requests and actions → &nbsp; ← Results and status updates</p>'+takeaway('The backend runs application logic, holds credentials and enforces authorization.','Backend'),
    'Use the connected boxes to follow the request and then the result. The agent runtime is normally part of the backend; it is shown separately here as a responsibility. The frontend renders events and results rather than executing privileged tools. A terminal can be the user interface in a small demo. The next slide adds model and data services; the streaming chapter explains ongoing updates.')
    add('A typical agentic app architecture','B',10,head('B','Agentic application<br><em>architecture</em>')+diagram([
        (0,10,230,70,'Browser / chat','User interface','#d9e9f0'),(300,10,230,70,'API','Identity and requests','#d3ead7'),(600,10,230,70,'Agent runtime','Instructions and tool loop','#fbd8c9'),(914,10,230,70,'Model API','Gemini','#f1dfa5'),
        (450,133,240,70,'Tools / services','Authorized data access','#d3ead7'),
        (0,256,250,70,'Database','Messages and run status','#e4ece0'),(298,256,250,70,'Cache','Repeated lookups; expiry','#f1dfa5'),(596,256,250,70,'Object storage','Uploads and artifacts','#e4ece0'),(894,256,250,70,'File storage','Workspace files and paths','#e4ece0')
    ],['M230 45H298','M530 45H598','M830 45H912','M715 80V108H570V131','M570 203V229H125V254','M570 229H423V254','M570 229H721V254','M721 229H1019V254'],
    'Browser connects to API, agent runtime and model API. Authorized tools and services access a database, cache, object storage and file storage.')+
    '<p class="diagram-caption">Logical components · cache is optional; durable records remain in the database or storage.</p>',
    'Follow a request across the top. Tool and application service code controls access to data. The cache may hold repeated lookup results with an expiry; access and cache keys must respect the user and data version. Database records include conversation and run status; object storage holds uploaded files and artifacts; file storage provides workspace paths. These are logical responsibilities, not a requirement for one server each. The streaming chapter later explains the event path back to the browser and how artifacts are rendered.')
    add('Request lifecycle','B',7,head('B','Request <em>lifecycle</em>')+flow([('1 / RECEIVE','Check the caller','The app accepts the question.'),('2 / DECIDE','Ask the model','Offer the approved tools.'),('3 / EXECUTE','Run a tool','Validate inputs and fetch data.'),('4 / RETURN','Explain the result','Show the answer and its source.')])+takeaway('Progress messages can show which stage the app has reached.'),'Use a participant as the user, another as the model and another as the tool. Pass a question card along the four stages. The model suggests a tool call; ordinary application code executes it. Show that an answer may take multiple model calls.')
    reuse(3,'B',8,'Add the difference between file storage and object storage: folders and file operations versus blobs addressed by keys. File storage can be durable. An agent workspace is often temporary by choice, not because all file storage is temporary.')
    add('Document processing pipeline','B',8,head('B','Document processing<br><em>pipeline</em>')+flow([('UPLOAD','Keep the original','PDF in object storage.'),('REGISTER','Record ownership','Database row: owner + file key.'),('PROCESS','Work on a copy','Extract text in a workspace.'),('DELIVER','Save the result','Report file + completed status.')])+takeaway('Set a retention period for originals, working files and results.'),'Use a fictional invoice. The database row references the object; it need not contain the whole PDF. Working text may be deleted after processing or retained if justified. A cache could store repeated lookups but should not become the only copy of important records.')
    add('Retrieval-augmented generation (RAG)','B',7,head('B','Retrieval-augmented<br><em>generation (RAG)</em>')+flow([('QUESTION','Find relevant text','Search approved documents.'),('CONTEXT','Bring back excerpts','Include the source and version.'),('ANSWER','Explain with evidence','Give a source the user can open.')])+takeaway('This pattern is often called RAG: retrieval-augmented generation.','Vocabulary'),'Explain retrieval with a handbook. Embeddings are numeric representations that can help find similar text; they are one search option. Keyword or database search can be enough for a small corpus. Retrieval does not retrain the model and does not guarantee a correct answer. Check permissions before supplying excerpts.')
    exercise('Exercise: select storage','B',8,'A document assistant has six pieces of information.', ['A user ID and the status of a processing job.','The original PDF and the finished report.','Temporary extracted text and a repeated vendor lookup.'],'a storage choice and a reason for each item.','Use pairs: five minutes to sort, two minutes to share, one minute to highlight uncertainty. Ask which items must survive a restart and which can be recreated. The next slide contains a suggested answer.')
    add('Storage exercise: suggested answer','B',5,head('B','Storage selection:<br><em>suggested answers</em>')+table(['Information','Starting choice','Why'],[('User ID + job status','Database','Structured records that need queries.'),('PDF + finished report','Object storage','Durable file objects with access controls.'),('Extracted working text','Temporary workspace','Scratch data with a cleanup policy.'),('Repeated vendor lookup','Cache with expiry','A speed-up backed by an authoritative source.')]),'Invite alternatives. Extracted text can be durable if it will be reused. A small prototype might use a local file rather than object storage. Reward reasoning about lifetime and access rather than insisting on a vendor product.')
    pause('Morning break','10:30–10:45',15,'how the code is packaged and organized.')

    # C — 75 minutes
    add('Frontend and backend responsibilities','C',5,head('C','Frontend and backend<br><em>responsibilities</em>')+cards([('FRONTEND','User interface','Collect a question. Show progress. Display results. Ask for confirmation.','Browser code is visible to its user.'),('BACKEND','Application logic','Validate requests. Hold provider credentials. Run tools. Store records.','Put authorization at the server boundary.')])+takeaway('An API is the agreed interface between these parts.'),'Explain why a provider API key should not be shipped in browser JavaScript. The starter keeps it in a local environment file and runs Python locally. A hosted app instead loads its own server-side credential. The browser should not be allowed to grant itself extra tool permissions.')
    reuse(4,'C',6)
    add('Docker Compose architecture','C',7,head('C','Docker Compose<br><em>architecture</em>')+diagram([
        (0,24,180,76,'Browser','Chat and previews','#d9e9f0'),(240,24,230,76,'Web container','Serves frontend assets','#d9e9f0'),(540,24,230,76,'API container','HTTP and streaming','#d3ead7'),(870,24,270,76,'Agent container','Worker and tool execution','#fbd8c9'),
        (0,244,240,72,'PostgreSQL','Persistent volume','#e4ece0'),(300,244,240,72,'Redis','Cache; separate job/events','#f1dfa5'),(600,244,250,72,'Storage','Objects and file volume','#e4ece0'),(900,244,240,72,'Gemini API','External provider','#f1dfa5')
    ],['M180 62H238','M470 62H538','M770 48H868','M870 78H772','M655 100V170H120V242','M655 170H420V242','M1005 100V170H725V242','M1005 170H1020V242','M1005 145H420V242'],
    'Browser uses the web container, which proxies requests to an API container. The API starts work in an agent container and receives events. Database, Redis and storage are supporting services; Gemini is external.')+
    '<p class="diagram-caption">API ↔ agent: job requests and events · Redis cache, queue and event data use separate policies.</p>',
    'This is a proposed Compose design, not a shipped runnable stack. The web service serves frontend assets and proxies API requests. The API authenticates requests, manages run records and streams events. The agent service runs work and emits progress. API-to-agent traffic may use internal HTTP or Redis jobs/events; the arrows show logical communication. The API and worker may both access supporting data services as required. Cache entries can expire; a reliable queue or event log needs its own retention and persistence policy. Separating containers supports independent deployment, but a small app can run the API and agent in one process. Database and file volumes survive container replacement. Object storage can be an external service.')
    add('Reference full-stack technologies','C',5,head('C','Reference <em>full-stack design</em>')+table(['Layer','Example technology','Responsibility'],[
        ('Web','React + TypeScript','Chat, streaming updates and artifact preview.'),('API','FastAPI + Uvicorn','Authentication, run endpoints and event streams.'),('Agent','Python + Deep Agents + Gemini','Model calls, tool execution and workflow state.'),('Data','PostgreSQL · Redis · object/file storage','Durable records, cache, jobs and file outputs.'),('Deployment','Docker Compose','Local containers, networks and volumes.')
    ],'event-table')+'<p class="mini-note">Reference design · the runnable demo stack is introduced in the demo chapter.</p>',
    'Explain each layer using the preceding container diagram. This is a proposed extension with example technologies; these packages and services are not installed by run.sh. The existing runnable app is a Python terminal program. React runs in the browser after assets are served. Uvicorn serves the FastAPI application. Deep Agents is the reference framework discussed in the workshop, but the included demo uses Google’s SDK directly. Redis can support several responsibilities, provided cache expiry is not accidentally used for durable jobs. The exact integration, versions and deployment still need implementation.',sources=('fastapi-responses','deepagents'))
    add('Synchronous requests and background jobs','C',7,head('C','Synchronous requests<br>and <em>background jobs</em>')+cards([('SHORT TASK','Wait for the result','Question → API → answer. Stream text or progress while waiting.','Good for a small lookup.'),('LONG TASK','Track a job','Submit → job ID → worker → saved result. The screen checks progress.','Good for processing a large document set.')])+takeaway('A queue organizes work. A cache speeds up access. Their jobs differ.'),'Explain the queue as a numbered ticket. The request can return before work is finished. A worker process takes a ticket and performs the job. The database holds durable job status so refreshing the browser does not lose it. Avoid introducing queue vendor details.')
    add('Example project structure','C',10,head('C','Example <em>project structure</em>')+code_pair('agentic-app/\n├── frontend/       # user interface\n├── backend/\n│   ├── api/        # requests\n│   ├── agent/      # agent configuration\n│   ├── tools/      # callable functions\n│   └── services/   # data access\n├── skills/         # skill definitions\n├── evals/          # evaluation cases\n├── infra/          # deployment configuration\n├── .env.example    # environment variables\n└── README.md       # setup instructions',[('Application components','Separate the user interface, API, agent logic and data access.'),('Configuration','Store environment variable names in .env.example and credentials outside Git.'),('Example directories','Directory names vary by project and framework.')],True),'Walk the tree slowly. Ask where to change a button, add a lookup, or alter an instruction. Explain services as ordinary code that talks to a database or API. Point to typical-app-scaffold.md for a more detailed map. Show that a small app can combine files initially; folders are for clarity rather than compliance.')
    add('Mapping the demo to application components','C',8,head('C','Demo code →<br><em>application components</em>')+table(['In run_agent.py','In a larger app','Purpose'],[('input() and print()','Frontend and API','Collect questions and show results.'),('System instruction + model call','Agent configuration','Configure the model and control loop.'),('find_workshop_session()','Tool functions','Expose a bounded capability.'),('SESSIONS sample dictionary','Data access and database','Retrieve authoritative data.')]),'Open the real script and point to these four parts. Make clear this is a mapping, not a claim that those folders exist in the starter. A refactor changes organization while retaining the behavior. A browser frontend requires an API layer that the terminal sample does not need.')
    add('Tool definition','C',7,head('C','Tool <em>definition</em>')+code_pair('Tool: find_workshop_session\n\nInput\n  topic: "backend"\n\nOutput\n  time: "9:30 AM"\n  topic: "Backend basics"\n\nIf no match\n  return a clear not-found result',[('Name and description','Explain when to use it.'),('Input and output','Give arguments and results a predictable shape.'),('Limits and permissions','Validate the request before accessing real data.')]),'A docstring is part of what the SDK can expose to the model. A tool description is not an authorization mechanism. Validate arguments, handle missing records and return a useful error. Avoid giving a model unrestricted query strings or arbitrary shell execution for a lookup task.')
    add('Configuration and credentials','C',5,head('C','Configuration and<br><em>credentials</em>')+cards([('SETTING','Which model?','GEMINI_MODEL selects the model for this example.','Availability changes; use a supported model.'),('SECRET','Who may call it?','GEMINI_API_KEY is your local credential.','Keep it outside Git.'),('DOCUMENTATION','How do I begin?','.env.example lists names and placeholders. README explains setup.','A project ID is not a credential.')]),'Explain the difference between a configuration value and a secret. A free-tier key inherits the associated project’s tier and quota. Do not change an existing project’s billing during the workshop. Show only placeholders, never a real key.')
    exercise('Exercise: application components','C',10,'Identify the application component responsible for each change.', ['“Make the progress message clearer.”','“Add a customer order lookup.”','“Keep completed job results after restart.”','“Check that unknown questions do not get invented answers.”'],'a component and a reason for each change.','Six minutes in pairs, three minutes to compare, one minute to surface alternate designs. People can answer using the diagram without reading Python.')
    add('Application components: suggested answers','C',5,head('C','Application components:<br><em>suggested answers</em>')+table(['Change','Component','Related components'],[('Clearer progress message','Frontend','API response format'),('Customer order lookup','Tool function','Data access and authorization'),('Durable job results','Data persistence','Database schema and migration'),('Unknown-question check','Evaluation','Agent instructions and tool errors')]),'Point out that useful changes often cross boundaries. Folder structure helps ownership but does not remove integration work. An evaluation is a realistic example with an expected outcome, not merely a test that the function returns something.')
    pause('Lunch','12:00–13:00',60,'agent patterns, frameworks, skills and MCP.')

    # D — 75 minutes
    add('Model, SDK, framework and runtime','D',4,head('D','Model, SDK,<br>framework and <em>runtime</em>')+table(['Term','Role','Example'],[('Model','Interprets the prompt and produces output','Gemini'),('SDK','Code library for calling a service','Google Gen AI SDK'),('Framework / harness','Organizes tools, instructions and agent behavior','ADK or Deep Agents'),('Runtime','Executes steps and manages execution state','LangGraph')]),'Our runnable script uses the Google SDK and automatic function calling. It is not currently a Deep Agents app. These categories overlap in products; use them to explain responsibilities. The model choice and the framework choice are separate decisions.')
    # Execution patterns — 25 minutes, before framework selection.
    add('ReAct: reason, act, observe','D',6,head('D','ReAct: reason,<br>act, <em>observe</em>')+diagram([
        (10,40,240,76,'Reason','Select the next step','#d3ead7'),
        (340,40,230,76,'Act','Application runs a tool','#fbd8c9'),
        (670,40,240,76,'Observe','Read the tool result','#d9e9f0'),
        (670,235,240,70,'Answer','Return a supported result','#f1dfa5')
    ],['M250 78H338','M570 78H668','M790 116V233','M790 116V174H130V118'],
    'Reason, act using a tool, and observe the result. Continue the loop if more information is needed, or return an answer.')+
    '<p class="diagram-caption">Example: find a report → read a section → answer with a source.</p>',
    'ReAct interleaves reasoning, actions and observations. Trace the return arrow when the first search result is insufficient; take the answer branch when evidence is sufficient. The application executes the tool and enforces access. Explain the decision at a high level; do not imply that internal reasoning must be displayed. The existing Gemini SDK demo illustrates a tool-call exchange, but it does not implement the original ReAct prompting method. Connect this diagram to the agent component in the architecture slide.',sources=('react',))
    add('Plan-and-execute','D',4,head('D','Plan-and-<em>execute</em>')+diagram([
        (5,50,230,76,'Plan','Break the task into steps','#d3ead7'),
        (310,50,230,76,'Execute','Run the next step','#fbd8c9'),
        (615,50,230,76,'Review','Check progress and evidence','#d9e9f0'),
        (915,50,220,76,'Complete','Return the result','#f1dfa5')
    ],['M235 88H308','M540 88H613','M845 88H913','M730 126V225H425V128','M730 225V280H120V128'],
    'Create a plan, execute a step, and review progress. Continue with the next step, revise the plan, or complete the task.')+
    '<p class="diagram-caption">Example plan: read three reports → compare findings → draft a briefing.</p>',
    'Walk through the document assistant. Planning is useful when a task has several dependent steps. The short return path runs another step; the longer path revises the plan when evidence changes. A plan can be represented as a task list or structured state. Fixed steps can also be ordinary workflow code. This is a general pattern, not a claim that every framework supplies the same planner API. An execution step may itself use a ReAct-style loop.',sources=('patterns',))
    add('Evaluator–optimizer','D',4,head('D','Evaluator–<em>optimizer</em>')+diagram([
        (20,55,260,76,'Generate','Produce a draft','#d3ead7'),
        (415,55,280,76,'Evaluate','Check against criteria','#d9e9f0'),
        (865,55,250,76,'Accept','Return the draft','#f1dfa5'),
        (415,235,280,70,'Feedback','Identify required changes','#fbd8c9')
    ],['M280 93H413','M695 93H863','M555 131V233','M415 270H150V133'],
    'Generate a draft, evaluate it against criteria, and accept it or return feedback for another draft.')+
    '<p class="diagram-caption">Example criteria: required sections, source references and no unsupported claims.</p>',
    'Apply this to a document briefing draft. A validator can check required fields, while a model or person can assess less mechanical criteria. Model evaluation is fallible, especially when generator and evaluator share blind spots. Use known examples to assess the evaluator. Set a revision limit and return unresolved issues when it is reached. Passing evaluation prepares a draft for review; it does not authorize publication.',sources=('patterns',))
    add('Multi-agent orchestration','D',4,head('D','Multi-agent <em>orchestration</em>')+diagram([
        (10,120,255,76,'Orchestrator','Assign bounded tasks','#d3ead7'),
        (435,20,260,76,'Agent A','Summarize report A','#d9e9f0'),
        (435,235,260,76,'Agent B','Summarize report B','#d9e9f0'),
        (870,120,255,76,'Synthesis','Compare and cite sources','#f1dfa5')
    ],['M265 158H345V58H433','M345 158V273H433','M695 58H775V158H868','M695 273H775V158'],
    'An orchestrator assigns separate report summaries to two agents. Their results are combined into one comparison.')+
    '<p class="diagram-caption">Define each agent’s task, allowed tools and expected output.</p>',
    'Replace the earlier brief orchestration slide with this concrete example. Explain sequence, routing and delegation verbally: sequence follows ordered steps, routing selects a specialist, delegation assigns work and combines results. Independent report summaries may run in parallel. Each worker may have its own tool loop. For three short reports, one agent may be sufficient; delegation adds coordination, model calls and failure cases. The synthesis step must preserve sources and handle missing worker results.',sources=('patterns',))
    add('Ralph loop: repeated agent runs','D',4,head('D','Ralph loop:<br><em>repeated agent runs</em>')+diagram([
        (10,45,245,76,'Load task state','Read specs, plan and files','#d3ead7'),
        (335,45,235,76,'Run coding agent','Implement one task','#fbd8c9'),
        (650,45,235,76,'Validate','Run relevant checks','#d9e9f0'),
        (650,235,235,70,'Save progress','Update files and plan','#f1dfa5')
    ],['M255 83H333','M570 83H648','M767 121V233','M650 270H130V123'],
    'An outer loop starts a coding agent with persisted task state. The agent implements a task, validates its work and saves progress for a subsequent run.')+
    '<p class="diagram-caption">Outer loop: repeated agent runs. Inner loop: model calls and tool execution.</p>',
    'Keep this as a reference example for building the document assistant, rather than the assistant’s normal document-processing flow. Geoffrey Huntley describes Ralph as a technique whose simplest form is a shell loop repeatedly invoking a coding agent. Files, specifications and the plan carry progress between runs. The diagram expands the work performed during an iteration; implementations vary. The original minimal loop does not provide a completion guarantee or automatic stop condition. A run may contain ReAct-style tool use. Use the controls on the next slide for a bounded implementation; do not demonstrate an unbounded shell loop.',sources=('ralph',))
    add('Completion criteria and execution limits','D',3,head('D','Completion criteria<br>and <em>execution limits</em>')+table(
        ['Control','Document assistant example'],[
        ('Completion criteria','Draft contains the requested sections and source references.'),
        ('Execution limits','Cap model calls, revisions, elapsed time and API usage.'),
        ('Failure handling','Stop on repeated failures and report missing evidence.'),
        ('Human approval','Require review before publishing or changing external records.')
    ]),
    'Close the pattern section by asking where the stop decision belongs. Application code should enforce budgets and permissions. Model assertions of completion are not sufficient evidence. A run may finish with a partial result or a request for human input. Transition: an execution pattern describes the flow; a framework supplies tools for implementing it. Frameworks can support several patterns, and a single application can combine patterns. Revisit these controls in the capstone.')
    add('Frameworks: side-by-side comparison','D',7,head('D','Agent framework<br><em>comparison</em>')+table(['Aspect','Google ADK','LangGraph','Deep Agents','CrewAI'],[
        ('Mental model','Agents and workflows','A graph of steps','An agent with more built-in task support','Roles, tasks and flows'),
        ('Strong fit*','Google-oriented apps and integrations','Explicit paths and resumable state','Longer tasks with files and delegation','Teams organized around responsibilities'),
        ('What you design','Tools, instructions and workflow','State, nodes and transitions','Tools, backends and allowed capabilities','Roles, task boundaries and flow'),
        ('Remember','Can use non-Google models','Lower-level execution control','Uses LangChain + LangGraph','Coordination still needs evaluation')
    ],'framework-table')+'<p class="framework-small">*Workshop fit guidance, not a benchmark or an exhaustive feature matrix.</p>','Allow about one minute per framework, then compare tradeoffs and take questions. These are overlapping approaches, not mutually exclusive capabilities. Match the app and team to the approach. None removes the need for authentication, data ownership, deployment or checks. Python Deep Agents is distinct from the community TypeScript deepagentsdk demo discussed earlier.',sources=('adk','langgraph','deepagents','crewai'))
    add('Framework selection','D',3,head('D','Framework <em>selection</em>')+''.join(f'<div class="decision-row"><div>{a}</div><span>→</span><div>{b}</div></div>' for a,b in [ ('One small tool lookup','Direct SDK may be enough'),('Must follow explicit branches','Consider a graph workflow'),('Need longer file-based tasks','Consider a Deep Agents harness'),('Team already uses Google tooling','Evaluate ADK integration fit')]),'These are facilitator recommendations, not exclusive product claims. A framework is useful when it reduces repeated work and improves control. Do not choose based only on a feature checklist or a popular name. Ask what people on the team can maintain.')
    add('Where Deep Agents fits','D',3,head('D','Deep Agents<br><em>architecture</em>')+'<div class="stack-bars"><div class="stack-bar"><strong>Your application</strong><span>Frontend · authentication · business rules</span></div><div class="stack-bar"><strong>Deep Agents</strong><span>Task-oriented agent harness</span></div><div class="stack-bar"><strong>LangChain</strong><span>Agent and tool building blocks</span></div><div class="stack-bar"><strong>LangGraph</strong><span>Execution and state</span></div><div class="stack-bar"><strong>Model + data services</strong><span>Gemini and your systems</span></div></div>','Think of nested responsibilities, not five separate machines. Deep Agents builds on LangChain and uses LangGraph. Your app still owns identity and data access. Do not present the starter SDK script as using this stack.',sources=('deepagents',))
    add('Deep Agents capabilities','D',4,head('D','Deep Agents<br><em>capabilities</em>')+cards([('FILES','Keep working material','Use a configured filesystem backend.','Choose where files actually live.'),('DELEGATION','Split focused tasks','Subagents can handle parts of the work.','Extra steps can add time and cost.'),('PLANNING','Track a task list','Enable planning when it helps the job.','Current v0.7+ docs make planning opt-in.')]),'Version behavior matters. Explain capabilities conceptually rather than teaching all configuration options. A virtual filesystem can be backed by memory, disk or another store; it does not imply a secure execution sandbox. Inspect installed-version docs before adapting production code.',sources=('deepagents','deep-backends'))
    add('Deep Agents configuration','D',4,head('D','Deep Agents<br><em>configuration</em>')+code_pair('agent = create_deep_agent(\n    model=gemini_model,\n    tools=[lookup_session],\n    system_prompt=(\n        "Use the schedule tool. "\n        "Say when information is missing."\n    ),\n)\n\nagent.invoke({"messages": [\n    {"role": "user", "content": question}\n]})',[('Model','A configured model connection.'),('Tools','The capabilities you expose.'),('Instructions','How the assistant should approach the task.')])+'<p class="mini-note">Code excerpt · model setup omitted</p>','This is deliberately a reading exercise, not copy-and-run code. Explain that Gemini can be configured through a compatible model integration. The actual runnable file stays run_agent.py and uses Google’s SDK.',sources=('deep-quickstart',))
    add('Skills, tools and MCP','D',3,head('D','Skills, tools and <em>MCP</em>')+table(['Concept','Role','Example'],[('Skill','A reusable guide for doing a task','How to summarize a report in a chosen format.'),('Tool','A capability the app can execute','Fetch an approved document.'),('MCP server','A program exposing capabilities through a standard protocol','A document service with search and read operations.')]),'The skill is guidance, the tool is an operation, and MCP is an integration interface. They can work together. A skill may include scripts and resources, but the app still decides how those run. MCP does not itself make a data source trustworthy or provide unlimited access.',sources=('skills','mcp'))
    add('Agent Skills','D',4,head('D','Agent <em>Skills</em>')+code_pair('skills/\n└── summarize-report/\n    ├── SKILL.md\n    ├── references/\n    │   └── style-guide.md\n    └── scripts/\n        └── format_output.py',[('What it contains','When to use it, steps to follow, and supporting material.'),('How it helps','Relevant instructions can be loaded when needed.'),('What to check','Review the source, any scripts, and the permissions they need.')],True),'Skills package task guidance and supporting assets. The host/framework decides how it discovers and loads them. Loading skill instructions does not grant new permissions or replace the model. Compatibility and supported behavior differ across hosts.',sources=('skills','deep-skills'))
    add('Model Context Protocol (MCP)','D',5,head('D','Model Context Protocol<br><em>(MCP)</em>')+diagram([(5,115,235,76,'AI application','The host','#d9e9f0'),(310,115,215,76,'MCP client','Connection component','#d3ead7'),(610,115,230,76,'MCP server','Local or remote program','#fbd8c9'),(909,40,225,70,'Documents','Approved content','#e4ece0'),(909,232,225,70,'Business API','Allowed operations','#e4ece0')],['M240 153H308','M525 153H608','M840 153H870V75H907','M870 153V267H907'],'An AI application uses an MCP client to connect to a local or remote MCP server, which exposes selected data or operations.')+'<p class="diagram-caption">Servers may expose tools, resources and prompt templates. Access still needs appropriate authorization.</p>','MCP is the protocol, and the server is software implementing it. The server may run on the same computer or remotely. It can provide more than tools: resources supply context and prompts provide templates. Avoid teaching protocol mechanics here.',sources=('mcp',))
    add('Example: skills and MCP tools','D',3,head('D','Example: skills and<br><em>MCP tools</em>')+flow([('SKILL','Summarize clearly','Use sections: purpose, findings, next steps.'),('TOOL VIA MCP','Read the document','Fetch only the document the user may access.'),('AGENT','Write a draft','Use the evidence and the requested format.')])+takeaway('The skill guides the work. The tool supplies data. The app controls access.'),'An application can call an ordinary local function without MCP. MCP is useful for reusable connections across compatible clients. The document remains input data; embedded instructions in it should not override application policy. This is a design example, not an installed integration.')
    add('Additional concepts','D',3,head('D','Additional <em>concepts</em>')+table(['Term','What it usually means','First question to ask'],[('Memory','Information retained across runs or turns','What is saved, for whom and for how long?'),('RAG / retrieval','Find relevant evidence before answering','Are sources current and permitted?'),('Sandbox','A restricted execution environment','Which files, network and processes can it reach?'),('Observability','Logs and traces of what happened','Can we see tool failures and run cost?')]),'These terms describe needs or patterns, not things every beginner app must install. A container alone is not proof of safe untrusted-code execution. A log should avoid credentials and unnecessary personal data. Use the reference handout for links and definitions.')
    exercise('Choose an approach','D',4,'A team needs an assistant that reads several reports and drafts a comparison.', ['Which execution pattern and framework would you start with?','Would a skill help keep the report format consistent?','Would you use a local function or an existing MCP connection for documents?'],'one choice, one tradeoff, and one thing to verify.','There is no unique correct framework. A reasonable answer might evaluate Deep Agents for long tasks, use a comparison-writing skill, and reuse an authorized document connector. ADK or a graph can also fit depending on the team. Assess the reasoning, not the logo.')
    add('Framework selection criteria','D',3,head('D','Framework selection<br><em>criteria</em>')+cards([('TEAM','Can we maintain it?','Language, familiar patterns and deployment options.',''),('TASK','Can we control it?','Required paths, tools, approvals and state.',''),('EVIDENCE','Does it work for us?','Run representative examples and inspect failures.','')]),'Close the framework discussion by asking which evidence would change the team’s mind. Small representative trials are more informative than a long feature list. Keep the chosen approach minimal and add integrations when they solve a real need.')
    pause('Afternoon break','14:15–14:30',15,'streaming chat, artifact rendering and the demo.')

    # E — 40 minutes
    from streaming_chapter import add_streaming
    add_streaming(add, head, diagram, table, flow, cards, takeaway, art)

    # F — 40 minutes
    add('Runnable demo stack','F',5,head('F','Runnable demo <em>stack</em>')+table(['Layer','Included technology','What it does'],[
        ('Interface','Terminal: input() / print()','Accept a question and display the complete answer.'),('Runtime','Python 3.10+','Run the local program.'),('Model integration','google-genai → Gemini Developer API','Call Gemini and handle Python tool calls.'),('Configuration','python-dotenv + .env','Load the API key and model setting.'),('Data and tool','SESSIONS + find_workshop_session()','Read a fixed in-memory timetable.')
    ],'event-table')+'<p class="mini-note">Launch scripts create .venv and install requirements.txt.</p>',
    'The stack shown here is what attendees receive. It has no browser UI, web API, database server, container runtime or Deep Agents dependency. It uses automatic function calling and prints the completed response rather than token streaming. Explain Python as the runtime and pip packages as dependencies. The launcher manages a local virtual environment so users do not need to activate it manually. A working internet connection, a valid key and access/quota for the configured model are required. The repository currently has no public remote; distribute the folder or publish a real URL before asking people to clone.')
    reuse(5,'F',3)
    add('Read the actual starter','F',4,head('F','Four parts<br>of <em>run_agent.py.</em>')+table(['Part','What to look for','What it does'],[('Configuration','load_dotenv() and GEMINI_MODEL','Loads local settings.'),('Sample data','SESSIONS and ALIASES','Stores the fictional timetable.'),('Tool','find_workshop_session()','Looks up a matching topic.'),('Loop','input() → generate_content() → print()','Sends a question and displays the result.')]),'Open the file on the presenter’s screen; do not ask attendees to type. Walk through it from top to bottom without explaining every Python token. The sample schedule is fictional and is not the timing plan for today. Tool matching is basic; use unknown-query behavior as a discussion point.')
    reuse(7,'F',4,'The model configured in .env must still be available. Check the key’s actual project tier before any API call. Free-tier access is not guaranteed for an existing billed project. Do not promise one request per answer because automatic function calling may involve several.')
    reuse(6,'F',5,'If a live API run has not been rehearsed, use the labelled example output and walk the code. The slide is not evidence that the API has been tested.')
    add('Demo test cases','F',4,head('F','Demo <em>test cases</em>')+table(['Question','What we expect','What it teaches'],[('When is the backend session?','Look up the stored session.','A useful tool call.'),('When is the quantum computing session?','Say there is no matching record.','Avoid invented timetable facts.'),('What about the session after that?','A follow-up may lack context.','The sample starts each turn fresh.')]),'Use fixed sample inputs. If the tool gives a bad match, explain the matching limitation rather than attributing everything to the model. Missing credentials, unavailable model and quota errors are environment cases. Never claim a successful run if only the transcript was shown.')
    add('Tool permissions and approval','F',4,head('F','Tool permissions<br>and <em>approval</em>')+cards([('READ','Look up a status','Check the user is allowed to see the record.','Use a bounded read-only tool.'),('DRAFT','Prepare a change','Show the proposed content or action.','Let a person review it.'),('COMMIT','Apply the change','Require the appropriate authorization and record the outcome.','Avoid repeating an action accidentally.')])+takeaway('A prompt is guidance. Application code enforces permissions.'),'Use an email example: finding an address, drafting an email, and sending it are different actions. For writes, retries need duplicate prevention. Mention idempotency as an optional word meaning repeated requests do not repeat a side effect. The starter is read-only.')
    add('Agent evaluation','F',4,head('F','Agent <em>evaluation</em>')+table(['Check','Example question','Useful evidence'],[('Correctness','Did it use the stored session time?','Compare against known data.'),('Honesty','Did it admit a missing session?','No invented schedule entries.'),('Boundaries','Did it stay within its allowed tool?','Tool/event trace.'),('Experience','Was it understandable and timely?','Answer clarity and elapsed time.')]),'Ask groups to propose one additional example. A small evaluation set can include known, unknown, ambiguous and malformed inputs. Record model/config changes and compare results. An answer sounding confident does not establish correctness.')
    add('Model calls, latency and cost','F',3,head('F','Model calls,<br>latency and <em>cost</em>')+flow([('CALL 1','Read the question','Model selects a tool.'),('TOOL','Fetch information','A service or database responds.'),('CALL 2','Read the result','Model writes the answer.')])+takeaway('More context, retries and delegation can increase usage and latency.'),'Use a hypothetical budget in model calls rather than unsupported prices: three model calls per request times fifty requests is 150 calls, before retries. Real billing often uses token counts and differs by provider/tool. Limit steps, set timeouts and monitor usage. Free tier means constrained allowance, not unlimited use.')
    add('Production checklist','F',4,head('F','Production <em>checklist</em>')+'<div class="checklist"><p><strong>Access</strong>Check identity and tool permissions.</p><p><strong>Data</strong>Choose retention, backup and deletion.</p><p><strong>Failures</strong>Handle missing records and timeouts.</p><p><strong>Visibility</strong>Record useful errors without secrets.</p><p><strong>Quality</strong>Run realistic known and unknown cases.</p><p><strong>Cost</strong>Set limits and inspect actual usage.</p></div>','Refer back to completion criteria and execution limits from the patterns section. Use this to bridge the small starter and production diagram. These are app responsibilities regardless of framework. Do not imply the current starter implements this checklist or is ready for untrusted multi-user deployment.')

    # G — 45 minutes
    add('Capstone: a document briefing assistant','G',5,head('G','Design a document<br><em>briefing assistant.</em>')+cards([('PERSON','An operations colleague','Uploads three fictional reports and asks for a one-page briefing.',''),('RESULT','A draft with sources','Show the key points, disagreements and open questions.',''),('BOUNDARY','A person reviews it','Prepare the draft. Publishing is a separate decision.','')]),'Form groups of three or four. Give each group the exercise sheet. Assign roles such as user, app designer and reviewer. Keep a common use case so architecture choices are comparable across groups.')
    exercise('Exercise: system architecture','G',20,'Sketch how a report becomes a useful draft.', ['Draw frontend → API → agent → tools → data.','Place originals, job records, working files and results.','Choose an execution pattern and framework; identify useful skills or MCP tools.','Show streaming status, artifact delivery, cancellation and approval.'],'one architecture sketch and a 60-second explanation.','Suggested pacing: 3 minutes user/output, 6 minutes architecture/data, 5 minutes patterns/integrations, 6 minutes streaming states, failure path and pitch. Walk around and ask who may see a document, what survives refresh, and how they know a draft is supported. Use paper or a shared whiteboard; no laptop is necessary.')
    add('Document assistant reference architecture','G',7,head('G','Document assistant:<br><em>reference architecture</em>')+diagram([(0,10,200,72,'Upload screen','Person submits reports','#d9e9f0'),(265,10,210,72,'API + job record','Validate ownership','#d3ead7'),(540,10,230,72,'Worker / agent','Read → compare → draft','#fbd8c9'),(890,10,230,72,'Gemini API','Text generation','#f1dfa5'),(20,245,225,72,'Object storage','Originals and draft','#e4ece0'),(390,245,220,72,'Approved read tool','Local or MCP-backed','#e4ece0'),(860,245,260,72,'Review screen','Person approves publication','#f1dfa5')],['M200 46H263','M475 46H538','M770 46H888','M370 82V166H132V243','M655 82V166H500V243','M390 281H247','M770 62H816V281H858'],'Upload screen calls API, API tracks ownership and a job, a worker agent uses Gemini and approved read tools, originals and drafts live in storage, the person reviews before publishing.')+'<p class="diagram-caption">Optional skill: briefing format. Durable status: database. Scratch work: a per-job workspace.</p>','This is a proposed extension, not the behavior of run_agent.py. Explain that the review screen needs authorization tied to the draft version. A skill can carry the briefing format; an MCP server can expose document reads. Neither is mandatory for a first version.')
    exercise('Share and compare','G',10,'Each group gets a short pitch.', ['Who is your assistant helping?','Where does the evidence come from?','Which action needs permission?','What happens when the tool fails?'],'one strong choice and one open question per group.','Allow approximately 60 seconds per group plus 30 seconds feedback, adapting to group count. Compare decisions instead of ranking brands. If there are many groups, pair them and ask two groups to share with the room.')
    reuse(8,'G',3,'The Git repository is local. Supply the published URL if it is published later; otherwise distribute the folder through an approved channel. Explain that .env.example is copied and real keys remain private.')

    # H — 25 minutes
    reuse(9,'H',4)
    add('Knowledge check','H',8,head('H','Knowledge <em>check</em>')+''.join(f'<div class="quiz-row"><span>{i:02d}</span><div>{q}</div></div>' for i,q in enumerate(['Where should an uploaded PDF usually live?','Does a model choice determine the framework?','How is a skill different from a tool?','What does an MCP server expose?','What must the app check before a write action?'],1)), 'Suggested answers: object storage with access controls; no, models and frameworks are distinct choices; skill is reusable guidance while a tool is an executable capability; tools/resources/prompts through MCP; identity, authorization, validated inputs and any required human approval. Ask for explanations rather than exact terminology.')
    add('Questions and next steps','H',9,head('H','Discussion and <em>Q&A</em>')+'<div class="illustrated-discussion"><div>'+cards([('START','One bounded task','What could you help someone do this week?',''),('CHECK','One known source','Where will the assistant find the answer?',''),('LEARN','One small trial','What result would tell you it is useful?','')])+'</div>'+art('agent-review-chibi.png','A chibi robot reviews reports and a checklist beside a laptop.','discussion-art')+'</div>','Reserve this time for questions. If an answer depends on a provider version or company policy, identify what to verify rather than guessing. Point to sources-and-frameworks.md and typical-app-scaffold.md. Advanced implementation details can be taken after the session.')
    reuse(10,'H',4,'Ask everyone to write one task they will try and one boundary they will keep. Thank the group and explain how they will receive the repository. Remind them that API credentials belong to their own account/project.')
    # Check that the proposed agenda really fits the requested day.
    for g,(_,_,budget) in MODULES.items():
        actual=sum(s['minutes'] for s in out if s['group']==g)
        assert actual==budget, (g,actual,budget)
    assert sum(s['minutes'] for s in out)==480
    return out

def write_supporting_materials(root, slides):
    def range_for(g):
        nums=[i+1 for i,s in enumerate(slides) if s['group']==g]
        return f'{nums[0]}–{nums[-1]}'
    runbook=['# Agentic App 101 — full-day facilitator runbook','',
        'Audience: people with mixed technical confidence. No participant installation or live coding is required. Use explanations, a presenter walkthrough, pair discussions and a paper/whiteboard capstone.', '',
        '## 09:00–17:00 agenda','',
        '| Time | Session | Slides | Minutes |','|---|---|---|---|']
    for g,(time,name,mins) in MODULES.items():
        runbook.append(f'| {time} | {name} | {range_for(g)} | {mins} |')
    runbook += ['', 'Breaks: 10:30–10:45 and 14:15–14:30. Lunch: 12:00–13:00. Total: 390 teaching/activity minutes + 90 break/lunch minutes = 480 minutes.', '',
        '## Preparation','',
        '- Open the HTML deck and use O for the overview, N for presenter notes, and arrow keys to navigate.',
        '- Read run_agent.py. Its fictional timetable is sample data, not the workshop agenda.',
        '- If using a live API demo, rehearse on the presenting machine with an available model and the project’s actual quota. A transcript is an acceptable fallback; label it as illustrative.',
        '- Keep API credentials private. The API example has not been validated with a live key as part of this content expansion.',
        '- Provide paper or a shared whiteboard. Use exercises.md for participant prompts.',
        '- The repository is currently local; add a real remote download URL only after publishing it.',
        '- The starter uses Google’s SDK. Deep Agents, ADK, LangGraph and CrewAI are comparison/reference material; the scaffold is a proposed organization.', '',
        '## Slide-by-slide notes','']
    outline=['# Full-day slide outline','', '| Slide | Module | Topic | Minutes |','|---|---|---|---|']
    for i,s in enumerate(slides,1):
        runbook += [f'### {i}. {s["title"]}', '',s['note'].replace('\\n','\n'),'']
        outline.append(f'| {i} | {s["group"]} | {s["title"]} | {s["minutes"]} |')
    (root/'facilitator-runbook.md').write_text('\n'.join(runbook).rstrip()+'\n')
    (root/'slide-outline.md').write_text('\n'.join(outline)+'\n')
    refs=['# Frameworks and related concepts — reference map','',
        'Reviewed against official documentation on 29 September 2026. These are learning references, not a performance ranking. Model names, APIs and capabilities evolve; check the linked documentation before implementing.', '',
        '| Lens | Google ADK | LangGraph | Deep Agents | CrewAI |','|---|---|---|---|---|',
        '| Organizing idea | Agents and workflows | Steps and transitions | A harness for extended tasks | Roles, tasks and flows |',
        '| Consider when | Google-oriented integrations suit the team | Explicit execution paths matter | File-oriented tasks and delegation help | Responsibilities divide into clear roles |',
        '| App work remains | Identity, data and deployment | Identity, data and deployment | Identity, data and deployment | Identity, data and deployment |','',
        'Fit guidance reflects the workshop’s design judgment. Many use cases can be implemented with more than one option.', '',
        '## High-level glossary','',
        '| Term | Plain-language meaning |', '|---|---|',
        '| Model | Produces outputs from the supplied prompt and context. |',
        '| SDK | A programming library for calling a service. |',
        '| Framework / harness | Helps organize how an agent uses tools and maintains a task. |',
        '| Runtime | Carries out execution steps and their state transitions. |',
        '| Tool | A specific operation exposed to an agent. |',
        '| Skill | Reusable task instructions, optionally with supporting files or scripts. |',
        '| MCP | A standard interface used by compatible applications and servers to exchange context and capabilities. |',
        '| MCP server | A local or remote program exposing selected capabilities, such as tools or resources. |',
        '| RAG | Retrieving relevant evidence and including it when generating an answer. |',
        '| Sandbox | A defined execution boundary whose actual permissions need inspection. |',
        '| Memory | Information retained for future use, with an ownership and retention policy. |',
        '| Observability | Logs, traces and measurements that help explain a run. |','',
        '## Execution patterns','',
        '| Pattern | Main role |', '|---|---|',
        '| ReAct | Interleave reasoning, tool actions and observations within a run. |',
        '| Plan-and-execute | Define steps, execute them and revise the plan when needed. |',
        '| Evaluator–optimizer | Generate a result, evaluate against criteria and revise with feedback. |',
        '| Multi-agent orchestration | Assign bounded tasks and combine the results. |',
        '| Ralph loop | Repeatedly invoke a coding agent, retaining progress in files and task state. |', '',
        'Patterns can be combined. A Ralph outer loop may invoke an agent with an inner ReAct-style loop. Framework selection is a separate implementation decision. Set completion criteria and enforce execution limits in the application.', '',
        '## Streaming and rendering','',
        'Application events connect backend execution to frontend state. Use stable run/message/event IDs, parse complete events rather than arbitrary network chunks, and separate text updates from tool status and artifacts. Persist messages and artifacts independently of the browser connection. SSE, streamed fetch responses and WebSockets are delivery choices; durable replay requires backend support.', '',
        'The example event names in the deck are a teaching schema, not a framework API. See streaming-and-artifacts.md for the design walkthrough.', '',
        '## Source references','']
    for title,url in SOURCES.values(): refs.append(f'- [{title}]({url})')
    refs += ['', '## Package names matter','',
        'The runnable starter uses google-genai. LangChain’s Python deepagents package is separate from the community TypeScript deepagentsdk demo previously referenced. Do not reuse one package’s APIs as if they belonged to another.', '',
        '## Skills and MCP together','',
        'Example design: a report-writing skill supplies formatting instructions; an authorized tool reads the report; an MCP server can make that tool available through a compatible interface. A direct local function can also supply the tool. Choose MCP when a shared integration is useful.', '',
        'Skills, retrieved documents and server-provided text are inputs to the app. They do not grant permissions. The app and its services enforce authorization.']
    (root/'sources-and-frameworks.md').write_text('\n'.join(refs)+'\n')
