import requests
import pytest
import time

SERVICE_URL = "http://35.205.72.135/"

# Тест 1: Проверка, что приложение запустилось и доступно
def test_app_is_reachable():
    for _ in range(10):
        try:
            response = requests.get(SERVICE_URL)
            assert response.status_code == 200, f"Ошибка доступа. Код: {response.status_code}"
            return
        except requests.ConnectionError:
            time.sleep(1)
    pytest.fail("Приложение не запустилось вовремя или недоступно.")

# Тест 2: Проверка, что API работает корректно (если есть endpoint)
def test_api_health():
    try:
        response = requests.get(SERVICE_URL + "/health")
        assert response.status_code == 200
        assert response.json().get("status") == "ok"
    except Exception as e:
        pytest.fail(f"Ошибка при обращении к API /health: {e}")
