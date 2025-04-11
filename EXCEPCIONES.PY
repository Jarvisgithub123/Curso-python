try:
    n1 = float(input("Ingrese el primer número de la division: "))
    n2 = float(input("Ingrese el segundo número de la division: "))
    
 
    resultado = n1 / n2
    
    print(f"El resultado de la división es: {resultado}")
    
except ZeroDivisionError:
   
    print("Error: No se puede dividir por cero.")

  
 


