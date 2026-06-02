from .dbTipo import DbTipo
import mysql.connector


class DbMariadb(DbTipo):
    """
    Implementación del DAO de gestión de la base de datos.
    """

    def __init__(self, logging=None):
        super().__init__(logging)  # llamamos al constructor del padre

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
        if (host == 'mariadb'):
            # Corrección necesaria para conexiones vía docker
            host = 'localhost'
        self.conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbName)
        self.name = dbName
        return self.conn

    def dropDB(self):
        """
        Elimina una base de datos si existe.

        :return: False si no se ha podido eliminar la base de datos, True si se
                 ha eliminado correctamente
        """
        cursor = None
        error = False
        try:
            dbName = self.conn.database
            cursor = self.conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS `{dbName}`;")
            self.conn.commit()
            self.printInfo(f"Base de datos '{dbName}' eliminada (si existía).")

        except mysql.connector.Error as err:
            self.printError(f"Error al eliminar la base de datos '{dbName}': {err}")
            error = True

        finally:
            if cursor:
                cursor.close()

        return True if not error else False

    def createDB(self, dbName):
        """
        Crea una base de datos si no existe.

        :param dbName: nombre de la base de datos
        :return: La conexión actual
        """
        cursor = None
        error = False
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{dbName}` "
                "CHARACTER SET utf8mb4 "
                "COLLATE utf8mb4_unicode_ci;"
            )
            self.conn.commit()
            self.printInfo(f"Base de datos '{dbName}' creada o ya existente.")

        except mysql.connector.Error as err:
            self.printError(f"Error al crear la base de datos '{dbName}': {err}")
            error = True

        finally:
            if cursor:
                cursor.close()

        # ¿La db es diferente?
        actual = self.conn.database
        if actual != dbName:
            self.printInfo(f"Cambiando a la base de datos '{dbName}'...")
            newConn = mysql.connector.connect(
                host=self.conn._host,
                port=self.conn._port,
                user=self.conn._user,
                password=self.conn._password,
                database=dbName)
            self.conn.close()  # Cerramos la conexión anterior
            self.conn = newConn
            self.name = dbName
        else:
            newConn = self.conn

        return newConn if not error else None

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
            statement = ""
            for line in sql.splitlines():
                line = line.strip()

                # Ignorar comentarios y líneas vacías
                if not line or line.startswith("--") or line.startswith("/*"):
                    continue

                statement += line + " "

                # Fin de sentencia
                if line.endswith(";"):
                    cursor.execute(statement)
                    statement = ""

            self.conn.commit()
            self.printInfo("Script sql ejecutado correctamente.")

        except mysql.connector.Error as err:
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
        lista = self.read(sql)
        simpleList = []
        for ele in lista:
            simpleList.append(self.dictToList(ele))
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
        cursor = self.conn.cursor()
        afectadas = 0
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, valores)
            self.conn.commit()
            afectadas = cursor.rowcount

        except mysql.connector.Error as err:
            self.printError(f"Error en la inserción sobre '{self.conn.database}': {err}")
            afectadas = -1

        finally:
            if cursor:
                cursor.close()

        if afectadas > 0:
            self.printInfo(f"Insertados/Actualizados/Borrados {afectadas} registros sobre {self.conn.database}.")
        elif afectadas == 0:
            self.printInfo(f"Ninguna fila afectada con la consulta '{sql}'.")
        else:
            self.printError("Ocurrió un error")

    def read(self, sql):
        """
        Devuelve una lista de [ diccionario {atributo: valor} ]
        """
        cursor = self.conn.cursor(buffered=True, dictionary=True)
        filasLeidas = []
        try:
            cursor.execute(sql)
            self.logging.debug(f'Lectura {sql} correcta')
            filasLeidas = cursor.fetchall()
        finally:
            cursor.close()
        return filasLeidas

    def dictToList(self, ele):
        """
        De un diccionario, devuelve una lista con los valores del diccionario
        (sin las claves).

        :param ele: elemento a convertir
        """
        lista = []
        for v in ele.values():
            lista.append(v)
        return lista
