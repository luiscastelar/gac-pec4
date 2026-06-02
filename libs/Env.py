from libs.contentOfFile import File

__all__ = ['Env']


class Env():

    def get(ruta) -> list[dict]:
        CLAVE = 0
        VALOR = 1
        archivoEnv = File().load(ruta)

        variablesDeEntorno = {}
        for linea in archivoEnv.split('\n'):
            pares = linea.split('=', 1)
            # Sólo partimos por el primer "=". Ésto nos premite que el valor
            # tenga "="
            if len(pares) >= 2:
                # que tenga al menos clave y valor
                key = pares[CLAVE]
                value = pares[VALOR]
                variablesDeEntorno[key] = value
        return variablesDeEntorno
