import sys
import tkinter as tk


def mostrar_notificacao():
  # Pega o texto passado como argumento (ou usa um padrão)
  texto_body = sys.argv[1] if len(sys.argv) > 1 else "Nova Mensagem!"

  root = tk.Tk()
  root.withdraw()

  win = tk.Toplevel(root)
  win.overrideredirect(True)
  win.attributes("-topmost", True)

  try:
    win.attributes("-alpha", 0.85)
  except Exception:
    pass

  # Posição (canto inferior direito)
  largura = 320
  altura = 80
  largura_tela = win.winfo_screenwidth()
  altura_tela = win.winfo_screenheight()
  x = largura_tela - largura - 20
  y = altura_tela - altura - 60
  win.geometry(f"{largura}x{altura}+{x}+{y}")

  frame = tk.Frame(win, bg="#1e1e1e", bd=2, relief="solid")
  frame.pack(fill="both", expand=True)

  label = tk.Label(
      frame,
      text=f"Nova Mensagem:\n{texto_body}",
      fg="#ffffff",
      bg="#1e1e1e",
      font=("Segoe UI", 10),
      justify="left",
      wraplength=300,
  )
  label.pack(padx=10, pady=10, fill="both", expand=True)

  win.after(4000, root.destroy)
  root.mainloop()


if __name__ == "__main__":
  mostrar_notificacao()