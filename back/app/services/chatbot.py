"""
챗봇 서비스: OpenAI Chat Completions를 httpx Async로 호출하는 간단 래퍼.
환경변수: OPENAI_API_KEY (절대 하드코딩 금지)
"""
import os
from typing import List, Dict

import httpx

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-3.5-turbo"

async def chat_with_openai(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL) -> str:
    """
    messages: [{"role": "system|user|assistant", "content": "..."} , ...]
    반환값: 모델의 텍스트 응답(문자열)
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7,
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(OPENAI_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]