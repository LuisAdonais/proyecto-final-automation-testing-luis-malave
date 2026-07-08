# utils/helpers.py
# Funciones de ayuda reutilizables para los tests.
# La idea es escribir la logica una sola vez y usarla en muchos archivos.

import json
from pathlib import Path

# Carpeta donde guardamos los archivos JSON de datos de prueba
CARPETA_DATA = Path(__file__).parent.parent / "data"


def cargar_json(ruta_archivo):
    """
    Lee un archivo JSON y devuelve datos de Python (lista o diccionario).

    Parametros:
        ruta_archivo: nombre del archivo (ej: 'usuarios.json')

    Ejemplo de uso en un test parametrizado:
        usuarios = cargar_json("usuarios.json")
        usuario = usuarios[0]["usuario"]
    """
    # Si nos pasan solo el nombre, buscamos dentro de data/
    ruta = CARPETA_DATA / ruta_archivo

    # Abrimos y leemos el JSON
    with open(ruta, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    return datos
