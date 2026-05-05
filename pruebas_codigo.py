import datetime
import pandas as pd 
import numpy as np

# Read the Excel file
ruta_doc = r"docs\seg_fusion_raw_labels.xlsx";
excel_inicial = pd.read_excel(ruta_doc)
ruta_doc_control_paciente = r"datos_visita_seg.csv";
control_paciente = pd.read_csv(ruta_doc_control_paciente);

# Función para extraer el número del código
def extraer_numero(codigo):
    try:
        # Extraer el número después del guion
        return int(codigo.split('-')[-1])
    except ValueError:
        # En caso de que no se pueda convertir a entero, devolver un valor alto para que quede al final
        return float('inf')
    
# Crear una nueva columna con los números extraídos
excel_inicial['record_id'] = excel_inicial['CODIGO'].apply(extraer_numero)
# Cambiar el nombre de la columna
excel_inicial.rename(columns={"Idvisitas": "id_visita"}, inplace=True)

fusion_seg_control = pd.merge(excel_inicial, control_paciente, on=['record_id', 'id_visita'], how='right')

fusion_seg_control = fusion_seg_control.drop(columns=['CODIGO', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'redcap_event_name'])

# Create CSV document for Redcap
fusion_datos = "fusion_seg_control.csv";
fusion_seg_control.to_csv(fusion_datos, index=False);

print("Archivo CSV exportado exitosamente.")