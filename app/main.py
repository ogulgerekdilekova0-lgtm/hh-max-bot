from app.config import MAX_BOT_TOKEN
from app.database import init_db
from app.knowledge.hh_docs_loader import download_docs
from app.yandex_assistant.assistant import build_or_update_index


def bootstrap() -> None:
    init_db()
    docs_path = download_docs()
    status = build_or_update_index(str(docs_path))
    print(f"index: {status}, docs: {docs_path}")


def main() -> None:
    bootstrap()
    if not MAX_BOT_TOKEN:
        from app.console import run_console

        run_console()
        return

    from app.max_bot.handler import run_bot

    run_bot()


if __name__ == "__main__":
    main()
