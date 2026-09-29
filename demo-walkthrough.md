# Presenter demo walkthrough

## Prepare

Run the app using the README. Choose Gemini mode for the real Deep Agents demonstration. If API access is unavailable, select `AGENT_MODE=sample`, restart, and explicitly describe the response as scripted. A build is not evidence of a successful live API run.

## 10-minute walkthrough

1. Open http://127.0.0.1:8000 (or port 8080 with Compose). Identify conversation history, chat and Sources.
2. Open **Explore the stack**. Map each displayed technology to the architecture slide.
3. Open a sample report. Explain that the text is stored as an object and its metadata is a database record.
4. Ask: **Compare the three regional reports. Highlight differences in cost assumptions and cite your sources.**
5. Watch **Agent activity**: search, read, and cache hit/miss events. Explain that model text is streamed into one assistant message.
6. Ask a follow-up about the South report. Explain bounded conversation history and cached document reads.
7. Ask for a **downloadable one-page briefing with source links**. Open the artifact preview and download the Markdown file.
8. Explain the file lifecycle: workspace staging file → object store → database metadata → artifact event → UI card.
9. Refresh the browser. Messages and artifacts remain; an active run can reconnect through its persisted event IDs.
10. Point to Stop. Explain that cancellation requests the worker to stop; it cannot undo completed writes.

If desired, upload a small fictional UTF-8 `.md` or `.txt` document. PDF parsing is outside this tutorial.

## Code tour

| File | Show |
|---|---|
| `frontend/src/main.tsx` | React message state, EventSource, artifact preview |
| `backend/main.py` | Run submission, ownership checks, event stream |
| `backend/agent.py` | `create_deep_agent`, Gemini model, application tools, skill |
| `backend/database.py` | Conversation, Message, Run, StreamEvent, Document, Artifact |
| `backend/storage.py` | Object adapter, workspace staging and TTL cache |
| `skills/briefing/SKILL.md` | Reusable report guidance loaded into virtual agent state |
| `compose.yaml` | Separate web/API/agent containers and backing services |

## What each storage type does

- **Database:** messages, run lifecycle, replayable events and file metadata.
- **Object storage:** original documents and generated Markdown files, addressed by keys.
- **File storage:** per-run intermediate report files.
- **Cache:** repeated document reads with 5-minute expiry, scoped by owner, ID and content hash.

## Implementation limits

This is a local teaching app with anonymous browser-session ownership, one worker process and bounded context. It is not a production account system or a distributed durable workflow engine. The UI handles streamed text and tool events, but not executable HTML artifacts. The Deep Agents scratch filesystem is ephemeral between runs; the app separately persists conversation messages and artifacts.

Keep the original `run_agent.py` only as optional reading for the simplest SDK tool-call example.
