import gradio as gr

from transformers import AutoModelForQuestionAnswering, AutoTokenizer

model_name = "bert-large-uncased-whole-word-masking-finetuned-squad"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

def generate_answer(question, context):
    QA_Input = {
        'question': question,
        'context': context      
    }
   
    inputs = tokenizer(question, context, return_tensors="pt")

    outputs = model(**inputs)

    # extract the start and end scores
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # get the most likely start and end positions
    start_index = start_scores.argmax()
    end_index = end_scores.argmax()

    # convert token IDs back to words
    answer_tokens = inputs["input_ids"][0][start_index : end_index + 1]
    answer = tokenizer.decode(answer_tokens, skip_special_tokens = True)

    return answer

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