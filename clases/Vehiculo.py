from datetime import date

class Vehiculo:
    def __init__(
        self,
        vehiculo_id: int | None = None,
        modelo: str | None = None,
        patente: str | None = None,
        tipo: str | None = None,
        fecha_adquisicion: date | None = None,
    )-> None:
        self.vehiculo_id = vehiculo_id
        self.modelo = modelo
        self.patente = patente
        self.tipo = tipo
        self.fecha_adquisicion = fecha_adquisicion