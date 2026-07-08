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


def _skip_si_no_hay_key(headers):
    """
    ReqRes exige x-api-key.
    Si el usuario no configuró REQRES_API_KEY, saltamos el test con un mensaje claro.
    """
    if headers is None:
        pytest.skip("Falta REQRES_API_KEY (variable de entorno) para llamar a ReqRes.")


# --- TC_API_01 - Obtener usuario existente --- #
def test_tc_api_01_get_usuario_existente(session):
    headers = _headers_reqres()
    _skip_si_no_hay_key(headers)

    url = f"{BASE_URL}/users/2"
    respuesta = session.get(url, headers=headers, timeout=15)

    assert respuesta.status_code == 200

    body = respuesta.json()
    assert "data" in body
    assert body["data"]["id"] == 2
    assert "email" in body["data"]
    assert "first_name" in body["data"]


# --- TC_API_02 - Crear usuario (POST) --- #
def test_tc_api_02_post_crear_usuario(session):
    headers = _headers_reqres()
    _skip_si_no_hay_key(headers)

    url = f"{BASE_URL}/users"
    payload = {"name": "luis", "job": "qa automation"}

    respuesta = session.post(url, headers=headers, json=payload, timeout=15)

    assert respuesta.status_code == 201

    body = respuesta.json()
    assert body["name"] == "luis"
    assert body["job"] == "qa automation"
    assert "id" in body
    assert "createdAt" in body
