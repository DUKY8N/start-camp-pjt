
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
```

### 3-2. 의존성 설치
```
pip install -r requirements.txt
```


### 3-3. 환경 변수 파일
프로젝트 루트(back)에 .env 파일을 만들고 필요한 값을 설정하세요

예시 .env 내용:

```
# 로컬 SQLite 기본값 (필요시 변경)
DATABASE_URL=sqlite+aiosqlite:///./dev.db

# OpenAI 사용 시 필요 (없으면 챗봇 호출 실패)
OPENAI_API_KEY=sk-...
```


### 3-4. 앱 실행
프로젝트 루트(back)에서 uvicorn으로 실행합니다:
```
python -m uvicorn app.main:app --reload
```

헬스체크: GET http://127.0.0.1:8000/health → 응답 예:

```
{"status":"ok"}
```

### 주요 엔드포인트 예시

POST /posts — 게시글 생성
요청 예:

```
{
  "category": "general",
  "title": "테스트 게시글",
  "content": "본문 내용",
  "password": "비밀번호"
}

```

응답 예 (201):

```
{
  "id": 1,
  "category": "general",
  "title": "테스트 게시글",
  "content": "본문 내용",
  "created_at": "2026-07-15T12:00:00Z",
  "views": 0
}

```

- GET /posts — 게시글 목록
- GET /posts/{id} — 게시글 상세
- PUT /posts/{id} — 게시글 수정 (비밀번호 필요)
- DELETE /posts/{id} — 게시글 삭제 (비밀번호 필요)
- POST /api/chat — 챗봇 질의 (body: {"question":"질문"})
응답 예:
```
{"answer":"데이터에 기반한 답변 예시"}
```

###자주 발생하는 문제와 해결

- ModuleNotFoundError: No module named 'dotenv' 등 패키지 관련 오류:

```
# 가상환경 활성화 후
pip install -r requirements.txt
# 또는
python -m pip install python-dotenv
```

- ModuleNotFoundError: No module named 'app':
 현재 작업 디렉터리가 back인지 확인하고 실행하세요.
- OpenAI 관련 오류:
 env에 OPENAI_API_KEY가 정확히 설정되어 있는지 확인하세요.
- DB 연결 문제:
.env의 DATABASE_URL 경로를 확인하세요. 기본값은 sqlite+aiosqlite:///./dev.db 입니다.

### 개발/유지관리 팁

- DB 엔진 및 세션 구현은 database.py를 단일 소스로 관리하세요. (중복 파일인 session.py가 있으면 정리 권장)
- 공공데이터(JSON)는 서울에 넣어두면 챗봇에서 사용됩니다.
- 배포 시 .env 및 민감키는 CI/CD 비밀로 관리하세요.

### 참고 파일

- 엔트리포인트: main.py:1-40
- DB 설정: database.py:1-80
- 게시판 라우트: posts.py:1-20
- 챗봇 라우트: chat.py:1-40