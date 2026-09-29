# Workshop illustrations

Generated with the built-in GPT image tool for this workshop.

- `agent-streaming-comic.png`: tool lookup, streaming text and report review.
- `agent-review-chibi.png`: reviewing documents and an output checklist.
- `agent-rag-comic.png`: retrieve a source, supply excerpts, and generate an answer with evidence (slide 12).
- `agent-containers-comic.png`: image, running container, and separate persistent storage (slide 17).
- `agent-skills-tools-mcp-comic.png`: task guidance, a tool operation, and an MCP service connection (slide 40).

The three additional comics use `agent-streaming-comic.png` as their character and style reference: coral robot, dark teal outlines, sage accents and warm cream paper. Exact generation prompts are recorded in [comic-prompts.md](comic-prompts.md). All were generated with the built-in GPT image tool.

The HTML builder embeds the original PNG files as data URLs, so the deck works offline as a single HTML file. Text and architecture diagrams remain native HTML/SVG for editing and accessibility. Rebuild with `python3 deck/build.py` after changing content.
