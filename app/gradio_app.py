import gradio as gr
import os
import requests

DOMAIN = os.environ["CDSW_DOMAIN"]
API_URL = f'https://modelservice.{DOMAIN}/model'
ACCESS_KEY = os.environ["CDSW_API_KEY"]
HEADERS = {'Content-Type': 'application/json'}

def generate_response(api_url, cml_access_key, headers, question):
    api_url = api_url
    cml_access_key = cml_access_key
    question = {'question': question}
    data = json.dumps({'accessKey': cml_access_key, 'request': question})
    headers = headers
    response = requests.post(api_url, data = data, headers = {'Content-Type': 'application/json'})
    try:
        response_json = response.json()
        return response_json.get('response')
    except json.JSONDecodeError:
        return "Failed to parse JSON response"
    
with gr.Blocks() as demo:
    gr.Markdown("# CML LLM Models ")
    with gr.Row():
        input = gr.Textbox("Question")
        output = gr.Textbox()
    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=generate_response, inputs=[API_URL, ACCESS_KEY, HEADERS, input], output)

if __name__ == "__main__":
    demo.launch(share=True,
                enable_queue=True,
                show_error=True,
                server_name='127.0.0.1',
                server_port=int(os.getenv('CDSW_APP_PORT'))) 

    print("Gradio app ready")