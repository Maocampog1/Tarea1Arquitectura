import mysql.connector
from mysql.connector import Error

DB_NAME = "guardar_nombres"
DB_USER = "root"
DB_PASS = "Admin123."
DB_HOST = "localhost"

class GestorNombres:
    def __init__(self):
        self.conexion = None
        self.cursor = None

    def ejecutar_sql(self, query, params=None, many=False):
        """Ejecuta una consulta SQL con opción de parámetros"""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall() if query.strip().lower().startswith("select") else self.conexion.commit()

    def conectar(self):
        """Crea la BD si no existe y conecta"""
        try:
            # Conexión temporal para crear la BD
            tmp = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
            tmp.cursor().execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
            tmp.close()

            # Conexión definitiva a la BD
            self.conexion = mysql.connector.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
            )
            self.cursor = self.conexion.cursor()
            print("Conectado a MySQL")

            # Crear tabla si no existe
            self.ejecutar_sql("""
                CREATE TABLE IF NOT EXISTS nombres(
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        except Error as e:
            print("Error:", e)
            return False
        return True

    def insertar_nombre(self, nombre):
        self.ejecutar_sql("INSERT INTO nombres (nombre) VALUES (%s)", (nombre,))
        print(f"Nombre '{nombre}' guardado.")

    def mostrar_nombres(self):
        filas = self.ejecutar_sql("SELECT id, nombre, fecha_registro FROM nombres ORDER BY fecha_registro DESC")
        if filas:
            for f in filas:
                print(f"ID: {f[0]} | Nombre: {f[1]} | Fecha: {f[2]}")
        else:
            print("No hay nombres guardados.")

    def cerrar(self):
        if self.cursor: self.cursor.close()
        if self.conexion: self.conexion.close()
        print("Conexión cerrada")

def main():
    gestor = GestorNombres()
    if not gestor.conectar():
        return

    while True:
        print("\nMenú:\n1. Agregar nombre\n2. Ver nombres\n3. Salir")
        op = input("Opción: ").strip()

        if op == "1":
            nombre = input("Ingresa el nombre: ").strip()
            if nombre: gestor.insertar_nombre(nombre)
            else: print("Nombre no válido.")
        elif op == "2":
            gestor.mostrar_nombres()
        elif op == "3":
            print("Adiosito")
            break
        else:
            print("Opción inválida")

    gestor.cerrar()

if __name__ == "__main__":
    main()
