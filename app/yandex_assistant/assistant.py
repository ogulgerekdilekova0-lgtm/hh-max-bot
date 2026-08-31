from yandex_ai_studio_sdk import AIStudio

from app.config import HH_DOCS_CACHE_DIR, YANDEX_API_KEY, YANDEX_FOLDER_ID
from app.knowledge.retriever import build_context
from app.yandex_assistant.index_builder import sync_search_index

_sdk: AIStudio | None = None
_model = None


def _get_model():
    global _sdk, _model
    if _model is None:
        _sdk = AIStudio(folder_id=YANDEX_FOLDER_ID, auth=YANDEX_API_KEY)
        _model = _sdk.models.completions("yandexgpt").configure(temperature=0.2)
    return _model


def build_or_update_index(docs_dir: str | None = None) -> str:
    docs_path = docs_dir or HH_DOCS_CACHE_DIR
    return sync_search_index(docs_path)


def ask_assistant(question: str, docs_dir: str | None = None) -> str:
    if not question.strip():
        return "Введите вопрос."

    if not YANDEX_FOLDER_ID or not YANDEX_API_KEY:
        return "Yandex Cloud не настроен. Заполните YANDEX_FOLDER_ID и YANDEX_API_KEY в .env."

    context = build_context(question, docs_dir=docs_dir)
    if not context.strip():
        return "База знаний пуста. Перезапустите бота после загрузки docs HH.ru."

    prompt = [
        {
            "role": "system",
            "text": (
                "Ты помощник по документации API HH.ru. "
                "Отвечай на русском, кратко и по делу. "
                "Используй только переданный контекст."
            ),
        },
        {
            "role": "user",
            "text": f"Контекст из документации:\n{context}\n\nВопрос: {question.strip()}",
        },
    ]

    try:
        result = _get_model().run(prompt)
        answer = result[0].text.strip()
        return answer or "Не удалось сформировать ответ."
    except Exception as exc:
        return f"Ошибка Yandex GPT: {exc}"
