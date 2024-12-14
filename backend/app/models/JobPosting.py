from typing import List, Optional  # List와 Optional을 import합니다.
from sqlmodel import Field, SQLModel
from sqlalchemy import ARRAY, String

class JobPosting(SQLModel, table=True):
    postingId: int = Field(primary_key=True)
    postingContent: str
    location: str  # 지역
    experience: str  # 경력
    salary: float  # 급여
    skills: str #기술 크롤링하면 그냥 한줄로줘
    views: int = Field(default=0)  # 조회수