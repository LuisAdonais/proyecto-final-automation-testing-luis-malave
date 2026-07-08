# tests/api/test_api_reqres.py
# Pruebas de API usando Requests contra ReqRes.
# Importante (junior): ReqRes ahora pide API Key (header x-api-key).
# Guardamos la key como variable de entorno para NO subirla al repo.

import os

import pytest
import requests

# Base URL pedida por el ticket
BASE_URL = "https://reqres.in/api"


def _obtener_api_key():
    """
    Lee la API key desde variable de entorno.
    Si no existe, devolvemos None y los tests se van a saltar (skip).
    """
    return os.getenv("REQRES_API_KEY")


def _headers_reqres():
    """
    Arma los headers que necesita ReqRes.
    """
    api_key = _obtener_api_key()
    if not api_key:
        return None
    return {"x-api-key": api_key}


@pytest.fixture
def session():
    """
    Reutilizamos una Session de requests (mejor performance y menos repetición).
    """
    return requests.Session()
