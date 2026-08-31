from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from agno.os import AgentOS  # <- substitui o antigo "from agno.playground import Playground"
from agno.db.sqlite import SqliteDb  # <- substitui o antigo "from agno.storage.sqlite import SqliteStorage"
from dotenv import load_dotenv

load_dotenv()

def celsius_to_fh(temperatura_celsius: float) -> float:
    """
    Converte a temperatura de Celsius para Fahrenheit.
    Args:
        temperatura_celsius: A temperatura em Celsius.
    Returns:
        A temperatura em Fahrenheit.
    """
    return (temperatura_celsius * 9/5) + 32


db = SqliteDb(db_file="tmp/agent.db")

agent = Agent(
    name="Agente do tempo",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[
        TavilyTools(),
        celsius_to_fh,
    ],
    db=db,                          # <- nome novo (era "storage")
    add_history_to_context=True,
    num_history_runs=4,
    debug_mode=True,
)

# AgentOS é o "porto" que hospeda seus agentes e expõe a API + interface
agent_os = AgentOS(agents=[agent], db=db)
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="13_own_tools:app", reload=False)