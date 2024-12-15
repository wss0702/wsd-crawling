import sentry_sdk
from fastapi import FastAPI, Depends
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from sqlmodel import Session
from starlette.middleware import Middleware

from app.api.main import api_router
from app.core.config import settings
from app.core.db import init_db, engine
from app.core.auth_middleware import AuthMiddleware
from app.utils.crawl_saramin import crawl_saramin
from app.models.JobPostingRepository import get_job_posting_repository
from app.api.routes import applications  # 추가된 라우터 임포트


def custom_generate_unique_id(route: APIRoute) -> str:
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    return f"untagged-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

#app.add_middleware(AuthMiddleware)

@app.on_event("startup")
def on_startup():
    with Session(engine) as session:
        init_db(session)
        repository = get_job_posting_repository(session)  # 레포지토리 인스턴스 생성
        crawl_saramin(keyword="개발자", pages=1, repository=repository)  # 레포지토리 전달

app.include_router(api_router)