from typing import Any
from .RegistroTiempo import RegistroTiempo

class RegistroTiempoRepositorio:
    def __init__(self, sesion: BaseDatos) -> None:
        self.config: BaseDatos = sesion

    def guardar(self, registro_tiempo: RegistroTiempo) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                           INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion_tareas, empleado_id, proyecto_id)
                           VALUES (%s, %s, %s, %s, %s)
                           ''', (registro_tiempo.fecha, registro_tiempo.horas_trabajadas, registro_tiempo.descripcion_tareas, registro_tiempo.empleado_id, registro_tiempo.proyecto_id))
            conexion.commit()
            #Las líneas siguientes retornan el objeto registro_tiempo con su id asignado por MySQL
            #El programa actualmente no requiere esta funcionalidad
            #registro_tiempo.registro_tiempo_id = cursor.lastrowid
            #return registro_tiempo

    def buscar_por_id(self, registro_tiempo: RegistroTiempo) -> RegistroTiempo:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT registro_tiempo_id, fecha, horas_trabajadas, descripcion_tareas, empleado_id, proyecto_id
                              FROM registro_tiempo
                              WHERE registro_tiempo_id = %s''', (registro_tiempo.registro_tiempo_id,))
            fila: tuple[Any,...] | None = cursor.fetchone()
            if fila is None: return None
            return RegistroTiempo(registro_tiempo_id=fila[0], fecha=fila[1], horas_trabajadas=fila[2], descripcion_tareas=fila[3], id_empleado=fila[4], id_proyecto=fila[5])

    def actualizar(self, registro_tiempo: RegistroTiempo) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''UPDATE registro_tiempo
                              SET fecha = %s, horas_trabajadas = %s, descripcion_tareas = %s, empleado_id = %s, proyecto_id = %s
                              WHERE registro_tiempo_id = %s''',
                           (registro_tiempo.fecha, registro_tiempo.horas_trabajadas, registro_tiempo.descripcion_tareas, registro_tiempo.empleado_id, registro_tiempo.proyecto_id, registro_tiempo.registro_tiempo_id))
            conexion.commit()

    def eliminar(self, registro_tiempo: RegistroTiempo) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM registro_tiempo WHERE registro_tiempo_id = %s', (registro_tiempo.registro_tiempo_id,))
            conexion.commit()