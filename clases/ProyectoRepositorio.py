from typing import Any
from .Proyecto import Proyecto

class ProyectoRepositorio:
    def __init__(self, sesion: BaseDatos) -> None:
        self.config: BaseDatos = sesion

    def guardar(self, proyecto: Proyecto) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            for empleado in proyecto.lista_empleados:
                cursor.execute('''
                               INSERT INTO proyectos (nombre, descripcion, fecha_proyecto, empleado)
                               VALUES (%s, %s, %s, %s)
                               ''', (proyecto.nombre, proyecto.descripcion, proyecto.fecha_proyecto, empleado))
                conexion.commit()

            #Las líneas siguientes retornan el objeto empleado con su id asignado por MySQL
            #El programa actualmente no requiere esta funcionalidad
            #empleado.empleado_id = cursor.lastrowid
            #return empleado

    def buscar_por_id(self, proyecto: Proyecto) -> Proyecto:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT p.proyecto_id, p.nombre, p.descripcion, p.fecha_proyecto, pe.empleado_id
                              FROM proyectos AS p
                              JOIN proyecto_empleados AS pe
                              ON p.proyecto_id = pe.empleado_id
                              WHERE p.proyecto_id = %s''', (proyecto.proyecto_id,))
            filas: tuple[tuple[Any,...]] | None = cursor.fetchall()
            if filas is None: return None
            resultados_consulta = []
            for fila in filas:
                resultados_consulta.append({"proyecto_id": fila[0], "nombre": fila[1], "descripcion": fila[2], "fecha_proyecto": fila[3], "empleado": fila[4]})
            return resultados_consulta

    def actualizar(self, proyecto: Proyecto) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''UPDATE proyecto
                                SET nombre = %s, descripcion = %s, fecha_proyecto = %s,
                                WHERE proyecto_id = %s''',
                            (proyecto.nombre, proyecto.descripcion, proyecto.fecha_proyecto, proyecto.proyecto_id))
            for empleado in proyecto.lista_empleados:
                cursor.execute('''UPDATE proyecto_empleados
                                  SET proyecto_id = %s,
                                      empleado_id     = %s
                               ''', (proyecto.proyecto_id, empleado))
            conexion.commit()

    def eliminar(self, proyecto: Proyecto) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM proyecto WHERE id = %s', (proyecto.proyecto_id,))
            conexion.commit()