from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import subprocess

app = Flask(__name__)
CORS(app)

# Función para conectar con la base de datos y traer los datos
def obtener_farmacias(solo_turnos=False):
    # Usamos la ruta simple porque en Render el Working Directory es /backend
    conexion = sqlite3.connect('farmacias.db')
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    if solo_turnos:
        cursor.execute("SELECT * FROM farmacias WHERE turno = 1")
    else:
        cursor.execute("SELECT * FROM farmacias")
    
    filas = cursor.fetchall()
    
    resultado = []
    for fila in filas:
        resultado.append(dict(fila))
    
    conexion.close()
    return resultado

@app.route('/api/farmacias', methods=['GET'])
def get_todas():
    try:
        # Esto ejecuta tu script de scraping antes de devolver los datos
        # Así los turnos siempre están al día en el servidor
        subprocess.run(["python", "actualizar_turnos.py"])
        
        farmacias = obtener_farmacias(solo_turnos=False)
        return jsonify(farmacias)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/farmacias/turno', methods=['GET'])
def get_turno():
    try:
        # También actualizamos acá por seguridad
        subprocess.run(["python", "actualizar_turnos.py"])
        
        farmacias = obtener_farmacias(solo_turnos=True)
        return jsonify(farmacias)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)