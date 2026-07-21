#!/usr/bin/env python3

import queue
import sys
import os
import time
import json
import requests
import threading
import winsound  # Sons nativos do Windows
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import pyttsx3

import tkinter as tk
import ctypes

DEVICE = None        
SAMPLERATE = 16000   
MODEL_PATH = "vosk-model-pt-fb-v0.1.1-pruned"

model = Model(MODEL_PATH)
rec = KaldiRecognizer(model, SAMPLERATE)

# Fila de Notificações
fila_notificacoes = queue.Queue()

class MensagemPayload(BaseModel):
    sender: str
    titulo: str = "Aviso Prioritário"
    mensagem: str

# --- SONS DO SISTEMA WINDOWS (Agradáveis e Suaves) ---

def tocar_som_notificacao_post():
    """Som do Windows disparado IMEDIATAMENTE quando a requisição POST chega."""
    def _tocar():
        try:
            # Usa o som suave de notificação do Windows
            winsound.PlaySound("SystemNotification", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception as e:
            print(f"[❌ ERRO SOM] Falha ao emitir som de recebimento: {e}")

    threading.Thread(target=_tocar, daemon=True).start()

def tocar_som_inicio_gravacao():
    """Som suave de confirmação (Asterisk do Windows) ao abrir o microfone."""
    def _tocar():
        try:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception as e:
            print(f"[❌ ERRO SOM] Falha ao emitir som de gravação: {e}")

    threading.Thread(target=_tocar, daemon=True).start()

def tocar_som_fim_gravacao():
    """Som suave de término (Exclamation do Windows)."""
    def _tocar():
        try:
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception as e:
            print(f"[❌ ERRO SOM] Falha ao emitir som de término: {e}")

    threading.Thread(target=_tocar, daemon=True).start()


def falar_texto_async(texto: str):
    """Executa o TTS em uma thread dedicada para não travar a interface."""
    def _falar():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 180)
            engine.say(texto)
            engine.runAndWait()
        except Exception as e:
            print(f"[❌ ERRO TTS] Falha ao sintetizar voz: {e}")

    thread = threading.Thread(target=_falar, daemon=True)
    thread.start()

def aplicar_dpi_awareness():
    """Força o Windows a reconhecer a resolução real da tela."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

def exibir_notificacao(sender: str, titulo: str, mensagem: str):
    """Exibe notificação com Fade In, texto com sombra e Fade Out (Sem título)."""
    print(f"[🔔 NOTIFICAÇÃO] Exibindo mensagem de: {sender}")
    
    aplicar_dpi_awareness()

    try:
        janela = tk.Tk()
        janela.overrideredirect(True)
        janela.attributes('-topmost', True)

        COR_TRANSPARENTE = "#ff00ff"
        janela.configure(bg=COR_TRANSPARENTE)
        janela.wm_attributes("-transparentcolor", COR_TRANSPARENTE)

        janela.attributes('-alpha', 0.0)

        largura, altura = 500, 150
        largura_tela = janela.winfo_screenwidth()
        
        x = int((largura_tela - largura) / 2)
        y = 30

        janela.geometry(f"{largura}x{altura}+{x}+{y}")

        canvas = tk.Canvas(
            janela, 
            bg=COR_TRANSPARENTE, 
            highlightthickness=0, 
            bd=0
        )
        canvas.pack(fill="both", expand=True)

        texto_completo = f"De: {sender}\n{mensagem}"

        # Sombra (Preto)
        canvas.create_text(
            (largura // 2) + 2, 62,
            text=texto_completo,
            font=("Segoe UI", 11, "bold"),
            fill="#000000",
            justify="center",
            width=460
        )

        # Texto Principal (Branco)
        canvas.create_text(
            largura // 2, 60,
            text=texto_completo,
            font=("Segoe UI", 11, "bold"),
            fill="#FFFFFF",
            justify="center",
            width=460
        )

        def fade_in(alpha=0.0):
            if alpha <= 1.0:
                janela.attributes('-alpha', alpha)
                janela.after(20, fade_in, alpha + 0.05)

        def fade_out(alpha=1.0):
            if alpha >= 0.0:
                janela.attributes('-alpha', alpha)
                janela.after(20, fade_out, alpha - 0.05)
            else:
                janela.destroy()

        fade_in()

        # Permanece 8s antes do fade-out
        janela.after(8000, fade_out)
        
        janela.mainloop()
        
    except Exception as e:
        print(f"[❌ ERRO TKINTER] Falha ao renderizar janela: {e}")

app = FastAPI(title="Serviço de Reconhecimento de Voz")
q = queue.Queue()

def callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def gravar_e_enviar():
    # Sound suave de início de gravação
    tocar_som_inicio_gravacao()
    print("\n[🔴 GRAVANDO] Microfone ativado por 10 segundos... Fale agora.")
    
    while not q.empty():
        q.get()
    rec.Reset()

    tempo_limite = time.time() + 10.0

    with sd.RawInputStream(samplerate=SAMPLERATE, blocksize=16000, device=DEVICE,
                            dtype="int16", channels=1, callback=callback):
        
        while time.time() < tempo_limite:
            try:
                data = q.get(timeout=0.1)
                rec.AcceptWaveform(data)
            except queue.Empty:
                continue

    # Som suave de fim de gravação
    print("[⏳ PROCESSANDO] Tempo esgotado. Interpretando áudio...")
    
    resultado_raw = rec.Result()
    resultado_json = json.loads(resultado_raw)
    
    texto_final = resultado_json.get("text", "")
    print(f"Texto reconhecido: \"{texto_final}\"")

    url_destino = "http://localhost:8080/message"
    payload = {"body": texto_final}
    
    try:
        print(f"[📤 ENVIANDO] Postando mensagem para {url_destino}...")
        response = requests.post(url_destino, json=payload, timeout=5)
        print(f"[✅ ENVIADO] Resposta do servidor: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[❌ ERRO] Falha ao enviar POST para o localhost:8080: {e}")

def processar_fluxo(payload: MensagemPayload):
    # 1. Dispara voz TTS
    texto_para_falar = f"Mensagem de {payload.sender}. {payload.mensagem}"
    falar_texto_async(texto_para_falar)

    # 2. Exibe notificação na tela
    exibir_notificacao(payload.sender, payload.titulo, payload.mensagem)
    
    # 3. Executa gravação do microfone (com som suave ao iniciar/terminar)
    gravar_e_enviar()

# --- WORKER THREAD (CONSUMIDOR DA FILA) ---
def worker_notificacoes():
    """Thread infinita que escuta a fila e processa as mensagens uma a uma."""
    while True:
        payload = fila_notificacoes.get()
        print(f"\n[📦 FILA] Processando mensagem (Restantes na fila: {fila_notificacoes.qsize()})")
        
        try:
            processar_fluxo(payload)
        except Exception as e:
            print(f"[❌ ERRO NO FLUXO] {e}")
        finally:
            fila_notificacoes.task_done()

# --- Rotas da API ---

@app.post("/start")
def iniciar_gravacao(payload: MensagemPayload):
    # 🔊 1. SOM IMEDIATO NO MOMENTO DO POST
    # tocar_som_notificacao_post()

    # 2. Enfileira a notificação
    fila_notificacoes.put(payload)
    posicao = fila_notificacoes.qsize()
    
    print(f"[📥 RECEBIDO] Nova mensagem adicionada à fila. Posição atual: {posicao}")
    
    return {
        "status": "enfileirado",
        "posicao_fila": posicao,
        "sender": payload.sender,
        "mensagem": payload.mensagem
    }

if __name__ == "__main__":
    t = threading.Thread(target=worker_notificacoes, daemon=True)
    t.start()

    print("\n" + "="*50)
    print(" SERVIÇO DE VOZ E NOTIFICAÇÃO ATIVO")
    print(" Envie um POST para: http://localhost:5000/start")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=5000)