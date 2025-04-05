import os
import pytest
from app import main
from flask import Flask

@pytest.fixture
def client():
    # Устанавливаем переменные окружения для теста
    os.environ['POSTGRES_DB'] = 'mydatabase'
    os.environ['POSTGRES_USER'] = 'myuser'
    os.environ['POSTGRES_PASSWORD'] = 'mypassword'

    main.app.config['TESTING'] = True
    client = main.app.test_client()

    yield client

def test_index_status_code(client):
    response = client.get('/')
    assert response.status_code == 200

def test_index_contains_table(client):
    response = client.get('/')
    assert b'<table' in response.data
    assert b'<th>Name</th>' in response.data
