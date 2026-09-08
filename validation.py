from fastapi import HTTPException
from app.config import settings


def validate_question(question: str) -> str:
    cleaned = question.strip()

    if not cleaned:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    if len(cleaned) > settings.max_question_length:
        raise HTTPException(
            status_code=400,
            detail=f"Question exceeds {settings.max_question_length} characters.",
        )

    return cleaned
