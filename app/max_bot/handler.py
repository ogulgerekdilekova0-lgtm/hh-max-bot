"""MAX messenger integration module."""

from app.config import MAX_BOT_TOKEN
from app.database import SessionLocal, init_db
from app.database.crud import get_or_create_user, save_message
from app.yandex_assistant.assistant import ask_assistant


async def handle_user_message(max_user_id: str, text: str, display_name: str | None = None) -> str:
    """Process one incoming MAX message and return bot reply."""
    answer = ask_assistant(text)

    db = SessionLocal()
    try:
        user = get_or_create_user(db, max_user_id=max_user_id, display_name=display_name)
        save_message(db, user.id, question=text, answer=answer)
    finally:
        db.close()

    return answer


def run_bot() -> None:
    """Start MAX bot polling loop."""
    if not MAX_BOT_TOKEN:
        raise RuntimeError("MAX_BOT_TOKEN is missing in .env")

    init_db()

    try:
        from maxogram.client.bot import Bot
        from maxogram.dispatcher.dispatcher import Dispatcher
        from maxogram.dispatcher.router import Router
        from maxogram.types.message import Message
    except ImportError as exc:
        raise RuntimeError("Install dependencies: pip install -r requirements.txt") from exc

    router = Router()
    bot = Bot(token=MAX_BOT_TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    @router.message_created()
    async def on_message(event: Message, **kwargs: object) -> None:
        text = (event.body.text or "").strip()
        chat_id = event.recipient.chat_id
        sender_id = str(event.sender.user_id) if event.sender else "unknown"

        if not text or not chat_id:
            return

        if text.lower() in {"/start", "start", "начать"}:
            reply = (
                "Привет! Я бот-помощник по API HH.ru. "
                "Задайте вопрос по документации, и я постараюсь ответить."
            )
        else:
            reply = await handle_user_message(
                max_user_id=sender_id,
                text=text,
                display_name=getattr(event.sender, "name", None),
            )

        await bot.send_message(chat_id=chat_id, text=reply)

    print("MAX bot is running...")
    dispatcher.run_polling(bot)


if __name__ == "__main__":
    run_bot()
