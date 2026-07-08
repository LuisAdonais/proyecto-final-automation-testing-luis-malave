# tests/ui/test_saucedemo.py
# Pruebas UI de SauceDemo con Page Object Model.
# Los tests solo orquestan acciones; la logica Selenium vive en pages/.

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.helpers import cargar_json

pytestmark = pytest.mark.ui

DATOS_LOGIN = cargar_json("usuarios.json")
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDA = "secret_sauce"
PRODUCTO_BACKPACK_ID = "sauce-labs-backpack"
PRODUCTO_BACKPACK_NOMBRE = "Sauce Labs Backpack"
DATOS_CHECKOUT = cargar_json("checkout_data.json")


def _login_exitoso(driver):
    """Helper interno: abre SauceDemo e inicia sesion valida."""
    login = LoginPage(driver)
    login.abrir()
    login.login(USUARIO_VALIDO, PASSWORD_VALIDA)


def _precio_a_numero(texto_precio):
    """Convierte '$29.99' a 29.99 para comparar orden de precios."""
    return float(texto_precio.replace("$", ""))


@pytest.mark.parametrize(
    "dato",
    DATOS_LOGIN,
    ids=[f"{item['usuario']}_{item['resultado_esperado']}" for item in DATOS_LOGIN],
)
def test_tc_ui_01_login_parametrizado(driver, dato):
    """Login positivo y negativo con datos de usuarios.json."""
    login = LoginPage(driver)
    inventario = InventoryPage(driver)

    login.abrir()
    login.login(dato["usuario"], dato["password"])

    if dato["resultado_esperado"] == "ok":
        assert "inventory" in driver.current_url
        assert inventario.obtener_titulo() == "Products"
    else:
        assert login.esta_en_login()
        mensaje = login.obtener_mensaje_error()
        assert dato["mensaje_esperado"].lower() in mensaje.lower()


def test_tc_ui_02_navegacion_al_catalogo(driver):
    """Tras login valido, el usuario llega al catalogo de productos."""
    inventario = InventoryPage(driver)

    _login_exitoso(driver)

    assert "inventory" in driver.current_url
    assert inventario.obtener_titulo() == "Products"
    assert len(inventario.obtener_nombres_productos()) > 0


def test_tc_ui_03_filtrar_productos_por_precio(driver):
    """Ordena el catalogo por precio ascendente y valida el resultado."""
    inventario = InventoryPage(driver)

    _login_exitoso(driver)
    inventario.seleccionar_ordenamiento("lohi")

    precios = [_precio_a_numero(precio) for precio in inventario.obtener_precios_productos()]
    assert precios == sorted(precios)


def test_tc_ui_04_agregar_producto_al_carrito(driver):
    """Agrega un producto y lo verifica en el carrito."""
    inventario = InventoryPage(driver)
    carrito = CartPage(driver)

    _login_exitoso(driver)
    inventario.agregar_producto_al_carrito(PRODUCTO_BACKPACK_ID)

    assert inventario.obtener_cantidad_carrito() == 1

    inventario.ir_al_carrito()
    assert "cart" in driver.current_url
    assert PRODUCTO_BACKPACK_NOMBRE in carrito.obtener_productos_en_carrito()


def test_tc_ui_05_remover_producto_del_carrito(driver):
    """Prepara su propio carrito y valida que quede vacio al remover."""
    inventario = InventoryPage(driver)
    carrito = CartPage(driver)

    _login_exitoso(driver)
    inventario.agregar_producto_al_carrito(PRODUCTO_BACKPACK_ID)
    inventario.ir_al_carrito()

    carrito.remover_producto()

    assert carrito.carrito_esta_vacio()
    assert carrito.obtener_productos_en_carrito() == []


def test_tc_ui_06_checkout_completo_exitoso(driver):
    """Flujo E2E: login, carrito, checkout y confirmacion."""
    inventario = InventoryPage(driver)
    carrito = CartPage(driver)
    checkout = CheckoutPage(driver)
    datos = DATOS_CHECKOUT[0]

    _login_exitoso(driver)
    inventario.agregar_producto_al_carrito(PRODUCTO_BACKPACK_ID)
    inventario.ir_al_carrito()
    carrito.click_checkout()

    checkout.completar_datos(datos["nombre"], datos["apellido"], datos["codigo_postal"])
    checkout.continuar()
    checkout.finalizar_compra()

    assert "Thank you for your order!" in checkout.obtener_mensaje_confirmacion()


def test_tc_ui_07_checkout_sin_datos_obligatorios(driver):
    """Muestra error al continuar checkout sin completar el formulario."""
    inventario = InventoryPage(driver)
    carrito = CartPage(driver)
    checkout = CheckoutPage(driver)

    _login_exitoso(driver)
    inventario.agregar_producto_al_carrito(PRODUCTO_BACKPACK_ID)
    inventario.ir_al_carrito()
    carrito.click_checkout()

    checkout.continuar()

    mensaje_error = checkout.obtener_mensaje_error()
    assert "First Name is required" in mensaje_error
