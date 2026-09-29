# Participant exercises — no coding required

Use paper or a shared whiteboard. All data is fictional. The facilitator has suggested answers in the notes and the following slides.

## A. Pick a small first job — 5 minutes

- Who needs help?
- What useful output do they want?
- Which source should the assistant consult?

Write: “Help ___ produce/find ___ using ___.”

## B. Sort the data — 8 minutes

Choose a database, object storage, file workspace or cache for:

1. A user ID and the status of a document-processing job.
2. The original PDF and the finished report.
3. Temporary extracted text and a repeated vendor lookup.

For each, explain whether it needs to survive a restart and who can read it.

## C. Find the right folder — 10 minutes

Using the scaffold slide, decide where you would start for each change:

- Make a progress message clearer.
- Add a customer order lookup.
- Keep results after the process restarts.
- Check that unknown questions do not receive invented answers.

More than one folder can be involved. Explain the responsibility of each.

## D. Choose an approach — 6 minutes

A team needs to read several reports and draft a comparison.

- Which framework would you evaluate first, and why?
- Would a skill help maintain the same report format?
- Would a direct function or an existing MCP connection help retrieve documents?
- What evidence would make you change your choice?

## E. Capstone — 60-minute session

Design a document briefing assistant for an operations colleague. It reads three uploaded reports and prepares a one-page draft with sources. A person reviews the result before publication.

| Design question | Your choice |
|---|---|
| User and useful output | |
| Screen and API | |
| Agent and allowed tools | |
| Where original files live | |
| Where ownership and job status live | |
| Where temporary work lives | |
| Where final drafts live | |
| Framework to evaluate and why | |
| Optional skill | |
| Optional MCP connection | |
| Approval point | |
| Failure and recovery path | |
| One quality check | |

The session includes a 5-minute brief, 25 minutes drawing, a 10-minute suggested design, 15 minutes sharing and a 5-minute take-home walkthrough.

## F. Five quick checks — 10 minutes

Explain each answer to a partner:

1. Where should an uploaded PDF usually live?
2. Does choosing Gemini determine which framework to use?
3. How does a skill differ from a tool?
4. What does an MCP server expose?
5. What should the app check before a tool changes a record?
