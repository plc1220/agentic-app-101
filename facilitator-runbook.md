# Facilitator runbook — simple version

## Workshop goal

Help a mostly non-technical audience understand what an AI agent does, where it fits inside an app, and what the basic data services are for. Participants do not install or run code during the workshop. They take home the repository and can try the script later.

## Suggested 2-hour session

| Time | Segment | Explain it simply |
|---|---|---|
| 0:00–0:10 | Welcome | Today: a helpful AI assistant with a small toolbox |
| 0:10–0:25 | What is an agent? | It can choose an approved tool, see the result, and answer |
| 0:25–0:45 | The app around it | Screen, app, AI, and tool |
| 0:45–1:05 | Data homes | Records, big files, working files, quick-access cache |
| 1:05–1:15 | Break | — |
| 1:15–1:25 | Containers | A packed lunchbox for an app; data still needs a proper home |
| 1:25–1:40 | Gemini and tool calling | The model suggests; the application performs |
| 1:40–1:50 | Take-home script | Show source and expected behavior; no installs in class |
| 1:50–2:00 | Questions and recap | Three practical takeaways |

## Running example

A workshop helper answers “When is the backend session?” by asking Gemini to use a tiny Python function that looks up a fixed sample schedule. The audience can understand the input, the one allowed action, and the returned result.

## Plain-language explanations

- Agent: an AI helper that can decide to use a small set of tools.
- Tool: a specific task the application allows, such as looking up a schedule.
- Database: a tidy, searchable list of records.
- Object storage: a cupboard for large files like PDFs and images.
- Working files: a desk for the current task.
- Cache: a quick-access sticky note that may be thrown away.
- Container: a packed version of an app that can be started consistently.

Avoid promising that the model “knows” the schedule. The sample Python tool supplies the schedule data.

## Presenter preparation

- Open the HTML slides and verify arrow-key navigation.
- Walk through `run_agent.py` and explain only the tool function and model call.
- Do not ask attendees to install Python or create API keys during the session.
- Keep the API key out of slides, screen recordings, and Git.
- Have screenshots or a prerecorded terminal run ready in case the API/network is unavailable.
- Use only fictional workshop data; free-tier Gemini prompts may be used to improve Google products.
- Review Google's current pricing/terms and the current demo model immediately before presenting.

## Discussion prompt

“If the assistant looked up a real customer order instead of a workshop timetable, what would we need to protect?” Lead toward identity, authorization, safe tools, and careful data storage without turning this into a security lecture.
