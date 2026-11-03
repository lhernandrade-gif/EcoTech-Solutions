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
        self.vehiculo_id = vehiculo_id
        self.modelo = modelo
        if patente != None:
            if not validar_patente(patente.strip()):
                raise ValueError("Formato de patente inválido.")
        self.patente = patente.strip()
        if tipo != None:
            if tipo.upper() not in tipo_vehiculo:
                raise ValueError("Tipo de vehiculo inválido. Introducir solo caracteres alfabéticos sin tildes. Entradas válidas: Auto, SUV, camioneta, furgon, van.")
        self.tipo = tipo
        if fecha_adquisicion != None:
            if not validar_y_convertir_fecha(fecha_adquisicion):
                raise ValueError("La fecha tiene un formato inválido. Debe utilizar YYYY-MM-DD o DD-MM-YYYY.")
        self.fecha_adquisicion = validar_y_convertir_fecha(fecha_adquisicion).strftime("%Y-%m-%d")

