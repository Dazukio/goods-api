# Goods API

## 🇷🇺 Описание (Russian)

**Goods API** — учебный / pet-проект backend-сервиса для работы с товарами.
Проект демонстрирует типичную архитектуру API-приложения на Python с разделением на домены, конфигурацию, инфраструктуру и деплой.

Цель проекта:

* отработать структуру backend-приложения
* показать работу с БД
* подготовить сервис к контейнеризации и деплою
* приблизиться к real-world backend разработке

---

## 🚀 Возможности

* REST API для работы с товарами
* Чёткое разделение слоёв (routers / models / database)
* Конфигурация через YAML
* Docker и docker-compose
* Kubernetes manifests
* Terraform конфигурация
* Poetry для управления зависимостями

---

## 📂 Структура проекта

```text
.
├── api_deployment.yml        # Kubernetes Deployment для API
├── api_service.yml           # Kubernetes Service для API
├── app/                      # Основное приложение
│   ├── config/               # Конфигурация приложения
│   │   └── conf.py
│   ├── database/             # Работа с базой данных
│   │   ├── db.py
│   │   └── __init__.py
│   ├── goods/                # Домен "товары"
│   │   ├── models/           # Модели данных
│   │   │   ├── goods.py
│   │   │   └── __init__.py
│   │   ├── routers/          # HTTP роуты
│   │   │   ├── goods.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   └── __init__.py
├── db_config.yml             # Конфигурация БД
├── db_secrets_example.yml    # Пример secrets (без реальных данных)
├── db_secrets.yml            # Реальные secrets (не должен попадать в git)
├── docker-compose.yml        # Локальный запуск
├── Dockerfile                # Docker образ приложения
├── main.py                   # Точка входа
├── main.tf                   # Terraform конфигурация
├── postgres_pvc.yml          # Kubernetes PVC для Postgres
├── postgres_service.yml      # Kubernetes Service для Postgres
├── postgres_stateful.yml     # Kubernetes StatefulSet для Postgres
├── pyproject.toml            # Poetry конфигурация
├── poetry.lock
├── README.md
└── LICENSE
```

---

## 🐳 Запуск через Docker

```bash
docker-compose up --build
```

После запуска API будет доступен локально (адрес зависит от конфигурации).

---

## ☸ Kubernetes

В репозитории присутствуют манифесты для деплоя:

* API
* PostgreSQL (StatefulSet + PVC + Service)

Файлы:

* `api_deployment.yml`
* `api_service.yml`
* `postgres_stateful.yml`
* `postgres_pvc.yml`
* `postgres_service.yml`

---

## 🧱 Terraform

Файл `main.tf` содержит базовую Terraform-конфигурацию и может быть использован
для развёртывания инфраструктуры (в зависимости от выбранного провайдера).

---

## 🔐 Secrets

⚠️ **Важно**

Файл `db_secrets.yml`:

* содержит чувствительные данные
* **не должен быть закоммичен**
* используется только локально или через CI/CD

В репозитории хранится только:

```text
db_secrets_example.yml
```

---

## 🛠 Технологии

* Python
* FastAPI (или аналогичный ASGI-фреймворк)
* PostgreSQL
* Docker / Docker Compose
* Kubernetes
* Terraform
* Poetry

---

## 📌 Статус проекта

Проект находится в активной разработке и используется как:

* учебный проект
* playground для backend / DevOps практик

---

## 👤 Автор

**Dazukio**
GitHub: [https://github.com/Dazukio](https://github.com/Dazukio)

---

---

## 🇬🇧 Description (English)

**Goods API** is a backend pet project that demonstrates a typical API service architecture built with Python.

The project focuses on:

* clean backend structure
* database interaction
* containerization
* Kubernetes deployment
* infrastructure as code basics

---

## ✨ Features

* REST API for goods management
* Modular application structure
* YAML-based configuration
* Docker & Docker Compose
* Kubernetes manifests
* Terraform configuration
* Poetry dependency management

---

## 🧑‍💻 Author

**Dazukio**
GitHub: [https://github.com/Dazukio](https://github.com/Dazukio)
