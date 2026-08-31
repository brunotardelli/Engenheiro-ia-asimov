from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.groq import Groq
from dotenv import load_dotenv
load_dotenv()
agent =Agent(
    model = Groq(id="llama-3.3-70b-versatile"),
    tools=[TavilyTools()],

)
agent.print_response("Use suas ferramentas para perguntar:Which win the world cup in 2026?")
