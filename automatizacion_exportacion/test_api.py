import tkinter as tk
from tkinter import filedialog
import requests

# Clave de la API de REDCap
API_KEY_REDCAP = "20490714C6ECE27AF700C5D5FBC3C9C1"

def obtener_reporte_redcap():
    data = {
    'token': '20490714C6ECE27AF700C5D5FBC3C9C1',
    'content': 'report',
    'format': 'csv',
    'report_id': '964',
    'csvDelimiter': '',
    'rawOrLabel': 'raw',
    'rawOrLabelHeaders': 'raw',
    'exportCheckboxLabel': 'false',
    'returnFormat': 'json'
            }
    r = requests.post('http://redcap.idissc.org/redcap/api/',data=data)


    print('HTTP Status: ' + str(r.status_code))
    print(r.text)

# Crear la ventana principal
root = tk.Tk()
root.title("Exportar Reporte REDCap")

# Botón para exportar el reporte desde REDCap
exportar_reporte_btn = tk.Button(root, text="Exportar Reporte", command=obtener_reporte_redcap)
exportar_reporte_btn.pack(pady=20)

# Etiqueta para mostrar el resultado o mensaje de error
resultado_label = tk.Label(root, text="")
resultado_label.pack()

# Ejecutar la aplicación
root.mainloop()
