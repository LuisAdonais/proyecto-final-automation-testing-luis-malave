# pages/checkout_page.py
# Page Object del flujo de checkout.

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Acciones del checkout: datos, resumen y confirmacion."""

    def completar_datos(self, nombre, apellido, codigo_postal):
        """Completa el formulario del paso 1."""
        self._escribir_texto(By.ID, "first-name", nombre)
        self._escribir_texto(By.ID, "last-name", apellido)
        self._escribir_texto(By.ID, "postal-code", codigo_postal)

    def continuar(self):
        """Confirma datos y avanza al resumen."""
        self._hacer_click(By.ID, "continue")

    def finalizar_compra(self):
        """Finaliza la compra en el resumen."""
        self._hacer_click(By.ID, "finish")

    def obtener_mensaje_confirmacion(self):
        """Mensaje de compra exitosa."""
        mensaje = self._esperar_visible(By.CLASS_NAME, "complete-header")
        return mensaje.text

    def obtener_mensaje_error(self):
        """Mensaje de error cuando faltan datos obligatorios."""
        error = self._esperar_visible(By.CSS_SELECTOR, "[data-test='error']")
        return error.text
