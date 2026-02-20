import type { DecisionOutput } from "../types/agent";
import "../styles/cards.css";

function DecisionCard({ decision }: { decision: DecisionOutput }) {
  return (
    <div className="card">
      <h3>✅ Final Recommendation</h3>
      <p>{decision.final_recommendation}</p>

      <h3>👍 Pros</h3>
      <ul className="list">
        {decision.pros.map((p, i) => <li key={i}>{p}</li>)}
      </ul>

      <h3>👎 Cons</h3>
      <ul className="list">
        {decision.cons.map((c, i) => <li key={i}>{c}</li>)}
      </ul>

      <h3>⚠ Risks</h3>
      <ul className="list">
        {decision.key_risks.map((r, i) => <li key={i}>{r}</li>)}
      </ul>

      <p><b>Confidence:</b> {(decision.confidence_score * 100).toFixed(1)}%</p>
    </div>
  );
}
export default DecisionCard;
