# tests/ui/test_saucedemo.py
# Pruebas UI de SauceDemo usando Page Object Model.
# Regla importante: los tests NO usan localizadores Selenium directos.

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.helpers import cargar_json

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
