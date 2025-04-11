try:
    diccionario = {"nombre": "Juan", "edad": 25}
    print(diccionario["apellido"])
except KeyError:
    print("Error: La clave no existe en el diccionario.")