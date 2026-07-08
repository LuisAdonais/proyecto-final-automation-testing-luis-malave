# pages/inventory_page.py
# Page Object del catalogo de productos.

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.base_page import BasePage, TIEMPO_ESPERA


class InventoryPage(BasePage):
    """Acciones del catalogo despues de un login exitoso."""

    def obtener_titulo(self):
        """Devuelve el titulo de la pagina (ej: Products)."""
        titulo = self._esperar_visible(By.CLASS_NAME, "title")
        return titulo.text

    def agregar_producto_al_carrito(self, producto_id):
        """Agrega un producto al carrito por su ID (ej: sauce-labs-backpack)."""
        selector = f'[data-test="add-to-cart-{producto_id}"]'
        self._hacer_click(By.CSS_SELECTOR, selector)

    def remover_producto(self, producto_id):
        """Quita un producto desde el catalogo."""
        selector = f'[data-test="remove-{producto_id}"]'
        self._hacer_click(By.CSS_SELECTOR, selector)

    def ir_al_carrito(self):
        """Navega al carrito de compras."""
        self._hacer_click(By.CLASS_NAME, "shopping_cart_link")

    def obtener_cantidad_carrito(self):
        """Devuelve la cantidad del badge del carrito (0 si esta vacio)."""
        try:
            badge = WebDriverWait(self.driver, TIEMPO_ESPERA).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
            )
            return int(badge.text)
        except TimeoutException:
            return 0

    def seleccionar_ordenamiento(self, valor):
        """Ordena el catalogo (az, za, lohi, hilo)."""
        select = self._esperar_visible(By.CLASS_NAME, "product_sort_container")
        Select(select).select_by_value(valor)

    def obtener_nombres_productos(self):
        """Lista de nombres visibles en el catalogo."""
        self._esperar_visible(By.CLASS_NAME, "inventory_item_name")
        elementos = self.driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        return [elemento.text for elemento in elementos]

    def obtener_precios_productos(self):
        """Lista de precios visibles en el catalogo."""
        self._esperar_visible(By.CLASS_NAME, "inventory_item_price")
        elementos = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        return [elemento.text for elemento in elementos]
