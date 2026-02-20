from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage

from app.services.llm import get_llm
from app.models.schemas import DecisionOutput, PlannerOutput, ResearchFinding
from app.services.memory import build_chat_input

parser = PydanticOutputParser(pydantic_object=DecisionOutput)

decision_prompt = PromptTemplate(
    template="""
You are a senior decision architect.

Intent:
{intent}

Evaluation Criteria:
{criteria}

Research Findings:
{research}

Your job:
1. Compare relevant options.
2. Analyze trade-offs.
3. Apply evaluation criteria.
4. Provide a final recommendation.
5. Assign a confidence score between 0 and 1.
6. Identify key risks.

{format_instructions}

Return only valid JSON.
""",
    input_variables=["intent", "criteria", "research"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

def run_decision(plan: PlannerOutput, research_findings: list[ResearchFinding], session_id: str):

    llm = get_llm(temperature=0.2)

    # Format research into readable block
    research_text = "\n\n".join(
        [
            f"Question: {r.question}\nSummary: {r.summary}"
            for r in research_findings
        ]
    )

    formatted_prompt = decision_prompt.format(
        intent=plan.intent,
        criteria=", ".join(plan.evaluation_criteria),
        research=research_text
    )

    messages = build_chat_input(session_id, formatted_prompt)

    response = llm.invoke(messages)

    try:
        parsed = parser.parse(response.content)
        return parsed
    except Exception as e:
        raise ValueError(f"Decision parsing failed: {e}")
