from app.database import SessionLocal, init_db
from app.database.crud import get_or_create_user, save_message
from app.yandex_assistant.assistant import ask_assistant


def run_console() -> None:
    init_db()
    print("hh-max-bot console")
    db = SessionLocal()
    try:
        user = get_or_create_user(db, max_user_id="cli-local", display_name="console")
        while True:
            try:
                question = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not question or question.lower() in {"exit", "quit", "q"}:
                break
            answer = ask_assistant(question)
            save_message(db, user.id, question=question, answer=answer)
            print(answer)
    finally:
        db.close()


if __name__ == "__main__":
    run_console()
