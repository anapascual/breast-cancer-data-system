import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import csv
import requests

# Crear la ventana principal
root = tk.Tk()
root.title("Carga de archivos CSV")

# Funcion para cargar y leer el archivo
def load_csv():
    # abre cuadro de diálogo para seleccionar archivo csv
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return
    # lee el archivo csv
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        documento = list(reader)

    # variable para guardar el contenido del csv
    global documento_csv
    documento_csv = documento

    # muestra un label indicando que se ha cargado y leído el archivo correctamente
    status_label.config(text=f"Archivo cargado y leído: {file_path}")

# Función para contar columnas del documento cargado (por ejemplo)
def contar_columnas():
    num_columnas = len(documento_csv[0]) if documento_csv else 0

    columnas_label.config(text=columnas_label.cget("text") + f"\nNúmero de columnas: {num_columnas}")
    columnas_label.pack(pady=5)

# Crear un botón para cargar el archivo CSV
load_button = tk.Button(root, text="Cargar CSV", command=load_csv)
load_button.pack(pady=20)

# Crear el botón para contar el número de columnas
contar_btn = tk.Button(root, text="Contar Columnas", command=contar_columnas)
contar_btn.pack(pady=5)

# Crear label para mostrar el estado
status_label = tk.Label(root, text="Esperando a cargar un archivo CSV")
status_label.pack(pady=20)

columnas_label = tk.Label(root)

# Variable global para almacenar el contenido del csv
documento_csv = None

'''# Crear un área de texto
text_area = tk.Text(root, wrap='word', width=80, height=20)
text_area.pack(pady=10)'''


# Iniciar el bucle principal de la ventana
root.mainloop()