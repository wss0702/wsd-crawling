from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session
from app.core.db import get_session
from app.crud.crud import list_job_postings, get_job_posting, create_job_posting
from app.models.JobPosting import JobPosting
from app.models.JobPostingRepository import get_job_posting_repository, JobPostingRepository

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
    repository: JobPostingRepository = Depends(get_job_posting_repository)
):
    filters = {
        "location": location,
        "experience": experience,
        "salary": salary,
        "skills": skills.split(",") if skills else None
    }
    return list_job_postings(repository=repository, skip=skip, limit=limit, sort_by=sort_by, **filters)


@router.get("/jobs/{posting_id}", response_model=JobPosting)
def read_job_posting(posting_id: int, repository: JobPostingRepository = Depends(get_job_posting_repository)):
    posting = get_job_posting(repository=repository, posting_id=posting_id)
    if posting is None:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return posting


@router.delete("/jobs/{posting_id}", response_model=JobPosting)
def delete_job_posting(posting_id: int, repository: JobPostingRepository = Depends(get_job_posting_repository)):
    posting = repository.delete(posting_id)
    if posting is None:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return posting