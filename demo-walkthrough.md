# Presenter demo walkthrough

The runnable program is `run_agent.py`. It uses the Google Gen AI SDK with one Python lookup function. Attendees can watch during the session and use the launch scripts later.

## What is implemented

- Local terminal input and output; complete responses rather than token streaming.
- Gemini Developer API call using the explicit key from `.env` beside the script.
- Automatic Python function calling through the SDK.
- A fixed sample workshop timetable and simple keyword aliases.
- A printed message when the lookup function runs.

Each question starts fresh. There is no saved conversation, web frontend, database, deployed service, Deep Agents runtime, or MCP server in the starter. Those appear in the full-day deck as architectural extensions and reference choices.

## Before presenting

1. Install Python 3.10+ and follow `stack-and-setup.md`. The launcher creates `.venv` and installs packages automatically.
2. Get a key from Google AI Studio, using the intended project's tier and quota. A project ID alone does not authenticate requests.
3. Select a model currently available to that key. The `.env` setting can change without changing the code.
4. Rehearse the known, unknown and follow-up examples. The content work has not established a successful live API run.
5. Keep a labelled recording or screenshots for a network/model outage. Keep credentials off-screen.

## Walkthrough sequence

1. Show `SESSIONS`: this is fictional demonstration data, not today's full-day agenda.
2. Show `find_workshop_session`: a normal Python function with a documented input and output.
3. Show `tools=[find_workshop_session]`: this makes the function available to the model through the SDK.
4. Explain the instruction and model setting; identify `google-genai`, `python-dotenv`, the terminal UI and in-memory sample data.
5. Run the program if rehearsed, or use the deck's labelled illustrative transcript.
6. Ask “When is the backend session?” and point out the printed tool event.
7. Ask about an unknown session and discuss what a good missing-data answer looks like.
8. Ask a follow-up such as “What happens after that?” and explain the sample's lack of conversation memory.

The exact wording may vary. A tool exchange can use multiple model calls. Basic keyword matching can return the wrong item for ambiguous topics; discuss that as an application limitation.

## Failure fallback

If credentials, quota, model availability or network access prevents a run, show the source and the labelled example output. Keep the session on schedule; do not spend the class repairing the environment. Do not claim an API test succeeded when only a transcript was shown.

## Optional public references

- [LangChain Deep Agents](https://github.com/langchain-ai/deepagents): framework source and examples.
- [Python Deep Agents tutorial](https://github.com/mkassaf/deepagents-tutorial): community learning examples.
- [deepagentsdk Next.js demo](https://github.com/chrispangg/deepagentsdk-nextjs-demo): earlier full-stack community reference; uses a distinct TypeScript SDK and Anthropic in its README.

These repositories are additional reading. They are not dependencies of this starter, and their setup/version requirements should be checked separately.
