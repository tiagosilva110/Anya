#!/usr/bin/env python3

import argparse
import queue
import sys
import os
import time
import json
import requests
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Dependências do servidor web
from fastapi import FastAPI, BackgroundTasks
import uvicorn

app = FastAPI(title="Serviço de Reconhecimento de Voz")
q = queue.Queue()

# --- Configurações do Vosk (Mantidas do seu script original) ---
def int_or_str(text):
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Configuração de parâmetros padrão
DEVICE = None        # ID do microfone (None usa o padrão)
SAMPLERATE = 16000   # Frequência padrão (comum para Vosk)
MODEL_PATH = "vosk-model-pt-fb-v0.1.1-pruned" # Seu modelo pesado

model = Model(MODEL_PATH)


rec = KaldiRecognizer(model, SAMPLERATE)


# --- Função Principal de Gravação (Ativada por 10 segundos) ---
def gravar_e_enviar():
    print("\n[🔴 GRAVANDO] Microfone ativado por 10 segundos... Fale agora.")
    
    # Limpa a fila e o reconhecedor de lixos anteriores
    while not q.empty():
        q.get()
    rec.Reset()

    # Define o tempo de término (Agora + 10 segundos)
    tempo_limite = time.time() + 10.0

    # Abre o fluxo do microfone
    with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=16000, device=DEVICE,
                            dtype="int16", channels=1, callback=callback):
        
        while time.time() < tempo_limite:
            try:
                # Pega o áudio da fila com timeout pequeno para não travar o loop
                data = q.get(timeout=0.1)
                rec.AcceptWaveform(data)
            except queue.Empty:
                continue

    print("[⏳ PROCESSANDO] Tempo esgotado. Interpretando áudio...")
    
    # Pega o resultado final estruturado pelo Vosk (retorna uma string JSON)
    resultado_raw = rec.Result()
    resultado_json = json.loads(resultado_raw)
    
    # Extrai apenas o texto transcrito
    texto_final = resultado_json.get("text", "")
    print(f"Texto reconhecido: \"{texto_final}\"")

    # Envia o resultado para o destino final
    url_destino = "http://localhost:8080/message"
    payload = {"body": texto_final}
    
    try:
        print(f"[📤 ENVIANDO] Postando mensagem para {url_destino}...")
        response = requests.post(url_destino, json=payload, timeout=5)
        print(f"[✅ ENVIADO] Resposta do servidor: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[❌ ERRO] Falha ao enviar POST para o localhost:8080: {e}")


# --- Rotas da API (Serviço) ---

@app.post("/start")
def iniciar_gravacao(background_tasks: BackgroundTasks):
    """
    Rota que recebe o POST para iniciar a gravação.
    Usa 'BackgroundTasks' para que o servidor responda imediatamente ao cliente (200 OK)
    enquanto executa o processo de gravação e envio em segundo plano.
    """
    background_tasks.add_task(gravar_e_enviar)
    return {"status": "gravacao_iniciada", "duracao": "10s"}


if __name__ == "__main__":
    # Inicia o servidor na porta 5000 do localhost
    print("\n" + "="*50)
    print(" SERVIÇO DE VOZ ATIVO")
    print(" Envie um POST para: http://localhost:5000/start")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=5000)