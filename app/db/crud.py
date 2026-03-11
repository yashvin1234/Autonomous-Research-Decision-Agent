from sqlalchemy.orm import Session
from app.models.db_models import User, Chat, Message


# ---------- USER ----------
def get_or_create_user(db: Session, email: str, name: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user

    user = User(email=email, name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# ---------- CHAT ----------
def create_chat(db: Session, user_id: int, title: str):
    chat = Chat(user_id=user_id, title=title)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chat(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()


def get_chat_messages(db: Session, chat_id: int):
    return (
        db.query(Message)
        .filter(Message.chat_id == chat_id)
        .order_by(Message.created_at.asc())  # important!
        .all()
    )


# ---------- MESSAGE ----------
def add_message(db: Session, chat_id: int, role: str, content: str):
    msg = Message(chat_id=chat_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def get_user_chats(db: Session, user_id: int):
    return (
        db.query(Chat)
        .filter(Chat.user_id == user_id)
        .order_by(Chat.created_at.desc())
        .all()
    )
