# Genshin Teams
[English](./README.md)

[Техническое задание](./docs/technical_requirements.md)

## Описание
Инструмент для Genshin Impact, предоставляющий редактор оружия, артефактов и персонажей и позволяющий планировать и делиться своими собственными командами.
### Стек технологий
- Backend
    - Python 3
    - FastAPI
    - SQLite
    - PostgreSQL
- Frontend
    - JavaScript
    - VueJS 3
# Backend
## Начало работы
1) 
    ```
    cd backend
    ```
2) Виртуальное окружение
    ```
    python -m venv venv
    ```
3) Установить зависимости
    ```
    pip install -r requirements.txt
    ```
4) Создать `backend/.env` файл и установить переменные окружения. Пример:
    ```
    SITE_DOMAIN=...
    DATABASE_URL=...
    ACCESS_TOKEN_TYPE=...
    ACCESS_TOKEN_SECRET_KEY=...
    REFRESH_TOKEN_TYPE=...
    REFRESH_TOKEN_SECRET_KEY=...
    EMAIL_CONFIRMATION_TOKEN_TYPE=...
    EMAIL_CONFIRMATION_TOKEN_SECRET_KEY=...
    PASSWORD_RESET_TOKEN_TYPE=..
    PASSWORD_RESET_TOKEN_SECRET_KEY=...
    MAIL_USERNAME=...
    MAIL_PASSWORD=...
    MAIL_FROM=...
    MAIL_PORT=...
    MAIL_SERVER=...
    ```
5) Создать суперпользователя
    ```
    python main.py createsuperuser
    ```
### Запуск сервера
    ```
    python main.py startserver --reload
    ```

# Frontend
## Начало работы
```
cd frontend
```
```
npm install
```

### Запуск сервера
```
npm run serve
```
