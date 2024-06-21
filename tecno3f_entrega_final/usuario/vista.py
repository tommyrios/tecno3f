import tkinter as tk
from tkinter import ttk, messagebox
from modelo.consultas_dao import (
    agregar_productos, agregar_transaccion, obtener_productos,
    editar_producto, eliminar_producto, agregar_stock, quitar_stock, limpiar_base_datos
)

def barrita_menu(root):
    barra = tk.Menu(root)
    root.config(menu = barra, width = 300 , height = 300)
    menu_inicio = tk.Menu(barra, tearoff=0)

    #  niveles  #

    #principal

    barra.add_cascade(label='Inicio', menu = menu_inicio)
    barra.add_cascade(label='Consultas')
    barra.add_cascade(label='Acerca de..')
    barra.add_cascade(label='Ayuda')

    #submenu
    menu_inicio.add_command(label='Conectar DB')
    menu_inicio.add_command(label='Desconectar DB')
    menu_inicio.add_command(label='Salir', command= root.destroy)

class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=800, height=600)
        self.root = root
        self.pack()
        self.id_producto_seleccionado = None

        self.crear_widgets()

    def crear_widgets(self):
        self.label_descripcion = tk.Label(self, text="Descripción: ")
        self.label_descripcion.config(font=('Arial', 12, 'bold'))
        self.label_descripcion.grid(row=0, column=0, padx=10, pady=10)

        self.label_precio = tk.Label(self, text="Precio: ")
        self.label_precio.config(font=('Arial', 12, 'bold'))
        self.label_precio.grid(row=1, column=0, padx=10, pady=10)

        self.descripcion = tk.StringVar()
        self.entry_descripcion = tk.Entry(self, textvariable=self.descripcion)
        self.entry_descripcion.config(width=50, font=('Arial', 12))
        self.entry_descripcion.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.precio = tk.StringVar()
        self.entry_precio = tk.Entry(self, textvariable=self.precio)
        self.entry_precio.config(width=50, font=('Arial', 12))
        self.entry_precio.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

        self.btn_nuevo = tk.Button(self, text='Nuevo', command=self.habilitar_campos)
        self.btn_nuevo.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#1C500B', cursor='hand2', activebackground='#3FD83F', activeforeground='#000000')
        self.btn_nuevo.grid(row=3, column=0, padx=10, pady=10)

        self.btn_guardar = tk.Button(self, text='Guardar', command=self.guardar_producto)
        self.btn_guardar.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#0D2A83', cursor='hand2', activebackground='#7594F5', activeforeground='#000000', state='disabled')
        self.btn_guardar.grid(row=3, column=1, padx=10, pady=10)

        self.btn_cancelar = tk.Button(self, text='Cancelar', command=self.cancelar_edicion)
        self.btn_cancelar.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#A90A0A', cursor='hand2', activebackground='#F35B5B', activeforeground='#000000', state='disabled')
        self.btn_cancelar.grid(row=3, column=2, padx=10, pady=10)

        self.label_producto = tk.Label(self, text="Producto: ")
        self.label_producto.config(font=('Arial', 12, 'bold'))
        self.label_producto.grid(row=4, column=0, padx=10, pady=10)

        self.productos = obtener_productos()
        self.lista_productos = [producto[1] for producto in self.productos]
        self.combo_producto = ttk.Combobox(self, values=self.lista_productos, state="readonly")
        self.combo_producto.config(width=50, font=('Arial', 12))
        self.combo_producto.grid(row=4, column=1, padx=10, pady=10, columnspan=2)

        self.label_cantidad = tk.Label(self, text="Cantidad: ")
        self.label_cantidad.config(font=('Arial', 12, 'bold'))
        self.label_cantidad.grid(row=5, column=0, padx=10, pady=10)

        self.cantidad = tk.IntVar()
        self.entry_cantidad = tk.Entry(self, textvariable=self.cantidad)
        self.entry_cantidad.config(width=50, font=('Arial', 12))
        self.entry_cantidad.grid(row=5, column=1, padx=10, pady=10, columnspan=2)

        self.label_tipo = tk.Label(self, text="Tipo Transacción: ")
        self.label_tipo.config(font=('Arial', 12, 'bold'))
        self.label_tipo.grid(row=6, column=0, padx=10, pady=10)

        self.tipo_transaccion = tk.StringVar()
        self.combo_tipo = ttk.Combobox(self, values=["Compra", "Venta"], textvariable=self.tipo_transaccion, state="readonly")
        self.combo_tipo.config(width=50, font=('Arial', 12))
        self.combo_tipo.grid(row=6, column=1, padx=10, pady=10, columnspan=2)

        self.btn_agregar_transaccion = tk.Button(self, text='Agregar Transacción', command=self.agregar_transaccion)
        self.btn_agregar_transaccion.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#1C500B', cursor='hand2', activebackground='#3FD83F', activeforeground='#000000')
        self.btn_agregar_transaccion.grid(row=7, column=0, padx=10, pady=10)

        self.btn_editar_producto = tk.Button(self, text='Editar Producto', command=self.editar_producto)
        self.btn_editar_producto.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#FF8C00', cursor='hand2', activebackground='#FFA500', activeforeground='#000000')
        self.btn_editar_producto.grid(row=7, column=1, padx=10, pady=10)

        self.btn_eliminar_producto = tk.Button(self, text='Eliminar Producto', command=self.eliminar_producto)
        self.btn_eliminar_producto.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#FF0000', cursor='hand2', activebackground='#FF6347', activeforeground='#000000')
        self.btn_eliminar_producto.grid(row=7, column=2, padx=10, pady=10)

        self.tree_productos = ttk.Treeview(self, columns=('Descripción', 'Precio'))
        self.tree_productos.heading('#0', text='ID')
        self.tree_productos.heading('#1', text='Descripción')
        self.tree_productos.heading('#2', text='Precio')
        self.tree_productos.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

        self.scroll_productos = ttk.Scrollbar(self, orient='vertical', command=self.tree_productos.yview)
        self.scroll_productos.grid(row=8, column=3, sticky='nse')
        self.tree_productos.configure(yscrollcommand=self.scroll_productos.set)

        self.cargar_productos()

        self.btn_limpiar_bd = tk.Button(self, text='Limpiar Base de Datos', command=self.limpiar_base_datos)
        self.btn_limpiar_bd.config(width=20, font=('Arial', 12, 'bold'), fg='#FFFFFF', bg='#FFA500', cursor='hand2', activebackground='#FFD700', activeforeground='#000000')
        self.btn_limpiar_bd.grid(row=10, column=1, padx=10, pady=10)

        self.tree_productos.bind('<ButtonRelease-1>', self.seleccionar_producto)

    def habilitar_campos(self):
        self.entry_descripcion.config(state='normal')
        self.entry_precio.config(state='normal')
        self.btn_guardar.config(state='normal')
        self.btn_cancelar.config(state='normal')
        self.btn_nuevo.config(state='disabled')
        self.combo_producto.config(state='normal')
        self.entry_cantidad.config(state='normal')
        self.combo_tipo.config(state='normal')

    def cancelar_edicion(self):
        self.entry_descripcion.config(state='disabled')
        self.entry_precio.config(state='disabled')
        self.btn_guardar.config(state='disabled')
        self.btn_cancelar.config(state='disabled')
        self.btn_nuevo.config(state='normal')
        self.combo_producto.config(state='disabled')
        self.entry_cantidad.config(state='disabled')
        self.combo_tipo.config(state='disabled')

        self.limpiar_campos()

    def limpiar_campos(self):
        self.descripcion.set('')
        self.precio.set('')
        self.entry_cantidad.delete(0, tk.END)
        self.id_producto_seleccionado = None

    def guardar_producto(self):
        descripcion = self.descripcion.get()
        precio = self.precio.get()

        if descripcion and precio:
            if self.id_producto_seleccionado:
                editar_producto(self.id_producto_seleccionado, descripcion, precio)
            else:
                agregar_productos(descripcion, precio)
            self.cargar_productos()
            self.actualizar_lista_productos()
            self.cancelar_edicion()
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos.")

    def cargar_productos(self):
        productos = obtener_productos()
        self.tree_productos.delete(*self.tree_productos.get_children())

        for producto in productos:
            self.tree_productos.insert("", 0, text=producto[0], values=(producto[1], producto[2]))

    def actualizar_lista_productos(self):
        self.productos = obtener_productos()
        self.lista_productos = [producto[1] for producto in self.productos]
        self.combo_producto['values'] = self.lista_productos

    def agregar_transaccion(self):
        producto_seleccionado = self.combo_producto.get()
        cantidad = self.cantidad.get()
        tipo_transaccion = self.tipo_transaccion.get()

        if producto_seleccionado and cantidad and tipo_transaccion:
            agregar_transaccion(producto_seleccionado, cantidad, tipo_transaccion)
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "Todos los campos son requeridos.")

    def seleccionar_producto(self, event):
        selection = self.tree_productos.selection()
        if selection:
            item = selection[0]
            self.id_producto_seleccionado = self.tree_productos.item(item, 'text')
            self.descripcion.set(self.tree_productos.item(item, 'values')[0])
            self.precio.set(self.tree_productos.item(item, 'values')[1])
            self.habilitar_campos()

    def editar_producto(self):
        if self.id_producto_seleccionado:
            descripcion = self.descripcion.get()
            precio = self.precio.get()

            if descripcion and precio:
                editar_producto(self.id_producto_seleccionado, descripcion, precio)
                self.cargar_productos()
                self.cancelar_edicion()
            else:
                messagebox.showerror("Error", "Todos los campos son requeridos.")
        else:
            messagebox.showerror("Error", "Seleccione un producto para editar.")

    def eliminar_producto(self):
        if self.id_producto_seleccionado:
            if messagebox.askyesno("Confirmar", "¿Está seguro que desea eliminar este producto?"):
                eliminar_producto(self.id_producto_seleccionado)
                self.cargar_productos()
                self.cancelar_edicion()
        else:
            messagebox.showerror("Error", "Seleccione un producto para eliminar.")

    def limpiar_base_datos(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro que desea limpiar toda la base de datos? Esta acción no se puede deshacer."):
            limpiar_base_datos()
            self.cargar_productos()

