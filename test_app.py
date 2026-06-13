from threading import Thread
import requests, json, time


URL = 'http://localhost:5000/API/v1'
tablas = ["alumnos", "calificaciones"]
tablas = ["alumnos"]
metodos = {
    "get": [None, 0, 1, 3, 50, -1, "1"],
    "post": [
        {"nombre": "Pedro", "apellidos": "Pérez", "edad": 24},
        {"nombre": "Juan", "apellidos": "García"},
        {"nombre": "María", "edad": 34},
    ],
    "put": [
        {"id": 1, "nombre": "Pedro", "apellidos": "Pérez", "edad": 24},
        {"id": -1, "nombre": "Juan", "apellidos": "García"},
        {"nombre": "María", "edad": 34},
    ],
    "delete": [
        {"id": 1},
        {"id": -2},
        {}
    ],
    "raro": [1, "b"],
}


def wordker(coleccion, metodo, carga):
    print(f'\n{coleccion}->{metodo}: {carga}')
    response = None
    try:
        match metodo:
            case 'get':
                if carga is None:
                    peticion = f'{URL}/{coleccion}'
                else:
                    peticion = f'{URL}/{coleccion}/{carga}'
                print(peticion)
                response = requests.get(peticion)

            case 'post':
                response = requests.post(URL, json={
                    "coleccion": coleccion,
                    "carga": carga
                })
            case 'put':
                response = requests.put(URL, json={
                    "coleccion": coleccion,
                    "carga": carga
                })
            case 'delete':
                response = requests.delete(URL, json={
                    "coleccion": coleccion,
                    "id": carga.get("id", None)
                })
            case _:
                raise NotImplementedError(f'Pendiente de implementar {metodo.upper()}')

        if response.headers['content-type'] == 'application/json; charset=utf8':
            print(response.json())
        else:
            print(f'[{response.status_code}]: {response.content}')
    except Exception as exc:
        print(f'Error {exc}')

threads_running = []
for metodo in metodos:
    for tabla in tablas:
        for carga in metodos[metodo]:
            t = Thread(
                target=wordker,
                name=f'{tabla}->{metodo}({carga})',
                kwargs={
                    "coleccion": tabla,
                    "metodo": metodo,
                    "carga": carga
                },
                daemon=True
            )
            threads_running.append(t)
            t.start()
            time.sleep(1.2)

# Wait for all threads to finish
for t in threads_running:
    print(f'Esperando a "{t.name}"')
    t.join()
