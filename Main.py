import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
import sqlite3
from datetime import datetime, timedelta
from ttkthemes import ThemedTk
from Libros import crear_pestaña_libros
from Usuarios import crear_pestaña_usuarios
from Prestamos import crear_pestaña_prestamos
class BibliotecaApp:
    def __init__(self):
        # Configuración de la ventana principal
        self.root = ThemedTk(theme="arc")
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Fuentes personalizadas
        self.font_title = font.Font(family="Arial", size=16, weight="bold")
        self.font_label = font.Font(family="Arial", size=10)
        
        # Crear base de datos
        self.crear_base_datos()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar datos iniciales
        self.cargar_datos()
    
    def crear_base_datos(self):
        """Crear las tablas de la base de datos"""
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        # Tabla usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                telefono TEXT,
                activo BOOLEAN DEFAULT 1,
                fecha_registro DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Tabla libros
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                isbn TEXT UNIQUE,
                categoria TEXT NOT NULL,
                disponible BOOLEAN DEFAULT 1,
                fecha_adquisicion DATE DEFAULT CURRENT_DATE
            )
        ''')
        
        # Tabla préstamos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                libro_id INTEGER NOT NULL,
                fecha_prestamo DATE NOT NULL,
                fecha_devolucion DATE,
                estado TEXT DEFAULT 'activo',
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
                FOREIGN KEY (libro_id) REFERENCES libros (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def crear_interfaz(self):
        """Crear la interfaz gráfica principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título de la ventana
        titulo = ttk.Label(main_frame, text="Sistema de Gestión de Biblioteca", font=self.font_title)
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear pestañas 
        crear_pestaña_usuarios(self)
        crear_pestaña_libros(self) 
        crear_pestaña_prestamos(self)
        
        # Frame para botones principales
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        tk.Button(button_frame, text="Actualizar Datos", 
                  command=self.cargar_datos, bg="#636564").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Salir", 
                  command=self.root.quit, bg="#A1A499").pack(side=tk.LEFT, padx=5)
    
    
    
    
    
    
    # Métodos para gestiónar los usuarios
    def agregar_usuario(self):
        if not self.validar_usuario():
            return
        
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO usuarios (nombre, apellido, email, telefono, activo)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.nombre_var.get(), self.apellido_var.get(), 
                  self.email_var.get(), self.telefono_var.get(), 
                  self.activo_var.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
            self.limpiar_formulario_usuario()
            self.cargar_usuarios()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El email ya existe")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar usuario: {str(e)}")
        finally:
            conn.close()
    
    def modificar_usuario(self):
        if not self.tree_usuarios.selection():
            messagebox.showwarning("Advertencia", "Seleccione un usuario para modificar")
            return
        
        if not self.validar_usuario():
            return
        
        item = self.tree_usuarios.selection()[0]
        usuario_id = self.tree_usuarios.item(item)['values'][0]
        
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE usuarios 
                SET nombre=?, apellido=?, email=?, telefono=?, activo=?
                WHERE id=?
            ''', (self.nombre_var.get(), self.apellido_var.get(), 
                  self.email_var.get(), self.telefono_var.get(), 
                  self.activo_var.get(), usuario_id))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario modificado correctamente")
            self.limpiar_formulario_usuario()
            self.cargar_usuarios()
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar usuario: {str(e)}")
        finally:
            conn.close()
    
    def eliminar_usuario(self):
        if not self.tree_usuarios.selection():
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este usuario?"):
            item = self.tree_usuarios.selection()[0]
            usuario_id = self.tree_usuarios.item(item)['values'][0]
            
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute('DELETE FROM usuarios WHERE id=?', (usuario_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                self.limpiar_formulario_usuario()
                self.cargar_usuarios()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar usuario: {str(e)}")
            finally:
                conn.close()
    
    def validar_usuario(self):
        if not self.nombre_var.get().strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return False
        if not self.apellido_var.get().strip():
            messagebox.showerror("Error", "El apellido es obligatorio")
            return False
        if not self.email_var.get().strip():
            messagebox.showerror("Error", "El email es obligatorio")
            return False
        return True
    
    def limpiar_formulario_usuario(self):
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.email_var.set("")
        self.telefono_var.set("")
        self.activo_var.set(True)
    
    def seleccionar_usuario(self, event):
        if self.tree_usuarios.selection():
            item = self.tree_usuarios.selection()[0]
            values = self.tree_usuarios.item(item)['values']
            
            self.nombre_var.set(values[1])
            self.apellido_var.set(values[2])
            self.email_var.set(values[3])
            self.telefono_var.set(values[4])
            self.activo_var.set(values[5] == 'Sí')
    
    # Métodos para gestión de libros
    def agregar_libro(self):

        if not self.validar_libro():
            return
        
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO libros (titulo, autor, isbn, categoria, disponible)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.titulo_var.get(), self.autor_var.get(), 
                  self.isbn_var.get(), self.categoria_var.get(), 
                  self.disponible_var.get()))
            conn.commit()
            messagebox.showinfo("Éxito", "Libro agregado correctamente")
            self.limpiar_formulario_libro()
            self.cargar_libros()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El ISBN ya existe")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar libro: {str(e)}")
        finally:
            conn.close()
    
    def modificar_libro(self):
        if not self.tree_libros.selection():
            messagebox.showwarning("Advertencia", "Seleccione un libro para modificar")
            return
        
        if not self.validar_libro():
            return
        
        item = self.tree_libros.selection()[0]
        libro_id = self.tree_libros.item(item)['values'][0]
        
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE libros 
                SET titulo=?, autor=?, isbn=?, categoria=?, disponible=?
                WHERE id=?
            ''', (self.titulo_var.get(), self.autor_var.get(), 
                  self.isbn_var.get(), self.categoria_var.get(), 
                  self.disponible_var.get(), libro_id))
            conn.commit()
            messagebox.showinfo("Éxito", "Libro modificado correctamente")
            self.limpiar_formulario_libro()
            self.cargar_libros()
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar libro: {str(e)}")
        finally:
            conn.close()
    
    def eliminar_libro(self):
        if not self.tree_libros.selection():
            messagebox.showwarning("Advertencia", "Seleccione un libro para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este libro?"):
            item = self.tree_libros.selection()[0]
            libro_id = self.tree_libros.item(item)['values'][0]
            
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            
            try:
                cursor.execute('DELETE FROM libros WHERE id=?', (libro_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Libro eliminado correctamente")
                self.limpiar_formulario_libro()
                self.cargar_libros()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar libro: {str(e)}")
            finally:
                conn.close()
    
    def validar_libro(self):
        if not self.titulo_var.get().strip():
            messagebox.showerror("Error", "El título es obligatorio")
            return False
        if not self.autor_var.get().strip():
            messagebox.showerror("Error", "El autor es obligatorio")
            return False
        if not self.categoria_var.get().strip():
            messagebox.showerror("Error", "La categoría es obligatoria")
            return False
        return True
    
    def limpiar_formulario_libro(self):
        self.titulo_var.set("")
        self.autor_var.set("")
        self.isbn_var.set("")
        self.categoria_var.set("")
        self.disponible_var.set(True)
    
    def seleccionar_libro(self, event):
        if self.tree_libros.selection():
            item = self.tree_libros.selection()[0]
            values = self.tree_libros.item(item)['values']
            
            self.titulo_var.set(values[1])
            self.autor_var.set(values[2])
            self.isbn_var.set(values[3])
            self.categoria_var.set(values[4])
            self.disponible_var.set(values[5] == 'Sí')
    
    # Métodos para gestión de préstamos
    def agregar_prestamo(self):
        if not self.validar_prestamo():
            return
        
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        try:
            # Obtener IDs de usuario y libro
            usuario_id = self.obtener_id_usuario(self.usuario_prestamo_var.get())
            libro_id = self.obtener_id_libro(self.libro_prestamo_var.get())
            
            if not usuario_id or not libro_id:
                messagebox.showerror("Error", "Usuario o libro no válido")
                return
            
            cursor.execute('''
                INSERT INTO prestamos (usuario_id, libro_id, fecha_prestamo, fecha_devolucion, estado)
                VALUES (?, ?, ?, ?, ?)
            ''', (usuario_id, libro_id, self.fecha_prestamo_var.get(), 
                  self.fecha_devolucion_var.get() if self.fecha_devolucion_var.get() else None, 
                  self.estado_var.get()))
            
            # Actualizar disponibilidad del libro si es préstamo activo
            if self.estado_var.get() == 'activo':
                cursor.execute('UPDATE libros SET disponible = 0 WHERE id = ?', (libro_id,))
            
            conn.commit()
            messagebox.showinfo("Éxito", "Préstamo agregado correctamente")
            self.limpiar_formulario_prestamo()
            self.cargar_prestamos()
            self.cargar_libros()  # Actualizar disponibilidad
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar préstamo: {str(e)}")
        finally:
            conn.close()
    
    def modificar_prestamo(self):
        if not self.tree_prestamos.selection():
            messagebox.showwarning("Advertencia", "Seleccione un préstamo para modificar")
            return
        
        if not self.validar_prestamo():
            return
        
        item = self.tree_prestamos.selection()[0]
        prestamo_id = self.tree_prestamos.item(item)['values'][0]
        
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        try:
            # Obtener IDs de usuario y libro
            usuario_id = self.obtener_id_usuario(self.usuario_prestamo_var.get())
            libro_id = self.obtener_id_libro(self.libro_prestamo_var.get())
            
            if not usuario_id or not libro_id:
                messagebox.showerror("Error", "Usuario o libro no válido")
                return
            
            # Obtener estado anterior
            cursor.execute('SELECT estado, libro_id FROM prestamos WHERE id = ?', (prestamo_id,))
            estado_anterior, libro_anterior = cursor.fetchone()
            
            cursor.execute('''
                UPDATE prestamos 
                SET usuario_id=?, libro_id=?, fecha_prestamo=?, fecha_devolucion=?, estado=?
                WHERE id=?
            ''', (usuario_id, libro_id, self.fecha_prestamo_var.get(), 
                  self.fecha_devolucion_var.get() if self.fecha_devolucion_var.get() else None, 
                  self.estado_var.get(), prestamo_id))
            
            # Actualizar disponibilidad del libro
            if estado_anterior == 'activo' and self.estado_var.get() == 'devuelto':
                cursor.execute('UPDATE libros SET disponible = 1 WHERE id = ?', (libro_anterior,))
            elif estado_anterior == 'devuelto' and self.estado_var.get() == 'activo':
                cursor.execute('UPDATE libros SET disponible = 0 WHERE id = ?', (libro_id,))
            
            conn.commit()
            messagebox.showinfo("Éxito", "Préstamo modificado correctamente")
            self.limpiar_formulario_prestamo()
            self.cargar_prestamos()
            self.cargar_libros()  # Actualizar disponibilidad
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar préstamo: {str(e)}")
        finally:
            conn.close()
    
    def eliminar_prestamo(self):
        """Eliminar préstamo seleccionado"""
        if not self.tree_prestamos.selection():
            messagebox.showwarning("Advertencia", "Seleccione un préstamo para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este préstamo?"):
            item = self.tree_prestamos.selection()[0]
            prestamo_id = self.tree_prestamos.item(item)['values'][0]
            
            conn = sqlite3.connect('biblioteca.db')
            cursor = conn.cursor()
            
            try:
                # Obtener información del préstamo antes de eliminar
                cursor.execute('SELECT libro_id, estado FROM prestamos WHERE id = ?', (prestamo_id,))
                libro_id, estado = cursor.fetchone()
                
                cursor.execute('DELETE FROM prestamos WHERE id=?', (prestamo_id,))
                
                # Si el préstamo estaba activo, liberar el libro
                if estado == 'activo':
                    cursor.execute('UPDATE libros SET disponible = 1 WHERE id = ?', (libro_id,))
                
                conn.commit()
                messagebox.showinfo("Éxito", "Préstamo eliminado correctamente")
                self.limpiar_formulario_prestamo()
                self.cargar_prestamos()
                self.cargar_libros()  # Actualizar disponibilidad
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar préstamo: {str(e)}")
            finally:
                conn.close()
    
    def validar_prestamo(self):
        """Validar datos del préstamo"""
        if not self.usuario_prestamo_var.get().strip():
            messagebox.showerror("Error", "Debe seleccionar un usuario")
            return False
        if not self.libro_prestamo_var.get().strip():
            messagebox.showerror("Error", "Debe seleccionar un libro")
            return False
        if not self.fecha_prestamo_var.get().strip():
            messagebox.showerror("Error", "La fecha de préstamo es obligatoria")
            return False
        return True
    
    def limpiar_formulario_prestamo(self):
        """Limpiar formulario de préstamo"""
        self.usuario_prestamo_var.set("")
        self.libro_prestamo_var.set("")
        self.fecha_prestamo_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.fecha_devolucion_var.set("")
        self.estado_var.set("activo")
    
    def seleccionar_prestamo(self, event):
        """Cargar datos del préstamo seleccionado"""
        if self.tree_prestamos.selection():
            item = self.tree_prestamos.selection()[0]
            values = self.tree_prestamos.item(item)['values']
            
            self.usuario_prestamo_var.set(values[1])
            self.libro_prestamo_var.set(values[2])
            self.fecha_prestamo_var.set(values[3])
            self.fecha_devolucion_var.set(values[4] if values[4] != 'None' else "")
            self.estado_var.set(values[5])
    
    # Métodos auxiliares
    def obtener_id_usuario(self, nombre_completo):
        """Obtener ID del usuario por nombre completo"""
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM usuarios WHERE nombre || ' ' || apellido = ?", (nombre_completo,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conn.close()
    
    def obtener_id_libro(self, titulo):
        """Obtener ID del libro por título"""
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM libros WHERE titulo = ?", (titulo,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            conn.close()
    
    # Métodos para cargar datos
    def cargar_datos(self):
        """Cargar todos los datos en las tablas"""
        self.cargar_usuarios()
        self.cargar_libros()
        self.cargar_prestamos()
        self.cargar_combos()
    
    def cargar_usuarios(self):
        """Cargar usuarios en el treeview"""
        # Limpiar treeview
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT id, nombre, apellido, email, telefono, activo FROM usuarios')
            usuarios = cursor.fetchall()
            
            for usuario in usuarios:
                activo_text = "Sí" if usuario[5] else "No"
                self.tree_usuarios.insert('', 'end', values=(
                    usuario[0], usuario[1], usuario[2], usuario[3], 
                    usuario[4], activo_text
                ))
        finally:
            conn.close()
    
    def cargar_libros(self):
        """Cargar libros en el treeview"""
        # Limpiar treeview
        for item in self.tree_libros.get_children():
            self.tree_libros.delete(item)
        
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT id, titulo, autor, isbn, categoria, disponible FROM libros')
            libros = cursor.fetchall()
            
            for libro in libros:
                disponible_text = "Sí" if libro[5] else "No"
                self.tree_libros.insert('', 'end', values=(
                    libro[0], libro[1], libro[2], libro[3], 
                    libro[4], disponible_text
                ))
        finally:
            conn.close()
    
    def cargar_prestamos(self):
        """Cargar préstamos en el treeview"""
        # Limpiar treeview
        for item in self.tree_prestamos.get_children():
            self.tree_prestamos.delete(item)
        
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT p.id, u.nombre || ' ' || u.apellido as usuario, 
                       l.titulo, p.fecha_prestamo, p.fecha_devolucion, p.estado
                FROM prestamos p
                JOIN usuarios u ON p.usuario_id = u.id
                JOIN libros l ON p.libro_id = l.id
            ''')
            prestamos = cursor.fetchall()
            
            for prestamo in prestamos:
                self.tree_prestamos.insert('', 'end', values=prestamo)
        finally:
            conn.close()
    
    def cargar_combos(self):
        """Cargar datos en los comboboxes"""
        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()
        
        try:
            # Cargar usuarios activos
            cursor.execute('SELECT nombre || " " || apellido FROM usuarios WHERE activo = 1')
            usuarios = [row[0] for row in cursor.fetchall()]
            self.combo_usuarios['values'] = usuarios
            
            # Cargar libros disponibles
            cursor.execute('SELECT titulo FROM libros WHERE disponible = 1')
            libros = [row[0] for row in cursor.fetchall()]
            self.combo_libros['values'] = libros
        finally:
            conn.close()
    
    def ejecutar(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

# Función principal
def main():
    app = BibliotecaApp()
    app.ejecutar()

if __name__ == "__main__":
    main()