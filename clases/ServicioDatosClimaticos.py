import os
import requests
import logging
from utilidades import validar_y_convertir_fecha
from datetime import date

def obtener_datos_climaticos(fecha: str, ciudad: str):
    try:
        token = os.getenv('TOKEN_CLIMA')
        if not token:
            raise ValueError("La variable TOKEN_CLIMA no está configurada.")
        if not ciudad.strip():
            raise ValueError("No se ha ingresado ninguna ciudad. Intente nuevamente.")
        if not validar_y_convertir_fecha(fecha):
            raise ValueError("Se ha ingresado una fecha inválida. La fecha debe estar en formato YYYY-MM-DD o DD-MM-YYYY.")
        hoy = date.today()
        #Verificación generada con IA para evaluar el requisito de la API Forecast de Weather API: Sólo evalúa fechas dentro de los próximos 14 días.
        if not 0 <= (validar_y_convertir_fecha(fecha) - hoy).days <= 14:
            raise ValueError("La fecha ingresada debe estar dentro de los próximos 14 días.")
        fecha_api = validar_y_convertir_fecha(fecha).strftime("%Y-%m-%d")
        url = 'https://api.weatherapi.com/v1/forecast.json'
        respuesta = requests.get(url,
                      params={'key': token,
                              'q': ciudad,
                              'days': 1,
                              'dt': fecha_api,
                              'lang': 'es'},
                      timeout=8)
        respuesta.raise_for_status()
        datos = respuesta.json()
        if not datos or datos["location"]["name"] != ciudad.strip():
            print("La búsqueda no ha arrojado resultados. Verifique que la ciudad ingresada sea correcta.")
            return None
        localidad = datos["location"]["name"]
        pais = datos["location"]["country"]
        clima = datos["forecast"]["forecastday"][0]["day"]["condition"]["text"]
        temperatura = datos["forecast"]["forecastday"][0]["day"]["avgtemp_c"]
        humedad_relativa = datos["forecast"]["forecastday"][0]["day"]["avghumidity"]
        velocidad_viento = datos["forecast"]["forecastday"][0]["day"]["maxwind_kph"]
        #print(f"{localidad}, {pais}, {clima}, {temperatura} °C, {humedad_relativa}%, {velocidad_viento} km/h")
        return clima, temperatura, humedad_relativa, velocidad_viento

    #Propagar la excepción a la capa de interfaz de usuario para mostrar el mensaje en pantalla.
    except ValueError as e:
        logging.exception(e)
        raise

    #Considerar refactorizar estos bloques de excepción en una sola función.
    except requests.exceptions.JSONDecodeError as e:
        mensaje = "La respuesta a la consulta fue recibida con un formato inválido."
        logging.exception(mensaje)
        raise Exception(mensaje) from e

    except requests.exceptions.ConnectionError as e:
        mensaje = "Hubo un error al establecer la conexión con el servicio externo."
        logging.exception(mensaje)
        raise Exception(mensaje) from e

    except requests.exceptions.Timeout as e:
        mensaje = "Se agotó el tiempo de espera para la conexión con el servicio externo."
        logging.exception(mensaje)
        raise Exception(mensaje) from e

    #Bloque except generado con IA.
    except requests.exceptions.HTTPError as e:
        codigo_estado = e.response.status_code
        if codigo_estado in (401, 403):
            mensaje = "Error de autenticación. Por favor verifica que tu clave API sea válida."
        elif codigo_estado >= 500:
            mensaje = "El servidor que proporciona el servicio está experimentando problemas. Inténtalo más tarde."
        else:
            mensaje = f"No se pudo realizar la conversión (Error {codigo_estado}). Revisa los datos ingresados."
        logging.exception(f"Error HTTP {codigo_estado} detectado. Respuesta del servidor: {e.response.text}")
        raise Exception(mensaje) from e

    except Exception as e:
        mensaje = "Ha ocurrido un error inesperado. Inténtelo más tarde."
        logging.exception(mensaje)
        raise Exception(mensaje) from e