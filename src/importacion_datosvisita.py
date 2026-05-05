import datetime
import pandas as pd 
import numpy as np

# Read the Excel file
ruta_doc = r"docs\basal_fusion_raw_labels.xlsx";
excel_inicial = pd.read_excel(ruta_doc);
ruta_doc_control_paciente = r"docs\CONTROL_PACIENTE.xlsx";
excel_control_paciente = pd.read_excel(ruta_doc_control_paciente);

# Función para extraer el número del código
def extraer_numero(codigo):
    try:
        # Extraer el número después del guion
        return int(codigo.split('-')[-1])
    except ValueError:
        # En caso de que no se pueda convertir a entero, devolver un valor alto para que quede al final
        return float('inf')
    
# Funcion para extraer el número del código de control_paciente
def extraer_numero_control_paciente(codigo):
    if isinstance(codigo, float):
        pass
    else:
        try:
            # Extraer el número después del guion
            return int(codigo.split('_')[-1])
        except ValueError:
            # En caso de que no se pueda convertir a entero, devolver un valor alto para que quede al final
            return float('inf')
    
# Crear una nueva columna con los números extraídos
excel_inicial['record_id'] = excel_inicial['CODIGO'].apply(extraer_numero)
excel_control_paciente['record_id'] = excel_control_paciente['id'].apply(extraer_numero_control_paciente)

# Establecer la columna 'record_id' como índice del DataFrame
excel_inicial.set_index('record_id', inplace=True)
excel_control_paciente.set_index('record_id', inplace=True)

# Ordenar el DataFrame por el índice
excel_ordenado = excel_inicial.sort_index()
excel_control_paciente = excel_control_paciente.sort_index()

# Create a dictionary for the names of the variables
catalogo_variables = {
    #'CODIGO' : 'codigo_mamavida',
    'Idvisitas' : 'id_visita',
    #'fechavalor' : 'fecha_visita',
    'VISITA inicio' : 'control_paciente',
    'Observaciones' : 'observaciones'
}

variables_control_paciente = {
    'invest' : 'investigadora',
    'VISITA inicio' : 'control_paciente',
    'INICIO_A' : 'fecha_visita',
    'OBSERVACIONES' : 'observaciones'
}

# Diccionario de mapeo de texto a número
texto_a_numero = {
    "Realizada": 1,
    "NO citada": 2,
    "Incompareciente": 3,
    "Pte de Citar": 4,
    "Ya citada": 5,
    "No hecha prueba": 6,
    "Retirada del estudio": 7,
    "Retira consentimiento": 8,
    "Hecha petición Selene": 9
}

investigadora_a_numero = {
    "PILAR" : 1,
    "ANGELICA" : 2,
    "MARIA" : 3,
    "GEMMA" : 4
}

# Change the names of each column following catalogo_variables
excel_ordenado.rename(columns=catalogo_variables, inplace=True);
excel_control_paciente.rename(columns=variables_control_paciente, inplace=True)

# Convertir la columna 'estado' usando el diccionario de mapeo
excel_control_paciente['control_paciente'] = excel_control_paciente['control_paciente'].map(texto_a_numero)
excel_control_paciente['investigadora'] = excel_control_paciente['investigadora'].map(investigadora_a_numero)

# Change the data type of the integer columns to int
integer_columns = ['control_paciente']
excel_control_paciente[integer_columns] = excel_control_paciente[integer_columns].fillna(0.0)
excel_control_paciente[integer_columns] = excel_control_paciente[integer_columns].astype(int)
excel_control_paciente[integer_columns] = excel_control_paciente[integer_columns].astype(str)

# Filtrar las columnas en función del form que nos interesa
# Agrupamos las claves del diccionario creado en una lista
claves_lista = list(catalogo_variables.values());
delete_columns = [col for col in excel_ordenado.columns if col not in claves_lista];
excel_transformado = excel_ordenado.drop(columns=delete_columns);

claves_control_paciente = list(variables_control_paciente.values())
delete_columns_control = [col for col in excel_control_paciente.columns if col not in claves_control_paciente]
excel_control_paciente = excel_control_paciente.drop(columns=delete_columns_control)

# Create four additional columns to match redcap
excel_transformado.insert(0, 'record_id', range(1, len(excel_inicial) + 1));
excel_transformado.insert(1, 'redcap_event_name', 'visitas_arm_1');
excel_transformado.insert(2, 'redcap_repeat_instrument', '');
excel_transformado.insert(3, 'redcap_repeat_instance', '1');
excel_transformado.insert(4, 'id_visita', '0');

# Convertir la columna 'record_id' a tipo numérico si es posible
excel_transformado['record_id'] = pd.to_numeric(excel_transformado['record_id'], errors='coerce')
# Establecer la columna 'record_id' como el índice del DataFrame
excel_transformado.set_index('record_id', inplace=True)

# Fusionar (merge) los DataFrames en función de la columna de identificación común ('id')
excel_fusionado = pd.merge(excel_transformado, excel_control_paciente, on='record_id', how='left')

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_fusionado['datos_de_la_visita_complete'] = ''
for index, row in excel_fusionado.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_without_observations = row.drop(labels=[ 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'observaciones', 'datos_de_la_visita_complete'])
    
    # Comprueba si todas las demás columnas están completas
    if row_without_observations.notnull().all():
        excel_fusionado.at[index, 'datos_de_la_visita_complete'] = '2'
    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    elif row_without_observations.dropna().empty:
        excel_fusionado.at[index, 'datos_de_la_visita_complete'] = ''
    # Si hay algún dato no nulo en la fila
    else:
        excel_fusionado.at[index, 'datos_de_la_visita_complete'] = '1'

# Change the data type of the integer columns to int
integer_columns = ['investigadora']
# Aplicar la conversión solo si en la fila hay algún dato
for column in integer_columns:
    excel_fusionado[column] = excel_fusionado[column].apply(
        lambda x: str(int(x)) if pd.notnull(x) else ''
    )

# Create CSV document for Redcap
datos_visita = "datos_visita.csv";
excel_fusionado.to_csv(datos_visita, index=True);

print("Archivo CSV exportado exitosamente.")

