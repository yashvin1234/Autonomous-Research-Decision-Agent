import os
import uuid
from git import Repo

BASE_DIR = "temp_repos"

def clone_repo(repo_url: str) -> str:
    os.makedirs(BASE_DIR, exist_ok=True)

    repo_id = str(uuid.uuid4())
    repo_path = os.path.join(BASE_DIR, repo_id)

    Repo.clone_from(repo_url, repo_path)

    return repo_path