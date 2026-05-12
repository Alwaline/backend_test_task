# Backend TT — Система аутентификации и авторизации

REST API на Django + DRF с кастомной JWT-аутентификацией и ролевой моделью доступа (RBAC).

---

## Стек

- Python 3.13
- Django 5.x + Django REST Framework
- PostgreSQL 16
- PyJWT — генерация и валидация токенов
- bcrypt — хэширование паролей
- drf-spectacular — Swagger документация
- Docker + Docker Compose

---

## Архитектура системы прав доступа

### Схема БД

```
User ──────────── Role
 │                  │
 │              AccessRoleRule ──── BusinessElement
 │
Orders (owner → User)
```

### Модели

**`Role`** — роли пользователей:
| Роль | Описание |
|------|----------|
| `admin` | Полный доступ ко всему |
| `manager` | Чтение всего, создание и изменение заказов |
| `user` | Работа только со своими объектами |
| `guest` | Только чтение своих объектов |

**`BusinessElement`** — типы ресурсов приложения (`orders`, `users`, `roles`)

**`AccessRoleRule`** — правила доступа роли к ресурсу:
| Поле | Описание |
|------|----------|
| `read` | Чтение своих объектов |
| `read_all` | Чтение всех объектов |
| `create` | Создание |
| `update` | Изменение своих объектов |
| `update_all` | Изменение всех объектов |
| `delete` | Удаление своих объектов |
| `delete_all` | Удаление всех объектов |

### Логика проверки прав

1. Запрос приходит → `JWTAuthentication` декодирует токен → устанавливает `request.user`
2. View проверяет `HasPermission(element, action)` — ищет `AccessRoleRule` по паре `(role, element)`
3. Если правило не найдено или `action=False` → 403
4. Если пользователь не аутентифицирован → 401

### Матрица прав (по умолчанию)

| Действие | admin | manager | user | guest |
|----------|-------|---------|------|-------|
| `read_all` orders | ✅ | ✅ | ❌ | ❌ |
| `create` orders | ✅ | ✅ | ✅ | ❌ |
| `update_all` orders | ✅ | ✅ | ❌ | ❌ |
| `delete_all` orders | ✅ | ❌ | ❌ | ❌ |
| `read_all` users | ✅ | ✅ | ❌ | ❌ |
| Управление ролями | ✅ | ❌ | ❌ | ❌ |

---

## Запуск через Docker (рекомендуется)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Alwaline/backend_test_task
cd backend_test_task
```

### 2. Создать `.env`

```env
SECRET_KEY="ваш-секретный-ключ"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

POSTGRES_DB=django_backend_tt
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=django_backend_tt
```

### 3. Запустить

```bash
docker compose up --build
```

### 4. Применить миграции и заполнить данными

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed
```

### 5. Открыть Swagger

```
http://localhost:8000/api/v1/docs/
```

---

## Локальный запуск

### 1. Создать виртуальное окружение

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Настроить `.env` (указать локальные параметры БД)

```env
DB_HOST=localhost
DB_PORT=5432
```

### 3. Запустить

```bash
python manage.py migrate
python manage.py seed
python manage.py runserver
```

---

## Тестовые пользователи (после seed)

| Email | Пароль | Роль |
|-------|--------|------|
| admin@example.com | admin123 | admin |
| manager@example.com | manager123 | manager |
| user@example.com | user123 | user |

---

## API

### Аутентификация

#### Регистрация
```http
POST /api/v1/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password1": "password123",
  "password2": "password123",
  "first_name": "Иван",
  "last_name": "Иванов",
  "patronymic": "Иванович"
}
```

Ответ `201`:
```json
{
  "email": "user@example.com",
  "first_name": "Иван",
  "last_name": "Иванов"
}
```

#### Вход
```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Ответ `200`:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Выход
```http
POST /api/v1/auth/logout/
Authorization: Bearer <token>
```

Ответ `200`:
```json
{
  "message": "Вы вышли из системы"
}
```

#### Мой профиль
```http
GET /api/v1/auth/me/
Authorization: Bearer <token>
```

```http
PATCH /api/v1/auth/me/
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "Новое имя"
}
```

```http
DELETE /api/v1/auth/me/
Authorization: Bearer <token>
```
Мягкое удаление — аккаунт деактивируется (`is_active=False`), вход становится невозможен.

---

### Заказы

```http
GET /api/v1/orders/
Authorization: Bearer <token>
```

```http
POST /api/v1/orders/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Заказ №1"
}
```

```http
PATCH /api/v1/orders/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Обновлённый заказ"
}
```

```http
DELETE /api/v1/orders/{id}/
Authorization: Bearer <token>
```

---

### Пользователи

```http
GET /api/v1/users/
Authorization: Bearer <token>
```

```http
GET /api/v1/users/{id}/
Authorization: Bearer <token>
```

```http
PATCH /api/v1/users/{id}/
Authorization: Bearer <token>
```

```http
DELETE /api/v1/users/{id}/
Authorization: Bearer <token>
```

---

### Управление правами (только admin)

```http
GET /api/v1/admin/roles/
GET /api/v1/admin/roles/{id}/
POST /api/v1/admin/roles/
PATCH /api/v1/admin/roles/{id}/
DELETE /api/v1/admin/roles/{id}/
```

```http
GET /api/v1/admin/elements/
GET /api/v1/admin/access-rules/
POST /api/v1/admin/access-rules/
PATCH /api/v1/admin/access-rules/{id}/
```

Все запросы требуют:
```http
Authorization: Bearer <token>
```

---

## Коды ошибок

| Код | Описание |
|-----|----------|
| 401 | Не аутентифицирован / невалидный токен |
| 403 | Недостаточно прав |
| 404 | Объект не найден |
| 400 | Ошибка валидации |

---

## Запуск тестов

```bash
python manage.py test api
```
