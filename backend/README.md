# FastAPI 프로젝트 - 백엔드

## 요구 사항

- [Docker](https://www.docker.com/)
- [Poetry](https://python-poetry.org/) (파이썬 패키지 및 환경 관리 도구)
- [uv](https://docs.astral.sh/uv/) (파이썬 패키지 및 환경 관리 도구)

## 설치 및 설정

1. **Poetry 설치**

   Poetry가 설치되어 있지 않다면, 다음 명령어를 통해 설치할 수 있습니다:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **의존성 설치**

   프로젝트의 `backend` 디렉토리로 이동한 후, 다음 명령어를 실행하여 의존성을 설치합니다:

   ```bash
   cd backend
   poetry install
   ```

3. **환경 변수 설정**

   `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다. 예를 들어:

   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
   SECRET_KEY=your_secret_key
   ```

## 빌드 및 실행

### Docker를 사용한 빌드 및 실행

1. **Docker 이미지 빌드**

   `backend` 디렉토리에서 다음 명령어를 실행하여 Docker 이미지를 빌드합니다:

   ```bash
   docker build -t fastapi-backend .
   ```

2. **Docker 컨테이너 실행**

   빌드된 이미지를 기반으로 컨테이너를 실행합니다:

   ```bash
   docker run -d -p 443:443 --name fastapi-backend-container fastapi-backend
   ```

3. **Docker Compose를 사용한 개발 환경 실행**

   개발 환경에서는 `docker-compose`를 사용하는 것이 편리합니다. `docker-compose.yml` 파일을 생성하고 다음과 같이 설정합니다:

   ```yaml
   version: '3.8'

   services:
     backend:
       build:
         context: .
         dockerfile: Dockerfile
       ports:
         - "443:443"
       volumes:
         - .:/app
       environment:
         - DATABASE_URL=${DATABASE_URL}
         - SECRET_KEY=${SECRET_KEY}
   ```

   그런 다음, 다음 명령어로 개발 환경을 시작합니다:

   ```bash
   docker-compose up --build
   ```

## 마이그레이션

데이터베이스 스키마 변경을 관리하기 위해 Alembic을 사용합니다.

1. **마이그레이션 적용**

   ```bash
   alembic upgrade head
   ```

2. **새로운 마이그레이션 생성**

   모델 변경 사항을 기반으로 새로운 마이그레이션 파일을 생성합니다:

   ```bash
   alembic revision --autogenerate -m "설명"
   ```

## 기타 명령어

- **컨테이너에 접속**

  ```bash
  docker compose exec backend bash
  ```

- **라이브 리로드 서버 실행**

  ```bash
  fastapi run --reload app/main.py
  ```
  
## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](./LICENSE)를 참조하세요.