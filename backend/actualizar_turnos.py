import requests
from bs4 import BeautifulSoup
import sqlite3
import os

def actualizar_turnos_db():
    url = "https://www.encampana.com/cat.php?txt=1669"
    archivo_db = 'farmacias.db'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    if not os.path.exists(archivo_db):
        print(f"Error: No se encuentra la base de datos {archivo_db}")
        return

    try:
        print("Conectando con el portal de turnos...")
        respuesta = requests.get(url, headers=headers, timeout=10)
        respuesta.encoding = 'utf-8'
        
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            parrafos = soup.find_all('p')
            textos_relevantes = [p.get_text().upper() for p in parrafos]
            
            # Conectamos a la base de datos
            conexion = sqlite3.connect(archivo_db)
            cursor = conexion.cursor()
            
            # 1. Primero ponemos todas las farmacias en "no turno" (limpieza)
            cursor.execute("UPDATE farmacias SET turno = 0")
            
            # 2. Traemos los nombres de las farmacias que tenemos en la DB
            cursor.execute("SELECT nombre FROM farmacias")
            nombres_farmacias = cursor.fetchall()
            
            encontradas = 0
            for (nombre,) in nombres_farmacias:
                nombre_buscado = nombre.upper().strip()
                esta_de_turno = False
                
                for texto in textos_relevantes:
                    if "FARMACIA" in texto and nombre_buscado in texto:
                        esta_de_turno = True
                        break
                
                if esta_de_turno:
                    # 3. Si está de turno, actualizamos esa fila específica
                    cursor.execute("UPDATE farmacias SET turno = 1 WHERE nombre = ?", (nombre,))
                    encontradas += 1
                    print(f" [+] {nombre} marcada DE TURNO en la DB")
            
            conexion.commit()
            conexion.close()
            print(f"\nBase de datos actualizada. Farmacias de turno hoy: {encontradas}")
        else:
            print(f"Error de conexión con la web. Código: {respuesta.status_code}")

    except Exception as e:
        print(f"Hubo un fallo: {e}")

if __name__ == "__main__":
    actualizar_turnos_db()