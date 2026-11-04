from typing import Any
from .Usuario import Usuario
from .BaseDatos import BaseDatos

class UsuarioRepositorio:
    def __init__(self, sesion: BaseDatos) -> None:
        self.config: BaseDatos = sesion

    def buscar_por_nombre_usuario(self, usuario: Usuario) -> Usuario | None:
        with self.config.conectar() as conexion:
            cursor = conexion.cursor()
            cursor.execute('''SELECT nombre_usuario, password_hash
                              FROM usuarios
                              WHERE nombre_usuario = %s''', (usuario.nombre_usuario,))
            fila: tuple[Any, ...] | None = cursor.fetchone()
            if fila is None: return None
            return Usuario(
                nombre_usuario=fila[0],
                password_hash=fila[1]
            )