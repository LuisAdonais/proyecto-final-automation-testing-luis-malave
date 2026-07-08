# utils/logger.py
# Sistema de logging del framework.
# Guarda mensajes en reports/ejecucion.log para depurar cuando algo falla.

import logging
from pathlib import Path

# Carpeta donde se guarda el archivo de log
CARPETA_REPORTES = Path(__file__).parent.parent / "reports"
ARCHIVO_LOG = CARPETA_REPORTES / "ejecucion.log"


def _obtener_logger():
    """
    Crea el logger una sola vez y lo reutiliza.
    Escribe en archivo (ejecucion.log) y tambien en consola.
    """
    # Creamos la carpeta reports/ si no existe
    CARPETA_REPORTES.mkdir(exist_ok=True)

    logger = logging.getLogger("automation")

    # Si ya tiene handlers, no los duplicamos
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Formato del mensaje: fecha | nivel | texto
    formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # Handler para escribir en archivo
    archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    archivo.setFormatter(formato)
    logger.addHandler(archivo)

    # Handler para ver mensajes en la consola
    consola = logging.StreamHandler()
    consola.setFormatter(formato)
    logger.addHandler(consola)

    return logger


# Logger global que usan conftest.py y los tests
logger = _obtener_logger()


def log_inicio_ejecucion():
    """Registra cuando empieza la sesion de pruebas."""
    logger.info("Inicio de ejecucion de pruebas")


def log_apertura_navegador():
    """Registra cuando se abre Firefox."""
    logger.info("Apertura del navegador Firefox")


def log_cierre_navegador():
    """Registra cuando se cierra el navegador."""
    logger.info("Cierre del navegador")


def log_inicio_test(nombre_test):
    """Registra el nombre del test que va a ejecutarse."""
    logger.info(f"Inicio de test: {nombre_test}")


def log_fallo(nombre_test, mensaje_error):
    """Registra cuando un test falla."""
    logger.error(f"Fallo en test '{nombre_test}': {mensaje_error}")


def log_ruta_screenshot(ruta):
    """Registra la ruta donde se guardo una captura de pantalla."""
    logger.info(f"Screenshot guardado en: {ruta}")


def log_ejecucion_api(nombre_test, metodo, url):
    """Registra cuando un test de API se ejecuta."""
    logger.info(f"Ejecucion API en '{nombre_test}' | {metodo} {url}")


def log_status_code_api(nombre_test, metodo, url, status_code):
    """Registra el status code HTTP recibido en una prueba API."""
    logger.info(
        f"API '{nombre_test}' | {metodo} {url} | status_code={status_code}"
    )
