from fastapi import FastAPI

from job_insights.completions import get_answer

app = FastAPI()


@app.get("/answer")
def answer_question(query: str):
    return {
        "answer": get_answer(query)
    }
