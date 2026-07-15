import os
from datetime import datetime
from pathlib import Path

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_get_delete_post(tmp_path, monkeypatch):
    # 임시 DB 파일을 사용하도록 환경변수 설정 (테스트 격리)
    test_db = tmp_path / "test_dev.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{test_db}")

    # .env 대신 환경변수 우선이므로 create_app을 여기서 생성
    from app.main import create_app
    app = create_app()

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        # 1) 게시글 생성
        payload = {
            "category": "general",
            "title": "integ test",
            "content": "integration test body",
            "password": "pw123",
        }
        res = await client.post("/posts", json=payload)
        assert res.status_code == 201, res.text
        created = res.json()
        assert created["title"] == payload["title"]
        # created_at 포맷 검증 (YYYY-MM-DD HH:MM)
        datetime.strptime(created["created_at"], "%Y-%m-%d %H:%M")

        post_id = created["id"]

        # 2) 게시글 조회
        res2 = await client.get(f"/posts/{post_id}")
        assert res2.status_code == 200, res2.text
        got = res2.json()
        assert got["id"] == post_id
        assert got["title"] == payload["title"]

        # 3) 게시글 삭제 (비밀번호 전달)
        res3 = await client.delete(f"/posts/{post_id}", json={"password": payload["password"]})
        assert res3.status_code == 200, res3.text
        assert res3.json().get("message") is not None

    # tmp_path 기반이므로 테스트 종료 후 파일은 자동 정리됨