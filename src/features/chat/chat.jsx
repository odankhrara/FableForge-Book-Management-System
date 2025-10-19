import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchConversations,
  fetchMessages,
  sendMessage,
  setCurrentConversation,
} from "./chatSlice";

export default function Chat() {
  const dispatch = useDispatch();
  const { conversations, messagesById, currentConversationId, userId, sending, error } =
    useSelector((s) => s.chat);

  const [input, setInput] = useState("");

  useEffect(() => {
    dispatch(fetchConversations(userId));
  }, [dispatch, userId]);

  const msgs = currentConversationId ? (messagesById[currentConversationId] || []) : [];

  const onNew = () => dispatch(setCurrentConversation(null));

  const onOpen = (id) => dispatch(fetchMessages(id));

  const onSend = (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;
    dispatch(
      sendMessage({
        user_id: userId,
        message: text,
        conversation_id: currentConversationId || undefined,
        title: currentConversationId ? undefined : "New chat",
      })
    );
    setInput("");
  };

  return (
    <div className="container" style={{ display: "grid", gridTemplateColumns: "260px 1fr", gap: 16 }}>
      <aside style={{ borderRight: "1px solid #eee", paddingRight: 12 }}>
        <h2>Conversations</h2>
        <button className="btn" onClick={onNew}>+ New Chat</button>
        <ul style={{ listStyle: "none", padding: 0, marginTop: 12 }}>
          {conversations.map((c) => (
            <li key={c.id} style={{ marginBottom: 8 }}>
              <button className="btn" onClick={() => onOpen(c.id)}>
                {c.title || `Chat ${c.id}`}
              </button>
            </li>
          ))}
        </ul>
      </aside>

      <main>
        <h2>Chat</h2>
        <div style={{ minHeight: 280, background: "#fff", border: "1px solid #eee",
                      borderRadius: 10, padding: 12, marginBottom: 12, overflowY: "auto" }}>
          {msgs.length === 0 ? (
            <p className="muted">Start a new chat by sending a message.</p>
          ) : (
            msgs.map((m, i) => (
              <div key={i} style={{ margin: "8px 0" }}>
                <strong>{m.role === "user" ? "You" : "Assistant"}:</strong> {m.content}
              </div>
            ))
          )}
        </div>

        {error && <p style={{ color: "red" }}>{String(error)}</p>}

        <form onSubmit={onSend} style={{ display: "flex", gap: 8 }}>
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message…"
            style={{ flex: 1, padding: "10px 12px", borderRadius: 10, border: "1px solid #e5e7eb" }}
          />
          <button className="btn primary" disabled={sending}>
            {sending ? "Sending…" : "Send"}
          </button>
        </form>
      </main>
    </div>
  );
}
