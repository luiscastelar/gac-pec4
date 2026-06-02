from .contentOfFile import File
from .utils import printInfo

# Variables globales
settings = None
logging = None


def generarIndex(metadatos, env) -> None:
    """
    Genera la página índice de la aplicación de salida mediante sustitución
    con plantilla común y fragmentos por tabla

    param metadatos: metadatos de la base de datos
    param env: variables de entorno con configuración de db y salida
    """
    logging.debug(f'Variables entorno en {__file__}: {env}')
    # DONE: Posible pagina índice de tablas
    plantillaIn = settings.TAREA_PATH + 'templates/' + env['tipoSalida'] + '/'
    plantillaOut = settings.TAREA_PATH + 'salida/' + env['tipoSalida'] + '/'
    plantillaBoton = File().load(plantillaIn + 'boton.template')
    alturaVentana = len(metadatos.tablas) * 50 + 50  # altura variable

    botones = ''
    uiId = 1  # Identif. de elemento gráfico
    for tabla in metadatos.tablas:
        boton = plantillaBoton.replace('%%ID%%', str(uiId))
        uiId += 1
        botones += boton.replace('%%TEXTO%%', tabla.nombre)+'\n'
        print(f'-> {tabla.nombre}')
    ventanaMain = File().load(plantillaIn + env['indexFile']).replace('%%BOTONES%%', botones)
    ventanaMain = ventanaMain.replace('%%ALTURA%%', str(alturaVentana))
    ventanaMain = ventanaMain.replace('%%UI_TYPE%%', env['tipoSalida'])
    ventanaMain = ventanaMain.replace('%%TIPO_DB%%', env['TIPO_DB'])
    logging.debug(ventanaMain)
    File().save(plantillaOut + env['indexFile'], ventanaMain)


def generarCRUD(tabla, db, env) -> None:
    plantillaIn = settings.TAREA_PATH + 'templates/' + env['tipoSalida'] + '/'
    plantillaOut = settings.TAREA_PATH + 'salida/' + env['tipoSalida'] + '/'
    plantillaTabla = File().load(plantillaIn + 'tabla.' + env['tipoSalida'])

    pdoType = db.comandosSQL['pdo_type'].replace("%%DB%%", db.name)
    contenidoTabla = plantillaTabla.replace('%%PDO_TYPE%%', pdoType)
    contenidoTabla = contenidoTabla.replace('%%UI_TYPE%%', env['tipoSalida'])
    contenidoTabla = contenidoTabla.replace('%%TIPO_DB%%', env['TIPO_DB'])
    contenidoTabla = contenidoTabla.replace('%%TABLA_NOMBRE%%', tabla.nombre)

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
    File().save(plantillaOut + f'tabla_{tabla.nombre}.' + env['tipoSalida'], contenidoTabla)


def buildApp(env):
    plantillaIn = settings.TAREA_PATH + 'templates/' + env['tipoSalida'] + '/'
    plantillaOut = settings.TAREA_PATH + 'salida/' + env['tipoSalida'] + '/'
    if env['tipoSalida'] == 'php':
        printInfo(f'''Aplicación funcionando en http://localhost:{env["WWW_PORT"]}

        ***********************************************************************************************
        * Verifica que tu servidor web local está corriendo mediante el contenedor docker facilitado. *
        * En caso contrario puedes lanzarlo desde cli mediante el comando `docker compose up -d`.     *
        ***********************************************************************************************
        ''')
        varEnv = f'''HOST={env["SERVER_DB"]}
DB={env["DOCKER_DB"]}
USER={env["USER_DB"]}
PASS={env["PASS_DB"]}
TIPO_DB={env["TIPO_DB"]}
'''
        File().save(plantillaOut + '.env', varEnv)
        import shutil
        shutil.copytree(plantillaIn + '/css', plantillaOut + 'css', dirs_exist_ok=True)
        shutil.copytree(plantillaIn + '/js', plantillaOut + 'js', dirs_exist_ok=True)
        import os  # , stat
        os.chmod(settings.TAREA_PATH + env['NAME_DB'], 0o777)

        # Primera vez copiar bbdd si es sqlite
        file = env["SERVER_DB"]
        src = ''+file
        dst = f'salida/{env["tipoSalida"]}/{file}'
        if env["TIPO_DB"] == 'sqlite':
            if not os.path.exists(dst):
                shutil.copy(src, dst)
                print(f"Se instala la base de datos sqlite en {dst}")
