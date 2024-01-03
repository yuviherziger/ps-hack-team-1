import gradio as gr
from gradio.themes.base import Base

from job_insights.completions import get_answer, get_openai_response


def query_data(query):
    return [
        # Contextualized answer:
        get_answer(question=query, context_length=2),
        # Non-contextualized answer:
        get_openai_response(question=query, context_docs=[])
    ]


with gr.Blocks(theme=Base(), title="Ask Job-Search Related Question") as demo:
    gr.Markdown(
        """
        # Ask Job-Search Related Question
        """)
    textbox = gr.Textbox(label="Enter your Question:")
    with gr.Row():
        button = gr.Button("Submit", variant="primary")
    with gr.Column():
        output1 = gr.Textbox(lines=1, max_lines=10,
                             label="Contextualized answer (with Atlas Vector Search):")
        output2 = gr.Textbox(lines=1, max_lines=10,
                             label="Non-contextualized answer (without Atlas Vector Search):")
    button.click(query_data, textbox, outputs=[output1, output2])

if __name__ == "__main__":
    demo.launch()
