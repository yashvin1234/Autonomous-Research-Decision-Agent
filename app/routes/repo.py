from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import crud
from app.db.sessions import get_db
from app.core.deps import get_current_user
from app.models.db_models import Repository
from app.models.schemas import RepoRequest, AskRepoRequest
from app.rag.chroma_manager import create_repo_store, load_repo_store
from app.rag.loader_service import load_and_split
from app.rag.qa_service import create_qa_chain
from app.rag.repo_service import clone_repo

router = APIRouter(prefix="/repos", tags=["Repositories"])

@router.post("/index")
def index_repo(data: RepoRequest, db: Session = Depends(get_db), email=Depends(get_current_user)):
    user = crud.get_user_by_email(db, email)

    repo = Repository(
        user_id=user.id,
        repo_url=data.repo_url,
        name=data.repo_url.split("/")[-1]
    )
    db.add(repo)
    db.commit()
    db.refresh(repo)

    # clone
    repo_path = clone_repo(data.repo_url)

    # split
    documents = load_and_split(repo_path)

    # embeddings
    collection = create_repo_store(documents, repo.id)

    repo.chroma_collection = collection
    db.commit()

    return {"repo_id": repo.id}

@router.post("/ask")
def ask_repo(data: AskRepoRequest, db: Session = Depends(get_db), email=Depends(get_current_user)):
    user = crud.get_user_by_email(db, email)

    repo = db.query(Repository).filter(
        Repository.id == data.repo_id,
        Repository.user_id == user.id
    ).first()

    if not repo:
        raise HTTPException(404, "Repo not found")

    vector_store = load_repo_store(repo.id)
    qa_chain = create_qa_chain(vector_store)

    answer = qa_chain.invoke(data.question)

    return {"answer": answer}

