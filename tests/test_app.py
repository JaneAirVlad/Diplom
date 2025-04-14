import subprocess
import requests
import pytest
import time

# Тест 1: Проверка корректности кода в main.py
def test_main_code():
    process = subprocess.Popen(['python', 'app/main.py'])
    
    # Ожидаем, пока приложение не станет доступным
    url = 'http://localhost:80'  # Замените на нужный URL, если необходимо
    for _ in range(10):  # Попробуем 10 раз
        try:
            response = requests.get(url)
            assert response.status_code == 200, f"Страница не доступна. Код ответа: {response.status_code}"
            break  # Если запрос успешен, выходим из цикла
        except requests.ConnectionError:
            time.sleep(1)  # Ждем секунду перед следующей попыткой
    else:
        pytest.fail("Приложение не запустилось вовремя.")
    
    process.terminate()  # Завершаем процесс после теста

# Тест 2: Проверка, что все контейнеры запустились и работают
def test_docker_containers():
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, check=True)
        assert 'nginx' in result.stdout, "Контейнер nginx не запущен"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Ошибка при получении списка контейнеров: {e}")

# Тест 3: Проверка доступности базы данных через docker-compose exec
def test_database_connection():
    try:
        command = [
            'docker-compose', 'exec', '-T', 'postgres', 'psql',
            '-U', 'myuser', '-d', 'mydatabase', '-c', 'SELECT 1;'
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Не удалось подключиться к базе данных: {e}")

# Тест 4: Проверка проксирования запросов через Nginx
def test_nginx_proxy():
    url = 'http://localhost'  # Замените на нужный URL вашего Nginx (например, http://localhost)
    try:
        response = requests.get(url)
        assert response.status_code == 200, f"Nginx не проксирует запросы. Код ответа: {response.status_code}"
    except requests.ConnectionError:
        pytest.fail("Не удалось подключиться к серверу Nginx")

# Тест 5: Проверка наличия пользователей в базе данных через docker-compose exec
def test_users_in_database():
    try:
        command = [
            'docker-compose', 'exec', '-T', 'postgres', 'psql',
            '-U', 'myuser', '-d', 'mydatabase', '-c', "SELECT * FROM users;"
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Проверяем вывод команды на наличие пользователей
        output = result.stdout.strip().splitlines()
        
        if len(output) <= 2:  # Если вывод содержит только заголовки и пустую строку
            pytest.fail("Таблица пользователей пуста.")
    
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Ошибка при выполнении команды psql: {e}")

if __name__ == "__main__":
    pytest.main()
