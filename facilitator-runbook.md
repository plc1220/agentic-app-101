# Agentic App 101 — full-day facilitator runbook

Audience: people with mixed technical confidence. No participant installation or live coding is required. Use explanations, a presenter walkthrough, pair discussions and a paper/whiteboard capstone.

## 09:00–17:00 agenda

| Time | Session | Slides | Minutes |
|---|---|---|---|
| 09:00–09:30 | Agent fundamentals | 1–6 | 30 |
| 09:30–10:30 | Architecture and data | 7–14 | 60 |
| 10:45–12:00 | Containers and project structure | 16–26 | 75 |
| 13:00–14:15 | Agent patterns and frameworks | 28–46 | 75 |
| 14:30–15:10 | Streaming chat and artifacts | 48–55 | 40 |
| 15:10–15:50 | Demo stack and walkthrough | 56–65 | 40 |
| 15:50–16:35 | System design exercise | 66–70 | 45 |
| 16:35–17:00 | Review and Q&A | 71–74 | 25 |

Breaks: 10:30–10:45 and 14:15–14:30. Lunch: 12:00–13:00. Total: 390 teaching/activity minutes + 90 break/lunch minutes = 480 minutes.

## Preparation

- Open the HTML deck and use O for the overview, N for presenter notes, and arrow keys to navigate.
- Read run_agent.py. Its fictional timetable is sample data, not the workshop agenda.
- If using a live API demo, rehearse on the presenting machine with an available model and the project’s actual quota. A transcript is an acceptable fallback; label it as illustrative.
- Keep API credentials private. The API example has not been validated with a live key as part of this content expansion.
- Provide paper or a shared whiteboard. Use exercises.md for participant prompts.
- The repository is currently local; add a real remote download URL only after publishing it.
- The starter uses Google’s SDK. Deep Agents, ADK, LangGraph and CrewAI are comparison/reference material; the scaffold is a proposed organization.

## Slide-by-slide notes

### 1. Agentic App 101

09:00–09:30 · Agent fundamentals · 3 minutes

Welcome the group. No installation or coding is required during the workshop. The downloadable starter lets participants revisit the idea afterwards. We will use a fictional workshop schedule throughout.

Today is a full-day workshop. Ask participants to think of one repetitive information task they would like help with.

### 2. Workshop agenda

09:00–09:30 · Agent fundamentals · 4 minutes

Explain the rhythm: short talks, examples, pair discussions and a capstone. Nobody needs to install software. Ask participants to return at the listed times. Use the slide overview to jump to a module if discussion runs long.

### 3. Learning objectives

09:00–09:30 · Agent fundamentals · 5 minutes

Invite participants to choose the outcome that is least familiar. Define repo as a folder whose changes Git tracks; API as an interface software uses to request a service. Gather two participant use cases for later discussion.

### 4. Chat, workflow or agent

09:00–09:30 · Agent fundamentals · 7 minutes

Ask the group to classify a receipt email and a research assistant. Explain that an agent still runs inside programmed limits. A workflow can call an LLM, and an agent can follow a mostly fixed workflow. These categories help choose control flow; they are not a ranking.

### 5. Agents and tools

09:00–09:30 · Agent fundamentals · 6 minutes

Explain that the schedule comes from a lookup function. The model is not expected to invent the time. This is an illustration, not a live API response. Ask the audience what other small lookup tasks they do regularly.

Show the question first. Ask “where should the answer come from?” Then discuss why an approved schedule lookup beats relying on model knowledge for a changing timetable.

### 6. Exercise: define a use case

09:00–09:30 · Agent fundamentals · 5 minutes

Allow two minutes alone, two minutes in pairs and one minute for examples. Prefer bounded jobs: find a policy, summarize a document, check a status. If someone proposes running an entire department, narrow it to one useful decision.

### 7. Application components

09:30–10:30 · Architecture and data · 7 minutes

Use the connected boxes to follow the request and then the result. The agent runtime is normally part of the backend; it is shown separately here as a responsibility. The frontend renders events and results rather than executing privileged tools. A terminal can be the user interface in a small demo. The next slide adds model and data services; the streaming chapter explains ongoing updates.

### 8. A typical agentic app architecture

09:30–10:30 · Architecture and data · 10 minutes

Follow a request across the top. Tool and application service code controls access to data. The cache may hold repeated lookup results with an expiry; access and cache keys must respect the user and data version. Database records include conversation and run status; object storage holds uploaded files and artifacts; file storage provides workspace paths. These are logical responsibilities, not a requirement for one server each. The streaming chapter later explains the event path back to the browser and how artifacts are rendered.

### 9. Request lifecycle

09:30–10:30 · Architecture and data · 7 minutes

Use a participant as the user, another as the model and another as the tool. Pass a question card along the four stages. The model suggests a tool call; ordinary application code executes it. Show that an answer may take multiple model calls.

### 10. Backend storage

09:30–10:30 · Architecture and data · 8 minutes

A database holds structured records. Object storage holds blobs addressed by an object key. File storage exposes named files and folders; it can be durable, while an agent workspace may be temporary. A cache improves speed and can expire. Keep these distinctions clear without requiring the audience to know particular cloud products.

Add the difference between file storage and object storage: folders and file operations versus blobs addressed by keys. File storage can be durable. An agent workspace is often temporary by choice, not because all file storage is temporary.

### 11. Document processing pipeline

09:30–10:30 · Architecture and data · 8 minutes

Use a fictional invoice. The database row references the object; it need not contain the whole PDF. Working text may be deleted after processing or retained if justified. A cache could store repeated lookups but should not become the only copy of important records.

### 12. Retrieval-augmented generation (RAG)

09:30–10:30 · Architecture and data · 7 minutes

Explain retrieval with a handbook. Embeddings are numeric representations that can help find similar text; they are one search option. Keyword or database search can be enough for a small corpus. Retrieval does not retrain the model and does not guarantee a correct answer. Check permissions before supplying excerpts.

### 13. Exercise: select storage

09:30–10:30 · Architecture and data · 8 minutes

Use pairs: five minutes to sort, two minutes to share, one minute to highlight uncertainty. Ask which items must survive a restart and which can be recreated. The next slide contains a suggested answer.

### 14. Storage exercise: suggested answer

09:30–10:30 · Architecture and data · 5 minutes

Invite alternatives. Extracted text can be durable if it will be reused. A small prototype might use a local file rather than object storage. Reward reasoning about lifetime and access rather than insisting on a vendor product.

### 15. Morning break

10:30–10:45 · 15 minutes. Resume on time; no setup tasks for participants.

### 16. Frontend and backend responsibilities

10:45–12:00 · Containers and project structure · 5 minutes

Explain why a provider API key should not be shipped in browser JavaScript. The starter keeps it in a local environment file and runs Python locally. A hosted app instead loads its own server-side credential. The browser should not be allowed to grant itself extra tool permissions.

### 17. Containerization

10:45–12:00 · Containers and project structure · 6 minutes

The packing analogy introduces consistent environments. Explain that containers can be replaced, so data that must survive needs a mounted volume or external store. The starter does not require Docker. This slide teaches the concept without adding installation work.

### 18. Docker Compose architecture

10:45–12:00 · Containers and project structure · 7 minutes

This is a proposed Compose design, not a shipped runnable stack. The web service serves frontend assets and proxies API requests. The API authenticates requests, manages run records and streams events. The agent service runs work and emits progress. API-to-agent traffic may use internal HTTP or Redis jobs/events; the arrows show logical communication. The API and worker may both access supporting data services as required. Cache entries can expire; a reliable queue or event log needs its own retention and persistence policy. Separating containers supports independent deployment, but a small app can run the API and agent in one process. Database and file volumes survive container replacement. Object storage can be an external service.

### 19. Reference full-stack technologies

10:45–12:00 · Containers and project structure · 5 minutes

Explain each layer using the preceding container diagram. This is a proposed extension with example technologies; these packages and services are not installed by run.sh. The existing runnable app is a Python terminal program. React runs in the browser after assets are served. Uvicorn serves the FastAPI application. Deep Agents is the reference framework discussed in the workshop, but the included demo uses Google’s SDK directly. Redis can support several responsibilities, provided cache expiry is not accidentally used for durable jobs. The exact integration, versions and deployment still need implementation.

References: https://fastapi.tiangolo.com/advanced/custom-response/; https://docs.langchain.com/oss/python/deepagents/overview

### 20. Synchronous requests and background jobs

10:45–12:00 · Containers and project structure · 7 minutes

Explain the queue as a numbered ticket. The request can return before work is finished. A worker process takes a ticket and performs the job. The database holds durable job status so refreshing the browser does not lose it. Avoid introducing queue vendor details.

### 21. Example project structure

10:45–12:00 · Containers and project structure · 10 minutes

Walk the tree slowly. Ask where to change a button, add a lookup, or alter an instruction. Explain services as ordinary code that talks to a database or API. Point to typical-app-scaffold.md for a more detailed map. Show that a small app can combine files initially; folders are for clarity rather than compliance.

### 22. Mapping the demo to application components

10:45–12:00 · Containers and project structure · 8 minutes

Open the real script and point to these four parts. Make clear this is a mapping, not a claim that those folders exist in the starter. A refactor changes organization while retaining the behavior. A browser frontend requires an API layer that the terminal sample does not need.

### 23. Tool definition

10:45–12:00 · Containers and project structure · 7 minutes

A docstring is part of what the SDK can expose to the model. A tool description is not an authorization mechanism. Validate arguments, handle missing records and return a useful error. Avoid giving a model unrestricted query strings or arbitrary shell execution for a lookup task.

### 24. Configuration and credentials

10:45–12:00 · Containers and project structure · 5 minutes

Explain the difference between a configuration value and a secret. A free-tier key inherits the associated project’s tier and quota. Do not change an existing project’s billing during the workshop. Show only placeholders, never a real key.

### 25. Exercise: application components

10:45–12:00 · Containers and project structure · 10 minutes

Six minutes in pairs, three minutes to compare, one minute to surface alternate designs. People can answer using the diagram without reading Python.

### 26. Application components: suggested answers

10:45–12:00 · Containers and project structure · 5 minutes

Point out that useful changes often cross boundaries. Folder structure helps ownership but does not remove integration work. An evaluation is a realistic example with an expected outcome, not merely a test that the function returns something.

### 27. Lunch

12:00–13:00 · 60 minutes. Resume on time; no setup tasks for participants.

### 28. Model, SDK, framework and runtime

13:00–14:15 · Agent patterns and frameworks · 4 minutes

Our runnable script uses the Google SDK and automatic function calling. It is not currently a Deep Agents app. These categories overlap in products; use them to explain responsibilities. The model choice and the framework choice are separate decisions.

### 29. ReAct: reason, act, observe

13:00–14:15 · Agent patterns and frameworks · 6 minutes

ReAct interleaves reasoning, actions and observations. Trace the return arrow when the first search result is insufficient; take the answer branch when evidence is sufficient. The application executes the tool and enforces access. Explain the decision at a high level; do not imply that internal reasoning must be displayed. The existing Gemini SDK demo illustrates a tool-call exchange, but it does not implement the original ReAct prompting method. Connect this diagram to the agent component in the architecture slide.

References: https://arxiv.org/abs/2210.03629

### 30. Plan-and-execute

13:00–14:15 · Agent patterns and frameworks · 4 minutes

Walk through the document assistant. Planning is useful when a task has several dependent steps. The short return path runs another step; the longer path revises the plan when evidence changes. A plan can be represented as a task list or structured state. Fixed steps can also be ordinary workflow code. This is a general pattern, not a claim that every framework supplies the same planner API. An execution step may itself use a ReAct-style loop.

References: https://www.anthropic.com/engineering/building-effective-agents

### 31. Evaluator–optimizer

13:00–14:15 · Agent patterns and frameworks · 4 minutes

Apply this to a document briefing draft. A validator can check required fields, while a model or person can assess less mechanical criteria. Model evaluation is fallible, especially when generator and evaluator share blind spots. Use known examples to assess the evaluator. Set a revision limit and return unresolved issues when it is reached. Passing evaluation prepares a draft for review; it does not authorize publication.

References: https://www.anthropic.com/engineering/building-effective-agents

### 32. Multi-agent orchestration

13:00–14:15 · Agent patterns and frameworks · 4 minutes

Replace the earlier brief orchestration slide with this concrete example. Explain sequence, routing and delegation verbally: sequence follows ordered steps, routing selects a specialist, delegation assigns work and combines results. Independent report summaries may run in parallel. Each worker may have its own tool loop. For three short reports, one agent may be sufficient; delegation adds coordination, model calls and failure cases. The synthesis step must preserve sources and handle missing worker results.

References: https://www.anthropic.com/engineering/building-effective-agents

### 33. Ralph loop: repeated agent runs

13:00–14:15 · Agent patterns and frameworks · 4 minutes

Keep this as a reference example for building the document assistant, rather than the assistant’s normal document-processing flow. Geoffrey Huntley describes Ralph as a technique whose simplest form is a shell loop repeatedly invoking a coding agent. Files, specifications and the plan carry progress between runs. The diagram expands the work performed during an iteration; implementations vary. The original minimal loop does not provide a completion guarantee or automatic stop condition. A run may contain ReAct-style tool use. Use the controls on the next slide for a bounded implementation; do not demonstrate an unbounded shell loop.

References: https://ghuntley.com/ralph/

### 34. Completion criteria and execution limits

13:00–14:15 · Agent patterns and frameworks · 3 minutes

Close the pattern section by asking where the stop decision belongs. Application code should enforce budgets and permissions. Model assertions of completion are not sufficient evidence. A run may finish with a partial result or a request for human input. Transition: an execution pattern describes the flow; a framework supplies tools for implementing it. Frameworks can support several patterns, and a single application can combine patterns. Revisit these controls in the capstone.

### 35. Frameworks: side-by-side comparison

13:00–14:15 · Agent patterns and frameworks · 7 minutes

Allow about one minute per framework, then compare tradeoffs and take questions. These are overlapping approaches, not mutually exclusive capabilities. Match the app and team to the approach. None removes the need for authentication, data ownership, deployment or checks. Python Deep Agents is distinct from the community TypeScript deepagentsdk demo discussed earlier.

References: https://google.github.io/adk-docs/; https://docs.langchain.com/oss/python/langgraph/overview; https://docs.langchain.com/oss/python/deepagents/overview; https://docs.crewai.com/en/introduction

### 36. Framework selection

13:00–14:15 · Agent patterns and frameworks · 3 minutes

These are facilitator recommendations, not exclusive product claims. A framework is useful when it reduces repeated work and improves control. Do not choose based only on a feature checklist or a popular name. Ask what people on the team can maintain.

### 37. Where Deep Agents fits

13:00–14:15 · Agent patterns and frameworks · 3 minutes

Think of nested responsibilities, not five separate machines. Deep Agents builds on LangChain and uses LangGraph. Your app still owns identity and data access. Do not present the starter SDK script as using this stack.

References: https://docs.langchain.com/oss/python/deepagents/overview

### 38. Deep Agents capabilities

13:00–14:15 · Agent patterns and frameworks · 4 minutes

Version behavior matters. Explain capabilities conceptually rather than teaching all configuration options. A virtual filesystem can be backed by memory, disk or another store; it does not imply a secure execution sandbox. Inspect installed-version docs before adapting production code.

References: https://docs.langchain.com/oss/python/deepagents/overview; https://docs.langchain.com/oss/python/deepagents/backends

### 39. Deep Agents configuration

13:00–14:15 · Agent patterns and frameworks · 4 minutes

This is deliberately a reading exercise, not copy-and-run code. Explain that Gemini can be configured through a compatible model integration. The actual runnable file stays run_agent.py and uses Google’s SDK.

References: https://docs.langchain.com/oss/python/deepagents/quickstart

### 40. Skills, tools and MCP

13:00–14:15 · Agent patterns and frameworks · 3 minutes

The skill is guidance, the tool is an operation, and MCP is an integration interface. They can work together. A skill may include scripts and resources, but the app still decides how those run. MCP does not itself make a data source trustworthy or provide unlimited access.

References: https://agentskills.io/what-are-skills; https://modelcontextprotocol.io/docs/learn/architecture

### 41. Agent Skills

13:00–14:15 · Agent patterns and frameworks · 4 minutes

Skills package task guidance and supporting assets. The host/framework decides how it discovers and loads them. Loading skill instructions does not grant new permissions or replace the model. Compatibility and supported behavior differ across hosts.

References: https://agentskills.io/what-are-skills; https://docs.langchain.com/oss/python/deepagents/skills

### 42. Model Context Protocol (MCP)

13:00–14:15 · Agent patterns and frameworks · 5 minutes

MCP is the protocol, and the server is software implementing it. The server may run on the same computer or remotely. It can provide more than tools: resources supply context and prompts provide templates. Avoid teaching protocol mechanics here.

References: https://modelcontextprotocol.io/docs/learn/architecture

### 43. Example: skills and MCP tools

13:00–14:15 · Agent patterns and frameworks · 3 minutes

An application can call an ordinary local function without MCP. MCP is useful for reusable connections across compatible clients. The document remains input data; embedded instructions in it should not override application policy. This is a design example, not an installed integration.

### 44. Additional concepts

13:00–14:15 · Agent patterns and frameworks · 3 minutes

These terms describe needs or patterns, not things every beginner app must install. A container alone is not proof of safe untrusted-code execution. A log should avoid credentials and unnecessary personal data. Use the reference handout for links and definitions.

### 45. Choose an approach

13:00–14:15 · Agent patterns and frameworks · 4 minutes

There is no unique correct framework. A reasonable answer might evaluate Deep Agents for long tasks, use a comparison-writing skill, and reuse an authorized document connector. ADK or a graph can also fit depending on the team. Assess the reasoning, not the logo.

### 46. Framework selection criteria

13:00–14:15 · Agent patterns and frameworks · 3 minutes

Close the framework discussion by asking which evidence would change the team’s mind. Small representative trials are more informative than a long feature list. Keep the chosen approach minimal and add integrations when they solve a real need.

### 47. Afternoon break

14:15–14:30 · 15 minutes. Resume on time; no setup tasks for participants.

### 48. Streaming chat and artifacts

14:30–15:10 · Streaming chat and artifacts · 5 minutes

Use the three panels to introduce separate UI responsibilities. Streaming reduces the wait before visible output; it does not guarantee faster total execution. A tool may run for some time without text, so show a real status event. An artifact is a saved output such as a report, CSV or image. The chapter describes a web application extension; the runnable terminal demo waits for a complete answer. Ask what users should see during a 30-second document lookup.

### 49. Streaming response architecture

14:30–15:10 · Streaming chat and artifacts · 6 minutes

Explain two directions: the browser sends a request, then receives many updates. The API adapts provider or framework events to an application event format. It retains credentials server-side and filters internal or sensitive tool data before delivery. A separate worker needs an event channel back to the API, such as a broker or database-backed event log. Configure application and proxy layers to flush data rather than buffer the complete response. A saved run can continue after a browser disconnect, depending on the app policy.

References: https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams; https://docs.langchain.com/oss/python/deepagents/streaming

### 50. HTTP streaming, SSE and WebSockets

14:30–15:10 · Streaming chat and artifacts · 4 minutes

These options overlap. Native EventSource opens a GET stream, so a common design creates a run with POST and subscribes using its run ID. A POST fetch can also return SSE data, but the client then parses the stream and manages reconnect logic. EventSource has built-in reconnection behavior; that alone does not persist or replay application events. WebSocket is useful when frequent bidirectional messages are needed. Plain polling remains a valid option for coarse job status. Recommend a single HTTP streaming approach for a first text-chat application.

References: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events; https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams

### 51. Application stream events

14:30–15:10 · Streaming chat and artifacts · 5 minutes

These names are a teaching schema, not SDK event names. A transport chunk may contain part of one event or several events; decode and buffer before parsing. Keep stable identifiers so tool events, messages and artifacts are not mixed between runs. Order events and discard duplicates when replaying. A final completion event is distinct from the last text delta and from an unexpectedly closed connection. A provider may expose other events, which the backend should map before sending to the browser.

### 52. Chat and artifact rendering

14:30–15:10 · Streaming chat and artifacts · 6 minutes

This is a static mockup; the displayed controls are illustrations. Append chunks to the same assistant message, not a new bubble per chunk. Render plain text safely or use a Markdown renderer that handles incomplete code blocks, links and tables. Disable or sanitize raw HTML. Batch visual updates and auto-scroll only when the reader is already near the bottom. Preserve scroll position when someone reads earlier content. Expose concise status updates for accessibility rather than announcing every token. Keep tool activity separate from answer text; do not expose hidden reasoning or credentials. The artifact opens in a separate preview with its own identity and version.

### 53. Message and run lifecycle

14:30–15:10 · Streaming chat and artifacts · 4 minutes

Distinguish a conversation from a run: one conversation contains multiple messages, and one run may involve multiple tools and model calls. A message can have partial content while the run is active. Keep partial output clearly marked if execution fails. Persistence supports refresh; local UI state alone does not. A cache can accelerate access but should not be the only copy of a completed conversation. Store replayable events when resuming a stream is a requirement; otherwise reload the latest saved state.

### 54. Artifact storage and delivery

14:30–15:10 · Streaming chat and artifacts · 5 minutes

An artifact is a durable output, not merely a long chat message. Store content type, size, owner, status and version. The arrows show a lifecycle, not a claim that object storage writes database records itself; backend code coordinates both writes. Return an authorized download endpoint or a short-lived signed URL after checking ownership. Use safe renderers for Markdown, CSV and images. Treat generated HTML as untrusted; sandbox previews and restrict scripts and network access. Use a new version for revisions so review applies to a specific artifact.

References: https://fastapi.tiangolo.com/advanced/custom-response/

### 55. Cancellation and reconnects

14:30–15:10 · Streaming chat and artifacts · 5 minutes

Aborting the browser fetch does not by itself guarantee that the server, model or worker stops. The backend must propagate cancellation and report the resulting state. Cancellation cannot undo side effects already committed. Reconnect with the same run ID; replay after the last event ID only if the backend retains events. If replay is unavailable, fetch a current snapshot rather than silently starting a duplicate run. For long tasks, persist job state outside the streaming connection. Ask participants to explain what a refresh should do during report generation.

References: https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams; https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events

### 56. Runnable demo stack

15:10–15:50 · Demo stack and walkthrough · 5 minutes

The stack shown here is what attendees receive. It has no browser UI, web API, database server, container runtime or Deep Agents dependency. It uses automatic function calling and prints the completed response rather than token streaming. Explain Python as the runtime and pip packages as dependencies. The launcher manages a local virtual environment so users do not need to activate it manually. A working internet connection, a valid key and access/quota for the configured model are required. The repository currently has no public remote; distribute the folder or publish a real URL before asking people to clone.

### 57. Tool calling

15:10–15:50 · Demo stack and walkthrough · 3 minutes

Python runs the lookup function after Gemini requests it. Google’s SDK handles the function-call exchange. The sample tool reads fixed data. It does not send email, modify files, or run shell commands. Tool use can require several model requests; do not describe it as necessarily one API request.

### 58. Read the actual starter

15:10–15:50 · Demo stack and walkthrough · 4 minutes

Open the file on the presenter’s screen; do not ask attendees to type. Walk through it from top to bottom without explaining every Python token. The sample schedule is fictional and is not the timing plan for today. Tool matching is basic; use unknown-query behavior as a discussion point.

### 59. Gemini API access

15:10–15:50 · Demo stack and walkthrough · 4 minutes

Presenter project: my-rd-coe-demo-gen-ai. In AI Studio, select or import that project if you have access. A key inherits its project’s billing tier; an existing billed project is not necessarily on the free tier. A project ID alone is not a credential. The script uses the Developer API key, not Vertex AI. Refer to the linked current pricing/billing pages rather than quoting fixed quotas.

The model configured in .env must still be available. Check the key’s actual project tier before any API call. Free-tier access is not guaranteed for an existing billed project. Do not promise one request per answer because automatic function calling may involve several.

### 60. Gemini tool-calling demo

15:10–15:50 · Demo stack and walkthrough · 5 minutes

The output on this slide is illustrative; wording varies by model. run_agent.py is a small Gemini tool-calling example, not a Deep Agents implementation. The original Deep Agents repos remain optional reading. Be clear that this program does not persist a conversation or implement a web frontend.

If a live API run has not been rehearsed, use the labelled example output and walk the code. The slide is not evidence that the API has been tested.

### 61. Demo test cases

15:10–15:50 · Demo stack and walkthrough · 4 minutes

Use fixed sample inputs. If the tool gives a bad match, explain the matching limitation rather than attributing everything to the model. Missing credentials, unavailable model and quota errors are environment cases. Never claim a successful run if only the transcript was shown.

### 62. Tool permissions and approval

15:10–15:50 · Demo stack and walkthrough · 4 minutes

Use an email example: finding an address, drafting an email, and sending it are different actions. For writes, retries need duplicate prevention. Mention idempotency as an optional word meaning repeated requests do not repeat a side effect. The starter is read-only.

### 63. Agent evaluation

15:10–15:50 · Demo stack and walkthrough · 4 minutes

Ask groups to propose one additional example. A small evaluation set can include known, unknown, ambiguous and malformed inputs. Record model/config changes and compare results. An answer sounding confident does not establish correctness.

### 64. Model calls, latency and cost

15:10–15:50 · Demo stack and walkthrough · 3 minutes

Use a hypothetical budget in model calls rather than unsupported prices: three model calls per request times fifty requests is 150 calls, before retries. Real billing often uses token counts and differs by provider/tool. Limit steps, set timeouts and monitor usage. Free tier means constrained allowance, not unlimited use.

### 65. Production checklist

15:10–15:50 · Demo stack and walkthrough · 4 minutes

Refer back to completion criteria and execution limits from the patterns section. Use this to bridge the small starter and production diagram. These are app responsibilities regardless of framework. Do not imply the current starter implements this checklist or is ready for untrusted multi-user deployment.

### 66. Capstone: a document briefing assistant

15:50–16:35 · System design exercise · 5 minutes

Form groups of three or four. Give each group the exercise sheet. Assign roles such as user, app designer and reviewer. Keep a common use case so architecture choices are comparable across groups.

### 67. Exercise: system architecture

15:50–16:35 · System design exercise · 20 minutes

Suggested pacing: 3 minutes user/output, 6 minutes architecture/data, 5 minutes patterns/integrations, 6 minutes streaming states, failure path and pitch. Walk around and ask who may see a document, what survives refresh, and how they know a draft is supported. Use paper or a shared whiteboard; no laptop is necessary.

### 68. Document assistant reference architecture

15:50–16:35 · System design exercise · 7 minutes

This is a proposed extension, not the behavior of run_agent.py. Explain that the review screen needs authorization tied to the draft version. A skill can carry the briefing format; an MCP server can expose document reads. Neither is mandatory for a first version.

### 69. Share and compare

15:50–16:35 · System design exercise · 10 minutes

Allow approximately 60 seconds per group plus 30 seconds feedback, adapting to group count. Compare decisions instead of ranking brands. If there are many groups, pair them and ask two groups to share with the room.

### 70. Demo setup

15:50–16:35 · System design exercise · 3 minutes

No attendee needs to install or run anything during the session. The local repo has not yet been published to a remote host; supply the eventual download link separately. The launch scripts install packages on the first run, so internet access is required. Keep .env private; Git ignores it.

The Git repository is local. Supply the published URL if it is published later; otherwise distribute the folder through an approved channel. Explain that .env.example is copied and real keys remain private.

### 71. Production considerations

16:35–17:00 · Review and Q&A · 4 minutes

Connect this to a real customer-order assistant: it needs identity, authorization, durable records, and error handling. Keep it concrete. A retry is not always safe for a tool that sends or charges something; read-only lookup is a simpler first capability.

### 72. Knowledge check

16:35–17:00 · Review and Q&A · 8 minutes

Suggested answers: object storage with access controls; no, models and frameworks are distinct choices; skill is reusable guidance while a tool is an executable capability; tools/resources/prompts through MCP; identity, authorization, validated inputs and any required human approval. Ask for explanations rather than exact terminology.

### 73. Questions and next steps

16:35–17:00 · Review and Q&A · 9 minutes

Reserve this time for questions. If an answer depends on a provider version or company policy, identify what to verify rather than guessing. Point to sources-and-frameworks.md and typical-app-scaffold.md. Advanced implementation details can be taken after the session.

### 74. Summary

16:35–17:00 · Review and Q&A · 4 minutes

Invite questions. Recap using the schedule example: one lookup function, fixed sample data, and application-controlled access. The guide is README.md in the same folder. The deck and starter work from local files; no external fonts or images are needed.

Ask everyone to write one task they will try and one boundary they will keep. Thank the group and explain how they will receive the repository. Remind them that API credentials belong to their own account/project.
