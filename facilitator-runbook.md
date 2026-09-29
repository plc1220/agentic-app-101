# Agentic App 101 — full-day facilitator runbook

Audience: people with mixed technical confidence. No participant installation or live coding is required. Use explanations, a presenter walkthrough, pair discussions and a paper/whiteboard capstone.

## 09:00–17:00 agenda

| Time | Session | Slides | Minutes |
|---|---|---|---|
| 09:00–09:30 | Start with the idea | 1–6 | 30 |
| 09:30–10:30 | Architecture and data | 7–14 | 60 |
| 10:45–12:00 | Containers and project structure | 16–25 | 75 |
| 13:00–14:15 | Frameworks, skills and MCP | 27–40 | 75 |
| 14:30–15:30 | Walkthrough and reliability | 42–50 | 60 |
| 15:30–16:30 | Design your own assistant | 51–55 | 60 |
| 16:30–17:00 | Review, questions and next steps | 56–59 | 30 |

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

09:00–09:30 · Start with the idea · 3 minutes

Welcome the group. No installation or coding is required during the workshop. The downloadable starter lets participants revisit the idea afterwards. We will use a fictional workshop schedule throughout.

Today is a full-day workshop. Ask participants to think of one repetitive information task they would like help with.

### 2. Our day together

09:00–09:30 · Start with the idea · 4 minutes

Explain the rhythm: short talks, examples, pair discussions and a capstone. Nobody needs to install software. Ask participants to return at the listed times. Use the slide overview to jump to a module if discussion runs long.

### 3. What you will be able to explain

09:00–09:30 · Start with the idea · 5 minutes

Invite participants to choose the outcome that is least familiar. Define repo as a folder whose changes Git tracks; API as an interface software uses to request a service. Gather two participant use cases for later discussion.

### 4. Chat, workflow or agent

09:00–09:30 · Start with the idea · 7 minutes

Ask the group to classify a receipt email and a research assistant. Explain that an agent still runs inside programmed limits. A workflow can call an LLM, and an agent can follow a mostly fixed workflow. These categories help choose control flow; they are not a ranking.

### 5. An assistant with a toolbox

09:00–09:30 · Start with the idea · 6 minutes

Explain that the schedule comes from a lookup function. The model is not expected to invent the time. This is an illustration, not a live API response. Ask the audience what other small lookup tasks they do regularly.

Show the question first. Ask “where should the answer come from?” Then discuss why an approved schedule lookup beats relying on model knowledge for a changing timetable.

### 6. Pick a small first job

09:00–09:30 · Start with the idea · 5 minutes

Allow two minutes alone, two minutes in pairs and one minute for examples. Prefer bounded jobs: find a policy, summarize a document, check a status. If someone proposes running an entire department, narrow it to one useful decision.

### 7. The app around the AI

09:30–10:30 · Architecture and data · 7 minutes

Use plain language before technical names. The screen is the frontend; the application services are the backend. The take-home script uses a terminal as its screen. A web app can provide a chat interface around the same idea.

Translate screen to frontend and app services to backend. Keep the same example: the schedule comes from a tool. The starter uses a terminal; this diagram also fits a web frontend.

### 8. A typical agentic app architecture

09:30–10:30 · Architecture and data · 10 minutes

Walk left to right, then downward. Identity and permissions belong to the app/API and tools. The model runs at a provider; it does not directly connect to your database. A backend function makes the database query. Explain one failure per boundary: login, model quota, tool timeout, storage access.

### 9. Trace a single request

09:30–10:30 · Architecture and data · 7 minutes

Use a participant as the user, another as the model and another as the tool. Pass a question card along the four stages. The model suggests a tool call; ordinary application code executes it. Show that an answer may take multiple model calls.

### 10. Four homes for data

09:30–10:30 · Architecture and data · 8 minutes

A database holds structured records. Object storage holds blobs addressed by an object key. File storage exposes named files and folders; it can be durable, while an agent workspace may be temporary. A cache improves speed and can expire. Keep these distinctions clear without requiring the audience to know particular cloud products.

Add the difference between file storage and object storage: folders and file operations versus blobs addressed by keys. File storage can be durable. An agent workspace is often temporary by choice, not because all file storage is temporary.

### 11. One upload, several data types

09:30–10:30 · Architecture and data · 8 minutes

Use a fictional invoice. The database row references the object; it need not contain the whole PDF. Working text may be deleted after processing or retained if justified. A cache could store repeated lookups but should not become the only copy of important records.

### 12. Retrieval: give the model the right pages

09:30–10:30 · Architecture and data · 7 minutes

Explain retrieval with a handbook. Embeddings are numeric representations that can help find similar text; they are one search option. Keyword or database search can be enough for a small corpus. Retrieval does not retrain the model and does not guarantee a correct answer. Check permissions before supplying excerpts.

### 13. Where should these go?

09:30–10:30 · Architecture and data · 8 minutes

Use pairs: five minutes to sort, two minutes to share, one minute to highlight uncertainty. Ask which items must survive a restart and which can be recreated. The next slide contains a suggested answer.

### 14. Storage exercise: suggested answer

09:30–10:30 · Architecture and data · 5 minutes

Invite alternatives. Extracted text can be durable if it will be reused. A small prototype might use a local file rather than object storage. Reward reasoning about lifetime and access rather than insisting on a vendor product.

### 15. Morning break

10:30–10:45 · 15 minutes. Resume on time; no setup tasks for participants.

### 16. Frontend and backend responsibilities

10:45–12:00 · Containers and project structure · 7 minutes

Explain why a provider API key should not be shipped in browser JavaScript. The starter keeps it in a local environment file and runs Python locally. A hosted app instead loads its own server-side credential. The browser should not be allowed to grant itself extra tool permissions.

### 17. Package the app

10:45–12:00 · Containers and project structure · 7 minutes

The packing analogy introduces consistent environments. Explain that containers can be replaced, so data that must survive needs a mounted volume or external store. The starter does not require Docker. This slide teaches the concept without adding installation work.

### 18. A local Compose architecture

10:45–12:00 · Containers and project structure · 8 minutes

A Compose file defines service images, ports, dependencies and volumes. Startup order alone is not a health check. Secrets should be supplied at runtime. This is a teaching diagram; the existing starter does not ship this Docker stack. Show how replacing the app container need not delete a database volume.

### 19. Short requests and long jobs

10:45–12:00 · Containers and project structure · 8 minutes

Explain the queue as a numbered ticket. The request can return before work is finished. A worker process takes a ticket and performs the job. The database holds durable job status so refreshing the browser does not lose it. Avoid introducing queue vendor details.

### 20. A typical project scaffold

10:45–12:00 · Containers and project structure · 10 minutes

Walk the tree slowly. Ask where to change a button, add a lookup, or alter an instruction. Explain services as ordinary code that talks to a database or API. Point to typical-app-scaffold.md for a more detailed map. Show that a small app can combine files initially; folders are for clarity rather than compliance.

### 21. From one script to those folders

10:45–12:00 · Containers and project structure · 8 minutes

Open the real script and point to these four parts. Make clear this is a mapping, not a claim that those folders exist in the starter. A refactor changes organization while retaining the behavior. A browser frontend requires an API layer that the terminal sample does not need.

### 22. A tool needs a clear contract

10:45–12:00 · Containers and project structure · 7 minutes

A docstring is part of what the SDK can expose to the model. A tool description is not an authorization mechanism. Validate arguments, handle missing records and return a useful error. Avoid giving a model unrestricted query strings or arbitrary shell execution for a lookup task.

### 23. Configuration belongs outside the logic

10:45–12:00 · Containers and project structure · 5 minutes

Explain the difference between a configuration value and a secret. A free-tier key inherits the associated project’s tier and quota. Do not change an existing project’s billing during the workshop. Show only placeholders, never a real key.

### 24. Which folder would you change?

10:45–12:00 · Containers and project structure · 10 minutes

Six minutes in pairs, three minutes to compare, one minute to surface alternate designs. People can answer using the diagram without reading Python.

### 25. Scaffold exercise: suggested answer

10:45–12:00 · Containers and project structure · 5 minutes

Point out that useful changes often cross boundaries. Folder structure helps ownership but does not remove integration work. An evaluation is a realistic example with an expected outcome, not merely a test that the function returns something.

### 26. Lunch

12:00–13:00 · 60 minutes. Resume on time; no setup tasks for participants.

### 27. Model, SDK, framework and runtime

13:00–14:15 · Frameworks, skills and MCP · 5 minutes

Our runnable script uses the Google SDK and automatic function calling. It is not currently a Deep Agents app. These categories overlap in products; use them to explain responsibilities. The model choice and the framework choice are separate decisions.

### 28. Frameworks: side-by-side comparison

13:00–14:15 · Frameworks, skills and MCP · 9 minutes

Spend about two minutes on each column. These are overlapping approaches, not mutually exclusive capabilities. Match the app and team to the approach. None removes the need for authentication, data ownership, deployment or checks. Python Deep Agents is distinct from the community TypeScript deepagentsdk demo discussed earlier.

References: https://google.github.io/adk-docs/; https://docs.langchain.com/oss/python/langgraph/overview; https://docs.langchain.com/oss/python/deepagents/overview; https://docs.crewai.com/en/introduction

### 29. Choose by the question you need to answer

13:00–14:15 · Frameworks, skills and MCP · 5 minutes

These are facilitator recommendations, not exclusive product claims. A framework is useful when it reduces repeated work and improves control. Do not choose based only on a feature checklist or a popular name. Ask what people on the team can maintain.

### 30. Where Deep Agents fits

13:00–14:15 · Frameworks, skills and MCP · 5 minutes

Think of nested responsibilities, not five separate machines. Deep Agents builds on LangChain and uses LangGraph. Your app still owns identity and data access. Do not present the starter SDK script as using this stack.

References: https://docs.langchain.com/oss/python/deepagents/overview

### 31. What Deep Agents can add

13:00–14:15 · Frameworks, skills and MCP · 6 minutes

Version behavior matters. Explain capabilities conceptually rather than teaching all configuration options. A virtual filesystem can be backed by memory, disk or another store; it does not imply a secure execution sandbox. Inspect installed-version docs before adapting production code.

References: https://docs.langchain.com/oss/python/deepagents/overview; https://docs.langchain.com/oss/python/deepagents/backends

### 32. A framework configuration: the shape

13:00–14:15 · Frameworks, skills and MCP · 6 minutes

This is deliberately a reading exercise, not copy-and-run code. Explain that Gemini can be configured through a compatible model integration. The actual runnable file stays run_agent.py and uses Google’s SDK.

References: https://docs.langchain.com/oss/python/deepagents/quickstart

### 33. Three coordination patterns

13:00–14:15 · Frameworks, skills and MCP · 5 minutes

Sequence follows an ordered path. Routing selects one path. Delegation assigns bounded work that returns a result. Parallel tasks can help when independent, but do not assume a group of agents improves correctness. Discuss one case where ordinary code is more predictable.

### 34. Skills, tools and MCP in one view

13:00–14:15 · Frameworks, skills and MCP · 5 minutes

The skill is guidance, the tool is an operation, and MCP is an integration interface. They can work together. A skill may include scripts and resources, but the app still decides how those run. MCP does not itself make a data source trustworthy or provide unlimited access.

References: https://agentskills.io/what-are-skills; https://modelcontextprotocol.io/docs/learn/architecture

### 35. A skill is a reusable task guide

13:00–14:15 · Frameworks, skills and MCP · 5 minutes

Skills package task guidance and supporting assets. The host/framework decides how it discovers and loads them. Loading skill instructions does not grant new permissions or replace the model. Compatibility and supported behavior differ across hosts.

References: https://agentskills.io/what-are-skills; https://docs.langchain.com/oss/python/deepagents/skills

### 36. An MCP server connects capabilities

13:00–14:15 · Frameworks, skills and MCP · 6 minutes

MCP is the protocol, and the server is software implementing it. The server may run on the same computer or remotely. It can provide more than tools: resources supply context and prompts provide templates. Avoid teaching protocol mechanics here.

References: https://modelcontextprotocol.io/docs/learn/architecture

### 37. One example using all three

13:00–14:15 · Frameworks, skills and MCP · 4 minutes

An application can call an ordinary local function without MCP. MCP is useful for reusable connections across compatible clients. The document remains input data; embedded instructions in it should not override application policy. This is a design example, not an installed integration.

### 38. Other terms you may hear

13:00–14:15 · Frameworks, skills and MCP · 4 minutes

These terms describe needs or patterns, not things every beginner app must install. A container alone is not proof of safe untrusted-code execution. A log should avoid credentials and unnecessary personal data. Use the reference handout for links and definitions.

### 39. Choose an approach

13:00–14:15 · Frameworks, skills and MCP · 6 minutes

There is no unique correct framework. A reasonable answer might evaluate Deep Agents for long tasks, use a comparison-writing skill, and reuse an authorized document connector. ADK or a graph can also fit depending on the team. Assess the reasoning, not the logo.

### 40. Compare on fit, then validate

13:00–14:15 · Frameworks, skills and MCP · 4 minutes

Close the framework discussion by asking which evidence would change the team’s mind. Small representative trials are more informative than a long feature list. Keep the chosen approach minimal and add integrations when they solve a real need.

### 41. Afternoon break

14:15–14:30 · 15 minutes. Resume on time; no setup tasks for participants.

### 42. The model asks, the app acts

14:30–15:30 · Walkthrough and reliability · 6 minutes

Python runs the lookup function after Gemini requests it. Google’s SDK handles the function-call exchange. The sample tool reads fixed data. It does not send email, modify files, or run shell commands. Tool use can require several model requests; do not describe it as necessarily one API request.

### 43. Read the actual starter

14:30–15:30 · Walkthrough and reliability · 7 minutes

Open the file on the presenter’s screen; do not ask attendees to type. Walk through it from top to bottom without explaining every Python token. The sample schedule is fictional and is not the timing plan for today. Tool matching is basic; use unknown-query behavior as a discussion point.

### 44. Start with Gemini

14:30–15:30 · Walkthrough and reliability · 6 minutes

Presenter project: my-rd-coe-demo-gen-ai. In AI Studio, select or import that project if you have access. A key inherits its project’s billing tier; an existing billed project is not necessarily on the free tier. A project ID alone is not a credential. The script uses the Developer API key, not Vertex AI. Refer to the linked current pricing/billing pages rather than quoting fixed quotas.

The model configured in .env must still be available. Check the key’s actual project tier before any API call. Free-tier access is not guaranteed for an existing billed project. Do not promise one request per answer because automatic function calling may involve several.

### 45. Meet the workshop helper

14:30–15:30 · Walkthrough and reliability · 7 minutes

The output on this slide is illustrative; wording varies by model. run_agent.py is a small Gemini tool-calling example, not a Deep Agents implementation. The original Deep Agents repos remain optional reading. Be clear that this program does not persist a conversation or implement a web frontend.

If a live API run has not been rehearsed, use the labelled example output and walk the code. The slide is not evidence that the API has been tested.

### 46. Try useful and awkward questions

14:30–15:30 · Walkthrough and reliability · 6 minutes

Use fixed sample inputs. If the tool gives a bad match, explain the matching limitation rather than attributing everything to the model. Missing credentials, unavailable model and quota errors are environment cases. Never claim a successful run if only the transcript was shown.

### 47. Before a tool changes something

14:30–15:30 · Walkthrough and reliability · 7 minutes

Use an email example: finding an address, drafting an email, and sending it are different actions. For writes, retries need duplicate prevention. Mention idempotency as an optional word meaning repeated requests do not repeat a side effect. The starter is read-only.

### 48. How would we judge the assistant?

14:30–15:30 · Walkthrough and reliability · 8 minutes

Ask groups to propose one additional example. A small evaluation set can include known, unknown, ambiguous and malformed inputs. Record model/config changes and compare results. An answer sounding confident does not establish correctness.

### 49. Where time and cost go

14:30–15:30 · Walkthrough and reliability · 7 minutes

Use a hypothetical budget in model calls rather than unsupported prices: three model calls per request times fifty requests is 150 calls, before retries. Real billing often uses token counts and differs by provider/tool. Limit steps, set timeouts and monitor usage. Free tier means constrained allowance, not unlimited use.

### 50. A small release checklist

14:30–15:30 · Walkthrough and reliability · 6 minutes

Use this to bridge the small starter and production diagram. These are app responsibilities regardless of framework. Do not imply the current starter implements this checklist or is ready for untrusted multi-user deployment.

### 51. Capstone: a document briefing assistant

15:30–16:30 · Design your own assistant · 5 minutes

Form groups of three or four. Give each group the exercise sheet. Assign roles such as user, app designer and reviewer. Keep a common use case so architecture choices are comparable across groups.

### 52. Draw your first version

15:30–16:30 · Design your own assistant · 25 minutes

Suggested pacing: 5 minutes user/output, 8 minutes architecture/data, 7 minutes framework/integrations/permissions, 5 minutes failure path and pitch. Walk around and ask who may see a document, what survives refresh, and how they know a draft is supported. Use paper or a shared whiteboard; no laptop is necessary.

### 53. One possible capstone design

15:30–16:30 · Design your own assistant · 10 minutes

This is a proposed extension, not the behavior of run_agent.py. Explain that the review screen needs authorization tied to the draft version. A skill can carry the briefing format; an MCP server can expose document reads. Neither is mandatory for a first version.

### 54. Share and compare

15:30–16:30 · Design your own assistant · 15 minutes

Allow approximately 60 seconds per group plus 30 seconds feedback, adapting to group count. Compare decisions instead of ranking brands. If there are many groups, pair them and ask two groups to share with the room.

### 55. Try it after the workshop

15:30–16:30 · Design your own assistant · 5 minutes

No attendee needs to install or run anything during the session. The local repo has not yet been published to a remote host; supply the eventual download link separately. The launch scripts install packages on the first run, so internet access is required. Keep .env private; Git ignores it.

The Git repository is local. Supply the published URL if it is published later; otherwise distribute the folder through an approved channel. Explain that .env.example is copied and real keys remain private.

### 56. As the app grows

16:30–17:00 · Review, questions and next steps · 5 minutes

Connect this to a real customer-order assistant: it needs identity, authorization, durable records, and error handling. Keep it concrete. A retry is not always safe for a tool that sends or charges something; read-only lookup is a simpler first capability.

### 57. Five quick checks

16:30–17:00 · Review, questions and next steps · 10 minutes

Suggested answers: object storage with access controls; no, models and frameworks are distinct choices; skill is reusable guidance while a tool is an executable capability; tools/resources/prompts through MCP; identity, authorization, validated inputs and any required human approval. Ask for explanations rather than exact terminology.

### 58. Questions and next steps

16:30–17:00 · Review, questions and next steps · 10 minutes

Reserve this time for questions. If an answer depends on a provider version or company policy, identify what to verify rather than guessing. Point to sources-and-frameworks.md and typical-app-scaffold.md. Advanced implementation details can be taken after the session.

### 59. Your first agent starts small

16:30–17:00 · Review, questions and next steps · 5 minutes

Invite questions. Recap using the schedule example: one lookup function, fixed sample data, and application-controlled access. The guide is README.md in the same folder. The deck and starter work from local files; no external fonts or images are needed.

Ask everyone to write one task they will try and one boundary they will keep. Thank the group and explain how they will receive the repository. Remind them that API credentials belong to their own account/project.
