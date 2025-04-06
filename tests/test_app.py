import subprocess
import requests
import pytest
import time

# Тест 1: Проверка корректности кода в main.py
def test_main_code():
    try:
        # Запускаем main.py в фоновом режиме
        process = subprocess.Popen(['python', 'app/main.py'])
        time.sleep(5)  # Даем время приложению на запуск
        
        # Проверяем доступность HTML-страницы после запуска приложения
        url = 'http://localhost:80'  # Замените на нужный URL, если необходимо
        response = requests.get(url)
        assert response.status_code == 200, f"Страница не доступна. Код ответа: {response.status_code}"
        
    except Exception as e:
        pytest.fail(f"Не удалось запустить main.py или проверить страницу: {e}")
    finally:
        process.terminate()  # Завершаем процесс после теста

# Тест 2: Проверка, что все контейнеры запустились и работают
def test_docker_containers():
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, check=True)
        assert 'nginx' in result.stdout, "Контейнер nginx не запущен"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Ошибка при получении списка контейнеров: {e}")

if __name__ == "__main__":
    pytest.main()
