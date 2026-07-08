# conftest.py
# Configuracion global de pytest.
# Aqui centralizamos: navegador, carpetas, capturas en fallos, logs y reporte HTML.

import base64
import os
from datetime import datetime
from pathlib import Path

import pytest
from pytest_html import extras
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from utils.logger import (
    log_apertura_navegador,
    log_cierre_navegador,
    log_ejecucion_api,
    log_fallo,
    log_inicio_ejecucion,
    log_inicio_test,
    log_ruta_screenshot,
)

# Rutas de carpetas del proyecto
CARPETA_REPORTES = Path("reports")
CARPETA_SCREENSHOTS = Path("screenshots")


@pytest.fixture(scope="session", autouse=True)
def preparar_carpetas():
    """
    Fixture automatico (autouse=True):
    - Crea reports/ y screenshots/ si no existen
    - Registra el inicio de la ejecucion en el log
    """
    CARPETA_REPORTES.mkdir(exist_ok=True)
    CARPETA_SCREENSHOTS.mkdir(exist_ok=True)
    log_inicio_ejecucion()


@pytest.fixture
def driver():
    """
    Fixture del navegador para tests UI.
    - Abre Firefox al inicio del test
    - Lo cierra al finalizar (yield)
    """
    log_apertura_navegador()

    opciones = Options()

    # En GitHub Actions no hay pantalla visible: usamos headless
    if os.getenv("GITHUB_ACTIONS") == "true":
        opciones.add_argument("-headless")

    navegador = webdriver.Firefox(options=opciones)

    if os.getenv("GITHUB_ACTIONS") != "true":
        navegador.maximize_window()

    yield navegador

    navegador.quit()
    log_cierre_navegador()


def pytest_runtest_setup(item):
    """
    Hook de pytest: se ejecuta antes de cada test.
    Registramos el nombre del test que va a correr.
    """
    log_inicio_test(item.name)

    if item.get_closest_marker("api"):
        log_ejecucion_api(item.name, "SETUP", "test de API detectado")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de pytest: si un test UI falla:
    - guarda screenshot en screenshots/
    - registra la ruta en el log
    - incrusta la imagen en reports/reporte.html
    """
    resultado = yield
    reporte = resultado.get_result()
    reporte.extras = getattr(reporte, "extras", [])

    if reporte.when == "call" and reporte.failed:
        mensaje_error = str(reporte.longrepr)
        log_fallo(item.name, mensaje_error)

        driver = item.funcargs.get("driver")
        if driver is not None:
            fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"failure_{item.name}_{fecha_hora}.png"
            ruta_screenshot = CARPETA_SCREENSHOTS / nombre_archivo

            driver.save_screenshot(str(ruta_screenshot))
            log_ruta_screenshot(ruta_screenshot)

            # Incrustamos la captura en el reporte HTML (pytest-html)
            with open(ruta_screenshot, "rb") as imagen:
                imagen_base64 = base64.b64encode(imagen.read()).decode("ascii")

            reporte.extras.append(
                extras.html(
                    f"<p><strong>Screenshot de fallo:</strong> {ruta_screenshot}</p>"
                )
            )
            reporte.extras.append(
                extras.image(
                    imagen_base64,
                    mime_type="image/png",
                    extension="png",
                )
            )
