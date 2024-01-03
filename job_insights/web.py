from typing import Union

from fastapi import FastAPI

from job_insights.completions import get_answer

app = FastAPI()


@app.get("/answer")
def answer_question(similar: str, prompt: str, context_length: Union[int, None] = 5):
    return get_answer(similar=similar, prompt=prompt, context_length=context_length)
