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


    plan = run_planner(goal, chat.id, db)
    research = run_research(plan, chat.id,db)
    decision = run_decision(plan, research, chat.id,db)

    crud.add_message(db, chat.id, "assistant", decision.final_recommendation)

    return {
        "chat_id": chat.id,
        "plan": plan,
        "research": research,
        "decision": decision
    }

@router.get("/my-chats")
def list_chats(db: Session = Depends(get_db), email: str = Depends(get_current_user)):
    user = crud.get_user_by_email(db, email)

    chats = crud.get_user_chats(db, user.id)

    return [
        {
            "id": chat.id,
            "title": chat.title,
            "created_at": chat.created_at
        }
        for chat in chats
    ]

@router.get("/{chat_id}")
def get_chat(chat_id: int, db: Session = Depends(get_db), email: str = Depends(get_current_user)):
    user = crud.get_user_by_email(db, email)

    chat = crud.get_chat(db, chat_id)

    if not chat or chat.user_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    messages =crud.get_chat_messages(db, chat_id)

    return [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in messages
    ]