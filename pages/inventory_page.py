# pages/inventory_page.py
# Page Object del catalogo de productos (inventory) en SauceDemo.

from selenium.webdriver.support.ui import Select


class InventoryPage:
    """
    Representa la pantalla de productos despues de un login exitoso.
    producto_id ejemplo: 'sauce-labs-backpack'
    """

    TITULO_PAGINA = ".title"
    ICONO_CARRITO = ".shopping_cart_link"
    BADGE_CARRITO = ".shopping_cart_badge"
    SELECT_ORDENAMIENTO = ".product_sort_container"
    NOMBRES_PRODUCTOS = ".inventory_item_name"
    PRECIOS_PRODUCTOS = ".inventory_item_price"

    def __init__(self, driver):
        self.driver = driver

    def obtener_titulo(self):
        """Devuelve el titulo visible de la pagina (ej: 'Products')."""
        titulo = self.driver.find_element("css selector", self.TITULO_PAGINA)
        return titulo.text

    def agregar_producto_al_carrito(self, producto_id):
        """
        Agrega un producto al carrito usando su ID.
        Ejemplo producto_id: 'sauce-labs-backpack'
        """
        boton = self.driver.find_element(
            "css selector",
            f'[data-test="add-to-cart-{producto_id}"]',
        )
        boton.click()

    def remover_producto(self, producto_id):
        """
        Quita un producto del catalogo (boton Remove en inventory).
        Ejemplo producto_id: 'sauce-labs-backpack'
        """
        boton = self.driver.find_element(
            "css selector",
            f'[data-test="remove-{producto_id}"]',
        )
        boton.click()

    def ir_al_carrito(self):
        """Hace click en el icono del carrito."""
        icono = self.driver.find_element("css selector", self.ICONO_CARRITO)
        icono.click()

    def obtener_cantidad_carrito(self):
        """
        Devuelve la cantidad de productos en el badge del carrito.
        Si el carrito esta vacio, devuelve 0.
        """
        badges = self.driver.find_elements("css selector", self.BADGE_CARRITO)
        if not badges:
            return 0
        return int(badges[0].text)

    def seleccionar_ordenamiento(self, valor):
        """
        Cambia el orden del catalogo.
        Valores comunes: 'az', 'za', 'lohi' (precio menor a mayor), 'hilo'
        """
        elemento_select = self.driver.find_element("css selector", self.SELECT_ORDENAMIENTO)
        Select(elemento_select).select_by_value(valor)

    def obtener_nombres_productos(self):
        """Devuelve lista con los nombres visibles de productos."""
        elementos = self.driver.find_elements("css selector", self.NOMBRES_PRODUCTOS)
        return [elemento.text for elemento in elementos]

    def obtener_precios_productos(self):
        """Devuelve lista con los precios visibles de productos."""
        elementos = self.driver.find_elements("css selector", self.PRECIOS_PRODUCTOS)
        return [elemento.text for elemento in elementos]
