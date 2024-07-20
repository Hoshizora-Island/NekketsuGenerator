import requests
import io
from PIL import Image
import os
import time
from googletrans import Translator
import tokens

#https://huggingface.co/runwayml/stable-diffusion-v1-5

# Hugging FaceのAPI URLと認証トークン
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {tokens.getToken('HF_TOKEN')}"}

def query(payload):
    while True:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 503:
            error_info = response.json()
            print(f"Model is still loading. Estimated time: {error_info.get('estimated_time', 'unknown')} seconds. Retrying in 60 seconds...")
            time.sleep(60)  # 60秒待機してから再試行
        elif response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None
        else:
            return response.content

# 日本語のテキストプロンプトの設定
japanese_prompt = "マラソンを世界最速で完走しました！"

# Google Translateを使用して日本語を英語に翻訳
translator = Translator()
translation = translator.translate(japanese_prompt, src='ja', dest='en')
english_prompt = translation.text
print(f"Translated prompt: {english_prompt}")

# 画像生成
image_bytes = query({
    "inputs": english_prompt,
})

# 画像の読み込みと保存
if image_bytes:
    try:
        # 画像の読み込み
        image = Image.open(io.BytesIO(image_bytes))

        # 保存先のフォルダとファイル名の設定
        folder = r"C:\Users\User\Desktop\NekketsuGenerator\backend\images"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # プロンプトからファイル名を生成
        safe_prompt = english_prompt.replace(" ", "_").replace("!", "").replace("?", "")  # ファイル名として不適切な文字を置換
        file_name = f"{safe_prompt}.png"
        file_path = os.path.join(folder, file_name)

        # 画像の保存
        image.save(file_path)
        print(f"Image saved successfully as {file_path}.")
    except Exception as e:
        print(f"Image processing error: {e}")
else:
    print("No image data received.")

