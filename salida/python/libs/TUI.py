import re

__all__ = ['getTypeDDL']

# Var global
settings = None


def getTypeDDL(tipo: str) -> int:
    match tipo.lower():
        case '.sql':
            return 1
        case '.json':
            return 2
        case '.dbml':
            return 3
        case _:
            txt = '''
                Formato de entrada del archivo DDL:
                1. SQL
                2. Json Schema
                3. DBML
                0. Otro
                '''
            elec = int(input(txt))
            if elec == 0:
                print('Formato no soportado aún. Deberás convertirlo con alguna otra herramienta')
                settings.logging.error('Formato de esquema no soportado')
                quit(1)

            return elec


def getTipoDB(sql: str) -> str:
    flags = re.IGNORECASE | re.MULTILINE
    if re.search('mariadb|mysql', sql, flags) is not None:
        # cat dump-gac2.sql | egrep --quiet --ignore-case 'mysql|mariadb' -> 0 ok y 1 NO
        return 'mariadb'
    elif re.search('sqlite', sql, flags) is not None:
        return 'sqlite'
    else:
        print(sql)
        txt = ''''
            No hemos reconocido el formato SQL de origen.
            ¿Es alguno de los siguientes?
            1. mariadb/mysql
            2. sqlite
            3. oracle-xe
            0. otro
            '''
        elec = int(input(txt))
        if elec == 0:
            msg = 'Formato sql no reconocido'
            settings.logging.error(msg)
            print(msg)
            quit(1)

        return elec


def operacionesDeImportacion() -> int:
    MIN = 1
    MAX = 3
    error = -1
    txt = '''
        Desea:
        1. Borrar los datos actuales y cargar los del archivo
        2. Cargar los del archivo conservando los actuales (que se puedan)
        3. Dejar los actuales e ignorar el archivo
        '''
    elec = int(input(txt))
    if MIN <= elec <= MAX:
        return elec
    else:
        return error


def eleccionDeSalida(tipo) -> tuple[str, str]:
    txt = ''''
        Seleccione el formato de salida:
        1. Python (CRUD)
        2. PHP (MVC)
        3. Java (JSP)  -- TODO
        0. Otro
        '''
    match tipo:
        case 0:  # Interactivo
            elec = int(input(txt))
        case 1:  # python
            elec = 1
        case 2:  # php
            elec = 2
        case _:  # Elección NO válida
            print(f'Selección NO válida {tipo}')
            exit(1)

    match elec:
        case 1:
            return 'python', 'crud.py'
        case 2:
            return 'php', 'index.php'
        case 3:
            return 'jsp', 'index.jsp'
        case _:
            msg = 'Formato de salida no soportado aún. Deberás implementarlo con alguna otra herramienta'
            settings.logging.error(msg)
            print(msg)
            quit(1)
    settings.logging.debug(f'Elección de salida: {elec}')
