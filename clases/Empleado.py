import logging
from datetime import date
from clases import RegistroTiempo
from utilidades import validar_rut
from utilidades import validar_y_convertir_fecha

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
        try:
            self.empleado_id = empleado_id
            self.primer_nombre = primer_nombre
            self.segundo_nombre = segundo_nombre
            self.primer_apellido = primer_apellido
            self.segundo_apellido = segundo_apellido
            if rut != None:
                if not validar_rut(rut):
                    # Se debe añadir el try/except que maneja la excepción en la capa de interfaz de usuario.
                    raise ValueError("Se ha ingresado un RUT inválido. Por favor verifique los datos e inténtelo nuevamente.")
            self.rut = validar_rut(rut)
            self.direccion = direccion
            self.telefono = telefono
            self.email = email
            if fecha_inicio_contrato != None:
                if not validar_y_convertir_fecha(fecha_inicio_contrato):
                    # Se debe añadir el try/except que maneja la excepción en la capa de interfaz de usuario.
                    raise ValueError("Se ha ingresado una fecha en formato inválido. Por favor ingrese una fecha en formato DD-MM-YYYY o YYYY-MM-DD.")
            self.fecha_inicio_contrato = validar_y_convertir_fecha(fecha_inicio_contrato)
            self.salario = salario
        except ValueError as e:
            logging.exception(e)
            raise

    def obtener_datos_contacto(self) -> dict:
        pass

    def registrar_horas(self, registro: RegistroTiempo) -> None:
        pass