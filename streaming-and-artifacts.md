# Streaming chat and artifacts

Reference design for extending the terminal demo into a web application.

## Three kinds of output

- **Text:** parts of one assistant message, assembled in order.
- **Activity:** actual tool and run status, such as reading documents or waiting for approval.
- **Artifacts:** saved outputs with an identity and version, such as reports, images or CSV files.

Streaming makes partial output visible earlier. It does not remove tool latency or guarantee a shorter total run. Avoid showing invented progress percentages or presenting internal reasoning as a tool trace.

## Delivery options

A fetch response can stream framed JSON or SSE-formatted events. Native `EventSource` uses a GET subscription, so creating a run with POST and then subscribing by run ID is one possible design. WebSockets support two-way messages on an open connection. Polling a job endpoint can be sufficient for infrequent status changes.

The backend and proxy must pass incremental output through. Heartbeats can keep a quiet connection active when a tool takes time. A separate agent worker also needs a channel back to the API; an in-process callback alone will not cross container boundaries.

## Example event contract

These are application-defined event names, not Deep Agents or Gemini SDK API names.

```json
{
  "run_id": "run-123",
  "message_id": "message-456",
  "event_id": 12,
  "type": "message.delta",
  "payload": {"text": "The reports agree on "}
}
```

| Event | Frontend behavior |
|---|---|
| `run.started` | Show accepted/in-progress state |
| `message.delta` | Append text to the matching message |
| `tool.started` / `tool.finished` | Update activity without mixing it into answer text |
| `artifact.ready` | Create or update the artifact card |
| `run.completed` | Mark the run complete |
| `run.failed` | Keep any partial output marked incomplete and show the error |
| `run.cancelled` | Stop the indicator and show cancellation |

Decode bytes incrementally and buffer until a complete event is available. One network chunk is not necessarily one token, JSON object or SSE event. Use stable IDs, ordering and duplicate handling when replaying events.

## Rendering

Maintain structured state for conversations, messages, runs, tools and artifacts. Reuse one assistant message component while text arrives. Batch rendering updates; avoid adding a new chat bubble for every delta.

A Markdown renderer needs to handle partial code fences, tables and links. Sanitize or disable raw HTML. Render source citations separately from application controls. Keep auto-scroll conditional on the reader being near the bottom and avoid announcing every token to assistive technology.

Separate the conversation from an artifact preview panel. An artifact card should identify its type, title, version and status. The preview can use a type-specific renderer: Markdown, table/CSV, image or document viewer. Generated HTML requires an isolated preview with restricted execution and network permissions.

## Persistence and delivery

Store final messages and run status in the database. Store artifact bytes in object storage and keep the object key, content type, size, owner and version in a database record. The backend coordinates these writes and emits `artifact.ready` only after both are usable.

The API checks the current viewer’s authorization before returning a download response or a short-lived signed URL. A storage URL should not be treated as an authorization policy. A revised report gets a new version so approvals refer to a specific output.

A cache can accelerate reads. Durable conversations, jobs and artifact metadata need an authoritative store independent of cache expiry.

## Cancellation, retry and reconnect

- A browser abort stops its stream consumption; backend cancellation must be propagated to the worker and provider separately.
- Cancelling cannot undo a write that already happened.
- Reconnect using the same run ID. Resume after the last event ID only if the server supports retained event replay; otherwise fetch a saved snapshot.
- Replaying events and restarting work are different actions. Use an idempotency key to prevent accidental duplicate jobs on retry.
- A closed connection does not establish successful completion. Use an explicit final run state.
- For long jobs, execution and saved progress should not depend on a browser tab staying open.

## Workshop discussion

A report takes 45 seconds to generate. Decide what the user sees after submitting, during a document lookup, while text arrives, after pressing Stop, after refreshing, and when the finished file becomes available.

## References

- [MDN: server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
- [MDN: readable streams](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API/Using_readable_streams)
- [Deep Agents streaming](https://docs.langchain.com/oss/python/deepagents/streaming)
- [FastAPI response types](https://fastapi.tiangolo.com/advanced/custom-response/)
