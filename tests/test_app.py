import pytest
import psycopg2

# Фикстура для подключения к базе данных
@pytest.fixture(scope='module')
def db_connection():
    conn = psycopg2.connect("dbname='mydatabase' user='myuser' host='db' password='mypassword'")
    yield conn
    conn.close()

# Фикстура для настройки базы данных перед тестами
@pytest.fixture(scope='module', autouse=True)
def setup_database(db_connection):
    cursor = db_connection.cursor()
    # Создание таблиц и начальных данных
    cursor.execute("CREATE TABLE IF NOT EXISTS test_table (id SERIAL PRIMARY KEY, name VARCHAR(100));")
    db_connection.commit()
    
    yield
    
    # Очистка таблиц после тестов
    cursor.execute("DROP TABLE IF EXISTS test_table;")
    db_connection.commit()

# Пример теста для вставки записи в базу данных
def test_database_insertion(db_connection):
    cursor = db_connection.cursor()
    
    # Вставка записи
    cursor.execute("INSERT INTO test_table (name) VALUES ('test_name');")
    db_connection.commit()
    
    # Проверка вставленной записи
    cursor.execute("SELECT * FROM test_table WHERE name='test_name';")
    result = cursor.fetchall()
    
    assert len(result) == 1
    assert result[0][1] == 'test_name'
