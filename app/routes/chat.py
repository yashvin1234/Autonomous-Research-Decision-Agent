from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.sessions import get_db
from app.db import crud
from app.agents.planner import run_planner
from app.agents.researcher import run_research
from app.agents.decision import run_decision
from app.models.schemas import GoalRequest
from app.core.deps import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])




@router.post("/analyze")
def run_agent(request: GoalRequest, db: Session = Depends(get_db), email: str = Depends(get_current_user)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    goal = request.goal

    if request.chat_id is None:
        chat = crud.create_chat(db, user.id, goal[:40])
    else:
        chat = crud.get_chat(db, request.chat_id)

        if not chat or chat.user_id != user.id:
            raise HTTPException(status_code=403, detail="Unauthorized chat")

    crud.add_message(db, chat.id, "user", goal)


    plan = run_planner(goal, chat.id)
    research = run_research(plan, chat.id)
    decision = run_decision(plan, research, chat.id)

    crud.add_message(db, chat.id, "assistant", decision.final_recommendation)

    return {
        "chat_id": chat.id,
        "plan": plan,
        "research": research,
        "decision": decision
    }



