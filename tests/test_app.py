import requests

def test_main_endpoint():
    response = requests.get('http://nginx:80/')  # Предполагается, что ваш Nginx проксирует запросы к приложению
    assert response.status_code == 200  # Проверяем, что ответ успешный (HTTP 200)
