# tests/ui/test_saucedemo.py
# Pruebas UI de SauceDemo usando Page Object Model.
# Regla importante: los tests NO usan localizadores Selenium directos.

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.helpers import cargar_json

# Marker del epic: todas las pruebas de este archivo son UI
pytestmark = pytest.mark.ui

# --- Constantes y datos externos ---
DATOS_LOGIN = cargar_json("usuarios.json")
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDA = "secret_sauce"


def _login_exitoso(driver):
    """Abre SauceDemo y hace login valido (helper interno)."""
    login = LoginPage(driver)
    login.abrir()
    login.login(USUARIO_VALIDO, PASSWORD_VALIDA)
    return login


# --- TC_UI_01: Login parametrizado positivo y negativo ---
@pytest.mark.parametrize(
    "dato",
    DATOS_LOGIN,
    ids=[f"{item['usuario']}_{item['resultado_esperado']}" for item in DATOS_LOGIN],
)
def test_tc_ui_01_login_parametrizado(driver, dato):
    """
    Valida login exitoso, usuario bloqueado y credenciales invalidas.
    Los datos vienen de data/usuarios.json (datos externos).
    """
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


# --- TC_UI_02: Navegacion al catalogo ---
def test_tc_ui_02_navegacion_al_catalogo(driver):
    """Valida que despues del login llegamos al catalogo de productos."""
    inventario = InventoryPage(driver)

    _login_exitoso(driver)

    assert "inventory" in driver.current_url
    assert inventario.obtener_titulo() == "Products"
    assert len(inventario.obtener_nombres_productos()) > 0


def _precio_a_numero(texto_precio):
    """Convierte '$29.99' a 29.99 para comparar orden de precios."""
    return float(texto_precio.replace("$", ""))


# --- TC_UI_03: Busqueda funcional por filtro de catalogo ---
def test_tc_ui_03_filtrar_productos_por_precio(driver):
    """
    En SauceDemo no hay barra de busqueda textual.
    Cubrimos busqueda funcional ordenando por precio (low to high).
    """
    inventario = InventoryPage(driver)

    _login_exitoso(driver)
    inventario.seleccionar_ordenamiento("lohi")

    precios = [_precio_a_numero(precio) for precio in inventario.obtener_precios_productos()]
    assert precios == sorted(precios)


PRODUCTO_BACKPACK_ID = "sauce-labs-backpack"
PRODUCTO_BACKPACK_NOMBRE = "Sauce Labs Backpack"


# --- TC_UI_04: Anadir producto al carrito ---
def test_tc_ui_04_agregar_producto_al_carrito(driver):
    """Valida agregar un producto y verlo en el carrito."""
    inventario = InventoryPage(driver)
    carrito = CartPage(driver)

    _login_exitoso(driver)
    inventario.agregar_producto_al_carrito(PRODUCTO_BACKPACK_ID)

    assert inventario.obtener_cantidad_carrito() == 1

    inventario.ir_al_carrito()
    assert "cart" in driver.current_url
    assert PRODUCTO_BACKPACK_NOMBRE in carrito.obtener_productos_en_carrito()


# --- TC_UI_05: Remover producto del carrito ---
def test_tc_ui_05_remover_producto_del_carrito(driver):
    """
    Test independiente: prepara su propio carrito y luego lo vacia.
    No depende de otros tests.
    """
    inventario = InventoryPage(driver)
    carrito = CartPage(driver)

    _login_exitoso(driver)
    inventario.agregar_producto_al_carrito(PRODUCTO_BACKPACK_ID)
    inventario.ir_al_carrito()

    carrito.remover_producto()

    assert carrito.carrito_esta_vacio()
    assert carrito.obtener_productos_en_carrito() == []


DATOS_CHECKOUT = cargar_json("checkout_data.json")


# --- TC_UI_06: Checkout completo exitoso ---
def test_tc_ui_06_checkout_completo_exitoso(driver):
    """Flujo E2E: login -> carrito -> checkout -> confirmacion."""
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


# --- TC_UI_07: Checkout negativo sin datos obligatorios ---
def test_tc_ui_07_checkout_sin_datos_obligatorios(driver):
    """Valida error al continuar checkout sin completar el formulario."""
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
