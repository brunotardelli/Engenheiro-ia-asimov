from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools
from agno.models.groq import Groq
from dotenv import load_dotenv
load_dotenv()
agent =Agent(
    model = Groq(id="llama-3.3-70b-versatile"),
    tools=[TavilyTools()],
    instructions="Use tabelas para mostrar as informações final. Não inclua nenhum outro texto",
)
agent.print_response("Qual a cotação atual da Tesla?", stream=True)