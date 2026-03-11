import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ChatWindow from "../components/chatwindow";
import { getMyChats } from "../services/api";
import "../styles/layout.css";

type Mode = "agent" | "repo";

interface ChatItem {
  id: number;
  title: string;
}

function Chat() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<Mode>("agent");
  const [chats, setChats] = useState<ChatItem[]>([]);
  const [activeChatId, setActiveChatId] = useState<number | null>(null);

  function handleLogout() {
    localStorage.removeItem("token");
    navigate("/auth");
  }

  async function loadChats() {
    const data = await getMyChats();
    setChats(data);
  }

  useEffect(() => {
    loadChats();
  }, []);

  function handleNewChat() {
    setActiveChatId(null);
  }

  function handleSelectChat(id: number) {
    setActiveChatId(id);
  }

  return (
    <div className="page">
      <div className="sidebar">
        <h3>Modes</h3>

        <button onClick={() => setMode("agent")}>Agent Chat</button>
        <button onClick={() => setMode("repo")}>Repo Chat</button>

        <hr />

        <h3>Your Chats</h3>

        <button className="new-chat-btn" onClick={handleNewChat}>
          + New Chat
        </button>

        <div className="chat-list">
          {chats.map((chat) => (
            <div
              key={chat.id}
              className={`chat-item ${
                activeChatId === chat.id ? "active" : ""
              }`}
              onClick={() => handleSelectChat(chat.id)}
            >
              {chat.title}
            </div>
          ))}
        </div>

        <hr />

        <button className="logout-btn" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <div className="app-card">
        <ChatWindow
          mode={mode}
          chatId={activeChatId}
          onNewChatCreated={loadChats}
        />
      </div>
    </div>
  );
}

export default Chat;

