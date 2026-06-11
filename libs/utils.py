from libs.Env import Env

settings = None


def printError(msg, err=None):
    """
    Docstring para printError

    :param msg: texto
    :param err: código de salida
    """
    if err is None:
        err = -1
    try:
        settings.logging.error(msg)
        print(msg)
        exit(err)
    except:
        import inspect
        print(f"""Error: No se pudo realizar el logging de datos.
Contacta con el administrador. ({__file__}:{inspect.currentframe().f_lineno})""")


def printInfo(msg):
    """
    Docstring para printInfo

    :param msg: texto
    """
    settings.logging.info(msg)
    print(msg)


def loadEnvironmentVar(tipoDB: str) -> dict:
    # DONE: 3. Captura de variables de entorno comunes a todos los tipos de salida
    variablesDeEntorno = {}
    variablesDeEntorno['TIPO_DB'] = tipoDB
    variablesDeEntorno.update(
        Env.get(settings.TAREA_PATH + 'config/' + tipoDB + '/config')
    )
    settings.logging.debug(f'Datos conexión a variablesDeEntorno: {variablesDeEntorno}')
    if len(variablesDeEntorno) > 0:
        settings.logging.debug(f'2. Tipo {tipoDB} procesado y datos de conexión recibidos')
    else:
        printError('Error datos de conexion', settings.EXIT['NOT_FOUND'])
    return variablesDeEntorno