import logging
import hashlib
from utilidades import validar_nombre_usuario
from utilidades import validar_password_usuario

class Usuario:
    def __init__(
        self,
        nombre_usuario: str,
        password_usuario: str | None = None,
        password_hash: str | None = None,
    ) -> None:
        try:
            if not nombre_usuario:
                raise ValueError("Debe ingresar un nombre de usuario.")
            if not validar_nombre_usuario(nombre_usuario):
                raise ValueError("Nombre de usuario no válido. Debe contener hasta 12 caracteres alfanuméricos.")
            self.nombre_usuario = nombre_usuario
            if not password_usuario and not password_hash:
                raise ValueError("No se ha ingresado una contraseña. Intente nuevamente.")
            if password_usuario != None:
                if not validar_password_usuario(password_usuario):
                    raise ValueError("La contraseña debe incluir entre 8 y 14 caracteres, y al menos 1 letra, 1 número y 1 símbolo.")
            if password_usuario:
                self.password_hash = hashlib.sha256(password_usuario.encode('utf-8')).hexdigest()
            else
                self.password_hash = password_hash
        except ValueError as e:
            logging.exception(e)
            raise
