from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

from app.services.llm import get_llm
from app.services.memory import build_chat_input
from app.services.web_search import search_web
from app.models.schemas import ResearchFinding, PlannerOutput
from sqlalchemy.orm import Session

summary_prompt = PromptTemplate(
    template="""
You are a research analyst.

Based on the search results below, extract key insights relevant to decision-making.

Focus only on important, factual, decision-impacting information.

Search Results:
{search_results}

Provide a concise but information-rich summary.
""",
    input_variables=["search_results"]
)

def run_research(plan: PlannerOutput, chat_id: int, db: Session):

    llm = get_llm(temperature=0.3)

    findings = []

    for question in plan.research_questions:

        # Step 1 — Search
        results = search_web(question)
        combined_content = "\n\n".join(
            [f"{r['title']}\n{r['content']}\nSource: {r['url']}" for r in results]
        )

        # Step 2 — Summarize
        formatted_prompt = summary_prompt.format(
            search_results=combined_content
        )
        messages = build_chat_input(db, chat_id, formatted_prompt)

        response = llm.invoke(messages)

        findings.append(
            ResearchFinding(
                question=question,
                summary=response.content,
                sources=[r["url"] for r in results]
            )
        )

    return findings
