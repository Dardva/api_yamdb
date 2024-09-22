### YaMDb API

**YaMDb** — это API для управления отзывами, рейтингами и комментариями на произведения в различных категориях, таких как книги, фильмы и музыка.

## **Описание**

**YaMDb** собирает отзывы пользователей на произведения. Пользователи могут оставлять отзывы, ставить оценки и обсуждать произведения с другими участниками платформы. API предоставляет функционал для взаимодействия с произведениями, категориями, жанрами, отзывами и комментариями, обеспечивая удобные методы для создания, редактирования и удаления контента.

## **Возможности**

- **Управление произведениями (создание, редактирование, удаление)**
- **Категоризация произведений по жанрам и категориям**
- **Создание и управление отзывами и оценками на произведения**
- **Добавление комментариев к отзывам**
- **Аутентификация пользователей с использованием JWT-токенов**
- **Управление пользователями и назначение ролей (пользователь, модератор, администратор)**

## **Стек технологий**

- **Python 3.7+**
- **Django 2.2**
- **Django REST Framework**
- **Simple JWT** — аутентификация по JWT-токену
- **SQLite** или **PostgreSQL** — база данных
- **Swagger / ReDoc** для автоматической генерации документации API

## **Установка**

### 1. Клонирование репозитория

**Склонируйте репозиторий на ваш локальный компьютер:**

```bash
git clone https://github.com/your-username/yamdb.git
cd yamdb
```

### 2. Создание и активация виртуального окружения

**Создайте виртуальное окружение и активируйте его:**

```bash
python -m venv venv
source venv/bin/activate  # для Linux и macOS
venv\Scripts\activate     # для Windows
```

### 3. Установка зависимостей

**Установите все необходимые зависимости:**

```bash
pip install -r requirements.txt
```

### 4. Применение миграций

**Примените миграции для настройки базы данных:**

```bash
python manage.py migrate
```

### 5. Создание суперпользователя

**Создайте суперпользователя для доступа к админке:**

```bash
python manage.py createsuperuser
```

### 6. Запуск сервера

**Запустите локальный сервер:**

```bash
python manage.py runserver
```

***Теперь приложение доступно по адресу http://127.0.0.1:8000/.***

### Документация API

**После запуска сервера, документация API будет доступна по следующим адресам:**

- **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **ReDoc:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## **Примеры запросов и ответов**

### Регистрация нового пользователя

**Запрос:**

```bash
POST /api/v1/auth/signup/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "user123"
}
```

**Ответ:**

```json
{
  "email": "user@example.com",
  "username": "user123"
}
```

### Получение JWT-токена

**Запрос:**

```bash
POST /api/v1/auth/token/
Content-Type: application/json

{
  "username": "user123",
  "confirmation_code": "your_confirmation_code"
}
```

**Ответ:**

```json
{
  "token": "your_jwt_token"
}
```

### Получение списка категорий

**Запрос:**

```bash
GET /api/v1/categories/
```

**Ответ:**

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "name": "Книги",
      "slug": "books"
    },
    {
      "name": "Фильмы",
      "slug": "movies"
    },
    {
      "name": "Музыка",
      "slug": "music"
    }
  ]
}
```

### Добавление нового отзыва

**Запрос:**

```bash
POST /api/v1/titles/1/reviews/
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
  "text": "Это потрясающее произведение!",
  "score": 10
}
```

**Ответ:**

```json
{
  "id": 1,
  "text": "Это потрясающее произведение!",
  "author": "user123",
  "score": 10,
  "pub_date": "2024-09-22T14:00:00Z"
}
```

### Добавление комментария к отзыву

**Запрос:**

```bash
POST /api/v1/titles/1/reviews/1/comments/
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
  "text": "Полностью согласен с обзором!"
}
```

**Ответ:**

```json
{
  "id": 1,
  "text": "Полностью согласен с обзором!",
  "author": "user123",
  "pub_date": "2024-09-22T15:00:00Z"
}
```

## **Права доступа**

- **Анонимные пользователи:** могут просматривать произведения, читать отзывы и комментарии.
- **Аутентифицированные пользователи:** могут создавать отзывы, комментарии и ставить оценки произведениям; могут редактировать и удалять свои отзывы и комментарии.
- **Модераторы:** имеют права аутентифицированных пользователей, а также могут удалять и редактировать любые отзывы и комментарии.
- **Администраторы:** имеют полные права на управление проектом и данными.

## **Авторы**

- **Малова Дарьяв** — система регистрации и аутентификации, права доступа, работа с токенами, система подтверждения через e-mail.
- **Данилин Иван** — модели, views и эндпоинты для произведений, категорий, жанров; реализация импорта данных из CSV-файлов.
- **Шевчук Максим** — отзывы, комментарии, рейтинг произведений.

## **Контакты**

*Если у вас есть вопросы или предложения, вы можете связаться с нами:*

- **Email:** support@yamdb.com

## **Лицензия**

**Проект распространяется под лицензией MIT. Подробности можно найти в файле LICENSE.**
