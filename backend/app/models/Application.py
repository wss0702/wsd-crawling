from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    job_posting_id: int  # 지원한 채용 공고 ID
    resume: Optional[str] = None  # 이력서 첨부 (파일 경로 등)
    status: str = Field(default="applied")  # 지원 상태 (applied, withdrawn 등)
    created_at: datetime = Field(default_factory=datetime.utcnow)  # 지원 날짜 