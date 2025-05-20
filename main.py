from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# ★OpenAI APIキーをここに直書き
openai.api_key = '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'

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')
    
    try:
        # HTML取得とテキスト抽出
        html = requests.get(url, timeout=5).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        # GPTに送信して評価コメントを生成
        prompt = f"以下のページ内容を要約し、改善提案を含めたフィードバックをください：\n\n{text[:2000]}"  # 長すぎ防止
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは優秀なマーケティングコンサルタントです。"},
                {"role": "user", "content": prompt}
            ]
        )

        feedback = response['choices'][0]['message']['content']

        return jsonify({"feedback": feedback})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
