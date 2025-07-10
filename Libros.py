import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
import sqlite3
from datetime import datetime, timedelta
from ttkthemes import ThemedTk
def crear_pestaña_libros(self):
        """Crear pestaña de gestión de libros"""
        self.frame_libros = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_libros, text="Libros")
        
        # Frame para formulario
        form_frame = ttk.LabelFrame(self.frame_libros, text="Datos del Libro", padding="10")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Campos del formulario
        ttk.Label(form_frame, text="Título:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.titulo_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.titulo_var, width=30).grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Autor:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.autor_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.autor_var, width=30).grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="ISBN:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.isbn_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.isbn_var, width=30).grid(row=2, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Categoría:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.categoria_var = tk.StringVar()
        categorias = ['Ficción', 'No Ficción', 'Ciencia', 'Historia', 'Biografía', 'Tecnología', 'Arte', 'Otros']
        ttk.Combobox(form_frame, textvariable=self.categoria_var, values=categorias, width=27).grid(row=3, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Disponible:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.disponible_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form_frame, variable=self.disponible_var).grid(row=4, column=1, sticky=tk.W, pady=2, padx=5)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Agregar", command=self.agregar_libro , bg="#0B3954").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Modificar", command=self.modificar_libro , bg="#25CED1").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_libro ,bg="#EB3838").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario_libro, bg="#2E3532").pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar libros
        tree_frame = ttk.Frame(self.frame_libros)
        tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.tree_libros = ttk.Treeview(tree_frame, columns=('ID', 'Título', 'Autor', 'ISBN', 'Categoría', 'Disponible'), show='headings')
        self.tree_libros.heading('ID', text='ID')
        self.tree_libros.heading('Título', text='Título')
        self.tree_libros.heading('Autor', text='Autor')
        self.tree_libros.heading('ISBN', text='ISBN')
        self.tree_libros.heading('Categoría', text='Categoría')
        self.tree_libros.heading('Disponible', text='Disponible')
        
        # Configurar ancho de columnas
        self.tree_libros.column('ID', width=50)
        self.tree_libros.column('Título', width=150)
        self.tree_libros.column('Autor', width=120)
        self.tree_libros.column('ISBN', width=100)
        self.tree_libros.column('Categoría', width=100)
        self.tree_libros.column('Disponible', width=80)
        
        # Scrollbar para treeview
        scrollbar_libros = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_libros.yview)
        self.tree_libros.configure(yscrollcommand=scrollbar_libros.set)
        
        self.tree_libros.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_libros.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind para seleccionar libro
        self.tree_libros.bind('<<TreeviewSelect>>', self.seleccionar_libro)
        
        # Configurar grid
        self.frame_libros.columnconfigure(1, weight=1)
        self.frame_libros.rowconfigure(0, weight=1)