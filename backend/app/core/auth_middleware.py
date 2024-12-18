from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_access_token  # 토큰 검증 함수
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Depends
import logging  # 로깅 모듈 추가

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
async def get_token_header(token: str = Depends(oauth2_scheme)):
    return token

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 스웨거 문서 및 회원가입, 로그인 경로를 제외합니다.
        excluded_paths = [
            "/api/v1/openapi.json",
            "/docs",
            "/register",
            "/auth/login",
            "/auth/login/login/access-token",
            "/auth/login/login/test-token",
            "/users/signup",
            "/auth/users/signup"
        ]
        
        if request.url.path in excluded_paths:
            response = await call_next(request)
            return response

        token = request.headers.get("Authorization")
        logger.info(f"Request token {token}")
        logger.info(f"Request headers: {request.headers}")
        if token is None or not token.lower().startswith("bearer "):
            logger.warning("토큰이 없습니다.")  # 토큰 없음 로깅
            raise HTTPException(status_code=401, detail="Not authenticated")

        token = token.split(" ")[1]  # "Bearer " 부분 제거

        try:
            # 토큰 검증 함수 호출
            payload = verify_access_token(token)
        except Exception as e:
            if "expired" in str(e):  # 유효기간 만료 체크
                logger.warning("토큰이 만료되었습니다.")  # 만료된 토큰 로깅
            else:
                logger.warning("유효하지 않은 토큰입니다.")  # 유효하지 않은 토큰 로깅
            raise HTTPException(status_code=403, detail="Invalid token")

        # 요청에 사용자 정보를 추가할 수 있습니다.
        request.state.user = payload

        logger.info(f"Received Authorization header: {request.headers.get('Authorization')}")

        response = await call_next(request)
        return response
