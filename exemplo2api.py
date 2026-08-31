# conta corrente bancária - Fast Api
# Gerenciar saques e depósitos de clientes 
#------------------------------------------------------

# imports
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel, Field

# inicializa a fastapi
app = FastAPI(title="Conta Bancaria - Conta Corrente")

# Adicionar clientes (simula banco de dados)
db_clientes = {
    "Joao": 0,
    "Maria": 0,
    "pedro": 0,
}

# Criar uma classe para as movimentações (saques e depósitos)
class Movimentacao(BaseModel):
    cliente: str = Field(..., description="Nome do cliente")
    valor: float = Field(..., gt=0, description="Valor de movimentação")

# Criar um endpoint raiz
@app.get("/")
def read_root():
    return {"message": "Conta Bancaria - Conta Corrente"}

# endpoint para consultar saldos
@app.post("/saldo")
def saldo(cliente: str):
    return {"message": f"Saldo do cliente {cliente} é {db_clientes[cliente]}"}

# Criar um endpoint para realizar saques 
@app.post("/saque")
def saque(movimentacao: Movimentacao):
    db_clientes[movimentacao.cliente] -= movimentacao.valor
    return {"message": {"cliente": movimentacao.cliente, "valor_movimentacao": -movimentacao.valor, "saldo": db_clientes[movimentacao.cliente]}}

# Criar um endpoint para realizar depósitos 
@app.post("/deposito")
def deposito(movimentacao: Movimentacao):
    db_clientes[movimentacao.cliente] += movimentacao.valor
    return {"message": {"cliente": movimentacao.cliente, "valor_movimentacao": movimentacao.valor, "saldo": db_clientes[movimentacao.cliente]}}
# Run (sempre no final do arquivo)
if __name__ == "__main__":
    uvicorn.run("exemplo2api:app", host="0.0.0.0", port=8000, reload=True)
