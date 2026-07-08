# tests/api/test_api_reqres.py
# Pruebas de API usando Requests contra ReqRes.
# Documentacion oficial: https://reqres.in/docs

import os
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv

from utils.logger import log_status_code_api

# Marker del epic: todas las pruebas de este archivo son API
pytestmark = pytest.mark.api

# Carga variables desde .env local (archivo ignorado por git)
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

BASE_URL = "https://reqres.in/api"
API_KEY = os.getenv("REQRES_API_KEY")

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}


@pytest.fixture(autouse=True)
def validar_api_key_configurada():
    """Falla con mensaje claro si falta REQRES_API_KEY."""
    if API_KEY is None:
        raise ValueError("Falta configurar la variable de entorno REQRES_API_KEY")


@pytest.fixture
def session():
    """Reutilizamos una Session de requests en todos los tests API."""
    return requests.Session()


# --- TC_API_01 - Obtener usuario existente --- #
def test_tc_api_01_get_usuario_existente(session):
    url = f"{BASE_URL}/users/2"
    respuesta = session.get(url, headers=HEADERS, timeout=15)
    log_status_code_api("test_tc_api_01_get_usuario_existente", "GET", url, respuesta.status_code)

    assert respuesta.status_code == 200

    data = respuesta.json()
    assert "data" in data
    assert data["data"]["id"] == 2
    assert "email" in data["data"]
    assert "first_name" in data["data"]


# --- TC_API_02 - Crear usuario (POST) --- #
def test_tc_api_02_post_crear_usuario(session):
    url = f"{BASE_URL}/users"
    payload = {"name": "luis", "job": "qa automation"}

    respuesta = session.post(url, json=payload, headers=HEADERS, timeout=15)
    log_status_code_api("test_tc_api_02_post_crear_usuario", "POST", url, respuesta.status_code)

    assert respuesta.status_code == 201

    data = respuesta.json()
    assert data["name"] == "luis"
    assert data["job"] == "qa automation"
    assert "id" in data
    assert "createdAt" in data


# --- TC_API_03 - Eliminar usuario (DELETE) --- #
def test_tc_api_03_delete_usuario(session):
    url = f"{BASE_URL}/users/2"
    respuesta = session.delete(url, headers=HEADERS, timeout=15)
    log_status_code_api("test_tc_api_03_delete_usuario", "DELETE", url, respuesta.status_code)

    assert respuesta.status_code == 204
    assert respuesta.text == ""


# --- TC_API_04 - Usuario no encontrado (negativo) --- #
def test_tc_api_04_get_usuario_no_encontrado(session):
    url = f"{BASE_URL}/users/23"
    respuesta = session.get(url, headers=HEADERS, timeout=15)
    log_status_code_api("test_tc_api_04_get_usuario_no_encontrado", "GET", url, respuesta.status_code)

    assert respuesta.status_code == 404

    body = respuesta.json()
    assert body == {} or "data" not in body


# --- TC_API_05 - Encadenamiento demostrativo (opcional) --- #
def test_tc_api_05_encadenamiento_crear_usuario_y_validar_id(session):
    """
    ReqRes NO persiste realmente los usuarios creados.
    Encadenamiento demostrativo: validamos que viene un id.
    """
    url = f"{BASE_URL}/users"
    payload = {"name": "luis", "job": "qa automation"}

    respuesta = session.post(url, json=payload, headers=HEADERS, timeout=15)
    log_status_code_api(
        "test_tc_api_05_encadenamiento_crear_usuario_y_validar_id",
        "POST",
        url,
        respuesta.status_code,
    )

    assert respuesta.status_code == 201

    data = respuesta.json()
    user_id = data.get("id")
    assert user_id is not None
    assert str(user_id).strip() != ""
