from app.database import init_db
from app.knowledge.hh_docs_loader import download_docs
from app.max_bot.handler import run_bot
from app.yandex_assistant.assistant import build_or_update_index


def bootstrap() -> None:
    init_db()
    docs_path = download_docs()
    status = build_or_update_index(str(docs_path))
    print(f"index: {status}, docs: {docs_path}")


def main() -> None:
    bootstrap()
    run_bot()


if __name__ == "__main__":
    main()
