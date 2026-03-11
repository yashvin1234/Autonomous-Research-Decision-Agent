from langchain_core.messages import HumanMessage, AIMessage
from sqlalchemy.orm import Session

from app.db.crud import get_chat_messages

def build_chat_input(db: Session, chat_id: int, new_input: str):

    history = get_chat_messages(db, chat_id)

    messages = []

    for msg in history:
        if msg.role == "user":
            messages.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            messages.append(AIMessage(content=msg.content))

    # add current user input (not stored yet)
    messages.append(HumanMessage(content=new_input))

    return messages
