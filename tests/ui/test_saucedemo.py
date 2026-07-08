# tests/ui/test_saucedemo.py
# Pruebas UI de SauceDemo usando Page Object Model.
# Regla importante: los tests NO usan localizadores Selenium directos.

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.helpers import cargar_json
