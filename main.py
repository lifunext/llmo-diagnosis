import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# OpenAI APIキーを環境変数から読み込み
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    print("✅ 受信データ:", data)  # デバッグ用ログ
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is missing'}), 400

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        html = requests.get(url, headers=headers).text
    except Exception as e:
        print("❌ HTML取得エラー:", e)
        return jsonify({'error': 'Failed to fetch HTML', 'detail': str(e)}), 500

    try:
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいプロのWebマーケターです。"},
                {"role": "user", "content": "このページを分析してコメントしてください：\n" + text}
            ]
        )

        comment = response['choices'][0]['message']['content']
        return jsonify({'result': comment})

    except Exception as e:
        print("❌ GPTエラー:", e)
        return jsonify({'error': 'Failed to generate comment', 'detail': str(e)}), 500

if __name__ == '__main__':
    app.run()
