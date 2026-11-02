import os
from dotenv import load_dotenv
from datetime import date

import clases
from clases import *


load_dotenv()
sesion_actual = clases.BaseDatos(
    os.getenv("DB_HOST"),
    os.getenv("DB_USER"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_NAME")
)


ENTIDADES = {
    "Empleados": [
        ("Primer nombre", "primer_nombre"),
        ("Segundo nombre", "segundo_nombre"),
        ("Primer apellido", "primer_apellido"),
        ("Segundo apellido", "segundo_apellido"),
        ("RUT", "rut"),
        ("Dirección", "direccion"),
        ("Teléfono", "telefono"),
        ("Email", "email"),
        ("Fecha de inicio de contrato (AAAA-MM-DD)", "fecha_inicio_contrato"),
        ("Salario", "salario"),
    ],
    "Departamentos": [
        ("Nombre", "nombre"),
        ("ID del gerente (opcional)", "gerente"),
        ("IDs de empleados (separados por coma)", "lista_empleados"),
    ],
    "Proyectos": [
        ("Nombre", "nombre"),
        ("Descripción", "descripcion"),
        ("Fecha del proyecto (AAAA-MM-DD)", "fecha_proyecto"),
        ("IDs de empleados (separados por coma)", "lista_empleados"),
    ],
    "Registros de tiempo": [
        ("Fecha (AAAA-MM-DD)", "fecha"),
        ("Horas trabajadas", "horas_trabajadas"),
        ("Descripción de tareas", "descripcion_tareas"),
        ("ID del empleado", "empleado_id"),
        ("ID del proyecto", "proyecto_id"),
    ],
}


IDS = {
    "Empleados": "empleado_id",
    "Departamentos": "departamento_id",
    "Proyectos": "proyecto_id",
    "Registros de tiempo": "registro_tiempo_id",
}


CLASES = {
    "Empleados": Empleado,
    "Departamentos": Departamento,
    "Proyectos": Proyecto,
    "Registros de tiempo": RegistroTiempo,
}


REPOSITORIOS = {
    "Empleados": EmpleadoRepositorio,
    "Departamentos": DepartamentoRepositorio,
    "Proyectos": ProyectoRepositorio,
    "Registros de tiempo": RegistroTiempoRepositorio,
}
