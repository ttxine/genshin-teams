# Genshin Teams
[Русский](./README.ru.md)

## Description
A tool for Genshin Impact providing an editor of weapons, artifacts and characters that allows you plan and share your own teams
### Technology
- Backend
    - Python 3
    - FastAPI
    - SQLite
    - PostgreSQL
- Frontend
    - JavaScript
    - VueJS 3
# Backend
## Project setup
1) 
    ```
    cd backend
    ```
2) Virtual environment
    ```
    python -m venv venv
    ```
3) Install dependencies
    ```
    pip install -r requirements.txt
    ```
4) Create an `backend/.env` file and set your environment variables. Example:
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
5) Create superuser
    ```
    python main.py createsuperuser
    ```
### Start server
    ```
    python main.py startserver --reload
    ```

# Frontend
## Project setup
```
cd frontend
```
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```
