import datetime
import pandas as pd 
import numpy as np

# Read the Excel file
ruta_doc = r"fusion_seg_control.csv";
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
    'HORA_desayuno_SEG' : 'hora_desayuno',
    'HORA_impedan_SEG' : 'hora_impedancia',
    'fm_SEG_kg' :'masa_grasa_kg',
    'fm_SEG_%' : 'masa_grasa_porc',
    'FFM_SEG_kg' : 'masa_magra_kg',
    'FFM_SEG_%' : 'masa_magra_porc',
    'REE_SEG' : 'consumo_e_reposo_kcal_dia',
    'PAL_SEG' : 'pal',
    'TEE_SEG' : 'consumo_tee_kcal_dia',
    'FMI_SEG' : 'indice_masa_grasa_kg_m2',
    'FFMI_SEG' : 'indice_masa_magra_kg_m2',
    'SMM_SEG' : 'masa_musculo_esqueletico_kg',
    'SMI_SEG' : 'smi',
    'brazo d_SEG' : 'impedancia_b_dcho',
    'brazo izq_SEG' : 'impedancia_b_izdo',
    'pierna d_SEG' : 'impedancia_p_dcha',
    'pierna izq_SEG' : 'impedancia_p_izda',
    'torso_SEG' : 'impedancia_torso',
    'TWC_L_SEG' : 'twc_l',
    'TWC_%_SEG' : 'twc_porc',
    'EWC_L_SEG' : 'ewc_l',
    'EWC_%_SEG' : 'ewc_porc',
    'resisten_SEG' : 'resistencia',
    'reactancia_SEG' : 'reactancia',
    'angu_fase_SEG' : 'angulo_fase',
    'angu_fase_percent_SEG' : 'angulo_fase_porc',
    'spa_seg-SEG' : 'spa',
    'grasavisceral_SEG' : 'grasa_visceral',
    'ECW/TBW_SEG' : 'ratio_ecw_tbw'
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

# Convertir el formato de hora al necesario
def convertir_hora(hora):
    if pd.isna(hora) or hora == "":
        return ""
    else:
        try:
            # Convertir el string a un objeto datetime
            hora_dt = pd.to_datetime(hora, format='%H:%M:%S')
            # Convertir el datetime a formato militar (HH:MM)
            return hora_dt.strftime('%H:%M')
        except ValueError:
            return hora
    
#Aplicar la función a las columnas
excel_ordenado['hora_desayuno'] = excel_ordenado['hora_desayuno'].apply(convertir_hora)
excel_ordenado['hora_impedancia'] = excel_ordenado['hora_impedancia'].apply(convertir_hora)

# Create four additional columns to match redcap
excel_ordenado.insert(1, 'redcap_event_name', 'visitas_arm_1');
excel_ordenado.insert(2, 'redcap_repeat_instrument', '');
excel_ordenado.insert(3, 'redcap_repeat_instance', excel_ordenado.groupby('record_id').cumcount() + 2)

# Nueva columna para comprobar que los datos se han rellenado todos completos
excel_ordenado['impedancia_seca_complete'] = ''
for index, row in excel_ordenado.iterrows():
    # Elimina las columnas que no se evaluarán
    row_without_observations = row.drop(labels=['record_id', 'codigo_mamavida', 'id_visita', 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'impedancia_seca_complete'])
    row_sum = row.drop(labels=['record_id', 'codigo_mamavida', 'id_visita', 'hora_impedancia', 'hora_desayuno', 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'impedancia_seca_complete'])

    # Comprueba si todas las demás columnas están completas
    if row_without_observations.notnull().all():
        excel_ordenado.at[index, 'impedancia_seca_complete'] = '2'
    
    # Comprueba si la fila está completamente vacía excepto las columnas indicadas anteriormente
    elif row_without_observations.dropna().empty:
        excel_ordenado.at[index, 'impedancia_seca_complete'] = ''
    elif row_sum.sum() == 0.0:
            excel_ordenado.at[index, 'impedancia_seca_complete'] = ''
    # Si hay algún dato no nulo en la fila
    else:
        excel_ordenado.at[index, 'impedancia_seca_complete'] = '1'

excel_ordenado = excel_ordenado.drop(columns=['codigo_mamavida', 'id_visita']);

for index, row in excel_ordenado.iterrows():
    row_horas = row[['hora_desayuno', 'hora_impedancia']]
    if (row.drop(labels=['record_id', 'redcap_event_name', 'redcap_repeat_instrument', 'redcap_repeat_instance', 'impedancia_seca_complete', 'hora_desayuno', 'hora_impedancia']).sum() == 0.0 and 
        (pd.isna(row['hora_desayuno']) or str(row['hora_desayuno']).strip() == '') and 
        (pd.isna(row['hora_impedancia']) or str(row['hora_impedancia']).strip() == '')):
        excel_ordenado.drop(index=index, axis=0, inplace=True)
    
# Create CSV document for Redcap
datos_impedancia_seg = "datos_impedancia_seg.csv";
excel_ordenado.to_csv(datos_impedancia_seg, index=False);

print("Archivo CSV exportado exitosamente.")

