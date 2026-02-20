export type Role = "user" | "assistant" | "system";

export interface ChatMessage {
  id: string;
  role: Role;
  content: string;
  timestamp: number;
}

export interface AgentRequest {
  email: string;
  goal: string;
}

export interface PlannerOutput {
  intent: string;
  research_questions: string[];
  evaluation_criteria: string[];
}

export interface ResearchFinding {
  question: string;
  summary: string;
  sources: string[];
}

export interface DecisionOutput {
  comparison_table: string;
  pros: string[];
  cons: string[];
  final_recommendation: string;
  confidence_score: number;
  key_risks: string[];
}

export interface FullAgentResponse {
  chat_id: number;
  plan: PlannerOutput;
  research: ResearchFinding[];
  decision: DecisionOutput;
}
