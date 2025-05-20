from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)  # ← ここが name だとエラーになる

# OpenAIのAPIキーを環境変数から読み込む
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is missing'}), 400

    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいプロのWebマーケターです。"},
                {"role": "user", "content": f"以下のページをSEOの観点で診断してください：\n{text}"}
            ]
        )
        comment = response['choices'][0]['message']['content']
        return jsonify({'result': comment})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
