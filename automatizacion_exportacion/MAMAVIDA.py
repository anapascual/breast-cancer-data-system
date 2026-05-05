import tkinter as tk
import traceback
import pandas as pd
from tkinter import Image, filedialog, messagebox, ttk
from PIL import Image, ImageTk
import requests
import csv
import io
import os
import chardet
import ast
import re

 # Clase que incluye la ventana de ayuda e instrucciones
class NuevaVentana:
    def __init__(self, master):
        self.master = master
        self.master.title("Instrucciones MAMAVIDA")
        self.master.configure(bg='#D883A3')

        # Directorio en el que se encuentra el archivo
        directory = os.path.dirname(__file__)

        # Establecer el icono de la ventana
        self.master.iconbitmap(os.path.join(directory, "logos y archivos", "LOGO_5.ico"))

        # Crear un Canvas para poder agregar el scrollbar
        self.canvas = tk.Canvas(self.master, bg='#D883A3')
        self.scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, padding="10")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Sección 1: Fusión de reportes
        self.fusion_label = tk.Label(self.scrollable_frame, text="Instrucciones para la fusión de reportes", font=("Cibeles", 24, "bold"), fg='#E27D92')
        self.fusion_label.pack(padx=20, pady=20, anchor="center")

        self.instrucciones_fusion_label = tk.Label(self.scrollable_frame, text="En esta sección puedes insertar archivos en formato CSV generados a partir de reportes de REDCAP.\n Se deben insertar mínimo dos archivos en formato CSV para poder fusionarlos.\n No hay límite de archivos que se puedan insertar. \n El archivo resultante será un archivo en formato Excel o CSV que podrás guardar en la carpeta que desees. \n Si tu propósito es utilizar el archivo para un análisis de datos en SPSS, recomendamos elegir formato CSV. \n Si por el contrario, la intención es un visionado de los datos, es preferible usar Excel", 
                                                   bg="#E27D92", fg="black", font=("Cibeles", 14), padx=20, pady=10)
        self.instrucciones_fusion_label.pack(padx=20, pady=(5, 20), anchor="center")
    
        # Sección 2: Endocrino
        self.endocrino_label = tk.Label(self.scrollable_frame, text="Instrucciones para generar reportes de endocrinología", font=("Cibeles", 24, "bold"), fg='#E27D92')
        self.endocrino_label.pack(padx=20, pady=20, anchor="center")

        self.instrucciones_endocrino_label = tk.Label(self.scrollable_frame, text="En esta sección puedes descargar reportes (tablas de datos) desde REDCap de la parte de endocrinología del proyecto MAMAVIDA. \n Para ello, debes seleccionar el momento temporal que desees (BASAL, 6 MESES, 1 AÑO o 2 AÑOS),\n el tipo de dato que será extraído (raw (raw) o etiquetas (label)),\n el formato del documento que desees exportar (Excel o CSV) y los formularios de los que desees descargar el reporte.\n Recordar que para utilizar la función de fusionar archivos, sólo se puede utilizar formato CSV. \n Todos los campos deben estar rellenos para poder descargar el reporte. \n Podrás guardar el reporte en la carpeta que desees.", 
                                                      bg="#E27D92", fg="black", font=("Cibeles", 14), padx=20, pady=10)
        self.instrucciones_endocrino_label.pack(padx=20, pady=(5, 20), anchor="center")
        
        # Sección 3: Patología mamaria
        self.patmam_label = tk.Label(self.scrollable_frame, text="Instrucciones para generar reportes de patología mamaria", font=("Cibeles", 24, "bold"), fg='#E27D92')
        self.patmam_label.pack(padx=20, pady=20, anchor="center")

        self.instrucciones_patmam_label = tk.Label(self.scrollable_frame, text="En esta sección podrás descargar reportes (tablas de datos) de Patología Mamaria para que puedan ser combinados\n con reportes de Endocrinología del proyecto MAMAVIDA.\n Para ello, primero debes subir un archivo en formato CSV que se corresponda con un reporte de REDCap de la Ud. de Patología Mamaria,\n y seguidamente, deberás subir un archivo maestro que contenga la correspondencia\n entre número de historia clínica y código MAMAVIDA.\n De esta manera, podrás acceder a fusionar reportes de patología mamaria con reportes del REDCap MAMAVIDA.\n Se generará un archivo en formato CSV que podrás guardar en la carpeta que desees.", 
                                                   bg="#E27D92", fg="black", font=("Cibeles", 14), padx=20, pady=10)
        self.instrucciones_patmam_label.pack(padx=20, pady=(5, 20), anchor="center")
        
        # Botón para cerrar la ventana
        self.boton_cerrar = tk.Button(self.scrollable_frame, text="Cerrar Ventana", command=self.cerrar_ventana, bg="#FF6F61", fg="white", font=("Cibeles", 12), padx=10, pady=5)
        self.boton_cerrar.pack(padx=20, pady=20)
    
    def cerrar_ventana(self):
        self.master.destroy()


# Clase principal que incluye todas las funcionalidades de la aplicación
class RedCapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MAMAVIDA")
        self.root.geometry(f'{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}')  # tamaño de la ventana a pantalla completa
        #self.root.attributes('-fullscreen', True)
        root.configure(bg='#ECAAB8')

        # Directorio en el que se encuentra el archivo
        directory = os.path.dirname(__file__)

        # Establecer el icono de la aplicación
        self.root.iconbitmap(os.path.join(directory, "logos y archivos", "LOGO_5.ico"))

        # Frame para contener ambos logos
        self.logo_frame = tk.Frame(self.root, bg='#ECAAB8')
        self.logo_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 40))

        # Widget de imagen para el logo del hospital
        self.logo_hcsc_path = os.path.join(directory, "logos y archivos", "logo_ui_idiscc-removebg.png")
        self.logo_hcsc_image = Image.open(self.logo_hcsc_path)
        self.logo_hcsc_image_resized = self.logo_hcsc_image.resize((self.logo_hcsc_image.width // 2, self.logo_hcsc_image.height // 2))
        self.logo_hcsc = ImageTk.PhotoImage(self.logo_hcsc_image_resized)
        self.logo_hcsc_label = tk.Label(self.logo_frame, image=self.logo_hcsc, bg='#ECAAB8')
        self.logo_hcsc_label.pack(side=tk.RIGHT, padx=200, anchor="se")

        # Widget de imagen para el logo de la universidad
        self.logo_etsit_path = os.path.join(directory, "logos y archivos", "LOGO_ESCUELA.png")
        self.logo_etsit_image = Image.open(self.logo_etsit_path)
        self.logo_etsit_image_resized = self.logo_etsit_image.resize((self.logo_etsit_image.width // 10, self.logo_etsit_image.height // 10))
        self.logo_etsit = ImageTk.PhotoImage(self.logo_etsit_image_resized)
        self.logo_etsit_label = tk.Label(self.logo_frame, image=self.logo_etsit, bg='#ECAAB8')
        self.logo_etsit_label.pack( padx=100, anchor="sw")

        # Frame para contener el icono y el título juntos
        self.title_frame = tk.Frame(root, bg='#ECAAB8')
        self.title_frame.pack(side=tk.TOP, pady=20)

       # Icono junto al título
        self.title_icon_path = os.path.join(directory, 'logos y archivos', 'LOGO_5.png')
        self.title_icon_image = Image.open(self.title_icon_path)
        self.title_icon_image_resized = self.title_icon_image.resize((self.title_icon_image.width // 10, self.title_icon_image.height // 10))
        self.title_icon = ImageTk.PhotoImage(self.title_icon_image_resized)
        self.title_icon_label = tk.Label(self.title_frame, image=self.title_icon, bg='#ECAAB8')
        self.title_icon_label.pack(padx=10)

        # Establecer el título en la parte superior
        self.title_label = tk.Label(self.title_frame, text="MAMAVIDA: Exportación de datos", font=("Cibeles", 24, "bold"), fg='#A20D47', bg='#ECAAB8')
        self.title_label.pack(side=tk.LEFT, pady=20)

        # Botón para generar reportes
        self.report_button = tk.Button(root, text="Generar Reporte REDCap MAMAVIDA", command=self.show_report_options, bg="#A20D47", fg="white", font=("Cibeles", 14), padx=20, pady=10)
        self.report_button.pack(pady=10)

        # Botón para generar reporte de patología mamaria
        self.breast_cancer_report_button = tk.Button(root, text="Reporte REDCap Patología Mamaria", command=self.show_breast_cancer_report_screen, bg="#A20D47", fg="white", font=("Cibeles", 14), padx=20, pady=10)
        self.breast_cancer_report_button.pack(pady=10)

        # Botón para cargar archivos
        self.upload_button = tk.Button(root, text="Fusión de reportes", command=self.show_file_upload_screen, bg="#E27D92", fg="black", font=("Cibeles", 14), padx=20, pady=10)
        self.upload_button.pack(pady=10)

        # Botón para salir de la aplicación
        self.exit_button = tk.Button(root, text="Salir", command=self.root.quit, bg="#FF6F61", fg="white", font=("Cibeles", 12), padx=10, pady=5)
        self.exit_button.place(relx=1.0, rely=0, anchor='ne')  # Colocar en la esquina superior derecha
        self.exit_button.configure(height=1, width=5)  # Ajustar el tamaño

        # Botón para volver a la página anterior
        self.back_button = tk.Button(root, text="Volver", command=self.go_back, bg="#E27D92", fg="black", font=("Cibeles", 12), padx=10, pady=5)
        self.back_button.place(relx=0, rely=0, anchor='nw')  # Colocar en la esquina superior izquierda
        self.back_button.configure(height=1, width=5)  # Ajustar el tamaño

        # Botón para abrir nueva ventana de ayuda
        self.help_button = tk.Button(root, text="ayuda", command=self.open_new_window, bg="#E27D92", fg="black", font=("Cibeles", 12), padx=10, pady=5)
        self.help_button.place(x=100, y=0)
        self.help_button.configure(height=1, width=5)  # Ajustar el tamaño

        self.filepaths = []
        self.file_status_label = None
        self.load_file_button = None
        self.file_list_frame = None
        self.merge_button = None

    # Función que abre la nueva ventana (ayuda e instrucciones)
    def open_new_window(self):
        nueva_ventana = tk.Toplevel(self.root)
        nueva_ventana.geometry('1300x600') # Tamaño de la nueva ventana
        
        # Crear instancia de la nueva ventana
        ventana_secundaria = NuevaVentana(nueva_ventana)
        

    # Función que abre la pantalla de fusion de reportes
    def show_file_upload_screen(self):
        # Eliminar los widgets existentes
        self.upload_button.pack_forget()
        self.report_button.pack_forget()
        self.breast_cancer_report_button.pack_forget()
        self.logo_frame.pack_forget()

        # Crear un frame principal para el canvas y la scrollbar
        main_frame = tk.Frame(self.root, bg='#ECAAB8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # Crear un canvas dentro del frame principal
        canvas = tk.Canvas(main_frame, bg='#ECAAB8', highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=60)

        # Añadir una scrollbar vertical al canvas
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el canvas para usar la scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Crear un frame secundario dentro del canvas
        frame = tk.Frame(canvas, bg='#ECAAB8')
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Etiqueta para mostrar el estado de archivos cargados
        self.file_status_label = tk.Label(frame, text="No hay archivos cargados.", font=("Cibeles", 14), bg='#ECAAB8')
        self.file_status_label.pack(pady=10)

        # Botón para cargar archivos
        self.load_file_button = tk.Button(frame, text="Cargar Archivos", command=self.load_csv, bg="#E27D92", fg="black", font=("Cibeles", 14))
        self.load_file_button.pack(pady=10)

         # Recordatorio de formato CSV
        self.csv_reminder_label = tk.Label(frame, text="* Solo se pueden subir archivos en formato CSV.", font=("Cibeles", 12), fg="black", bg='#ECAAB8')
        self.csv_reminder_label.pack(pady=5)

        # Frame para mostrar la lista de archivos cargados
        self.file_list_frame = tk.Frame(frame, bg='#ECAAB8')
        self.file_list_frame.pack(pady=10)

        # Recordatorio de formato CSV
        self.csv_reminder_format = tk.Label(frame, text="Seleccione el formato del archivo fusionado:", font=("Cibeles", 14), fg="black", bg='#ECAAB8')
        self.csv_reminder_format.pack(pady=5, padx=10)
        
        # Combobox para seleccionar formato de archivo
        self.file_format_selection_fusion = ttk.Combobox(frame, values=["CSV", "Excel"], font=("Cibeles", 14))
        self.file_format_selection_fusion.pack(side=tk.TOP, pady=10)

         # Recordatorio preferencia formato
        self.csv_reminder_label_1 = tk.Label(frame, text="* Para el posterior uso en SPSS, conviene la fusión en formato CSV. \n Si la intención es la visualización de los datos, conviene la fusión en Excel.", font=("Cibeles", 12), fg="black", bg='#ECAAB8')
        self.csv_reminder_label_1.pack(pady=5)

        # Botón para fusionar archivos (inicialmente deshabilitado)
        self.merge_button = tk.Button(frame, text="Fusionar", command=self.merge_files, bg="#A20D47", fg="white", font=("Cibeles", 14), padx=20, pady=10, state=tk.DISABLED)
        self.merge_button.pack(side=tk.TOP, pady=10)

    # Funcion para cargar y leer el archivo
    def load_csv(self):
        # abre cuadro de diálogo para seleccionar archivo csv
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        # agregar el archivo a la lista de archivos cargados
        self.filepaths.append(file_path)
        self.update_file_list()

        # actualiza el estado del label
        self.file_status_label.config(text=f"{len(self.filepaths)} archivo(s) cargado(s)")
        

    # Funcion para actualizar la lista de archivos subidos
    def update_file_list(self):
        for widget in self.file_list_frame.winfo_children():
            widget.destroy()

        for idx, path in enumerate(self.filepaths):
            file_frame = tk.Frame(self.file_list_frame, bg='#ECAAB8')
            file_frame.pack(fill='x', pady=2)

            file_label = tk.Label(file_frame, text=os.path.basename(path), font=("Cibeles", 12), bg='#ECAAB8')
            file_label.pack(side='left', padx=5)

            remove_button = tk.Button(file_frame, text="Eliminar", command=lambda idx=idx: self.remove_file(idx), font=("Cibeles", 12))
            remove_button.pack(side='right', padx=5)

        if len(self.filepaths) >= 2:
            self.merge_button.config(state=tk.NORMAL)
        else:
            self.merge_button.config(state=tk.DISABLED)

    # Funcion para eliminar archivos de la lista
    def remove_file(self, idx):
        del self.filepaths[idx]
        self.update_file_list()
        self.file_status_label.config(text=f"{len(self.filepaths)} archivo(s) cargado(s): {', '.join([os.path.basename(path) for path in self.filepaths])}")

    # Funcion para fusionar los archivos cargados
    def merge_files(self):
        # Coge el formato seleccionado
        file_format = self.file_format_selection_fusion.get()
        # Comprueba que haya al menos dos archivos subidos
        if len(self.filepaths) < 2:
            messagebox.showerror("Error", "Debe cargar al menos dos archivos para fusionar.")
            return

        # Lee los archivos cargados y detecta su codificacion con chardet
        try:
            # Crea una lista vacia de dataframes a los que iremos añadiendo los archivos subidos
            dfs = []
            for file_path in self.filepaths:
                with open(file_path, 'rb') as f:
                    result = chardet.detect(f.read())
                charenc = result['encoding']

                # Lee los archivos cargados
                df = pd.read_csv(file_path, encoding=charenc, delimiter='|')

                # Renombrar la columna específica a 'record_id'
                for col in df.columns:
                    if 'record_id' in col:
                        df.rename(columns={col: 'record_id'}, inplace=True)
                        break
                    elif 'Record ID' in col:
                        df.rename(columns={col: 'record_id'}, inplace=True)
                        break

                # Añade el data frame a la lista creada anteriormente
                dfs.append(df)

            # Fusionar todos los DataFrames por la columna 'record_id' usando merge
            merged_df = dfs[0]

            '''# DEBUG: Verificar columnas antes del merge
            for i, d in enumerate(dfs):
                print(f"Archivo {i+1} columnas:", d.columns.tolist())'''

            # Itera sobre los DataFrames en la lista para comprobar los nombres de las columnas
            for df in dfs[1:]:
                # Comprueba si el DataFrame tiene la columna 'record_id'
                if 'record_id' in df.columns:
                    merged_df = merged_df.merge(df, on='record_id', how='outer')
                # Si no tiene la columna 'record_id', comprueba si tiene 'Record ID'
                elif 'Record ID' in df.columns:
                    merged_df = merged_df.merge(df, on='Record ID', how='outer')

            # Guarda el DataFrame en el formato seleccionado
            if file_format == 'CSV':
                merged_df = merged_df.to_csv(filedialog.asksaveasfilename(defaultextension=".csv",
                                                              filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]), index=False, sep='|')
                # Mensajes de confirmacion
                messagebox.showinfo("Fusión Completa", "Archivos fusionados correctamente y guardados.")
                
            elif file_format == 'Excel':
                merged_df = merged_df.to_excel(filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                               filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]), index=False)
                # Mensajes de confirmacion
                messagebox.showinfo("Fusión Completa", "Archivos fusionados correctamente y guardados.")

        # Mensaje de error
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al fusionar los archivos: {str(e)}")
            

    # Función que enseña la pantalla con las opciones para generar reporte del REDCap MAMAVIDA
    def show_report_options(self):
        # Eliminar los widgets existentes
        self.upload_button.pack_forget()
        self.report_button.pack_forget()
        self.breast_cancer_report_button.pack_forget()
        self.title_frame.pack_forget()
        self.logo_frame.pack_forget()

        # Crear un frame principal para el canvas y la scrollbar
        main_frame = tk.Frame(self.root, bg='#ECAAB8')
        main_frame.pack(fill=tk.BOTH, expand=True, pady=60, padx=10)

        # Crear un canvas dentro del frame principal
        canvas = tk.Canvas(main_frame, bg='#ECAAB8', highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Añadir una scrollbar vertical al canvas
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el canvas para usar la scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Crear un frame secundario dentro del canvas
        frame = tk.Frame(canvas, bg='#ECAAB8')
        canvas.create_window((0, 0), window=frame, anchor="nw")

        # Subframe horizontal para las opciones de selección
        selection_frame = tk.Frame(frame, bg='#ECAAB8')
        selection_frame.pack(side=tk.TOP, padx=10, pady=20)

        # Etiqueta y Combobox para seleccionar momento temporal
        tk.Label(selection_frame, text="Seleccione el momento temporal:", font=("Cibeles", 14), bg='#ECAAB8').pack(side=tk.LEFT, padx=10, pady=10)
        self.time_selection = ttk.Combobox(selection_frame, values=["BASAL", "6 MESES", "1 AÑO", "2 AÑOS", "3 AÑOS", "4 AÑOS", "5 AÑOS", "Datos Generales"], font=("Cibeles", 14))
        self.time_selection.pack(side=tk.LEFT, padx=10, pady=10)

        # Recordatorio de formato CSV
        self.csv_reminder_generales = tk.Label(frame, text="* Si selecciona Datos Generales, no debe\n seleccionar ningún formulario en la parte de abajo.", font=("Cibeles", 12), fg="black", bg='#ECAAB8')
        self.csv_reminder_generales.pack(anchor="w", pady=5, padx=10)

        # Etiqueta y Combobox para seleccionar tipo de dato
        tk.Label(selection_frame, text="Seleccione el tipo de dato:", font=("Cibeles", 14), bg='#ECAAB8').pack(side=tk.LEFT, padx=10, pady=10)
        self.data_type_selection = ttk.Combobox(selection_frame, values=["raw", "label"], font=("Cibeles", 14))
        self.data_type_selection.pack(side=tk.LEFT, padx=10, pady=10)

        # Recordatorio de cómo es el tipo de dato
        self.reminder_data_type = tk.Label(frame, text="*Raw = Dato bruto || Label = Etiqueta.", font=("Cibeles", 12), fg="black", bg='#ECAAB8')
        self.reminder_data_type.pack(anchor="e", pady=5, padx=10)

        # Subframe para la selección del formato del archivo
        format_frame = tk.Frame(frame, bg='#ECAAB8')
        format_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Etiqueta y Combobox para seleccionar formato de archivo
        tk.Label(format_frame, text="Seleccione el formato del archivo:", font=("Cibeles", 14), bg='#ECAAB8').pack(side=tk.LEFT, padx=10, pady=10)
        self.file_format_selection = ttk.Combobox(format_frame, values=["CSV", "Excel"], font=("Cibeles", 14))
        self.file_format_selection.pack(side=tk.LEFT, padx=10, pady=10)

        # Recordatorio de formato CSV
        self.csv_reminder_label = tk.Label(frame, text="* Al utilizar la funcionalidad de fusión de reportes, solo se pueden cargar archivos en formato CSV.", font=("Cibeles", 12), fg="black", bg='#ECAAB8')
        self.csv_reminder_label.pack(pady=5, padx=10)

        # Etiqueta para seleccionar formularios
        tk.Label(frame, text="Seleccione los formularios:", font=("Cibeles", 14), bg='#ECAAB8').pack(pady=10, padx=20)

        # Frame para el Listbox y Scrollbar
        listbox_frame = tk.Frame(frame, bg='#ECAAB8')
        listbox_frame.pack(pady=10, padx=20)

        # List box para seleccionar los formularios que se quieran exportar
        self.form_selection = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, font=("Cibeles", 14), width=30, height=8, bd=2, relief='sunken')
        listbox_scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.form_selection.yview)
        self.form_selection.config(yscrollcommand=listbox_scrollbar.set)

        #Configuracion del Listbox
        self.form_selection.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=20)

        # Lista con los nombres de los formularios, se insertan en el listbox
        forms = ["Datos de la visita", "Datos antropométricos", "Test SPPB", "MEDAS-14", "IPAQ", "Datos de la impedancia", "Datos de la ecografia", "Datos de la analitica", "R.24h", "Datos demograficos", "Datos oncologicos-1", "Datos oncologicos-2", "BIPQ", "BIS", "EORTC QLQ-C30", "EORTC QLQ-BR23", "HADS", "Evaluacion continuidad en el estudio"]
        for form in forms:
            self.form_selection.insert(tk.END, form)

        # Botón para generar el reporte
        generate_button = tk.Button(frame, text="Generar", command=self.generate_report, bg="#A20D47", fg="white", font=("Cibeles", 14), padx=20, pady=10)
        generate_button.pack(pady=20, padx=20)


    #Función que lleva de vuelta a la pantalla principal de la aplicacion
    def go_back(self):
        # Eliminar los widgets de la página de selección de opciones
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Restaurar los widgets de la página inicial
        self.title_frame.pack(side=tk.TOP, pady=20)
        self.report_button.pack(pady=10)
        self.breast_cancer_report_button.pack(pady=10)
        self.upload_button.pack(pady=10)
        self.exit_button.place(relx=1.0, rely=0, anchor='ne')
        self.exit_button.configure(height=1, width=5)
        self.help_button.place(x=100, y=0)
        self.help_button.configure(height=1, width=5)

        # Restaurar los logos
        self.logo_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 40))

        # Configurar la imagen del logo del hospital
        self.logo_hcsc_label.configure(image=self.logo_hcsc)
        self.logo_hcsc_label.image = self.logo_hcsc  # Mantener una referencia al objeto PhotoImage

        # Configurar la imagen del logo de la universidad
        self.logo_etsit_label.configure(image=self.logo_etsit)
        self.logo_etsit_label.image = self.logo_etsit  # Mantener una referencia al objeto PhotoImage


    #Funcion que genera el reporte de endocrinologia
    def generate_report(self):
        # Conseguir las variables necesarias (formularios seleccionados, tipo de dato, formato deseado, y momento temporal)
        selected_time = self.time_selection.get()
        selected_forms = [self.form_selection.get(i) for i in self.form_selection.curselection()]
        selected_data_type = self.data_type_selection.get()
        selected_file_format = self.file_format_selection.get()

        # Seleccionar el report_id basado en el momento temporal, y añadir el sufijo dependiendo del momento temporal seleccionado
        if selected_time == "BASAL":
            report_id = '1155'
            suffix = "_basal"
        elif selected_time == "6 MESES":
            report_id = '1156'
            suffix = "_6meses"
        elif selected_time == "1 AÑO":
            report_id = '1157'
            suffix = "_1ano"
        elif selected_time == "2 AÑOS":
            report_id = '1158'
            suffix = "_2anos"
        elif selected_time == "3 AÑOS":
            report_id = '1159'
            suffix = "_3anos"
        elif selected_time == "4 AÑOS":
            report_id = '1160'
            suffix = "_4anos"
        elif selected_time == "5 AÑOS":
            report_id = '1161'
            suffix = "_5anos"
        elif selected_time == "Datos Generales":
            report_id = '1162'
        else:
            messagebox.showerror("Error", "Debe seleccionar un momento temporal.")
            return
        
        # Verificar si se ha seleccionado al menos un formulario
        if selected_time != "Datos Generales" and not selected_forms:
            messagebox.showerror("Error", "Debe seleccionar al menos un formulario.")
            return
        
        # Verificar si se ha seleccionado el tipo de dato
        if not selected_data_type:
            messagebox.showerror("Error", "Debe seleccionar el tipo de dato.")
            return
        
        # Verificar si se ha seleccionado el formato de archivo
        if not selected_file_format:
            messagebox.showerror("Error", "Debe seleccionar el formato del archivo.")
            return

        #Codigo proporcionado por el API playground de REDCap que permite exportar el reporte del servidor web
        data = {
            'token': '20490714C6ECE27AF700C5D5FBC3C9C1',
            'content': 'report',
            'format': 'csv',
            'report_id': report_id,
            'csvDelimiter': '',
            'rawOrLabel': selected_data_type,
            'rawOrLabelHeaders': selected_data_type,
            'exportCheckboxLabel': 'false',
            'returnFormat': 'json'
                }
        r = requests.post('http://redcap.idissc.org/redcap/api/',data=data)

        if r.status_code == 200:
            # Procesar el reporte CSV
            csv_content = r.text
            csv_reader = csv.reader(io.StringIO(csv_content))
            rows = list(csv_reader)

            if selected_time == "Datos Generales":

                # Leer el CSV con pandas
                df = pd.read_csv(io.StringIO(csv_content))

                # Eliminar las columnas si se selecciona "Datos Generales"
                if selected_time == "Datos Generales":
                    if 'record_id' in df.columns:
                        df = df.drop(columns=["redcap_repeat_instrument", "redcap_repeat_instance", "redcap_event_name"], errors='ignore')
                    if 'Record ID' in df.columns:
                        df = df.drop(columns=["Repeat Instrument", "Repeat Instance", "Event Name"], errors='ignore')

                # Guardar el reporte como un archivo CSV o Excel
                if selected_file_format == "CSV":
                    report_filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
                    if report_filename:
                        df.to_csv(report_filename, index=False, encoding='utf-8', sep='|')
                        messagebox.showinfo("Reporte Generado", f"Reporte guardado con éxito en: {report_filename}")
                elif selected_file_format == "Excel":
                    report_filename = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
                    if report_filename:
                        df.to_excel(report_filename, index=False)
                        messagebox.showinfo("Reporte Generado", f"Reporte guardado con éxito en: {report_filename}")

            else:
                # Filtrar las columnas basadas en los formularios seleccionados (funcion filter_columns mas abajo)
                filtered_rows = self.filter_columns(rows, selected_forms, selected_data_type)

                # Añadir el sufijo a los nombres de las columnas (indicado mas arriba según el momento temporal seleccionado)
                if filtered_rows:
                    header = filtered_rows[0]
                    modified_header = [col + suffix for col in header]
                    filtered_rows[0] = modified_header  

                # Guardar el reporte como un archivo CSV o Excel
                if selected_file_format == "CSV":
                    report_filename = filedialog.asksaveasfilename(defaultextension=".csv",
                                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
                    if report_filename:
                        with open(report_filename, 'w', newline='', encoding='utf-8') as csvfile:
                            csv_writer = csv.writer(csvfile, delimiter='|')
                            for row in filtered_rows:
                                csv_writer.writerow([str(cell).encode('utf-8').decode('utf-8') for cell in row])
                        messagebox.showinfo("Reporte Generado", f"Reporte guardado con éxito en: {report_filename}")
                elif selected_file_format == "Excel":
                    report_filename = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
                    if report_filename:
                        df = pd.DataFrame(filtered_rows[1:], columns=filtered_rows[0])
                        df.to_excel(report_filename, index=False)
                        messagebox.showinfo("Reporte Generado", f"Reporte guardado con éxito en: {report_filename}")
                else:
                    messagebox.showerror("Error", f"Error al generar el reporte: {r.status_code}")


    # Funcion que filtra las columnas segun los formularios seleccionados
    def filter_columns(self, rows, selected_forms, selected_data_type):
        # Definir el nombre del archivo .txt donde está la estructura de datos
        directory_forms = os.path.dirname(__file__)
        file_path_raw = os.path.join(directory_forms, 'logos y archivos' ,'dict_form_raw.txt')
        file_path_label = os.path.join(directory_forms,'logos y archivos', 'dict_form_label.txt')

        # Función para cargar los diccionarios desde los archivos .txt
        def load_dicts_from_files(raw_file, label_file):
            form_columns_raw = {}
            form_columns_label = {}

            with open(raw_file, 'r', encoding='utf-8') as file:
                for line in file:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().strip('"')  # Elimina espacios en blanco y comillas del principio y final
                        value = value.strip().strip('[],').replace('"', '').split(', ')  # Limpia y convierte a lista
                        form_columns_raw[key] = value

            with open(label_file, 'r', encoding='utf-8') as file:
                for line in file:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip().strip('"')  # Elimina espacios en blanco y comillas del principio y final
                        value = value.strip().strip('[],').replace('"', '').split(', ')  # Limpia y convierte a lista
                        form_columns_label[key] = value

            return form_columns_raw, form_columns_label

        # Cargar los diccionarios desde los archivos
        form_columns_raw, form_columns_label = load_dicts_from_files(file_path_raw, file_path_label)

        # Dependiendo de si se ha seleccionado raw o label, los nombres de las variables seran distintos, aqui distinguimos si tenemos "record_id" o "Record ID"
        if selected_data_type == 'raw':
            selected_columns = ["record_id"]
            for form in selected_forms:
                selected_columns.extend(form_columns_raw.get(form, []))
        else:
            selected_columns = ["Record ID"]
            for form in selected_forms:
                selected_columns.extend(form_columns_label.get(form, []))

        if len(selected_columns) == 1:
            messagebox.showerror("Error", "Debe seleccionar al menos un formulario.")
            return None

        # Filtrar las columnas basadas en los formularios seleccionados
        header = rows[0]
        selected_indices = [header.index(col) for col in selected_columns if col in header]

        filtered_rows = [[row[i] for i in selected_indices] for row in rows]

        return filtered_rows
    
     # Funcion que enseña la pantalla de la funcionalidad para reportes de Patologia Mamaria
    def show_breast_cancer_report_screen(self):
        # Eliminar los widgets existentes
        self.upload_button.pack_forget()
        self.report_button.pack_forget()
        self.breast_cancer_report_button.pack_forget()

        # Añadir una etiqueta con instrucciones
        instrucciones = tk.Label(self.root, text="Primero selecciona el archivo CSV con los datos.\nLuego selecciona el archivo Excel con la correspondencia entre NHC y código MAMAVIDA.", font=("Cibeles", 12), fg="black", bg='#ECAAB8')
        instrucciones.pack(pady=10)

        # Botón para cargar archivo CSV
        self.load_csv_button = tk.Button(self.root, text="Cargar Archivo CSV - Reporte Ud. Patologia Mamaria", command=self.load_csv_file, bg="#E27D92", fg="black", font=("Cibeles", 14), padx=20, pady=10)
        self.load_csv_button.pack(pady=10)

        # Botón para cargar archivo Excel
        self.load_excel_button = tk.Button(self.root, text="Cargar Archivo Excel - Archivo Maestro correspondencia NHC-Codigo MAMAVIDA", command=self.load_excel_file, bg="#E27D92", fg="black", font=("Cibeles", 14), padx=20, pady=10)
        self.load_excel_button.pack(pady=10)

        # Botón para generar el reporte
        self.generate_report_button = tk.Button(self.root, text="Generar Documento", command=self.generate_report_pat_mam, bg="#A20D47", fg="white", font=("Cibeles", 14), padx=20, pady=10)
        self.generate_report_button.pack(pady=10)

        self.csv_feedback_label = tk.Label(self.root, text="", font=("Cibeles", 12), fg="green", bg='#ECAAB8')
        self.csv_feedback_label.pack(pady=(0, 10))

        self.excel_feedback_label = tk.Label(self.root, text="", font=("Cibeles", 12), fg="green", bg='#ECAAB8')
        self.excel_feedback_label.pack(pady=(0, 10))


    # Funcion para cargar un archivo csv con el reporte de patologia mamaria
    def load_csv_file(self):
        self.csv_file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not self.csv_file_path:
            messagebox.showerror("Error", "No se seleccionó ningún archivo CSV.")

        if self.csv_file_path:
            filename = os.path.basename(self.csv_file_path)
            self.csv_feedback_label.config(text=f"✅ CSV cargado: {filename}")

    # Funcion para cargar un archivo excel que contenga la correspondencia entre NHC y codigo MAMAVIDA (archivo maestro)
    def load_excel_file(self):
        self.excel_file_path = filedialog.askopenfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not self.excel_file_path:
            messagebox.showerror("Error", "No se seleccionó ningún archivo Excel.")

        if self.excel_file_path:
            filename = os.path.basename(self.excel_file_path)
            self.excel_feedback_label.config(text=f"✅ Excel cargado: {filename}")


    # Funcion que genera el reporte de patologia mamaria sustituyendo NHC por codigo MAMAVIDA
    def generate_report_pat_mam(self):
        # Errores para comprobar que se han subido los archivos correctamente
        if not self.csv_file_path:
            messagebox.showerror("Error", "Debe seleccionar un archivo CSV.")
            return

        if not self.excel_file_path:
            messagebox.showerror("Error", "Debe seleccionar un archivo Excel.")
            return

        try:
            # Lee el excel subido con la correspondencia entre NHC y codigo MAMAVIDA
            nhc_mamavida_df = pd.read_excel(self.excel_file_path)

            # Verificar que contiene la columna necesaria (NHC y record_id) ya sea en raw o label
            if not ('num_histor' in nhc_mamavida_df.columns or 'Número de historia' in nhc_mamavida_df.columns or 'record_id' in nhc_mamavida_df.columns or 'Record ID' in nhc_mamavida_df.columns):
                messagebox.showerror("Error", "El archivo cargado debe contener la columna correspondiente al número de historia clínica. (Problema en el archivo maestro).")
                return

            # Leer el archivo CSV subido y utiliza chardet para detectar la codificacion de dicho archivo y evitar errores de lectura
            with open(self.csv_file_path, 'rb') as f:
                result = chardet.detect(f.read())
                charenc = result['encoding']
            df = pd.read_csv(self.csv_file_path, delimiter='|', encoding=charenc)

            # Verificar que contiene la columna necesaria (NHC)
            if not ('num_histor' in df.columns or 'Número de historia' in df.columns):
                messagebox.showerror("Error", "El archivo cargado debe contener la columna correspondiente al número de historia clínica. (Problema en el reporte de patología mamaria)")
                return

            def extraer_numero(codigo):
                if isinstance(codigo, str):
                    # Separar usando guión o guión bajo como delimitadores
                    partes = re.split(r'[-_]', codigo)
                    try:
                        return int(partes[-1])
                    except ValueError:
                        return float('inf')
                return float('inf')

            # Aplicar la función a la columna 'record_id' y renombrar columnas
            # Renombrar columnas si tienen nombres con etiquetas
            if 'Número de historia' in nhc_mamavida_df.columns:
                nhc_mamavida_df = nhc_mamavida_df.rename(columns={'Número de historia': 'num_histor'})
            if 'Número de historia' in df.columns:
                df = df.rename(columns={'Número de historia': 'num_histor'})

            # Verificar que ambos ahora sí tienen 'num_histor'
            if 'num_histor' not in nhc_mamavida_df.columns:
                raise ValueError("Falta la columna 'num_histor' en el archivo maestro.")
            if 'num_histor' not in df.columns:
                raise ValueError("Falta la columna 'num_histor' en el archivo CSV.")

            if 'record_id' in df.columns:
                df['record_id'] = df['record_id'].apply(extraer_numero)
            if 'record_id' in nhc_mamavida_df.columns:
                nhc_mamavida_df['record_id'] = nhc_mamavida_df['record_id'].apply(extraer_numero)

            # DEBUG: Ver columnas disponibles antes de hacer el merge
            #print("Columnas en df:", df.columns.tolist())
            #print("Columnas en nhc_mamavida_df:", nhc_mamavida_df.columns.tolist())

            # DEBUG opcional: muestra algunas filas si lo necesitas
            # print("df preview:\n", df.head())
            # print("nhc_mamavida_df preview:\n", nhc_mamavida_df.head())

            # Verificar que ambas tablas tienen la columna 'num_histor'
            if 'num_histor' not in df.columns:
                raise ValueError("La columna 'num_histor' no existe en el dataframe CSV.")
            if 'num_histor' not in nhc_mamavida_df.columns:
                raise ValueError("La columna 'num_histor' no existe en el dataframe del archivo maestro.")

            # Fusionamos el archivo maestro con el archivo cargado por numero de historia clinica
            merged_df = df.merge(nhc_mamavida_df, on='num_histor', how='left')

            # Eliminar la columna de nhc del df y nos quedamos solo con record_id
            merged_df = merged_df.drop(columns=['num_histor'])

            # Eliminamos una de las columnas de record_id
            merged_df.insert(0, 'record_id_1', merged_df['record_id'])
            merged_df = merged_df.drop(columns=['record_id'])
            merged_df = merged_df.rename(columns={'record_id_1': 'record_id'})

            # Group by 'record_id' and take the first non-null value for each column
            merged_df = merged_df.groupby('record_id').agg(lambda x: x.dropna().iloc[0] if not x.dropna().empty else None).reset_index()

            # Guardar el archivo resultante
            save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if save_path:
                merged_df.to_csv(save_path, index=False, sep='|')
                messagebox.showinfo("Éxito", f"Archivo guardado en {save_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar los archivos: {str(e)}")
            print("TRACEBACK:\n", traceback.format_exc())  # para debugging en consola
            messagebox.showerror("Error", f"Error al procesar los archivos: {str(e)}")

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)  # Sin bordes ni botones
        self.root.configure(bg="#ECAAB8")

        width = 400
        height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        label = tk.Label(self.root, text="Cargando MAMAVIDA...", font=("Cibeles", 18, "bold"), bg="#ECAAB8", fg="#A20D47")
        label.pack(expand=True)

        self.root.after(2500, self.close_splash)  # Espera 2.5 segundos antes de cerrar

    def close_splash(self):
        self.root.destroy()
        main_root = tk.Tk()
        app = RedCapApp(main_root)
        main_root.mainloop()


if __name__ == "__main__":
    splash_root = tk.Tk()
    splash = SplashScreen(splash_root)
    splash_root.mainloop()



