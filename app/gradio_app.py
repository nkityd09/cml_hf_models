import gradio as gr
import os
import requests
import json
import cmlapi


def generate_response(question):
    DOMAIN = os.environ["CDSW_DOMAIN"]
    API_KEY = os.environ["CDSW_APIV2_KEY"]
    PROJECT_ID = os.environ["CDSW_PROJECT_ID"]
    HEADERS = {'Content-Type': 'application/json'}
    API_URL = f'https://modelservice.{DOMAIN}/model'
    WORKSPACE_DOMAIN = f"https://{DOMAIN}"
    CML_CLIENT = cmlapi.default_client(WORKSPACE_DOMAIN, API_KEY)
    models = CML_CLIENT.list_models(PROJECT_ID, search_filter=json.dumps({"name": "LLM_Model"}))
    MODEL_ACCESS_KEY = models.models[0].access_key    
    
    question = {'question': question}
    data = json.dumps({'accessKey': MODEL_ACCESS_KEY, 'request': question})
    response = requests.post(API_URL, data = data, headers = HEADERS)
    try:
        response_json = response.json()
        return response_json.get('response')
    except json.JSONDecodeError:
        return "Failed to parse JSON response"
    
with gr.Blocks() as demo:
    HF_MODEL=os.environ["HF_MODEL"]
    gr.Markdown(f"# {HF_MODEL} CML Model ")
    gr.Markdown(f'Interact with {HF_MODEL} deplyed as a CML Model')
    with gr.Row():
        input = gr.Textbox("Question",label= "Question", show_copy_button=True)
        output = gr.Textbox(label="Answer", show_copy_button=True)
    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=generate_response, inputs=input, outputs=output)

if __name__ == "__main__":
    demo.launch(share=True,
                #enable_queue=True,
                show_error=True,
                server_name='127.0.0.1',
                server_port=int(os.getenv('CDSW_APP_PORT'))) 

    print("Gradio app ready")