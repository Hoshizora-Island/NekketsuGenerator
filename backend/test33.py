import requests
import tokens

API_URL = "https://api-inference.huggingface.co/models/xinsir/controlnet-union-sdxl-1.0"
headers = {"Authorization": f"Bearer {tokens.getToken('HF_TOKEN')}"}

def test_model():
    response = requests.post(API_URL, headers=headers, json={"inputs": "test"})
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.status_code, response.text)

test_model()
