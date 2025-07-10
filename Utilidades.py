from tkinter import messagebox
import tkinter as tk

# Permite unicamente numeros en un entry
def validar_numeros(P):
    if P == "" or all(c.isdigit() for c in P):
        return True
    else:
        messagebox.showerror("Error", "Solo se permiten números")
        return False