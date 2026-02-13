from tavily import TavilyClient
from app.config import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

def search_web(query: str, max_results: int = 3):
    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results
    )
    return response["results"]
