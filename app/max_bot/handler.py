import asyncio

from app.config import MAX_BOT_TOKEN
from app.database import SessionLocal, init_db
from app.database.crud import get_or_create_user, save_message
from app.yandex_assistant.assistant import ask_assistant


async def handle_user_message(max_user_id: str, text: str, display_name: str | None = None) -> str:
    answer = await asyncio.to_thread(ask_assistant, text)

    db = SessionLocal()
    try:
        user = get_or_create_user(db, max_user_id=max_user_id, display_name=display_name)
        save_message(db, user.id, question=text, answer=answer)
    finally:
        db.close()

    return answer


def run_bot() -> None:
    if not MAX_BOT_TOKEN:
        raise RuntimeError("MAX_BOT_TOKEN is missing")

    init_db()

    from maxogram.client.bot import Bot
    from maxogram.dispatcher.dispatcher import Dispatcher
    from maxogram.dispatcher.router import Router
    from maxogram.types.message import Message

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

        if text.lower() in {"/start", "start"}:
            reply = "Привет. Задайте вопрос по API HH.ru."
        else:
            reply = await handle_user_message(
                max_user_id=sender_id,
                text=text,
                display_name=getattr(event.sender, "name", None),
            )

        await bot.send_message(chat_id=chat_id, text=reply)

    dispatcher.run_polling(bot)


if __name__ == "__main__":
    run_bot()
