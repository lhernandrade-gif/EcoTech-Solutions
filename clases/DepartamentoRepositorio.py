from typing import Any
from .Departamento import Departamento
import utilidades

class DepartamentoRepositorio:
    def __init__(self, sesion: BaseDatos) -> None:
        self.config: BaseDatos = sesion

    def guardar(self, departamento: Departamento) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                           INSERT INTO departamentos (nombre, gerente)
                           VALUES (%s, %s)
                           ''', (departamento.nombre, departamento.gerente))
            departamento.departamento_id = cursor.lastrowid
            for empleado in departamento.lista_empleados:
                cursor.execute('''
                               INSERT INTO departamento_empleados (departamento_id, empleado_id)
                               VALUES (%s, %s)
                               ''', (departamento.departamento_id, empleado))
            conexion.commit()
            #return empleado

    def buscar_por_id(self, departamento: Departamento) -> Departamento:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT d.departamento_id, d.nombre, d.gerente, de.empleado_id
                              FROM departamentos AS d
                              JOIN departamento_empleados AS de
                              ON d.departamento_id = de.departamento_id
                              WHERE d.departamento_id = %s''', (departamento.departamento_id,))
            filas: tuple[tuple[Any,...]] | None = cursor.fetchall()
            if filas is None: return None
            resultados_consulta = []
            for fila in filas:
                resultados_consulta.append({"departamento_id": fila[0], "nombre": fila[1], "gerente": fila[2], "empleado_id": fila[3]})
            return resultados_consulta

    def actualizar(self, departamento: Departamento) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''UPDATE departamentos
                              SET nombre = %s, gerente = %s
                              WHERE departamento_id = %s''',
                           (departamento.nombre, departamento.gerente, departamento.departamento_id))
            cursor.execute('''DELETE
                              FROM departamento_empleados
                              WHERE departamento_id = %s''',
                           (departamento.departamento_id,))
            for empleado in departamento.lista_empleados:
                cursor.execute('''INSERT INTO departamento_empleados (departamento_id, empleado_id)
                                  VALUES (%s, %s)
                               ''', (departamento.departamento_id, empleado))
            conexion.commit()

    def eliminar(self, departamento: Departamento) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM departamentos WHERE departamento_id = %s', (departamento.departamento_id,))
            conexion.commit()