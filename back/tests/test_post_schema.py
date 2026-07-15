from datetime import datetime

import pytest

from app.schemas.post import PostResponse


class DummyPost:
    def __init__(self, id, category, title, content, created_at, views):
        self.id = id
        self.category = category
        self.title = title
        self.content = content
        self.created_at = created_at
        self.views = views


def test_created_at_serialization_truncates_seconds():
    src = DummyPost(
        id=1,
        category="general",
        title="테스트 게시글",
        content="본문 내용",
        created_at=datetime(2026, 7, 15, 15, 23, 45),
        views=0,
    )

    resp = PostResponse.model_validate(src)
    dumped = resp.model_dump()
    assert dumped["created_at"] == "2026-07-15 15:23"
    assert dumped["id"] == 1
    assert dumped["title"] == "테스트 게시글"