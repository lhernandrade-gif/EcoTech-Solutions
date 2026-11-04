## Prerrequisitos

Antes de ejecutar esta aplicación, debes tener **MySQL Server** instalado y ejecutándose en tu computador.

### 1. Instalar MySQL Server
* **Windows:** Descarga y ejecuta el [Instalador de MySQL](https://mysql.com)
* **macOS:** Instálalo a través de Homebrew con el comando: `brew install mysql`
* **Linux (Ubuntu/Debian):** Ejecuta en el terminal: `sudo apt update && sudo apt install mysql-server`

### 2. Configurar la Base de Datos
1. Asegúrate de que el servicio de MySQL se esté ejecutando.
2. Ejecuta en MySQL el script `schema.sql`. Esto creará la base de datos del programa e insertará valores de prueba.

### 3. Configuración del Entorno
Crea un archivo llamado `.env` en el directorio raíz del proyecto y agrega las credenciales de tu base de datos:
```env
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=ecotech
```

### 4. Configuración de Claves API (API Keys)
Visita https://api-ninjas.com/api/convertcurrency y obtén una API Key para Currency Conversion API. Añádela en `.env` como:
```env
TOKEN_DIVISAS=tu_clave_api
```
Visita también https://www.weatherapi.com y obtén una API Key para Weather API. Ingrésala en `.env`:
```env
TOKEN_CLIMA=tu_clave_api
```

### 5. Instalar dependencias
Desde el terminal, ejecutar en el directorio raíz del proyecto el comando `pip install -r requirements.txt`.

### 6. Ejecutar el programa
Desde el terminal, ejecutar en el directorio raíz del proyecto el comando `main.py`.
Para ingresar al usuario de prueba obtenido de `schema.sql`, utilice el usuario `Admin`, contraseña `@Password`.