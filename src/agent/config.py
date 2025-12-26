from dotenv import load_dotenv
import os

load_dotenv()

class AgentConfig:
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")