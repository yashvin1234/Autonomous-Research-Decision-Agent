from pydantic import BaseModel
from typing import List, Optional

class GoalRequest(BaseModel):
    goal: str
    session_id: str

class PlannerOutput(BaseModel):
    intent: str
    research_questions: List[str]
    evaluation_criteria: List[str]

class ResearchFinding(BaseModel):
    question: str
    summary: str
    sources: List[str]

class DecisionOutput(BaseModel):
    comparison_table: str
    pros: List[str]
    cons: List[str]
    final_recommendation: str
    confidence_score: float
    key_risks: List[str]
