from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ApplicationBase(SQLModel):
    job_posting_id: int
    resume: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    status: str = Field(default="applied")  # 지원 상태
    created_at: datetime = Field(default_factory=datetime.utcnow)  # 지원 날짜