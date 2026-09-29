# Agentic App 101

A beginner-friendly workshop pack and a tiny runnable Gemini agent. Attendees can take this folder home and run the example later; nobody needs to install software or run code during the workshop.

## Start here

1. Install Python 3.10 or newer.
2. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey). The Gemini API has a free tier for selected models, subject to current model availability and project quotas. Free-tier usage has data-use terms that differ from paid use; do not enter confidential or personal data.
3. Copy `.env.example` to `.env` and paste the API key after `GEMINI_API_KEY=`.
4. Run `run.bat` on Windows, or `./run.sh` on macOS/Linux. The first run installs the required Python packages.
5. Ask: `When is the backend session?` or `What happens in the demo?` Type `quit` to exit.

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

- `agentic-app-101.html` — workshop slide deck. Use left/right arrow keys; press `N` for speaker notes.
- `run_agent.py` — small Gemini tool-calling example.
- `run.sh` / `run.bat` — install dependencies and start the program.
- `facilitator-runbook.md` — suggested three-hour facilitation plan.
- `slide-outline.md` — original slide sequence and teaching notes.
- `demo-walkthrough.md` — reference repository walkthrough and backup plan.
- `backend-building-blocks.md` — database, object storage, workspace, cache, and container notes.

## Framework and reference notes

The earlier full-stack reference, [deepagentsdk-nextjs-demo](https://github.com/chrispangg/deepagentsdk-nextjs-demo), uses the TypeScript `deepagentsdk` package and needs an Anthropic key. For this audience, the included Python script is the simpler run-later demonstration and uses Google's official `google-genai` SDK with automatic Python function calling.

LangChain's Python [`deepagents`](https://github.com/langchain-ai/deepagents) is a separate package with related ideas. A public beginner tutorial is [mkassaf/deepagents-tutorial](https://github.com/mkassaf/deepagents-tutorial). Keep the concepts in the slides, but avoid implying these APIs are interchangeable.

## Keep your key private

- Do not paste the API key into Python source code, slides, chat, or a public repository.
- Keep the key only in `.env`; Git ignores that file.
- If a key is accidentally shared, revoke it in AI Studio and create another.
