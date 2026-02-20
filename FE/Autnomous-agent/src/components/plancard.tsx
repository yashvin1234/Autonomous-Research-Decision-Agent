import type { PlannerOutput } from "../types/agent";
import "../styles/cards.css";

function PlanCard({ plan }: { plan: PlannerOutput }) {
  return (
    <div className="card">
      <h3>🧠 Intent</h3>
      <p>{plan.intent}</p>

      <h3>📋 Research Questions</h3>
      <ul className="list">
        {plan.research_questions.map((q, i) => (
          <li key={i}>{q}</li>
        ))}
      </ul>

      <h3>📊 Evaluation Criteria</h3>
      <ul className="list">
        {plan.evaluation_criteria.map((c, i) => (
          <li key={i}>{c}</li>
        ))}
      </ul>
    </div>
  );
}
export default PlanCard;