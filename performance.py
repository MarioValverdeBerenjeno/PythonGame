import psutil
import tkinter as tk

def get_memory_usage():
    memory = psutil.virtual_memory()
    return f"Memoria en uso: {memory.percent}%"

def get_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    return f"Uso de CPU: {cpu_usage}%"

def get_battery():
    battery = psutil.sensors_battery()
    return f"Bateria: {battery.percent}%"
    
def crear_ventana_mod():
    root = tk.Tk()
    root.title("Performance")

    # Definir las dimensiones de la ventana
    root_width = 300
    root_height = 100

    # Obtener el ancho de la pantalla
    screen_width = root.winfo_screenwidth()

    # Calcular la posición en la esquina superior derecha
    x_position = screen_width - root_width
    y_position = 0  # 0 para la parte superior

    # Establecer las dimensiones y posición de la ventana
    root.geometry(f"{root_width}x{root_height}+{x_position}+{y_position}")
    
    memory_label = tk.Label(root, text="", font=("Courier", 12))
    memory_label.pack()

    battery_label = tk.Label(root, text="", font=("Courier", 12))
    battery_label.pack()

    cpu_label = tk.Label(root, text="", font=("Courier", 12))
    cpu_label.pack()
    
    def update_labels():
        memory_label.config(text=get_memory_usage())
        battery_label.config(text=get_battery())
        cpu_label.config(text=get_cpu_usage())
        root.after(1000, update_labels)

    update_labels()
    
    root.mainloop()