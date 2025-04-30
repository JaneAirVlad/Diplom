pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['dev', 'prod'], description: 'Выбери окружение для деплоя')
    }

    environment {
        POSTGRES_DB = ''
        POSTGRES_USER = ''
        POSTGRES_PASSWORD = ''
        IMAGE_NAME = ''
        CLUSTER_NAME = ''
        REGION = ''
        PROJECT_ID = ''
        SONAR_HOST_URL = ''
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'github-pat', branch: 'main', url: ''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEY')]) {
                    sh '''
                        echo "[INFO] Авторизация в GCP..."
                        gcloud auth activate-service-account --key-file=$GCP_KEY
                        gcloud auth configure-docker --quiet

                        echo "[INFO] Сборка и пуш Docker-образа..."
                        docker build -t diplom_aplicate:latest ./app
                        docker tag diplom_aplicate:latest $IMAGE_NAME
                        docker push $IMAGE_NAME
                    '''
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withCredentials([string(credentialsId: 'SONARQUBE_TOKEN', variable: 'SONAR_TOKEN')]) {
                    sh '''
                        echo "[INFO] Установка SonarScanner..."
                        curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                        unzip -qo sonar-scanner.zip
                        export PATH=$PWD/sonar-scanner-5.0.1.3006-linux/bin:$PATH

                        echo "[INFO] Запуск анализа SonarQube..."
                        sonar-scanner \
                          -Dsonar.projectKey=diplom \
                          -Dsonar.sources=app \
                          -Dsonar.host.url=$SONAR_HOST_URL \
                          -Dsonar.login=$SONAR_TOKEN
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'gcp-sa-key', variable: 'GCP_KEY')]) {
                    sh '''
                        echo "[INFO] Авторизация и подключение к кластеру GKE..."
                        gcloud auth activate-service-account --key-file=$GCP_KEY
                        gcloud container clusters get-credentials $CLUSTER_NAME --region $REGION --project $PROJECT_ID

                        echo "[INFO] Удаление старого деплоймента..."
                        kubectl delete deployment diplom-app -n diplom --ignore-not-found=true

                        echo "[INFO] Деплой в Kubernetes..."
                        kubectl apply -n diplom -f k8s-cluster/deployment.yaml
                        kubectl apply -n diplom -f k8s-cluster/postgres-deployment.yaml
                        kubectl apply -n diplom -f k8s-cluster/postgres-service.yaml
                        kubectl apply -n diplom -f k8s-cluster/postgres.yaml
                        kubectl apply -n diplom -f k8s-cluster/service.yaml

                        echo "[INFO] Применение Grafana..."
                        kubectl apply -f k8s-cluster/grafana-service.yaml
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "[INFO] Запуск тестов..."
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r app/requirements.txt
                    PYTHONPATH=${WORKSPACE}/tests pytest tests/test_app.py --junitxml=pytest_results.xml
                '''
            }
            post {
                always {
                    junit 'pytest_results.xml'
                }
            }
        }

        stage('Security Scan (Bandit)') {
            steps {
                sh '''
                    echo "[INFO] Запуск Bandit..."
                    pip install --user bandit
                    export PATH=$HOME/.local/bin:$PATH
                    bandit -r app -f html -o bandit_report.html || true
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'bandit_report.html', onlyIfSuccessful: false
                }
            }
        }

        stage('Dependency Scan (Snyk CLI)') {
            steps {
                withCredentials([string(credentialsId: 'snyk-api-token', variable: 'SNYK_TOKEN')]) {
                    sh '''
                        echo "[INFO] Установка и запуск Snyk..."
                        mkdir -p snyk-bin
                        curl -sSL https://static.snyk.io/cli/latest/snyk-linux -o snyk-bin/snyk
                        chmod +x snyk-bin/snyk
                        export PATH="${PWD}/snyk-bin:$PATH"

                        snyk auth $SNYK_TOKEN
                        cd app
                        python3 -m venv .venv
                        . .venv/bin/activate
                        pip install -e .

                        snyk test --file=setup.py --command=python3 || true
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker-compose down || true'
        }
    }
}
