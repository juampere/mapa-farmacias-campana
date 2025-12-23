from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Función para conectar con la base de datos y traer los datos
def obtener_farmacias(solo_turnos=False):
    conexion = sqlite3.connect('farmacias.db')
    # Esto es para que los resultados se puedan leer como diccionarios (con nombres de columna)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    if solo_turnos:
        cursor.execute("SELECT * FROM farmacias WHERE turno = 1")
    else:
        cursor.execute("SELECT * FROM farmacias")
    
    filas = cursor.fetchall()
    
    # Convertimos los resultados a una lista de diccionarios para que JS los entienda
    resultado = []
    for fila in filas:
        resultado.append(dict(fila))
    
    conexion.close()
    return resultado

@app.route('/api/farmacias', methods=['GET'])
def get_todas():
    try:
        farmacias = obtener_farmacias(solo_turnos=False)
        return jsonify(farmacias)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/farmacias/turno', methods=['GET'])
def get_turno():
    try:
        farmacias = obtener_farmacias(solo_turnos=True)
        return jsonify(farmacias)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)