import datetime
import pandas as pd 
import numpy as np

# Read the Excel file
ruta_doc = r"fusion_seg_control.csv"
excel_inicial = pd.read_csv(ruta_doc);

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
    'record_id' : 'codigo_mamavida',
    'id_visita' : 'id_visita',
    'GLUC_SEG' : 'glucosa',
    'homocist_SEG' : 'homocisteina',
    'pcr_SEG' : 'pcr',
    'il6_SEG' : 'il6',
    'InSUL_seg' : 'insulina',
    'HOMA_seg' : 'homa',
    'colestotal_SEG' : 'colesterol_total',
    'colest_hdl_SEG' : 'colesterol_hdl',
    'colest_no-HDL_seg' : 'colesterol_no_hdl',
    'colest_LDL_seg' : 'colesterol_ldl',
    'TG_SEG' : 'tg',
    'FSH_SEG' : 'fsh',
    'ESTRADIOL_SEG' : 'estradiol',
    'tsh_SEG' : 'tsh',
    'T4L_SEG' : 't4_l',
    'VITd_SEG' : 'vitamina_d_analitica',
    'HBa1C_SEG' : 'hba1c',
    'sodio_seg' : 'sodio_analitica',
    'potasio_seg' : 'potasio_analitica',
    'calciob_seg' : 'calcio_analitica',
    'cloro_seg' : 'cloro_analitica'
}

# Change the names of each column following catalogo_variables
excel_inicial.rename(columns=catalogo_variables, inplace=True);

# Filtrar las columnas en función del form que nos interesa
# Agrupamos las claves del diccionario creado en una lista
claves_lista = list(catalogo_variables.values());
delete_columns = [col for col in excel_inicial.columns if col not in claves_lista];
excel_transformado = excel_inicial.drop(columns=delete_columns);

# Aplicar la función y crear la nueva columna al principio del DataFrame
excel_transformado.insert(0, 'record_id', excel_transformado['codigo_mamavida'])

# Ordenar el DataFrame por el índice
excel_ordenado = excel_transformado.sort_values(by=['record_id', 'id_visita'])

# Create four additional columns to match redcap
excel_ordenado.insert(1, 'redcap_event_name', 'visitas_arm_1');
excel_ordenado.insert(2, 'redcap_repeat_instrument', '');
excel_ordenado.insert(3, 'redcap_repeat_instance', excel_ordenado.groupby('record_id').cumcount() + 2)

# Incluimos columnas de miostatina y fgf-21 (aunque van vacías)
excel_ordenado['miostatina'] = ''
excel_ordenado['fgf_21'] = ''

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_ordenado['analtica_complete'] = ''
for index, row in excel_ordenado.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_without_observations = row.drop(labels=[ 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'analtica_complete', 'miostatina', 'fgf_21', 'codigo_mamavida', 'id_visita' , 'record_id'])
    
    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    if row_without_observations.dropna().empty:
        excel_ordenado.at[index, 'analtica_complete'] = ''

    # Comprueba si todas las demás columnas están completas
    elif row_without_observations.notnull().all():
        excel_ordenado.at[index, 'analtica_complete'] = '2'
    
    # Si hay algún dato no nulo en la fila
    else:
        if row_without_observations.sum() == 0.0:
            excel_ordenado.at[index, 'analtica_complete'] = ''
        else:
            excel_ordenado.at[index, 'analtica_complete'] = '1'

excel_ordenado = excel_ordenado.drop(columns=['codigo_mamavida', 'id_visita']);

for index, row in excel_ordenado.iterrows():
    if row.drop(labels=['redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'analtica_complete', 'miostatina', 'fgf_21', 'record_id']).sum() == 0.0:
        excel_ordenado.drop(index=index, axis=0, inplace=True)
    
# Create CSV document for Redcap
datos_analitica_seg = "datos_analitica_seg.csv";
excel_ordenado.to_csv(datos_analitica_seg, index=False);

print("Archivo CSV exportado exitosamente.")

