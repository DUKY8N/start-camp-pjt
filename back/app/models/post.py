# areaProject/app/models/post.py
"""
익명 커뮤니티 게시글 모델 (SQLAlchemy 2.0 declarative, async 호환)
주의: 교육 요구사항에 따라 `password`는 평문(plain text)으로 저장합니다. (절대 해시하지 않음)
"""
from datetime import datetime  # 생성일 타입 힌트용
from sqlalchemy import Integer, String, Text, DateTime, func  # 컬럼 타입 및 SQL 함수
from sqlalchemy.orm import Mapped, mapped_column  # SQLAlchemy 2.0 권장형 어노테이션
from app.db.database import Base  # 이전에 만든 declarative Base 가져오기

class Post(Base):
    __tablename__ = "posts"  # DB 테이블 이름 지정

    # 고유 번호(ID) - 기본키, 자동증가 정수
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    # 카테고리 - 문자열(최대 길이 50), 비어있을 수 없음
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="general",  # 기본값을 지정해 둘 수 있음(선택)
    )

    # 제목 - 문자열(최대 200), 비어있을 수 없음
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    # 내용 - 길이 제한 없는 텍스트 필드
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # 작성일 - DB에서 생성 시점으로 기본값 설정 (타임존은 DB/환경에 따라 다름)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),  # 레코드가 생길 때 DB 수준에서 현재 시간 자동 설정
    )

    # 조회수 - 정수, 기본값 0
    views: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    # 수정/삭제용 비밀번호(중요: 평문 저장) - 문자열 필드
    # 보안 규칙상 일반적으로는 절대 이런 방식으로 저장하지 않지만,
    # 교육/요구사항에 의해 평문으로 저장합니다(실서비스 금지).
    password: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    def __repr__(self) -> str:
        # 디버깅 시 보기 좋은 표현 형태
        return f"<Post id={self.id} title={self.title!r} category={self.category!r}>"