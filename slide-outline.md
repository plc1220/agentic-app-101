# Slide outline — Agentic App 101

Target: 12–14 slides for a three-hour workshop, with live walkthrough and discussion.

## 1. Title: Agentic App 101

Subtitle: From backend building blocks to a running agent application.
Speaker note: Set the expectation that this is application architecture, not a prompt-engineering session.

## 2. Learning goals

- Sketch the main pieces of a full-stack agent app.
- Choose a home for durable data, files, and cached values.
- Explain what containerization gives the development workflow.
- Trace a request through a Deep Agents example.

## 3. A chatbot versus an agentic app

Diagram: User → app API → model; then agent loop: model → selected tool → result → model → answer.
Point: tools and control flow make actions possible; the surrounding app still owns policy and product behavior.

## 4. Reference architecture

Diagram: Browser UI → application API → agent framework → model provider; agent tools → application services/data. Add streaming events back to UI.
Speaker note: Keep the model provider outside the app boundary and mark network calls/failure points.

## 5. Where does the data go?

Use invoice assistant examples: DB = job/status/metadata; object storage = original PDF/report; workspace = temporary processing files; cache = reusable lookup/short-lived result.
Question: Which item must survive a restart?

## 6. Storage roles at a glance

Table from `backend-building-blocks.md`. Emphasize lifecycle, ownership, and access controls.

## 7. Containers in one picture

Diagram: image → running container; Compose connects web, API, DB; volume/external storage holds persistent state.
Callout: environment variables and secrets are injected at runtime.

## 8. Deep Agents: the useful mental model

Show model + instructions + tools + harness/runtime + state. Explain framework as reusable control and middleware, not a replacement for application architecture.

## 9. What makes a “deep” agent?

Concept cards: planning, filesystem/workspace, context management, subagents/delegation. Explain these are ways to manage longer tasks; they are not automatically required for every use case.

## 10. The demo repo and its boundaries

Show repo architecture: Next.js UI → `/api/chat` → TypeScript `deepagentsdk` → local sandbox; stream events to chat/file explorer.
Disclosure: this is a community demo and uses the TypeScript SDK. It is not the Python `deepagents` package and does not demonstrate a production database/object-storage/cache stack.

## 11. Live walkthrough: follow one request

1. Enter prompt.
2. Inspect API route and agent configuration.
3. Watch event stream and tool activity.
4. Inspect created file in workspace.
5. Change one instruction and rerun.

## 12. Application responsibilities around the agent

Identity and authorization; input validation; tool limits; error handling; persistence; user confirmation; observability; quotas/cost controls.

## 13. Small-group design prompt

“Build an assistant that reads uploaded invoices and drafts an expense summary.” Teams sketch API, agent capability, database record, object storage, workspace, cache, and approval point.

## 14. Wrap-up

Three takeaways: make capabilities explicit; put data in the right store; choose the simplest orchestration that meets the task. Add links to demo and Python tutorial.
