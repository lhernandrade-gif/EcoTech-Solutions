def mostrar_datos(objeto) -> None:
    lista = []
    if isinstance(objeto, list):
        for dict in objeto:
            for clave, valor in dict.items():
                print(f"{clave}: {valor}", end=" ")
    else:
        for clave, valor in vars(objeto).items():
            #print(f"{clave}: {valor}", end=" ")
            lista.append((clave, valor))
    return lista

def generar_informe():
    pass

def exportar_informe():
    pass


