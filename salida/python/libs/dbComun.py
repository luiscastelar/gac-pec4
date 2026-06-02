from . import utils
from .baseDatos import BaseDatos
from .tabla import Tabla
from .columna import Columna

"""
Módulo de utilidades relativas a bases de datos

- Obtención del driver adecuado
- Obtención de la conexión a la base de datos
- Obtención de los metadatos de la db
"""

# Diccionario de variables globales
settings = None


def getDriverDB(tipoDB):
    """
    Importación de driver db según tipo (DAO)
    """

    match tipoDB:
        case 'mariadb':
            from .dbMariadb import DbMariadb as db
        case 'sqlite':
            from .dbSqlite import DbSqlite as db
        case 'oracle-xe':
            # Ejemplo de ampliación
            pass
        case _:
            utils.printError(f'Gestor de BBDD {tipoDB} no disponible', settings.EXIT['FORMAT_ERROR'])
    db = db(settings.logging)  # Instanciamos el driver de la base de datos
    return db


def getConexionDB(db, variablesDeEntorno):
    """
    Generamos la conexión a la base de datos
    """
    host = variablesDeEntorno['SERVER_DB']
    port = variablesDeEntorno['PORT_DB']
    user = variablesDeEntorno['USER_DB']
    dbName = variablesDeEntorno['NAME_DB']
    password = variablesDeEntorno['PASS_DB']
    try:
        conn = db.getConn(host, port, user, password, dbName)

    except Exception as e:
        print(f'Error al conectar a la base de datos: {e} (db={host})')
        try:
            # Cuando nos queremos conectar para crear una db nueva
            conn = db.getConn(host, port, user, password, None)

        except Exception as e:
            utils.printError(f'Error al conectar a la base de datos sin especificar el nombre: {e}')
            exit(1)
            return None

    return conn


def generacionDeMetadatos(db):
    """
    Función especial que toma un objeto "db" y nos devuelve los metadatos.

    Nos genera una estructura:
    - Objeto tipo baseDatos.py (nombre de la db)
        |-> Objetos tipo tabla.py (uno por cada tabla de la db)
              |-> Objetos tipo columna.py (uno por cada columna de cada tabla)

    Al realizarse de forma parametrizada por los "comandosSQL" es completamente
    transparente a la tecnología subyacente del gestor del db devolviendo una.
    estructura uniforme y conocida.

    Esta función es clave en mi desarrollo ya que simplifica la captura
    independiente de la tecnología.
    """

    dbName = db.name
    print(f'4. Generando metadatos de la base de datos {dbName}...')

    # Captura de comandos normalizados y enconcreto del "show_tables"
    comandosSQL = db.comandosSQL
    sql = comandosSQL['show_tables'].replace("%%DB%%", dbName)

    # Inicializamos estructura de metadatos con campos/atributos normalizados
    metadatos = BaseDatos(dbName)
    tablas = []
    atributos = [
                    'TABLE_NAME', 'COLUMN_NAME', 'ORDINAL_POSITION',
                    'COLUMN_DEFAULT', 'IS_NULLABLE', 'DATA_TYPE',
                    'CHARACTER_MAXIMUM_LENGTH', 'NUMERIC_PRECISION',
                    'COLUMN_TYPE', 'COLUMN_KEY', 'COLUMN_COMMENT'
                ]

    # Rellenamos la estructura
    INDEX_TABLE_NAME = atributos.index('TABLE_NAME')
    INDEX_COLUMN_NAME = atributos.index('COLUMN_NAME')
    for tab in db.readSimpleList(sql):
        nombreTabla = tab[INDEX_TABLE_NAME]

        # Captura de columnas normalizada
        sql = comandosSQL['show_columns'].replace('%%TABLA%%', nombreTabla)
        columnas = db.readSimpleList(sql)
        tabla = Tabla(nombreTabla)
        for col in columnas:
            columnaNombre = col[INDEX_COLUMN_NAME]
            columna = Columna(columnaNombre)
            for i in range(0, len(col)):
                k = atributos[i]
                v = col[i]
                setattr(columna, k, v)
            tabla.columnas.append(columna)  # añadimos columna a columnas[]
        tablas.append(tabla)                # añadimos tabla a tablas[]
    metadatos.tablas = tablas               # añadimos tablas[] a db
    settings.logging.debug('Metadatos capturados:\n' + metadatos.str())
    return metadatos
