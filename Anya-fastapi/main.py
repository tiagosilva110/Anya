import sys
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
            payload = (
                mensagem.model_dump()
                if hasattr(mensagem, "model_dump")
                else mensagem.dict()
            )

            response = await client.post(
                f"{SPRING_BOOT_URL}/message",
                json=payload,
                timeout=5.0,
            )
            response.raise_for_status()
            resposta_json = response.json()

            # Extrai o nome dentro de 'contact' -> 'name'
            # Caso não venha o contact, tenta buscar account.name ou fallback para "Desconhecido"
            contact_info = resposta_json.get("contact") or {}
            remetente = contact_info.get("name") or resposta_json.get("account", {}).get("name", "Desconhecido")
            
            body_resposta = resposta_json.get("body", "Nova mensagem!")

            # Chama o notifications.py passando "Gaby" e "Ola mundo"
            subprocess.Popen([sys.executable, "notifications.py", remetente, body_resposta])

            return resposta_json

        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Erro ao comunicar com o Spring Boot",
            )