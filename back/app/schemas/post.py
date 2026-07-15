from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator, field_serializer


class PostCreate(BaseModel):
    """
    게시글 생성 요청 body
    프론트엔드에서 POST /posts로 보낼 데이터입니다.
    """
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    category: str = Field(
        default="general",
        description="게시글 카테고리. 기본값은 'general'입니다.",
    )
    title: str = Field(
        ...,
        min_length=1,
        description="게시글 제목. 비어 있으면 안 됩니다.",
    )
    content: str = Field(
        ...,
        min_length=1,
        description="게시글 본문. 비어 있으면 안 됩니다.",
    )
    password: str = Field(
        ...,
        min_length=1,
        description="게시글 수정/삭제용 비밀번호. 교육용 프로젝트라 평문으로 저장됩니다.",
    )


class PostUpdate(BaseModel):
    """
    게시글 수정 요청 body
    수정하고 싶은 필드만 보내면 됩니다.
    password는 필수입니다.
    """
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    category: str | None = Field(
        default=None,
        description="수정할 카테고리",
    )
    title: str | None = Field(
        default=None,
        description="수정할 제목",
    )
    content: str | None = Field(
        default=None,
        description="수정할 본문",
    )
    password: str = Field(
        ...,
        min_length=1,
        description="게시글 수정 권한 확인용 비밀번호",
    )

    @model_validator(mode="after")
    def validate_has_any_update(self) -> "PostUpdate":
        """
        최소 한 개 이상의 수정 필드가 있어야 합니다.
        """
        if self.category is None and self.title is None and self.content is None:
            raise ValueError("수정할 값이 하나 이상 필요합니다.")
        return self


class PostDelete(BaseModel):
    """
    게시글 삭제 요청 body
    """
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    password: str = Field(
        ...,
        min_length=1,
        description="게시글 삭제 권한 확인용 비밀번호",
    )


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="게시글 고유 번호")
    category: str = Field(..., description="게시글 카테고리")
    title: str = Field(..., description="게시글 제목")
    content: str = Field(..., description="게시글 본문")
    created_at: datetime = Field(..., description="게시글 작성일시")
    views: int = Field(..., description="게시글 조회수")

    @field_serializer("created_at")
    def _ser_created_at(self, v: datetime, _info):
        return v.strftime("%Y-%m-%d %H:%M")