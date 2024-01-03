import json

import gradio as gr
from gradio.themes.base import Base

from job_insights.completions import get_answer, get_openai_response


def query_data(query):
    context_answer, context = get_answer(question=query, context_length=5)
    return [
        # Contextualized answer:
        context_answer,
        # Non-contextualized answer:
        get_openai_response(question=query, context_docs=[]),
        json.dumps([{
            "summary": item.get("summary"),
            "score": item.get("score")
        } for item in context], indent=2)
    ]


with gr.Blocks(theme=Base(), title="Ask Job-Search Related Question") as demo:
    gr.Markdown(
        """
        # Ask Job-Search Related Question
        """)
    textbox = gr.Textbox(label="Enter a question:")
    with gr.Row():
        button = gr.Button("Submit", variant="primary")
    with gr.Column():
        output1 = gr.Textbox(lines=1, max_lines=10,
                             label="Contextualized answer (with Atlas Vector Search):")
        output2 = gr.Textbox(lines=1, max_lines=10,
                             label="Non-contextualized answer (without Atlas Vector Search):")
        output3 = gr.Code(label="Context used for my first answer", language="json")
    button.click(query_data, textbox, outputs=[output1, output2, output3])

if __name__ == "__main__":
    demo.launch()
