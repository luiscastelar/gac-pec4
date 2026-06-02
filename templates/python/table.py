import os.path
import tkinter as tk
from tkinter import ttk
import libs.dbComun as dbComun
import libs.utils as utils
import libs.db as db
from libs.Env import Env
import logging

TAREA_PATH = os.path.dirname(__file__) + '/'
LOGGING = logging.DEBUG       # modo de depuración
FILE_LOGGIN = TAREA_PATH + 'app-%%TABLA_NOMBRE%%.log'
logger = None


def create_%%TABLA_NOMBRE%%_widgets(self):
    env = {
        'SERVER_DB': "%%HOST%%",
        'PORT_DB': "%%PORT_DB%%", 
        'USER_DB': "%%USER%%",
        'NAME_DB': "%%DB%%",
        'PASS_DB': "%%PASS%%",
        'TIPO_DB': "%%TIPO_DB%%"
    }
    columnas = %%COLUMNAS%%

    root = self.root

    # Create the main widgets for the book management interface
    self.clear_widgets()
    root.title(f"Gestión de %%TABLA_NOMBRE%%")


    # DONE: 4. Carga driver
    match env['TIPO_DB']:
        case 'mariadb':
            from libs.db import DbMariadb as DB
        case 'sqlite':
            from libs.db import DbSqlite as DB

        case 'oracle-xe':
            #from libs import oracleDB as db
            pass
        case _:
            print(f'Gestor de BBDD {tipoDB} no disponible', settings.EXIT['FORMAT_ERROR'])
    #db = dbComun.getDriverDB(env['TIPO_DB'])
    db = DB(logger)  # Instanciamos el driver de la base de datos

    # DONE: 5. Comandos "normalizados" vía plantilla
    #pathToSql = 'templates/' + env['TIPO_DB'] + '/sql'
    pathToSql = TAREA_PATH + 'templates/sql'
    logger.debug(f'Path to sql:{pathToSql}')
    db.comandosSQL = Env.get(pathToSql)

    # DONE: 6. Crear conexion
    conn = dbComun.getConexionDB(db, env)

    # DONE: 7. Captrua de datos    
    tabla = db.readSimpleList("SELECT * FROM %%TABLA_NOMBRE%%")
    logger.debug(tabla)

    """------------------ Creación del menú del CRUD ------------------------"""
    # Creamos el notebook (zona de etiquetas)
    tabControl = ttk.Notebook(root)
    #tabControl = ttk.Notebook(master=root, height=400, width=600, padding=10)
    
    # Creamos las etiquetas del CRUD
    create = viewCreate(self, root, columnas, db)
    read = viewRead(self, root, columnas, db)
    update = viewUpdate(self, root, columnas, db)
    delete = viewDelete(self, root, columnas, db)
    
    # Las añadimos al notebook
    tabControl.add(create, text='Insertar')
    tabControl.add(read, text='Leer')
    tabControl.add(update, text='Actualizar')
    tabControl.add(delete, text='Borrar')    

    # Las situamos en el notebook
    tabControl.pack(expand=1, fill="both")


# CREATE
#--------
def viewCreate(self, parent, columnas, db):

    frame = ttk.Frame(parent)

    entries = {}

    for i, col in enumerate(columnas):
        if col == "id":
            continue

        ttk.Label(frame, text=col).grid(row=i, column=0, sticky="w", padx=5, pady=5)
        e = ttk.Entry(frame)
        e.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
        entries[col] = e


    def insertar():
        campos = []
        valores = []

        for c, e in entries.items():
            campos.append(c)
            valores.append(e.get())

        sql = f"""
        INSERT INTO alumnos ({",".join(campos)})
        VALUES ({",".join(["%s"] * len(valores))})
        """

        db.execute(sql, tuple(valores))

    ttk.Button(frame, text="Insertar", command=insertar).grid(
        row=len(columnas), column=0, columnspan=2, pady=10
    )

    frame.columnconfigure(1, weight=1)

    return frame


# READ
#--------
def viewRead(self, parent, columnas, db):

    frame = ttk.Frame(parent)

    tree = ttk.Treeview(frame, columns=columnas, show="headings")

    for c in columnas:
        tree.heading(c, text=c)
        tree.column(c, anchor=tk.CENTER)

    tree.pack(expand=True, fill="both")

    def cargar():
        tree.delete(*tree.get_children())

        datos = db.readSimpleList("SELECT * FROM alumnos")

        for fila in datos:
            tree.insert("", tk.END, values=tuple(fila))

    ttk.Button(frame, text="Actualizar vista", command=cargar).pack(pady=5)

    cargar()

    return frame

    
# UPDATE
#--------
def viewUpdate(self, parent, columnas, db):

    frame = ttk.Frame(parent)

    tree = ttk.Treeview(frame, columns=columnas, show="headings", height=6)

    for c in columnas:
        tree.heading(c, text=c)
        tree.column(c, anchor=tk.CENTER)

    tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

    entradas = {}

    fila = 1
    for col in columnas:
        ttk.Label(frame, text=col).grid(row=fila, column=0, sticky="w", padx=5)
        e = ttk.Entry(frame)
        e.grid(row=fila, column=1, sticky="ew", padx=5)
        entradas[col] = e
        fila += 1

    def cargar():
        tree.delete(*tree.get_children())
        for f in db.readSimpleList("SELECT * FROM alumnos"):
            tree.insert("", tk.END, values=tuple(f))

    def seleccionar(event):
        item = tree.selection()
        if not item:
            return

        valores = tree.item(item[0])["values"]

        for i, col in enumerate(columnas):
            entradas[col].delete(0, tk.END)
            entradas[col].insert(0, valores[i])

    def actualizar():

        idv = entradas["id"].get()

        campos = []
        valores = []

        for col in columnas:
            if col == "id":
                continue
            campos.append(f"{col}=%s")
            valores.append(entradas[col].get())

        valores.append(idv)

        sql = f"""
        UPDATE alumnos
        SET {",".join(campos)}
        WHERE id=%s
        """

        db.execute(sql, tuple(valores))
        cargar()

    tree.bind("<<TreeviewSelect>>", seleccionar)

    ttk.Button(frame, text="Actualizar", command=actualizar).grid(
        row=fila, column=0, columnspan=2, pady=5
    )

    frame.columnconfigure(1, weight=1)

    cargar()

    return frame


# DELETE
#--------
def viewDelete(self, parent, columnas, db):

    frame = ttk.Frame(parent)

    tree = ttk.Treeview(frame, columns=columnas, show="headings")

    for c in columnas:
        tree.heading(c, text=c)
        tree.column(c, anchor=tk.CENTER)

    tree.pack(expand=True, fill="both")

    def cargar():
        tree.delete(*tree.get_children())
        for f in db.readSimpleList("SELECT * FROM alumnos"):
            tree.insert("", tk.END, values=tuple(f))

    def borrar():
        item = tree.selection()
        if not item:
            return

        idv = tree.item(item[0])["values"][0]

        db.execute("DELETE FROM alumnos WHERE id=%s", (idv,))
        cargar()

    ttk.Button(frame, text="Borrar seleccionado", command=borrar).pack(pady=5)

    cargar()

    return frame


# ---------------------------------------------------------------------
# # Opciones de depuración:
#  - DEBUG, INFO, WARNING, ERROR, CRITICAL
# ---------------------------------------------------------------------
def initLoggin():
    logging.basicConfig(filename = FILE_LOGGIN,
                            filemode = 'a',
                            level = LOGGING,
                            format='''%(asctime)s - f:%(module)s:%(lineno)d [%(levelname)s]:\n%(message)s''')
    return logging
logger = initLoggin()

# Dado que reaprobechamos librerías entre app generadora y final debemos realizar
# algunas correcciones:
settings = {}
settings['logging'] = logger
utils.settings = settings