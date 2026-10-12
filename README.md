## Prerrequisitos

Antes de ejecutar esta aplicación, debes tener **MySQL Server** instalado y ejecutándose en tu computador.

### 1. Instalar MySQL Server
* **Windows:** Descarga y ejecuta el [Instalador de MySQL](https://mysql.com)
* **macOS:** Instálalo a través de Homebrew con el comando: `brew install mysql`
* **Linux (Ubuntu/Debian):** Ejecuta en el terminal: `sudo apt update && sudo apt install mysql-server`

### 2. Configurar la Base de Datos
1. Asegúrate de que el servicio de MySQL se esté ejecutando.
2. Crea una nueva base de datos para este proyecto:
   ```sql
   CREATE DATABASE mi_proyecto_db
    CHARACTER SET utf8mb4 -- Establece compatibilidad extendida con caracteres Unicode
    COLLATE utf8mb4_0900_ai_ci; -- Esta línea permite comparar valores sin importar las tildes o capitalización (por ej. un usuario que busca "jose" puede encontrar "José")

   USE mi_proyecto_db;
   ```

### 3. Configuración del Entorno
Crea un archivo llamado `.env` en el directorio raíz del proyecto y agrega las credenciales de tu base de datos:
```env
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=mi_proyecto_db
```