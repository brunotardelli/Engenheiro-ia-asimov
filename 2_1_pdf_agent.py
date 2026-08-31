from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge  # <- classe universal nova
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv

load_dotenv()

# --- Banco de dados (sessões e histórico) ---
db = SqliteDb(db_file="tmp/agent.db")

# --- RAG: base de conhecimento vinda do PDF ---
vector_db = ChromaDb(collection="pdf_agent", path="tmp/chromadb")

knowledge = Knowledge(vector_db=vector_db)

# Insere o PDF na base de conhecimento (lê, quebra em pedaços, gera embeddings)
knowledge.add_content(path="mais_ricos.pdf")

agent = Agent(
    name="Agente do PDF",
    model=OpenAIChat(id="gpt-4o-mini"),
    db=db,
    knowledge=knowledge,
    search_knowledge=True,   # <- diz pro agente: "você TEM uma ferramenta de busca no PDF, use quando precisar"
    add_history_to_context=True,
    num_history_runs=4,
    debug_mode=True,
)

agent_os = AgentOS(agents=[agent], db=db)
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="2_1_pdf_agent:app", reload=False)