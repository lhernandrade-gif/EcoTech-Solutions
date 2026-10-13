from datetime import date

class Proyecto:
    def __init__(
        self,
        proyecto_id: int | None = None,
        nombre: str | None = None,
        descripcion: str | None = None,
        fecha_proyecto: date | None = None,
        lista_empleados: list[int] | None = None

    )-> None:
        self.proyecto_id = proyecto_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_proyecto = fecha_proyecto
        self.lista_empleados = lista_empleados





