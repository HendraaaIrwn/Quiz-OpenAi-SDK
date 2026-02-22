from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path
from typing import Annotated, Literal
from app.utils.openai_client import get_client
from app.prompts.quiz_prompt import SYSTEM_PROMPT
from app.schemas.quiz import Quiz


router = APIRouter(prefix="/quiz", tags=["quiz"])
PROJECT_ROOT = Path(__file__).resolve().parents[3]
templates = Jinja2Templates(directory=str(PROJECT_ROOT / "templates"))

@router.get("/")
def quiz_form(request: Request):
    return templates.TemplateResponse("quiz_form.html", {"request": request})

@router.post("/")
def generate_quiz(
    request: Request,
    topic: str = Form(...),
    difficulty: Annotated[Literal["easy", "medium", "hard"], Form()] = "medium",
    total_questions: Annotated[int, Form(ge=1, le=30)] = 5,
    context: str = Form(""),
):
    client = get_client()
    context = context.strip()
    user_prompt = f"""
Topic: {topic}
Difficulty: {difficulty}
Total Questions: {total_questions}
"""
    if context:
        user_prompt += f"\nAdditional Context:\n{context}\n"
    else:
        user_prompt += "\nAdditional Context:\n(none)\n"

    result = client.beta.chat.completions.parse(
        model = os.getenv("OPENAI_MODEL", "gpt-5-mini-2025-08-07"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format=Quiz,
    )

    quiz_obj = result.choices[0].message.parsed
    return templates.TemplateResponse("quiz_result.html", {"request": request, "quiz": quiz_obj})
