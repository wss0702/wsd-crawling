from sqlmodel import Session, create_engine, select
import logging
from contextlib import contextmanager

from app import crud
from app.core.config import settings
from app.models.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

logging.basicConfig(level=logging.INFO)


def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

def init_db(session: Session) -> None:
    logging.info("Initializing the database...")
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)
