"""Yandex Cloud AI Studio: search index and answer generation."""

from pathlib import Path

from app.config import HH_DOCS_CACHE_DIR, YANDEX_API_KEY, YANDEX_FOLDER_ID


def build_or_update_index(docs_dir: str | None = None) -> str:
    """
    Build or refresh the Yandex search index from local HH docs.

    Returns a status message. Full SDK integration is added in sprint 4.
    """
    docs_path = Path(docs_dir or HH_DOCS_CACHE_DIR)
    if not docs_path.exists() or not any(docs_path.glob("*.md")):
        return "Knowledge base is empty. Run docs sync first."

    if not YANDEX_FOLDER_ID or not YANDEX_API_KEY:
        return "Yandex Cloud credentials are missing in .env."

    file_count = len(list(docs_path.glob("*.md")))
    return f"Ready to index {file_count} markdown files in Yandex AI Studio."


def ask_assistant(question: str) -> str:
    """
    Ask Yandex Assistant a question using RAG over HH API docs.

    Placeholder until search index and Responses API are connected.
    """
    if not question.strip():
        return "Пожалуйста, задайте вопрос по документации API HH.ru."

    if not YANDEX_FOLDER_ID or not YANDEX_API_KEY:
        return (
            "Yandex Cloud не настроен. Заполните YANDEX_FOLDER_ID и YANDEX_API_KEY в .env."
        )

    return (
        "Бот получил ваш вопрос. Модуль Yandex Assistant будет подключён на спринте 4. "
        f"Вопрос: {question.strip()}"
    )
