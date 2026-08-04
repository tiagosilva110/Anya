from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import httpx

app = FastAPI(title="Anya Client Side", version="0.0.1")

SPRING_BOOT_URL = "http://localhost:8080"

class MessageCreate(BaseModel):
    contact: str
    body: str
    account: str

@app.post("/message", status_code=status.HTTP_201_CREATED)
async def criar_mensagem_no_spring(mensagem: MessageCreate):
    async with httpx.AsyncClient() as client:
        try:
            # Requisição POST enviando JSON para o Spring Boot
            response = await client.post(
                f"{SPRING_BOOT_URL}/message",
                json=mensagem.model_dump(),
                timeout=5.0
            )
            response.raise_for_status()
            return response.json()

        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Erro ao comunicar com o Spring Boot"
            )

# # Rota GET raiz
# @app.get("/")
# def read_root():
#     return {"mensagem": "API rodando com sucesso!"}

# # Rota GET com parâmetro
# @app.get("/itens/{Message_id}")
# def read_Message(Message_id: int):
#     return {"Message_id": Message_id, "status": "encontrado"}

# # Rota POST para criar um Message
# @app.post("/itens/")
# def create_Message(Message: Message):
#     return {"mensagem": "Message criado", "dados": item}