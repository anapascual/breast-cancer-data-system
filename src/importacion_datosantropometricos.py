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
    

# Create a dictionary for the names of the variables
catalogo_variables = {
    'CODIGO' : 'codigo_mamavida',
    'peso_basal' : 'peso_kg',
    'talla_basal' : 'talla_m',
    'IMC_basal' : 'imc_kgm2',
    'cintura' : 'perimetro_cintura_cm',
    'cadera' : 'perimetro_cadera_cm',
    'mano_dinamome' : 'manos_dinamometria',
    'dina_1_basal_dcha' : 'dinamometria_1_dcha_kg',
    'dina_2_basal_dcha': 'dinamometria_2_dcha_kg',
    'dina_3_basal_dcha' : 'dinamometria_3_dcha_kg',
    'dina_media_basal dcha' : 'dinamometria_media_dcha',
    'dina_1_basal_izq' : 'dinamometria_1_izda_kg',
    'dina_2_basal_izq' : 'dinamometria_2_izda_kg',
    'dina_3_basal_izq' : 'dinamometria_3_izda_kg',
    'dina_media_basal izq' : 'dinamometria_media_izda',
    'escal_ECOG_basal' : 'escala_ecog'
}

# Change the names of each column following catalogo_variables
excel_inicial.rename(columns=catalogo_variables, inplace=True);

# Change the data type of the integer columns to int
# Definir las columnas que queremos convertir
integer_columns = ['manos_dinamometria', 'escala_ecog']

# Filtrar las columnas en función del form que nos interesa
# Agrupamos las claves del diccionario creado en una lista
claves_lista = list(catalogo_variables.values());
delete_columns = [col for col in excel_inicial.columns if col not in claves_lista];
excel_transformado = excel_inicial.drop(columns=delete_columns);

# Aplicar la función y crear la nueva columna al principio del DataFrame
excel_transformado.insert(0, 'record_id', excel_inicial['codigo_mamavida'].apply(extraer_numero))

# Ordenar el DataFrame por el índice
excel_ordenado = excel_transformado.sort_values(by=['record_id'])

# Create four additional columns to match redcap
excel_ordenado.insert(1, 'redcap_event_name', 'visitas_arm_1');
excel_ordenado.insert(2, 'redcap_repeat_instrument', '');
excel_ordenado.insert(3, 'redcap_repeat_instance', '1');

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_ordenado['datos_antropomtricos_complete'] = ''

columnas_rellenas_1 = ['peso_kg', 'talla_m', 'perimetro_cintura_cm', 'perimetro_cadera_cm', 'manos_dinamometria', 'escala_ecog']
columnas_dinamometria_dcha = ['dinamometria_1_dcha_kg', 'dinamometria_2_dcha_kg', 'dinamometria_3_dcha_kg']
columnas_dinamometria_izda = ['dinamometria_1_izda_kg', 'dinamometria_2_izda_kg', 'dinamometria_3_izda_kg']

for index, row in excel_ordenado.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_without_observations = row.drop(labels=['redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'imc_kgm2', 'datos_antropomtricos_complete'])
    row_dinamometria_dcha = row[columnas_dinamometria_dcha]
    row_dinamometria_izda = row[columnas_dinamometria_izda]
    row_rellenas = row[columnas_rellenas_1]
    
    # Comprueba si todas las demás columnas están completas
    if row_without_observations.notnull().all():
        excel_ordenado.at[index, 'datos_antropomtricos_complete'] = '2'

    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    if row_rellenas.dropna().empty:
        excel_ordenado.at[index, 'datos_antropomtricos_complete'] = ''

    else:
        if (row_dinamometria_dcha.notnull().all() or row_dinamometria_izda.notnull().all()) and row_rellenas.notnull().all():
            excel_ordenado.at[index, 'datos_antropomtricos_complete'] = '2'
        else:
            excel_ordenado.at[index, 'datos_antropomtricos_complete'] = '1'

    

# Aplicar la conversión solo si en la fila hay algún dato
for column in integer_columns:
    # Para cada columna de la lista de columnas que son integers del DataFrame que se ha obtenido
    excel_ordenado[column] = excel_ordenado[column].apply(
        # Se aplica la función lambda: se convierte el dato a tipo entero (int), y si no es posible, se deja vacío
        lambda x: str(int(x)) if pd.notnull(x) else ''
    )

excel_ordenado = excel_ordenado.drop(columns=['codigo_mamavida']);
    
# Create CSV document for Redcap
datos_antropometricos = "datos_antropometricos.csv";
excel_ordenado.to_csv(datos_antropometricos, index=False);

print("Archivo CSV exportado exitosamente.")

