import logging
from datetime import date
from utilidades import validar_y_convertir_fecha
from utilidades import validar_y_convertir_ingreso_ids

class Proyecto:
    def __init__(
        self,
        proyecto_id: int | None = None,
        nombre: str | None = None,
        descripcion: str | None = None,
        fecha_proyecto: str | date | None = None,
        lista_empleados: list[int] | None = None
    )-> None:
        try:
            self.proyecto_id = proyecto_id
            self.nombre = nombre
            self.descripcion = descripcion
            if fecha_proyecto != None:
                if not validar_y_convertir_fecha(fecha_proyecto):
                    # Se debe añadir el try/except que maneja la excepción en la capa de interfaz de usuario.
                    raise ValueError("Se ha ingresado una fecha en formato inválido. Por favor ingrese una fecha en formato DD-MM-YYYY o YYYY-MM-DD.")
            self.fecha_proyecto = validar_y_convertir_fecha(fecha_proyecto)
            if lista_empleados != None:
                if not validar_y_convertir_ingreso_ids(lista_empleados):
                    raise ValueError("Se han ingresado IDs inválidos. Por favor ingrese los IDs como números separados por comas sin espacios.")
            self.lista_empleados = validar_y_convertir_ingreso_ids(lista_empleados)
        except ValueError as e:
            logging.exception(e)
            raise





