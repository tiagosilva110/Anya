#!/usr/bin/env python3

import argparse
import queue
import sys
import sounddevice as sd
import keyboard  # Nova biblioteca para detectar os botões

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Função auxiliar para a análise de argumentos."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """Esta função é chamada para cada bloco de áudio."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="mostra a lista de dispositivos de áudio e sai")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)

parser = argparse.ArgumentParser(
    description="Script de reconhecimento de fala controlado por botões.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="dispositivo de entrada (ID numérico ou parte do nome)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="taxa de amostragem (sample rate)")
parser.add_argument(
    "-m", "--model", type=str, help="modelo de idioma; o padrão é pt")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        model = Model(lang="pt")
    else:
        model = Model(lang=args.model)

    rec = KaldiRecognizer(model, args.samplerate)

    print("#" * 50)
    print(" Pressione ESPAÇO para COMEÇAR a ouvir.")
    print(" Pressione Ctrl+C a qualquer momento para sair.")
    print("#" * 50)

    while True:
        # 1. Espera o usuário apertar ESPAÇO para começar
        keyboard.wait('space')
        print("\n[🔴 GRAVANDO] Ouvindo... Fale agora.")
        print("[⌨️] Pressione ENTER para PARAR e interpretar.")
        
        # Limpa qualquer resíduo anterior do áudio e do reconhecedor
        while not q.empty():
            q.get()
        rec.Reset()

        # 2. Inicia o fluxo do microfone
        with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
                                dtype="int16", channels=1, callback=callback):
            
            # Loop de gravação ativa até que ENTER seja pressionado
            while True:
                data = q.get()
                rec.AcceptWaveform(data)  # Alimenta o modelo em segundo plano
                
                if keyboard.is_pressed('enter'):
                    print("\n[⏳ PROCESSANDO] Interpretando o áudio...")
                    break
        
        # 3. Exibe o resultado final após parar o microfone
        print("\nResultado Final:")
        print("-" * 40)
        print(rec.Result())
        print("-" * 40)
        print("\nPronto para a próxima! Pressione ESPAÇO para começar de novo.\n")

except KeyboardInterrupt:
    print("\nEncerrado pelo usuário.")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))