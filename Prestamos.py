import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
import sqlite3
from datetime import datetime, timedelta
from ttkthemes import ThemedTk
def crear_pestaña_prestamos(self):
        """Crear pestaña de gestión de préstamos"""
        self.frame_prestamos = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_prestamos, text="Préstamos")
        
        # Frame para formulario
        form_frame = ttk.LabelFrame(self.frame_prestamos, text="Datos del Préstamo", padding="10")
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Campos del formulario
        ttk.Label(form_frame, text="Usuario:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.usuario_prestamo_var = tk.StringVar()
        self.combo_usuarios = ttk.Combobox(form_frame, textvariable=self.usuario_prestamo_var, 
                                          width=27, state="readonly")
        self.combo_usuarios.grid(row=0, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Libro:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.libro_prestamo_var = tk.StringVar()
        self.combo_libros = ttk.Combobox(form_frame, textvariable=self.libro_prestamo_var, 
                                        width=27, state="readonly")
        self.combo_libros.grid(row=1, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Fecha Préstamo:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.fecha_prestamo_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(form_frame, textvariable=self.fecha_prestamo_var, width=30).grid(row=2, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Fecha Devolución:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.fecha_devolucion_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.fecha_devolucion_var, width=30).grid(row=3, column=1, pady=2, padx=5)
        
        ttk.Label(form_frame, text="Estado:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.estado_var = tk.StringVar(value="activo")
        estados = ['activo', 'devuelto', 'vencido']
        ttk.Combobox(form_frame, textvariable=self.estado_var, values=estados, width=27).grid(row=4, column=1, pady=2, padx=5)
        
        # Botones
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="Agregar", command=self.agregar_prestamo, bg="#0B3954").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Modificar", command=self.modificar_prestamo , bg="#25CED1").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_prestamo,bg="#EB3838").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario_prestamo, bg="#2E3532").pack(side=tk.LEFT, padx=5)
        
        # Treeview para mostrar préstamos
        tree_frame = ttk.Frame(self.frame_prestamos)
        tree_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.tree_prestamos = ttk.Treeview(tree_frame, 
                                          columns=('ID', 'Usuario', 'Libro', 'F.Préstamo', 'F.Devolución', 'Estado'), 
                                          show='headings')
        self.tree_prestamos.heading('ID', text='ID')
        self.tree_prestamos.heading('Usuario', text='Usuario')
        self.tree_prestamos.heading('Libro', text='Libro')
        self.tree_prestamos.heading('F.Préstamo', text='F.Préstamo')
        self.tree_prestamos.heading('F.Devolución', text='F.Devolución')
        self.tree_prestamos.heading('Estado', text='Estado')
        
        # Configurar ancho de columnas
        self.tree_prestamos.column('ID', width=50)
        self.tree_prestamos.column('Usuario', width=120)
        self.tree_prestamos.column('Libro', width=150)
        self.tree_prestamos.column('F.Préstamo', width=100)
        self.tree_prestamos.column('F.Devolución', width=100)
        self.tree_prestamos.column('Estado', width=80)
        
        # Scrollbar para treeview
        scrollbar_prestamos = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_prestamos.yview)
        self.tree_prestamos.configure(yscrollcommand=scrollbar_prestamos.set)
        
        self.tree_prestamos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_prestamos.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind para seleccionar préstamo
        self.tree_prestamos.bind('<<TreeviewSelect>>', self.seleccionar_prestamo)
        
        # Configurar grid
        self.frame_prestamos.columnconfigure(1, weight=1)
        self.frame_prestamos.rowconfigure(0, weight=1)