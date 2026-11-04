import threading
import tkinter as tk
from tkinter import ttk

import pymysql

import utilidades
from clases.Empleado import Empleado
from clases.EmpleadoRepositorio import EmpleadoRepositorio
from clases.ServicioCambioDivisa import cambio_divisa
from .configuracion import sesion_actual


def abrir_herramientas(app):
    ventana = app._nueva_ventana("Herramientas", "760x720")
    contenedor = ttk.Frame(ventana, padding=(30, 24))
    contenedor.pack(fill="both", expand=True)

    ttk.Label(
        contenedor, text="Conversión de Divisas", style="Seccion.TLabel"
    ).pack(anchor="w", pady=(0, 12))

    origen_var = tk.StringVar(value="manual")
    ttk.Label(contenedor, text="Origen del monto").pack(anchor="w")
    opciones_origen = ttk.Frame(contenedor)
    opciones_origen.pack(anchor="w", pady=(4, 10))
    ttk.Radiobutton(
        opciones_origen, text="Monto manual", variable=origen_var,
        value="manual", command=lambda: cambiar_origen()
    ).pack(side="left", padx=(0, 18))
    ttk.Radiobutton(
        opciones_origen, text="Salario de empleado", variable=origen_var,
        value="empleado", command=lambda: cambiar_origen()
    ).pack(side="left")

    monto_var = tk.StringVar()
    monto_marco = ttk.Frame(contenedor)
    ttk.Label(monto_marco, text="Monto").pack(side="left", padx=(0, 12))
    ttk.Entry(monto_marco, textvariable=monto_var, width=24).pack(side="left")

    empleado_marco = ttk.Frame(contenedor)
    criterio_var = tk.StringVar(value="ID")
    ttk.Radiobutton(
        empleado_marco, text="ID", variable=criterio_var, value="ID",
        command=lambda: limpiar_empleado()
    ).grid(row=0, column=0, sticky="w", padx=(0, 12))
    ttk.Radiobutton(
        empleado_marco, text="RUT", variable=criterio_var, value="RUT",
        command=lambda: limpiar_empleado()
    ).grid(row=0, column=1, sticky="w", padx=(0, 12))
    busqueda_var = tk.StringVar()
    ttk.Entry(empleado_marco, textvariable=busqueda_var, width=24).grid(
        row=0, column=2, sticky="ew", padx=(0, 8)
    )
    empleado_marco.columnconfigure(2, weight=1)
    resultado_empleado_var = tk.StringVar()
    ttk.Label(
        empleado_marco, textvariable=resultado_empleado_var,
        style="Subtitulo.TLabel"
    ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(8, 0))

    datos_empleado = {"salario": None}
    origen_actual = {"valor": "manual"}
    estado_var = tk.StringVar()
    ttk.Label(
        contenedor, textvariable=estado_var, style="Subtitulo.TLabel"
    ).pack(anchor="w", pady=(8, 0))

    def limpiar_empleado(*_args):
        datos_empleado["salario"] = None
        monto_var.set("")
        resultado_empleado_var.set("")

    def cambiar_origen():
        origen = origen_var.get()
        if origen != origen_actual["valor"]:
            limpiar_empleado()
            busqueda_var.set("")
            origen_actual["valor"] = origen
        monto_marco.pack_forget()
        empleado_marco.pack_forget()
        estado_var.set("")
        if origen == "manual":
            monto_marco.pack(fill="x", pady=(0, 10))
        else:
            empleado_marco.pack(fill="x", pady=(0, 10))

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
            if empleado.salario is None:
                raise ValueError("El empleado no tiene un salario registrado.")
            datos_empleado["salario"] = empleado.salario
            monto_var.set(str(empleado.salario))
            nombre = " ".join(
                parte for parte in (
                    empleado.primer_nombre,
                    empleado.primer_apellido,
                    empleado.segundo_apellido,
                ) if parte
            )
            resultado_empleado_var.set(
                f"{nombre} · Salario cargado: {empleado.salario} CLP"
            )
            estado_var.set("")
        except (ValueError, TypeError) as error:
            resultado_empleado_var.set(str(error))
        except pymysql.MySQLError as error:
            resultado_empleado_var.set(f"Error de base de datos: {error}")
        except Exception as error:
            resultado_empleado_var.set(f"No se pudo buscar el empleado: {error}")

    ttk.Button(
        empleado_marco, text="Buscar", style="Secundaria.TButton",
        command=buscar_empleado
    ).grid(row=0, column=3, sticky="e")
    cambiar_origen()

    monedas = ("CLP", "USD", "EUR")
    fila_monedas = ttk.Frame(contenedor)
    fila_monedas.pack(fill="x", pady=(4, 14))
    moneda_base_var = tk.StringVar(value="CLP")
    moneda_destino_var = tk.StringVar(value="USD")
    ttk.Label(fila_monedas, text="Moneda base").grid(row=0, column=0, sticky="w")
    ttk.Combobox(
        fila_monedas, textvariable=moneda_base_var, values=monedas,
        state="readonly", width=12
    ).grid(row=1, column=0, sticky="w", pady=(4, 0))
    ttk.Label(fila_monedas, text="Convertir a").grid(
        row=0, column=1, sticky="w", padx=(24, 0)
    )
    ttk.Combobox(
        fila_monedas, textvariable=moneda_destino_var, values=monedas,
        state="readonly", width=12
    ).grid(row=1, column=1, sticky="w", padx=(24, 0), pady=(4, 0))

    resultado_var = tk.StringVar()
    ttk.Label(
        contenedor, textvariable=resultado_var, style="Seccion.TLabel"
    ).pack(anchor="w", pady=(10, 4))

    def convertir():
        if origen_var.get() == "empleado" and datos_empleado["salario"] is None:
            estado_var.set("Busca primero un empleado con salario registrado.")
            return
        monto = monto_var.get().strip()
        if not utilidades.validar_monto(monto):
            estado_var.set("Ingresa un monto numérico válido, igual o mayor que cero.")
            return

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
                ventana.after(0, lambda mensaje=str(error): conversion_fallida(mensaje))
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
        contenedor, text="Convertir", style="Accion.TButton", command=convertir
    )
    boton_convertir.pack(anchor="w", pady=(0, 18))

    ttk.Separator(contenedor, orient="horizontal").pack(fill="x", pady=12)

    ttk.Label(
        contenedor, text="Consulta de Datos Climáticos", style="Seccion.TLabel"
    ).pack(anchor="w", pady=(0, 10))
    ttk.Frame(contenedor).pack(fill="both", expand=True)