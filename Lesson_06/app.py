import gradio as gr

from transformers import pipeline

model_name = "deepset/roberta-base-squad2"

nlp = pipeline(
   'question-answering', 
    model=model_name, 
    tokenizer=model_name
)

def generate_answer(question, context):
    QA_Input = {
        'question': question,
        'context': context      
    }

    response = nlp(question=question, context=context)
    result = response['answer']

    return result

iface = gr.Interface(
    fn=generate_answer, 
    
    inputs=[
        gr.Textbox(label="Question:", placeholder="Enter your question here..."),
        gr.Textbox(label="Context:", placeholder="Enter the context here...")
    ],

    outputs=gr.Textbox(label="Answer:"),
    
    title="Question and Answering",
    description="Enter a question and a context and the system will provide an answer."
)

iface.launch(server_name="0.0.0.0", server_port=7860)