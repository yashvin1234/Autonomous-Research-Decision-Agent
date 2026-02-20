from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.services.llm import get_llm


def create_qa_chain(vector_store):
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})


    prompt = ChatPromptTemplate.from_template(
        """
You are a senior software architect analyzing a codebase.

Use the provided context to answer the question.
If you don't know, say you don't know.

Context:
{context}

Question:
{question}
"""
    )

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | get_llm()
        | StrOutputParser()
    )

    return chain