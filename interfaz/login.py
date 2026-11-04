import hmac
import tkinter as tk
from tkinter import ttk

from clases.Usuario import Usuario
from clases.UsuarioRepositorio import UsuarioRepositorio
from .configuracion import sesion_actual
from .errores import texto_error


def autenticar_usuario(nombre_usuario, password_usuario):
    usuario = Usuario(
        nombre_usuario=nombre_usuario.strip(),
        password_usuario=password_usuario,
    )
    repositorio = UsuarioRepositorio(sesion_actual)
    usuario_guardado = repositorio.buscar_por_nombre_usuario(usuario)
    if usuario_guardado is None or not hmac.compare_digest(
        usuario.password_hash, usuario_guardado.password_hash
    ):
        raise ValueError("Nombre de usuario o contraseña incorrectos.")


def construir_login(app):
    raiz = app.root
    contenedor = ttk.Frame(raiz, padding=(42, 34))
    contenedor.pack(fill="both", expand=True)

    ttk.Label(
        contenedor, text="ECOTECH  /  OPERACIONES", font=("Segoe UI", 9, "bold"),
        foreground="#528064"
    ).pack(anchor="w", pady=(0, 10))
    ttk.Label(
        contenedor, text="Iniciar sesión", style="Titulo.TLabel"
    ).pack(anchor="w")
    ttk.Label(
        contenedor, text="Ingresa tus credenciales para continuar.",
        style="Subtitulo.TLabel"
    ).pack(anchor="w", pady=(8, 24))

    ttk.Label(contenedor, text="Nombre de usuario").pack(anchor="w", pady=(0, 5))
    nombre_var = tk.StringVar()
    nombre_entrada = ttk.Entry(contenedor, textvariable=nombre_var)
    nombre_entrada.pack(fill="x", ipady=5, pady=(0, 16))

    ttk.Label(contenedor, text="Contraseña").pack(anchor="w", pady=(0, 5))
    password_var = tk.StringVar()
    password_entrada = ttk.Entry(
        contenedor, textvariable=password_var, show="*"
    )
    password_entrada.pack(fill="x", ipady=5, pady=(0, 12))

    mensaje_var = tk.StringVar()
    ttk.Label(
        contenedor, textvariable=mensaje_var, foreground="#a33b32",
        wraplength=360
    ).pack(anchor="w", pady=(0, 10))

    def iniciar_sesion(_evento=None):
        try:
            autenticar_usuario(nombre_var.get(), password_var.get())
        except Exception as error:
            mensaje_var.set(texto_error(error))
            password_entrada.focus_set()
            password_entrada.selection_range(0, tk.END)
            return
        mensaje_var.set("")
        app.acceso_concedido()

    ttk.Button(
        contenedor, text="Ingresar", style="Accion.TButton",
        command=iniciar_sesion
    ).pack(fill="x", pady=(8, 0))
    nombre_entrada.bind("<Return>", lambda _evento: password_entrada.focus_set())
    password_entrada.bind("<Return>", iniciar_sesion)
    nombre_entrada.focus_set()
