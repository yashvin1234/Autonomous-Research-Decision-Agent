import { useState } from "react";
import "../styles/chat.css";
import { runAgent, askRepo, loadRepo } from "../services/api";
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
}

interface Message {
  role: "user" | "assistant";
  text?: string;
  data?: AgentData;
}

function ChatWindow({ mode }: Props) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [chatId, setChatId] = useState<number | null>(null);
  const [activeRepoId, setActiveRepoId] = useState<number | null>(null);

  const sendMessage = async (input: string) => {
    setMessages(prev => [...prev, { role: "user", text: input }]);
    setMessages(prev => [...prev, { role: "assistant", text: "Thinking..." }]);
    setLoading(true);

    try {
      // ===== AGENT MODE (UNCHANGED) =====
      if (mode === "agent") {
        const response = await runAgent(input, chatId ?? undefined);
        if (!chatId) setChatId(response.chat_id);

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
        // Step 1 → load repo
        if (!activeRepoId) {
          const res = await loadRepo(input);
          setActiveRepoId(res.repo_id);

          setMessages(prev => [
            ...prev.slice(0, -1),
            { role: "assistant", text: `Repo indexed. Ask your question.` },
          ]);
        }

        // Step 2 → ask question
        else {
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


