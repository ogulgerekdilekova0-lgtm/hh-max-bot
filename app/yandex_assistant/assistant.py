from pathlib import Path

from app.config import HH_DOCS_CACHE_DIR, YANDEX_API_KEY, YANDEX_FOLDER_ID


def build_or_update_index(docs_dir: str | None = None) -> str:
    docs_path = Path(docs_dir or HH_DOCS_CACHE_DIR)
    if not docs_path.exists() or not any(docs_path.glob("*.md")):
        return "empty"

    if not YANDEX_FOLDER_ID or not YANDEX_API_KEY:
        return "no yandex creds"

    return "ok"


def ask_assistant(question: str) -> str:
    if not question.strip():
        return "Введите вопрос."

    if not YANDEX_FOLDER_ID or not YANDEX_API_KEY:
        return "Yandex Cloud не настроен."

    return "Ответ будет после подключения ассистента."
