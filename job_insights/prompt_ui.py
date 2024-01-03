import gradio as gr
from gradio.themes.base import Base

from job_insights.completions import get_answer


def query_data(query):
    return get_answer(question=query, context_length=2)


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
                             label="Answer")
        # output2 = gr.Textbox(lines=1, max_lines=10,
        #                      label="Output generated by chaining Atlas Vector Search to Langchain's RetrieverQA + OpenAI LLM:")
    button.click(query_data, textbox, outputs=[output1])

if __name__ == "__main__":
    demo.launch()