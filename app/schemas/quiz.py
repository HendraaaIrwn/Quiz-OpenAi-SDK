from pydantic import BaseModel
from typing import List, Literal

Difficulty = Literal["easy", "medium", "hard"]

class Choice(BaseModel):
    label: Literal["A", "B", "C", "D"]
    text: str

class Question(BaseModel):
    number: int
    question: str
    choices: List[Choice]
    answer: Literal["A", "B", "C", "D"]
    explanation: str


class Quiz(BaseModel):
    topic: str
    difficulty: Difficulty
    total_questions: int
    questions: List[Question]
