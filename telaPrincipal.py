import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
import keyboard  


class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("300x350")
        self.root.resizable(False, False)

        self.running = False
        self.click_count = 0
        self.start_time = None

        # Intervalo
        ttk.Label(root, text="Intervalo (segundos):").pack(pady=5)
        self.interval_entry = ttk.Entry(root, justify="center")
        self.interval_entry.insert(0, "1")
        self.interval_entry.pack(pady=5)

        # Cliques simultâneos
        ttk.Label(root, text="Cliques por intervalo:").pack(pady=5)
        self.clicks_entry = ttk.Entry(root, justify="center")
        self.clicks_entry.insert(0, "5")
        self.clicks_entry.pack(pady=5)

        # Botão iniciar/parar
        self.start_button = ttk.Button(root, text="Iniciar", command=self.toggle)
        self.start_button.pack(pady=10)

        # Status
        self.status_label = ttk.Label(root, text="Status: Parado", foreground="red")
        self.status_label.pack(pady=5)

        # Contador de cliques
        self.counter_label = ttk.Label(root, text="Cliques dados: 0", font=("Arial", 10, "bold"))
        self.counter_label.pack(pady=5)

        # CPS
        self.cps_label = ttk.Label(root, text="CPS: 0.00", font=("Arial", 10, "bold"))
        self.cps_label.pack(pady=5)

        # Atalho
        self.hotkey_label = ttk.Label(root, text="Pressione F6 para Iniciar/Parar", font=("Arial", 9))
        self.hotkey_label.pack(pady=10)

        # Thread para monitorar tecla
        threading.Thread(target=self.monitor_hotkey, daemon=True).start()

    def monitor_hotkey(self):
        while True:
            keyboard.wait("F6")  # espera até apertar F6
            self.toggle()
            time.sleep(0.3)  # evita ativar/desativar rápido demais

    def toggle(self):
        if not self.running:
            self.running = True
            self.click_count = 0
            self.start_time = time.time()
            self.start_button.config(text="Parar")
            self.status_label.config(text="Status: Rodando", foreground="green")
            threading.Thread(target=self.click_loop, daemon=True).start()
        else:
            self.running = False
            self.start_button.config(text="Iniciar")
            self.status_label.config(text="Status: Parado", foreground="red")

    def click_loop(self):
        try:
            intervalo = float(self.interval_entry.get())
            cliques = int(self.clicks_entry.get())
        except ValueError:
            self.status_label.config(text="Valores inválidos!", foreground="orange")
            self.running = False
            self.start_button.config(text="Iniciar")
            return

        while self.running:
            for _ in range(cliques):
                pyautogui.click()
                self.click_count += 1
                self.update_display()
                time.sleep(0.01)
            time.sleep(intervalo)

    def update_display(self):
        self.counter_label.config(text=f"Cliques dados: {self.click_count}")
        elapsed = time.time() - self.start_time
        cps = self.click_count / elapsed if elapsed > 0 else 0
        self.cps_label.config(text=f"CPS: {cps:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    AutoClicker(root)
    root.mainloop()
