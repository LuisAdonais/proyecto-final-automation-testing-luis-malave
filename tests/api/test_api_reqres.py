# tests/api/test_api_reqres.py
# Pruebas de API usando Requests contra ReqRes.
# Documentacion oficial: https://reqres.in/docs
# Todas las requests requieren el header x-api-key.

import os

import pytest
import requests

# Base URL pedida por el ticket
BASE_URL = "https://reqres.in/api"

# Leemos la API key desde variable de entorno (NO hardcodear en GitHub)
API_KEY = os.getenv("REQRES_API_KEY")

# Headers comunes para ReqRes
HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}


@pytest.fixture(autouse=True)
def validar_api_key_configurada():
    """
    Control temprano: si falta la key, el error es claro para un junior.
  No subas la key al repo; configurala en PowerShell:
    $env:REQRES_API_KEY="tu_api_key_aqui"
    """
    if API_KEY is None:
        raise ValueError("Falta configurar la variable de entorno REQRES_API_KEY")


@pytest.fixture
def session():
    """Reutilizamos una Session de requests en todos los tests API."""
    return requests.Session()


# --- TC_API_01 - Obtener usuario existente --- #
def test_tc_api_01_get_usuario_existente(session):
    respuesta = session.get(f"{BASE_URL}/users/2", headers=HEADERS, timeout=15)

    assert respuesta.status_code == 200

    data = respuesta.json()
    assert "data" in data
    assert data["data"]["id"] == 2
    assert "email" in data["data"]
    assert "first_name" in data["data"]


# --- TC_API_02 - Crear usuario (POST) --- #
def test_tc_api_02_post_crear_usuario(session):
    payload = {"name": "luis", "job": "qa automation"}

    respuesta = session.post(
        f"{BASE_URL}/users",
        json=payload,
        headers=HEADERS,
        timeout=15,
    )

    assert respuesta.status_code == 201

    data = respuesta.json()
    assert data["name"] == "luis"
    assert data["job"] == "qa automation"
    assert "id" in data
    assert "createdAt" in data


# --- TC_API_03 - Eliminar usuario (DELETE) --- #
def test_tc_api_03_delete_usuario(session):
    respuesta = session.delete(f"{BASE_URL}/users/2", headers=HEADERS, timeout=15)

    assert respuesta.status_code == 204
    assert respuesta.text == ""


# --- TC_API_04 - Usuario no encontrado (negativo) --- #
def test_tc_api_04_get_usuario_no_encontrado(session):
    respuesta = session.get(f"{BASE_URL}/users/23", headers=HEADERS, timeout=15)

    assert respuesta.status_code == 404

    body = respuesta.json()
    assert body == {} or "data" not in body


# --- TC_API_05 - Encadenamiento demostrativo (opcional) --- #
def test_tc_api_05_encadenamiento_crear_usuario_y_validar_id(session):
    """
    Importante (junior):
    ReqRes NO persiste realmente los usuarios creados.
    Este encadenamiento es demostrativo: validamos que viene un 'id'
    y lo usamos como dato dentro del mismo test.
    """
    payload = {"name": "luis", "job": "qa automation"}

    respuesta = session.post(
        f"{BASE_URL}/users",
        json=payload,
        headers=HEADERS,
        timeout=15,
    )
    assert respuesta.status_code == 201

    data = respuesta.json()
    user_id = data.get("id")
    assert user_id is not None
    assert str(user_id).strip() != ""
