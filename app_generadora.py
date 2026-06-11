# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------
import subprocess
from pathlib import Path

from libs.Env import Env
from libs.contentOfFile import File
import libs.TUI as TUI
import libs.utils as utils
import settings
import libs.dbComun as dbComun


# ---------------------------------------------------------------------
# Constantes de sistema
# ---------------------------------------------------------------------
# Constantes de posción de argumentos de entrada
ARG_FILE_SCRIPT = 0
ARG_DB_SELECT = 1
ARG_OUT_SELECT = 2
ARG_OP_OVER_DB = 3

# Constantes de selección de argumentos
DEFAULT = 0
DB_MARIA_DB = 1
DB_SQLITE = 2
OUT_PYTHON = 1
OUT_PHP = 2
CORRECTOR_ARRAY = 1  # los arrays comienzan por 0 por lo que debemos sumar el corrector en las comparaciones posicionales

# Constantes de operación sobre db
NO_SOPORTADO = 0
DROP_DB = 1
CREATE_DB = 2
LOAD_SCRIPT = 3


# ---------------------------------------------------------------------
# Variables globales
# ---------------------------------------------------------------------
log = None
variablesDeEntorno = None

# ---------------------------------------------------------------------
# Main()
# ---------------------------------------------------------------------
def main():
    # DONE 0. Inicializar variables globales
    global log
    global variablesDeEntorno

    initGlobalSettings()

    # TODO 1. Análisis de DB (refactorizar)
    metadatos = getMetadatosDb(variablesDeEntorno['SERVER_DB'])

    # TODO 2. Generarción de DAOs
    generateDAOs(metadatos)

    log.info("voy por aquí")
    # DONE 4. QUEUE-SINGLETON
    # No requiere personalización. Emplearemos implementación estándard

    # TODO 3. WORKER
    

    # TODO 5. DISPACHER


    # TODO 6. APP (endpoints)
    NOMBRE_APP_FINAL = "app.py"
    generateApp(metadatos, NOMBRE_APP_FINAL)

    # TODO 7. TESTS


# ----------------------------------------------------------------------
# Funciones auxiliares
# ----------------------------------------------------------------------
def initGlobalSettings():
    global log
    global variablesDeEntorno
    # DONE: 0. Cargamos las variables globales en settings
    log = settings.initLoggin(Path(__file__).stem + ".log")
    TUI.settings = settings
    utils.settings = settings
    dbComun.settings = settings
    log.info('0. Variables globales cargadas en settings')

    # DONE: 1.2. Carga de variables de entorno
    tipoDB = "sqlite"
    variablesDeEntorno = utils.loadEnvironmentVar(tipoDB)


def getMetadatosDb(db_file: str) -> BaseDatos:
    tipoDB = variablesDeEntorno['TIPO_DB']
    # DONE: 1.3. Carga driver
    db = dbComun.getDriverDB(tipoDB)

    # DONE: 1.4. Comandos "normalizados" vía plantilla
    db.comandosSQL = Env.get(settings.TAREA_PATH + 'templates/' + tipoDB + '/sql')

    # TODO: 1.5. Import en db pruebas -> sólo conectar
    dbComun.getConexionDB(db, variablesDeEntorno)

    # DONE: 1.6. Generación de metadatos
    metadatos = dbComun.generacionDeMetadatos(db)
    utils.printInfo(f'1. Carga de metadatos de la bbdd: "{metadatos.nombre}"')
    return metadatos


def generateApp(metadatos, file: str):
    """Genera la aplicación final con los endpoints correspondientes a la base de datos"""
    BASE = settings.TAREA_PATH
    with \
        open(BASE + "core/app.template", "r", encoding="utf-8") as plantilla, \
        open(BASE + "app.py", "w", encoding="utf-8") as escritura:
        for linea in plantilla:
            if linea == '%%WORKER%%\n':
                """Forma correcta:
                with open(BASE + "core/worker.template", "r", encoding="utf-8") as plantilla_worker:
                    for linea_worker in plantilla_worker:
                        escritura.write(linea_worker)
                """
                escritura.write( File().load(BASE + "core/worker.template") )
            else:
                escritura.write(linea)
    log.info("6. Generar app base")
    return None


def generateDAOs(metadatos):
    """Generador de DAOs

    Parametros:
        - metadatos (BaseDatos) de la base de datos
    """
    for tabla in metadatos.tablas:
        columnas = ', '.join([column.nombre for column in tabla.columnas])
        placeholders = ', '.join(['?' for _ in tabla.columnas])
        set_clause = ', '.join([f"{columna.nombre}=?" for columna in tabla.columnas])
        dao_content = f"""
class {tabla.nombre.capitalize()}DAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_{tabla.nombre}(self, id):
        query = "SELECT * FROM {tabla.nombre} WHERE id = ?"
        return self.db_connection.execute(query, (id,)).fetchone()

    def create_{tabla.nombre}(self, data):
        query = "INSERT INTO {tabla.nombre} ({columnas}) VALUES ({placeholders})"
        self.db_connection.execute(query, tuple(data.values()))
        self.db_connection.commit()
        return self.db_connection.lastrowid

    def update_{tabla.nombre}(self, id, data):
        query = f"UPDATE {tabla.nombre} SET {set_clause} WHERE id = ?"
        self.db_connection.execute(query, tuple(data.values()) + (id,))
        self.db_connection.commit()

    def delete_{tabla.nombre}(self, id):
        query = "DELETE FROM {tabla.nombre} WHERE id = ?"
        self.db_connection.execute(query, (id,))
        self.db_connection.commit()
"""
        with open(f"{settings.TAREA_PATH}/daos/{tabla.nombre.capitalize()}DAO.py", 'w') as f:
            f.write(dao_content)
    utils.printInfo(f'2. DAOs  generados: {", ".join([t.nombre for t in metadatos.tablas])}')


# Autocargador de programa externo
if __name__ == "__main__":
    main()
