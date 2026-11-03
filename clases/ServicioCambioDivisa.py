import os
import requests
import logging
from utilidades import validar_monto

#Nota: No será necesario validar códigos de moneda ya que se usará un combobox con constantes predefinidas.

def cambio_divisa(monto: str):
    try:
        token = os.getenv('TOKEN_DIVISAS')
        if not token:
            raise ValueError("La variable TOKEN_DIVISAS no está configurada.")
        if not validar_monto(monto):
            raise ValueError("Se ha ingresado un monto inválido.")
        url = 'https://api.api-ninjas.com/v1/convertcurrency'
        moneda_base = 'CLP'
        moneda_intercambio = 'USD'
        respuesta = requests.get(url,
                      headers={'X-Api-Key': token},
                      params={'have': moneda_base, 'want': moneda_intercambio, 'amount': monto},
                      timeout=8)
        respuesta.raise_for_status()
        datos = respuesta.json()
        print(datos.get('new_amount'))
        return datos.get('new_amount')

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

    #Bloque except generado con IA. Revisar y validar.
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








