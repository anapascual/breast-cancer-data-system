from cx_Freeze import setup, Executable

# Configuración del ejecutable
executables = [Executable("MAMAVIDA.py", base="Win32GUI")]

# Configuración del setup
setup(
    name="MAMAVIDA",
    version="0.1",
    description="Descarga y fusión de reportes desde REDCap para el proyecto MAMAVIDA",
    executables=executables
)
