from threading import Thread
import requests, json, time


URL = 'http://localhost:5000/API/v1'
tablas = ["alumnos", "calificaciones"]
metodos = {
    "get": [None, 0, 1, 3, 50, -1],
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
}


def wordker(coleccion, metodo, carga):
    print(f'{coleccion}->{metodo}: {carga}')
    match metodo:
        case 'get':
            if carga is None:
                peticion = f'{URL}/{coleccion}'
            else:
                peticion = f'{URL}/{coleccion}/{carga}'
            print(peticion)
            response = requests.get(peticion)
            if response.headers['content-type'] == 'application/json; charset=utf8':
                print(response.json())
            else:
                print(f'[{response.status_code}]: {response.content}')
            
        case 'post':
            print(f'GET {coleccion}')
        case 'put':
            print(f'PUT {coleccion}')
        case 'delete':
            print(f'DELETE {coleccion}')
        case _:
            print('Error!!!!')


for metodo in metodos:
    for tabla in tablas:
        for carga in metodos[metodo]:
            Thread(
                target=wordker,
                name=f'{tabla}->{metodo}',
                kwargs={
                    "coleccion": tabla,
                    "metodo": metodo,
                    "carga": carga
                },
                daemon=True
            ).start()
            time.sleep(5)
