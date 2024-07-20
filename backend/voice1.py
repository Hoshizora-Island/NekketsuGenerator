import requests
import os
import time
from googletrans import Translator
import tokens

# Hugging FaceのAPI URLと認証トークン
API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
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
japanese_prompt = "怒っている"

# Google Translateを使用して日本語を英語に翻訳
translator = Translator()
translation = translator.translate(japanese_prompt, src='ja', dest='en')
english_prompt = translation.text
print(f"Translated prompt: {english_prompt}")

# 音声生成
audio_bytes = query({
    "inputs": english_prompt,
})

# 音声データの保存
if audio_bytes:
    try:
        # 保存先のフォルダとファイル名の設定
        folder = r"C:\Users\User\Desktop\NekketsuGenerator\backend\voices"
        if not os.path.exists(folder):
            os.makedirs(folder)

        # プロンプトからファイル名を生成
        safe_prompt = english_prompt.replace(" ", "_").replace("!", "").replace("?", "")  # ファイル名として不適切な文字を置換
        file_name = f"{safe_prompt}.wav"  # 音声ファイルの拡張子を設定
        file_path = os.path.join(folder, file_name)

        # 音声データの保存
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        
        print(f"Audio saved successfully as {file_path}.")
    except Exception as e:
        print(f"Audio processing error: {e}")
else:
    print("No audio data received.")