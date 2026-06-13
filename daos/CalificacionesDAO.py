# *****************************************************************************
#   Archivo generado desde plantilla -> NO TOCAR                              *
# *****************************************************************************

import sqlite3

class CalificacionesDAO:
    def __init__(self, fileDB):
        self.db_connection = sqlite3.connect(fileDB)

    def get_calificaciones(self, id = 0):
        query = "SELECT * FROM alumnos"
        if id == 0:
            return self.db_connection.execute(query).fetchall()
        else:
            query += ' WHERE id = ?'
            return self.db_connection.execute(query, (id,)).fetchone()

    def create_calificaciones(self, data):
        query = "SELECT id FROM calificaciones ORDER BY id DESC LIMIT 1"
        id = self.db_connection.execute(query).fetchone()
        data_new = dict()  # Como los dict a partir de 3.6 son ordenados...
        data_new['id'] = id[0] + 1
        data_new.update(**data)
        query = "INSERT INTO calificaciones (id, alumnoId, valor) VALUES (?, ?, ?)"
        self.db_connection.execute(query, tuple(data_new.values()))
        self.db_connection.commit()
        #return self.db_connection.lastrowid -> debe ser el cursor
        return data_new['id']

    def update_calificaciones(self, id, data):
        query = f"UPDATE calificaciones SET id=?, alumnoId=?, valor=? WHERE id = ?"
        self.db_connection.execute(query, tuple(data.values()) + (id,))
        self.db_connection.commit()
        return 0  # ok

    def delete_calificaciones(self, id):
        query = "DELETE FROM calificaciones WHERE id = ?"
        self.db_connection.execute(query, (id,))
        self.db_connection.commit()
        return 0  # ok
