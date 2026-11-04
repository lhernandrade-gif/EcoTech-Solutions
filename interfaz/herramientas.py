import threading
import tkinter as tk
from tkinter import ttk
from datetime import date

from clases.Empleado import Empleado
from clases.EmpleadoRepositorio import EmpleadoRepositorio
from clases.ServicioCambioDivisa import cambio_divisa
from clases.ServicioDatosClimaticos import obtener_datos_climaticos
from .configuracion import sesion_actual
from .errores import texto_error


def abrir_herramientas(app):
    ventana = app._nueva_ventana("Herramientas", "760x720")
    contenedor = ttk.Frame(ventana, padding=(30, 24))
    contenedor.pack(fill="both", expand=True)

    ttk.Label(
        contenedor, text="Conversión de Divisas", style="Seccion.TLabel"
    ).pack(anchor="w", pady=(0, 12))

    conversion = ttk.Frame(contenedor)
    conversion.pack(fill="x")
    conversion.columnconfigure(0, weight=3)
    conversion.columnconfigure(1, weight=2)

    origen_var = tk.StringVar(value="manual")
    ttk.Label(conversion, text="Origen del monto").grid(
        row=0, column=0, columnspan=2, sticky="w"
    )
    opciones_origen = ttk.Frame(conversion)
    opciones_origen.grid(row=1, column=0, columnspan=2, sticky="w", pady=(4, 12))
    ttk.Radiobutton(
        opciones_origen, text="Monto manual", variable=origen_var,
        value="manual", command=lambda: cambiar_origen()
    ).pack(side="left", padx=(0, 18))
    ttk.Radiobutton(
        opciones_origen, text="Salario de empleado", variable=origen_var,
        value="empleado", command=lambda: cambiar_origen()
    ).pack(side="left")

    monto_var = tk.StringVar()
    monto_marco = ttk.Frame(conversion)
    monto_marco.grid(row=2, column=0, sticky="ew", padx=(0, 18), pady=(0, 12))
    ttk.Label(monto_marco, text="Monto").pack(anchor="w", pady=(0, 4))
    monto_entrada = ttk.Entry(monto_marco, textvariable=monto_var, width=24)
    monto_entrada.pack(anchor="w", fill="x")

    monedas = ("CLP", "USD", "EUR")
    fila_monedas = ttk.Frame(conversion)
    fila_monedas.grid(row=2, column=1, sticky="ew", pady=(0, 12))
    fila_monedas.columnconfigure(0, weight=1)
    fila_monedas.columnconfigure(1, weight=1)
    moneda_base_var = tk.StringVar(value="CLP")
    moneda_destino_var = tk.StringVar(value="USD")
    ttk.Label(fila_monedas, text="Moneda base").grid(row=0, column=0, sticky="w")
    ttk.Label(fila_monedas, text="Convertir a").grid(
        row=0, column=1, sticky="w", padx=(12, 0)
    )
    ttk.Combobox(
        fila_monedas, textvariable=moneda_base_var, values=monedas,
        state="readonly", width=10
    ).grid(row=1, column=0, sticky="ew", pady=(4, 0))
    ttk.Combobox(
        fila_monedas, textvariable=moneda_destino_var, values=monedas,
        state="readonly", width=10
    ).grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=(4, 0))

    empleado_marco = ttk.Frame(conversion)
    empleado_marco.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 12))
    empleado_marco.columnconfigure(3, weight=1)
    criterio_var = tk.StringVar(value="ID")
    ttk.Label(empleado_marco, text="Buscar empleado por").grid(
        row=0, column=0, sticky="w", padx=(0, 8)
    )
    ttk.Radiobutton(
        empleado_marco, text="ID", variable=criterio_var, value="ID",
        command=lambda: limpiar_empleado()
    ).grid(row=0, column=1, sticky="w", padx=(0, 8))
    ttk.Radiobutton(
        empleado_marco, text="RUT", variable=criterio_var, value="RUT",
        command=lambda: limpiar_empleado()
    ).grid(row=0, column=2, sticky="w", padx=(0, 8))
    busqueda_var = tk.StringVar()
    ttk.Entry(empleado_marco, textvariable=busqueda_var, width=22).grid(
        row=0, column=3, sticky="ew", padx=(0, 8)
    )
    resultado_empleado_var = tk.StringVar()
    ttk.Label(empleado_marco, textvariable=resultado_empleado_var, style="Subtitulo.TLabel").grid(
        row=1, column=0, columnspan=5, sticky="w", pady=(8, 0)
    )

    datos_empleado = {"salario_CLP": None}
    origen_actual = {"valor": "manual"}
    estado_var = tk.StringVar()
    ttk.Label(
        conversion, textvariable=estado_var, style="Subtitulo.TLabel"
    ).grid(row=5, column=0, columnspan=2, sticky="w", pady=(4, 0))

    def limpiar_empleado(*_args):
        datos_empleado["salario_CLP"] = None
        monto_var.set("")
        resultado_empleado_var.set("")

    def cambiar_origen():
        origen = origen_var.get()
        if origen != origen_actual["valor"]:
            limpiar_empleado()
            busqueda_var.set("")
            origen_actual["valor"] = origen
        estado_var.set("")
        if origen == "manual":
            monto_entrada.configure(state="normal")
            empleado_marco.grid_remove()
        else:
            monto_entrada.configure(state="readonly")
            empleado_marco.grid()

    busqueda_var.trace_add("write", limpiar_empleado)

    def buscar_empleado():
        limpiar_empleado()
        valor = busqueda_var.get().strip()
        try:
            repositorio = EmpleadoRepositorio(sesion_actual)
            if criterio_var.get() == "ID":
                if not valor.isdigit() or int(valor) <= 0:
                    raise ValueError("Ingresa un ID entero mayor que cero.")
                empleado = repositorio.buscar_por_id(
                    Empleado(empleado_id=int(valor))
                )
            else:
                empleado = repositorio.buscar_por_rut(Empleado(rut=valor))
            if empleado is None:
                raise ValueError("No se encontró un empleado con esos datos.")
            if empleado.salario_CLP is None:
                raise ValueError("El empleado no tiene un salario registrado.")
            datos_empleado["salario_CLP"] = empleado.salario_CLP
            monto_var.set(str(empleado.salario_CLP))
            moneda_base_var.set("CLP")
            nombre = " ".join(
                parte for parte in (
                    empleado.primer_nombre,
                    empleado.primer_apellido,
                    empleado.segundo_apellido,
                ) if parte
            )
            resultado_empleado_var.set(
                f"{nombre} · Salario cargado: {empleado.salario_CLP} CLP"
            )
            estado_var.set("")
        except Exception as error:
            resultado_empleado_var.set(texto_error(error))

    ttk.Button(
        empleado_marco, text="Buscar", style="Secundaria.TButton",
        command=buscar_empleado
    ).grid(row=0, column=4, sticky="e")
    cambiar_origen()

    resultado_var = tk.StringVar()
    ttk.Label(
        conversion, textvariable=resultado_var, style="Seccion.TLabel",
        wraplength=320, justify="right", anchor="e"
    ).grid(row=4, column=1, sticky="e", pady=(4, 0))

    def convertir():
        if origen_var.get() == "empleado" and datos_empleado["salario_CLP"] is None:
            estado_var.set("Busca primero un empleado con salario registrado.")
            return
        monto = monto_var.get().strip()

        moneda_base = moneda_base_var.get()
        moneda_destino = moneda_destino_var.get()
        boton_convertir.configure(state="disabled")
        estado_var.set("Convirtiendo…")
        resultado_var.set("")

        def consultar():
            try:
                convertido = cambio_divisa(monto, moneda_base, moneda_destino)
                if convertido is None:
                    raise ValueError("El servicio no devolvió un monto convertido.")
            except Exception as error:
                mensaje = texto_error(error)
                ventana.after(0, lambda: conversion_fallida(mensaje))
            else:
                ventana.after(
                    0,
                    lambda valor=str(convertido): conversion_completada(
                        monto, moneda_base, valor, moneda_destino
                    ),
                )

        threading.Thread(target=consultar, daemon=True).start()

    def conversion_fallida(mensaje):
        if ventana.winfo_exists():
            estado_var.set(mensaje)
            boton_convertir.configure(state="normal")

    def conversion_completada(monto, moneda_base, convertido, moneda_destino):
        if ventana.winfo_exists():
            resultado_var.set(
                f"{monto} {moneda_base} = {convertido} {moneda_destino}"
            )
            estado_var.set("")
            boton_convertir.configure(state="normal")

    boton_convertir = ttk.Button(
        conversion, text="Convertir", style="Accion.TButton", command=convertir
    )
    boton_convertir.grid(row=4, column=0, sticky="w", pady=(4, 0))

    ttk.Separator(contenedor, orient="horizontal").pack(fill="x", pady=12)

    ttk.Label(
        contenedor, text="Consulta de Datos Climáticos", style="Seccion.TLabel"
    ).pack(anchor="w", pady=(0, 10))

    clima = ttk.Frame(contenedor)
    clima.pack(fill="x")
    clima.columnconfigure(1, weight=1)
    clima.columnconfigure(3, weight=1)

    fecha_var = tk.StringVar(value=date.today().isoformat())
    ciudad_var = tk.StringVar()
    ttk.Label(clima, text="Fecha (AAAA-MM-DD)").grid(
        row=0, column=0, sticky="w", padx=(0, 8)
    )
    ttk.Label(clima, text="Ciudad").grid(
        row=0, column=2, sticky="w", padx=(18, 8)
    )
    ttk.Entry(clima, textvariable=fecha_var, width=18).grid(
        row=1, column=0, columnspan=2, sticky="ew"
    )
    ttk.Entry(clima, textvariable=ciudad_var).grid(
        row=1, column=2, columnspan=2, sticky="ew", padx=(18, 0)
    )

    clima_estado_var = tk.StringVar()
    ttk.Label(
        clima, textvariable=clima_estado_var, style="Subtitulo.TLabel",
        wraplength=680
    ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(8, 2))

    campos_clima = (
        ("Condición", "condicion"),
        ("Temperatura", "temperatura"),
        ("Humedad relativa", "humedad"),
        ("Velocidad del viento", "viento"),
    )
    valores_clima = {clave: tk.StringVar() for _, clave in campos_clima}
    for indice, (etiqueta, clave) in enumerate(campos_clima):
        fila = 4 + indice // 2
        columna = (indice % 2) * 2
        ttk.Label(clima, text=etiqueta).grid(
            row=fila, column=columna, sticky="w", pady=(6, 0),
            padx=(0, 8 if columna == 0 else 0)
        )
        ttk.Label(
            clima, textvariable=valores_clima[clave], style="Subtitulo.TLabel"
        ).grid(
            row=fila, column=columna + 1, sticky="w", pady=(6, 0),
            padx=(0, 10) if columna == 0 else (28, 0)
        )

    def mostrar_datos_climaticos(datos):
        condicion, temperatura, humedad, viento = datos
        valores_clima["condicion"].set(str(condicion))
        valores_clima["temperatura"].set(f"{temperatura} °C")
        valores_clima["humedad"].set(f"{humedad} %")
        valores_clima["viento"].set(f"{viento} km/h")
        clima_estado_var.set("")
        boton_clima.configure(state="normal")

    def fallo_clima(mensaje):
        clima_estado_var.set(mensaje)
        boton_clima.configure(state="normal")

    def consultar_clima():
        fecha = fecha_var.get().strip()
        ciudad = ciudad_var.get().strip()
        for variable in valores_clima.values():
            variable.set("")
        boton_clima.configure(state="disabled")
        clima_estado_var.set("Consultando datos climáticos…")

        def consultar():
            try:
                datos = obtener_datos_climaticos(fecha, ciudad)
                if datos is None:
                    mensaje = "No se encontraron datos para esa ciudad y fecha."
                    ventana.after(0, lambda: fallo_clima(mensaje))
                    return
            except Exception as error:
                mensaje = texto_error(error)
                ventana.after(0, lambda: fallo_clima(mensaje))
            else:
                ventana.after(0, lambda: mostrar_datos_climaticos(datos))

        threading.Thread(target=consultar, daemon=True).start()

    boton_clima = ttk.Button(
        clima, text="Consultar clima", style="Secundaria.TButton",
        command=consultar_clima
    )
    boton_clima.grid(row=2, column=0, sticky="w", pady=(10, 0))