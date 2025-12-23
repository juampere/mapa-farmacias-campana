import json
import time
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="mi_actualizador_farmacias", timeout=10)

# 1. Cargamos tu base de datos actual
with open("farmacias_campana.json", "r", encoding="utf-8") as f:
    farmacias = json.load(f)

print(f"Empezando a geolocalizar {len(farmacias)} farmacias...")

for f in farmacias:
    # Armamos la dirección completa para el mapa
    direccion_completa = f"{f['direccion']}, Campana, Buenos Aires, Argentina"
    
    try:
        location = geolocator.geocode(direccion_completa)
        if location:
            f["latitud"] = location.latitude
            f["longitud"] = location.longitude
            print(f"Encontrada: {f['nombre']}")
        else:
            f["latitud"] = None
            f["longitud"] = None
            print(f"No se encontró: {f['nombre']}")
            
        # IMPORTANTE: Esperamos 1 segundo entre cada consulta
        # para que el servidor gratuito no nos bloquee.
        time.sleep(1)
        
    except:
        print(f"Error con {f['nombre']}, reintentando...")

# 2. Guardamos los datos enriquecidos en un archivo nuevo
with open("farmacias_con_mapa.json", "w", encoding="utf-8") as f:
    json.dump(farmacias, f, indent=4, ensure_ascii=False)

print("\n¡Proceso terminado! Revisá el archivo farmacias_con_mapa.json")