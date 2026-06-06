# routes.py

import concurrent.futures
from flask import Blueprint, current_app, jsonify

api = Blueprint("api", __name__)


@api.route("/alumnos/<int:id>", methods=["GET"])
def get_alumno(id):
    try:
        future = concurrent.futures.Future()
        queue = current_app.extensions["work_queue"]
        print(f"ENCOLANDO -> {id}")
        queue.put((future, {"coleccion": "alumnos", "id": id}))
        resultado = future.result(timeout=30)
        return jsonify(resultado)

    except KeyError:
        return {"error": "incorrect keys"}, 400

    except concurrent.futures.CancelledError:
        return {"error": "cancelled"}, 449

    except TimeoutError:
        return {"error": "timeout"}, 504

    #finally:
    #    pending.pop(request_id, None)
