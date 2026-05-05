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
    '1DIAS_activfisica_intensa_BASAL' : 'actividad_intensa_dias',
    '1activfisica_intensa_basal' : 'realizo_actividad_intensa',
    '2horas_actvfisica_intensa_basal' : 'actividad_intensa_horas',
    '2min_actvfisica_intensa_basal' : 'actividad_intensa_minutos',
    '2no sabe_intensa_basal' : 'actividad_intensa_nsnc',
    '3DIAS_activfisica_moderada_BASAL' : 'actividad_moderada_dias',
    '3activfisica_moderada_basal' : 'realizo_actividad_moderada',
    '4horas_actvfisica_moderada_basal' : 'actividad_moderada_horas',
    '4min_actvfisica_moderada_basal' : 'actividad_moderada_minutos',
    '4activfisica_moderada_basal' : 'actividad_moderada_nsnc',
    '5Dias_andar_10m_basal' : 'caminar_dias',
    '5activfisica_10min_basal' : 'realizo_caminar',
    '6horas_CaMINAR_día_basal' : 'caminar_horas',
    '6min_caminar_min_basal' : 'caminar_minutos',
    '6CAMINAR_basal' : 'caminar_nsnc',
    '7horas_sENTADOdía_basal' : 'sentado_horas',
    '7min_sENTADOdia_basal' : 'sentado_minutos', 
    '7_sENTADO_basal' : 'sentado_nsnc',

}

# Change the names of each column following catalogo_variables
excel_inicial.rename(columns=catalogo_variables, inplace=True);

# Filtrar las columnas en función del form que nos interesa
# Agrupamos las claves del diccionario creado en una lista
claves_lista = list(catalogo_variables.values());
delete_columns = [col for col in excel_inicial.columns if col not in claves_lista];
excel_transformado = excel_inicial.drop(columns=delete_columns);

# Hay columnas que necesitamos cambiar el 2 por un 1 y el 1 por un 0
columnas_realizo = ['realizo_actividad_intensa', 'realizo_actividad_moderada', 'realizo_caminar']
columnas_nsnc = ['actividad_intensa_nsnc', 'actividad_moderada_nsnc', 'caminar_nsnc', 'sentado_nsnc']

# Reemplazar los valores en todas las columnas especificadas
excel_transformado[columnas_realizo] = excel_transformado[columnas_realizo].replace({1: 0, 2: 1})
excel_transformado[columnas_nsnc] = excel_transformado[columnas_nsnc].replace({1: 0, 2: 1})

# Aplicar la función y crear la nueva columna al principio del DataFrame
excel_transformado.insert(0, 'record_id', excel_transformado['codigo_mamavida'].apply(extraer_numero))

# Ordenar el DataFrame por el índice
excel_ordenado = excel_transformado.sort_values(by=['record_id'])

# Create four additional columns to match redcap
excel_ordenado.insert(1, 'redcap_event_name', 'visitas_arm_1');
excel_ordenado.insert(2, 'redcap_repeat_instrument', '');
excel_ordenado.insert(3, 'redcap_repeat_instance', '1');
excel_ordenado['mets'] = ''

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_ordenado['ipaq_actividad_fsica_complete'] = ''
for index, row in excel_ordenado.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_without_observations = row.drop(labels=[ 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'ipaq_actividad_fsica_complete', 'mets'])
    
    # Comprueba si todas las demás columnas están completas
    if row_without_observations.notnull().all():
        excel_ordenado.at[index, 'ipaq_actividad_fsica_complete'] = '2'
    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    elif row_without_observations.dropna().empty:
        excel_ordenado.at[index, 'ipaq_actividad_fsica_complete'] = ''
    # Si hay algún dato no nulo en la fila
    else:
        excel_ordenado.at[index, 'ipaq_actividad_fsica_complete'] = '1'

# Change the data type of the integer columns to int
integer_columns = excel_ordenado.columns.difference(['codigo_mamavida', 'mets', 'redcap_event_name', 'redcap_repeat_instrument'])
# Aplicar la conversión solo si en la fila hay algún dato
for column in integer_columns:
    excel_ordenado[column] = excel_ordenado[column].apply(
        lambda x: str(int(x)) if pd.notnull(x) else ''
    )

excel_ordenado = excel_ordenado.drop(columns=['codigo_mamavida']);

for index, row in excel_ordenado.iterrows():
    rows_nsnc = row[columnas_nsnc]
    # Verifica si todas las columnas en `columnas_nsnc` están vacías (NaN, cadena vacía, o contienen solo espacios en blanco)
    if rows_nsnc.apply(lambda x: pd.isna(x) or str(x).strip() == '').all():
        # Verifica si la suma de las otras columnas es 0
        if row.drop(labels=["record_id", 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'ipaq_actividad_fsica_complete', 'mets']).sum() == 0:
            excel_ordenado.drop(index=index, axis=0, inplace=True)

    
# Create CSV document for Redcap
datos_ipaq = "datos_ipaq.csv";
excel_ordenado.to_csv(datos_ipaq, index=False);

print("Archivo CSV exportado exitosamente.")

