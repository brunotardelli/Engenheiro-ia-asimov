# pyrefly: ignore [missinpig-import]
from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="FastAPI exemplo",
    description="Esse é o Exemplo 1 API",
    version="1.0.0",
    contact={
        "name": "Bruno",
        "email": "tardelli.bruno1@exemplo.com",
    },
)

@app.get("/")
def read_root():
    return {"message": "Hello world"}

@app.get("/hello/{name}")
def read_hello_name(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run("exemplo1api:app", host="0.0.0.0", port=8000, reload=True)
