import gradio as gr
import os
import requests
import json
import cmlapi


def generate_response(question):
    DOMAIN = os.environ["CDSW_DOMAIN"]
    API_KEY = os.environ["CDSW_APIV2_KEY"]
    PROJECT_ID = os.environ["CDSW_PROJECT_ID"]
    
    API_URL = f'https://modelservice.{DOMAIN}/model'
    WORKSPACE_DOMAIN = f"https://{DOMAIN}"
    CML_CLIENT = cmlapi.default_client(WORKSPACE_DOMAIN, API_KEY)
    models = CML_CLIENT.list_models(PROJECT_ID, search_filter=json.dumps({"name": "LLM_Model"}))
    MODEL_ACCESS_KEY = models.models[0].access_key    
    HEADERS = {'Content-Type': 'application/json'}
    question = {'question': question}
    data = json.dumps({'accessKey': MODEL_ACCESS_KEY, 'request': question})
    response = requests.post(API_URL, data = data, headers = HEADERS)
    try:
        response_json = response.json()
        print(response_json.get('response'))
        return response_json.get('response')
    except json.JSONDecodeError:
        return "Failed to parse JSON response"
    
with gr.Blocks() as demo:
    gr.Markdown("# CML LLM Models ")
    with gr.Row():
        input = gr.Textbox("Question")
        output = gr.Textbox()
    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=generate_response, inputs=input, outputs=output)

if __name__ == "__main__":
    demo.launch(share=True,
                #enable_queue=True,
                show_error=True,
                server_name='127.0.0.1',
                server_port=int(os.getenv('CDSW_APP_PORT'))) 

    print("Gradio app ready")