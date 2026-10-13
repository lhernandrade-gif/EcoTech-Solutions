from clases import Empleado

class Departamento:
    def __init__(
            self,
            departamento_id: int | None = None,
            nombre: str | None = None,
            gerente: int | None = None,
            lista_empleados: list[int] | None = None,
    ) -> None:
        self.departamento_id = departamento_id
        self.nombre = nombre
        self.gerente = gerente
        self.lista_empleados = lista_empleados

    def asignar_empleado(self, empleado: Empleado) -> None:
        pass

    def reasignar_empleado(self, empleado: Empleado, departamento: Departamento) -> None:
        pass

