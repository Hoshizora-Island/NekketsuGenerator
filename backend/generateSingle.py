import requests
import io
from PIL import Image
import os
import time
from googletrans import Translator
import tokens

# Hugging FaceのAPI URLと認証トークン
TEXT_GEN_API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"
IMAGE_GEN_API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": f"Bearer {tokens.getToken('HF_TOKEN')}"}

def query(api_url, payload):
    while True:
        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 503:
            error_info = response.json()
            print(f"Model is still loading. Estimated time: {error_info.get('estimated_time', 'unknown')} seconds. Retrying in 60 seconds...")
            time.sleep(60)  # 60秒待機してから再試行
        elif response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None
        else:
            return response.json() if api_url == TEXT_GEN_API_URL else response.content

def generate_text(prompt):
    # テキスト生成
    text_gen_payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 2.0  # 温度パラメータを2.0に設定
        }
    }
    text_gen_response = query(TEXT_GEN_API_URL, text_gen_payload)
    if text_gen_response:
        return text_gen_response[0]['generated_text'].split()[0]
    else:
        return "デフォルト"

def main():
    # ランダムな単語を生成するためのプロンプト
    prompt = "Generate a random single word:"
    
    # テキスト生成
    generated_text = generate_text(prompt)
    print(f"Generated text: {generated_text}")

    # Google Translateを使用して日本語を英語に翻訳（必要な場合）
    translator = Translator()
    translation = translator.translate(generated_text, src='ja', dest='en')
    english_prompt = translation.text
    print(f"Translated prompt: {english_prompt}")

    # 画像生成
    image_gen_payload = {
        "inputs": english_prompt,
        "parameters": {
            "max_split_size_mb": 512  # メモリ管理オプションを設定
        }
    }
    image_bytes = query(IMAGE_GEN_API_URL, image_gen_payload)

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

if __name__ == "__main__":
    main()

