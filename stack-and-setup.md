# Stack and setup

## Runnable demo

| Layer | Technology | Purpose |
|---|---|---|
| Runtime | Python 3.10+ | Runs the local application |
| Interface | Terminal | Reads questions and prints complete responses |
| Model client | `google-genai` | Calls the Gemini Developer API and manages Python function calling |
| Configuration | `python-dotenv` | Loads `.env` beside the script |
| Tool | `find_workshop_session()` | Reads a fixed in-memory timetable |
| Environment | Python `venv` + `pip` | Isolates and installs dependencies |

The launcher installs `google-genai` and `python-dotenv`, including their dependencies. The demo does not install React, FastAPI, Deep Agents, Docker, a database, or an MCP server. It does not stream tokens or save conversation history.

## Setup steps

1. Install **Python 3.10 or newer**. On Windows, enable the installer’s PATH option or use the Python launcher.
2. Get the repository folder. Git is optional if you receive a ZIP or copied folder. A public Git remote has not yet been configured.
3. Copy `.env.example` to `.env` in that folder. Replace `paste_your_key_here` with your Gemini API key.
4. Keep or update `GEMINI_MODEL` to a model your key can access. The current example value is `gemini-3-flash-preview`.
5. Run the launcher from the repository folder:

| Platform | Command |
|---|---|
| macOS / Linux | `bash run.sh` |
| Windows Command Prompt | `run.bat` |
| Windows PowerShell | `.\run.bat` |

The launcher creates `.venv` if needed, upgrades pip, installs `requirements.txt`, and starts `run_agent.py`. There is no manual virtual-environment activation step. If `.env` is missing, the launcher creates a template and asks you to fill it in before continuing.

Internet access is needed for package installation and Gemini requests. API access depends on the key’s project, model availability and quota. The content update has not established a successful live API run with your key.

### Project and credentials

Use an AI Studio Gemini Developer API key associated with the intended project, such as `my-rd-coe-demo-gen-ai` if you have access. A project ID is not a credential. This script explicitly selects the Developer API and the key loaded from `.env`; it does not require `gcloud` login, a service-account JSON file, or a Vertex AI configuration.

Free-tier eligibility depends on the selected model and project tier. Check [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) and [model availability](https://ai.google.dev/gemini-api/docs/models). Keep keys in `.env`, which Git ignores.

### Common setup issues

| Message or symptom | Next action |
|---|---|
| Python not found / old Python | Install Python 3.10+ and reopen the terminal |
| `venv` or `ensurepip` unavailable | Install the Python venv component for your OS distribution |
| Missing or placeholder key | Edit `.env` beside `run_agent.py` |
| Model not found or unavailable | Select an accessible model in `GEMINI_MODEL` |
| Quota / rate-limit response | Inspect that project’s quota and tier |
| Package download blocked | Check internet access and any organization-managed proxy |

## Reference full-stack design

This is a proposed web application architecture for discussion. It is not installed or implemented by the demo launchers.

| Layer | Example technology | Why it appears in the design |
|---|---|---|
| Frontend | React + TypeScript | Chat state, progress, streaming text and artifact previews |
| Web service | Static assets and API reverse proxy | Delivers the frontend and routes same-origin requests |
| API service | FastAPI + Uvicorn | Authenticates requests, creates runs, streams events and serves artifacts |
| Agent worker | Python + Deep Agents + Gemini | Executes agent tasks and emits progress events |
| Database | PostgreSQL | Stores conversations, run status and artifact metadata |
| Cache | Redis | Speeds up repeat lookups; entries have an expiry |
| Jobs / events | A queue or event log; Redis is one option | Connects API and worker; needs separate durability/retention policies |
| Object storage | S3-compatible storage or Google Cloud Storage | Holds uploads and generated files |
| File storage | Mounted filesystem volume | Provides workspace paths for processing |
| Local deployment | Docker Compose | Connects web, API, worker and support services |

Separate containers make responsibilities visible and allow independent deployment. A first version can combine the API and agent runtime in one service. A container boundary is not a complete sandbox for untrusted code.

## How a streamed request works

1. The browser submits a message to the API.
2. The API checks permissions and creates a run record.
3. The agent worker calls the model and tools.
4. The worker emits events; the API forwards appropriate updates to the browser.
5. The frontend updates the current message, tool status and artifact cards.
6. The backend saves final messages and artifacts for refresh and later retrieval.

See `streaming-and-artifacts.md` for event, rendering and recovery details.
