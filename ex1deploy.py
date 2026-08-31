import os
from pathlib import Path

# --- Correção para deploy no Render (ou qualquer servidor com SQLite antigo) ---
# O ChromaDB exige uma versão do SQLite mais nova do que a que vem por padrão
# em muitos servidores. Essas 3 linhas "substituem" o sqlite3 padrão do Python
# pela versão mais nova instalada via pysqlite3-binary (ver requirements.txt).
# Isso precisa vir ANTES de qualquer import relacionado a chromadb.
try:
    __import__("pysqlite3")
    import sys
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass  # Na sua máquina local isso não é necessário, então ignoramos se não existir

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

load_dotenv()

# Garante que a pasta "tmp" existe antes de tentar usá-la.
# No Render, o repositório clonado NÃO tem essa pasta (ela está no .gitignore),
# então se não criarmos, o SqliteDb/ChromaDb vão quebrar procurando um lugar que não existe.
Path("tmp").mkdir(exist_ok=True)

# --- Banco de dados (sessões e histórico) ---
db = SqliteDb(db_file="tmp/agent.db")

# --- RAG: base de conhecimento vinda do PDF ---
vector_db = ChromaDb(collection="pdf_agent", path="tmp/chromadb")
knowledge = Knowledge(vector_db=vector_db)
knowledge.add_content(path="mais_ricos.pdf")

agent = Agent(
    name="Agente do PDF",
    model=OpenAIChat(id="gpt-4o-mini"),
    db=db,
    knowledge=knowledge,
    search_knowledge=True,
    add_history_to_context=True,
    num_history_runs=4,
    debug_mode=True,
)

app = FastAPI(title="API do Agente PDF")

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    run_output = agent.run(request.message, user_id=request.user_id)
    return ChatResponse(response=run_output.content)

@app.get("/")
def health_check():
    return {"status": "ok", "agent": agent.name}

if __name__ == "__main__":
    # PORT vem do ambiente (é assim que o Render informa qual porta usar).
    # Localmente, se essa variável não existir, cai no padrão 8000.
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)