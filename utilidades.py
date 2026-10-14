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

def generar_informe():
    pass

def exportar_informe():
    pass


