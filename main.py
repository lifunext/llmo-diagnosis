from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)

# 環境変数から OpenAI API キーを読み込む
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        response = openai.ChatCompletion.create(
            model="gpt-4o",  # GPT-4o モデルを使用（アクセス可能なら）
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいWebマーケターです。ページ構成・見出し・UX改善などの観点からコメントしてください。"},
                {"role": "user", "content": f"以下のWebページをSEOの観点で診断してください：\n{text}"}
            ]
        )

        comment = response['choices'][0]['message']['content']
        return jsonify({"comment": comment})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
