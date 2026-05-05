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
    'GLUC_basal' : 'glucosa',
    'homocist_basal' : 'homocisteina',
    'pcr_basal' : 'pcr',
    'il6_basal' : 'il6',
    'InSUL_basal' : 'insulina',
    'HOMA_basal' : 'homa',
    'colestotal_basal' : 'colesterol_total',
    'colest_hdl_basal' : 'colesterol_hdl',
    'colest_no-HDL_basal' : 'colesterol_no_hdl',
    'colest_LDL_basal' : 'colesterol_ldl',
    'TG_basal' : 'tg',
    'FSH_basal' : 'fsh',
    'ESTRADIOL_basal' : 'estradiol',
    'tsh_basal' : 'tsh',
    'T4L_basal' : 't4_l',
    'VITd_basal' : 'vitamina_d_analitica',
    'HBa1C_basal' : 'hba1c',
    'sodio_basal' : 'sodio_analitica',
    'potasio_basal' : 'potasio_analitica',
    'calciob_basal' : 'calcio_analitica',
    'cloro_basal' : 'cloro_analitica'
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

# Incluimos columnas de miostatina y fgf-21 (aunque van vacías)
excel_ordenado['miostatina'] = ''
excel_ordenado['fgf_21'] = ''

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_ordenado['analtica_complete'] = ''
for index, row in excel_ordenado.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_without_observations = row.drop(labels=[ 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'analtica_complete', 'miostatina', 'fgf_21', 'codigo_mamavida', 'record_id'])
    

    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    if row_without_observations.dropna().empty:
        excel_ordenado.at[index, 'analtica_complete'] = ''

    # Comprueba si todas las demás columnas están completas
    elif row_without_observations.notnull().all():
        excel_ordenado.at[index, 'analtica_complete'] = '2'
    
    # Si hay algún dato no nulo en la fila
    else:
        excel_ordenado.at[index, 'analtica_complete'] = '1'

excel_ordenado = excel_ordenado.drop(columns=['codigo_mamavida']);
    
# Create CSV document for Redcap
datos_analitica = "datos_analitica.csv";
excel_ordenado.to_csv(datos_analitica, index=False);

print("Archivo CSV exportado exitosamente.")

