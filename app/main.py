import os
import psycopg2
import requests
from flask import Flask, render_template_string, jsonify

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
            email VARCHAR(100) UNIQUE,
            age INTEGER,
            zodiac_sign VARCHAR(100)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def load_data():
    file_path = "input_data.txt"
    
    if not os.path.exists(file_path):
        print(f"[ERROR] Файл {file_path} не найден.")
        return

    with open(file_path, "r") as f:
        lines = f.readlines()

    if len(lines) < 4:
        print("[ERROR] Недостаточно строк в input_data.txt")
        return

    name = lines[0].strip()
    email = lines[1].strip()
    age = int(lines[2].strip())
    zodiac_sign = lines[3].strip()

    try:
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host=os.getenv("DB_HOST", "postgres")
        )
        cursor = conn.cursor()

        # Проверка, есть ли пользователь с таким email
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            print(f"[INFO] Пользователь с email {email} уже существует, пропускаем.")
        else:
            cursor.execute(
                'INSERT INTO users (name, email, age, zodiac_sign) VALUES (%s, %s, %s, %s)',
                (name, email, age, zodiac_sign)
            )
            conn.commit()
            print(f"[INFO] Добавлен пользователь: {name} ({email})")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Ошибка при добавлении данных в БД: {e}")

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
                <th>Age</th>
                <th>Zodiac Sign</th>
            </tr>
            {% for user in users %}
            <tr>
                <td>{{ user[0] }}</td>
                <td>{{ user[1] }}</td>
                <td>{{ user[2] }}</td>
                <td>{{ user[3] }}</td>
                <td>{{ user[4] }}</td>
            </tr>
            {% endfor %}
        </table>
    ''', users=users)

@app.route('/users')
def get_users():
    conn = psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.getenv("DB_HOST", "postgres")
    )
    cursor = conn.cursor()
    cursor.execute('SELECT name, email, age, zodiac_sign FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify([
        {
            "name": user[0],
            "email": user[1],
            "age": user[2],
            "zodiac_sign": user[3]
        } for user in users
    ])

@app.route('/health')
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    init_db()
    load_data()
    app.run(host='0.0.0.0', port=5000)
