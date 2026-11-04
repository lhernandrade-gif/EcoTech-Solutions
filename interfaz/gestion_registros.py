import tkinter as tk
from tkinter import ttk, messagebox

import utilidades

from .configuracion import ENTIDADES, IDS, REPOSITORIOS, crear_entidad, sesion_actual
from .errores import mostrar_error, texto_error


def abrir_buscar(app):
    _abrir_formulario_id(app, "Buscar por ID", "Buscar", "buscar")


def abrir_actualizar(app):
    _abrir_formulario_id(app, "Actualizar registro", "Actualizar", "actualizar")


def abrir_eliminar(app):
    _abrir_formulario_id(app, "Eliminar registro", "Eliminar", "eliminar")


def _abrir_formulario_id(app, titulo, texto_boton, accion):
    ventana = app._nueva_ventana(titulo, "700x650")
    marco = ttk.Frame(ventana, padding=24)
    marco.pack(fill="both", expand=True)

    ttk.Label(marco, text=titulo, style="Titulo.TLabel").pack(
        anchor="w", pady=(0, 5)
    )
    subtitulo = {
        "buscar": "Consulta los datos de un registro por su identificador.",
        "actualizar": "Completa los campos para reemplazar los datos actuales.",
        "eliminar": "La eliminación no se puede deshacer.",
    }[accion]
    ttk.Label(marco, text=subtitulo, style="Subtitulo.TLabel").pack(
        anchor="w", pady=(0, 18)
    )
    entidad = tk.StringVar(value="Empleados")
    app._selector_entidad(marco, entidad, lambda: dibujar_campos())

    fila_id = ttk.Frame(marco)
    fila_id.pack(fill="x", pady=(0, 12))
    etiqueta_id = ttk.Label(fila_id, text=f"ID ({IDS[entidad.get()]}):", width=34)
    etiqueta_id.pack(side="left")
    id_var = tk.StringVar()
    ttk.Entry(fila_id, textvariable=id_var).pack(side="left", fill="x", expand=True, ipady=4)

    area = ttk.Frame(marco)
    area.pack(fill="both", expand=True)
    entradas = {}
    resultado = tk.Text(
        marco, height=8, wrap="word", state="disabled", relief="solid",
        borderwidth=1, padx=10, pady=8, font=("TkFixedFont", 10)
    )
    if accion != "actualizar":
        resultado.pack(fill="both", expand=True, pady=(8, 0))

    def mostrar_resultado(texto):
        resultado.configure(state="normal")
        resultado.delete("1.0", tk.END)
        resultado.insert("1.0", texto)
        resultado.configure(state="disabled")

    def obtener_id():
        valor = id_var.get().strip()
        if not valor.isdigit() or int(valor) <= 0:
            raise ValueError("Ingresa un ID entero mayor que cero.")
        return int(valor)

    def dibujar_campos():
        etiqueta_id.config(text=f"ID ({IDS[entidad.get()]}):")
        for widget in area.winfo_children():
            widget.destroy()
        entradas.clear()
        if accion == "buscar" or accion == "eliminar":
            mensaje = (
                "Los datos encontrados aparecerán aquí."
                if accion == "buscar"
                else "Se pedirá confirmación antes de eliminar el registro."
            )
            ttk.Label(
                area, text=mensaje, style="Subtitulo.TLabel", wraplength=520
            ).pack(anchor="w", pady=8)
            return
        for etiqueta, atributo in ENTIDADES[entidad.get()]:
            fila = ttk.Frame(area)
            fila.pack(fill="x", pady=5)
            ttk.Label(
                fila, text=etiqueta, width=34, wraplength=240
            ).pack(side="left", anchor="w")
            entrada = ttk.Entry(fila)
            entrada.pack(side="left", fill="x", expand=True, ipady=4)
            entradas[atributo] = entrada

    def ejecutar():
        try:
            registro_id = obtener_id()
            repositorio = REPOSITORIOS[entidad.get()](sesion_actual)
            if accion == "buscar":
                objeto = crear_entidad(entidad.get(), {}, registro_id)
                encontrado = repositorio.buscar_por_id(objeto)
                texto = utilidades.mostrar_datos(encontrado)
                mostrar_resultado(texto or "No existen resultados para esta búsqueda.")
                app.registrar_log(f"Consulta de {entidad.get()} ID {registro_id} completada.")
            elif accion == "actualizar":
                valores = {atributo: entrada.get() for atributo, entrada in entradas.items()}
                objeto = crear_entidad(entidad.get(), valores, registro_id)
                repositorio.actualizar(objeto)
                app.registrar_log(f"Registro {entidad.get()} ID {registro_id} actualizado.")
                messagebox.showinfo("Registro actualizado", "La información se actualizó correctamente.", parent=ventana)
            else:
                if not messagebox.askyesno(
                    "Confirmar eliminación",
                    f"¿Eliminar {entidad.get().lower()} con ID {registro_id}? Esta acción no se puede deshacer.",
                    parent=ventana
                ):
                    return
                objeto = crear_entidad(entidad.get(), {}, registro_id)
                repositorio.eliminar(objeto)
                app.registrar_log(f"Registro {entidad.get()} ID {registro_id} eliminado.")
                mostrar_resultado("Registro eliminado correctamente.")
        except Exception as error:
            app.registrar_log(f"Error en operación: {texto_error(error)}")
            mostrar_error(ventana, error)

    dibujar_campos()
    ttk.Button(
        marco, text=texto_boton, style="Accion.TButton", command=ejecutar
    ).pack(anchor="e", pady=(12, 0))
