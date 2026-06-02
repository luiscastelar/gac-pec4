class BaseDatos:
    """
    Clase que representa una base de datos, con un nombre y una lista de
    tablas.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.tablas = []

    def __str__(self):
        """
        Devuelve la representación de la base de datos
        """

        txt = f"DB: {self.nombre}. Tablas:\n"
        for tabla in self.tablas:
            txt += f'  + {tabla.str()}'
        return txt
