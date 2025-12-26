from src.agent import build_chef_agent
from langchain.messages import HumanMessage

chef_agent = build_chef_agent()

config = {"configurable": {"thread_id": "user_session_123"}}

input_user = "Tenho ovos, bacon e creme de leite. O que posso fazer?"

print("👨‍🍳 Chef Consultando...")

response = chef_agent.invoke(
    {"messages": [HumanMessage(content=input_user)]},
    config=config
)

print(response['messages'][-1].content)