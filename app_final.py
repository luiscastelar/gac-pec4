# app_final.py

from flask import Flask
from queue import Queue
from threading import Thread


def dispatcher(queue):

    while True:
        future, payload = queue.get()
        print(f"INICIO -> {payload}")

        try:
            resultado = worker(payload)
            future.set_result(resultado)

        except Exception as exc:
            future.set_exception(exc)

        finally:
            print(f"FIN -> {payload}")
            queue.task_done()


def worker(payload: dict) -> dict:
    """Procesador de tareas (llama a los DAO)"""
    print(f"Procesando: {payload}")

    # retardo para pruebas
    import time
    time.sleep(10)

    return {
        "status": "ok",
        "payload": payload,
        "mensaje": "procesado"
    }


def create_app():

    app = Flask(__name__)

    work_queue = Queue()

    Thread(
        target=dispatcher,
        args=(work_queue,),
        daemon=True
    ).start()

    app.extensions["work_queue"] = work_queue

    from core.routes import api
    app.register_blueprint(api)

    return app
