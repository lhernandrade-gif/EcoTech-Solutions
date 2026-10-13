from typing import Any
from .Departamento import Departamento

class DepartamentoRepositorio:
    def __init__(self, sesion: BaseDatos) -> None:
        self.config: BaseDatos = sesion

    def guardar(self, departamento: Departamento) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            for empleado in departamento.lista_empleados:
                cursor.execute('''
                               INSERT INTO departamentos (nombre, gerente, empleado)
                               VALUES (%s, %s, %s)
                               ''', (departamento.nombre, departamento.gerente, empleado))
                conexion.commit()
            #Las líneas siguientes retornan el objeto empleado con su id asignado por MySQL
            #El programa actualmente no requiere esta funcionalidad
            #empleado.empleado_id = cursor.lastrowid
            #return empleado

    def buscar_por_id(self, departamento: Departamento) -> Departamento:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT id, nombre, gerente, empleado
                              FROM departamentos
                              WHERE id = %s''', (departamento.departamento_id,))
            filas: tuple[tuple[Any,...]] | None = cursor.fetchall()
            if filas is None: return None
            resultados_consulta = ()
            for fila in filas:
                resultados_consulta.append(Departamento(departamento_id=fila[0], nombre=fila[1], gerente=fila[2], empleado=fila[3]))
            return resultados_consulta

    def actualizar(self, departamento: Departamento) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            for empleado in departamento.lista_empleados:
                cursor.execute('''UPDATE departamentos
                                  SET nombre = %s, gerente = %s, empleado = %s
                                  WHERE id = %s''',
                               (departamento.nombre, departamento.gerente, empleado, departamento.departamento_id))
            conexion.commit()

    def eliminar(self, departamento: Departamento) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM departamentos WHERE id = %s', (departamento.departamento_id,))
            conexion.commit()