import hashlib
from utilidades import validar_nombre_usuario
from utilidades import validar_password_usuario

class Usuario:
    def __init__(
        self,
        nombre_usuario: str,
        password_usuario: str
    ) -> None:
        self.nombre_usuario = nombre_usuario
        self.password_hash = hashlib.sha256(password_usuario.encode('utf-8')).hexdigest()