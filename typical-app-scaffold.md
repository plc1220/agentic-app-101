# A typical agentic app scaffold

This is an illustrative folder map for discussion. The runnable example remains `run_agent.py`; the directories below are not a shipped full-stack implementation.

```text
agentic-app/
├── frontend/
│   ├── chat/                  # input and message display
│   └── progress/              # tool/run status
├── backend/
│   ├── api/                   # HTTP routes, identity, input validation
│   ├── agent/                 # instructions, model, workflow
│   ├── tools/                 # bounded model-callable capabilities
│   ├── services/              # database/API access and business rules
│   └── workers/               # optional long-running jobs
├── skills/
│   └── summarize-report/
│       ├── SKILL.md           # when and how to perform the task
│       └── references/        # formatting examples, domain guidance
├── integrations/
│   └── mcp/                   # optional client/connection configuration
├── evals/                     # examples and expected outcomes
├── infra/                     # containers and deployment configuration
├── .env.example               # setting names, never real secrets
└── README.md                  # prerequisites and launch instructions
```

## Follow one request

1. The frontend sends a question to the app API.
2. The API checks the caller and validates the request.
3. Agent code supplies instructions and allowed tools to the model.
4. A tool validates arguments and calls an authorized service.
5. The result returns to the model for an answer.
6. The app stores any required run metadata and presents the answer.

For a long job, the API can create a durable job record and place work on a queue. A worker performs it. The frontend follows a job ID rather than keeping one request open forever.

## Where each change belongs

| Change | Starting location | Related responsibility |
|---|---|---|
| Change a label or chat layout | frontend/ | Accessibility and clear progress |
| Add a model-callable lookup | backend/tools/ | Input validation and permissions |
| Connect a database | backend/services/ | Credentials, queries and schema |
| Change agent instructions | backend/agent/ | Evaluation of changed behavior |
| Standardize a report process | skills/ | Host support and reviewed assets |
| Reuse an external capability | integrations/mcp/ | Server trust, access and lifecycle |
| Check a regression | evals/ | Realistic input and expected result |
| Package the service | infra/ | Runtime config and durable storage |

## From the included script

- `input()` and `print()` become a frontend and an API interface.
- The instruction and model call move into `backend/agent/`.
- `find_workshop_session()` belongs in `backend/tools/`.
- `SESSIONS` could later be retrieved through `backend/services/`.
- The sample has no persistent conversation, web API or production authorization layer.

A small app can combine files until separation helps. No framework imposes this exact tree.
