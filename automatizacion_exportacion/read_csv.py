import csv
import chardet

'''def read_csv(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter='|')
        print(next(reader))  # Print only the first row
        print(next(reader))'''

def read_csv_comma(file_path):
    # Step 1: Detect encoding
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # Read sample for detection
        result = chardet.detect(raw_data)
        charenc = result['encoding']
        print(f"Detected encoding: {charenc}")

    # Step 2: Open with detected encoding
    with open(file_path, 'r', encoding=charenc, errors='replace') as f:
        reader = csv.reader(f)
        print(next(reader))  # Read and print first row

# Example usage
# read_csv_comma("path_to_your_file.csv")


# Example usage
file_path = r"C:\Users\USUARIO\OneDrive - Universidad Politécnica de Madrid\4_CUARTO\TFG\IMPORTACION PRUEBAS\python\automatizacion_exportacion\revision_marzo\test_app_mamavida_v2\UnidadDePatologaMama-Mamavidaui_DATA_LABELS_2025-04-04_1300.csv"

df = read_csv_comma(file_path)

# Aplicar la función a la columna 'record_id' y renombrar columnas
if 'Record ID' in df.columns:
    df = df.rename(columns={'Record ID': 'record_id'})
if 'Número de historia' in df.columns:
    nhc_mamavida_df = df.rename(columns={'Número de historia': 'num_histor'})

print(df.columns(0))

#read_csv(file_path)
#read_csv_comma(file_path)

