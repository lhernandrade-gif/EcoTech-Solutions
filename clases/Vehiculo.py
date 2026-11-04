import logging
from datetime import date
from utilidades import validar_patente
from utilidades import validar_y_convertir_fecha

tipo_vehiculo = ('AUTO', 'SUV', 'CAMIONETA', 'FURGON', 'VAN')

class Vehiculo:
    def __init__(
        self,
        vehiculo_id: int | None = None,
        modelo: str | None = None,
        patente: str | None = None,
        tipo: str | None = None,
        fecha_adquisicion: str | date | None = None,
    )-> None:
        try:
            self.vehiculo_id = vehiculo_id
            self.modelo = modelo
            if not isinstance(patente, str) or not patente.strip():
                raise ValueError("Debe ingresar una patente.")
            patente = patente.strip().upper()
            if not validar_patente(patente):
                raise ValueError("Formato de patente inválido.")
            self.patente = patente
            if tipo != None:
                if tipo.upper() not in tipo_vehiculo:
                    raise ValueError("Tipo de vehiculo inválido. Introducir solo caracteres alfabéticos sin tildes. Entradas válidas: Auto, SUV, camioneta, furgon, van.")
            self.tipo = tipo
            fecha_validada = validar_y_convertir_fecha(fecha_adquisicion)
            if fecha_adquisicion is not None and fecha_validada is False:
                raise ValueError("La fecha tiene un formato inválido. Debe utilizar YYYY-MM-DD o DD-MM-YYYY.")
            self.fecha_adquisicion = (
                fecha_validada.strftime("%Y-%m-%d") if fecha_validada else None
            )
        except ValueError as e:
            logging.exception(e)
            raise

