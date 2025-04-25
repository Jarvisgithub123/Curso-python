#Calcular el promedio de una lista de números usando args y un operador ternario                                                                           
#Imprimir un mensaje de error si no se pasan suficientes argumentos
def calcular_promedio (*Numeros):
    return sum(Numeros) / len(Numeros) if len(Numeros) >= 1 else "Ingrese al menos 1 numero"

try:
    numeros_ingresados= input("Ingresa numeros separados por espacios")

    lista_numeros = [float(n) for n in numeros_ingresados.split()]

    resultado = calcular_promedio(*lista_numeros)
    print(f"El promedio es {resultado}")
except:
    print("Ingrese numeros validos")