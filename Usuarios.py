import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
import sqlite3
from datetime import datetime, timedelta
from ttkthemes import ThemedTk
from Utilidades import validar_numeros

def crear_pestaña_usuarios(self):
    
        """Crear pestaña de gestión de usuarios"""
        self.frame_usuarios = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_usuarios, text="Usuarios")
        
        # Frame para formulario
        form_frame = ttk.LabelFrame(self.frame_usuarios, text="Datos del Usuario", padding="10")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Campos del formulario
        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.nombre_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Apellido:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.apellido_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.apellido_var, width=30).grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.email_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, pady=2, padx=5)
        
        
        ttk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.telefono_var = tk.StringVar()
        vcmd = (self.root.register(validar_numeros), '%P')
        telefono = ttk.Entry(form_frame, textvariable=self.telefono_var, width=30, validate="key", validatecommand=vcmd).grid(row=3, column=1, pady=2, padx=5)
        ttk.Label(form_frame, text="Activo:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.activo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, variable=self.activo_var).grid(row=4, column=1, sticky=tk.W, pady=2, padx=5)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Agregar", command=self.agregar_usuario, bg="#0B3954").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Modificar", command=self.modificar_usuario, bg="#25CED1").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_usuario,bg="#EB3838").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario_usuario, bg="#2E3532").pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar usuarios
        tree_frame = ttk.Frame(self.frame_usuarios)
        tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.tree_usuarios = ttk.Treeview(tree_frame, columns=('ID', 'Nombre', 'Apellido', 'Email', 'Teléfono', 'Activo'), show='headings')
        self.tree_usuarios.heading('ID', text='ID')
        self.tree_usuarios.heading('Nombre', text='Nombre')
        self.tree_usuarios.heading('Apellido', text='Apellido')
        self.tree_usuarios.heading('Email', text='Email')
        self.tree_usuarios.heading('Teléfono', text='Teléfono')
        self.tree_usuarios.heading('Activo', text='Activo')
        
        # Configurar ancho de columnas
        self.tree_usuarios.column('ID', width=50)
        self.tree_usuarios.column('Nombre', width=100)
        self.tree_usuarios.column('Apellido', width=100)
        self.tree_usuarios.column('Email', width=150)
        self.tree_usuarios.column('Teléfono', width=100)
        self.tree_usuarios.column('Activo', width=60)
        
        # Scrollbar para treeview
        scrollbar_usuarios = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_usuarios.yview)
        self.tree_usuarios.configure(yscrollcommand=scrollbar_usuarios.set)
        
        self.tree_usuarios.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_usuarios.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind para seleccionar usuario
        self.tree_usuarios.bind('<<TreeviewSelect>>', self.seleccionar_usuario)
        
        # Configurar grid
        self.frame_usuarios.columnconfigure(1, weight=1)
        self.frame_usuarios.rowconfigure(0, weight=1)
        