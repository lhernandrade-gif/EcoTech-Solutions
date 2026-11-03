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
                      params={'have': moneda_base, 'want': moneda_intercambio, 'amount': monto})
        respuesta.raise_for_status()
        datos = respuesta.json()
        print(datos.get('new_amount'))
        return datos.get('new_amount')

    #Propagar la excepción a la capa de interfaz de usuario para mostrar el mensaje en pantalla.
    except ValueError as e:
        print("Llegaste aquí.")
        logging.exception(e)
        raise






