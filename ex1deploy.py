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

# ---------------------------------------------------------
# A partir daqui é a parte NOVA: nosso próprio FastAPI
# ---------------------------------------------------------

# 1. Cria o "restaurante" (a aplicação web)
app = FastAPI(title="API do Agente PDF")

# 2. Define o "cardápio": o formato exato que esperamos receber
class ChatRequest(BaseModel):
    message: str          # a pergunta do usuário (obrigatório)
    user_id: str = "default_user"   # opcional, com valor padrão

# 3. Define o formato da resposta que vamos devolver
class ChatResponse(BaseModel):
    response: str

# 4. Cria a rota /chat, que aceita requisições do tipo POST
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Chama o agente "cozinheiro" com a pergunta recebida
    run_output = agent.run(request.message, user_id=request.user_id)
    # .content é onde mora o texto da resposta final do agente
    return ChatResponse(response=run_output.content)

# 5. Uma rota simples de "saúde" — útil pra checar se o servidor tá de pé
@app.get("/")
def health_check():
    return {"status": "ok", "agent": agent.name}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)