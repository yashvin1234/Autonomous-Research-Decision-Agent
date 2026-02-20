import { useState } from "react";
import "../styles/inputbox.css";

interface Props {
  onSend: (message: string) => void;
  loading: boolean;
  placeholder?: string;
}

function InputBox({ onSend, loading, placeholder }: Props) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <div className="input-box">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder={placeholder || "Type your goal..."}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
      />
      <button onClick={handleSend} disabled={loading}>
        {loading ? "Thinking..." : "Send"}
      </button>
    </div>
  );
}

export default InputBox;
