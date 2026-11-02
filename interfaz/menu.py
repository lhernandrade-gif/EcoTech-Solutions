import tkinter as tk
from tkinter import ttk


def construir_menu(app):
    contenedor = ttk.Frame(app.root, padding=18)
    contenedor.pack(fill="both", expand=True)

    encabezado = ttk.Label(
        contenedor, text="Gestor de EcoTech", style="Titulo.TLabel"
    )
    encabezado.pack(anchor="w", pady=(0, 18))

    zona = ttk.Frame(contenedor, padding=18, relief="groove")
    zona.pack(fill="both", expand=True)

    zona.columnconfigure(0, weight=1)
    zona.columnconfigure(1, weight=1)
    zona.rowconfigure(0, weight=1)
    zona.rowconfigure(1, weight=1)
    zona.rowconfigure(2, weight=1)

    ttk.Button(
        zona, text="Ingresar Nuevo", style="Accion.TButton",
        command=app.abrir_ingresar
    ).grid(row=0, column=0, padx=20, pady=12)

    ttk.Button(
        zona, text="Buscar por ID", style="Accion.TButton",
        command=app.abrir_buscar
    ).grid(row=0, column=1, padx=20, pady=12)

    ttk.Button(
        zona, text="Actualizar", style="Accion.TButton",
        command=app.abrir_actualizar
    ).grid(row=1, column=0, padx=20, pady=12)

    ttk.Button(
        zona, text="Eliminar", style="Accion.TButton",
        command=app.abrir_eliminar
    ).grid(row=1, column=1, padx=20, pady=12)

    # ttk.Button(
    #     zona, text="Generar Informe", style="Accion.TButton",
    #     command=app.abrir_informe
    # ).grid(row=2, column=0, columnspan=2, padx=20, pady=12)

    app.log_var = tk.StringVar(value="LOG: Programa inicializado con éxito.")
    barra = ttk.Label(
        contenedor, textvariable=app.log_var, relief="sunken",
        anchor="w", style="Estado.TLabel"
    )
    barra.pack(fill="x", pady=(10, 0))
