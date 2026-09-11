import sys
import subprocess
import threading
import uvicorn
from fastapi import FastAPI, HTTPException, status
import httpx
from pydantic import BaseModel
import base64
import io
import sounddevice as sd
import soundfile as sf
import numpy as np
from pynput import keyboard

app = FastAPI(title="Anya Client Side", version="0.0.1")

SPRING_BOOT_URL = "http://localhost:8080"


class MessageCreate(BaseModel):
    phone: str
    body: str
    account: str


def gravar_voz(duracao=5, taxa_amostragem=44100):
    print(f"\n[Voz] Gravando por {duracao} segundos...")
    
    audio_dados = sd.rec(
        int(duracao * taxa_amostragem), 
        samplerate=taxa_amostragem, 
        channels=1, 
        dtype='int16'
    )
    sd.wait()
    print("[Voz] Gravação finalizada!")

    buffer = io.BytesIO()
    sf.write(buffer, audio_dados, taxa_amostragem, format='WAV', subtype='PCM_16')
    
    buffer.seek(0)
    audio_bytes = buffer.read()
    
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    return audio_base64


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

            contact_info = resposta_json.get("contact") or {}
            remetente = contact_info.get("name") or resposta_json.get("account", {}).get("name", "Desconhecido")
            body_resposta = resposta_json.get("body", "Nova mensagem!")

            subprocess.Popen([sys.executable, "notifications.py", remetente, body_resposta])

            return resposta_json

        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Erro ao comunicar com o Spring Boot",
            )


def ao_pressionar_tecla(key):
    try:
        if key == keyboard.Key.enter:
            print("\n[Global] Tecla ENTER detectada! Iniciando gravação...")
            audio_b64 = gravar_voz(duracao=5)
            print(f"[Voz] Áudio convertido para base64! Tamanho: {len(audio_b64)}")
    except Exception as e:
        print(f"Erro ao capturar tecla: {e}")


def rodar_escuta_global():
    with keyboard.Listener(on_press=ao_pressionar_tecla) as listener:
        listener.join()


if __name__ == "__main__":
    print("=== Anya Client rodando em segundo plano ===")
    print("Pressione ENTER em *qualquer lugar* do seu computador para gravar a voz.")

    thread_api = threading.Thread(
        target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning"),
        daemon=True
    )
    thread_api.start()

    thread_teclado = threading.Thread(
        target=rodar_escuta_global,
        daemon=True
    )
    thread_teclado.start()

    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("Encerrando...")