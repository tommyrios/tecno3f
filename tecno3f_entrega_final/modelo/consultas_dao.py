import re
from tkinter import messagebox
from .conexiondb import ConexionDB

def crear_tablas():
    with ConexionDB() as con:
        sql = '''
            CREATE TABLE IF NOT EXISTS productos (
                id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
                descripcion TEXT NOT NULL UNIQUE,
                precio REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS transacciones (
                id_transaccion INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto INTEGER,
                cantidad INTEGER NOT NULL,
                tipo_transaccion TEXT NOT NULL,
                FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
            );

            CREATE TABLE IF NOT EXISTS stock_productos (
                id_producto INTEGER PRIMARY KEY,
                stock INTEGER NOT NULL,
                FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
            );
            '''

        try:
            con.cursor.executescript(sql)
            print("Tablas creadas exitosamente.")
        except Exception as e:
            print(f"Error al crear tablas: {e}")

def limpiar_base_datos():
    try:
        con = ConexionDB()
        con.cursor.execute("DROP TABLE IF EXISTS transacciones")
        con.cursor.execute("DROP TABLE IF EXISTS stock_productos")
        con.cursor.execute("DROP TABLE IF EXISTS productos")
        crear_tablas()
        con.conexion.commit()
        messagebox.showinfo("Éxito", "Base de datos limpiada exitosamente. Tablas recreadas.")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo limpiar la base de datos: {e}")
        
    finally:
        con.cerrar_con()

def actualizar_treeview(tree):
    con = ConexionDB()
    try:
        records = tree.get_children()
        for element in records:
            tree.delete(element)

        sql = "SELECT * FROM productos ORDER BY id_producto DESC"
        con.cursor.execute(sql)
        resultados = con.cursor.fetchall()

        for fila in resultados:
            tree.insert("", 0, text=fila[0], values=(fila[1], fila[2]))

    except Exception as e:
        print(f"Error al actualizar treeview: {e}")

    finally:
        con.cerrar_con()

def validar_precio(precio):
    patron_precio = r"^[0-9]*\.?[0-9]+$"    
    return re.match(patron_precio, str(precio)) 

def agregar_productos(descripcion, precio):
    con = ConexionDB()
    try:
        if not validar_precio(precio):
            messagebox.showerror("Error", "Precio no válido. Debe ser un número positivo.")
            return

        patron_descrip = r"^[A-Za-záéíóúñÑ\s]+$"
        if re.match(patron_descrip, descripcion):
            con.cursor.execute("SELECT descripcion FROM productos")
            productos_existentes = [fila[0].lower() for fila in con.cursor.fetchall()]
            if descripcion.lower() in productos_existentes:
                messagebox.showerror("Error", "El producto ya existe en la base de datos.")
            else:
                sql_insert_producto = "INSERT INTO productos (descripcion, precio) VALUES (?, ?)"
                con.cursor.execute(sql_insert_producto, (descripcion, precio))
                con.conexion.commit()

                sql_insert_stock = "INSERT INTO stock_productos (id_producto, stock) VALUES (?, ?)"
                con.cursor.execute(sql_insert_stock, (con.cursor.lastrowid, 0))
                con.conexion.commit()

                messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
        else:
            messagebox.showerror("Error", "El campo descripción debe contener solo letras y espacios.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")

    finally:
        con.cerrar_con()

def editar_producto(id_producto, nueva_descripcion, nuevo_precio):
    con = ConexionDB()
    try:
        if not validar_precio(nuevo_precio):
            messagebox.showerror("Error", "Precio no válido. Debe ser un número positivo.")
            return

        patron_descrip = r"^[A-Za-záéíóúñÑ\s]+$"
        if re.match(patron_descrip, nueva_descripcion):
            sql_update_producto = "UPDATE productos SET descripcion = ?, precio = ? WHERE id_producto = ?"
            con.cursor.execute(sql_update_producto, (nueva_descripcion, nuevo_precio, id_producto))
            con.conexion.commit()
            messagebox.showinfo("Éxito", "Producto editado exitosamente.")
        else:
            messagebox.showerror("Error", "El campo descripción debe contener solo letras y espacios.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo editar el producto: {e}")

    finally:
        con.cerrar_con()

def eliminar_producto(id_producto):
    con = ConexionDB()
    try:
        con.cursor.execute("DELETE FROM transacciones WHERE id_producto = ?", (id_producto,))
        con.cursor.execute("DELETE FROM stock_productos WHERE id_producto = ?", (id_producto,))
        con.cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
        con.conexion.commit()
        messagebox.showinfo("Éxito", "Producto eliminado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")

    finally:
        con.cerrar_con()

def agregar_transaccion(nombre_producto, cantidad, tipo_transaccion):
    con = ConexionDB()
    try:
        con.cursor.execute("SELECT id_producto, stock FROM productos JOIN stock_productos USING (id_producto) WHERE LOWER(descripcion) = LOWER(?)", (nombre_producto,))
        resultado = con.cursor.fetchone()

        if resultado:
            id_producto = resultado[0]
            stock_actual = resultado[1]

            if tipo_transaccion.lower() == 'venta' and cantidad > stock_actual:
                messagebox.showerror("Error", "No hay suficiente stock para realizar la venta.")
                return

            if tipo_transaccion.lower() == 'compra':
                nuevo_stock = stock_actual + cantidad
                sql_update_stock = "UPDATE stock_productos SET stock = ? WHERE id_producto = ?"
            elif tipo_transaccion.lower() == 'venta':
                nuevo_stock = stock_actual - cantidad
                sql_update_stock = "UPDATE stock_productos SET stock = ? WHERE id_producto = ?"

            con.cursor.execute(sql_update_stock, (nuevo_stock, id_producto))

            sql_insert_transaccion = "INSERT INTO transacciones (id_producto, cantidad, tipo_transaccion) VALUES (?, ?, ?)"
            con.cursor.execute(sql_insert_transaccion, (id_producto, cantidad, tipo_transaccion))

            con.conexion.commit()  # Confirmar la transacción

            messagebox.showinfo("Éxito", "Transacción agregada exitosamente.")
        else:
            messagebox.showerror("Error", "Producto no encontrado en la base de datos.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar la transacción: {e}")

    finally:
        con.cerrar_con()

def obtener_productos():
    try:
        with ConexionDB() as con:
            con.cursor.execute('SELECT * FROM productos')
            productos = con.cursor.fetchall()
            return productos
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []

def obtener_transacciones():
    con = ConexionDB()
    try:
        con.cursor.execute('SELECT * FROM transacciones')
        transacciones = con.cursor.fetchall()
        return transacciones
    except Exception as e:
        print(f"Error al obtener transacciones: {e}")
        return []
    finally:
        con.cerrar_con()

def obtener_stock():
    con = ConexionDB()
    try:
        con.cursor.execute('SELECT * FROM stock_productos')
        stock = con.cursor.fetchall()
        return stock
    except Exception as e:
        print(f"Error al obtener stock: {e}")
        return []
    finally:
        con.cerrar_con()

def agregar_stock(id_producto, cantidad):
    con = ConexionDB()
    try:
        sql = "UPDATE stock_productos SET stock = stock + ? WHERE id_producto = ?"
        con.cursor.execute(sql, (cantidad, id_producto))
        con.conexion.commit()
        print("Stock agregado correctamente.")
    except Exception as e:
        print(f"Error al agregar stock: {e}")
    finally:
        con.cerrar_con()

def quitar_stock(id_producto, cantidad):
    con = ConexionDB()
    try:
        sql = "UPDATE stock_productos SET stock = stock - ? WHERE id_producto = ?"
        con.cursor.execute(sql, (cantidad, id_producto))
        con.conexion.commit()
        print("Stock quitado correctamente.")
    except Exception as e:
        print(f"Error al quitar stock: {e}")
    finally:
        con.cerrar_con()
