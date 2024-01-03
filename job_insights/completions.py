from typing import Dict, List

from openai import OpenAI
from openai.types.chat import ChatCompletion

from job_insights.embeddings import search_similar_docs

openai_client = OpenAI()


def get_openai_response(question: str, context_docs: List[Dict]) -> str:
    context_messages = [{
        "role": "user",
        "content": "For context, here is a job posting summary: " + doc.get("summary"),
    } for doc in context_docs]
    response: ChatCompletion = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            *context_messages,
            {"role": "user", "content": question},
        ],
        temperature=0.8
    )
    return response.choices[0].message.content


def get_answer(question: str, context_length: int = 5) -> (str, List[Dict]):
    similar_docs = search_similar_docs(query=question, limit=context_length)
    return get_openai_response(question, similar_docs), similar_docs
