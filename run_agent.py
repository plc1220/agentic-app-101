"""A tiny Gemini agent demo: ask about the workshop and watch it use one tool."""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

SESSIONS = {
    "welcome": {"time": "9:00 AM", "topic": "Welcome and what makes an app agentic"},
    "backend": {"time": "9:30 AM", "topic": "Backend basics: database, files, and cache"},
    "containers": {"time": "10:15 AM", "topic": "Containerization"},
    "agent": {"time": "10:45 AM", "topic": "How the agent works and tool calling"},
    "demo": {"time": "11:15 AM", "topic": "Full-stack demo and discussion"},
}
ALIASES = {
    "welcome": ("welcome", "start", "beginning"),
    "backend": ("backend", "database", "files", "cache"),
    "containers": ("container", "containers", "docker"),
    "agent": ("agent", "tool", "tools"),
    "demo": ("demo", "example", "discussion"),
}


def find_workshop_session(topic: str) -> dict:
    """Look up the time and name of a workshop session by topic.

    Args:
        topic: The topic the attendee wants to find, such as backend, containers, or demo.
    """
    search = topic.lower().strip()
    for keyword, session in SESSIONS.items():
        if any(alias in search for alias in ALIASES[keyword]):
            print(f"\n[The agent used its workshop lookup tool: {keyword}]\n")
            return session
    print("\n[The agent used its workshop lookup tool]\n")
    return {"message": "I couldn't find that session. Try welcome, backend, containers, agent, or demo."}


def main() -> None:
    if not os.getenv("GEMINI_API_KEY"):
        print("Gemini API key not found. Add GEMINI_API_KEY to the .env file first.")
        return

    client = genai.Client()
    print("Agentic App 101 helper")
    print("Ask when a workshop session is, or type 'quit' to leave.\n")

    try:
        while True:
            question = input("You: ").strip()
            if question.lower() in {"quit", "exit", "q"}:
                print("See you at the workshop!")
                break
            if not question:
                continue

            response = client.models.generate_content(
                model=MODEL,
                contents=question,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are a friendly workshop helper. Use the workshop lookup tool "
                        "when asked about session times or topics. Answer briefly and plainly. "
                        "If the tool has no matching session, say so."
                    ),
                    tools=[find_workshop_session],
                ),
            )
            print(f"Agent: {response.text or 'I could not produce a text answer.'}\n")
    except KeyboardInterrupt:
        print("\nSee you at the workshop!")
    finally:
        client.close()


if __name__ == "__main__":
    main()
