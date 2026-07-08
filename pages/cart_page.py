# pages/cart_page.py
# Page Object del carrito de compras.

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    """Acciones de la pantalla del carrito."""

    def obtener_nombre_producto(self):
        """Nombre del primer producto del carrito."""
        productos = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        if not productos:
            return ""
        return productos[0].text

    def obtener_productos_en_carrito(self):
        """Lista con todos los nombres del carrito."""
        self._esperar_visible(By.CLASS_NAME, "cart_list")
        productos = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        return [producto.text for producto in productos]

    def remover_producto(self):
        """Elimina el primer producto visible del carrito."""
        boton = self._esperar_clickeable(By.CSS_SELECTOR, "[data-test^='remove-']")
        boton.click()
        self._espera().until(lambda driver: len(driver.find_elements(By.CLASS_NAME, "cart_item")) == 0)

    def click_checkout(self):
        """Avanza al formulario de checkout."""
        self._hacer_click(By.ID, "checkout")

    def carrito_esta_vacio(self):
        """True si no hay productos en el carrito."""
        items = self.driver.find_elements(By.CLASS_NAME, "cart_item")
        return len(items) == 0
