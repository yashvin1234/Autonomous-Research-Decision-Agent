from langchain_groq import ChatGroq
from app.config import settings

def get_llm(temperature: float = 0.2):
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.MODEL_NAME,
        temperature=temperature
    )
