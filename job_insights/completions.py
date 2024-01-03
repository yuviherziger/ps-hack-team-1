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
        ]
    )
    return response.choices[0].message.content


def get_answer(similar: str,prompt:str, context_length: int = 5) -> str:
    similar_docs = search_similar_docs(query=similar, limit=context_length)
    return {
        "jobs": [{"title": doc.get("jobtitle")} for doc in similar_docs],
        "openai": get_openai_response(prompt, similar_docs)
    }
