from datetime import date

class RegistroTiempo:
    def __init__(self, registro_tiempo_id = None,
                 fecha = None,
                 horas_trabajadas = None,
                 descripcion_tareas = None,
                 empleado_id = None,
                 proyecto_id = None):
        self.registro_tiempo_id = registro_tiempo_id
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion_tareas = descripcion_tareas
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id

    def obtener_resumen(self):
        pass