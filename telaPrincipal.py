import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
from pynput import mouse, keyboard

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("320x360")
        self.root.resizable(False, False)

        self.enabled = False  # Ligado/desligado pelo F6 ou botão
        self.clicando = False  # Apenas enquanto o botão lateral estiver pressionado
        self.click_count = 0
        self.start_time = None

        # Intervalo
        ttk.Label(root, text="Intervalo (segundos):").pack(pady=5)
        self.interval_entry = ttk.Entry(root, justify="center")
        self.interval_entry.insert(0, "0.05")
        self.interval_entry.pack(pady=5)

        # Cliques por intervalo
        ttk.Label(root, text="Cliques por intervalo:").pack(pady=5)
        self.clicks_entry = ttk.Entry(root, justify="center")
        self.clicks_entry.insert(0, "1")
        self.clicks_entry.pack(pady=5)

        # Botão ligar/desligar
        self.toggle_button = ttk.Button(root, text="Ligar", command=self.toggle_enabled)
        self.toggle_button.pack(pady=10)

        # Status
        self.status_label = ttk.Label(root, text="Status: Desligado", foreground="red")
        self.status_label.pack(pady=5)

        # Contador de cliques
        self.counter_label = ttk.Label(root, text="Cliques dados: 0", font=("Arial", 10, "bold"))
        self.counter_label.pack(pady=5)

        # CPS
        self.cps_label = ttk.Label(root, text="CPS: 0.00", font=("Arial", 10, "bold"))
        self.cps_label.pack(pady=5)

        # Info
        ttk.Label(root, text="Segure o botão lateral do mouse para clicar\nF6 para ligar/desligar", font=("Arial", 9)).pack(pady=10)

        # Threads
        threading.Thread(target=self.click_loop, daemon=True).start()
        threading.Thread(target=self.mouse_listener, daemon=True).start()
        threading.Thread(target=self.keyboard_listener, daemon=True).start()

    def toggle_enabled(self):
        """Liga ou desliga o auto click"""
        self.enabled = not self.enabled
        if self.enabled:
            self.toggle_button.config(text="Desligar")
            self.status_label.config(text="Status: Ligado", foreground="green")
        else:
            self.toggle_button.config(text="Ligar")
            self.status_label.config(text="Status: Desligado", foreground="red")
            self.clicando = False  # garante que o clique pare

    def mouse_listener(self):
        """Monitora o botão lateral do mouse"""
        def on_click(x, y, button, pressed):
            if button == mouse.Button.x_button1 and self.enabled:
                self.clicando = pressed
                if pressed:
                    self.start_time = time.time()
                    self.click_count = 0

        with mouse.Listener(on_click=on_click) as listener:
            listener.join()

    def keyboard_listener(self):
        """Monitora F6 para ligar/desligar"""
        def on_press(key):
            try:
                if key == keyboard.Key.f6:
                    self.toggle_enabled()
            except AttributeError:
                pass

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def click_loop(self):
        while True:
            if self.enabled and self.clicando:
                try:
                    intervalo = float(self.interval_entry.get())
                    cliques = int(self.clicks_entry.get())
                except ValueError:
                    intervalo = 0.05
                    cliques = 1

                for _ in range(cliques):
                    pyautogui.click()
                    self.click_count += 1
                    self.update_display()
                    time.sleep(0.01)
                time.sleep(intervalo)
            else:
                time.sleep(0.01)

    def update_display(self):
        self.counter_label.config(text=f"Cliques dados: {self.click_count}")
        elapsed = time.time() - self.start_time if self.start_time else 0
        cps = self.click_count / elapsed if elapsed > 0 else 0
        self.cps_label.config(text=f"CPS: {cps:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    AutoClicker(root)
    root.mainloop()
