from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.core.db import get_session
from app.crud.crud import list_job_postings, get_job_posting
from app.models.JobPosting import JobPosting

router = APIRouter()

@router.get("/jobs", response_model=list[JobPosting])
def read_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    sort_by: str = Query("postingId"),
    location: str = None,
    experience: str = None,
    salary: float = None,
    skills: str = None,
    session: Session = Depends(get_session)
):
    filters = {
        "location": location,
        "experience": experience,
        "salary": salary,
        "skills": skills.split(",") if skills else None
    }
    return list_job_postings(session=session, skip=skip, limit=limit, sort_by=sort_by, **filters)

@router.get("/jobs/{posting_id}", response_model=JobPosting)
def read_job(posting_id: int, session: Session = Depends(get_session)):
    job_posting = get_job_posting(session=session, posting_id=posting_id)
    if job_posting:
        job_posting.views += 1  # 조회수 증가
        session.add(job_posting)
        session.commit()
        session.refresh(job_posting)
        return job_posting
    return {"message": "Job posting not found"} 