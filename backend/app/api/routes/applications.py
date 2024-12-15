from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.core.db import get_session
from app.models.Application import Application
from app.models.models import User  # User 모델 가져오기
from app.models.ApplicationRepository import get_application_repository, ApplicationRepository
import hashlib
from uuid import UUID
from datetime import datetime
from app.api.deps import get_current_user  # 현재 사용자 의존성 주입 함수

router = APIRouter()

def uuid_to_int(user_uuid: UUID) -> int:
    # UUID를 해시하여 고유한 정수 생성
    hash_object = hashlib.md5(user_uuid.bytes)
    return int.from_bytes(hash_object.digest()[:4], byteorder='big')  # 앞의 4바이트를 사용하여 정수로 변환

@router.post("/applications", response_model=Application)
def apply_for_job(
    user: User,  # User 모델을 통해 사용자 정보를 받음
    job_posting_id: int,
    resume: Optional[str] = None,
    session: Session = Depends(get_session),
    application_repository: ApplicationRepository = Depends(get_application_repository)  # ApplicationRepository 의존성 주입
):
    # user.id를 UUID로 변환 (문자열인 경우 변환)
    try:
        user_id_uuid = UUID(user.id)  # 문자열을 UUID 객체로 변환
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 사용자 ID입니다.")

    user_id = uuid_to_int(user_id_uuid)  # UUID를 int형으로 변환

    application = Application(user_id=user_id, job_posting_id=job_posting_id, resume=resume)
    try:
        return application_repository.create(application)  # ApplicationRepository를 통해 애플리케이션 생성
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

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
    status: Optional[str] = Query(None),
    job_posting_id: Optional[int] = Query(None),
    user: User = Depends(get_current_user),  # 의존성 주입으로 현재 사용자 받기
    session: Session = Depends(get_session),
    application_repository: ApplicationRepository = Depends(get_application_repository)
):
    """
    사용자 지원 내역 조회 API
    """
    # user.id가 이미 UUID인 경우 변환하지 않음
    try:
        if isinstance(user.id, UUID):
            user_id_uuid = user.id  # 이미 UUID 객체인 경우
        else:
            user_id_uuid = UUID(user.id)  # 문자열을 UUID 객체로 변환
    except ValueError:
        raise HTTPException(status_code=400, detail="유효하지 않은 사용자 ID입니다.")

    user_id = uuid_to_int(user_id_uuid)  # UUID를 int형으로 변환

    try:
        applications = application_repository.list(user_id=user_id, status=status, job_posting_id=job_posting_id)
        return applications
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="서버 내부 오류가 발생했습니다.")
