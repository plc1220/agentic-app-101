# Agentic App 101

A beginner-friendly full-day workshop (09:00–17:00) and a tiny runnable Gemini agent. Attendees can take this folder home and run the example later; nobody needs to install software or run code during the workshop.

## Start here

1. Install Python 3.10 or newer and get the repository folder (ZIP/copy, or clone after a public URL is available). Git is optional when using a ZIP.
2. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey). The Gemini API has a free tier for selected models, subject to current model availability and project quotas. Free-tier usage has data-use terms that differ from paid use; do not enter confidential or personal data.
3. Copy `.env.example` to `.env` and paste the API key after `GEMINI_API_KEY=`.
4. Run `run.bat` in Windows Command Prompt (`.\run.bat` in PowerShell), or `bash run.sh` on macOS/Linux. The launcher creates `.venv` and installs the Python packages automatically.
5. Ask: `When is the backend session?` or `What happens in the demo?` Type `quit` to exit.

There is no manual virtual-environment activation or cloud CLI setup. Internet access, a valid API key and model quota are required. See `stack-and-setup.md` for platform instructions and common setup issues. The repository is currently local with no public clone URL.

The example is intentionally small: Gemini answers questions and can call one safe Python function that looks up a fixed workshop schedule. The terminal prints when the function is used. No database, cloud storage, Docker, or framework setup is required.

## Your Google Cloud project

The easiest route is the Gemini Developer API key from Google AI Studio. The key is associated with a Google Cloud project; if you have access to `my-rd-coe-demo-gen-ai`, select or import that project when creating the key. The script reads `GEMINI_API_KEY`; it does not need the project ID as a separate setting.

This example does not use Vertex AI. Using Vertex AI with that project is a different configuration and may require enabling services, credentials, and billing. A project ID by itself is not an API credential.

Free-tier access, available models, data handling, and quotas can change. Check Google's current [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing), [billing and tiers](https://ai.google.dev/gemini-api/docs/billing), and [rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) before the workshop.

## What the code demonstrates

- The attendee enters a normal-language question.
- Gemini can decide to call `find_workshop_session`.
- Python runs that specific function and returns its result to Gemini.
- Gemini turns the result into a short answer.

This is tool calling: the model chooses whether a capability should be used, while the app owns and runs the capability. The function only reads fixed sample data; it cannot execute arbitrary commands or access files.

## Files

- `agentic-app-101.html` — workshop slide deck. Use left/right arrow keys; `N` opens presenter notes, `O` opens the slide overview, and `F` toggles fullscreen. The illustrated deck works offline without external fonts or images.
- `run_agent.py` — small Gemini tool-calling example.
- `run.sh` / `run.bat` — install dependencies and start the program.
- `facilitator-runbook.md` — full-day agenda, exact slide timings, and speaker notes.
- `slide-outline.md` — all slides, modules, and planned durations.
- `demo-walkthrough.md` — presenter walkthrough of the actual starter and backup plan.
- `typical-app-scaffold.md` — a reference project tree and responsibility map.
- `sources-and-frameworks.md` — framework comparison, skills/MCP glossary, and official references.
- `exercises.md` — discussion prompts and a capstone worksheet.
- `stack-and-setup.md` — actual demo stack, exact setup, and proposed full-stack technologies.
- `streaming-and-artifacts.md` — stream events, chat rendering, artifact delivery and recovery.
- `assets/` — generated chibi illustrations embedded in the HTML.
- `backend-building-blocks.md` — database, object storage, workspace, cache, and container notes.

## Framework and reference notes

The earlier full-stack reference, [deepagentsdk-nextjs-demo](https://github.com/chrispangg/deepagentsdk-nextjs-demo), uses the TypeScript `deepagentsdk` package and needs an Anthropic key. For this audience, the included Python script is the simpler run-later demonstration and uses Google's official `google-genai` SDK with automatic Python function calling.

LangChain's Python [`deepagents`](https://github.com/langchain-ai/deepagents) is a separate package with related ideas. A public beginner tutorial is [mkassaf/deepagents-tutorial](https://github.com/mkassaf/deepagents-tutorial). Keep the concepts in the slides, but avoid implying these APIs are interchangeable.

## Keep your key private

- Do not paste the API key into Python source code, slides, chat, or a public repository.
- Keep the key only in `.env`; Git ignores that file.
- If a key is accidentally shared, revoke it in AI Studio and create another.

## Editing the full-day deck

The HTML is self-contained, with inline diagrams, embedded illustrations and presenter notes. Editable source is in `deck/build.py`, `deck/lesson_content.py`, `deck/streaming_chapter.py`, and `deck/extra.css`. Run `python3 deck/build.py` to rebuild the HTML, slide outline, reference map, and facilitator runbook. The build checks that planned sessions and breaks add up to an eight-hour day.

The day includes architecture, storage, containers, a typical app scaffold, ReAct, plan-and-execute, evaluator–optimizer, multi-agent orchestration, a Ralph loop reference, ADK/LangGraph/Deep Agents/CrewAI comparisons, skills, MCP, a 40-minute streaming/chat/artifact chapter, evaluation, and group design. Framework snippets and full-stack architecture diagrams are teaching references; the only runnable application is the Gemini SDK starter.
