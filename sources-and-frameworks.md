# Frameworks and related concepts — reference map

Reviewed against official documentation on 29 September 2026. These are learning references, not a performance ranking. Model names, APIs and capabilities evolve; check the linked documentation before implementing.

| Lens | Google ADK | LangGraph | Deep Agents | CrewAI |
|---|---|---|---|---|
| Organizing idea | Agents and workflows | Steps and transitions | A harness for extended tasks | Roles, tasks and flows |
| Consider when | Google-oriented integrations suit the team | Explicit execution paths matter | File-oriented tasks and delegation help | Responsibilities divide into clear roles |
| App work remains | Identity, data and deployment | Identity, data and deployment | Identity, data and deployment | Identity, data and deployment |

Fit guidance reflects the workshop’s design judgment. Many use cases can be implemented with more than one option.

## High-level glossary

| Term | Plain-language meaning |
|---|---|
| Model | Produces outputs from the supplied prompt and context. |
| SDK | A programming library for calling a service. |
| Framework / harness | Helps organize how an agent uses tools and maintains a task. |
| Runtime | Carries out execution steps and their state transitions. |
| Tool | A specific operation exposed to an agent. |
| Skill | Reusable task instructions, optionally with supporting files or scripts. |
| MCP | A standard interface used by compatible applications and servers to exchange context and capabilities. |
| MCP server | A local or remote program exposing selected capabilities, such as tools or resources. |
| RAG | Retrieving relevant evidence and including it when generating an answer. |
| Sandbox | A defined execution boundary whose actual permissions need inspection. |
| Memory | Information retained for future use, with an ownership and retention policy. |
| Observability | Logs, traces and measurements that help explain a run. |

## Execution patterns

| Pattern | Main role |
|---|---|
| ReAct | Interleave reasoning, tool actions and observations within a run. |
| Plan-and-execute | Define steps, execute them and revise the plan when needed. |
| Evaluator–optimizer | Generate a result, evaluate against criteria and revise with feedback. |
| Multi-agent orchestration | Assign bounded tasks and combine the results. |
| Ralph loop | Repeatedly invoke a coding agent, retaining progress in files and task state. |

Patterns can be combined. A Ralph outer loop may invoke an agent with an inner ReAct-style loop. Framework selection is a separate implementation decision. Set completion criteria and enforce execution limits in the application.

## Source references

- [ReAct paper](https://arxiv.org/abs/2210.03629)
- [Agent workflow patterns](https://www.anthropic.com/engineering/building-effective-agents)
- [Ralph: original description](https://ghuntley.com/ralph/)
- [Google ADK](https://google.github.io/adk-docs/)
- [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)
- [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview)
- [Deep Agents quickstart](https://docs.langchain.com/oss/python/deepagents/quickstart)
- [Deep Agents backends](https://docs.langchain.com/oss/python/deepagents/backends)
- [CrewAI](https://docs.crewai.com/en/introduction)
- [Agent Skills](https://agentskills.io/what-are-skills)
- [Deep Agents skills](https://docs.langchain.com/oss/python/deepagents/skills)
- [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Google Gen AI SDK](https://googleapis.github.io/python-genai/)

## Package names matter

The runnable starter uses google-genai. LangChain’s Python deepagents package is separate from the community TypeScript deepagentsdk demo previously referenced. Do not reuse one package’s APIs as if they belonged to another.

## Skills and MCP together

Example design: a report-writing skill supplies formatting instructions; an authorized tool reads the report; an MCP server can make that tool available through a compatible interface. A direct local function can also supply the tool. Choose MCP when a shared integration is useful.

Skills, retrieved documents and server-provided text are inputs to the app. They do not grant permissions. The app and its services enforce authorization.
