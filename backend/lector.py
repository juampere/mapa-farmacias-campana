import pdfplumber
import json

archivo_pdf = "farmacias.pdf"
base_de_datos = []

with pdfplumber.open(archivo_pdf) as pdf:
    for pagina in pdf.pages:
        texto = pagina.extract_text()
        if texto:
            for linea in texto.split('\n'):
                if "CAMPANA" in linea:
                    # Limpiamos los "CAMPANA" de los bordes
                    limpia = linea.replace("CAMPANA", "").strip()
                    palabras = limpia.split()
                    
                    if len(palabras) > 2:
                        # El primer elemento es el Nombre
                        nombre = palabras[0]
                        # El último elemento suele ser el Teléfono
                        telefono = palabras[-1]
                        # Todo lo que quedó en el medio es la Dirección
                        direccion = " ".join(palabras[1:-1])
                        
                        ficha = {
                            "nombre": nombre,
                            "direccion": direccion,
                            "telefono": telefono
                        }
                        base_de_datos.append(ficha)

with open("farmacias_campana.json", "w", encoding="utf-8") as f:
    json.dump(base_de_datos, f, indent=4, ensure_ascii=False)

print("Base de datos actualizada con campos separados.")