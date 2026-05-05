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
    'usa_aceite_basal': 'usa_aceite_oliva',
    'cuanto_aceite_basal' : 'consumo_aceite_diario',
    'cuanta_verd_basal' : 'raciones_verdura_diario',
    'cuanta_fruta_basal' : 'piezas_fruta_diario',
    'cuanta_carneroja_basal' : 'raciones_carne_roja_diario',
    'cuanta_mantequilla_basal' : 'raciones_mantequilla_dia',
    'cuanta_bebida_basal' : 'bebidas_carbonatadas_dia',
    'cuanto_vino_basal' : 'consumo_vino_semana',
    'cuanta_legumbre_basal' : 'raciones_legumbres_semana',
    'pesc_blan_basal' : 'raciones_pescado_semana',
    'cuanto_dulce_basal' : 'consumo_reposteria',
    'cuanto_frutos secos_basal' : 'consumo_frutos_secos',
    'cuanto_pollo_basal' : 'preferencia_pollo_ternera',
    'cuanto_sofritos_basal' : 'consumo_sofritos_semana'
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
excel_ordenado['puntuacion_total_dieta'] = ''

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_ordenado['medas14_adherencia_a_la_dieta_mediterrnea_complete'] = ''
for index, row in excel_ordenado.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_without_observations = row.drop(labels=['record_id', 'codigo_mamavida', 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'puntuacion_total_dieta', 'medas14_adherencia_a_la_dieta_mediterrnea_complete'])
    
    # Comprueba si todas las demás columnas están completas
    if row_without_observations.notnull().all():
        excel_ordenado.at[index, 'medas14_adherencia_a_la_dieta_mediterrnea_complete'] = '2'
    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    elif row_without_observations.dropna().empty:
        excel_ordenado.at[index, 'medas14_adherencia_a_la_dieta_mediterrnea_complete'] = ''
    # Si hay algún dato no nulo en la fila
    else:
        excel_ordenado.at[index, 'medas14_adherencia_a_la_dieta_mediterrnea_complete'] = '1'

# Change the data type of the integer columns to int
integer_columns = excel_ordenado.columns.difference(['codigo_mamavida', 'redcap_repeat_instrument', 'puntuacion_total_dieta', 'redcap_event_name', 'medas14_adherencia_a_la_dieta_mediterrnea_complete'])
# Aplicar la conversión solo si en la fila hay algún dato
for column in integer_columns:
    excel_ordenado[column] = excel_ordenado[column].apply(
        lambda x: str(int(x)) if pd.notnull(x) else ''
    )

excel_ordenado = excel_ordenado.drop(columns=['codigo_mamavida']);
    
# Create CSV document for Redcap
datos_medas = "datos_medas.csv";
excel_ordenado.to_csv(datos_medas, index=False);

print("Archivo CSV exportado exitosamente.")

