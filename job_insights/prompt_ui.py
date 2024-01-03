import json

import gradio as gr
from gradio.themes.base import Base
from job_insights.embeddings import search_similar_docs
from job_insights.completions import get_openai_response


def query_data(query,prompt, context_length: int = 5):
    similar_docs = search_similar_docs(query=query, limit=context_length)
    context_answer = get_openai_response(question=prompt, context_docs=similar_docs)

    return [
        # Contextualized answer:
        context_answer,
        # Non-contextualized answer:
        get_openai_response(question=prompt, context_docs=[]),
        json.dumps([{
            "summary": item.get("summary"),
            "score": item.get("score")
        } for item in similar_docs], indent=2)
    ]


with gr.Blocks(theme=Base(), title="Ask Job-Search Related Question") as demo:
    gr.Markdown(
        """
        # Ask Job-Search Related Question
        """)
    with gr.Row():    
        query = gr.Textbox(label="Context search:")
        limit = gr.Number(label="Context limit:", value=5)
    prompt = gr.Textbox(label="ChatGPT prompt:")
    with gr.Row():
        button = gr.Button("Submit", variant="primary")
    with gr.Column():
        output1 = gr.Textbox(lines=1, max_lines=10,
                             label="Contextualized answer (with Atlas Vector Search):")
        output2 = gr.Textbox(lines=1, max_lines=10,
                             label="Non-contextualized answer (without Atlas Vector Search):")
        output3 = gr.Code(label="Context used for my first answer", language="json")
    button.click(query_data, inputs=[ query, prompt,limit], outputs=[output1, output2, output3])

if __name__ == "__main__":
    demo.launch()
