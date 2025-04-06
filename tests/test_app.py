import subprocess
import requests
import pytest

# Тест 1: Проверка корректности кода в main.py
def test_main_code():
    try:
        # Попробуем выполнить main.py и поймать любые ошибки
        subprocess.run(['python', 'main.py'], check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"main.py не выполнен успешно: {e}")

# Тест 2: Проверка, что все контейнеры запустились и работают
def test_docker_containers():
    try:
        # Получаем список запущенных контейнеров
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, check=True)
        assert 'nginx' in result.stdout, "Контейнер nginx не запущен"
        # Добавьте дополнительные проверки для других контейнеров по мере необходимости
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Ошибка при получении списка контейнеров: {e}")

# Тест 3: Проверка доступности HTML-страницы
def test_html_page():
    url = 'http://localhost'  # Замените на нужный URL, если необходимо
    try:
        response = requests.get(url)
        assert response.status_code == 200, f"Страница не доступна. Код ответа: {response.status_code}"
    except requests.ConnectionError:
        pytest.fail("Не удалось подключиться к серверу")

if __name__ == "__main__":
    pytest.main()
