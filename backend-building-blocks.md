# Backend building blocks for agentic apps

## One scenario

A user uploads invoices and asks an agent to summarize spending by category. The application needs to accept and process files, track a run, let the agent work, and show the result.

| Component | Main job | Example in the scenario | Common mistake |
|---|---|---|---|
| Database | Durable, queryable application records | User, run status, invoice metadata, category totals, conversation/thread reference | Treating the database as a good place for large binary files by default |
| Object storage | Durable storage for blobs/artifacts | Original PDFs, extracted images, exported report | Assuming an object URL alone provides authorization |
| File storage/workspace | Files arranged by path for an app or job to read/write | Temporary extraction output, agent scratch files, generated draft | Assuming a container's writable layer is persistent or safely isolated |
| Cache | Fast access to reusable or short-lived data | Vendor lookup, rate limit counters, short-lived results | Using cache as the source of truth or assuming it never expires |

## Decision prompts

For each piece of data, ask:

1. Must it survive a process or machine restart?
2. Does it need relational queries, path-based operations, or blob retrieval?
3. Who can read or change it?
4. How long should it live, and how is it deleted?
5. Does it contain sensitive information?
6. Can concurrent agent runs access it safely?

## Agent state is not one thing

- **Run state:** current messages, tool results, plan, and progress needed to finish a run.
- **Thread/conversation state:** information needed to continue a conversation later.
- **Application records:** ownership, permissions, status, billing, and audit history.
- **Working files:** intermediate artifacts the agent creates or reads.

A framework may offer checkpoints or a virtual filesystem, but that does not automatically define the application's retention, tenant isolation, or authorization model. Decide those at the app level.

## Containerization in plain terms

- **Image:** a versioned package of application code, runtime, and dependencies.
- **Container:** a running instance of an image.
- **Volume:** storage mounted into a container to retain or share data across container replacement.
- **Compose:** a local way to define and start multiple connected services.

For an agent app, containers can make the web server, API, worker, database, and cache easier to run consistently. They do not by themselves make a service secure, durable, or isolated. Secrets should be supplied at runtime; persistent files should use an intentional volume or external storage service.

## Example whiteboard architecture

```text
Browser
  │ HTTPS + streamed events
  ▼
Web/API service ───────► Model provider
  │                         ▲
  ├── agent runner ─────────┘
  │       ├── bounded tools ─► application services
  │       └── workspace ─────► temporary job files
  ├── database ─────────────► durable records and run metadata
  ├── object storage ───────► uploads and generated artifacts
  └── cache ────────────────► short-lived/reusable values
```

## Discussion: what belongs where?

| Data | Suggested starting point | Reason |
|---|---|---|
| User profile and permissions | Database | Structured, durable, queried frequently |
| Uploaded PDF | Object storage | Large binary object with controlled access and lifecycle |
| Extracted page text for one run | Temporary workspace or object storage | Depends on whether it must be reused after the run |
| Agent plan and events | Run state/checkpoint store plus chosen retention policy | Needed to resume or inspect the run; avoid accidental indefinite retention |
| Final category totals | Database | Structured business result that users query later |
| Repeated vendor metadata | Cache with an expiry, backed by a source of truth | Speed up reads without making cache authoritative |

## Instructor caveat

Keep the distinction between file storage and object storage understandable rather than dogmatic. Some clouds expose object storage through filesystem-like interfaces; the important teaching point is the access pattern, durability, ownership, and lifecycle contract.
