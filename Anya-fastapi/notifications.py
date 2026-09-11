import os
import sys
import tkinter as tk
import winsound


def tocar_som_wav():
    candidatos = ["not_sound.wav", "not_sound"]
    caminho_som = None

    for nome in candidatos:
        if os.path.exists(nome):
            caminho_som = nome
            break

    if caminho_som:
        try:
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

    # Criando um Canvas transparente para desenhar o texto com contorno perfeito
    canvas = tk.Canvas(
        win, 
        bg=COR_TRANSPARENTE, 
        highlightthickness=0, 
        bd=0
    )
    canvas.pack(fill="both", expand=True)

    # Coordenada central do canvas
    cx = largura / 2
    cy = altura / 2
    fonte_estilo = ("Segoe UI", 12, "bold")

    # Desenha as cópias ao redor para simular o Outline (Contorno Preto)
    offsets = [
        (-1, -1), (0, -1), (1, -1),
        (-1,  0),          (1,  0),
        (-1,  1), (0,  1), (1,  1)
    ]

    for ox, oy in offsets:
        canvas.create_text(
            cx + ox, cy + oy,
            text=texto_formatado,
            font=fonte_estilo,
            fill="#000000",
            width=480,
            justify="center"
        )

    # Texto Principal por cima (Branco)
    canvas.create_text(
        cx, cy,
        text=texto_formatado,
        font=fonte_estilo,
        fill="#ffffff",
        width=480,
        justify="center"
    )

    def fade_in(alpha=0.0):
        if alpha <= 1.0:
            win.attributes("-alpha", alpha)
            win.after(20, fade_in, alpha + 0.05)
        else:
            win.after(3000 + (len(body) * 50), fade_out, 1.0)

    def fade_out(alpha=1.0):
        if alpha >= 0.0:
            win.attributes("-alpha", alpha)
            win.after(20, fade_out, alpha - 0.05)
        else:
            root.destroy()

    tocar_som_wav()
    fade_in()
    root.mainloop()


if __name__ == "__main__":
    mostrar_notificacao()