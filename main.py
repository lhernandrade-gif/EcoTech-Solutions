import os
import pymysql
from dotenv import load_dotenv
from datetime import date

class BaseDatos:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def conectar(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )


class Empleado:
    def __init__(
            self,
            primer_nombre: str | None = None,
            primer_apellido: str | None = None,
            segundo_apellido: str | None = None,
            rut: str | None = None,
            email: str | None = None,
            segundo_nombre: str | None = None,
            empleado_id: int | None = None,
            direccion: str | None = None,
            telefono: str | None = None,
            fecha_inicio_contrato: date | None = None,
            salario: int | None = None
    ) -> None:
        self.empleado_id = empleado_id
        self.primer_nombre = primer_nombre
        self.segundo_nombre = segundo_nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.rut = rut
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario

    def obtener_datos_contacto(self) -> dict:
        pass

    def registrar_horas(self, registro: RegistroTiempo) -> None:
        pass


class EmpleadoRepositorio:
    def __init__(self, sesion: BaseDatos) -> None:
        self.config: BaseDatos = sesion

    def guardar(self, empleado: Empleado) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                           INSERT INTO empleados (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, rut, direccion, telefono, email, fecha_inicio_contrato, salario)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                           ''', (empleado.primer_nombre, empleado.segundo_nombre, empleado.primer_apellido, empleado.segundo_apellido, empleado.rut, empleado.direccion, empleado.telefono, empleado.email, empleado.fecha_inicio_contrato, empleado.salario))
            conexion.commit()
            #Las líneas siguientes retornan el objeto empleado con su id asignado por MySQL
            #El programa actualmente no requiere esta funcionalidad
            #empleado.empleado_id = cursor.lastrowid
            #return empleado

    def buscar_por_id(self, empleado: Empleado) -> Empleado:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT id, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, rut, direccion, telefono, email, fecha_inicio_contrato, salario
                              FROM empleados
                              WHERE id = %s''', (empleado.empleado_id,))
            fila: tuple = cursor.fetchone()
            if fila is None: return None
            return Empleado(empleado_id=fila[0], primer_nombre=fila[1], segundo_nombre=fila[2], primer_apellido=fila[3], segundo_apellido=fila[4], rut=fila[5], direccion=fila[6], telefono=fila[7], email=fila[8], fecha_inicio_contrato=fila[9], salario=fila[10])

    def actualizar(self, empleado: Empleado) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''UPDATE empleados
                              SET primer_nombre = %s, segundo_nombre = %s, primer_apellido = %s, segundo_apellido = %s, rut = %s, direccion = %s, telefono = %s, email = %s, fecha_inicio_contrato = %s, salario = %s
                              WHERE id = %s''',
                           (empleado.primer_nombre, empleado.segundo_nombre, empleado.primer_apellido, empleado.segundo_apellido, empleado.rut, empleado.direccion, empleado.telefono, empleado.email, empleado.fecha_inicio_contrato, empleado.salario, empleado.empleado_id))
            conexion.commit()

    def eliminar(self, empleado: Empleado) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM empleados WHERE id = %s', (empleado.empleado_id,))
            conexion.commit()

load_dotenv()
sesion = BaseDatos(os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))
empleado_repositorio = EmpleadoRepositorio(sesion)
empleado_test = Empleado(empleado_id = 1)
empleado_test = empleado_repositorio.buscar_por_id(empleado_test)
print(empleado_test.primer_nombre)

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