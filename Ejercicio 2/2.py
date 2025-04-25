#Buscar una palabra en una lista ingresada por teclado usando args y un operador  ternario   
def buscar_palabra(palabra_buscada, *lista_palabras):
    return f"'{palabra_buscada}' encontrada" if palabra_buscada in lista_palabras else f"'{palabra_buscada}' no encontrada"


ingreso_palabras = input("Ingresa palabras separadas por espacios:")
palabras = ingreso_palabras.split()


palabra = input("¿Qué palabra quieres buscar?")

resultado = buscar_palabra(palabra, *palabras)
print(resultado)