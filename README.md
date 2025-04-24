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
