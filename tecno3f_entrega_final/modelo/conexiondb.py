import sqlite3

class ConexionDB:
    def __init__(self):
        self.base_datos = "ddbb/entregaFinal.db"
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar_con(self):
        self.conexion.commit()
        self.conexion.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cerrar_con()
