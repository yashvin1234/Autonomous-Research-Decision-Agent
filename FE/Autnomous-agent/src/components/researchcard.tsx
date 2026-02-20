import { useState } from "react";
import type { ResearchFinding } from "../types/agent";
import "../styles/cards.css";

function ResearchCard({ research }: { research: ResearchFinding[] }) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <div className="card">
      <h3>🔎 Research Findings</h3>

      {research.map((r, i) => (
        <div
          key={i}
          className="research-item"
          onClick={() => setOpenIndex(openIndex === i ? null : i)}
        >
          <strong>{r.question}</strong>

          {openIndex === i && (
            <div className="summary">
              <p>{r.summary}</p>
              <small>Sources: {r.sources.join(", ")}</small>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
export default ResearchCard;
