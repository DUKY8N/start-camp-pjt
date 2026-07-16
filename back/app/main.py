# areaProject/app/main.py
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.posts import router as posts_router
from app.api.routes.chat import router as chat_router
from app.db.database import init_db
from app.utils.data_loader import PublicDataLoader
import uvicorn

DATA_DIR = BASE_DIR / "data" / "서울"

def create_app() -> FastAPI:
    app = FastAPI(title="LocalHub")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "http://0.0.0.0:5173",
            "https://amazing-cupcake-320e07.netlify.app",
        ],
        allow_origin_regex=r"^http://(localhost|127\.0\.0\.1|0\.0\.0\.0|192\.168\.\d+\.\d+):(?:3000|5173)$",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    async def startup():
        await init_db()

        loader = PublicDataLoader(DATA_DIR)
        try:
            app.state.public_data = loader.load_directory()
        except Exception as exc:
            raise RuntimeError(f"공공데이터 로드 실패: {exc}") from exc

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    app.include_router(posts_router)
    app.include_router(chat_router)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)