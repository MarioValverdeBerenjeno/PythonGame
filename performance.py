import psutil
import tkinter as tk
import time

def get_memory_usage():
    memory = psutil.virtual_memory()
    return f"Memoria en uso: {memory.percent}%"

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"Uso de CPU: {cpu_usage}%"

def crear_ventana_mod():
    root = tk.Tk()
    root.title("Uso de memoria y CPU")
    
    # Ajusta el tamaño de la ventana
    root.geometry("400x150")
    
    memory_label = tk.Label(root, text="", font=("Helvetica", 12))
    memory_label.pack()
    
    def update_labels():
        memory_label.config(text=get_memory_usage())
        cpu_label.config(text=get_cpu_usage())
        root.after(1000, update_labels)
    
    cpu_label = tk.Label(root, text="", font=("Helvetica", 12))
    cpu_label.pack()

    update_labels()
    
    root.mainloop()