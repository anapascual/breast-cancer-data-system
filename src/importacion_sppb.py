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
    'test1_equil_basal' : 'sppb_pies_juntos',
    'test2_equil_basal' : 'sppb_semi_tandem',
    'test3_equil_basal' : 'sppb_tandem',
    'puntos_speed test_basal' : 'sppb_velocidad_marcha',
    'Pretest_silla_BASAL' : 'sppb_capacidad_levantarse',
    'test_silla_basal_s' : 'sppb_levantarse_5_reps',
    'test_silla_basal' : 'sppb_total_silla',
    #'pto_total_sppb_basal' : 'sppb_total',
    'clasifSPPB' : 'sppb_clasificacion',
    'Tiempo_get_up_basal': 'tiempo_levantarse',
    'calsif_get_up_basal': 'clasificacion_levantarse'
}

# Change the names of each column following catalogo_variables
excel_inicial.rename(columns=catalogo_variables, inplace=True);

# Change the data type of the integer columns to int
integer_columns = ['sppb_pies_juntos', 'sppb_semi_tandem', 'sppb_tandem', 'sppb_velocidad_marcha', 'sppb_capacidad_levantarse', 'sppb_total_silla', 'clasificacion_levantarse', 'sppb_clasificacion']
# Convertir las columnas a cadenas de texto antes de la conversión
excel_inicial[integer_columns] = excel_inicial[integer_columns].astype(str)

# Iterate over each column and convert its type to int
for col in integer_columns:
    excel_inicial[col] = excel_inicial[col].apply(lambda x: int(float(x)) if x.strip().replace('.', '').isdigit() else pd.NA)

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
excel_ordenado.insert(1, 'redcap_event_name', 'visitas_arm_1')
excel_ordenado.insert(2, 'redcap_repeat_instrument', '')
excel_ordenado.insert(3, 'redcap_repeat_instance', '1')

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_ordenado['test_sppb_test_get_up_and_go_complete'] = ''
for index, row in excel_ordenado.iterrows():
    # Elimina la columna 'OBSERVACIONES' de la evaluación
    row_without_observations = row.drop(labels=[ 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'test_sppb_test_get_up_and_go_complete'])
    
    # Comprueba si todas las demás columnas están completas
    if row_without_observations.notnull().all():
        excel_ordenado.at[index, 'test_sppb_test_get_up_and_go_complete'] = '2'
    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    elif row_without_observations.dropna().empty:
        excel_ordenado.at[index, 'test_sppb_test_get_up_and_go_complete'] = ''
    # Si hay algún dato no nulo en la fila
    else:
        excel_ordenado.at[index, 'test_sppb_test_get_up_and_go_complete'] = '1'

excel_ordenado = excel_ordenado.drop(columns=['codigo_mamavida']);

for index, row in excel_ordenado.iterrows():
    if row.drop(labels=['record_id','redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'test_sppb_test_get_up_and_go_complete']).sum() == 0:
        excel_ordenado.drop(index=index, axis=0, inplace=True)
    
# Create CSV document for Redcap
datos_sppb = "datos_sppb.csv";
excel_ordenado.to_csv(datos_sppb, index=False);

print("Archivo CSV exportado exitosamente.")

