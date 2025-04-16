import os
import time
import requests
import pytest
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL", "http://localhost")


def test_app_is_reachable():
    for _ in range(10):
        try:
            response = requests.get(SERVICE_URL)
            assert response.status_code == 200, f"Ошибка доступа. Код: {response.status_code}"
            return
        except requests.ConnectionError:
            time.sleep(1)
    pytest.fail("Приложение не запустилось вовремя или недоступно.")


def test_api_health():
    try:
        response = requests.get(SERVICE_URL + "/health")
        assert response.status_code == 200
        assert response.json().get("status") == "ok"
    except Exception as e:
        pytest.fail(f"Ошибка при обращении к API /health: {e}")


def test_api_users_endpoint():
    try:
        response = requests.get(SERVICE_URL + "/users")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    except Exception as e:
        pytest.fail(f"Ошибка при обращении к API /users: {e}")


def test_invalid_route():
    response = requests.get(SERVICE_URL + "/nonexistent")
    assert response.status_code == 404, "Ожидался 404, но получен другой код"
