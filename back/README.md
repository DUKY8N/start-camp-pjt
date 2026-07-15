
# 데이터베이스 URL을 환경변수에서 읽되, 없으면 로컬 SQLite 파일을 기본값으로 사용합니다.
# (절대 하드코딩된 비밀값을 넣지 마세요)
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "서울"


# LocalHub

LocalHub는 FastAPI, SQLAlchemy, SQLite를 기반으로 한 익명 커뮤니티 + 챗봇 서비스입니다.
이 프로젝트는 다음 기능을 제공합니다.

- 게시판 CRUD 기능
- 익명 게시글 작성/수정/삭제
- 서울 관광지/문화시설/축제 등 공공데이터 기반 챗봇 응답
- Vue 프론트엔드와 API 연동 가능

---

## 1. 프로젝트 개요

이 프로젝트는 백엔드 API 서버로 FastAPI를 사용하며, 프론트엔드에서 다음과 같은 기능을 연동할 수 있습니다.

- 게시글 목록 조회
- 게시글 상세 조회
- 게시글 작성
- 게시글 수정
- 게시글 삭제
- 챗봇 질문 응답

---

## 2. 기술 스택

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0
- SQLite
- Pydantic
- OpenAI API
- python-dotenv

---

## 3. 실행 방법

### 3-1. 가상환경 생성
```bash
python -m venv venv
source venv/bin/activate