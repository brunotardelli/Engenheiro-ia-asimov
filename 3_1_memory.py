from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv

load_dotenv()

db = SqliteDb(db_file="tmp/agent.db")

agent = Agent(
    name="Agente Pesquisador",
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[TavilyTools()],
    instructions="Você é um pesquisador. Responda sempre chamando o usuário de senhor.",
    db=db,                     # <- a mesma "gaveta" de antes, sem precisar de Memory() separado
    enable_agentic_memory=True,
    debug_mode=True,
)

agent_os = AgentOS(agents=[agent], db=db)
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="3_1_memory:app", reload=False)