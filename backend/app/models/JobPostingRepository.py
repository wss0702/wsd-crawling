from sqlmodel import Session, select
from app.models.JobPosting import JobPosting
from fastapi import Depends
from app.core.db import get_session  # get_session 함수 가져오기

class JobPostingRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, posting: JobPosting) -> JobPosting:
        # 중복 확인
        existing_posting = self.session.exec(
            select(JobPosting).where(JobPosting.postingId == posting.postingId)
        ).first()
        if existing_posting:
            return existing_posting  # 중복된 경우 기존 게시물 반환

        self.session.add(posting)
        self.session.commit()
        self.session.refresh(posting)
        return posting

    def get(self, posting_id: int) -> JobPosting:
        statement = select(JobPosting).where(JobPosting.postingId == posting_id)
        return self.session.exec(statement).first()

    def update(self, posting: JobPosting) -> JobPosting:
        self.session.add(posting)
        self.session.commit()
        self.session.refresh(posting)
        return posting

    def delete(self, posting_id: int) -> JobPosting:
        posting = self.get(posting_id)
        if posting:
            self.session.delete(posting)
            self.session.commit()
            return posting
        return None

    def list(self, skip: int = 0, limit: int = 20, sort_by: str = "postingId", **filters) -> list[JobPosting]:
        query = select(JobPosting)

        # 필터링
        if "location" in filters and filters["location"]:
            query = query.where(JobPosting.location == filters["location"])
        if "experience" in filters and filters["experience"]:
            query = query.where(JobPosting.experience == filters["experience"])
        if "salary" in filters and filters["salary"] is not None:
            query = query.where(JobPosting.salary >= filters["salary"])
        if "skills" in filters and filters["skills"]:
            query = query.where(JobPosting.skills.contains(filters["skills"]))

        # 정렬
        query = query.order_by(getattr(JobPosting, sort_by))

        # 세션을 사용하여 쿼리 실행
        return self.session.exec(query.offset(skip).limit(limit)).all()

# FastAPI에서 사용할 수 있도록 의존성 주입 함수 추가
def get_job_posting_repository(session: Session = Depends(get_session)) -> JobPostingRepository:
    return JobPostingRepository(session)