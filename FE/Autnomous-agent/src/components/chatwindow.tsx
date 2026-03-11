import { useState, useEffect } from "react";
import "../styles/chat.css";
import { runAgent, askRepo, loadRepo, getChatMessages } from "../services/api";
import type { PlannerOutput, ResearchFinding, DecisionOutput } from "../types/agent";
import MessageBubble from "./messagebubble";
import InputBox from "./inputbox";

import PlanCard from "./plancard";
import ResearchCard from "./researchcard";
import DecisionCard from "./decisioncard";

type Mode = "agent" | "repo";

type AgentData = {
  plan: PlannerOutput;
  research: ResearchFinding[];
  decision: DecisionOutput;
};

interface Props {
  mode: Mode;
  chatId: number | null;
  onNewChatCreated: () => void;
}

interface Message {
  role: "user" | "assistant";
  text?: string;
  data?: AgentData;
}

function ChatWindow({ mode, chatId, onNewChatCreated }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [internalChatId, setInternalChatId] = useState<number | null>(chatId);
  const [activeRepoId, setActiveRepoId] = useState<number | null>(null);

  // 🔥 When sidebar changes chat
  useEffect(() => {
  console.log("chatId changed:", chatId);
}, [chatId]);
  useEffect(() => {
    if (chatId === null) {
      setMessages([]);
      setInternalChatId(null);
      return;
    }

    async function loadMessages() {
      const data = await getChatMessages(chatId!);

      const formatted: Message[] = data.map((msg: any) => ({
        role: msg.role,
        text: msg.content,
      }));

      setMessages(formatted);
      setInternalChatId(chatId);
    }

    loadMessages();
  }, [chatId]);

  const sendMessage = async (input: string) => {
    setMessages(prev => [...prev, { role: "user", text: input }]);
    setMessages(prev => [...prev, { role: "assistant", text: "Thinking..." }]);
    setLoading(true);

    try {
      // ===== AGENT MODE =====
      if (mode === "agent") {
        const response = await runAgent(input, internalChatId ?? undefined);

        // If new chat was created
        if (!internalChatId) {
          setInternalChatId(response.chat_id);
          onNewChatCreated(); // refresh sidebar
        }

        setMessages(prev => prev.slice(0, -1));

        setMessages(prev => [
          ...prev,
          {
            role: "assistant",
            data: {
              plan: response.plan,
              research: response.research,
              decision: response.decision,
            },
          },
        ]);
      }

      // ===== REPO MODE =====
      else {
        if (!activeRepoId) {
          const res = await loadRepo(input);
          setActiveRepoId(res.repo_id);

          setMessages(prev => [
            ...prev.slice(0, -1),
            { role: "assistant", text: `Repo indexed. Ask your question.` },
          ]);
        } else {
          const res = await askRepo(activeRepoId, input);

          setMessages(prev => [
            ...prev.slice(0, -1),
            { role: "assistant", text: res.answer },
          ]);
        }
      }

    } catch (err) {
      setMessages(prev => [
        ...prev.slice(0, -1),
        { role: "assistant", text: "Something went wrong." },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="chat-root">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <MessageBubble key={index} role={msg.role}>
            {msg.text && <p>{msg.text}</p>}

            {msg.data && (
              <>
                <PlanCard plan={msg.data.plan} />
                <ResearchCard research={msg.data.research} />
                <DecisionCard decision={msg.data.decision} />
              </>
            )}
          </MessageBubble>
        ))}
      </div>

      <div className="chat-input-area">
        <InputBox
          loading={loading}
          onSend={sendMessage}
          placeholder={
            mode === "repo"
              ? activeRepoId
                ? "Ask question about repo..."
                : "Paste GitHub repo URL..."
              : "Enter your goal..."
          }
        />
      </div>
    </div>
  );
}

export default ChatWindow;


