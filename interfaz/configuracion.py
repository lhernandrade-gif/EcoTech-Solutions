import os
from dotenv import load_dotenv
from decimal import Decimal, InvalidOperation

import clases
from clases import *
import utilidades


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
        ("Salario (CLP)", "salario_CLP"),
    ],
    "Departamentos": [
        ("Nombre", "nombre"),
        ("ID del gerente (opcional)", "gerente"),
        ("IDs de empleados (separados por coma)", "lista_empleados"),
    ],
    "Proyectos": [
        ("Nombre", "nombre"),
        ("Descripción", "descripcion"),
        ("Fecha del proyecto (AAAA-MM-DD)", "fecha_inicio_proyecto"),
        ("IDs de empleados (separados por coma)", "lista_empleados"),
    ],
    "Registros de tiempo": [
        ("Fecha (AAAA-MM-DD)", "fecha"),
        ("Horas trabajadas", "horas_trabajadas"),
        ("Descripción de tareas", "descripcion_tareas"),
        ("ID del empleado", "empleado_id"),
        ("ID del proyecto", "proyecto_id"),
    ],
    "Vehículos": [
        ("Modelo", "modelo"),
        ("Patente", "patente"),
        ("Tipo (AUTO, SUV, CAMIONETA, FURGON, VAN)", "tipo"),
        ("Fecha de adquisición (AAAA-MM-DD)", "fecha_adquisicion"),
    ],
}


IDS = {
    "Empleados": "empleado_id",
    "Departamentos": "departamento_id",
    "Proyectos": "proyecto_id",
    "Registros de tiempo": "registro_tiempo_id",
    "Vehículos": "vehiculo_id",
}


CLASES = {
    "Empleados": Empleado,
    "Departamentos": Departamento,
    "Proyectos": Proyecto,
    "Registros de tiempo": RegistroTiempo,
    "Vehículos": Vehiculo,
}


REPOSITORIOS = {
    "Empleados": EmpleadoRepositorio,
    "Departamentos": DepartamentoRepositorio,
    "Proyectos": ProyectoRepositorio,
    "Registros de tiempo": RegistroTiempoRepositorio,
    "Vehículos": VehiculoRepositorio,
}


CAMPOS_REQUERIDOS = {
    "Empleados": {"primer_nombre", "primer_apellido", "segundo_apellido", "rut", "email"},
    "Departamentos": {"nombre"},
    "Proyectos": {"nombre"},
    "Registros de tiempo": {"fecha", "horas_trabajadas", "empleado_id", "proyecto_id"},
    "Vehículos": {"fecha_adquisicion"},
}

IDS_LISTA = {"lista_empleados"}
IDS_NUMERICOS = {"gerente", "salario_CLP", "empleado_id", "proyecto_id"}


def crear_entidad(entidad, valores, registro_id=None):
    datos = {}
    for atributo, valor in valores.items():
        valor = valor.strip() if isinstance(valor, str) else valor
        if atributo in IDS_LISTA:
            if not valor:
                datos[atributo] = []
                continue
            ids = utilidades.validar_y_convertir_ingreso_ids(valor)
            if ids is False:
                raise ValueError("Los IDs deben ser números separados por comas.")
            datos[atributo] = ids
        elif valor == "" or valor is None:
            if atributo in CAMPOS_REQUERIDOS[entidad]:
                etiqueta = next((nombre for nombre, campo in ENTIDADES[entidad] if campo == atributo), atributo)
                raise ValueError(f"El campo '{etiqueta}' es obligatorio.")
            datos[atributo] = None
        elif atributo in IDS_NUMERICOS:
            try:
                datos[atributo] = int(valor)
            except (TypeError, ValueError) as error:
                raise ValueError(f"El campo '{atributo}' debe ser un número entero.") from error
            if atributo in {"gerente", "empleado_id", "proyecto_id"} and datos[atributo] <= 0:
                raise ValueError(f"El campo '{atributo}' debe ser mayor que cero.")
            if atributo == "salario_CLP" and datos[atributo] < 0:
                raise ValueError("El salario no puede ser negativo.")
        elif atributo == "horas_trabajadas":
            try:
                datos[atributo] = Decimal(valor)
            except (InvalidOperation, TypeError, ValueError) as error:
                raise ValueError("Las horas deben ser un número, por ejemplo 7.5.") from error
            if not datos[atributo].is_finite() or not 0 < datos[atributo] <= 24:
                raise ValueError("Las horas deben ser mayores que cero y no superar 24.")
        elif atributo == "tipo" and entidad == "Vehículos":
            datos[atributo] = valor.upper()
        elif atributo in {"fecha", "fecha_inicio_contrato", "fecha_inicio_proyecto", "fecha_adquisicion"}:
            fecha = utilidades.validar_y_convertir_fecha(valor)
            if fecha is False:
                raise ValueError(f"La fecha de '{atributo}' debe tener formato AAAA-MM-DD o DD-MM-AAAA.")
            datos[atributo] = fecha
        else:
            datos[atributo] = valor

    if registro_id is not None:
        datos[IDS[entidad]] = registro_id
        if entidad == "Vehículos" and "fecha_adquisicion" not in datos:
            # Vehiculo necesita fecha incluso para operaciones que solo usan el ID.
            datos["fecha_adquisicion"] = utilidades.validar_y_convertir_fecha("2000-01-01")
    return CLASES[entidad](**datos)
