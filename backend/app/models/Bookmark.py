from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class Bookmark(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int  # 사용자 ID
    item_id: int  # 북마크한 항목의 ID로 변경
    created_at: datetime = Field(default_factory=datetime.utcnow)  # 북마크 생성 날짜
