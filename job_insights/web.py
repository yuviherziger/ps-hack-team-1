from typing import Union

from fastapi import FastAPI

from job_insights.completions import get_answer

app = FastAPI()


@app.get("/answer")
def answer_question(query: str, context_length: Union[int, None] = 5):
    return {
        # "answer": get_answer(question=query, context_length=context_length)
    }
