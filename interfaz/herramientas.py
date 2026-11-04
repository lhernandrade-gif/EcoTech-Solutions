from tkinter import ttk


def abrir_herramientas(app):
    ventana = app._nueva_ventana("Herramientas", "640x440")
    contenedor = ttk.Frame(ventana, padding=(32, 26))
    contenedor.pack(fill="both", expand=True)

    ttk.Label(
        contenedor, text="Conversión de Divisas", style="Seccion.TLabel"
    ).pack(anchor="w", pady=(0, 10))
    ttk.Frame(contenedor).pack(fill="both", expand=True)

    ttk.Separator(contenedor, orient="horizontal").pack(fill="x", pady=12)

    ttk.Label(
        contenedor, text="Consulta de Datos Climáticos", style="Seccion.TLabel"
    ).pack(anchor="w", pady=(0, 10))
    ttk.Frame(contenedor).pack(fill="both", expand=True)