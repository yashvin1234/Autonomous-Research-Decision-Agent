from typing import Dict, List
from langchain_core.messages import HumanMessage, AIMessage

# Simple in-memory store
conversation_store: Dict[str, List] = {}


def get_conversation(session_id: str):
    return conversation_store.get(session_id, [])


def append_message(session_id: str, message):
    if session_id not in conversation_store:
        conversation_store[session_id] = []

    conversation_store[session_id].append(message)


def clear_conversation(session_id: str):
    conversation_store.pop(session_id, None)
