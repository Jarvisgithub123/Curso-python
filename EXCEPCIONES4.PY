try:
    with open("archivo_inexistente.txt", "r") as archivo:
        contenido = archivo.read()
except FileNotFoundError:
    print("Error: El archivo no existe. Creándolo...")
    with open("archivo_inexistente.txt", "w") as archivo:
        archivo.write("Este archivo fue creado automáticamente.")