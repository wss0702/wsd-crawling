from fastapi import APIRouter

from app.api.routes import login, users, utils
from app.api.jobs import router as jobs_router

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(jobs_router, prefix="/api/v1")