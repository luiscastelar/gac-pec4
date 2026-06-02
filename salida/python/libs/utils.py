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
