import datetime
import pandas as pd 
import numpy as np

# Read the Excel file
ruta_doc = r"docs\seg_raw_con_codigomamavida.xlsx";
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


# Create a dictionary for the names of the variables
catalogo_variables = {
    'CODIGO' : 'codigo_mamavida',
    'Idvisitas' : 'id_visita',
    'fechavalor_seg' : 'fecha_visita',
}

variables_control_paciente = {
    'id' : 'codigo_mamavida',
    '1 VISITA_B_6 meses' : 'control_paciente_6meses',
    '2 VISITA_C_1 AÑO' : 'control_paciente_1año',
    '3_VISITA_D_2 AÑOS' : 'control_paciente_2años',
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





# Especificar las columnas que quieres copiar como una lista
columnas_df1 = ['CODIGO', 'Idvisitas', 'fechavalor_seg']
columnas_df2 = ['id', '1 VISITA_B_6 meses', '2 VISITA_C_1 AÑO', '3_VISITA_D_2 AÑOS', 'OBSERVACIONES']

df_1 = excel_inicial[columnas_df1]
df_2 = excel_control_paciente[columnas_df2]
# Aplicar la función y crear la nueva columna al principio del DataFrame
df_1.insert(0, 'record_id', df_1['CODIGO'].apply(extraer_numero))
df_2.insert(0, 'record_id', df_2['id'].apply(extraer_numero_control_paciente))

df_3 = pd.merge(df_1, df_2, on='record_id', how='left')

excel_ordenado_control = df_3.sort_values(by=['record_id', 'Idvisitas'])

excel_ordenado_control['control_paciente'] = ''

for index, row in excel_ordenado_control.iterrows():
    id_visita = row['Idvisitas']
    if id_visita == 1:
        #Codigo para que ponga control_paciente de 6meses
        excel_ordenado_control.at[index, 'control_paciente'] = row['1 VISITA_B_6 meses']
    elif id_visita == 2:
        # codigo para que ponga control paciente de 1 año
        excel_ordenado_control.at[index, 'control_paciente'] = row['2 VISITA_C_1 AÑO']
    elif id_visita == 3:
        # codigo para que ponga control paciente de 2 años
        excel_ordenado_control.at[index, 'control_paciente'] = row['3_VISITA_D_2 AÑOS']
    else:
        excel_ordenado_control.at[index, 'control_paciente'] = 'No hay datos'
        
control_paciente = excel_ordenado_control.drop(columns=['CODIGO', 'id', '1 VISITA_B_6 meses', '2 VISITA_C_1 AÑO', '3_VISITA_D_2 AÑOS'])





# Change the names of each column following catalogo_variables
excel_inicial.rename(columns=catalogo_variables, inplace=True);
control_paciente.rename(columns=variables_control_paciente, inplace=True)

# Change the data type of the integer columns to int
integer_columns = ['control_paciente']
# Aplicar la conversión solo si en la fila hay algún dato
for column in integer_columns:
    control_paciente[column] = control_paciente[column].apply(
        lambda x: str(int(x)) if pd.notnull(x) and x != 0 else ''
    )

# Filtrar las columnas en función del form que nos interesa
# Agrupamos las claves del diccionario creado en una lista
claves_lista = list(catalogo_variables.values());
delete_columns = [col for col in excel_inicial.columns if col not in claves_lista];
excel_transformado = excel_inicial.drop(columns=delete_columns);

claves_control_paciente = list(variables_control_paciente.values())
delete_columns_control = [col for col in control_paciente.columns if col not in claves_control_paciente]
control_paciente = control_paciente.drop(columns=delete_columns_control)

# Aplicar la función y crear la nueva columna al principio del DataFrame
excel_transformado.insert(0, 'record_id', excel_inicial['codigo_mamavida'].apply(extraer_numero))
control_paciente.insert(0, 'record_id', control_paciente['codigo_mamavida'].apply(extraer_numero_control_paciente))

# Ordenar el DataFrame por el índice
excel_ordenado = excel_transformado.sort_values(by=['record_id'])
control_paciente = control_paciente.sort_values(by=['record_id'])

excel_ordenado = excel_ordenado.drop(columns=['codigo_mamavida']);
control_paciente = control_paciente.drop(columns=['codigo_mamavida']);

# Fusionar (merge) los DataFrames en función de la columna de identificación común ('id')
excel_fusionado = pd.merge(excel_transformado, control_paciente, on='record_id', how='left')
excel_fusionado = excel_fusionado.sort_values(by=['record_id', 'id_visita'])
# Create four additional columns to match redcap
excel_fusionado.insert(1, 'redcap_event_name', 'endnutrud_pat_mama_arm_1');
excel_fusionado.insert(2, 'redcap_repeat_instrument', '');
excel_fusionado.insert(3, 'redcap_repeat_instance', excel_fusionado.groupby('record_id').cumcount() + 2)
excel_fusionado = excel_fusionado.drop(columns=['codigo_mamavida'])

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_fusionado['datos_de_la_visita_complete'] = excel_fusionado.apply(lambda row: '2' if row.notnull().all() else '1', axis=1)

# Create CSV document for Redcap
datos_visita_seg = "datos_visita_seg.csv"
excel_fusionado.to_csv(datos_visita_seg, index=False)

print("Archivo CSV exportado exitosamente.")

