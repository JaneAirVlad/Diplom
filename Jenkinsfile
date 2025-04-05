pipeline {
    agent any

    environment {
        POSTGRES_DB = 'mydatabase'
        POSTGRES_USER = 'myuser'
        POSTGRES_PASSWORD = 'mypassword'
    }

    stages {
        stage('Checkout') {
            steps {
                // Клонируем репозиторий
                git 'https://github.com/JaneAirVlad/Diplom.git'
            }
        }
        
        stage('Build') {
            steps {
                // Сборка Docker образа
                script {
                    docker.build("myapp")
                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                  sh 'pip install -r app/requirements.txt'
                  sh 'pytest tests'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    // Деплой с использованием docker-compose
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }
        
        stage('Post-Deploy') {
            steps {
                script {
                    // Пример пост-развертывания (например, очистка или проверка)
                    sh 'docker-compose logs'
                }
            }
        }
    }

    post {
        always {
            // Чистим после каждого запуска (например, удаляем контейнеры)
            sh 'docker-compose down'
        }
    }
}
