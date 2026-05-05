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
    'eco_grasasubc_basal_1' : 'eco_grasa_subcutanea_1',
    'eco_ejex_basal_1' : 'eco_eje_x_1',
    'eco_ejey_basal_1' : 'eco_eje_y_1',
    'eco_circumf_basal_1' : 'eco_circunf_1',
    'eco_area_basal_1' : 'eco_area_1',
    'eco_contraccio_distancia _basal_1' : 'eco_contraccion_1',
    'ECO_longitud_distancia_basal_1' : 'eco_long_distancia_1',
    'ECO_grasasubcut_superf_basal_1' : 'eco_abd_subcut_superf_1',
    'ECO_grasasubcut_total_basal_1' : 'eco_abd_subcut_total_1',
    'ECO_grasas_preperitoneal_basal_1' : 'eco_abd_preperitoneal_1',
    'eco_grasasubc_basal_2' : 'eco_grasa_subcutanea_2',
    'eco_ejex_basal_2' : 'eco_eje_x_2',
    'eco_ejey_basal_2' : 'eco_eje_y_2',
    'eco_circumf_basal_2' : 'eco_circunf_2',
    'eco_area_basal_2' : 'eco_area_2',
    'eco_contraccio_distancia _basal_2' : 'eco_contraccion_2',
    'ECO_longitud_distancia_basal_2' : 'eco_long_distancia_2',
    'ECO_grasasubcut_superf_basal_2' : 'eco_abd_subcut_superf_2',
    'ECO_grasasubcut_total_basal_2' : 'eco_abd_subcut_total_2',
    'ECO_grasas_preperitoneal_basal_2' : 'eco_abd_preperitoneal_2',
    'eco_grasasubc_basal_3' : 'eco_grasa_subcutanea_3',
    'eco_ejex_basal_3' : 'eco_eje_x_3',
    'eco_ejey_basal_3' : 'eco_eje_y_3',
    'eco_circumf_basal_3' : 'eco_circunf_3',
    'eco_area_basal_3' : 'eco_area_3',
    'eco_contraccio_distancia _basal_3' : 'eco_contraccion_3',
    'ECO_longitud_distancia_basal_3' : 'eco_long_distancia_3',
    'ECO_grasasubcut_superf_basal_3' : 'eco_abd_subcut_superf_3',
    'ECO_grasasubcut_total_basal_3' : 'eco_abd_subcut_total_3',
    'ECO_grasas_preperitoneal_basal_3' : 'eco_abd_preperitoneal_3'
}

# Change the names of each column following catalogo_variables
excel_inicial.rename(columns=catalogo_variables, inplace=True);

# Filtrar las columnas en función del form que nos interesa
# Agrupamos las claves del diccionario creado en una lista
claves_lista = list(catalogo_variables.values());
delete_columns = [col for col in excel_inicial.columns if col not in claves_lista];
excel_transformado = excel_inicial.drop(columns=delete_columns);

# Aplicar la función y crear la nueva columna al principio del DataFrame
excel_transformado.insert(0, 'record_id', excel_transformado['codigo_mamavida'].apply(extraer_numero))

# Ordenar el DataFrame por el índice
excel_ordenado = excel_transformado.sort_values(by=['record_id'])

# Create four additional columns to match redcap
excel_ordenado.insert(1, 'redcap_event_name', 'visitas_arm_1');
excel_ordenado.insert(2, 'redcap_repeat_instrument', '');
excel_ordenado.insert(3, 'redcap_repeat_instance', '1');
excel_ordenado.insert(4, 'valorable', '')

# Columna valorable: rellenar con 1 si hay al menos algún dato relleno dentro
excel_ordenado['valorable'] = ''
for index, row in excel_ordenado.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_for_valorable = row.drop(labels=['record_id', 'codigo_mamavida', 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'valorable'])
    
    # Comprueba si todas las demás columnas están completas
    if row_for_valorable.notnull().any():
        excel_ordenado.at[index, 'valorable'] = '1'

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_ordenado['eco_complete'] = ''
for index, row in excel_ordenado.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_without_observations = row.drop(labels=['record_id', 'codigo_mamavida', 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'valorable', 'eco_complete'])
    
    # Comprueba si todas las demás columnas están completas
    if row_without_observations.notnull().all():
        excel_ordenado.at[index, 'eco_complete'] = '2'
    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    elif row_without_observations.dropna().empty:
        excel_ordenado.at[index, 'eco_complete'] = ''
    # Si hay algún dato no nulo en la fila
    else:
        excel_ordenado.at[index, 'eco_complete'] = '1'

excel_ordenado = excel_ordenado.drop(columns=['codigo_mamavida']);
    
# Create CSV document for Redcap
datos_eco = "datos_eco.csv";
excel_ordenado.to_csv(datos_eco, index=False);

print("Archivo CSV exportado exitosamente.")

