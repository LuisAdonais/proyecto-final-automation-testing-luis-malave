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
