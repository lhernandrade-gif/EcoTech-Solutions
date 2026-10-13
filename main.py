import os
import pymysql
from dotenv import load_dotenv
from datetime import date
from typing import Any
import clases
import utilidades

def main():
     load_dotenv()
     sesion_actual = clases.BaseDatos(os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))
     empleado_repositorio = clases.EmpleadoRepositorio(sesion_actual)
     empleado_test = clases.Empleado(empleado_id = 1)
     empleado_test = empleado_repositorio.buscar_por_id(empleado_test)
     utilidades.mostrar_datos(empleado_test)

#El siguiente código permitiría crear el esquema de la BD durante la ejecución del programa
"""
def inicializar_base_de_datos(connection):
    cursor = connection.cursor()

    # 1. Crear tablas
    if os.path.exists("schema.sql"):
        with open("schema.sql", "r", encoding="utf-8") as f:
            # Dividir por punto y coma para ejecutar comando por comando
            comandos = f.read().split(";")
            for comando in comandos:
                if comando.strip():
                    cursor.execute(comando)
        print("[INFO] Estructura de la base de datos creada exitosamente.")

    # 2. Insertar datos de prueba
    if os.path.exists("seed.sql"):
        with open("seed.sql", "r", encoding="utf-8") as f:
            comandos = f.read().split(";")
            for comando in comandos:
                if comando.strip():
                    cursor.execute(comando)
        print("[INFO] Datos de prueba insertados exitosamente.")

    connection.commit()
"""

if __name__ == "__main__":
    main()