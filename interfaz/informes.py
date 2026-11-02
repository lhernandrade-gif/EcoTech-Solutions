import tkinter as tk
from tkinter import ttk


def abrir_informe(app):
    ventana = app._nueva_ventana("Generar informe", "500x260")
    marco = ttk.Frame(ventana, padding=18)
    marco.pack(fill="both", expand=True)
    ttk.Label(
        marco, text="Generar informe", font=("Segoe UI", 14)
    ).pack(anchor="w", pady=(0, 14))

    entidad = tk.StringVar(value="Empleados")
    app._selector_entidad(marco, entidad, lambda: None)

    ttk.Label(
        marco,
        text="La vista o archivo del informe se implementará al conectar los repositorios.",
        wraplength=430
    ).pack(anchor="w", pady=12)

    def generar():
        # PENDIENTE: consultar el repositorio seleccionado y mostrar/exportar el informe.
        app.registrar_log(
            f"Informe de {entidad.get()} solicitado; lógica pendiente de implementar."
        )

    ttk.Button(
        marco, text="Generar", command=generar
    ).pack(anchor="e", pady=(8, 0))
