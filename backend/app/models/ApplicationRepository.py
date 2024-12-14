from sqlmodel import Session, select
from app.models.Application import Application
from fastapi import Depends
from app.core.db import get_session  # get_session 함수 가져오기
from typing import Optional

class ApplicationRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, application: Application) -> Application:
        self.session.add(application)
        self.session.commit()
        self.session.refresh(application)
        return application

    def get(self, application_id: int) -> Application:
        statement = select(Application).where(Application.id == application_id)
        return self.session.exec(statement).first()

    def delete(self, application_id: int) -> Application:
        application = self.get(application_id)
        if application:
            self.session.delete(application)
            self.session.commit()
            return application
        return None

    def list(self, user_id: int, status: Optional[str] = None) -> list[Application]:
        query = select(Application).where(Application.user_id == user_id)

        if status:
            query = query.where(Application.status == status)

        return self.session.exec(query).all()

# FastAPI에서 사용할 수 있도록 의존성 주입 함수 추가
def get_application_repository(session: Session = Depends(get_session)) -> ApplicationRepository:
    return ApplicationRepository(session)
