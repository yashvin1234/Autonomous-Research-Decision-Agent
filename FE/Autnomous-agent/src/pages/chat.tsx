import { useState } from "react";
import { useNavigate } from "react-router-dom";
import ChatWindow from "../components/chatwindow";
import "../styles/layout.css";

type Mode = "agent" | "repo";

function Chat() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<Mode>("agent");

  function handleLogout() {
    localStorage.removeItem("token");
    navigate("/auth");
  }

  return (
    <div className="page">
      <div className="sidebar">
        <h3>Modes</h3>

        <button onClick={() => setMode("agent")}>Agent Chat</button>
        <button onClick={() => setMode("repo")}>Repo Chat</button>

        <hr />

        <button onClick={handleLogout}>Logout</button>
      </div>

      <div className="app-card">
        <ChatWindow mode={mode} />
      </div>
    </div>
  );
}

export default Chat;

