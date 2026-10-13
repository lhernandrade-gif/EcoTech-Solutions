from datetime import date

class RegistroTiempo:
    def __init__(self, registro_tiempo_id = None, fecha = None, horas_trabajadas = None, descripcion_tareas = None, id_empleado = None, id_proyecto = None):
        self.registro_tiempo_id = registro_tiempo_id
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion_tareas = descripcion_tareas
        self.empleado_id = id_empleado
        self.proyecto_id = id_proyecto

    def obtener_resumen(self):
        pass