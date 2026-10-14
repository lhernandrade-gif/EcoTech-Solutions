from typing import Any
from .Empleado import Empleado
from .BaseDatos import BaseDatos

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
            cursor.execute('''SELECT empleado_id, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, rut, direccion, telefono, email, fecha_inicio_contrato, salario
                              FROM empleados
                              WHERE empleado_id = %s''', (empleado.empleado_id,))
            fila: tuple[Any,...] | None = cursor.fetchone()
            if fila is None: return None
            return Empleado(empleado_id=fila[0], primer_nombre=fila[1], segundo_nombre=fila[2], primer_apellido=fila[3], segundo_apellido=fila[4], rut=fila[5], direccion=fila[6], telefono=fila[7], email=fila[8], fecha_inicio_contrato=fila[9], salario=fila[10])

    def actualizar(self, empleado: Empleado) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''UPDATE empleados
                              SET primer_nombre = %s, segundo_nombre = %s, primer_apellido = %s, segundo_apellido = %s, rut = %s, direccion = %s, telefono = %s, email = %s, fecha_inicio_contrato = %s, salario = %s
                              WHERE empleado_id = %s''',
                           (empleado.primer_nombre, empleado.segundo_nombre, empleado.primer_apellido, empleado.segundo_apellido, empleado.rut, empleado.direccion, empleado.telefono, empleado.email, empleado.fecha_inicio_contrato, empleado.salario, empleado.empleado_id))
            conexion.commit()

    def eliminar(self, empleado: Empleado) -> None:
        print("Se entra al método Empleado.eliminar")
        print(empleado.empleado_id)
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM empleados WHERE empleado_id = %s', (empleado.empleado_id,))
            print("Línea siguiente al .execute")
            conexion.commit()