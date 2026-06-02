import os
import re

__all__ = ['File']


class File():
    """
    Clase para gestión de archivos del sistema.
    Ofrece:
      - Carga segura
      - Volcado seguro
      - Ruta de archivo (tipo realPath() de bash)
      - esRuta abtoluta que nos indica si es absoluta (True) o relativa (False)
    """

    def load(self, filepath):
        """
        Retorna todo el contenido del archivo o da error y finaliza programa
        """
        EMPTY = 0  # constante
        if len(filepath) == EMPTY:
            filepath = self.getRuta()

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()

        except IOError as e:
            print(f'Fallo de lectura: {e}')
            quit(2)

    def save(self, filepath, content):
        """
        Vuelca contenido en archivo o da error y finaliza programa.

        ADVERTENCIA: Sobreescribe el contenido anterior
        """

        if len(filepath) == 0:
            filepath = self.getRuta()

        # Crea el directorio si no existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

        except IOError as e:
            print(f'Write failed: {e}')
            quit(2)

    def getRuta(self) -> str:
        """
        Obtiene la ruta real del archivo.

        - Si le damos una ruta absoluta la devuelve
        - Si le damos una ruta relativa, obtiene la absoluta y la devuelve

        _Nota: Debería exportarse a TUI_
        """

        filepath = input('Introduce el nombre del archivo (ruta completa o relativa a la aplicación): ')
        if not self.esRutaAbsoluta(filepath):
            # Si la ruta es relativa corregimos
            filepath = os.path.dirname(__file__) + '/' + filepath
        return filepath

    def esRutaAbsoluta(self, ruta: str) -> bool:
        FIRST_CHAR = 0  # constante
        if ruta[FIRST_CHAR] == '/':
            # Ruta absoluta en Unix
            return True

        match = re.search('^\\w:', ruta)
        if match is not None:
            # Ruta absoluta en Windows
            return True

        # Ruta relativa
        return False
