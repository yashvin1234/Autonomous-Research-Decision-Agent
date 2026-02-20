import "../styles/messagebubble.css";

interface Props {
  role: "user" | "assistant";
  children: React.ReactNode;
}

function MessageBubble({ role, children }: Props) {
  return (
    <div className={`message ${role}`}>
      {children}
    </div>
  );
}
export default MessageBubble;

