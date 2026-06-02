class DbTipo:
    """
    DAO de gestión de la base de datos de forma transparente a la tecnología.
    """

    def __init__(self, logging=None):
        self.logging = logging
        self.__conn = None      # inicializo var conexión
        self.__name = None      # inicializo var nombre de la db
        self.comandosSQL = {}   # inicializo dict de comandos normalizados

    @property
    def conn(self):
        """Getter conexion a la base de datos"""
        return self.__conn

    @conn.setter
    def conn(self, value):
        """Setter conexion a la base de datos"""
        self.__conn = value

    @property
    def name(self):
        """Getter nombre de la base de datos"""
        return self.__name

    @name.setter
    def name(self, value):
        """Setter nombre de la base de datos"""
        self.__name = value

    def getConn(
            self,
            host='localhost',
            port=None,
            user=None,
            password=None,
            dbName=None
            ):
        """Estandarizamos la conexión a bbdd

        :param host: Host de la base de datos
        :param port: Puerto de la base de datos
        :param user: Usuario de la base de datos
        :param password: Contraseña de la base de datos
        :param dbName: Nombre de la base de datos
        :return: Conexión a la base de datos
        """
        self.__conn = None
        self.__name = dbName
        return self.__conn

    def dropDB(self):
        """
        Elimina una base de datos si existe.

        :return: False si no se ha podido eliminar la base de datos, True si se
                 ha eliminado correctamente
        """
        return False

    def createDB(self, dbName):
        """
        Crea una base de datos si no existe.

        :param dbName: nombre de la base de datos
        :return: La conexión actual (para el caso de SQLite)
        """
        return None

    def loadFromSQL(self, sql):
        """
        Ejecuta un fichero SQL completo (DDL + DML) sobre una conexión MySQL.

        :param sql: contenido del fichero sql
        :return: False si no se ha podido ejecutar el script SQL, True si se ha
                 ejecutado correctamente
        """
        return False

    def readSimpleList(self, sql: str) -> list[list[str]]:
        """
        Select ... -> lista (filas) de listas (columnas)

        :param sql: consulta SQL a ejecutar
        :type sql: str
        :return: lista de listas con los resultados de la consulta SQL
        :rtype: list[list[str]]
        """
        simpleList = []
        return simpleList

    def execute(self, sql, valores: tuple) -> int:
        """
        Es la ejecución de una consulta preparada.

        :param self: el objeto db
        :param sql: la SENTENCIA
        :param valores: los valores
        :type valores: tupla
        :return: las filas afectadas o -1 si error
        :rtype: entero
        """
        return False

    def convertDataType(self, tipo: str) -> str:
        """
        Convierte un tipo de dato SQL a un tipo de dato Python.

        :param tipo: tipo en SQL a convertir
        :type tipo: str
        :return: tipo de dato en Python equivalente al tipo de dato SQL
                 proporcionado
        :rtype: str
        """
        match(tipo):
            case 'int':
                return 'number'
            case 'varchar':
                return 'text'
            case _:
                return 'text'

    def printInfo(self, msg):
        self.logging.info(msg)
        print(msg)

    def printError(self, msg):
        self.logging.error(msg)
        print(f'ERROR: {msg}')
