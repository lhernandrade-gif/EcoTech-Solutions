from datetime import date
from clases import RegistroTiempo

class Empleado:
    def __init__(
            self,
            primer_nombre: str | None = None,
            primer_apellido: str | None = None,
            segundo_apellido: str | None = None,
            rut: str | None = None,
            email: str | None = None,
            segundo_nombre: str | None = None,
            empleado_id: int | None = None,
            direccion: str | None = None,
            telefono: str | None = None,
            fecha_inicio_contrato: date | None = None,
            salario: int | None = None
    ) -> None:
        self.empleado_id = empleado_id
        self.primer_nombre = primer_nombre
        self.segundo_nombre = segundo_nombre
        self.primer_apellido = primer_apellido
        self.segundo_apellido = segundo_apellido
        self.rut = rut
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario

    def obtener_datos_contacto(self) -> dict:
        pass

    def registrar_horas(self, registro: RegistroTiempo) -> None:
        pass