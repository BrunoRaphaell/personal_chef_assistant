from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from .config import AgentConfig
from .prompts import CHEF_SYSTEM_PROMPT
from .tools import search_web

def build_chef_agent():
    "Constrói o agente para responder as dúvidas"
    tools = [search_web]
    
    agent = create_agent(
        model=AgentConfig.MODEL_NAME,
        tools=tools,
        checkpointer=InMemorySaver(),
        system_prompt=CHEF_SYSTEM_PROMPT
    )
    
    return agent

