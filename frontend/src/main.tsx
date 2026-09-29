import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  ArrowUp,
  Square,
  Plus,
  FileText,
  Download,
  X,
  Upload,
  Layers,
  BookOpen,
  MessageSquare,
  Check,
  LoaderCircle,
  ChevronDown,
  Sparkles,
  PanelRightClose,
  PanelRightOpen,
  Search,
  AlertCircle,
} from "lucide-react";
import "./style.css";

type Conversation = { id: string; title: string; created: number };
type Doc = {
  id: string;
  title: string;
  size: number;
  sample: boolean;
  download_url: string;
};
type Artifact = {
  id: string;
  title: string;
  size: number;
  run_id: string;
  download_url: string;
  content?: string;
};
type Message = {
  id: string;
  run_id: string;
  role: string;
  content: string;
  status: string;
};
type Boot = {
  mode: string;
  model: string;
  configured: boolean;
  stack: Record<string, string>;
  conversations: Conversation[];
  documents: Doc[];
};
type Detail = {
  id: string;
  title: string;
  active_run: string | null;
  messages: Message[];
  artifacts: Artifact[];
  runs: { id: string; status: string }[];
};
type Activity = { id: string; name: string; state: string };

async function api<T>(url: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(url, {
    ...options,
    headers: { "X-Requested-With": "workshop", ...options.headers },
  });
  if (!response.ok) {
    const body = await response
      .json()
      .catch(() => ({ detail: "Request failed" }));
    throw new Error(
      typeof body.detail === "string"
        ? body.detail
        : "Please check your input.",
    );
  }
  return response.json();
}
const labels: Record<string, string> = {
  search_documents: "Search documents",
  read_document: "Read document",
  create_report: "Create report",
  read_file: "Read skill / working file",
  write_file: "Write working file",
  edit_file: "Edit working file",
  ls: "List working files",
  glob: "Find working files",
  grep: "Search working files",
  task: "Delegate task",
};
function Markdown({ text }: { text: string }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      skipHtml
      components={{
        img: ({ alt }) => <span>[Image: {alt || "image"}]</span>,
        a: ({ children, href }) => (
          <a href={href} target="_blank" rel="noopener noreferrer">
            {children}
          </a>
        ),
      }}
    >
      {text}
    </ReactMarkdown>
  );
}
const prompts = [
  {
    title: "Compare the reports",
    sub: "Find similarities and differences",
    text: "Compare the three regional reports. Highlight the differences in cost assumptions and cite your sources.",
  },
  {
    title: "Create a briefing",
    sub: "Generate a downloadable report",
    text: "Read the three reports and create a one-page briefing as a downloadable Markdown report. Include a comparison, open questions and source links.",
  },
  {
    title: "Find the main risks",
    sub: "Ask a question grounded in the data",
    text: "What are the main operational risks across the three reports? Cite the reports and suggest questions for the teams.",
  },
];

function App() {
  const [boot, setBoot] = useState<Boot | null>(null),
    [error, setError] = useState(""),
    [draft, setDraft] = useState("");
  const [conversation, setConversation] = useState<Detail | null>(null),
    [activeRun, setActiveRun] = useState<string | null>(null);
  const [busy, setBusy] = useState(false),
    [uploading, setUploading] = useState(false),
    [connected, setConnected] = useState(true);
  const [activities, setActivities] = useState<Activity[]>([]),
    [cacheInfo, setCacheInfo] = useState("");
  const [artifact, setArtifact] = useState<Artifact | null>(null),
    [rightOpen, setRightOpen] = useState(true),
    [showStack, setShowStack] = useState(false);
  const [tab, setTab] = useState<"sources" | "artifacts">("sources");
  const scroll = useRef<HTMLDivElement>(null),
    input = useRef<HTMLTextAreaElement>(null),
    upload = useRef<HTMLInputElement>(null);
  const nearBottom = useRef(true),
    selected = useRef<string | null>(null),
    pendingRequest = useRef<{
      prompt: string;
      conversation: string;
      id: string;
    } | null>(null);
  const streamGeneration = useRef(0);
  async function refreshBoot() {
    const data = await api<Boot>("/api/bootstrap");
    setBoot(data);
    return data;
  }
  useEffect(() => {
    refreshBoot()
      .then((data) => {
        const saved = localStorage.getItem("workshop-conversation");
        if (saved && data.conversations.some((c) => c.id === saved))
          loadConversation(saved);
      })
      .catch((e) => setError(e.message));
  }, []);
  useEffect(() => {
    if (conversation?.messages.length && nearBottom.current && scroll.current)
      scroll.current.scrollTop = scroll.current.scrollHeight;
  }, [conversation?.messages, activities]);

  async function loadConversation(id: string) {
    localStorage.setItem("workshop-conversation", id);
    selected.current = id;
    setError("");
    setArtifact(null);
    setActivities([]);
    setCacheInfo("");
    setActiveRun(null);
    try {
      const detail = await api<Detail>(`/api/conversations/${id}`);
      if (selected.current !== id) return;
      setConversation(detail);
      setActiveRun(detail.active_run);
      nearBottom.current = true;
    } catch (e) {
      if (selected.current === id) setError((e as Error).message);
    }
  }
  function newConversation() {
    localStorage.removeItem("workshop-conversation");
    selected.current = null;
    setConversation(null);
    setActiveRun(null);
    setArtifact(null);
    setActivities([]);
    setCacheInfo("");
    setError("");
    pendingRequest.current = null;
    input.current?.focus();
  }
  async function showArtifact(item: Artifact) {
    setTab("artifacts");
    setRightOpen(true);
    try {
      const value = await api<Artifact>(`/api/artifacts/${item.id}`);
      setArtifact(value);
    } catch (e) {
      setError((e as Error).message);
    }
  }

  useEffect(() => {
    if (!activeRun || !conversation) return;
    const id = conversation.id,
      generation = ++streamGeneration.current;
    setConnected(true);
    setActivities([]);
    setCacheInfo("");
    // Replay the complete run after refresh. Native EventSource resumes by event ID after a transient disconnect.
    setConversation((old) =>
      old
        ? {
            ...old,
            messages: old.messages.map((m) =>
              m.run_id === activeRun && m.role === "assistant"
                ? { ...m, content: "", status: "streaming" }
                : m,
            ),
          }
        : old,
    );
    const source = new EventSource(`/api/runs/${activeRun}/events`);
    source.onopen = () => setConnected(true);
    source.onerror = () => setConnected(false);
    source.onmessage = (event) => {
      if (selected.current !== id || streamGeneration.current !== generation)
        return;
      let item: { type: string; payload: any };
      try {
        item = JSON.parse(event.data);
      } catch {
        return;
      }
      const p = item.payload;
      if (item.type === "message.delta")
        setConversation((old) =>
          old
            ? {
                ...old,
                messages: old.messages.map((m) =>
                  m.run_id === activeRun && m.role === "assistant"
                    ? { ...m, content: m.content + p.text }
                    : m,
                ),
              }
            : old,
        );
      if (item.type === "tool.started")
        setActivities((old) =>
          old.some((a) => a.id === p.id)
            ? old
            : [...old, { id: p.id, name: p.name, state: "running" }],
        );
      if (item.type === "tool.finished")
        setActivities((old) =>
          old.map((a) =>
            a.id === p.id
              ? { ...a, state: p.status === "error" ? "error" : "complete" }
              : a,
          ),
        );
      if (item.type === "cache.hit" || item.type === "cache.miss")
        setCacheInfo(
          `${item.type === "cache.hit" ? "Cache hit" : "Read from storage"} · ${p.document}`,
        );
      if (item.type === "artifact.ready") {
        setConversation((old) =>
          old
            ? {
                ...old,
                artifacts: old.artifacts.some((a) => a.id === p.id)
                  ? old.artifacts
                  : [...old.artifacts, p],
              }
            : old,
        );
        setTab("artifacts");
        setRightOpen(true);
      }
      if (
        ["run.completed", "run.failed", "run.cancelled"].includes(item.type)
      ) {
        source.close();
        setActiveRun(null);
        setConnected(true);
        setActivities((old) =>
          old.map((a) =>
            a.state === "running" ? { ...a, state: "stopped" } : a,
          ),
        );
        if (p.error) setError(p.error);
        api<Detail>(`/api/conversations/${id}`)
          .then((value) => {
            if (selected.current === id) setConversation(value);
          })
          .catch((e) => setError(e.message));
        refreshBoot().catch(() => {});
      }
    };
    return () => {
      source.close();
    };
  }, [activeRun, conversation?.id]);

  async function send(event?: React.FormEvent) {
    event?.preventDefault();
    const prompt = draft.trim();
    if (!prompt || activeRun || busy || !boot?.configured) return;
    setBusy(true);
    setError("");
    nearBottom.current = true;
    try {
      let id = conversation?.id;
      if (!id) {
        const created = await api<Conversation>("/api/conversations", {
          method: "POST",
        });
        id = created.id;
        selected.current = id;
        localStorage.setItem("workshop-conversation", id);
        setConversation({
          ...created,
          active_run: null,
          messages: [],
          artifacts: [],
          runs: [],
        });
      }
      if (
        !pendingRequest.current ||
        pendingRequest.current.prompt !== prompt ||
        pendingRequest.current.conversation !== id
      )
        pendingRequest.current = {
          prompt,
          conversation: id,
          id: crypto.randomUUID(),
        };
      const result = await api<{ run_id: string; status: string }>(
        `/api/conversations/${id}/runs`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            prompt,
            request_id: pendingRequest.current.id,
          }),
        },
      );
      pendingRequest.current = null;
      setDraft("");
      const detail = await api<Detail>(`/api/conversations/${id}`);
      if (selected.current === id) {
        setConversation(detail);
        setActiveRun(result.run_id);
      }
      refreshBoot().catch(() => {});
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function cancel() {
    if (!activeRun) return;
    try {
      await api(`/api/runs/${activeRun}/cancel`, { method: "POST" });
    } catch (e) {
      setError((e as Error).message);
    }
  }
  async function addDocument(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;
    if (file.size > 1_000_000) {
      setError("Choose a text or Markdown file smaller than 1 MB.");
      event.target.value = "";
      return;
    }
    setUploading(true);
    setError("");
    const data = new FormData();
    data.append("file", file);
    try {
      await api("/api/documents", { method: "POST", body: data });
      await refreshBoot();
      setTab("sources");
      setRightOpen(true);
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }
  const artifacts = conversation?.artifacts || [];
  return (
    <div className={"app " + (!rightOpen ? "panel-hidden" : "")}>
      <aside className="sidebar">
        <a className="brand" href="/" aria-label="Agentic App 101 home">
          <span className="brand-icon">
            <Sparkles size={19} />
          </span>
          <span>
            Agentic App <b>101</b>
            <small>WORKSHOP TUTORIAL</small>
          </span>
        </a>
        <button className="new-chat" onClick={newConversation} disabled={busy}>
          <Plus size={17} />
          New conversation
        </button>
        <div className="sidebar-label">CONVERSATIONS</div>
        <nav className="conversations" aria-label="Saved conversations">
          {boot?.conversations.length ? (
            boot.conversations.map((c) => (
              <button
                key={c.id}
                className={conversation?.id === c.id ? "selected" : ""}
                onClick={() => loadConversation(c.id)}
                disabled={busy}
              >
                <MessageSquare size={15} />
                <span>{c.title}</span>
              </button>
            ))
          ) : (
            <p className="muted tiny">Your conversations will appear here.</p>
          )}
        </nav>
        <div className="sidebar-bottom">
          <button onClick={() => setShowStack(true)}>
            <Layers size={16} />
            Explore the stack
          </button>
          <a
            href="https://github.com/plc1220/agentic-app-101"
            target="_blank"
            rel="noreferrer"
          >
            <BookOpen size={16} />
            Tutorial & source code
          </a>
          <div className="local-note">
            <i />
            Running on your computer
          </div>
        </div>
      </aside>
      <main className="main">
        <header>
          <div>
            <span className="eyebrow">DOCUMENT ASSISTANT</span>
            <h1>{conversation?.title || "New conversation"}</h1>
          </div>
          <div className="header-actions">
            <button
              className="icon-button"
              aria-label="New conversation"
              title="New conversation"
              onClick={newConversation}
              disabled={busy}
            >
              <Plus size={19} />
            </button>
            <span
              className={"mode " + (boot?.mode === "sample" ? "sample" : "")}
            >
              <i />
              {boot?.mode === "sample"
                ? "Sample · no AI"
                : "Deep Agents + Gemini"}
            </span>
            <button
              className="icon-button"
              title={rightOpen ? "Hide documents" : "Show documents"}
              aria-label={rightOpen ? "Hide documents" : "Show documents"}
              onClick={() => setRightOpen(!rightOpen)}
            >
              {rightOpen ? (
                <PanelRightClose size={19} />
              ) : (
                <PanelRightOpen size={19} />
              )}
            </button>
          </div>
        </header>
        <div
          className="chat-scroll"
          ref={scroll}
          onScroll={() => {
            const e = scroll.current;
            if (e)
              nearBottom.current =
                e.scrollHeight - e.scrollTop - e.clientHeight < 90;
          }}
        >
          {!conversation?.messages.length ? (
            <section className="welcome">
              <span className="welcome-icon">
                <BookOpen size={30} />
              </span>
              <div className="eyebrow">FROM DOCUMENTS TO ANSWERS</div>
              <h2>
                Ask. Compare.
                <br />
                <em>Create a briefing.</em>
              </h2>
              <p>
                Explore three sample reports, follow the agent’s tools,
                <br className="desktop" /> and turn the findings into a
                downloadable document.
              </p>
              <div className="prompt-grid">
                {prompts.map((p, i) => (
                  <button
                    key={p.title}
                    onClick={() => {
                      setDraft(p.text);
                      input.current?.focus();
                    }}
                  >
                    <span className="prompt-number">0{i + 1}</span>
                    <strong>{p.title}</strong>
                    <span>{p.sub}</span>
                    <ArrowUp size={15} />
                  </button>
                ))}
              </div>
              <div className="sample-caption">
                Three fictional regional reports are ready in Sources.
              </div>
            </section>
          ) : (
            <div className="messages">
              {conversation.messages.map((m) => (
                <article className={"message " + m.role} key={m.id}>
                  <div className="message-author">
                    {m.role === "assistant" ? (
                      <>
                        <span className="avatar">
                          <Sparkles size={14} />
                        </span>
                        Document assistant
                      </>
                    ) : (
                      <>You</>
                    )}
                    {m.status === "failed" || m.status === "cancelled" ? (
                      <span className="message-state">
                        {m.status} · partial response
                      </span>
                    ) : null}
                  </div>
                  <div className="message-content">
                    {m.content ? (
                      <Markdown text={m.content} />
                    ) : m.status === "streaming" ? (
                      <span className="thinking">
                        <LoaderCircle size={15} className="spin" />
                        Working with your documents…
                      </span>
                    ) : (
                      <span className="muted">No response text.</span>
                    )}
                  </div>
                  {m.role === "assistant" &&
                    artifacts
                      .filter((a) => a.run_id === m.run_id)
                      .map((a) => (
                        <button
                          className="artifact-inline"
                          key={a.id}
                          onClick={() => showArtifact(a)}
                        >
                          <FileText size={20} />
                          <span>
                            <strong>{a.title}</strong>
                            <small>Markdown · open preview</small>
                          </span>
                          <ChevronDown size={17} />
                        </button>
                      ))}
                </article>
              ))}
            </div>
          )}
        </div>
        <div className="composer-area">
          {activities.length > 0 && (
            <details className="activity" open={!!activeRun}>
              <summary>
                <span>
                  {activeRun ? (
                    <LoaderCircle size={14} className="spin" />
                  ) : (
                    <Check size={14} />
                  )}
                  Agent activity
                </span>
                <span>
                  {activities.length} actions
                  <ChevronDown size={13} />
                </span>
              </summary>
              <div className="activity-content">
                {activities.map((a) => (
                  <div key={a.id}>
                    {a.state === "running" ? (
                      <LoaderCircle className="spin" size={13} />
                    ) : a.state === "error" ? (
                      <AlertCircle size={13} />
                    ) : (
                      <Check size={13} />
                    )}
                    <span>{labels[a.name] || a.name}</span>
                    <small>{a.state}</small>
                  </div>
                ))}
                {cacheInfo && <p>{cacheInfo}</p>}
              </div>
            </details>
          )}
          {!connected && (
            <div className="notice">
              Connection interrupted. Reconnecting to the saved run…
            </div>
          )}
          {!boot?.configured && boot && (
            <div className="notice">
              Add your Gemini key to <code>.env</code> and restart. Or set{" "}
              <code>AGENT_MODE=sample</code> for the offline walkthrough.
            </div>
          )}
          {error && (
            <div className="error" role="alert">
              <AlertCircle size={16} />
              <span>{error}</span>
              <button aria-label="Dismiss error" onClick={() => setError("")}>
                <X size={15} />
              </button>
            </div>
          )}
          <form className="composer" onSubmit={send}>
            <textarea
              ref={input}
              value={draft}
              maxLength={8000}
              onChange={(e) => setDraft(e.target.value)}
              placeholder="Ask about the reports, or request a briefing…"
              aria-label="Message"
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  send();
                }
              }}
            />
            <div className="composer-bottom">
              <span>
                <span className="small-dot" />
                {boot?.mode === "sample"
                  ? "Scripted walkthrough"
                  : boot?.model || "Connecting…"}
              </span>
              {activeRun ? (
                <button
                  type="button"
                  onClick={cancel}
                  className="send"
                  title="Stop generation"
                  aria-label="Stop generation"
                >
                  <Square size={15} />
                </button>
              ) : (
                <button
                  className="send"
                  type="submit"
                  disabled={!draft.trim() || busy || !boot?.configured}
                  title="Send message"
                  aria-label="Send message"
                >
                  {busy ? (
                    <LoaderCircle className="spin" size={18} />
                  ) : (
                    <ArrowUp size={20} />
                  )}
                </button>
              )}
            </div>
          </form>
          <p className="composer-note">
            Review generated answers against their sources.{" "}
            <span>Enter to send · Shift + Enter for a new line</span>
          </p>
        </div>
      </main>
      {rightOpen && (
        <aside className="resources">
          <div className="resource-tabs">
            <button
              className={tab === "sources" ? "active" : ""}
              onClick={() => {
                setTab("sources");
                setArtifact(null);
              }}
            >
              Sources <span>{boot?.documents.length || 0}</span>
            </button>
            <button
              className={tab === "artifacts" ? "active" : ""}
              onClick={() => setTab("artifacts")}
            >
              Artifacts <span>{artifacts.length}</span>
            </button>
          </div>
          {tab === "sources" ? (
            <>
              <div className="resource-heading">
                <h2>Reference documents</h2>
                <p>The agent can search and read these files.</p>
              </div>
              <div className="doc-list">
                {boot?.documents.map((d) => (
                  <a
                    className="document"
                    key={d.id}
                    href={d.download_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    <span className="document-icon">
                      <FileText size={21} />
                    </span>
                    <span>
                      <strong>{d.title}</strong>
                      <small>
                        {d.sample ? "Sample report" : "Uploaded document"} ·{" "}
                        {Math.max(1, Math.ceil(d.size / 1024))} KB
                      </small>
                    </span>
                  </a>
                ))}
              </div>
              <button
                className="upload"
                onClick={() => upload.current?.click()}
                disabled={uploading}
              >
                {uploading ? (
                  <LoaderCircle size={18} className="spin" />
                ) : (
                  <Upload size={18} />
                )}
                <strong>{uploading ? "Uploading…" : "Add a document"}</strong>
                <span>.txt or .md · up to 1 MB</span>
              </button>
              <input
                ref={upload}
                type="file"
                accept=".txt,.md"
                hidden
                onChange={addDocument}
              />
              <div className="source-tip">
                <Search size={17} />
                <p>
                  Ask the agent to compare the reports and explain where their
                  assumptions differ.
                </p>
              </div>
            </>
          ) : artifact ? (
            <>
              <div className="preview-heading">
                <button
                  className="text-button"
                  onClick={() => setArtifact(null)}
                >
                  ← All artifacts
                </button>
                <h2>{artifact.title}</h2>
                <a className="download" href={artifact.download_url}>
                  <Download size={16} />
                  Download Markdown
                </a>
              </div>
              <div className="artifact-preview">
                <Markdown text={artifact.content || ""} />
              </div>
            </>
          ) : (
            <>
              <div className="resource-heading">
                <h2>Generated artifacts</h2>
                <p>Saved reports from this conversation.</p>
              </div>
              {artifacts.length ? (
                <div className="doc-list">
                  {artifacts.map((a) => (
                    <button
                      className="document"
                      key={a.id}
                      onClick={() => showArtifact(a)}
                    >
                      <span className="document-icon">
                        <FileText size={21} />
                      </span>
                      <span>
                        <strong>{a.title}</strong>
                        <small>Markdown · ready to preview</small>
                      </span>
                    </button>
                  ))}
                </div>
              ) : (
                <div className="empty-artifacts">
                  <FileText size={34} />
                  <h3>Your reports appear here</h3>
                  <p>
                    Ask for a downloadable briefing. The agent will save a
                    document you can preview and keep.
                  </p>
                </div>
              )}
            </>
          )}
          <div className="resource-footer">
            AGENTIC APP 101 <span>LEARN BY BUILDING</span>
          </div>
        </aside>
      )}
      {showStack && (
        <div className="modal-backdrop" onClick={() => setShowStack(false)}>
          <section
            className="stack-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="stack-title"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              className="modal-close"
              aria-label="Close stack"
              onClick={() => setShowStack(false)}
            >
              <X size={20} />
            </button>
            <div className="eyebrow">THE RUNNING APPLICATION</div>
            <h2 id="stack-title">Explore the stack</h2>
            <p>Each component has a specific responsibility.</p>
            <div className="stack-list">
              {Object.entries(boot?.stack || {}).map(([name, value]) => (
                <div key={name}>
                  <span>{name}</span>
                  <strong>{value}</strong>
                </div>
              ))}
            </div>
            <p className="stack-foot">
              Messages and events live in the database. Files live in object
              storage. The cache expires; saved records remain.
            </p>
          </section>
        </div>
      )}
    </div>
  );
}
createRoot(document.getElementById("root")!).render(<App />);
