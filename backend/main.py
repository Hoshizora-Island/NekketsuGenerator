from flask import Flask, Response, request
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
import tokens
import torch
import re

app = Flask(__name__)

login(token=tokens.getToken("HF_TOKEN"))

model = AutoModelForCausalLM.from_pretrained("HuggingFaceH4/zephyr-7b-alpha")
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-alpha")

config = {
    "max_new_tokens": 200,
    "temperature": 0.7,
    "top_p": 0.9,
    "do_sample": True,
}

@app.route("/")
def index():
    return {"message": "hello"}

@app.route("/getTextFervor", methods=["POST"])
def getTextFervor():
    req = request.json
    try:
        messages = [
            {
                "role": "system",
                "content": "あなたは文章の熱血度合いを評価するアシスタントです。熱血とは、熱い血潮、血がわきたつような激しい情熱、熱烈な意気込みを意味します。入力された文章がどのくらい熱血かを0～100で評価してください。必ず日本語を使用してください。必ず次のコードブロック内のフォーマットと同じ形式で１回出力してください。##value: 評価した値を数字のみで入力 ##reason: 理由を日本語で入力",
            },
            {
                "role": "user",
                "content": req.get("text")
            },
        ]

        inputs = tokenizer(
            tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True),
            return_tensors="pt",
        )

        outputs = model.generate(
            **inputs,
            **config,
        )

        result = str(tokenizer.decode(outputs[0], skip_special_tokens=True))
        result = result.replace("\n", "")
        result = re.split(r"<\|(?:system|user|assistant)\|>", result)[1:]

        result = result[2].replace(" ", "")
        result = result.split("##")
        result = result[1:]
        value = int(result[0].split(":")[1])
        reason = str(result[1].split(":")[1])

        return {"value": value, "reason": reason}
    
    except Exception:
        return Response(status=400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3030, debug=True)