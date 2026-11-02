import tkinter as tk
from tkinter import ttk

from . import menu
from .configuracion import ENTIDADES


class EcoTechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de EcoTech")
        self.root.geometry("760x480")
        self.root.minsize(680, 440)

        self._configurar_estilos()
        self._construir_menu()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("vista" if "vista" in estilo.theme_names() else "clam")
        except tk.TclError:
            pass
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 17))
        estilo.configure("Accion.TButton", font=("Segoe UI", 11), padding=(12, 8))
        estilo.configure("Estado.TLabel", padding=(8, 5))

    def _construir_menu(self):
        menu.construir_menu(self)

    def registrar_log(self, mensaje):
        """Actualiza la barra de estado inferior."""
        self.log_var.set(f"[LOG] {mensaje}")

    def _nueva_ventana(self, titulo, geometria="560x520"):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry(geometria)
        ventana.minsize(460, 360)
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
