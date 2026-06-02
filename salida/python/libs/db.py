from .dbTipo import DbTipo
import os
import sqlite3


class DbSqlite(DbTipo):
    """
    Implementación del DAO de gestión de la base de datos.
    """
    def __init__(self, logging=None):
        super().__init__(logging)  # llamamos al constructor del padre
        # Ruta del proyecto
        self.TAREA_PATH = os.path.dirname(__file__)[:-len('libs')]

    def getConn(
            self,
            host='sqlite-gap2.db',
            port=None,
            user=None,
            password=None,
            dbName=None):
        """Estandarizamos la conexión a bbdd

        :param host: Host de la base de datos
        :param port: no procede
        :param user: no procede
        :param password: no procede
        :param dbName: no procede
        :return: Conexión a la base de datos
        """
        self.fileDB = self.TAREA_PATH + host
        self.printInfo(f"3. Conectando a la base de datos SQLite en '{self.fileDB}'...")
        self.conn = sqlite3.connect(self.fileDB)
        self.name = host
        return self.conn

    def dropDB(self):
        """
        Elimina una base de datos si existe.

        :return: False si no se ha podido eliminar la base de datos, True si se
                 ha eliminado correctamente
        """
        error = False
        try:
            from pathlib import Path
            Path.unlink(self.fileDB)
            self.printInfo('3.1. BBDD eliminada')

        except sqlite3.Error as err:
            self.printError(f"Error al eliminar la base de datos '{self.name}': {err}")
            error = True

        return True if not error else False

    def createDB(self, dbName):
        """
        Crea una base de datos si no existe.

        :param dbName: nombre de la base de datos
        :return: La conexión actual (para el caso de SQLite)
        """

        conexion = self.getConn(self.name, None, None, None)
        if conexion is not None:
            self.printInfo(f'3.2. BBDD "{self.name}" creada nuevamente')
            return conexion
        else:
            self.printError(f'Problemas creando la "{self.name}"')
        return None

    def loadFromSQL(self, sql):
        """
        Ejecuta un fichero SQL completo (DDL + DML) sobre una conexión MySQL.

        :param sql: contenido del fichero sql
        :return: False si no se ha podido ejecutar el script SQL, True si se ha
                 ejecutado correctamente
        """
        cursor = self.conn.cursor()
        error = False
        try:
            cursor = self.conn.cursor()
            cursor.executescript(sql)
            self.printInfo("3.3. Script sql ejecutado correctamente.")

        except sqlite3.Error as err:
            self.conn.rollback()
            self.printError(f"Error ejecutando el script SQL: {err}")
            error = True

        finally:
            cursor.close()

        if error:
            raise Exception("Error ejecutando el script SQL")
        else:
            return True

    def readSimpleList(self, sql: str) -> list[list[str]]:
        """
        Select ... -> lista (filas) de listas (columnas)

        :param sql: consulta SQL a ejecutar
        :type sql: str
        :return: lista de listas con los resultados de la consulta SQL
        :rtype: list[list[str]]
        """
        listOfTuples = self.read(sql)
        salida = []
        for fila in listOfTuples:
            arrayFila = []
            for ele in fila:
                arrayFila.append(ele)
            salida.append(arrayFila)
        return salida

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
        cursor = self.conn.cursor()
        afectadas = 0
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, valores)
            self.conn.commit()
            afectadas = cursor.rowcount

        except sqlite3.Error as err:
            self.conn.rollback()
            self.printError(f"Error en la inserción/actualización/borrado sobre '{self.name}': {err}")
            afectadas = -1

        finally:
            if cursor:
                cursor.close()

        if afectadas > 0:
            self.printInfo(f"Insertados/Actualizados/Borrados {afectadas} registros sobre {self.name}.")
        elif afectadas == 0:
            self.printInfo(f"Ninguna fila afectada con la consulta '{sql}'.")
        else:
            self.printError("Ocurrió un error")

    def read(self, sql):
        """
        Devuelve una lista [ de tuplas de (atributos, valores) ]
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.logging.debug(f'Lectura {sql} correcta')
            return cursor.fetchall()

        except sqlite3.Error as err:
            self.printError(f"Error en la inserción/actualización/borrado sobre '{self.name}': {err}")

        finally:
            cursor.close()
