# *****************************************************************************
#   Archivo generado desde plantilla -> NO TOCAR                              *
# *****************************************************************************
# ----------------------------------------------------------------------------
# Plantilla: WORKER
# ----------------------------------------------------------------------------
def worker(payload: dict) -> dict:
    """Procesador de tareas (llama a los DAO)"""
    log.debug(f"Procesando: {payload}")

    # retardo para simular carga de la base de datos
    import time
    time.sleep(2)


    coleccion = payload.get('coleccion', '')
    id = payload.get('id', None)
    ope = payload.get('ope', None)
    match coleccion:
        case 'alumnos':
            from daos.AlumnosDAO import AlumnosDAO
            vAlumnosDAO = AlumnosDAO( db_file )
            match ope:
                case 'read':
                    result = vAlumnosDAO.get_alumnos( id )
                case 'create':
                    result = vAlumnosDAO.create_alumnos( payload.get('data', {}) )
                case 'update':
                    result = vAlumnosDAO.update_alumnos( id, payload.get('data', {}) )
                case 'delete':
                    result = vAlumnosDAO.delete_alumnos( id )
                case _:
                    result = "Método no soportado"

            # Traducimos SQL code a HTTP code
            if result is None:  # No return
                code = 500
            else:               # SQL ok -> code 0 or 101:
                code = 200

            return {
                "code": code,
                "payload": payload,
                "res": result
            }

        case 'calificaciones':
            from daos.CalificacionesDAO import CalificacionesDAO
            vCalificacionesDAO = CalificacionesDAO( db_file )
            match ope:
                case 'read':
                    result = vCalificacionesDAO.get_calificaciones( id )
                case 'create':
                    result = vCalificacionesDAO.create_calificaciones( payload.get('data', {}) )
                case 'update':
                    result = vCalificacionesDAO.update_calificaciones( id, payload.get('data', {}) )
                case 'delete':
                    result = vCalificacionesDAO.delete_calificaciones( id )
                case _:
                    result = "Método no soportado"

            # Traducimos SQL code a HTTP code
            if result is None:  # No return
                code = 500
            else:               # SQL ok -> code 0 or 101:
                code = 200

            return {
                "code": code,
                "payload": payload,
                "res": result
            }
        
        case _:
            return {'code': 500, 'error': f'Coleccion {coleccion} incorrecta'}

# ----------------------------------------------------------------------------
