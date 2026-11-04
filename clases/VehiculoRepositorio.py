#Clase generada con IA mediante la siguiente información contextual: Clase Vehiculo, tabla vehiculos en schema.sql, clase EmpleadoRepositorio.

from typing import Any
from .Vehiculo import Vehiculo
from .BaseDatos import BaseDatos


class VehiculoRepositorio:
    def __init__(self, sesion: BaseDatos) -> None:
        self.config: BaseDatos = sesion

    def guardar(self, vehiculo: Vehiculo) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''
                           INSERT INTO vehiculos (modelo, patente, tipo, fecha_adquisicion)
                           VALUES (%s, %s, %s, %s)
                           ''', (vehiculo.modelo, vehiculo.patente, vehiculo.tipo, vehiculo.fecha_adquisicion))
            conexion.commit()

    def buscar_por_id(self, vehiculo: Vehiculo) -> Vehiculo | None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT vehiculo_id, modelo, patente, tipo, fecha_adquisicion
                              FROM vehiculos
                              WHERE vehiculo_id = %s''', (vehiculo.vehiculo_id,))
            fila: tuple[Any, ...] | None = cursor.fetchone()
            if fila is None: return None
            return Vehiculo(
                vehiculo_id=fila[0],
                modelo=fila[1],
                patente=fila[2],
                tipo=fila[3],
                fecha_adquisicion=fila[4]
            )

    def actualizar(self, vehiculo: Vehiculo) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''UPDATE vehiculos
                              SET modelo = %s, patente = %s, tipo = %s, fecha_adquisicion = %s
                              WHERE vehiculo_id = %s''',
                           (vehiculo.modelo, vehiculo.patente, vehiculo.tipo, vehiculo.fecha_adquisicion, vehiculo.vehiculo_id))
            conexion.commit()

    def eliminar(self, vehiculo: Vehiculo) -> None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM vehiculos WHERE vehiculo_id = %s', (vehiculo.vehiculo_id,))
            conexion.commit()
