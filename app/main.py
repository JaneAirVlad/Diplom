import os
import psycopg2
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

def init_db():
    conn = psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.getenv("DB_HOST", "postgres")
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            password_count INTEGER
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def load_data():
    # Прямая ссылка на файл input_data.txt в GitHub
    url = "https://raw.githubusercontent.com/JaneAirVlad/jenkins_3/main/input_data.txt"
    
    # Загрузка данных из файла
    response = requests.get(url)
    
    if response.status_code == 200:
        lines = response.text.splitlines()
        
        # Проверяем, что файл содержит достаточное количество строк
        if len(lines) >= 9:
            name = lines[7].strip()
            email = lines[8].strip()
            password_count = int(lines[0].strip())

            conn = psycopg2.connect(
                dbname=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD'],
                host=os.getenv("DB_HOST", "postgres")
            )
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, email, password_count) VALUES (%s, %s, %s)', (name, email, password_count))
            conn.commit()
            cursor.close()
            conn.close()
        else:
            print("Ошибка: недостаточно строк в загруженных данных.")
    else:
        print(f"Ошибка при загрузке данных: {response.status_code}")

@app.route('/')
def index():
    conn = psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.getenv("DB_HOST", "postgres")
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template_string('''
        <h1>Users</h1>
        <table border="1">
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Password Count</th>
            </tr>
            {% for user in users %}
            <tr>
                <td>{{ user[0] }}</td>
                <td>{{ user[1] }}</td>
                <td>{{ user[2] }}</td>
                <td>{{ user[3] }}</td>
            </tr>
            {% endfor %}
        </table>
    ''', users=users)

@app.route('/health')
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    init_db()
    load_data()  
    app.run(host='0.0.0.0', port=5000)
