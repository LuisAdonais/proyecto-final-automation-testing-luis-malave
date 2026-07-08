# pages/cart_page.py
# Page Object de la pantalla del carrito en SauceDemo.


class CartPage:
    """
    Representa el carrito de compras.
    Los localizadores estan aqui para que el test no los repita.
    """

    NOMBRE_PRODUCTO = ".inventory_item_name"
    ITEMS_CARRITO = ".cart_item"
    BOTON_REMOVE = "[data-test^='remove-']"
    BOTON_CHECKOUT = "#checkout"

    def __init__(self, driver):
        self.driver = driver

    def obtener_nombre_producto(self):
        """
        Devuelve el nombre del primer producto en el carrito.
        Si no hay productos, devuelve cadena vacia.
        """
        productos = self.driver.find_elements("css selector", self.NOMBRE_PRODUCTO)
        if not productos:
            return ""
        return productos[0].text

    def obtener_productos_en_carrito(self):
        """Devuelve lista con los nombres de todos los productos del carrito."""
        productos = self.driver.find_elements("css selector", self.NOMBRE_PRODUCTO)
        return [producto.text for producto in productos]

    def remover_producto(self):
        """Elimina el primer producto visible del carrito."""
        botones_remove = self.driver.find_elements("css selector", self.BOTON_REMOVE)
        if botones_remove:
            botones_remove[0].click()

    def click_checkout(self):
        """Hace click en Checkout para avanzar al formulario de datos."""
        boton = self.driver.find_element("css selector", self.BOTON_CHECKOUT)
        boton.click()

    def carrito_esta_vacio(self):
        """Indica si el carrito no tiene productos."""
        items = self.driver.find_elements("css selector", self.ITEMS_CARRITO)
        return len(items) == 0
