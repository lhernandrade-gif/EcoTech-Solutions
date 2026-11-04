import pymysql
from tkinter import messagebox


def texto_error(error):
    return str(error).strip() or type(error).__name__


def titulo_error(error):
    if isinstance(error, pymysql.MySQLError):
        return "Error de base de datos"
    if isinstance(error, (ValueError, TypeError)):
        return "Revisa los datos"
    return "No se pudo completar la operación"


def mostrar_error(parent, error):
    messagebox.showerror(
        titulo_error(error), texto_error(error), parent=parent
    )
