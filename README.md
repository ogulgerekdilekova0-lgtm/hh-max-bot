# hh-max-bot

Чат-бот MAX для вопросов по API HH.ru.

База знаний: https://github.com/hhru/api/tree/master/docs

## Установка

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

PostgreSQL: https://www.postgresql.org/download/windows/

## Запуск

```
python -m app.main
```

## .env

| Поле | Пример |
|------|--------|
| DATABASE_URL | postgresql+psycopg2://postgres:pass@localhost:5432/hh_max_bot |
| MAX_BOT_TOKEN | токен бота MAX |
| YANDEX_FOLDER_ID | id каталога Yandex Cloud |
| YANDEX_API_KEY | api-ключ Yandex Cloud |
| HH_DOCS_REPO_URL | https://github.com/hhru/api |
| HH_DOCS_BRANCH | master |
| HH_DOCS_PATH | docs |
| HH_DOCS_CACHE_DIR | data/knowledge |

Секреты загружаются через `load_dotenv()` в `app/config.py`.
