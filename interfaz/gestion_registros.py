import tkinter as tk
from tkinter import ttk, messagebox

import pymysql
import utilidades

from .configuracion import ENTIDADES, IDS, CLASES, REPOSITORIOS, sesion_actual


def abrir_buscar(app):
    _abrir_formulario_id(app, "Buscar por ID", "Buscar", "buscar")


def abrir_actualizar(app):
    _abrir_formulario_id(app, "Actualizar registro", "Cargar / actualizar", "actualizar")


def abrir_eliminar(app):
    _abrir_formulario_id(app, "Eliminar registro", "Eliminar", "eliminar")


def _abrir_formulario_id(app, titulo, texto_boton, accion):
    ventana = app._nueva_ventana(titulo, "560x560")
    marco = ttk.Frame(ventana, padding=18)
    marco.pack(fill="both", expand=True)

    ttk.Label(marco, text=titulo, font=("Segoe UI", 14)).pack(
        anchor="w", pady=(0, 12)
    )
    entidad = tk.StringVar(value="Empleados")
    app._selector_entidad(marco, entidad, lambda: dibujar_campos())

    fila_id = ttk.Frame(marco)
    fila_id.pack(fill="x", pady=(0, 12))
    etiqueta_id = ttk.Label(
        fila_id, text=f"ID ({IDS[entidad.get()]}):", width=32
    )
    etiqueta_id.pack(side="left")
    id_var = tk.StringVar()
    ttk.Entry(fila_id, textvariable=id_var).pack(
        side="left", fill="x", expand=True
    )

    area = ttk.Frame(marco)
    area.pack(fill="both", expand=True)
    entradas = {}

    def dibujar_campos():
        etiqueta_id.config(text=f"ID ({IDS[entidad.get()]}):")
        for widget in area.winfo_children():
            widget.destroy()
        entradas.clear()
        if accion == "buscar" or accion == "eliminar":
            ttk.Label(
                area,
                text=("Se mostrarán aquí los datos encontrados."
                      if accion == "buscar"
                      else "Confirma el ID antes de eliminar el registro."),
                wraplength=450
            ).pack(anchor="w", pady=8)
            return
        for etiqueta, atributo in ENTIDADES[entidad.get()]:
            fila = ttk.Frame(area)
            fila.pack(fill="x", pady=4)
            ttk.Label(
                fila, text=etiqueta, width=32, wraplength=210
            ).pack(side="left")
            entrada = ttk.Entry(fila)
            entrada.pack(side="left", fill="x", expand=True)
            entradas[atributo] = entrada

    def ejecutar():
        datos_finales = {}
        clase = CLASES[entidad.get()]
        objeto = clase(**datos_finales)
        clase_repositorio = REPOSITORIOS[entidad.get()]
        objeto_repositorio = clase_repositorio(sesion_actual)

        if accion == "buscar":
            try:
                datos_finales = {}
                datos_finales[IDS[entidad.get()]] = id_var.get()
                print(datos_finales)
                clase = CLASES[entidad.get()]
                objeto = clase(**datos_finales)
                clase_repositorio = REPOSITORIOS[entidad.get()]
                objeto_repositorio = clase_repositorio(sesion_actual)
                app.registrar_log(
                    f"Búsqueda visual preparada para {entidad.get()} ID {id_var.get()}; lógica pendiente."
                )
                objeto = objeto_repositorio.buscar_por_id(objeto)
                messagebox.showinfo(
                    'Resultados de Búsqueda por ID',
                    f'{utilidades.mostrar_datos(objeto)}'
                )
            except pymysql.MySQLError as e:
                # Capturar fallos de MySQL (ej. tabla no existe, error de sintaxis)
                app.registrar_log(f"Error en la ejecución: {e}")

        elif accion == "actualizar":
            datos_finales = {}
            for atributo, entrada in entradas.items():
                if entrada.get() == "":
                    datos_finales[atributo] = [None, ]
                else:
                    datos_finales[atributo] = entrada.get()
            datos_finales[IDS[entidad.get()]] = int(id_var.get())
            clase = CLASES[entidad.get()]
            objeto = clase(**datos_finales)
            clase_repositorio = REPOSITORIOS[entidad.get()]
            objeto_repositorio = clase_repositorio(sesion_actual)
            utilidades.mostrar_datos(objeto)
            app.registrar_log(
                f"Actualización visual preparada para {entidad.get()} ID {id_var.get()}."
            )
            try:
                objeto_repositorio.actualizar(objeto)
                app.registrar_log(
                    f"Actualizado con éxito."
                )
            except pymysql.err.IntegrityError as e:
                app.registrar_log(
                    f"ERROR: Código de excepción: {e}"
                )
            except pymysql.MySQLError as e:
                app.registrar_log(
                    f"Error en la ejecución: {e}"
                )

        else:
            try:
                datos_finales = {}
                datos_finales[IDS[entidad.get()]] = int(id_var.get())
                print(datos_finales)
                clase = CLASES[entidad.get()]
                objeto = clase(**datos_finales)
                clase_repositorio = REPOSITORIOS[entidad.get()]
                objeto_repositorio = clase_repositorio(sesion_actual)
                app.registrar_log(
                    f"Eliminación visual preparada para {entidad.get()} ID {id_var.get()}."
                )
                objeto_repositorio.eliminar(objeto)
                app.registrar_log(
                    f"Borrado con éxito."
                )
            except pymysql.MySQLError as e:
                # Capturar fallos de MySQL (ej. tabla no existe, error de sintaxis)
                app.registrar_log(f"Error en la ejecución: {e}")

    dibujar_campos()
    ttk.Button(
        marco, text=texto_boton, command=ejecutar
    ).pack(anchor="e", pady=(12, 0))
