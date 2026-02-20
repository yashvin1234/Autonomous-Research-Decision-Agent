import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # -------- AI --------
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    # -------- DATABASE --------
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://agent:agent123@localhost:5432/agentdb"
    )

    # -------- OKTA AUTH (use later) --------
    OKTA_DOMAIN: str = os.getenv("OKTA_DOMAIN", "")
    OKTA_AUDIENCE: str = os.getenv("OKTA_AUDIENCE", "api://default")
    OKTA_ISSUER: str = os.getenv("OKTA_ISSUER", "")
    OKTA_CLIENT_ID: str = os.getenv("OKTA_CLIENT_ID", "")


settings = Settings()
