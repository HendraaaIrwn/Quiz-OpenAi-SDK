from fastapi import FastAPI
from app.modules.quiz.router import router as quiz_router

app = FastAPI()
app.include_router(quiz_router)
