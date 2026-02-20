from typing import Dict, List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

conversation_store: Dict[str, List[BaseMessage]] = {}


def get_history(session_id: str) -> List[BaseMessage]:
    """Return history for session"""
    return conversation_store.get(session_id, [])


def add_user_message(session_id: str, message: str):
    conversation_store.setdefault(session_id, [])
    conversation_store[session_id].append(HumanMessage(content=message))


def add_ai_message(session_id: str, message: str):
    conversation_store.setdefault(session_id, [])
    conversation_store[session_id].append(AIMessage(content=message))


def build_chat_input(session_id: str, new_input: str):
    """
    Returns messages list ready for LLM invoke
    DOES NOT store anything
    """
    history = get_history(session_id)
    return history + [HumanMessage(content=new_input)]

