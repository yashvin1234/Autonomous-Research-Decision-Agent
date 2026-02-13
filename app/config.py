import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

settings = Settings()
