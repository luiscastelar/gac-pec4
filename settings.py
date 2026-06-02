import os
import logging

# ---------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------
TAREA_PATH = os.path.dirname(__file__) + '/'
realPathDB = ''

LOGGING = logging.INFO       # modo de depuración

FILE_LOGGIN = TAREA_PATH + 'app.log'
ENV='.env'
ENTRADAS = {
   'MARIADB': 'mariadb',
   'ORACLE' : 'oracle-xe',
   'SQLITE' : 'sqlite'    
}
EXIT = {
    'SUCCESS': 0,
    'GENERAL': 1,
    'INCORRECT': 2, 
    'INVALID_ARG': 3,
    'NOT_DEVICE':6,
    'FORMAT_ERROR': 65,
    'IO_ERROR': 74,
    'PERMISS': 126,
    'NOT_FOUND': 127,
    'INVALID_EXIT': 128,
    'OUT_OF_RANGE': 255
}

# Diccionario de códigos de salida basado en las fuentes de Linux/Unix
exitCode = {
    # Códigos Estándar (0–255)
    "Success": 0,
    "General Error": 1,
    "Misuse of Shell Builtins": 2,
    "Command Usage Error": 64,
    "Data Format Error": 65,
    "Cannot Open Input": 66,
    "Addressee Unknown": 67,
    "Hostname Unknown": 68,
    "Service Unavailable": 69,
    "Internal Software Error": 70,
    "System Error": 71,
    "Critical OS File Missing": 72,
    "Can't Create Output File": 73,
    "I/O Error": 74,
    "Temporary Failure": 75,
    "Remote Protocol Error": 76,
    "Permission Denied": 77,
    "Configuration Error": 78,
    "Command Not Executable": 126,
    "Command Not Found": 127,
    "Invalid Exit Argument": 128,
    "Exit Status Out of Range": 255,

    # Códigos Reservados y Específicos de Aplicaciones (79–125)
    "Permission Issue": 79,
    "Remote/Host Error": 100,
    "Capabilities Required": 101,
    "Filesystem Error": 102,
    "Service Unresponsive": 108,
    "Temporary Failure (Specific)": 109,
    "Timeout": 124,
    "Partial Success": 125,

    # Códigos relacionados con Señales (128 + Número de Señal)
    "SIGHUP": 129,
    "SIGINT (Interrupted by Ctrl+C)": 130,
    "SIGQUIT": 131,
    "SIGILL": 132,
    "SIGTRAP": 133,
    "SIGABRT": 134,
    "SIGBUS": 135,
    "SIGFPE": 136,
    "SIGKILL": 137,
    "SIGSEGV (Segmentation fault)": 139,
    "SIGTERM (Graceful termination)": 143,
    "SIGSTOP": 147,

    # Códigos para Apps/Scripts (193–254)
    "Custom success with warnings": 200,
    "Reserved for runtime limits": 201,
    "External dependency failed": 202,
    "Checksum mismatch": 203,
    "Graceful shutdown requested": 250,
    "Dry-run or simulation mode detected": 253,
    "Conditional not executed": 254
}

# ---------------------------------------------------------------------
# Variables globales
# ---------------------------------------------------------------------
#servidor = {}



# ---------------------------------------------------------------------
# # Opciones de depuración:
#  - DEBUG, INFO, WARNING, ERROR, CRITICAL
# ---------------------------------------------------------------------
def initLoggin():
    logging.basicConfig(filename = FILE_LOGGIN,
                            filemode = 'a',
                            level = LOGGING,
                            format='''%(asctime)s - f:%(module)s:%(lineno)d [%(levelname)s]:\n%(message)s''')
    return logging

logger = initLoggin()