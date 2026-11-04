from typing import Any
from .Proyecto import Proyecto
from .BaseDatos import BaseDatos

class ProyectoRepositorio:
    def __init__(self, sesion: BaseDatos) -> None:
        self.config: BaseDatos = sesion

    def guardar(self, proyecto: Proyecto) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                            INSERT INTO proyectos (nombre, descripcion, fecha_inicio_proyecto)
                            VALUES (%s, %s, %s)
                            ''', (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio_proyecto))
            proyecto_id = cursor.lastrowid
            for empleado in proyecto.lista_empleados:
                cursor.execute('''
                                INSERT INTO proyecto_empleados (proyecto_id, empleado_id)
                                VALUES (%s, %s)
                                ''',
                               (proyecto_id, empleado))
            conexion.commit()

    def buscar_por_id(self, proyecto: Proyecto) -> Proyecto | None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT proyecto_id, nombre, descripcion, fecha_inicio_proyecto
                              FROM proyectos
                              WHERE proyecto_id = %s''', (proyecto.proyecto_id,))
            fila: tuple[Any, ...] | None = cursor.fetchone()
            if fila is None:
                return None
            cursor.execute('''SELECT empleado_id
                              FROM proyecto_empleados
                              WHERE proyecto_id = %s
                              ORDER BY empleado_id''', (fila[0],))
            empleados = [fila_empleado[0] for fila_empleado in cursor.fetchall()]
            return Proyecto(
                proyecto_id=fila[0],
                nombre=fila[1],
                descripcion=fila[2],
                fecha_inicio_proyecto=fila[3],
                lista_empleados=empleados,
            )

    def actualizar(self, proyecto: Proyecto) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''UPDATE proyectos
                              SET nombre = %s, descripcion = %s, fecha_inicio_proyecto = %s
                              WHERE proyecto_id = %s''',
                           (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio_proyecto, proyecto.proyecto_id))
            cursor.execute('''DELETE FROM proyecto_empleados
                              WHERE proyecto_id = %s''', (proyecto.proyecto_id,))
            for empleado in proyecto.lista_empleados:
                cursor.execute('''INSERT INTO proyecto_empleados (proyecto_id, empleado_id)
                                  VALUES (%s, %s)''', (proyecto.proyecto_id, empleado))
            conexion.commit()

    def eliminar(self, proyecto: Proyecto) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM proyectos WHERE proyecto_id = %s', (proyecto.proyecto_id,))
            conexion.commit()