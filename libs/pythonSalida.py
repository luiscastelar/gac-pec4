from .contentOfFile import File
from .utils import printInfo
import shutil
from os import mkdir

# Var globales
settings = None
logging = None


def generarIndex(metadatos, env) -> None:
    """
    Genera la página índice de la aplicación de salida mediante sustitución
    con plantilla común y fragmentos por tabla

    param metadatos: metadatos de la base de datos
    param env: variables de entorno con configuración de db y salida
    """
    settings.logging.debug(f'Variables entorno en {__file__}: {env}')

    # DONE: Posible pagina índice de tablas
    plantillaIn = settings.TAREA_PATH + 'templates/' + env['tipoSalida'] + '/'
    plantillaOut = settings.TAREA_PATH + 'salida/' + env['tipoSalida'] + '/'
    plantillaBoton = File().load(plantillaIn + 'boton.template')
    plantillaAccionBoton = File().load(plantillaIn + 'accion_boton.template')
    alturaVentana = len(metadatos.tablas) * 50 + 50  # altura variable

    botones = ''
    acciones = ''
    for i, tabla in enumerate(metadatos.tablas):
        boton = plantillaBoton.replace('%%FILA%%', str(i+1))
        # dejamos el hueco para el mensaje superior
        botones += boton.replace('%%TEXTO%%', tabla.nombre)+'\n'
        print(f'-> {tabla.nombre}')

        acciones += plantillaAccionBoton.replace('%%TEXTO%%', tabla.nombre)

    ventanaMain = File().load(plantillaIn + env['indexFile']).replace('%%BOTONES%%', botones)
    ventanaMain = ventanaMain.replace('%%ALTURA%%', str(alturaVentana))
    ventanaMain = ventanaMain.replace('%%ACCIONES_DE_BOTONES%%', acciones)

    # DB: %%TIPO_DB%% ➡️ UI: %%UI_TYPE%%
    ventanaMain = ventanaMain.replace('%%UI_TYPE%%', env['tipoSalida'])
    ventanaMain = ventanaMain.replace('%%TIPO_DB%%', env['TIPO_DB'])
    logging.debug(ventanaMain)
    File().save(plantillaOut + env['indexFile'], ventanaMain)


def generarCRUD(tabla, db, env) -> None:
    logging.info(f'Generando CRUD para tabla {tabla.nombre}...')
    logging.info(f'DB: {db.name}, Tipo de salida: {env["tipoSalida"]}')
    HOST = env["SERVER_DB"]
    USER = env["USER_DB"]
    PASS = env["PASS_DB"]
    TIPO_DB = env["TIPO_DB"]

    plantillaIn = settings.TAREA_PATH + 'templates/' + env['tipoSalida'] + '/'
    plantillaOut = settings.TAREA_PATH + 'salida/' + env['tipoSalida'] + '/'

    # Importo el driver db y librerías creadas
    try:
        mkdir(plantillaOut + 'libs/')
    except:
        pass
    try:
        mkdir(plantillaOut + 'templates/')
    except:
        pass

    import os
    os.listdir(settings.TAREA_PATH)
    shutil.copy(settings.TAREA_PATH + f'libs/db{TIPO_DB.capitalize()}.py', plantillaOut + 'libs/db.py')
    shutil.copy(settings.TAREA_PATH + 'templates/' + TIPO_DB + '/sql', plantillaOut + 'templates/')

    filesToCopy = [
                    'dbComun.py', 'Env.py', 'contentOfFile.py', 'TUI.py',
                    'utils.py', 'baseDatos.py', 'tabla.py', 'columna.py',
                    'dbTipo.py'
                    ]
    [shutil.copy(settings.TAREA_PATH + f'libs/{dir}', plantillaOut+'libs/') for dir in filesToCopy]
    plantillaTabla = File().load(plantillaIn + 'table.py')
    contenidoTabla = plantillaTabla.replace('%%DB%%', db.name)
    contenidoTabla = contenidoTabla.replace('%%HOST%%', HOST)
    contenidoTabla = contenidoTabla.replace('%%USER%%', USER)
    contenidoTabla = contenidoTabla.replace('%%PASS%%', PASS)
    contenidoTabla = contenidoTabla.replace('%%PORT_DB%%', env['PORT_DB'])
    contenidoTabla = contenidoTabla.replace('%%TIPO_DB%%', env['TIPO_DB'])
    contenidoTabla = contenidoTabla.replace('%%TABLA_NOMBRE%%', tabla.nombre)

    jsonColumnas = '['
    for columna in tabla.columnas:
        jsonColumnas += f'"{columna.COLUMN_NAME}", '
    jsonColumnas = jsonColumnas[:-2]+']'

    contenidoTabla = contenidoTabla.replace('%%COLUMNAS%%', jsonColumnas)

    # Columnas
    nombresDeCampos = ''
    bindCampos = ''
    postCampos = ''
    formCreateCampos = ''
    readColumns = ''
    readDatos = ''
    columnaPK = None
    updateBindCampos = ''
    updatePostCampos = ''

    for columna in tabla.columnas:
        nombre = columna.COLUMN_NAME
        # Form
        dataType = db.convertDataType(columna.DATA_TYPE)
        required = 'required' if columna.IS_NULLABLE.upper() == 'NO' else ''

        # Create
        nombresDeCampos += nombre + ', '
        bindCampos += '?, '
        postCampos += f'\t$_POST["{nombre}"],\n'
        formCreateCampos += f'<div class="mb-3">\t<label class="form-label">{nombre.upper()}</label>\n<input type="{dataType}" name="{nombre}" class="form-control" {required} /></div>\n'

        # Read
        readColumns += f'\t<th>{nombre.capitalize()}</th>\n'
        readDatos += f'\t<td><?= htmlspecialchars($fila["{nombre}"]) ?></td>\n'

        # Update
        if columna.COLUMN_KEY == 'PRI':
            columnaPK = columna.COLUMN_NAME
            logging.debug(f'Columna PK detectada: {columnaPK}')
        else:
            updateBindCampos += f'{nombre} = ?, '
            updatePostCampos += f'\t\t$_POST["{nombre}"],\n'

    updateBindCampos = updateBindCampos[:-2] + f'\n\t\tWHERE {columnaPK} = ? ;'
    updatePostCampos += f'\t\t$_POST["{columnaPK}"]'

    # quitamos última coma y espacio
    nombresDeCampos = nombresDeCampos[:-2]
    bindCampos = bindCampos[:-2]
    postCampos = postCampos[:-2]

    contenidoTabla = contenidoTabla.replace('%%NOMBRES_DE_CAMPOS%%', nombresDeCampos)
    contenidoTabla = contenidoTabla.replace('%%BIND_CAMPOS%%', bindCampos)
    contenidoTabla = contenidoTabla.replace('%%POST_CAMPOS%%', postCampos)
    contenidoTabla = contenidoTabla.replace('%%FORM_CREATE_CAMPOS%%', formCreateCampos)
    contenidoTabla = contenidoTabla.replace('%%READ_COLUMNS%%', readColumns)
    contenidoTabla = contenidoTabla.replace('%%READ_DATOS%%', readDatos)
    contenidoTabla = contenidoTabla.replace('%%UPDATE_BIND_CAMPOS%%', updateBindCampos)
    contenidoTabla = contenidoTabla.replace('%%POST_UPDATE_CAMPOS%%', updatePostCampos)
    contenidoTabla = contenidoTabla.replace('%%CAMPO_KEY%%', columnaPK)

    columnasDef = f'// Tabla: {tabla.nombre}\n'
    for columna in tabla.columnas:
        columnasDef += f'//  + {columna.COLUMN_NAME} : {columna.DATA_TYPE}\n'
    contenidoTabla = contenidoTabla.replace('%%COLUMNAS_DEF%%', columnasDef)
    # Guardado
    File().save(plantillaOut + f'tabla_{tabla.nombre}.py', contenidoTabla)


def buildApp(env):
    plantillaOut = settings.TAREA_PATH + 'salida/' + env['tipoSalida'] + '/'
    salida = plantillaOut + 'crud.py'
    printInfo(f"Lanzar aplicación con 'python3 {salida}'")

    # Primera vez copiar bbdd si es sqlite
    import os
    file = env["SERVER_DB"]
    src = ''+file
    dst = f'salida/{env["tipoSalida"]}/{file}'
    if env["TIPO_DB"] == 'sqlite':
        if not os.path.exists(dst):
            shutil.copy(src, dst)
            print(f"Se instala la base de datos sqlite en {dst}")
    return None
