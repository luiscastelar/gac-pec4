class Tabla:

    def __init__(self, nombre):
        self.nombre = nombre
        self.columnas = []

    def str(self):
        txt = f"{self.nombre}\n"
        for c in self.columnas:
            txt += f'{c.str()}\n'

        return txt
