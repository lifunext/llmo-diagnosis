from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)

# OpenAI APIキーを環境変数から取得
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/fetch', methods=['POST'])
def fetch():
    # JSONデータからURLを取得
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is missing'}), 400

    try:
        # HTML取得＆テキスト抽出
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        # OpenAI APIを使って診断コメント生成
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいプロのWebマーケターです。"},
                {"role": "user", "content": f"以下のページをSEOの観点で診断してください：\n{text}"}
            ]
        )

        comment = response['choices'][0]['message']['content']

        # 結果返却
        return jsonify({'result': comment})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
