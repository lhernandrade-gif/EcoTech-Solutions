def mostrar_datos(objeto) -> None:
    print(type(objeto))
    if isinstance(objeto, list):
        for dict in objeto:
            for clave, valor in dict.items():
                print(f"{clave}: {valor}")
    else:
        for clave, valor in vars(objeto).items():
            print(f"{clave}: {valor}")

def generar_informe():
    pass

def exportar_informe():
    pass


