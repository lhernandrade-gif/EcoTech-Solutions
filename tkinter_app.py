"""
Interfaz visual de EcoTech Solutions.
La interfaz no ejecuta consultas ni llama a los repositorios todavía.
Completa los métodos marcados como TODO cuando quieras conectar la lógica.
"""
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql
from datetime import date
import utilidades
import clases
from clases import Empleado, Departamento, Proyecto, RegistroTiempo, BaseDatos, EmpleadoRepositorio, DepartamentoRepositorio, ProyectoRepositorio, RegistroTiempoRepositorio

# Campos que se mostrarán en los formularios.
# Las claves son nombres visibles; los valores son los nombres de atributos
# de las clases/modelos para facilitar la futura conexión con los repositorios.
load_dotenv()
sesion_actual = clases.BaseDatos(os.getenv("DB_HOST"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))

ENTIDADES = {
    "Empleados": [
        ("Primer nombre", "primer_nombre"),
        ("Segundo nombre", "segundo_nombre"),
        ("Primer apellido", "primer_apellido"),
        ("Segundo apellido", "segundo_apellido"),
        ("RUT", "rut"),
        ("Dirección", "direccion"),
        ("Teléfono", "telefono"),
        ("Email", "email"),
        ("Fecha de inicio de contrato (AAAA-MM-DD)", "fecha_inicio_contrato"),
        ("Salario", "salario"),
    ],
    "Departamentos": [
        ("Nombre", "nombre"),
        ("ID del gerente (opcional)", "gerente"),
        ("IDs de empleados (separados por coma)", "lista_empleados"),
    ],
    "Proyectos": [
        ("Nombre", "nombre"),
        ("Descripción", "descripcion"),
        ("Fecha del proyecto (AAAA-MM-DD)", "fecha_proyecto"),
        ("IDs de empleados (separados por coma)", "lista_empleados"),
    ],
    "Registros de tiempo": [
        ("Fecha (AAAA-MM-DD)", "fecha"),
        ("Horas trabajadas", "horas_trabajadas"),
        ("Descripción de tareas", "descripcion_tareas"),
        ("ID del empleado", "empleado_id"),
        ("ID del proyecto", "proyecto_id"),
    ],
}

IDS = {
    "Empleados": "empleado_id",
    "Departamentos": "departamento_id",
    "Proyectos": "proyecto_id",
    "Registros de tiempo": "registro_tiempo_id",
}

CLASES = {"Empleados": Empleado, "Departamentos": Departamento, "Proyectos": Proyecto, "Registros de tiempo": RegistroTiempo}

REPOSITORIOS = {"Empleados": EmpleadoRepositorio, "Departamentos": DepartamentoRepositorio, "Proyectos": ProyectoRepositorio, "Registros de tiempo": RegistroTiempoRepositorio}

class EcoTechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de EcoTech")
        self.root.geometry("760x480")
        self.root.minsize(680, 440)

        self._configurar_estilos()
        self._construir_menu()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("vista" if "vista" in estilo.theme_names() else "clam")
        except tk.TclError:
            pass
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 17))
        estilo.configure("Accion.TButton", font=("Segoe UI", 11), padding=(12, 8))
        estilo.configure("Estado.TLabel", padding=(8, 5))

    def _construir_menu(self):
        contenedor = ttk.Frame(self.root, padding=18)
        contenedor.pack(fill="both", expand=True)

        encabezado = ttk.Label(contenedor, text="Gestor de EcoTech", style="Titulo.TLabel")
        encabezado.pack(anchor="w", pady=(0, 18))

        zona = ttk.Frame(contenedor, padding=18, relief="groove")
        zona.pack(fill="both", expand=True)

        zona.columnconfigure(0, weight=1)
        zona.columnconfigure(1, weight=1)
        zona.rowconfigure(0, weight=1)
        zona.rowconfigure(1, weight=1)
        zona.rowconfigure(2, weight=1)

        ttk.Button(
            zona, text="Ingresar Nuevo", style="Accion.TButton",
            command=self.abrir_ingresar
        ).grid(row=0, column=0, padx=20, pady=12)

        ttk.Button(
            zona, text="Buscar por ID", style="Accion.TButton",
            command=self.abrir_buscar
        ).grid(row=0, column=1, padx=20, pady=12)

        ttk.Button(
            zona, text="Actualizar", style="Accion.TButton",
            command=self.abrir_actualizar
        ).grid(row=1, column=0, padx=20, pady=12)

        ttk.Button(
            zona, text="Eliminar", style="Accion.TButton",
            command=self.abrir_eliminar
        ).grid(row=1, column=1, padx=20, pady=12)

        #ttk.Button(
        #    zona, text="Generar Informe", style="Accion.TButton",
        #    command=self.abrir_informe
        #).grid(row=2, column=0, columnspan=2, padx=20, pady=12)

        self.log_var = tk.StringVar(value="LOG: Programa inicializado con éxito.")
        barra = ttk.Label(
            contenedor, textvariable=self.log_var, relief="sunken",
            anchor="w", style="Estado.TLabel"
        )
        barra.pack(fill="x", pady=(10, 0))

    def registrar_log(self, mensaje):
        """Actualiza la barra de estado inferior."""
        self.log_var.set(f"[LOG] {mensaje}")

    def _nueva_ventana(self, titulo, geometria="560x520"):
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry(geometria)
        ventana.minsize(460, 360)
        ventana.transient(self.root)
        return ventana

    def _selector_entidad(self, parent, variable, callback):
        fila = ttk.Frame(parent)
        fila.pack(fill="x", pady=(0, 12))
        ttk.Label(fila, text="Tabla / entidad:", width=20).pack(side="left")
        selector = ttk.Combobox(
            fila, textvariable=variable, values=list(ENTIDADES),
            state="readonly"
        )
        selector.pack(side="left", fill="x", expand=True)
        selector.bind("<<ComboboxSelected>>", lambda _evento: callback())
        return selector

    def abrir_ingresar(self):
        ventana = self._nueva_ventana("Ingresar nuevo registro")
        marco = ttk.Frame(ventana, padding=18)
        marco.pack(fill="both", expand=True)

        entidad = tk.StringVar(value="Empleados")
        ttk.Label(marco, text="Ingresar nuevo registro", font=("Segoe UI", 14)).pack(
            anchor="w", pady=(0, 12)
        )
        self._selector_entidad(marco, entidad, lambda: dibujar_campos())

        area = ttk.Frame(marco)
        area.pack(fill="both", expand=True)

        entradas = {}

        def dibujar_campos():
            for widget in area.winfo_children():
                widget.destroy()
            entradas.clear()
            for etiqueta, atributo in ENTIDADES[entidad.get()]:
                fila = ttk.Frame(area)
                fila.pack(fill="x", pady=4)
                ttk.Label(fila, text=etiqueta, width=32, wraplength=210).pack(side="left")
                entrada = ttk.Entry(fila)
                entrada.pack(side="left", fill="x", expand=True)
                entradas[atributo] = entrada

        def guardar_visual():
            datos_finales = {}
            for atributo, entrada in entradas.items():
                if entrada.get() == "":
                    datos_finales[atributo] = [None,]
                else:
                    datos_finales[atributo] = entrada.get()
            clase = CLASES[entidad.get()]
            objeto = clase(**datos_finales)
            clase_repositorio = REPOSITORIOS[entidad.get()]
            objeto_repositorio = clase_repositorio(sesion_actual)
            try:
                objeto_repositorio.guardar(objeto)
                self.registrar_log(
                    f"Información guardada con éxito.")
            except pymysql.err.IntegrityError as e:
                self.registrar_log(
                    f"ERROR: Código de excepción: {e}")
            except pymysql.MySQLError as e:
                self.registrar_log(
                    f"Error en la ejecución: {e}"
            )

        dibujar_campos()
        ttk.Button(marco, text="Guardar", command=guardar_visual).pack(anchor="e", pady=(12, 0))

    def abrir_buscar(self):
        self._abrir_formulario_id("Buscar por ID", "Buscar", "buscar")

    def abrir_actualizar(self):
        self._abrir_formulario_id("Actualizar registro", "Cargar / actualizar", "actualizar")

    def abrir_eliminar(self):
        self._abrir_formulario_id("Eliminar registro", "Eliminar", "eliminar")

    def _abrir_formulario_id(self, titulo, texto_boton, accion):
        ventana = self._nueva_ventana(titulo, "560x560")
        marco = ttk.Frame(ventana, padding=18)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text=titulo, font=("Segoe UI", 14)).pack(anchor="w", pady=(0, 12))
        entidad = tk.StringVar(value="Empleados")
        self._selector_entidad(marco, entidad, lambda: dibujar_campos())

        fila_id = ttk.Frame(marco)
        fila_id.pack(fill="x", pady=(0, 12))
        etiqueta_id = ttk.Label(fila_id, text=f"ID ({IDS[entidad.get()]}):", width=32)
        etiqueta_id.pack(side="left")
        id_var = tk.StringVar()
        ttk.Entry(fila_id, textvariable=id_var).pack(side="left", fill="x", expand=True)

        area = ttk.Frame(marco)
        area.pack(fill="both", expand=True)
        entradas = {}

        def dibujar_campos():
            etiqueta_id.config(text=f"ID ({IDS[entidad.get()]}):")
            for widget in area.winfo_children():
                widget.destroy()
            entradas.clear()
            if accion == "buscar" or accion == "eliminar":
                ttk.Label(
                    area,
                    text=("Se mostrarán aquí los datos encontrados."
                          if accion == "buscar"
                          else "Confirma el ID antes de eliminar el registro."),
                    wraplength=450
                ).pack(anchor="w", pady=8)
                return
            for etiqueta, atributo in ENTIDADES[entidad.get()]:
                fila = ttk.Frame(area)
                fila.pack(fill="x", pady=4)
                ttk.Label(fila, text=etiqueta, width=32, wraplength=210).pack(side="left")
                entrada = ttk.Entry(fila)
                entrada.pack(side="left", fill="x", expand=True)
                entradas[atributo] = entrada

        def ejecutar():
            datos_finales = {}
            clase = CLASES[entidad.get()]
            objeto = clase(**datos_finales)
            clase_repositorio = REPOSITORIOS[entidad.get()]
            objeto_repositorio = clase_repositorio(sesion_actual)
            if accion == "buscar":
                try:
                    datos_finales = {}
                    datos_finales[IDS[entidad.get()]] = id_var.get()
                    print(datos_finales)
                    clase = CLASES[entidad.get()]
                    objeto = clase(**datos_finales)
                    clase_repositorio = REPOSITORIOS[entidad.get()]
                    objeto_repositorio = clase_repositorio(sesion_actual)
                    self.registrar_log(f"Búsqueda visual preparada para {entidad.get()} ID {id_var.get()}; lógica pendiente.")
                    objeto = objeto_repositorio.buscar_por_id(objeto)
                    messagebox.showinfo('Resultados de Búsqueda por ID', f'{utilidades.mostrar_datos(objeto)}')
                except pymysql.MySQLError as e:
                    # Capturar fallos de MySQL (ej. tabla no existe, error de sintaxis)
                    self.registrar_log(f"Error en la ejecución: {e}")
            elif accion == "actualizar":
                datos_finales = {}
                for atributo, entrada in entradas.items():
                    if entrada.get() == "":
                        datos_finales[atributo] = [None, ]
                    else:
                        datos_finales[atributo] = entrada.get()
                datos_finales[IDS[entidad.get()]] = int(id_var.get())
                clase = CLASES[entidad.get()]
                objeto = clase(**datos_finales)
                clase_repositorio = REPOSITORIOS[entidad.get()]
                objeto_repositorio = clase_repositorio(sesion_actual)
                utilidades.mostrar_datos(objeto)
                self.registrar_log(
                    f"Actualización visual preparada para {entidad.get()} ID {id_var.get()}.")
                try:
                    objeto_repositorio.actualizar(objeto)
                    self.registrar_log(
                        f"Actualizado con éxito.")
                except pymysql.err.IntegrityError as e:
                    self.registrar_log(
                        f"ERROR: Código de excepción: {e}")
                except pymysql.MySQLError as e:
                    self.registrar_log(
                        f"Error en la ejecución: {e}"
                    )
            else:
                try:
                    datos_finales = {}
                    datos_finales[IDS[entidad.get()]] = int(id_var.get())
                    print(datos_finales)
                    clase = CLASES[entidad.get()]
                    objeto = clase(**datos_finales)
                    clase_repositorio = REPOSITORIOS[entidad.get()]
                    objeto_repositorio = clase_repositorio(sesion_actual)
                    self.registrar_log(f"Eliminación visual preparada para {entidad.get()} ID {id_var.get()}.")
                    objeto_repositorio.eliminar(objeto)
                    self.registrar_log(
                        f"Borrado con éxito.")
                except pymysql.MySQLError as e:
                    # Capturar fallos de MySQL (ej. tabla no existe, error de sintaxis)
                    self.registrar_log(f"Error en la ejecución: {e}")

        dibujar_campos()
        ttk.Button(marco, text=texto_boton, command=ejecutar).pack(anchor="e", pady=(12, 0))

    def abrir_informe(self):
        ventana = self._nueva_ventana("Generar informe", "500x260")
        marco = ttk.Frame(ventana, padding=18)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text="Generar informe", font=("Segoe UI", 14)).pack(anchor="w", pady=(0, 14))

        entidad = tk.StringVar(value="Empleados")
        self._selector_entidad(marco, entidad, lambda: None)

        ttk.Label(
            marco,
            text="La vista o archivo del informe se implementará al conectar los repositorios.",
            wraplength=430
        ).pack(anchor="w", pady=12)

        def generar():
            # PENDIENTE: consultar el repositorio seleccionado y mostrar/exportar el informe.
            self.registrar_log(f"Informe de {entidad.get()} solicitado; lógica pendiente de implementar.")

        ttk.Button(marco, text="Generar", command=generar).pack(anchor="e", pady=(8, 0))


def main():
    root = tk.Tk()
    EcoTechApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
