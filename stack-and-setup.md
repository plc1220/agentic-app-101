# Stack and setup

The complete quick start and component matrix are in [README.md](README.md).

## Default launch

Install Python 3.11+, get the repository, copy `.env.example` to `.env`, add the Gemini key, and run `bash run.sh` or `run.bat`. Open http://127.0.0.1:8000.

The launcher manages `.venv` and pip. The committed React bundle is served by FastAPI. SQLite, a local object-store adapter, workspace files and an in-memory TTL cache initialize automatically. Python is the only runtime attendees need to install.

Deep Agents calls Gemini through `langchain-google-genai`. The key stays on the server. This path uses the Gemini Developer API and does not need a Cloud project ID in the runtime configuration, ADC, `gcloud`, or a service-account file.

## Environment variables

| Setting | Default | Purpose |
|---|---|---|
| `GEMINI_API_KEY` | Required for Gemini mode | Model API credential |
| `GEMINI_MODEL` | `gemini-3-flash-preview` | Model accessible to your project |
| `AGENT_MODE` | `gemini` | `sample` selects a labelled no-model walkthrough |
| `PORT` | `8000` | Local launcher port |
| `DATA_DIR` | `.data/` | Local persistent and workspace files |
| `DATABASE_URL` | Local SQLite | Compose overrides with PostgreSQL |
| `REDIS_URL` | Unset | Compose selects Redis; otherwise local TTL cache |
| `S3_ENDPOINT` | Unset | Compose selects MinIO; otherwise local files |
| `WORKER_URL` | Unset | Compose dispatches to a separate agent service |
| `WORKER_TOKEN` | Unset locally | Authenticates internal worker requests in Compose |

The optional container path uses `docker compose up --build` and serves the app at http://127.0.0.1:8080. Example service credentials are intended only for the private Compose network in this local tutorial. Do not expose it as a production system.

## Troubleshooting

| Symptom | Action |
|---|---|
| Python missing or older than 3.11 | Install a supported Python; reopen the terminal |
| Existing `.venv` uses an old Python | Move the old environment aside; rerun with Python 3.11+ |
| `venv` / `ensurepip` missing on Linux | Install the distribution’s Python venv component |
| UI says the key is missing | Edit `.env` and restart the server |
| Model/permission/quota error | Check the key’s project and `GEMINI_MODEL`; use sample mode if unavailable |
| Address already in use | Set `PORT` to a free port and restart |
| Frontend source changed but UI did not | Run `npm run build --prefix frontend` and refresh |
| Docker agent unavailable | Inspect `docker compose logs api agent`; wait for service health |
| MinIO not ready during initial startup | API retries via Compose’s restart policy |
| Run failed after restart | Saved partial output remains; submit a new request |

Changing from `127.0.0.1` to `localhost`, clearing cookies, or using another browser creates a separate anonymous session, so its conversation list differs. Use the same browser origin to return to saved chats.

## Data and reset

Default local data lives in `.data/` and is ignored by Git. The session signing secret also lives there. Preserve the folder to retain chats and files; move it aside while the server is stopped for a fresh workshop instance. Compose uses named volumes for its database, objects, API session secret and workspace.

The app does not implement automatic retention cleanup or account management. Use fictional workshop data. Setup does not call Gemini until a user submits a message in Gemini mode.
