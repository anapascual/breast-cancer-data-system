from PIL import Image

# Ruta de tu archivo de imagen
img_path = r"C:\Users\USUARIO\Downloads\LOGO_5.jpeg"
ico_path = r"C:\Users\USUARIO\Escritorio"

# Convertir la imagen a formato .ico
img = Image.open(img_path)
img.save(ico_path, format='ICO')
