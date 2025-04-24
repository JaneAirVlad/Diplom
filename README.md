# Дипломный проект

Веб-приложение на Flask, которое:
- подключается к PostgreSQL
- отображает таблицу пользователей
- показывает информацию через REST API (`/users`, `/health`)
- интегрировано с Jenkins, SonarQube, Grafana, Prometheus
- развёрнуто в Kubernetes (GKE) с поддержкой HTTPS через DuckDNS

## Стек технологий

- **Python (Flask)** — основное веб-приложение
- **PostgreSQL** — база данных
- **Docker / Docker Compose** — контейнеризация
- **Kubernetes (GKE)** — оркестрация
- **Terraform** — инфраструктура как код
- **Jenkins** — CI/CD пайплайн
- **Prometheus + Grafana** — мониторинг
- **SonarQube** — анализ кода
- **DuckDNS + Ingress + HTTPS** — внешний доступ

Доступы

- Приложение	https://tabletime.duckdns.org/ или https://35.205.72.135
- SonarQube	https://sonarqube.tabletime.duckdns.org/
- Prometheus	https://prometheus.tabletime.duckdns.org/
- Grafana	https://34.38.103.51
- Jenkins	http://34.135.37.98:8080
