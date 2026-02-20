from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split(repo_path: str):
    loader = DirectoryLoader(
        repo_path,
        glob="**/*.py",  # Start with Python for MVP
        loader_cls=TextLoader,
        show_progress=True
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(documents)

    return split_docs