import json

import gradio as gr
from gradio.themes.base import Base
from job_insights.embeddings import search_similar_docs
from job_insights.completions import get_openai_response
from job_insights.embeddings import data


def query_data(type,query,prompt, context_length: int = 5):
    data_type = data[type]
    path=data_type["path"]
    raw_path = path.partition("_")[2]
    print(f"path={path}, raw={raw_path}")
    
    similar_docs = search_similar_docs(collection=data_type["collection"], path=path, index_name=data_type["index"], query=query, limit=context_length)
    context_list=[doc.get(raw_path) for doc in similar_docs]
    context_answer = get_openai_response(question=prompt, context_list=context_list)


    return [
        # Contextualized answer:
        context_answer,
        # Non-contextualized answer:
        get_openai_response(question=prompt, context_list=[]),
        json.dumps([{
            "path": item.get(raw_path),
            "score": item.get("score")
        } for item in similar_docs], indent=2)
    ]


with gr.Blocks(theme=Base(), title="Ask Job-Search Related Question") as demo:
    gr.Markdown(
        """
        # Ask Job-Search Related Question
        """)
    type = gr.Dropdown(label="Collections", choices=["jobs", "dog_traits", "dog_health"])
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
    button.click(query_data, inputs=[ type,query, prompt,limit], outputs=[output1, output2, output3])

if __name__ == "__main__":
    demo.launch()
