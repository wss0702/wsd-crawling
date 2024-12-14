from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.core.db import get_session
from app.models.Application import Application
from app.models.models import User  # User 모델 가져오기
from app.models.ApplicationRepository import get_application_repository, ApplicationRepository  # ApplicationRepository 가져오기
import uuid
import hashlib
from uuid import UUID
from datetime import datetime

router = APIRouter()

@router.post("/applications", response_model=Application)
def apply_for_job(
    user: User,  # User 모델을 통해 사용자 정보를 받음
    job_posting_id: int,
    resume: Optional[str] = None,
    session: Session = Depends(get_session),
    application_repository: ApplicationRepository = Depends(get_application_repository)  # ApplicationRepository 의존성 주입
):
    # user.id를 UUID로 변환
    user_id_uuid = UUID(user.id)  # user.id가 문자열로 되어 있을 경우 UUID로 변환
    user_id = uuid_to_int(user_id_uuid)  # UUID를 int형으로 변환

    application = Application(user_id=user_id, job_posting_id=job_posting_id, resume=resume)
    try:
        return application_repository.create(application)  # ApplicationRepository를 통해 애플리케이션 생성
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def uuid_to_int(user_uuid: UUID) -> int:
    # UUID를 해시하여 고유한 정수 생성
    hash_object = hashlib.md5(user_uuid.bytes)
    return int.from_bytes(hash_object.digest()[:4], byteorder='big')  # 앞의 4바이트를 사용하여 정수로 변환


@router.delete("/applications/{application_id}", response_model=Application)
def withdraw_application(
    application_id: int, 
    user: User, 
    session: Session = Depends(get_session),
    application_repository: ApplicationRepository = Depends(get_application_repository)  # ApplicationRepository 의존성 주입
):
    application = application_repository.delete(application_id)  # ApplicationRepository를 통해 애플리케이션 삭제
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application 


@router.get("/applications", response_model=list[Application])
def get_applications(
    user: User,  # 현재 사용자 정보
    status: Optional[str] = None,  # 상태 필터링 (선택 사항)
    session: Session = Depends(get_session),  # 데이터베이스 세션
    application_repository: ApplicationRepository = Depends(get_application_repository)  # 의존성 주입
):
    """
    사용자 지원 내역 조회 API
    - 사용자 ID로 지원 내역을 필터링
    - 상태(status) 필터링은 선택 사항
    """
    # `user` 객체에서 UUID를 int로 변환
    user_id_uuid = UUID(user.id)
    user_id = uuid_to_int(user_id_uuid)

    try:
        # ApplicationRepository를 사용하여 지원 내역 조회
        applications = application_repository.list(user_id=user_id, status=status)
        return applications
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def uuid_to_int(user_uuid: UUID) -> int:
    # UUID를 해시하여 고유한 정수 생성
    hash_object = hashlib.md5(user_uuid.bytes)
    return int.from_bytes(hash_object.digest()[:4], byteorder='big')  # 앞의 4바이트를 사용하여 정수로 변환


