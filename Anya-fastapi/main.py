import subprocess
from fastapi import FastAPI, HTTPException, status
import httpx
from pydantic import BaseModel

app = FastAPI(title="Anya Client Side", version="0.0.1")

SPRING_BOOT_URL = "http://localhost:8080"


class MessageCreate(BaseModel):
  phone: str
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
          timeout=5.0,
      )
      response.raise_for_status()
      resposta_json = response.json()

      # Extrai o 'body' da resposta recebida
      body_resposta = resposta_json.get("body", "Mensagem enviada com sucesso!")

      # Dispara o Tkinter como um processo independente (garante que aparece na tela)
      subprocess.Popen(["py", "notifications.py", body_resposta])

      return resposta_json

    except httpx.RequestError:
      raise HTTPException(
          status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
          detail="Erro ao comunicar com o Spring Boot",
      )