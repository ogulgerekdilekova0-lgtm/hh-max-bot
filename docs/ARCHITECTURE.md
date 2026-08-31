# HH MAX Bot — архитектура проекта

## Цель

Чат-бот **MAX** на базе **Yandex Assistant (RAG + YandexGPT)** отвечает на вопросы разработчиков по документации **API HH.ru**.

Источник знаний: https://github.com/hhru/api/tree/master/docs

## Модули (по ТЗ)

```
┌─────────────────────────────────────────────────────────┐
│                    app/main.py                          │
│              (общий orchestrator)                       │
└────────────┬──────────────┬──────────────┬──────────────┘
             │              │              │
    ┌────────▼────────┐ ┌───▼──────────┐ ┌─▼──────────────────┐
    │  app/max_bot/   │ │ app/database/│ │ app/yandex_assist. │
    │  MAX messenger  │ │ PostgreSQL   │ │ RAG + YandexGPT    │
    └────────┬────────┘ └───▲──────────┘ └─▲──────────────────┘
             │              │              │
             │         история диалогов    │
             │                             │
             └──────────► app/knowledge/ ◄─┘
                          HH docs sync
```

| № | Модуль | Папка | Ответственность |
|---|--------|-------|-----------------|
| 1 | Orchestrator | `app/main.py` | запуск, связка модулей |
| 2 | Database | `app/database/` | users, message_history, SQLAlchemy |
| 3 | MAX | `app/max_bot/` | приём/отправка сообщений в MAX |
| 4 | Yandex Assistant | `app/yandex_assistant/` | индекс, RAG, ответы |
| — | Knowledge | `app/knowledge/` | загрузка markdown из GitHub HH |

> В плане наставника в задаче 3 указан Telegram — в описании проекта мессенджер **MAX**. Реализуем **MAX**; при необходимости Telegram — отдельный модуль позже.

## База данных (PostgreSQL + SQLAlchemy)

### Таблица `users`
| Поле | Тип | Описание |
|------|-----|----------|
| id | INT PK | внутренний id |
| max_user_id | VARCHAR(64) UNIQUE | id пользователя в MAX |
| display_name | VARCHAR(255) | имя (опционально) |
| created_at | DATETIME | дата регистрации |

### Таблица `message_history`
| Поле | Тип | Описание |
|------|-----|----------|
| id | INT PK | id сообщения |
| user_id | FK → users | пользователь |
| question | TEXT | вопрос пользователя |
| answer | TEXT | ответ бота |
| created_at | DATETIME | время диалога |

## Поток обработки сообщения

1. Пользователь пишет боту в **MAX**
2. `max_bot` получает текст
3. `yandex_assistant` ищет ответ в базе знаний HH (RAG)
4. `database` сохраняет вопрос и ответ
5. `max_bot` отправляет ответ пользователю

## Спринты

| Спринт | Задача |
|--------|--------|
| **1** (текущий) | изучение SDK, архитектура, каркас repo |
| **2** | модуль БД (полная реализация + миграции) |
| **3** | модуль MAX (полный polling/webhook) |
| **4** | Yandex Assistant + автообновление KB |
| **5** | интеграция, тесты, видео-демо |

## Технологии

- Python 3.11+
- PostgreSQL + SQLAlchemy
- MAX: `maxogram` / https://dev.max.ru/docs-api
- Yandex Cloud AI Studio SDK + search indexes
- HH docs: markdown из GitHub
