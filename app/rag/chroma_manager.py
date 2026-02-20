from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

EMBED_MODEL = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

BASE_DIR = "chroma_db"

def create_repo_store(documents, repo_id: int):
    collection = f"repo_{repo_id}"

    vector_store = Chroma.from_documents(
        documents,
        EMBED_MODEL,
        persist_directory=BASE_DIR,
        collection_name=collection
    )

    vector_store.persist()
    return collection


def load_repo_store(repo_id: int):
    collection = f"repo_{repo_id}"

    return Chroma(
        persist_directory=BASE_DIR,
        collection_name=collection,
        embedding_function=EMBED_MODEL
    )
