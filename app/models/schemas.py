from pydantic import BaseModel, EmailStr
from typing import List, Optional

class GoalRequest(BaseModel):
    goal: str
    chat_id: Optional[int] = None

class SignupRequest(BaseModel):
    email: str
    password: str

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

class RepoRequest(BaseModel):
    repo_url: str

class AskRepoRequest(BaseModel):
    repo_id: int
    question: str