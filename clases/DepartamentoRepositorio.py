from typing import Any
from .Departamento import Departamento
from .BaseDatos import BaseDatos
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
            for empleado in departamento.lista_empleados or []:
                cursor.execute('''
                               INSERT INTO departamento_empleados (departamento_id, empleado_id)
                               VALUES (%s, %s)
                               ''', (departamento.departamento_id, empleado))
            conexion.commit()
            #return empleado

    def buscar_por_id(self, departamento: Departamento) -> Departamento | None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT departamento_id, nombre, gerente
                              FROM departamentos
                              WHERE departamento_id = %s''', (departamento.departamento_id,))
            fila: tuple[Any, ...] | None = cursor.fetchone()
            if fila is None:
                return None
            cursor.execute('''SELECT empleado_id
                              FROM departamento_empleados
                              WHERE departamento_id = %s
                              ORDER BY empleado_id''', (fila[0],))
            empleados = [fila_empleado[0] for fila_empleado in cursor.fetchall()]
            return Departamento(
                departamento_id=fila[0],
                nombre=fila[1],
                gerente=fila[2],
                lista_empleados=empleados,
            )

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
            for empleado in departamento.lista_empleados or []:
                cursor.execute('''INSERT INTO departamento_empleados (departamento_id, empleado_id)
                                  VALUES (%s, %s)
                               ''', (departamento.departamento_id, empleado))
            conexion.commit()

    def eliminar(self, departamento: Departamento) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM departamentos WHERE departamento_id = %s', (departamento.departamento_id,))
            conexion.commit()