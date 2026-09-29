# Tutorial repository structure

```text
frontend/
  src/main.tsx          Chat, EventSource, sources and artifact preview
  src/style.css         Responsive interface styles
backend/
  main.py               API routes, session ownership, SSE and worker dispatch
  agent.py              Deep Agents, Gemini and three application tools
  database.py           Durable SQLAlchemy models
  storage.py            Object store, workspace files and cache
  config.py             Local defaults and environment settings
  static/               Prebuilt React bundle for Python-only setup
skills/briefing/         SKILL.md used by the real agent
sample-documents/       Three fictional regional reports
infra/                  Dockerfile and streaming reverse proxy
compose.yaml            Optional multi-container deployment
launch.py               Local server entry point
run.sh / run.bat         Environment and dependency setup
.env.example            Configuration placeholders
```

## Change-to-component map

| Change | File |
|---|---|
| Change chat or progress rendering | `frontend/src/main.tsx` |
| Add an API endpoint | `backend/main.py` |
| Add a model-callable operation | `backend/agent.py` |
| Change database records | `backend/database.py` |
| Change storage/cache behavior | `backend/storage.py` |
| Change briefing guidance | `skills/briefing/SKILL.md` |
| Change container boundaries | `compose.yaml` and `infra/` |

The local launch combines API and agent in one Python process. Compose runs the same backend image in API and agent roles, with internal authenticated HTTP dispatch and database-backed stream events. Redis caches document reads; it is not the run queue.
