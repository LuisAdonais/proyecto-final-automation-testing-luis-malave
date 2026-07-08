# pages/login_page.py
# Page Object del login en SauceDemo.

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Acciones y localizadores de la pantalla de login."""

    URL = "https://www.saucedemo.com/"

    def abrir(self):
        """Abre la pagina de login."""
        self.driver.get(self.URL)
        self._esperar_visible(By.ID, "user-name")

    def login(self, usuario, password):
        """Ingresa credenciales y hace click en Login."""
        self._escribir_texto(By.ID, "user-name", usuario)
        self._escribir_texto(By.ID, "password", password)
        self._hacer_click(By.ID, "login-button")

    def obtener_mensaje_error(self):
        """Devuelve el mensaje de error visible."""
        mensaje = self._esperar_visible(By.CSS_SELECTOR, "[data-test='error']")
        return mensaje.text

    def esta_en_login(self):
        """Indica si seguimos en la pantalla de login."""
        return self.driver.current_url == self.URL
