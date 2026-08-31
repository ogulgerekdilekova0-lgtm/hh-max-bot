# HH MAX Bot

Практический проект: чат-бот **MAX** на базе **Yandex Assistant (RAG)** для ответов на вопросы по документации **API HH.ru**.

## Стек

- Python 3.11+
- PostgreSQL + SQLAlchemy
- MAX Bot API (`maxogram`)
- Yandex Cloud AI Studio (YandexGPT + search index)
- База знаний: [hhru/api/docs](https://github.com/hhru/api/tree/master/docs)

## Структура

```
hh-max-bot/
├── app/
│   ├── main.py                 # точка входа
│   ├── config.py               # load_dotenv()
│   ├── max_bot/                # модуль MAX
│   ├── database/               # PostgreSQL + SQLAlchemy
│   ├── yandex_assistant/       # RAG + YandexGPT
│   └── knowledge/              # загрузка docs HH.ru
├── docs/
│   └── ARCHITECTURE.md
├── requirements.txt
├── .env.example
└── .gitignore
```

Подробная архитектура: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Переменные окружения (`.env`)

Скопируйте `.env.example` в `.env` и заполните поля:

| Переменная | Описание | Пример |
|------------|----------|--------|
| `DATABASE_URL` | строка подключения PostgreSQL | `postgresql+psycopg2://postgres:pass@localhost:5432/hh_max_bot` |
| `MAX_BOT_TOKEN` | токен бота MAX | `1234567890:ABC...` |
| `YANDEX_FOLDER_ID` | ID каталога Yandex Cloud | `b1gxxxxxxxxxx` |
| `YANDEX_API_KEY` | API-ключ сервисного аккаунта | `AQVNxxxx...` |
| `HH_DOCS_REPO_URL` | репозиторий HH API | `https://github.com/hhru/api` |
| `HH_DOCS_BRANCH` | ветка с документацией | `master` |
| `HH_DOCS_PATH` | папка docs | `docs` |
| `HH_DOCS_CACHE_DIR` | локальный кэш markdown | `data/knowledge` |

Секреты загружаются через:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Установка

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # заполнить значения
```

### PostgreSQL (Windows)

1. Установить PostgreSQL: https://www.postgresql.org/download/windows/
2. Создать БД `hh_max_bot` в pgAdmin
3. Указать `DATABASE_URL` в `.env`

## Запуск

```bash
python -m app.main
```

Или только модуль MAX:

```bash
python -m app.max_bot.handler
```

## Спринт 1 — подготовка

- [x] Модульная архитектура
- [x] Каркас проекта + requirements.txt
- [x] .env.example + README
- [ ] Изучить Yandex AI Studio SDK
- [ ] Изучить MAX Bot API
- [ ] Ознакомиться со структурой docs HH.ru
- [ ] Загрузить материалы в Октагон

## Автор

Огулгерек — практика Octagon
