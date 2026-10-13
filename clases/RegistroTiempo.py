from datetime import date

class RegistroTiempo:
    def __init__(self, id_registro_tiempo, fecha, horas_trabajadas, descripcion_tareas, id_empleado, id_proyecto):
        self.registro_tiempo_id = id_registro_tiempo
        self.fecha = fecha
        self.horas_trabajadas = horas_trabajadas
        self.descripcion_tareas = descripcion_tareas
        self.empleado_id = id_empleado
        self.proyecto_id = id_proyecto

    def obtener_resumen(self):
        pass