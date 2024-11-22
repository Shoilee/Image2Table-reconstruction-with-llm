import requests
import base64
import io

from LLM_key import gpt_apikey, gpt_url, gemini_url, gemini_apikey
from PIL import Image


def call_LLM(mes, model_name, temperature=0):
    if model_name == "gpt-4o":
        url = gpt_url
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {gpt_apikey}'
        }
    elif model_name == "gemini-1.5-pro":
        url = gemini_url
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {gemini_apikey}'
        }
    else:
        raise "model_name error!"
    data = {
        'model': model_name,
        'temperature': temperature,
        'messages': [
            {
                "role": "user",
                "content": mes
            }
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        resp = response.json()
        result = resp['choices'][0]['message']['content']
        return result
    else:
        raise Exception(f"{response.status_code} error!")