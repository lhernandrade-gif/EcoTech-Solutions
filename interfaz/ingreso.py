import tkinter as tk
from tkinter import ttk

import pymysql

from .configuracion import ENTIDADES, CLASES, REPOSITORIOS, sesion_actual


def abrir_ingresar(app):
    ventana = app._nueva_ventana("Ingresar nuevo registro")
    marco = ttk.Frame(ventana, padding=18)
    marco.pack(fill="both", expand=True)

    entidad = tk.StringVar(value="Empleados")
    ttk.Label(marco, text="Ingresar nuevo registro", font=("Segoe UI", 14)).pack(
        anchor="w", pady=(0, 12)
    )
    app._selector_entidad(marco, entidad, lambda: dibujar_campos())

    area = ttk.Frame(marco)
    area.pack(fill="both", expand=True)

    entradas = {}

    def dibujar_campos():
        for widget in area.winfo_children():
            widget.destroy()
        entradas.clear()
        for etiqueta, atributo in ENTIDADES[entidad.get()]:
            fila = ttk.Frame(area)
            fila.pack(fill="x", pady=4)
            ttk.Label(fila, text=etiqueta, width=32, wraplength=210).pack(side="left")
            entrada = ttk.Entry(fila)
            entrada.pack(side="left", fill="x", expand=True)
            entradas[atributo] = entrada

    def guardar_visual():
        datos_finales = {}
        for atributo, entrada in entradas.items():
            if entrada.get() == "":
                datos_finales[atributo] = [None,]
            else:
                datos_finales[atributo] = entrada.get()
        clase = CLASES[entidad.get()]
        objeto = clase(**datos_finales)
        clase_repositorio = REPOSITORIOS[entidad.get()]
        objeto_repositorio = clase_repositorio(sesion_actual)
        try:
            objeto_repositorio.guardar(objeto)
            app.registrar_log(
                f"Información guardada con éxito."
            )
        except pymysql.err.IntegrityError as e:
            app.registrar_log(
                f"ERROR: Código de excepción: {e}"
            )
        except pymysql.MySQLError as e:
            app.registrar_log(
                f"Error en la ejecución: {e}"
            )

    dibujar_campos()
    ttk.Button(
        marco, text="Guardar", command=guardar_visual
    ).pack(anchor="e", pady=(12, 0))
