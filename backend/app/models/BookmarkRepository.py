from sqlmodel import Session, select
from app.models.Bookmark import Bookmark
from fastapi import Depends
from app.core.db import get_session  # get_session 함수 가져오기
from typing import List, Optional

class BookmarkRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, bookmark: Bookmark) -> Bookmark:
        self.session.add(bookmark)
        self.session.commit()
        self.session.refresh(bookmark)
        return bookmark

    def remove(self, bookmark: Bookmark) -> None:
        self.session.delete(bookmark)
        self.session.commit()

    def get(self, user_id: int, job_posting_id: int) -> Optional[Bookmark]:
        statement = select(Bookmark).where(Bookmark.user_id == user_id, Bookmark.item_id == job_posting_id)
        return self.session.exec(statement).first()

    def list(self, user_id: int, page: int, page_size: int) -> List[Bookmark]:
        statement = select(Bookmark).where(Bookmark.user_id == user_id).order_by(Bookmark.created_at.desc())
        return self.session.exec(statement).offset((page - 1) * page_size).limit(page_size).all()

# FastAPI에서 사용할 수 있도록 의존성 주입 함수 추가
def get_bookmark_repository(session: Session = Depends(get_session)) -> BookmarkRepository:
    return BookmarkRepository(session)
