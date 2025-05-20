from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import os

app = Flask(__name__)

# OpenAIのAPIキーを環境変数から読み込み
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/fetch', methods=['POST'])
def fetch():
    # Makeから受け取ったURLを取得
    data = request.get_json()
    url = data.get('url')

    # URLがない場合は400エラーを返す
    if not url:
        return jsonify({'error': 'URL is missing'}), 400

    try:
        # HTMLを取得して本文抽出
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        # OpenAIに診断リクエスト送信
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいプロのWebマーケターです。"},
                {"role": "user", "content": f"以下のページをSEOの観点で診断してください：\n{text}"}
            ]
        )

        comment = response['choices'][0]['message']['content']

        # 診断結果を返す
        return jsonify({'result': comment})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
