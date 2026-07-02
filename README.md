# Backend приложения учёта финансов

Это backend-часть приложения для управления личными финансами.

Приложение реализовано на:
- FastAPI
- Python 3.13
- SQLAlchemy
- Alembic

## Краткая структура проекта

- `src/libs` - общие инфраструктурные и прикладные компоненты, которые используются во всём проекте: аутентификация, константы, работа с базой данных, message bus, утилиты.
- `src/modules` - прикладные доменные модули приложения. Здесь собрана бизнес-логика по отдельным предметным областям.

Основные модули в `src/modules`:
- `accounts` - счета и операции, связанные со счетами.
- `budgets` - бюджеты и их правила.
- `categories` - категории для финансовых операций.
- `identity` - пользователи, сессии и аутентификация.
- `transactions` - финансовые транзакции.

## Что умеет backend

- Аутентификация и работа с JWT
- RBAC: роли `user` (по умолчанию) и `admin`, роль хранится в JWT и проверяется зависимостью `require_role`
- Работа со счетами
- Работа с транзакциями
- Работа с бюджетами
- Работа с категориями
- Публикация и обработка доменных событий

## Требования

Перед запуском убедитесь, что установлены:
- Python 3.13
- PostgreSQL
- `uv` для установки зависимостей

Также должны быть заданы переменные окружения:
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_ENGINE`
- `DB_ALEMBIC_HOST`
- `DB_ALEMBIC_PORT`
- `DB_MIGRATION_ENGINE`
- `AUTHENTICATION_JWT_PRIVATE_KEY_PATH`
- `AUTHENTICATION_JWT_PUBLIC_KEY_PATH`
- `AUTHENTICATION_JWT_ACCESS_EXPIRATION_SECONDS` (необязательно, по умолчанию `300`)
- `AUTHENTICATION_JWT_REFRESH_EXPIRATION_SECONDS` (необязательно, по умолчанию `3600`)
- `ADMIN_EMAIL` (необязательно) - email уже зарегистрированного пользователя, которому при старте приложения будет выдана роль `admin`

По умолчанию backend ожидает подключение к PostgreSQL и использует `.env` через `python-dotenv`.

### Роли и RBAC

Каждый пользователь имеет роль `user` (по умолчанию) или `admin`. Роль передаётся в claim `role` JWT-токена и проверяется зависимостью `require_role` (`src/libs/authentication/authentication_client.py`) на административных эндпоинтах, например `GET /identity/admin/users`.

Роль `admin` нельзя получить через публичную регистрацию (`POST /identity/users`). Чтобы назначить администратора:
1. Зарегистрируйте пользователя обычным способом.
2. Укажите его email в переменной окружения `ADMIN_EMAIL` и перезапустите сервер - при старте роль будет обновлена автоматически.
3. Пользователю нужно заново залогиниться (`POST /identity/auth`), чтобы получить новый JWT с ролью `admin` - действующие токены роль не обновляют.

## Установка зависимостей

```bash
uv pip install --system -r pyproject.toml
```

## Запуск в режиме разработки

```bash
uvicorn src.server:app --host 0.0.0.0 --port 8000
```

После запуска API будет доступно по адресу:
- http://localhost:8000

## Применение миграций

```bash
alembic upgrade head
```

## Запуск через Docker

Сборка образа:

```bash
docker build -t finance-backend .
```

Запуск контейнера:

```bash
docker run --rm -p 8000:8000 --env-file .env finance-backend
```

После запуска откройте:
- http://localhost:8000
