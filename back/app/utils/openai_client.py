# areaProject/app/utils/openai_client.py
import os
import json
from pathlib import Path
from typing import Any
from urllib import response

import httpx
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5-mini"

def _build_public_data_summary(public_data: dict[str, Any], max_items_per_file: int = 2) -> str:
    summary_lines: list[str] = []

    for file_name, data in public_data.items():
        region = data.get("region", "")
        content_type = data.get("contentType", "")
        total = data.get("total", "")
        summary_lines.append(f"파일: {file_name}, 지역: {region}, 타입: {content_type}, 총개수: {total}")

        items = data.get("items", [])
        for item in items[:max_items_per_file]:
            title = item.get("title", "")
            addr1 = item.get("addr1", "")
            tel = item.get("tel", "")
            summary_lines.append(
                f"  - title: {title}, addr1: {addr1}, tel: {tel}, mapx: {item.get('mapx','')}, mapy: {item.get('mapy','')}"
            )
        summary_lines.append("")

    return "\n".join(summary_lines)

async def chat_with_public_data(question: str, public_data: dict[str, Any]) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY가 설정되어 있지 않습니다.")

    data_summary = _build_public_data_summary(public_data, max_items_per_file=2)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Use only the given Seoul public data summary to answer the user's question. "
                "If the user asks for information not in the data, say you cannot answer from the data."
            ),
        },
        {
            "role": "user",
            "content": (
                "Here is the Seoul public dataset summary:\n"
                f"{data_summary}\n\n"
                f"User question: {question}"
            ),
        },
    ]

    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "max_completion_tokens": 500
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(OPENAI_URL, json=payload, headers=headers)
        print("OpenAI 상태 코드:", response.status_code)

        if not response.is_success:
            print("OpenAI 오류 응답:", response.text)
        response.raise_for_status()
        result = response.json()

    return result["choices"][0]["message"]["content"].strip()