#Calcular el mayor de dos números ingresados por teclado usando un operador ternario
n1 = float(input("Ingrese el primer numero"))
n2 = float(input("Ingrese el segundo numero"))

num_mayor = "el numero mayor es el primero" if n1 > n2 else "el numero mayor es el segundo"

print(num_mayor)