from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.db import get_session
from app.models.Bookmark import Bookmark
from app.models.BookmarkRepository import get_bookmark_repository, BookmarkRepository  # BookmarkRepository 가져오기
from app.models.models import User  # User 모델 가져오기
from typing import List
from uuid import UUID
import hashlib

router = APIRouter()

def uuid_to_int(user_uuid: UUID) -> int:
    # UUID를 해시하여 고유한 정수 생성
    hash_object = hashlib.md5(user_uuid.bytes)
    return int.from_bytes(hash_object.digest()[:4], byteorder='big')  # 앞의 4바이트를 사용하여 정수로 변환

@router.post("/bookmarks", response_model=Bookmark)
def toggle_bookmark(
    job_posting_id: int,
    user: User,
    session: Session = Depends(get_session),
    bookmark_repository: BookmarkRepository = Depends(get_bookmark_repository)  # BookmarkRepository 의존성 주입
):
    # user.id를 UUID로 변환
    user_id_uuid = UUID(user.id)  # user.id가 문자열로 되어 있을 경우 UUID로 변환
    user_id = uuid_to_int(user_id_uuid)  # UUID를 int형으로 변환

    bookmark = bookmark_repository.get(user_id, job_posting_id)  # 사용자의 북마크 조회
    
    if bookmark:
        bookmark_repository.remove(bookmark)  # 북마크가 존재하면 삭제
        return bookmark  # 삭제된 북마크 반환
    else:
        new_bookmark = Bookmark(user_id=user_id, item_id=job_posting_id)  # 북마크 생성 시 user_id 사용
        return bookmark_repository.add(new_bookmark)  # 북마크가 없으면 추가하고 반환

@router.get("/bookmarks", response_model=List[Bookmark])
def list_bookmarks(
    user: User,
    page: int = 1,
    page_size: int = 10,
    bookmark_repository: BookmarkRepository = Depends(get_bookmark_repository)  # BookmarkRepository 의존성 주입
):
    # user.id를 UUID로 변환
    user_id_uuid = UUID(user.id)  # user.id가 문자열로 되어 있을 경우 UUID로 변환
    user_id = uuid_to_int(user_id_uuid)  # UUID를 int형으로 변환

    bookmarks = bookmark_repository.list(user_id, page, page_size)  # 사용자별 북마크 목록 조회
    return bookmarks  # 요청된 페이지의 북마크 반환
