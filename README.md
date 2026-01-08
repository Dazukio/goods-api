# goods-api

## 🇷🇺 Описание (RU)

**goods-api** — это backend-сервис для управления товарами.
Проект задуман как учебно-практический API с упором на:

* чистую структуру,
* контейнеризацию,
* инфраструктуру,
* CI/CD и DevOps-подходы.

Репозиторий используется для экспериментов с архитектурой, Docker, Kubernetes, Terraform и автоматизацией процессов разработки.

---

## 🚀 Основные возможности

* REST API для работы с товарами
* Python backend (структурированный по модулям)
* Docker / Docker Compose
* Подготовка к деплою в Kubernetes
* Infrastructure as Code (Terraform)
* CI (пример конфигурации)

---

## 🧱 Структура проекта

```text
.
├── app/                    # Приложение
│   ├── goods/              # Логика товаров
│   ├── database/           # Работа с БД
│   └── config/             # Конфигурация
├── Dockerfile
├── docker-compose.yml
├── main.py
├── pyproject.toml
├── terraform / k8s yaml
└── README.md
```

---

## ▶️ Запуск локально

### 1. Клонирование репозитория

```bash
git clone git@github.com:Dazukio/goods-api.git
cd goods-api
```

### 2. Запуск через Docker Compose

```bash
docker-compose up --build
```

---

## 🛠 Используемые технологии

* Python
* Docker / Docker Compose
* PostgreSQL
* Kubernetes (YAML manifests)
* Terraform
* GitHub

---

## 📌 Статус проекта

Проект находится в активной разработке и используется в учебных и практических целях.
Функциональность и структура могут меняться.

---

## 👤 Автор

**Dazukio**
GitHub: [https://github.com/Dazukio](https://github.com/Dazukio)

---

---

## 🇬🇧 Description (EN)

**goods-api** is a backend service for managing goods.
This project is built as a practice-oriented API with a focus on:

* clean architecture,
* containerization,
* infrastructure,
* CI/CD and DevOps practices.

The repository is used for experimenting with architecture, Docker, Kubernetes, Terraform, and automation workflows.

---

## 🚀 Features

* REST API for goods management
* Modular Python backend
* Docker & Docker Compose support
* Kubernetes deployment manifests
* Infrastructure as Code (Terraform)
* CI configuration example

---

## ▶️ Local run

```bash
git clone git@github.com:Dazukio/goods-api.git
cd goods-api
docker-compose up --build
```

---

## 📄 License

MIT (or specify another license if needed)
