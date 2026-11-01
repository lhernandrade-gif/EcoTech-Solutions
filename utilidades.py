from datetime import datetime

def mostrar_datos(objeto) -> None:
    lista = []
    if isinstance(objeto, list):
        for dict in objeto:
            for clave, valor in dict.items():
                print(f"{clave}: {valor}", end=" ")
                lista.append(f"{clave}: {valor}")
    else:
        for clave, valor in vars(objeto).items():
            lista.append(f"{clave}: {valor}\n")
    print("\n".join(lista))
    return "\n".join(lista)

def validar_rut(rut: str) -> bool:
    rut = rut.replace(".", "").replace("-", "").strip().upper()

    if not rut:
        #print("No se han ingresado datos.")
        return False

    if not rut.isalnum():
        #print("El RUT contiene caracteres inválidos.")
        return False

    for digito in rut[:-1]:
        if digito.isalpha():
            #print("El RUT contiene caracteres inválidos.")
            return False

    if len(rut) != 8 and len(rut) != 9:
        #print("Ingresó un rut de longitud inválida.")
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

    return True

def validar_contraseña(contraseña: str) -> bool:
    pass

def validar_patente(patente: str) -> bool:
    pass

#Función modificada con IA para validar una fecha y devolverla en formato datetime.
def validar_y_convertir_fecha(fecha: str):
    formatos = ("%Y-%m-%d", "%d-%m-%Y")

    for formato in formatos:
        try:
            return datetime.strptime(fecha, formato).date()
        except ValueError:
            continue

    return False

def generar_informe():
    pass

def exportar_informe():
    pass


