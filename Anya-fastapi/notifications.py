import os
import sys
import tkinter as tk
import winsound


def tocar_som_wav():
    # Procura pelo arquivo not_sound.wav ou not_sound na pasta atual
    candidatos = ["not_sound.wav", "not_sound"]
    caminho_som = None

    for nome in candidatos:
        if os.path.exists(nome):
            caminho_som = nome
            break

    if caminho_som:
        try:
            # SND_FILENAME: especifica arquivo local
            # SND_ASYNC: toca sem travar/congelar a interface do Tkinter
            winsound.PlaySound(
                caminho_som, winsound.SND_FILENAME | winsound.SND_ASYNC
            )
        except Exception as e:
            print(f"Erro ao tocar áudio WAV: {e}")


def mostrar_notificacao():
    sender = sys.argv[1] if len(sys.argv) > 1 else "Anya"
    body = sys.argv[2] if len(sys.argv) > 2 else "Nova Mensagem!"

    texto_formatado = f"{sender}: {body}"

    root = tk.Tk()
    root.withdraw()

    win = tk.Toplevel(root)
    win.overrideredirect(True)
    win.attributes("-topmost", True)

    COR_TRANSPARENTE = "#000001"
    win.configure(bg=COR_TRANSPARENTE)

    try:
        win.wm_attributes("-transparentcolor", COR_TRANSPARENTE)
        win.attributes("-alpha", 0.0)
    except Exception:
        pass

    largura = 500
    altura = 100
    largura_tela = win.winfo_screenwidth()

    x = (largura_tela - largura) // 2
    y = 30
    win.geometry(f"{largura}x{altura}+{x}+{y}")

    # Sombra
    label_sombra = tk.Label(
        win,
        text=texto_formatado,
        fg="#000000",
        bg=COR_TRANSPARENTE,
        font=("Segoe UI", 14, "bold"),
        justify="center",
        wraplength=480,
    )
    label_sombra.place(x=2, y=2, relwidth=1, relheight=1)

    # Texto Principal
    label_texto = tk.Label(
        win,
        text=texto_formatado,
        fg="#ffffff",
        bg=COR_TRANSPARENTE,
        font=("Segoe UI", 14, "bold"),
        justify="center",
        wraplength=480,
    )
    label_texto.place(x=0, y=0, relwidth=1, relheight=1)

    def fade_in(alpha=0.0):
        if alpha <= 1.0:
            win.attributes("-alpha", alpha)
            win.after(20, fade_in, alpha + 0.05)
        else:
            win.after(3000, fade_out, 1.0)

    def fade_out(alpha=1.0):
        if alpha >= 0.0:
            win.attributes("-alpha", alpha)
            win.after(20, fade_out, alpha - 0.05)
        else:
            root.destroy()

    # Dispara o som WAV e inicia o Fade In
    tocar_som_wav()
    fade_in()
    root.mainloop()


if __name__ == "__main__":
    mostrar_notificacao()