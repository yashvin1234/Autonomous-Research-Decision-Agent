from fastapi import FastAPI

from app.agents.decision import run_decision
from app.agents.planner import run_planner
from app.agents.researcher import run_research
from app.models.schemas import GoalRequest

app = FastAPI(title="Autonomous Research & Decision Agent")

@app.get("/")
def health_check():
    return {"status": "running"}

@app.post("/analyze")
async def analyze_goal(request: GoalRequest):
    plan = run_planner(request.goal)
    research = run_research(plan)
    decision = run_decision(plan, research)

    return {
        "plan": plan,
        "research": research,
        "decision": decision
    }
#fewfee