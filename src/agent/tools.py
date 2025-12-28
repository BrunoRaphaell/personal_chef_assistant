from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient
from .config import AgentConfig
import base64

tavily_client = TavilyClient(api_key=AgentConfig.TAVILY_API_KEY)

@tool
def search_web(query: str) -> Dict[str, Any]:
    """
    Search the web for the user's query.
    
    Args:
        query: Search terms to look for
    """
    try:
        return tavily_client.search(query=query)
    except Exception as e:
        return {"Erro":f"Erro na busca: {e}"}
        