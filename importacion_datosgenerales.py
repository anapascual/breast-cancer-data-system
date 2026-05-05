import datetime
import pandas as pd 
import numpy as np

# Read the Excel file
ruta_doc = r"docs\basal_fusion_raw_labels.xlsx";
excel_inicial = pd.read_excel(ruta_doc);

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

# Establecer la columna 'record_id' como índice del DataFrame
excel_inicial.set_index('record_id', inplace=True)

# Ordenar el DataFrame por el índice
excel_ordenado = excel_inicial.sort_index()

# Create a dictionary for the names of the variables
catalogo_variables = {
    #'CODIGO' : 'codigo_mamavida',
    "fechanacimiento" : "fecha_nacimiento",
    "peso_habitual" : "peso_habitual_kg"
}

# Change the names of each column following catalogo_variables
excel_ordenado.rename(columns=catalogo_variables, inplace=True);

# Filtrar las columnas en función del form que nos interesa
# Agrupamos las claves del diccionario creado en una lista
claves_lista = list(catalogo_variables.values());
delete_columns = [col for col in excel_ordenado.columns if col not in claves_lista];
excel_transformado = excel_ordenado.drop(columns=delete_columns);

# Create four additional columns to match redcap
excel_transformado.insert(0, 'record_id', range(1, len(excel_inicial) + 1))
excel_transformado.insert(1, 'redcap_event_name', 'general_arm_1')
excel_transformado.insert(2, 'redcap_repeat_instrument', '')
excel_transformado.insert(3, 'redcap_repeat_instance', '')

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_transformado['datos_generales_complete'] = ''
for index, row in excel_transformado.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_without_observations = row.drop(labels=['record_id', 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'datos_generales_complete'])
    
    # Comprueba si todas las demás columnas están completas
    if row_without_observations.notnull().all():
        excel_transformado.at[index, 'datos_generales_complete'] = '2'
    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    elif row_without_observations.dropna().empty:
        excel_transformado.at[index, 'datos_generales_complete'] = ''
    # Si hay algún dato no nulo en la fila
    else:
        excel_transformado.at[index, 'datos_generales_complete'] = '1'
    
# Create CSV document for Redcap
datos_generales = "datos_generales.csv";
excel_transformado.to_csv(datos_generales, index=False);

print("Archivo CSV exportado exitosamente.")

