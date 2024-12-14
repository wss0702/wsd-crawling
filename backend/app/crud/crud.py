import uuid
from typing import Any, Optional

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models.models import User, UserCreate, UserUpdate
from app.models.JobPosting import JobPosting
from app.models.JobPostingRepository import get_job_posting_repository, JobPostingRepository
from app.models.Application import Application


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

# JobPosting SQL Model에 대한 CRUD

def list_job_postings(repository: JobPostingRepository, skip: int = 0, limit: int = 20, sort_by: str = "postingId", **filters):
    return repository.list(skip=skip, limit=limit, sort_by=sort_by, **filters)


def get_job_posting(repository: JobPostingRepository, posting_id: int) -> JobPosting | None:
    return repository.get(posting_id)


def create_job_posting(repository: JobPostingRepository, job_posting: JobPosting):
    return repository.create(job_posting)


def create_application(session: Session, user_id: int, job_posting_id: int, resume: Optional[str] = None) -> Application:
    # 중복 지원 체크
    existing_application = session.exec(
        select(Application).where(Application.user_id == user_id, Application.job_posting_id == job_posting_id)
    ).first()
    if existing_application:
        raise ValueError("User has already applied for this job posting.")

    application = Application(user_id=user_id, job_posting_id=job_posting_id, resume=resume)
    session.add(application)
    session.commit()
    session.refresh(application)
    return application


def get_applications(session: Session, user_id: int, status: Optional[str] = None):
    query = select(Application).where(Application.user_id == user_id)
    if status:
        query = query.where(Application.status == status)
    return session.exec(query).all()


def delete_application(session: Session, application_id: int) -> Application:
    application = session.get(Application, application_id)
    if not application:
        raise ValueError("Application not found.")
    
    # 취소 가능 여부 확인 (예: 상태가 applied일 때만 취소 가능)
    if application.status != "applied":
        raise ValueError("Application cannot be withdrawn.")
    
    session.delete(application)
    session.commit()
    return application


