import requests
import io
from PIL import Image
import tokens

# Hugging FaceのAPI URLと認証トークン
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

headers = {"Authorization": f"Bearer {tokens.getToken('HF_TOKEN')}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    return response.content


# テキストプロンプトの設定
prompt = "頑張るぞ！"

# 画像生成
image_bytes = query({
    "inputs": prompt,
})

# 画像の読み込みと保存
image = Image.open(io.BytesIO(image_bytes))
image.save("generated_image.png")
