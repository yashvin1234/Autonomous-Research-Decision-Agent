from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat
from app.routes import user
from app.routes import repo
# from app.db.init_db import init_db


app = FastAPI(title="Autonomous Research & Decision Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # for dev (later restrict)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router)
app.include_router(user.router)
app.include_router(repo.router)

@app.get("/")
def health_check():
    return {"status": "running"}

#fewfee