from datetime import date, datetime
#Decimal se utiliza en aplicaciones financieras por su mayor precisión en comparación con float.
from decimal import Decimal, InvalidOperation
import string #Utilizar para el método string.punctuation en validar_contrasena

def mostrar_datos(objeto) -> str | None:
    if not objeto:
        return "No existen resultados para esta búsqueda."
    lista = []
    if isinstance(objeto, list):
        for dict in objeto:
            for clave, valor in dict.items():
                #print(f"{clave}: {valor}", end=" ")
                lista.append(f"{clave}: {valor}")
            lista.append("\n")
    else:
        for clave, valor in vars(objeto).items():
            lista.append(f"{clave}: {valor}\n")
    #print("\n".join(lista))
    return "\n".join(lista)

def validar_rut(rut: str) -> str | bool:
    rut = rut.replace(".", "").replace("-", "").strip().upper()

    if not rut:
        #print("No se han ingresado datos.")
        return False

    if not rut.isalnum():
        #print("El RUT contiene caracteres inválidos.")
        return False

    for digito in rut[:-1]:
        if not digito.isdigit():
            #print("El RUT contiene caracteres inválidos.")
            return False

    if len(rut) != 8 and len(rut) != 9:
        #print("Ingresó un RUT de longitud inválida.")
        return False

    multiplo = 2  # Valor inicial para el cálculo del múltiplo secuencial de los números del RUT
    total_verificador = 0

    for digito in reversed(rut[:-1]):
        total_verificador += int(digito) * multiplo
        multiplo += 1
        if multiplo > 7:
            multiplo = 2

    final_verificador = 11 - total_verificador % 11

    if final_verificador < 10:
        if final_verificador != int(rut[-1]):
            #print("RUT inválido. El dígito verificador para el RUT ingresado debería ser {}.".format(final_verificador))
            return False

    if final_verificador == 10:
        if str(rut[-1]) != "K":
            #print("Rut inválido. El dígito verificador para el RUT ingresado debería ser K.")
            return False

    if final_verificador == 11:
        if int(rut[-1]) != 0:
            #print("RUT inválido. El dígito verificador para el RUT ingresado debería ser 0.")
            return False

    return rut[0:-1] + "-" + rut[-1:]

def validar_nombre_usuario (nombre_usuario: str) -> bool:
    #No más de 12 caracteres alfanuméricos
    pass

def validar_contrasena(contrasena: str) -> bool:
    #Entre 8 y 14 caracteres. Debe contener al menos una mayúscula, una minúscula y un símbolo: *, #, $, @, _
    #Recomendación de IA: Usar string.punctuation, que contiene los siguientes caracteres: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    #Esta verificación de caracteres puede hacerse en una sola línea -> has_symbol = any(char in string.punctuation for char in password)
    pass

#Adaptado de código en módulos de la unidad 3
def validar_patente(patente: str) -> bool:
    return len(patente) == 6 and (patente[:2].isalpha() and patente[2:].isdigit()) or (patente[:4].isalpha() and patente[4:].isdigit())

#Función generada con IA y refactorizada para validar una fecha y devolverla en formato datetime.
def validar_y_convertir_fecha(fecha: str) -> date | bool:
    formatos = ("%Y-%m-%d", "%d-%m-%Y")
    for formato in formatos:
        try:
            return datetime.strptime(fecha, formato).date()
        except ValueError:
        #Ignorar la excepción para poder evaluar ambos formatos dentro del ciclo for en caso de que el primero falle.
        #Si se detecta una excepción ValueError, se manejará externamente con un raise, para el caso que la función retorne False.
            continue
    return False

def validar_y_convertir_ingreso_ids(ids: str) -> list | bool:
    lista_ids = ids.split(",")
    for id in lista_ids:
        if not id.isdigit():
            return False
    return lista_ids

#Validación de monto sugerida por IA. No se modificó el output.
#Pendiente añadir verificación de separador de decimales (por ej. si el usuario ingresa , en lugar de .)
def validar_monto(monto: str) -> bool:
    try:
        valor = Decimal(monto)
        return valor.is_finite() and valor >= 0
    except InvalidOperation:
        return False

def control_excepciones_api(excepcion) -> str:
    pass

def generar_informe():
    pass

def exportar_informe():
    pass


