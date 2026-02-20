from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage

from app.services.llm import get_llm
from app.models.schemas import PlannerOutput
from app.services.memory import build_chat_input

parser = PydanticOutputParser(pydantic_object=PlannerOutput)

planner_prompt = PromptTemplate(
    template="""
You are a senior business and technical strategist.

Your job is to convert a vague goal into a structured research plan.

Goal:
{goal}

Instructions:
1. Identify the core intent.
2. Break the goal into clear research questions.
3. Define evaluation criteria for decision-making.

{format_instructions}

Only return valid JSON.
""",
    input_variables=["goal"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

def run_planner(goal: str, session_id: str) -> PlannerOutput:
    llm = get_llm(temperature=0.2)

    formatted_prompt = planner_prompt.format(goal=goal)

    messages = build_chat_input(session_id, formatted_prompt)

    response = llm.invoke(messages)

    try:
        parsed_output = parser.parse(response.content)
        return parsed_output
    except Exception as e:
        raise ValueError(f"Planner parsing failed: {e}")
