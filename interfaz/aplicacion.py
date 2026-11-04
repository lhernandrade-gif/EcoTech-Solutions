import tkinter as tk
from tkinter import ttk

from . import menu
from .configuracion import ENTIDADES


class EcoTechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de EcoTech")
        self.root.geometry("900x600")
        self.root.minsize(760, 520)

        self._configurar_estilos()
        self._construir_menu()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        self.root.configure(background="#f1f3ed")
        estilo.configure("TFrame", background="#f1f3ed")
        estilo.configure("TLabel", background="#f1f3ed", foreground="#26352d", font=("Segoe UI", 10))
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 25, "bold"), foreground="#183b2c")
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 11), foreground="#627168")
        estilo.configure("Seccion.TLabel", font=("Segoe UI", 12, "bold"), foreground="#183b2c")
        estilo.configure("Accion.TButton", font=("Segoe UI", 11, "bold"), padding=(18, 14), background="#1c6246", foreground="#ffffff")
        estilo.map("Accion.TButton", background=[("active", "#164c36"), ("pressed", "#123d2c")])
        estilo.configure("Secundaria.TButton", font=("Segoe UI", 10), padding=(12, 8))
        estilo.configure("Estado.TLabel", padding=(10, 7), background="#dce6dc", foreground="#34463a")

    def _construir_menu(self):
        menu.construir_menu(self)

    def registrar_log(self, mensaje):
        """Actualiza la barra de estado inferior."""
        self.log_var.set(f"[LOG] {mensaje}")

    def _nueva_ventana(self, titulo, geometria="640x600"):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry(geometria)
        ventana.minsize(520, 440)
        ventana.transient(self.root)
        return ventana

    def _selector_entidad(self, parent, variable, callback):
        fila = ttk.Frame(parent)
        fila.pack(fill="x", pady=(0, 12))
        ttk.Label(fila, text="Tabla / entidad:", width=20).pack(side="left")
        selector = ttk.Combobox(
            fila, textvariable=variable, values=list(ENTIDADES),
            state="readonly"
        )
        selector.pack(side="left", fill="x", expand=True)
        selector.bind("<<ComboboxSelected>>", lambda _evento: callback())
        return selector

    def abrir_ingresar(self):
        from .ingreso import abrir_ingresar
        abrir_ingresar(self)

    def abrir_buscar(self):
        from .gestion_registros import abrir_buscar
        abrir_buscar(self)

    def abrir_actualizar(self):
        from .gestion_registros import abrir_actualizar
        abrir_actualizar(self)

    def abrir_eliminar(self):
        from .gestion_registros import abrir_eliminar
        abrir_eliminar(self)

    def abrir_informe(self):
        from .informes import abrir_informe
        abrir_informe(self)
