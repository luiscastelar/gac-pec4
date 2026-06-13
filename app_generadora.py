# ---------------------------------------------------------------------
# Importaciones
# ---------------------------------------------------------------------
from pathlib import Path

from libs.Env import Env
from libs.contentOfFile import File
import libs.utils as utils
import settings
import libs.dbComun as dbComun


# ---------------------------------------------------------------------
# Constantes de sistema
# ---------------------------------------------------------------------
# Aviso que marca el inicio de los archivos generados
AVISO = f'''# {"*"*77}
#   Archivo generado desde plantilla -> NO TOCAR                              *
# {"*"*77}
'''


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
    initGlobalSettings()

    # DONE 1. Análisis de DB (refactorizar)
    metadatos = getMetadatosDb(variablesDeEntorno['SERVER_DB'])

    # DONE 2. Generarción de DAOs
    generateDAOs(metadatos)

    # DONE 3. QUEUE-SINGLETON
    # No requiere personalización. Emplearemos implementación estándard

    # DONE 4. WORKER
    generateWorker(metadatos)

    # DONE 5. DISPACHER
    # En plantilla app.template

    # DONE 6. APP (endpoints)
    NOMBRE_APP_FINAL = "app.py"
    generateApp(metadatos, NOMBRE_APP_FINAL)

    # DONE 7. TESTS
    # Ejecutar el script de testeo de forma manual con 
    #     python3 test_app.py


# ----------------------------------------------------------------------
# Funciones auxiliares
# ----------------------------------------------------------------------
def initGlobalSettings():
    global log
    global variablesDeEntorno
    # DONE: 0. Cargamos las variables globales en settings
    log = settings.initLoggin(Path(__file__).stem + ".log")
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
    metadatos.db_file = db_file
    return metadatos


def generateWorker(metadatos):
    BASE = settings.TAREA_PATH

    # Cargamos las plantillas con las marcas a sustituir
    worker_final = AVISO + File().load('core/worker.template')
    tabla_final = ''
    for tabla in metadatos.tablas:
        tabla_inicial = File().load('core/table.template').replace('%%_NAME_%%', tabla.nombre)
        tabla_final += tabla_inicial.replace('%%_DAO_%%', tabla.nombre.capitalize()+'DAO')

    worker_final = worker_final.replace('%%_TABLAS_%%', tabla_final[:-1])
    File().save('core/worker.py', worker_final)
    utils.printInfo(f'3. WORKER  generado')


def generateApp(metadatos, file: str):
    """Genera la aplicación final con los endpoints correspondientes a la base de datos"""
    BASE = settings.TAREA_PATH
    with \
        open(BASE + "core/app.template", "r", encoding="utf-8") as plantilla, \
        open(BASE + file, "w", encoding="utf-8") as escritura:
        escritura.write( AVISO )
        for linea in plantilla:
            match linea:
                case '%%_WORKER_%%\n':
                    escritura.write( File().load(BASE + "core/worker.py") )  # forma rápida pero con consumo brutal de memoria
                case '%%_DB_FILE_%%\n':
                    escritura.write(f'db_file = "{metadatos.db_file}"\n')
                case _:
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
        dao_content = f"""{AVISO}
import sqlite3

class {tabla.nombre.capitalize()}DAO:
    def __init__(self, fileDB):
        self.db_connection = sqlite3.connect(fileDB)

    def get_{tabla.nombre}(self, id = 0):
        query = "SELECT * FROM alumnos"
        if id == 0:
            return self.db_connection.execute(query).fetchall()
        else:
            query += ' WHERE id = ?'
            return self.db_connection.execute(query, (id,)).fetchone()

    def create_{tabla.nombre}(self, data):
        query = "SELECT id FROM {tabla.nombre} ORDER BY id DESC LIMIT 1"
        id = self.db_connection.execute(query).fetchone()
        data_new = dict()  # Como los dict a partir de 3.6 son ordenados...
        data_new['id'] = id[0] + 1
        data_new.update(**data)
        query = "INSERT INTO {tabla.nombre} ({columnas}) VALUES ({placeholders})"
        self.db_connection.execute(query, tuple(data_new.values()))
        self.db_connection.commit()
        #return self.db_connection.lastrowid -> debe ser el cursor
        return data_new['id']

    def update_{tabla.nombre}(self, id, data):
        query = f"UPDATE {tabla.nombre} SET {set_clause} WHERE id = ?"
        self.db_connection.execute(query, tuple(data.values()) + (id,))
        self.db_connection.commit()
        return 0  # ok

    def delete_{tabla.nombre}(self, id):
        query = "DELETE FROM {tabla.nombre} WHERE id = ?"
        self.db_connection.execute(query, (id,))
        self.db_connection.commit()
        return 0  # ok
"""
        with open(f"{settings.TAREA_PATH}/daos/{tabla.nombre.capitalize()}DAO.py", 'w') as f:
            f.write(dao_content)
    utils.printInfo(f'2. DAOs  generados: {", ".join([t.nombre for t in metadatos.tablas])}')


# Autocargador de programa externo
if __name__ == "__main__":
    main()
