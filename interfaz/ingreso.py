import tkinter as tk
from tkinter import ttk, messagebox

from .configuracion import ENTIDADES, REPOSITORIOS, crear_entidad, sesion_actual
from .errores import mostrar_error, texto_error


def abrir_ingresar(app):
    ventana = app._nueva_ventana("Ingresar nuevo registro", "700x650")
    marco = ttk.Frame(ventana, padding=24)
    marco.pack(fill="both", expand=True)

    entidad = tk.StringVar(value="Empleados")
    ttk.Label(marco, text="Nuevo registro", style="Titulo.TLabel").pack(
        anchor="w", pady=(0, 5)
    )
    ttk.Label(marco, text="Completa los datos de la entidad seleccionada.", style="Subtitulo.TLabel").pack(
        anchor="w", pady=(0, 18)
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
            fila.pack(fill="x", pady=5)
            ttk.Label(fila, text=etiqueta, width=34, wraplength=240).pack(side="left", anchor="w")
            entrada = ttk.Entry(fila)
            entrada.pack(side="left", fill="x", expand=True, ipady=4)
            entradas[atributo] = entrada

    def guardar_visual():
        try:
            datos = {atributo: entrada.get() for atributo, entrada in entradas.items()}
            objeto = crear_entidad(entidad.get(), datos)
            objeto_repositorio = REPOSITORIOS[entidad.get()](sesion_actual)
            objeto_repositorio.guardar(objeto)
            app.registrar_log(f"Registro de {entidad.get()} guardado correctamente.")
            messagebox.showinfo("Registro guardado", "La información se guardó correctamente.", parent=ventana)
            for entrada in entradas.values():
                entrada.delete(0, tk.END)
        except Exception as error:
            app.registrar_log(f"No se pudo guardar: {texto_error(error)}")
            mostrar_error(ventana, error)

    dibujar_campos()
    ttk.Button(
        marco, text="Guardar registro", style="Accion.TButton", command=guardar_visual
    ).pack(anchor="e", pady=(12, 0))
