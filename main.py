# -------- main.py -----------
import tkinter as tk
from view import View
from controller import Controller
from model import Model

def splash_screen():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="#6B4126")
    largeur, hauteur = 400, 200
    x = (splash.winfo_screenwidth() // 2) - (largeur // 2)
    y = (splash.winfo_screenheight() // 2) - (hauteur // 2)
    splash.geometry(f"{largeur}x{hauteur}+{x}+{y}")

    tk.Label(splash, text="📚 La Bibliothèque 📚\n 📚 Du Collège 📚",
             bg="#6B4126", fg="white", font=("Segoe UI", 22, "bold")).pack(expand=True)
    splash.after(2000, splash.destroy)
    splash.mainloop()

if __name__ == "__main__":
    splash_screen()
    model = Model()
    view = View()
    controller = Controller(model, view)
    view.mainloop()
