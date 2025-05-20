from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)

# OpenAI APIキーを環境変数から読み込む
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # WebページのHTMLを取得
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        short_text = text[:2000]  # トークン削減のために先頭2,000文字だけ使用

        # OpenAI GPT-4oを使って診断コメントを生成
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいWebマーケターです。"},
                {"role": "user", "content": f"以下のWebページをSEOの観点で診断してください：\n{short_text}"}
            ]
        )

        comment = response['choices'][0]['message']['content']
        return jsonify({"comment": comment})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
