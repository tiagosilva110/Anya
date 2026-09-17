import sys
import subprocess
import threading
import queue
import time
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

# Fila global para gerenciar as notificações em ordem de chegada
fila_notificacoes = queue.Queue()


class MessageCreate(BaseModel):
    phone: str
    body: str
    account: str


def processador_de_fila():
    """Consome a fila sequencialmente para garantir que uma notificação
    só apareça após a anterior fechar completamente."""
    while True:
        remetente, body_resposta = fila_notificacoes.get()
        try:
            # subprocess.run bloqueia até que o script de notificação feche
            subprocess.run(
                [sys.executable, "notifications.py", remetente, body_resposta],
                check=True
            )
        except Exception as e:
            print(f"Erro ao exibir notificação da fila: {e}")
        finally:
            fila_notificacoes.task_done()
            # Pequena pausa opcional entre uma notificação e outra
            time.sleep(0.3)


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

            # Em vez de chamar o subprocess direto, jogamos na fila
            fila_notificacoes.put((remetente, body_resposta))

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
            params = {"idString": "123"}
            headers = {"Content-Type": "text/plain"}
            
            response = requests.put(url, params=params, data=audio_b64, headers=headers)
            
            if response.status_code == 204:
                print(f"[Voz] Áudio enviado com sucesso! Status: {response.status_code}")
            else:
                print(f"[Voz] Falha no envio. Status: {response.status_code}, Resposta: {response.text}")
    except Exception as e:
        print(f"Erro ao capturar tecla: {e}")


def rodar_escuta_global():
    with keyboard.Listener(on_press=ao_pressionar_tecla) as listener:
        listener.join()


if __name__ == "__main__":
    print("=== Anya Client rodando em segundo plano ===")
    print("Pressione ENTER em *qualquer lugar* do seu computador para gravar a voz.")

    # Inicializa a thread da fila de notificações
    thread_fila = threading.Thread(
        target=processador_de_fila,
        daemon=True
    )
    thread_fila.start()

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