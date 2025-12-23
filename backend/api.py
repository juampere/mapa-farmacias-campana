from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def obtener_farmacias(solo_turnos=False):
    try:
        conexion = sqlite3.connect('farmacias.db')
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()
        
        if solo_turnos:
            cursor.execute("SELECT * FROM farmacias WHERE turno = 1")
        else:
            cursor.execute("SELECT * FROM farmacias")
        
        filas = cursor.fetchall()
        resultado = [dict(fila) for fila in filas]
        conexion.close()
        return resultado
    except Exception as e:
        print(f"Error: {e}")
        return []

@app.route('/api/farmacias', methods=['GET'])
def get_todas():
    return jsonify(obtener_farmacias(solo_turnos=False))

@app.route('/api/farmacias/turno', methods=['GET'])
def get_turno():
    return jsonify(obtener_farmacias(solo_turnos=True))

if __name__ == '__main__':
    app.run(debug=True, port=5000)