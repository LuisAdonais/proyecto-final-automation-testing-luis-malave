# pages/base_page.py
# Clase base con waits explicitos para todos los Page Objects.
# Evita time.sleep() y hace los tests mas estables.

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIEMPO_ESPERA = 10


class BasePage:
    """Metodos de espera compartidos por las paginas del framework."""

    def __init__(self, driver):
        self.driver = driver

    def _espera(self):
        return WebDriverWait(self.driver, TIEMPO_ESPERA)

    def _esperar_visible(self, by, localizador):
        return self._espera().until(EC.visibility_of_element_located((by, localizador)))

    def _esperar_clickeable(self, by, localizador):
        return self._espera().until(EC.element_to_be_clickable((by, localizador)))

    def _escribir_texto(self, by, localizador, texto):
        campo = self._esperar_visible(by, localizador)
        campo.clear()
        campo.send_keys(texto)

    def _hacer_click(self, by, localizador):
        self._esperar_clickeable(by, localizador).click()
