from sqlalchemy.orm import Session

from .models import MessageHistory, User


def get_or_create_user(db: Session, max_user_id: str, display_name: str | None = None) -> User:
    user = db.query(User).filter(User.max_user_id == max_user_id).first()
    if user:
        return user

    user = User(max_user_id=max_user_id, display_name=display_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_message(db: Session, user_id: int, question: str, answer: str) -> MessageHistory:
    record = MessageHistory(user_id=user_id, question=question, answer=answer)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_user_history(db: Session, user_id: int, limit: int = 20) -> list[MessageHistory]:
    return (
        db.query(MessageHistory)
        .filter(MessageHistory.user_id == user_id)
        .order_by(MessageHistory.created_at.desc())
        .limit(limit)
        .all()
    )
