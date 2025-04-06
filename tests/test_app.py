import subprocess
import requests
import pytest
import time
import psycopg2

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

# Тест 3: Проверка доступности базы данных
def test_database_connection():
    time.sleep(15)
    try:
        conn = psycopg2.connect(
            dbname='mydatabase',  # Замените на имя вашей базы данных
            user='myuser',       # Замените на имя пользователя вашей базы данных
            password='mypassword',# Замените на пароль вашей базы данных
            host='db'               # Замените на адрес вашего сервера базы данных (например, 'db' для Docker)
        )
        conn.close()
    except Exception as e:
        pytest.fail(f"Не удалось подключиться к базе данных: {e}")

# Тест 4: Проверка проксирования запросов через Nginx
def test_nginx_proxy():
    url = 'http://localhost'  # Замените на нужный URL вашего Nginx (например, http://localhost)
    try:
        response = requests.get(url)
        assert response.status_code == 200, f"Nginx не проксирует запросы. Код ответа: {response.status_code}"
    except requests.ConnectionError:
        pytest.fail("Не удалось подключиться к серверу Nginx")

# Тест 5: Проверка наличия пользователей в базе данных
def test_users_in_database():
    try:
        conn = psycopg2.connect(
            dbname='mydatabase',  # Замените на имя вашей базы данных
            user='myuser',       # Замените на имя пользователя вашей базы данных
            password='mypassword',# Замените на пароль вашей базы данных
            host='db'               # Замените на адрес вашего сервера базы данных (например, 'db' для Docker)
        )
        
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        
        assert len(users) > 0, "Нет пользователей в базе данных."
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        pytest.fail(f"Ошибка при проверке пользователей в базе данных: {e}")

if __name__ == "__main__":
    pytest.main()
