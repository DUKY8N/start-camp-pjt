# areaProject/app/api/routes/chat.py
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from app.utils.openai_client import chat_with_public_data

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    question: str = Field(..., description="사용자가 질문한 내용")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="OpenAI가 생성한 답변")


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def post_chat(
    request: Request,
    body: ChatRequest,
) -> ChatResponse:
    """
    사용자 질문과 서울 공공데이터를 결합해 OpenAI에 전달하는 비동기 엔드포인트
    """
    public_data = getattr(request.app.state, "public_data", None)
    if public_data is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서울 공공데이터가 로드되지 않았습니다."
        )

    try:
        answer = await chat_with_public_data(body.question, public_data)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OpenAI 응답 처리 중 오류가 발생했습니다: {exc}"
        ) from exc

    return ChatResponse(answer=answer)