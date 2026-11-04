import tkinter as tk
from tkinter import ttk


def construir_menu(app):
    contenedor = ttk.Frame(app.root, padding=(42, 30, 42, 22))
    contenedor.pack(fill="both", expand=True)

    ttk.Label(
        contenedor, text="ECOTECH  /  OPERACIONES", font=("Segoe UI", 9, "bold"),
        foreground="#528064"
    ).pack(anchor="w", pady=(0, 8))
    ttk.Label(
        contenedor, text="Gestión de equipo y proyectos", style="Titulo.TLabel"
    ).pack(anchor="w")
    ttk.Label(
        contenedor,
        text="Administra empleados, departamentos, proyectos y horas de trabajo.",
        style="Subtitulo.TLabel"
    ).pack(anchor="w", pady=(8, 24))

    ttk.Label(contenedor, text="¿Qué necesitas hacer?", style="Seccion.TLabel").pack(
        anchor="w", pady=(0, 12)
    )
    zona = ttk.Frame(contenedor)
    zona.pack(fill="both", expand=True)

    zona.columnconfigure(0, weight=1)
    zona.columnconfigure(1, weight=1)
    zona.rowconfigure(0, weight=1)
    zona.rowconfigure(1, weight=1)

    ttk.Button(
        zona, text="＋   Ingresar nuevo registro", style="Accion.TButton",
        command=app.abrir_ingresar
    ).grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

    ttk.Button(
        zona, text="⌕   Buscar por ID", style="Accion.TButton",
        command=app.abrir_buscar
    ).grid(row=0, column=1, padx=8, pady=8, sticky="nsew")

    ttk.Button(
        zona, text="↻   Actualizar registro", style="Accion.TButton",
        command=app.abrir_actualizar
    ).grid(row=1, column=0, padx=8, pady=8, sticky="nsew")

    ttk.Button(
        zona, text="−   Eliminar registro", style="Accion.TButton",
        command=app.abrir_eliminar
    ).grid(row=1, column=1, padx=8, pady=8, sticky="nsew")

    app.log_var = tk.StringVar(value="LOG: Programa inicializado con éxito.")
    barra = ttk.Label(
        contenedor, textvariable=app.log_var, relief="sunken",
        anchor="w", style="Estado.TLabel"
    )
    barra.pack(fill="x", pady=(10, 0))
