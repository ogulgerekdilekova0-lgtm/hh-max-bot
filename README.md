# hh-max-bot

Чат-бот по документации API HH.ru (Yandex Assistant + RAG).

База знаний: https://github.com/hhru/api/tree/master/docs

Если `MAX_BOT_TOKEN` пустой — запуск в консольном режиме (`app/console.py`). Модуль MAX: `app/max_bot/`.

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
python init_db.py
python -m app.main
```

```
python -m app.console
```

## .env

| Поле | Назначение | Пример |
|------|------------|--------|
| DATABASE_URL | PostgreSQL | `postgresql+psycopg2://postgres:pass@localhost:5432/hh_max_bot` |
| MAX_BOT_TOKEN | токен MAX | |
| YANDEX_FOLDER_ID | каталог Yandex Cloud | `b1g0j5pptldea64arrnf` |
| YANDEX_API_KEY | API-ключ | |
| HH_DOCS_REPO_URL | репозиторий docs | `https://github.com/hhru/api` |
| HH_DOCS_BRANCH | ветка | `master` |
| HH_DOCS_PATH | папка docs | `docs` |
| HH_DOCS_CACHE_DIR | локальный кэш | `data/knowledge` |
| INDEX_STATE_PATH | состояние индекса | `data/index_state.json` |
| YANDEX_INDEX_LABEL | метка индекса | `hh-max-bot` |

Секреты загружаются через `load_dotenv()` в `app/config.py`.
