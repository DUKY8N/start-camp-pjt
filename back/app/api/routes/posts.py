import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy import delete, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.models.post import Post
from app.schemas.post import PostCreate, PostResponse

router = APIRouter(prefix="/posts", tags=["posts"])


class PostUpdate(BaseModel):
    """
    게시글 수정 요청 바디 모델
    - 수정하고 싶은 필드만 보내면 됩니다.
    - 비밀번호는 필수입니다.
    """
    category: str | None = Field(None, description="수정할 카테고리")
    title: str | None = Field(None, description="수정할 제목")
    content: str | None = Field(None, description="수정할 본문")
    password: str = Field(..., description="수정용 비밀번호")


class PostDelete(BaseModel):
    """
    게시글 삭제 요청 바디 모델
    - 비밀번호가 맞아야 삭제할 수 있습니다.
    """
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    password: str = Field(..., min_length=1, description="삭제용 비밀번호")


async def _parse_json_body(request: Request) -> dict[str, Any]:
    raw_body = await request.body()

    if not raw_body:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="요청 본문이 비어 있습니다.",
        )

    text = None
    for encoding in ("utf-8", "utf-8-sig", "cp949", "cp1252"):
        try:
            text = raw_body.decode(encoding)
            break
        except UnicodeDecodeError:
            continue

    if text is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="본문 인코딩을 해석할 수 없습니다.",
        )

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JSON 형식이 올바르지 않습니다.",
        ) from exc

    if not isinstance(payload, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="JSON 본문은 객체 형태여야 합니다.",
        )

    return payload


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    request: Request,
    db: AsyncSession = Depends(get_session),
) -> Post:
    payload = await _parse_json_body(request)

    try:
        post_in = PostCreate(**payload)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.errors(),
        ) from exc

    new_post = Post(
        category=post_in.category,
        title=post_in.title,
        content=post_in.content,
        password=post_in.password,
    )

    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


@router.get("", response_model=list[PostResponse])
async def list_posts(
    keyword: str | None = None,
    db: AsyncSession = Depends(get_session),
) -> list[Post]:
    query = select(Post).order_by(Post.created_at.desc())

    if keyword:
        lower_keyword = f"%{keyword.lower()}%"
        query = query.where(
            or_(
                func.lower(Post.title).like(lower_keyword),
                func.lower(Post.content).like(lower_keyword),
            )
        )

    result = await db.execute(query)
    posts = result.scalars().all()
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_session),
) -> Post:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    post.views += 1
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    db: AsyncSession = Depends(get_session),
) -> Post:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    if (post.password or "").strip() != (post_in.password or "").strip():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비밀번호가 일치하지 않습니다.",
        )

    if post_in.category is not None:
        post.category = post_in.category
    if post_in.title is not None:
        post.title = post_in.title
    if post_in.content is not None:
        post.content = post_in.content

    db.add(post)
    await db.commit()
    await db.refresh(post)

    return post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    request: Request,
    db: AsyncSession = Depends(get_session),
) -> dict:
    payload = await _parse_json_body(request)

    try:
        body = PostDelete(**payload)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.errors(),
        ) from exc

    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다.",
        )

    stored_password = (post.password or "").strip()
    input_password = (body.password or "").strip()

    if stored_password != input_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="비밀번호가 일치하지 않습니다.",
        )

    await db.execute(delete(Post).where(Post.id == post_id))
    await db.commit()

    return {"message": "게시글이 삭제되었습니다."}