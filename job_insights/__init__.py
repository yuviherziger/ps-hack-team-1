from job_insights.completions import get_answer
from job_insights.embeddings import get_transformer_embeddings, search_similar_docs

if __name__ == "__main__":
    question = "What are the most common skills for a Java software engineer?"
    print(get_answer(question))
