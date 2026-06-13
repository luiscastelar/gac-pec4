# routes.py
# ----------------------------------------------------------------------------
# No requiere personalización mediante plantilla debido a que el propio
# route nos ofrece una personalización completa de rutas y métodos
#
import concurrent.futures
from flask import Blueprint, current_app, jsonify, request, Response, make_response

# Constantes globales
WAIT = 30  # segundos a esperar la respuesta del worker

# Var global
settings = None
api = Blueprint("api", __name__)

"""
Opciones para crear las rutas:

@api.route("/coleccion/<coleccion>/<int:id>", methods=["GET", "POST"])
def nombre(coleccion=None, id=None):
if request.method == 'POST':
    # 1. -> datos = request.get_json()  # Obtenemos objeto enviado
    # 2. -> todos = request.args.to_dict()  # De argumentos a diccionario
    # 3. -> user = request.args.get("name", None)  # argumentos concretos de forma segura
    # 4. -> user = request.form['name']  # para GET y POST de forma insegura
    # 5. -> cabeceras = request.headers  # para cabeceras

# Respuestas:
    # 1. -> Respuesta formada
    response = make_response(render_template('index.html', foo=42), 404)  # el código es opcional
    response.headers['X-Parachutes'] = 'parachutes are cool'
    return response

    return render_template('users.html', users=users)  # Una plantilla html

    headers = {'Content-Type': 'application/json'}
    return "Mensaje de salida", 200, headers  # msg, codigo y cabeceras opcionales
"""
#@user.route('/<user_id>', defaults={'username': None})
#@user.route('/<user_id>/<username>')
@api.route('/API/v1/<coleccion>',
           defaults={'id': 0},
           methods=["GET", "POST", "PUT", "DELETE"]
           )
@api.route("/API/v1/<coleccion>/<int:id>",
           methods=["GET", "POST", "PUT", "DELETE"]
           )
def do(coleccion: str = "", id: int = 0) -> Response:
    """Actuación frente a una petición http.

    GET: Puede recibir un parámetro opcional que es el "id" del elemento
        solicitado que será devuelto como json-diccionario.
        Si no se recibe el parámetro o se recibe el 0, se devuelve la
        colección completa.
        Devuelve un json con:
        - ok: true si la colección existe
        - [code]: codigo de error SQL si procede
        - [array]: con el elemento solicitado o todos
    POST: Debe recibir un json con:
        - coleccion: nombre de la tabla
        - objeto-diccionario: con pares clave, valor de la tabla
        - [opcional]: en un futuro puede recibir objetos relacionados
          con la tabla actual para satisfacer relaciones.
        Devuelve un json con:
        - ok: true si fue creado con éxito
        - [code]: codigo de error SQL si no fue creado con éxito
        - [id]: identificador del objeto creado
    PUT: igual que POST pero con el parámetro OBLIGATORIO id que
        marcará el recurso a modificar
    DELETE: Debe recibir el id a eliminar y devolverá lo mismo que POST
    """
    try:
        log = settings.log
        future = concurrent.futures.Future()
        queue = current_app.extensions["work_queue"]
        data_back = {"ok": False, "code": 0, "msg": "No procesado"}
        match request.method:
            case "GET":
                #coleccion = request.args.get('coleccion', "")
                if len(coleccion) == 0:
                    log.error(f"GET ERROR: sin colección -> {request.args}")
                    return make_response(
                        jsonify({"ok": False, "code": "sin colección"}),
                        400
                    )
                else:
                    log.debug(f"GET: {coleccion}/{id}")
                    if id is None:
                        id = 0
                    data_back = {
                        "coleccion": coleccion,
                        "ope": "read",
                        "id": id
                    }
            case "POST":
                payload = request.get_json()
                coleccion = payload.get("coleccion", None)
                if coleccion is None:
                    log.error(f"POST ERROR: sin colección -> {payload}")
                    return make_response(
                        jsonify({"ok": False, "code": "sin colección"}),                        
                        400
                    )
                else:
                    log.debug(f"POST: {coleccion} / {payload}")
                    data_back = {
                        "coleccion": coleccion,
                        "ope": "create",
                        "data": payload
                    }
            case _:
                raise NotImplementedError(f'Se solicita {request.method} con carga: {payload}')

        queue.put((future, data_back))
        resultado = future.result(timeout=WAIT)
        log.debug(resultado)
        return make_response(
            jsonify(resultado),
            resultado.get("code", 999)
        )

    except KeyError:
        return make_response(jsonify({"error": "DO: incorrect keys"}), 400)

    except concurrent.futures.CancelledError:
        return make_response(jsonify({"error": "DO: cancelled"}), 449)

    except TimeoutError:
        return make_response(jsonify({"error": "DO: timeout"}), 504)

    #finally:
    #    pending.pop(request_id, None)
