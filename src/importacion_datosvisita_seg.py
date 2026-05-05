import datetime
import pandas as pd 
import numpy as np

# Read the Excel file
ruta_doc_control_paciente = r"docs\CONTROL_PACIENTE.xlsx";
excel_control_paciente = pd.read_excel(ruta_doc_control_paciente);


# Especificar las columnas que quieres copiar como una lista
columnas_df2 = ['id', 'invest', 'VISITA_6 meses', 'VISITA_1 AÑO', 'VISITA_2 AÑOS', 'OBSERVACIONES', 'Fecha_visita_6 meses', 'Fecha_ visita_1 AÑO', 'Fecha_visita_2 AÑOS']

df_2 = excel_control_paciente[columnas_df2]

# Crear una lista para almacenar las filas de la tabla pivotada
pivot_data = []

# Definir los nombres de las visitas y las columnas correspondientes
id_visita = {
    "1": ("Fecha_visita_6 meses", 'VISITA_6 meses'),
    "2": ("Fecha_ visita_1 AÑO", 'VISITA_1 AÑO'),
    "3": ("Fecha_visita_2 AÑOS", 'VISITA_2 AÑOS'),
}

# Iterar sobre las filas del DataFrame original
for index, row in df_2.iterrows():
    # Iterar sobre las visitas definidas
    for visit, (fecha_col, control_col) in id_visita.items():
        # Verificar si alguna de las celdas de fecha o control está vacía
        if pd.notna(row[fecha_col]) or pd.notna(row[control_col]):
            # Crear una nueva fila para la tabla pivotada
            new_row = {
                "id": row["id"],
                "investigadora": row["invest"],
                "fecha_visita": row[fecha_col],
                "control_paciente": row[control_col],
                "id_visita": visit,
                'observaciones':row['OBSERVACIONES']
            }
            # Agregar la nueva fila a la lista de datos pivotados
            pivot_data.append(new_row)

# Crear el DataFrame pivotado a partir de la lista de datos
df_pivotado = pd.DataFrame(pivot_data)

    
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
        

# Create a dictionary for the names of the variables

variables_control_paciente = {
    'id' : 'codigo_mamavida',
    'invest' : 'investigadora',
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


# Aplicar la función y crear la nueva columna al principio del DataFrame
df_pivotado.insert(0, 'record_id', df_pivotado['id'].apply(extraer_numero_control_paciente))

control_paciente = df_pivotado.sort_values(by=['record_id', 'id_visita'])

control_paciente.rename(columns=variables_control_paciente, inplace=True)

# Convertir la columna 'estado' usando el diccionario de mapeo
control_paciente['control_paciente'] = control_paciente['control_paciente'].map(texto_a_numero)
control_paciente['investigadora'] = control_paciente['investigadora'].map(investigadora_a_numero)

# Create four additional columns to match redcap
control_paciente.insert(1, 'redcap_event_name', 'visitas_arm_1');
control_paciente.insert(2, 'redcap_repeat_instrument', '');
control_paciente.insert(3, 'redcap_repeat_instance', control_paciente.groupby('record_id').cumcount() + 2)

# Si solo está relleno el campo de la investigadora, eliminar la fila
for index, row in control_paciente.iterrows():
    # Selecciona solo la serie de datos
    data = row.drop(labels=['investigadora', 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'record_id', 'observaciones'])
    # Verifica si todos los demás campos son nulos
    if data.isnull().all():
        # Elimina la fila basada en el índice
        control_paciente.drop(index, inplace=True)


# Nueva columna para comprobar que los datos se han rellenado todos completos
control_paciente['datos_de_la_visita_complete'] = ''
for index, row in control_paciente.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_without_observations = row.drop(labels=[ 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'observaciones', 'datos_de_la_visita_complete'])
    
    # Comprueba si todas las demás columnas están completas
    if row_without_observations.notnull().all():
        control_paciente.at[index, 'datos_de_la_visita_complete'] = '2'
    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    elif row_without_observations.dropna().empty:
        control_paciente.at[index, 'datos_de_la_visita_complete'] = ''
    # Si hay algún dato no nulo en la fila
    else:
        control_paciente.at[index, 'datos_de_la_visita_complete'] = '1'

control_paciente = control_paciente.dropna(subset=['record_id'])
control_paciente = control_paciente.drop(columns=['codigo_mamavida'])

print(control_paciente[control_paciente['record_id'] == 72])

# Change the data type of the integer columns to int
integer_columns = ['redcap_repeat_instance', 'control_paciente', 'id_visita', 'investigadora', 'record_id']
# Aplicar la conversión solo si en la fila hay algún dato
for column in integer_columns:
    control_paciente[column] = control_paciente[column].apply(
        lambda x: str(int(x)) if pd.notnull(x) else ''
    )

# Create CSV document for Redcap
datos_visita_seg = "datos_visita_seg.csv";
control_paciente.to_csv(datos_visita_seg, index=False);
print("Archivo CSV exportado exitosamente.")
