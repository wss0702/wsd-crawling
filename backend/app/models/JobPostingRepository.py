# app/repositories/job_posting_repository.py
from sqlmodel import Session, select
from app.models.JobPosting import JobPosting

class JobPostingRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, posting: JobPosting):
        self.session.add(posting)
        self.session.commit()
        self.session.refresh(posting)
        return posting

    def get(self, posting_id: int):
        statement = select(JobPosting).where(JobPosting.postingId == posting_id)
        return self.session.exec(statement).first()

    def update(self, posting: JobPosting):
        self.session.add(posting)
        self.session.commit()
        self.session.refresh(posting)
        return posting

    def delete(self, posting_id: int):
        posting = self.get(posting_id)
        if posting:
            self.session.delete(posting)
            self.session.commit()
            return posting
        return None

    def list(self, skip: int = 0, limit: int = 20, sort_by: str = "postingId", **filters):
        query = select(JobPosting)

        # 필터링
        if "location" in filters:
            query = query.where(JobPosting.location == filters["location"])
        if "experience" in filters:
            query = query.where(JobPosting.experience == filters["experience"])
        if "salary" in filters:
            query = query.where(JobPosting.salary >= filters["salary"])
        if "skills" in filters:
            query = query.where(JobPosting.skills.contains(filters["skills"]))

        # 정렬
        query = query.order_by(getattr(JobPosting, sort_by))

        return self.session.exec(query.offset(skip).limit(limit)).all()