# Demo walkthrough — Deep Agents in a full-stack app

## Selected reference

[chrispangg/deepagentsdk-nextjs-demo](https://github.com/chrispangg/deepagentsdk-nextjs-demo)

The repository README describes a Next.js app with a chat UI, `/api/chat` route, event streaming, file operations, a file explorer, and a local sandbox workspace. It lists Bun or Node, an Anthropic API key, and an optional Tavily key for web search.

This repo uses the TypeScript package `deepagentsdk`. Do not present its API as the API for LangChain's Python package `deepagents`. For Python framework teaching, pair this with [mkassaf/deepagents-tutorial](https://github.com/mkassaf/deepagents-tutorial), which has small examples and a FastAPI server example.

## Before the session

1. Clone the repository from its public GitHub URL.
2. Read its README and current package scripts.
3. Install with the package manager and lockfile the repository specifies.
4. Create a local environment file from the example, and supply a private Anthropic key. Add Tavily only if demonstrating web search.
5. Start the development server and open the local app.
6. Test one prompt that creates a harmless text file and another short multi-step task.
7. Confirm what workspace files are created and how to reset them.
8. Keep a screen recording or screenshots available as a fallback.

Do not commit or project the environment file. Do not put API keys in slides, terminal history, or screen recordings.

## 25–35 minute live path

### Part A — Establish the app boundary (3 minutes)

Show the repository tree. Find:

- `src/app/page.tsx`: chat UI and event/file views.
- `src/app/api/chat/route.ts`: agent setup and request handling.
- `.sandbox-workspace/`: local demo workspace.

Explain that this is a Next.js full-stack app: UI and server route live in one project. It is different from a separate React frontend and Python API.

### Part B — Trace request and response (8 minutes)

Submit: “Create a short file named `workshop-notes.txt` containing three bullet points about the task you are doing.”

Trace browser submission to `/api/chat`, agent invocation, tool/file events, and streamed UI updates. Point out which data is ephemeral workspace content versus durable application data. This demo illustrates the former; it is not an example of a DB-backed chat history service.

### Part C — Explain the agent setup (8 minutes)

In the API route, locate model selection, system prompt, sandbox construction, and event handler/streaming integration. Explain:

- The model proposes a tool call; the app/framework executes only tools that are made available.
- Tool results return to the model, which can continue or finish.
- The event stream exposes progress to the UI.
- The sandbox/workspace is the agent's file boundary in this demo.

### Part D — Small customization (6 minutes)

Change the system prompt so that the agent must first outline the intended file changes and then create only the requested file. Rerun the same prompt and compare the visible events and final workspace. Revert the edit afterwards.

### Part E — Debrief (5 minutes)

Ask what is missing for a real multi-user service: authentication/authorization, isolated per-user execution, durable conversations, external object storage, database migrations, cache/limits, operational monitoring, and deployment configuration.

## Backup plan

If the model endpoint, key, network, or dependency install fails:

- Show a previously captured run and explain the request path from source.
- Use a prepared screenshot of the event stream and generated file.
- Continue with a whiteboard trace; do not spend the workshop debugging environment setup.

## Safety and architecture note

The demo can execute commands and manipulate workspace files. Treat it as a local educational demo. Do not expose it to untrusted users or imply that a local workspace alone provides production-grade isolation. For a real app, run untrusted code/actions inside an explicitly designed and tested execution boundary, and grant tools the minimum required permissions.
